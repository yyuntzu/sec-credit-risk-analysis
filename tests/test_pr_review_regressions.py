"""PR #1 defects: offline regression coverage; no live services or credentials."""
from copy import deepcopy
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from jinja2 import Environment
import sqlglot
from sqlglot.optimizer.qualify import qualify

from scripts import agent_runner as runner
from scripts import loan_review_pipeline as pipeline
from scripts import review_workflow as flow
from scripts.loan_review_contract import Evidence, Fact, METRICS, Status, _dates
from scripts.loan_review_sources import parse_request, prepare_source_inputs
from scripts.review_cloud import ReviewCloud
from scripts.review_outputs import report_payload
from test_loan_review_contract import complete_fixture, source_fact
from test_loan_review_pipeline import nexstar
from test_loan_review_sources import request_fixture, entry, extract, rows_of
from test_review_integration import snapshot

ROOT = Path(__file__).resolve().parents[1]


def accepted_fixture():
    """Explicit canonical sources and reviewed equations, rather than PASS flags."""
    report = complete_fixture('annual')
    report = replace(report, decisions={**report.decisions, 'DEC-08': 'approval', 'DEC-09': 'approval'})
    checks = []
    for period in report.periods:
        role = period.role
        for metric, value in [('beginning_cash', 100), ('ending_cash', 100), ('cash_change', 0),
                              ('cfo', 10), ('cfi', -5), ('cff', -5), ('cash_fx', 0), ('cash_other', 0),
                              ('total_assets', 100), ('total_liabilities', 60), ('net_worth', 40)]:
            fid = metric + ':' + role
            if fid not in report.facts:
                start, end = _dates(metric, period)
                fact = Fact(fid, metric, role, Status.MISSING, None, 'money', METRICS[metric].definition,
                            start, end, report.entity, report.scope, currency=report.currency,
                            reason='Not populated', period_kind='instant' if start is None else 'duration')
                report = replace(report, facts={**report.facts, fid: fact})
            report = source_fact(report, fid, D(value))
        for kind, reported, components in [
                ('cash_bridge', 'ending_cash', ('beginning_cash', 'cfo', 'cfi', 'cff', 'cash_fx', 'cash_other')),
                ('balance_sheet_equation', 'total_assets', ('total_liabilities', 'net_worth'))]:
            terms = [{'fact_id': m + ':' + role, 'coefficient': 1} for m in components]
            binding = dict(kind=kind, period_role=role, terms=terms, reported_fact_id=reported + ':' + role,
                           currency=report.currency, scale=str(report.scale), tolerance='0')
            eid = 'review:' + kind + ':' + role
            evidence = Evidence(eid, report.entity, report.scope, 'synthetic-bridge', 'v1', date(2026, 1, 1),
                                'fixture://complete-bridge', 'review', (role,), json.dumps(binding))
            report = replace(report, evidence={**report.evidence, eid: evidence})
            ids = [t['fact_id'] for t in terms] + [binding['reported_fact_id']]
            eids = sorted({e for fid in ids for e in report.facts[fid].evidence_ids}) + [eid]
            checks.append({**binding, 'status': 'matched', 'calculated_value': D(100),
                           'reported_value': D(100), 'difference': D(0), 'evidence_ids': eids})
    return report, pipeline.acceptance_result(report, checks)


class PeriodComparabilityTests(unittest.TestCase):
    def test_same_quarter_label_cannot_hide_three_vs_nine_months(self):
        request = request_fixture('quarterly')
        request['periods'][1].update(end='2024-03-31', ltm_start='2023-04-01', quarter=3)
        request['periods'][3].update(end='2025-09-30', ltm_start='2024-10-01', quarter=3)
        with self.assertRaisesRegex(ValueError, 'not comparable'):
            parse_request(request)
        with patch.object(runner, 'SECEdgarClient') as sec, tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'not comparable'):
                flow.run_review('SYNTHETIC-ONLY', request, output_dir=tmp)
            sec.assert_not_called()
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_valid_calendar_ytd_passes(self):
        parse_request(request_fixture('quarterly'))

    def test_invalid_quarter_length_blocked_even_if_both_match(self):
        request = request_fixture('quarterly')
        for pos in (1, 3):
            request['periods'][pos]['quarter'] = 1
        with self.assertRaisesRegex(ValueError, 'not comparable'):
            parse_request(request)


