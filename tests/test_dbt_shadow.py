"""Contract tests for shadow-only execution. Network tests are explicitly opt-in."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock,patch

from scripts import dbt_shadow as shadow
from scripts.loan_review_contract import METRICS
from scripts.loan_review_sources import prepare_source_inputs
from scripts.review_workflow import run_review
from test_loan_review_sources import request_fixture,supplement

ROOT=Path(__file__).resolve().parents[1]
SHADOW_RUN_ID='a'*32


def rich_bundle(mode='annual', *, values_override=None):
    request=request_fixture(mode)
    envelope=supplement()
    records=[]
    # Complete defined direct inputs. DSCR intentionally remains unresolved.
    values=dict(revenue='120',cost_of_revenue='40',gross_profit='80',operating_expense='20',
        operating_income='60',interest_expense='10',pretax_profit='50',income_tax='-5',net_income='55',
        beginning_cash='10',ending_cash='20',cfo='20',cfi='-5',cff='-5',capitalized_interest='2',da='15',
        current_assets='90',current_liabilities='30',quick_assets='60',net_worth='200',
        total_liabilities='100',total_assets='300',cash_fx='0',cash_other='0',total_debt='120')
    values.update(values_override or {})
    for period in request['periods']:
        for metric,value in values.items():
            spec=METRICS[metric]
            rec=deepcopy(envelope['records'][0])
            start=period['start'];end=period['end']
            if spec.period_kind in ('instant','opening'):
                start=None
                if spec.period_kind=='opening':
                    from datetime import date,timedelta
                    end=str(date.fromisoformat(period['start'])-timedelta(days=1))
            rec.update(metric=metric,value=value,definition=spec.definition,basis='',
                start=start,end=end,period_kind='instant' if start is None else 'duration',
                locator=f'{metric}:{period["role"]}',document_date='2026-09-01')
            rec["verification"]["verified_at"]="2026-09-02"
            records.append(rec)
    envelope['records']=records
    return prepare_source_inputs(request,[],[envelope])


class ShadowContractTests(unittest.TestCase):
    def test_plan_contains_no_python_selected_values_and_no_baseline(self):
        bundle=rich_bundle()
        metadata,records,baseline,_=shadow.prepare_run(bundle,run_id='a'*32)
        self.assertEqual(metadata['source_hash'],shadow.digest(bundle))
        self.assertFalse(metadata['precision_approved'])
        slots=[r[2] for r in records if r[0]=='slot']
        self.assertTrue(all('value' not in s and 'status' not in s for s in slots))
        self.assertFalse(any(kind=='baseline' for kind,_,_ in records))
        leverage=next(s for s in slots if s['fact_id']=='total_leverage:fy_t')
        self.assertEqual(leverage['input_ids'],['total_debt:fy_t','ltm_ebitda:fy_t'])
        self.assertGreater(leverage['depth'],1)
        self.assertEqual(len(slots),len(baseline['facts']))

    def test_snapshot_without_complete_ltm_preserves_dates_and_roles(self):
        bundle=rich_bundle('quarterly')
        plans=shadow.prepare_plan(bundle)
        target=next(p for p in plans if p['fact_id']=='revenue_growth:current_interim')
        self.assertEqual(target['input_ids'],['revenue:current_interim','revenue:prior_interim'])
        self.assertNotEqual(str(next(p for p in plans if p['fact_id']=='ltm_ebitda:current_interim')['start']),bundle['request']['periods'][-1]['start'])

    def test_exact_numeric_comparison_never_waives_native_rounding_difference(self):
        _,_,baseline,_=shadow.prepare_run(rich_bundle())
        rows=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in baseline['facts'].values()]
        self.assertEqual(shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID)['mismatches'],0)
        row=next(r for r in rows if r['fact_id']=='interest_coverage:fy_t')
        row['value']=str(Decimal(row['value'])+Decimal('0.0000000000000001'))
        result=shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID)
        self.assertEqual(result['numeric_differences'],1)
        self.assertFalse(result['publication_eligible'])
        self.assertFalse(result['precision_approved'])

    def test_identity_metadata_changes_cannot_pass_if_value_matches(self):
        _,_,baseline,_=shadow.prepare_run(rich_bundle())
        rows=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in baseline['facts'].values()]
        next(r for r in rows if r['fact_id']=='current_ratio:fy_t')['input_ids'].reverse()
        self.assertGreater(shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID)['mismatches'],0)
        with self.assertRaisesRegex(ValueError,'Duplicate warehouse'):
            shadow.compare_facts(baseline,rows+[rows[0]],expected_run_id=SHADOW_RUN_ID)
        self.assertEqual(shadow.compare_facts(baseline,rows[:-1],expected_run_id=SHADOW_RUN_ID)['facts_compared'],len(rows))

    def test_foreign_or_missing_identity_is_rejected_before_values_are_compared(self):
        _,_,baseline,_=shadow.prepare_run(rich_bundle())
        original=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in baseline['facts'].values()]
        for field,foreign in [('run_id','b'*32),('entity','OTHER-BORROWER'),('scope','foreign-scope')]:
            for count in (1,len(original)):
                for value in (foreign,None):
                    with self.subTest(field=field,count=count,value=value):
                        rows=deepcopy(original)
                        for row in rows[:count]:
                            if value is None:
                                row.pop(field)
                            else:
                                row[field]=value
                        with self.assertRaisesRegex(ValueError,'identity mismatch: '+field):
                            shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID)
        self.assertEqual(shadow.compare_facts(baseline,original,expected_run_id=SHADOW_RUN_ID)['equivalent'],len(original))

    def test_identity_failure_marks_the_run_failed_and_retains_audit_files(self):
        bundle=rich_bundle()
        _,_,baseline,_=shadow.prepare_run(bundle)
        warehouse=MagicMock()
        def execute(records,directory):
            metadata=next(value for kind,_,value in records if kind=='metadata')
            rows=[dict(deepcopy(f),fact_id=f['id'],run_id=metadata['run_id']) for f in baseline['facts'].values()]
            rows[0]['run_id']='b'*32 if metadata['run_id']!='b'*32 else 'c'*32
            return rows,[],{}
        warehouse.execute.side_effect=execute
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'shadow'
            with self.assertRaisesRegex(ValueError,'identity mismatch: run_id'):
                shadow.run_shadow(bundle,directory,project='fixture',warehouse=warehouse)
            manifest=json.loads((directory/'shadow_manifest.json').read_text())
            self.assertEqual(manifest['status'],'failed')
            self.assertFalse(manifest['publication_eligible'])
            self.assertFalse((directory/'comparison.json').exists())
            self.assertTrue((directory/'warehouse_facts.json').exists())

    def test_cast_loss_overflow_and_duplicate_records_are_rejected_before_writes(self):
        self.assertEqual(shadow._exact_bignumeric('1.00000000000000000000000000000000000001'),Decimal('1.00000000000000000000000000000000000001'))
        for value in ('1e-39','1e100','NaN','Infinity'):
            with self.assertRaises(ValueError):shadow._exact_bignumeric(value)
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            shadow.validate_records([('slot','x',{}),('slot','x',{})])

    def test_normalization_underflow_and_quantum_loss_are_rejected_before_writes(self):
        for value,scale,quantum in (('1e-33','1','1e-33'),('1e-38','0.1','1e-38'),
                                   ('1','1','1e-33'),('1e38','100','1'),('1','1','1e-39')):
            for kind in ('observation','commentary_observation'):
                with self.subTest(value=value,scale=scale,quantum=quantum,kind=kind),self.assertRaises(ValueError):
                    shadow.validate_records([(kind,'x',dict(unit='USD',value=value,scale=scale,source_quantum=quantum))])
        shadow.validate_records([('observation','x',dict(unit='USD',value='0',scale='1000000',source_quantum='0.01'))])

    def test_prepare_only_is_offline_immutable_and_records_decimal_context(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(shadow,'ShadowWarehouse') as warehouse:
            directory=Path(tmp)/'shadow'
            result=shadow.run_shadow(rich_bundle(),directory,project='fixture',prepare_only=True)
            self.assertEqual(result['status'],'prepared')
            warehouse.assert_not_called()
            self.assertIn('precision',result['baseline_context'])
            with self.assertRaises(FileExistsError):
                shadow.run_shadow(rich_bundle(),directory,project='fixture',prepare_only=True)

    def test_failed_warehouse_retains_manifest_and_source_files(self):
        warehouse=MagicMock();warehouse.execute.side_effect=RuntimeError('SQL test failure')
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'shadow'
            with self.assertRaisesRegex(RuntimeError,'SQL test'):
                shadow.run_shadow(rich_bundle(),directory,project='fixture',warehouse=warehouse)
            result=json.loads((directory/'shadow_manifest.json').read_text())
            self.assertEqual(result['status'],'failed')
            self.assertFalse(result['publication_eligible'])
            self.assertTrue((directory/'baseline.json').exists())

    def test_shadow_mode_requires_cloud_and_never_silently_handles_workbook(self):
        for options in ({'execution':'local'},{'execution':'cloud','source':'workbook'}):
            with self.assertRaisesRegex(ValueError,'dbt-shadow requires'):
                run_review('SYNTHETIC-ONLY',calculation_mode='dbt-shadow',**options)

    def test_kernel_fixture_covers_every_approved_formula_id(self):
        cases=json.loads((ROOT/'tests/fixtures/dbt_shadow/kernel_cases.json').read_text())
        ids={r['formula_id'] for r in cases}
        self.assertEqual(len(ids),21)
        self.assertEqual(len({r['case_id'] for r in cases}),len(cases))
        # Hand calculated signed tax benefit and combined interest denominators.
        self.assertEqual(next(r for r in cases if r['case_id']=='DER-05-signed')['expected'],'60')
        self.assertEqual(next(r for r in cases if r['case_id']=='CF-04-signed')['expected'],'4')


class WorkflowShadowTests(unittest.TestCase):
    def test_shadow_reviews_cannot_be_silently_ignored_in_python_mode(self):
        with self.assertRaisesRegex(ValueError,'shadow_reconciliations requires'):
            run_review('SYNTHETIC-ONLY',shadow_reconciliations={})

    def test_cli_loads_shadow_reviews(self):
        from scripts import review_workflow as flow
        envelope={'schema_version':1,'checks':[],'evidence':{}}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'reviews.json')
            path.write_text(json.dumps(envelope))
            with patch.object(flow,'run_review',return_value={'status':'draft','final_report_accepted':False}) as run, patch('builtins.print'):
                code=flow.cli(['SYNTHETIC-ONLY','--execution','cloud','--calculation-mode','dbt-shadow',
                               '--shadow-reconciliations',str(path)])
            self.assertEqual(code,2)
            self.assertEqual(run.call_args.kwargs['shadow_reconciliations'],envelope)

    def test_requested_shadow_records_differences_without_replacing_report(self):
        from scripts import review_workflow as flow
        from scripts import agent_runner as runner
        bundle=rich_bundle()
        cloud=MagicMock();cloud.project='fixture-project'
        cloud.stage_bundle.side_effect=lambda run_id,entity,bundle:bundle
        result=dict(status='compared',equivalent=100,mismatches=0,numeric_differences=2)
        reviews={'schema_version':1,'checks':[],'evidence':{}}
        with tempfile.TemporaryDirectory() as tmp,patch.object(runner,'prepare_loan_review_source_stage',return_value=bundle),patch.object(shadow,'run_shadow',return_value=result) as compare:
            manifest=flow.run_review('SYNTHETIC-ONLY',bundle['request'],execution='cloud',
                cloud=cloud,output_dir=tmp,excel=False,commentary_mode='off',calculation_mode='dbt-shadow',
                shadow_reconciliations=reviews)
            self.assertEqual(manifest['calculation_mode'],'dbt-shadow')
            self.assertEqual(manifest['shadow_comparison']['numeric_differences'],2)
            self.assertEqual(manifest['status'],'draft')
            compare.assert_called_once()
            self.assertEqual(compare.call_args.kwargs['reconciliations'],reviews)
            cloud.publish.assert_not_called()
            report=json.loads(Path(tmp,'report.json').read_text())
            self.assertEqual(report['facts']['current_ratio:fy_t']['value'],'3')

    def test_shadow_failure_preserves_original_deliverables(self):
        from scripts import review_workflow as flow
        from scripts import agent_runner as runner
        bundle=rich_bundle()
        cloud=MagicMock();cloud.project='fixture-project'
        cloud.stage_bundle.side_effect=lambda run_id,entity,bundle:bundle
        with tempfile.TemporaryDirectory() as tmp,patch.object(runner,'prepare_loan_review_source_stage',return_value=bundle),patch.object(shadow,'run_shadow',side_effect=RuntimeError('test failure')):
            manifest=flow.run_review('SYNTHETIC-ONLY',bundle['request'],execution='cloud',
                cloud=cloud,output_dir=tmp,excel=False,commentary_mode='off',calculation_mode='dbt-shadow')
            self.assertEqual(manifest['status'],'failed')
            self.assertEqual(manifest['stages']['dbt_shadow'],'failed')
            self.assertTrue(Path(tmp,'report.md').exists())
            self.assertTrue(Path(tmp,'dashboard.html').exists())
            cloud.publish.assert_not_called()


def adversarial_bundle():
    from test_loan_review_sources import extract,entry,rows_of
    tags={
        'Revenues':{'units':{'USD':[entry(1000000),entry(1200000,accn='0000000001-26-000002',filed='2026-03-01',form='10-K/A')]}},
        'GrossProfit':{'units':{'USD':[entry(600000),entry(700000,accn='0000000001-26-000003',filed='2026-04-01')]}},
        'NetIncomeLoss':{'units':{'USD':[entry(100000),entry(999000000,accn='0000000001-27-000001',filed='2027-01-01')]}},
        'OperatingIncomeLoss':{'units':{'USD':[entry(500000)],'EUR':[entry(500000)]}},
        'AssetsCurrent':{'units':{'USD':[entry(0,start=None)]}},
        'LiabilitiesCurrent':{'units':{'USD':[entry(300000,start=None)]}},
        'IncomeTaxExpenseBenefit':{'units':{'USD':[entry(-40000)]}},
    }
    na=supplement('quick_assets',None,'not_applicable')
    na['records'][0].update(period_kind='instant',start=None,definition=METRICS['quick_assets'].definition)
    return prepare_source_inputs(request_fixture(),rows_of(extract(tags)),[na])


class ShadowSourceTests(unittest.TestCase):
    def test_adversarial_baseline_fixes_expected_selection_without_using_sql(self):
        bundle=adversarial_bundle()
        _,_,baseline,_=shadow.prepare_run(bundle)
        facts=baseline['facts']
        self.assertEqual(facts['revenue:fy_t']['value'],'1.2')
        self.assertEqual(facts['gross_profit:fy_t']['status'],'conflict')
        self.assertEqual(facts['operating_income:fy_t']['status'],'conflict')
        self.assertEqual(facts['quick_ratio:fy_t']['status'],'not_calculable')
        self.assertEqual(facts['input:quick_assets:fy_t']['status'],'not_applicable')
        self.assertEqual(facts['current_ratio:fy_t']['value'],'0E+1')
        self.assertEqual(facts['net_income:fy_t']['value'],'0.1')