class ReconciliationTests(unittest.TestCase):
    def test_independently_valid_bridges_can_pass_acceptance(self):
        report, acceptance = accepted_fixture()
        self.assertTrue(acceptance['substantive_data_ready'], acceptance['acceptance_blockers'])
        self.assertTrue(all(c['verified'] for c in acceptance['reconciliations']))
        with tempfile.TemporaryDirectory() as tmp:
            pipeline.write_report_artifacts(report, acceptance, tmp)
            _, saved = pipeline.validate_saved_artifacts(tmp)
            self.assertTrue(saved['final_report_accepted'])

    def test_original_forged_pass_with_nonzero_difference_is_rejected(self):
        report, acceptance = accepted_fixture()
        checks = deepcopy(acceptance['reconciliations'])
        for c in checks:
            c.update(calculated_value=0, reported_value=1000000, difference=-1000000, status='matched')
        result = pipeline.acceptance_result(report, checks)
        self.assertFalse(result['substantive_data_ready'])
        self.assertFalse(any(c['verified'] for c in result['reconciliations']))

    def test_unrelated_fact_evidence_is_not_canonical_bridge_evidence(self):
        report, acceptance = accepted_fixture()
        checks = deepcopy(acceptance['reconciliations'])
        for c in checks:
            c['evidence_ids'] = ['source:revenue:' + c['period_role'], 'approval']
        self.assertFalse(pipeline.acceptance_result(report, checks)['substantive_data_ready'])

    def test_tolerance_cannot_exceed_original_precision(self):
        report, acceptance = accepted_fixture()
        c = deepcopy(acceptance['reconciliations'][0]); c['tolerance'] = '999999'
        result = pipeline.verify_reconciliation(report, c)
        self.assertFalse(result['verified'])
        self.assertIn('precision', result['verification_error'])

    def test_review_must_bind_the_equation_and_tolerance(self):
        report, acceptance = accepted_fixture()
        c = deepcopy(acceptance['reconciliations'][0]); c['tolerance'] = '0.01'
        self.assertFalse(pipeline.verify_reconciliation(report, c)['verified'])
        c = deepcopy(acceptance['reconciliations'][0]); c['terms'][0]['coefficient'] = -1
        self.assertFalse(pipeline.verify_reconciliation(report, c)['verified'])

    def test_canonical_source_change_invalidates_a_previous_pass(self):
        report, acceptance = accepted_fixture()
        report = source_fact(report, 'cfo:fy_t_minus_3', D(11))
        self.assertFalse(pipeline.acceptance_result(report, acceptance['reconciliations'])['substantive_data_ready'])

    def test_rounding_difference_uses_actual_values_and_reviewed_precision(self):
        report, acceptance = accepted_fixture()
        c = deepcopy(acceptance['reconciliations'][1])
        report = source_fact(report, c['reported_fact_id'], D('100.01'))
        c.update(tolerance='0.01', reported_value=D('100.01'), difference=D('-0.01'), status='within_precision')
        eid = next(e for e in c['evidence_ids'] if e.startswith('review:'))
        binding = {key: c[key] for key in ('kind','period_role','terms','reported_fact_id','currency','scale','tolerance')}
        evidence = replace(report.evidence[eid], content=json.dumps(binding))
        report = replace(report, evidence={**report.evidence, eid: evidence})
        result = pipeline.verify_reconciliation(report, c)
        self.assertTrue(result['verified'], result)
        c['tolerance'] = '-1'
        self.assertFalse(pipeline.verify_reconciliation(report, c)['verified'])


class CovenantCompatibilityTests(unittest.TestCase):
    def execute_model(self, full_ttm):
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        self.addCleanup(db.close)
        db.create_function('SAFE_DIVIDE', 2, lambda a,b: a/b if a is not None and b not in (None,0) else None)
        db.executescript('''
            create table stg_covenant_terms(ticker,covenant_name,covenant_type,threshold_value,threshold_unit,severity_level,rationale);
            create table fct_credit_kpis(ticker,period_end,filed_date,is_full_ttm,net_leverage_ratio,total_leverage_ratio,
                interest_coverage_ratio,dscr,current_ratio,debt_ratio,cfo_to_debt_ratio,coverage_flag);
        ''')
        for name in ('current_ratio','total_leverage_ratio','interest_coverage_ratio','dscr'):
            db.execute('insert into stg_covenant_terms values (?,?,?,?,?,?,?)', ('TEST',name,'min',1,'x','HIGH','fixture'))
        db.execute('insert into fct_credit_kpis values (?,?,?,?,?,?,?,?,?,?,?,?)',
                   ('TEST','2025-12-31','2026-02-01',full_ttm,2,2,2,2,2,2,2,'OK'))
        text = (ROOT/'references/dbt/models/model/marts/fct_covenant_status.sql').read_text()
        sql = Environment().from_string(text).render(config=lambda **k:'', ref=lambda name:name)
        sql = sqlglot.transpile(sql, read='bigquery', write='sqlite')[0]
        return [dict(r) for r in db.execute(sql)]

    def test_incomplete_ttm_keeps_rows_and_point_in_time_evaluation(self):
        rows = self.execute_model(False)
        self.assertEqual(len(rows), 4)
        for row in rows:
            if row['covenant_name'] == 'current_ratio':
                self.assertEqual(row['compliance_status'], 'COMPLIANT')
            else:
                self.assertEqual(row['compliance_status'], 'NO_DATA')
                self.assertIsNone(row['headroom_absolute'])

    def test_complete_ttm_preserves_existing_evaluations(self):
        self.assertTrue(all(r['compliance_status']=='COMPLIANT' for r in self.execute_model(True)))

    def test_legacy_kpis_are_not_replaced_by_unconditional_null(self):
        for name in ('int_ttm_metrics','int_leverage_ratios','int_coverage_ratios','int_liquidity_ratios'):
            text = (ROOT/f'references/dbt/models/model/intermediate/{name}.sql').read_text().lower()
            self.assertNotIn('cast(null as float64)', text)
        text = (ROOT/'references/dbt/models/model/intermediate/int_ttm_metrics.sql').read_text()
        self.assertIn('verified_legacy_ttm_interval as is_full_ttm', text)

    def test_existing_income_model_still_computes_legacy_ebitda(self):
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        self.addCleanup(db.close)
        columns = ['ticker','filing_type','accession_number','filed_date','period_end','period_start','period_days','field_name','value']
        db.execute('create table raw_income_statement (' + ','.join(columns) + ')')
        for metric, value in [('revenue',100000000),('operating_income',20000000),('da',3000000)]:
            db.execute('insert into raw_income_statement values (?,?,?,?,?,?,?,?,?)',
                       ('TEST','10-K','fixture','2026-02-01','2025-12-31','2025-01-01',364,metric,value))
        text=(ROOT/'references/dbt/models/model/staging/stg_income_statement.sql').read_text()
        sql=Environment().from_string(text).render(config=lambda **k:'',source=lambda a,b:b)
        tree=qualify(sqlglot.parse_one(sql,read='bigquery'),dialect='bigquery',schema={'raw_income_statement':{c:'TEXT' for c in columns}})
        row=dict(db.execute(tree.sql(dialect='sqlite')).fetchone())
        self.assertEqual(row['ebitda_m'],23)
        self.assertEqual(row['revenue_m'],100)


class PublicationTests(unittest.TestCase):
    def test_offline_dbt_manifest_enforces_all_formal_tests(self):
        executable=Path(__import__('sys').executable).with_name('dbt')
        if not executable.is_file():self.skipTest('dbt unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            run=subprocess.run([__import__('sys').executable,str(executable),'--warn-error','parse',
                '--project-dir',str(ROOT/'references/dbt'),'--profiles-dir',str(ROOT/'references/dbt'),
                '--target-path',tmp+'/target','--log-path',tmp+'/logs','--no-partial-parse'],
                capture_output=True,text=True,timeout=60)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            manifest=json.loads(Path(tmp,'target/manifest.json').read_text())
            tests=[n for n in manifest['nodes'].values() if n['resource_type']=='test' and 'formal_review' in n['original_file_path']]
            self.assertGreaterEqual(len(tests),7)
            self.assertTrue(all(n['config']['severity']=='error' for n in tests))

    def test_unaccepted_report_cannot_publish_even_when_flags_are_forged(self):
        report, acceptance = pipeline.report_from_source_bundle(prepare_source_inputs(request_fixture(), []))
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        with patch.object(cloud, 'write') as write:
            with self.assertRaisesRegex(ValueError, 'independently verified'):
                cloud.publish('a'*32, report.entity, report_payload(report), {**acceptance,
                    'final_report_accepted':True, 'technical_validation_passed':True, 'rendered_validation_passed':True})
            write.assert_not_called()

    def test_dbt_failure_is_fatal_with_warning_promotion(self):
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        with patch.dict(os.environ, {'DBT_EXECUTABLE':'dbt'}), patch('scripts.review_cloud.subprocess.run',
                side_effect=[MagicMock(returncode=0), MagicMock(returncode=1, stderr='integrity failure', stdout='')]) as run:
            with self.assertRaisesRegex(RuntimeError, 'publish/test failed'):
                cloud.dbt('publish')
            self.assertIn('--warn-error', run.call_args.args[0])

    def test_accepted_report_cloud_failure_cannot_be_success(self):
        report, acceptance = accepted_fixture()
        cloud = MagicMock(); cloud.stage_bundle.side_effect = lambda run_id, entity, bundle: bundle
        cloud.publish.side_effect = RuntimeError('dbt integrity failed')
        with tempfile.TemporaryDirectory() as tmp, patch.object(flow, 'report_from_source_bundle', return_value=(report, acceptance)):
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(),
                                     output_dir=tmp, excel=False, execution='cloud', cloud=cloud)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['cloud_status'], 'failed')
        cloud.publish.assert_called_once()

    def test_accepted_report_can_publish_after_all_checks(self):
        report, acceptance = accepted_fixture()
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        acceptance = {**acceptance, 'final_report_accepted':True, 'rendered_validation_passed':True}
        with patch.object(cloud,'write') as write, patch.object(cloud,'dbt') as dbt:
            cloud.publish('a'*32, report.entity, report_payload(report), acceptance)
            write.assert_called_once(); dbt.assert_called_once_with('publish')

    def test_delivery_failure_blocks_publication_of_accepted_report(self):
        report, acceptance = accepted_fixture()
        cloud = MagicMock(); cloud.stage_bundle.side_effect = lambda run_id, entity, bundle: bundle
        with tempfile.TemporaryDirectory() as tmp, patch.object(flow, 'report_from_source_bundle', return_value=(report, acceptance)), \
                patch.object(flow, 'export_excel', side_effect=RuntimeError('export failed')):
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(),
                                     output_dir=tmp, execution='cloud', cloud=cloud)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['cloud_status'], 'blocked_delivery')
        cloud.publish.assert_not_called()


class HttpCompatibilityTests(unittest.TestCase):
    def test_legacy_batch_and_single_request_shapes_remain_supported(self):
        if runner.app is None: self.skipTest('Flask unavailable')
        with runner.app.test_client() as client, patch.object(runner, 'analyze_ticker',
                return_value={'status':'success','final_report_accepted':False}) as analyze:
            response = client.post('/run', json={'tickers':['AMZN']})
            self.assertEqual(response.status_code,200);self.assertTrue(response.get_json()['success'])
            self.assertTrue(analyze.call_args.kwargs['legacy_compatibility'])
            self.assertEqual(client.post('/analyze/AMZN',json={}).status_code,200)
            self.assertEqual(client.get('/run').status_code,200)
            self.assertEqual(client.post('/v2/run',json={'tickers':['AMZN']}).status_code,400)
            self.assertEqual(client.post('/v2/analyze/AMZN',json={}).status_code,400)

    def test_legacy_get_still_serves_html(self):
        if runner.app is None: self.skipTest('Flask unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp,'dashboard.html');target.write_text('<h1>Legacy</h1>')
            with runner.app.test_client() as client, patch.object(runner,'analyze_ticker',return_value={'status':'success','html_path':str(target)}):
                response=client.get('/analyze/AMZN')
                self.assertEqual(response.mimetype,'text/html')
                self.assertIn(b'Legacy',response.data)

    def test_legacy_mart_reads_keep_existing_metric_values(self):
        loader=MagicMock(dataset_ref='fixture.raw')
        loader.client.query.return_value.result.return_value=[{'period_end':date(2025,12,31),'ebitda_m':123,'total_debt_m':456}]
        rows=runner.query_legacy_mart('AMZN',loader,annual=True)
        self.assertEqual(rows[0]['ebitda_m'],123);self.assertEqual(rows[0]['total_debt_m'],456)
        self.assertEqual(loader.client.query.call_args.kwargs['job_config'].query_parameters[0].value,'AMZN')


class RestatementTests(unittest.TestCase):
    def prepare(self, entries, as_of=None):
        request=request_fixture()
        if as_of:request['as_of']=as_of
        rows=rows_of(extract({'Revenues':{'units':{'USD':entries}}}))
        return prepare_source_inputs(request,rows)

    def test_latest_amendment_used_and_old_evidence_retained(self):
        bundle=self.prepare([entry(),entry(2000000,accn='0000000001-26-000002',filed='2026-03-01',form='10-K/A')])
        fact=bundle['inputs']['revenue:fy_t']
        self.assertEqual(fact['value'],'2');self.assertEqual(len(fact['candidate_ids']),2)
        self.assertEqual(len(fact['evidence_ids']),1);self.assertEqual(len(fact['superseded_candidate_ids']),1)
        report,_=pipeline.report_from_source_bundle(bundle)
        self.assertEqual(report.facts['revenue:fy_t'].value,D(2))

    def test_future_amendment_does_not_leak_into_as_of(self):
        bundle=self.prepare([entry(),entry(2000000,accn='0000000001-26-000002',filed='2026-03-01',form='10-K/A')], '2026-02-15')
        self.assertEqual(bundle['inputs']['revenue:fy_t']['value'],'1')
        self.assertEqual(len(bundle['excluded']),1)

    def test_nonamended_and_same_date_conflicts_are_not_latest_wins(self):
        for entries in ([entry(),entry(2000000,accn='0000000001-26-000002',filed='2026-03-01')],
                        [entry(form='10-K/A'),entry(2000000,accn='0000000001-26-000002',form='10-K/A')]):
            self.assertEqual(self.prepare(entries)['inputs']['revenue:fy_t']['status'],'conflict')


class ArtifactTests(unittest.TestCase):
    def test_negative_tax_is_regenerated_and_stale_pass_receipt_rejected(self):
        report, acceptance,_,_=nexstar('E-Loan YQYQ-Nexstar Q1.xls','quarterly',1)
        with tempfile.TemporaryDirectory() as tmp:
            pipeline.write_report_artifacts(report,acceptance,tmp)
            pipeline.validate_saved_artifacts(tmp)
            path=Path(tmp,'report.md');text=path.read_text()
            self.assertIn('(7.00)',text)
            path.write_text(text.replace('(7.00)','-7.00'))
            with self.assertRaisesRegex(ValueError,'Stale artifact'):
                pipeline.validate_saved_artifacts(tmp)
            with self.assertRaisesRegex(ValueError,'Stale artifact'):
                flow.export_excel(tmp)

    def test_generated_outputs_and_dependency_links_are_not_tracked(self):
        # Consult the index: cleanup deliberately preserves local artifact copies.
        paths=subprocess.check_output(['git','ls-files','-z','--','outputs/'],cwd=ROOT).decode().split('\0')
        self.assertEqual([p for p in paths if p], [])
        self.assertFalse(any(Path(p).name=='node_modules' for p in paths if p))


if __name__=='__main__':unittest.main()
