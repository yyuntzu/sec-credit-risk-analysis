"""SQL commentary adapters, strict migrations and document provenance fixtures."""
from copy import deepcopy
from decimal import Decimal, localcontext
import json
import unittest

from scripts import dbt_shadow as shadow
from scripts.review_workflow import restore_report
from scripts.ratio_commentary_analysis import build_ratio_analysis
from scripts.filing_commentary_sources import document_observations
from scripts.warehouse_commentary import assemble_analysis,build_narratives
from scripts.shadow_commentary import compare_commentary
from test_dbt_shadow import rich_bundle,SHADOW_RUN_ID
from test_loan_review_sources import supplement
from scripts.loan_review_sources import prepare_source_inputs


def commentary_fixture(mode='annual',*,adversarial=False):
    original=rich_bundle(mode)
    fields=set(supplement()['records'][0])
    current='fy_t' if mode=='annual' else 'current_interim'
    old='fy_t_minus_1' if mode=='annual' else 'latest_fy_end'
    periods={p['role']:p for p in original['request']['periods']}
    updates=dict(current_assets='120',current_liabilities='40',quick_assets='90',net_worth='220',
                 total_liabilities='110',total_assets='330')
    envelope=supplement();records=[]
    for item in original['evidence'].values():
        row={k:item[k] for k in fields}
        if row['end']==periods[current]['end'] and row['metric'] in updates:
            row['value']=updates[row['metric']]
        records.append(row)
    envelope['records']=records
    bundle=prepare_source_inputs(original['request'],[],[envelope])
    documents=[]
    for role in (old,current):
        is_current=role==current
        values={'CashAndCashEquivalentsAtCarryingValue':'999' if is_current else '10',
                'AccountsReceivableNetCurrent':'105' if is_current else '80',
                'AccountsPayableCurrent':'25' if is_current else '20',
                'OtherLiabilitiesCurrent':'15' if is_current else '10',
                'AssetsCurrent':'120' if is_current else '90','LiabilitiesCurrent':'40' if is_current else '30',
                'Assets':'330' if is_current else '300','Liabilities':'110' if is_current else '100',
                'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest':'220' if is_current else '200'}
        if adversarial and is_current:
            values.update(PrepaidExpenseAndOtherAssetsCurrent='1',OtherAssetsCurrent='2')
        documents.append(dict(id='bs:'+role,entity=bundle['entity'],cik=bundle['cik'],scope=bundle['scope'],
            source_id='SYNTHETIC-BALANCE-SHEET',version='v1',document_date='2026-09-01',source_url='fixture://balance-sheet',
            section='Balance Sheet',filing_type='10-K',periods=[{k:periods[role][k] for k in ('role','start','end')}],
            text='Synthetic balance sheet, not real borrower data.',observations=[dict(tag=tag,value=value,unit='USD',scale='1000000',end=periods[role]['end'],locator=tag) for tag,value in values.items()]))
    amendment=deepcopy(documents[-1]);amendment.update(id='bs:amendment',version='v2',document_date='2026-09-02',filing_type='10-K' if adversarial else '10-K/A')
    amendment['observations']=[dict(tag='CashAndCashEquivalentsAtCarryingValue',value='15',unit='USD',scale='1000000',end=periods[current]['end'],locator='cash-amended')]
    if adversarial:
        amendment['observations'].append(dict(tag='AssetsCurrent',value='999',unit='EUR',scale='1000000',end=periods[current]['end'],locator='foreign-currency'))
    documents.append(amendment)
    return bundle,documents


def fake_commentary_rows(baseline,metadata,documents=()):
    """Adapter fixture only; cannot substitute for execution of dbt SQL."""
    report=restore_report(baseline)
    pack=build_ratio_analysis(report,document_observations(documents),documents)
    bindings={k:metadata[k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version')}
    rows=[]
    def add(kind,key,item):
        rows.append(dict(bindings,record_kind=kind,record_id=key,payload=json.dumps(item),publication_eligible=False))
    for key,item in pack['ratios'].items(): add('ratio',key,item)
    for item in pack['source_total_checks']: add('total_check',item['metric']+':'+item['period_role'],item)
    for item in pack['component_reconciliations']: add('component_reconciliation',item['group']+':'+item['period_role'],item)
    for group in ('current_assets','current_liabilities'): add('coverage',group,dict(status=pack['component_coverage'][group]))
    for index,text in enumerate(pack['limitations']): add('limitation',str(index),dict(text=text))
    for index,item in enumerate(pack['components']):
        item=deepcopy(item);sources=item.pop('sources')
        item.update(position=index+1,before_sources_json=json.dumps(sources[pack['period_roles'][0]]),after_sources_json=json.dumps(sources[pack['period_roles'][1]]))
        add('component',item['concept'],item)
    metrics={f.metric for f in report.facts.values() if f.unit!='text' and ':pct:' not in f.id}
    for kind in ('income','balance'):
        roles=pack['period_roles'] if kind=='balance' or report.mode.value=='annual' else ('prior_interim','current_interim')
        for metric in sorted(metrics):
            facts=[report.facts.get(metric+':'+r) or report.facts.get('input:'+metric+':'+r) for r in roles]
            before,after=[f.value if f else None for f in facts]
            with localcontext() as ctx:
                ctx.prec=256
                change=after-before if before is not None and after is not None else None
                growth=change/before if change is not None and before>0 else None
            add('comparison',kind+':'+metric,dict(kind=kind,metric=metric,unit=next(f.unit for f in facts if f),
                before_role=roles[0],after_role=roles[1],before_fact_id=facts[0].id if facts[0] else None,
                after_fact_id=facts[1].id if facts[1] else None,before_status=facts[0].status.value if facts[0] else None,
                after_status=facts[1].status.value if facts[1] else None,
                before=str(before) if before is not None else None,after=str(after) if after is not None else None,
                change=str(change) if change is not None else None,growth=str(growth) if growth is not None else None,
                status='available' if change is not None else 'missing',
                direction='not_comparable' if change is None else 'unchanged' if change==0 else 'increased' if change>0 else 'decreased'))
    return rows


class ShadowCommentaryTests(unittest.TestCase):
    def setUp(self):
        self.bundle=rich_bundle()
        self.metadata,_,self.baseline,_=shadow.prepare_run(self.bundle,run_id=SHADOW_RUN_ID)
        self.bindings={k:self.metadata[k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version')}
        self.rows=fake_commentary_rows(self.baseline,self.metadata)
        facts=[dict(f,fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in self.baseline['facts'].values()]
        self.facts=shadow.compare_facts(self.baseline,facts,expected_run_id=SHADOW_RUN_ID)

    def test_adapter_and_shadow_agree_without_approving_precision(self):
        result=compare_commentary(self.bundle,self.baseline,self.rows,self.facts,bindings=self.bindings)
        self.assertEqual(result['mismatches'],0)
        self.assertFalse(result['publication_eligible'])
        report=restore_report(self.baseline)
        pack,pairs=assemble_analysis(report,self.rows,bindings=self.bindings)
        self.assertEqual(pack['ratios']['current_ratio']['before'],'3')
        narrated=build_narratives(report,pairs)
        self.assertIn('Current ratio',next(n for t in narrated.tables if t.spec.key=='ratios' for n in t.narratives if n.topic=='liquidity').text)

    def test_exact_delta_defect_is_never_called_precision(self):
        for kind,key in (('comparison','income:revenue'),('ratio','current_ratio')):
            rows=deepcopy(self.rows)
            row=next(r for r in rows if r['record_kind']==kind and r['record_id']==key)
            payload=json.loads(row['payload']);payload['change']='999';row['payload']=json.dumps(payload)
            result=compare_commentary(self.bundle,self.baseline,rows,self.facts,bindings=self.bindings)
            self.assertGreater(result['mismatches'],0)

    def test_growth_difference_is_unapproved_and_foreign_or_incomplete_lineage_is_rejected(self):
        rows=deepcopy(self.rows)
        row=next(r for r in rows if r['record_kind']=='ratio')
        payload=json.loads(row['payload']);payload['growth']='0.00000000000000000000000000000000000001';row['payload']=json.dumps(payload)
        result=compare_commentary(self.bundle,self.baseline,rows,self.facts,bindings=self.bindings)
        self.assertEqual(result['mismatches'],0);self.assertEqual(result['numeric_differences'],1)
        for bad in ([dict(self.rows[0],scope='foreign')]+self.rows[1:], self.rows+[self.rows[0]],self.rows[:-1]):
            with self.assertRaises(ValueError): assemble_analysis(restore_report(self.baseline),bad,bindings=self.bindings)

    def test_quarterly_income_and_balance_pairs_remain_distinct(self):
        metadata,_,baseline,_=shadow.prepare_run(rich_bundle('quarterly'),run_id=SHADOW_RUN_ID)
        rows=fake_commentary_rows(baseline,metadata)
        _,pairs=assemble_analysis(restore_report(baseline),rows,bindings={k:metadata[k] for k in self.bindings})
        self.assertEqual(pairs['income:revenue']['before_role'],'prior_interim')
        self.assertEqual(pairs['balance:current_assets']['before_role'],'latest_fy_end')

    def test_bad_document_is_rejected_before_warehouse_access(self):
        with self.assertRaisesRegex(ValueError,'fields'):
            shadow.prepare_run(self.bundle,commentary_documents=[{'id':'bad'}])

    def test_hand_calculated_component_fixture_and_adversarial_selection(self):
        for adversarial in (False,True):
            bundle,documents=commentary_fixture(adversarial=adversarial)
            metadata,_,baseline,_=shadow.prepare_run(bundle,run_id=SHADOW_RUN_ID,commentary_documents=documents)
            pack,_=assemble_analysis(restore_report(baseline),fake_commentary_rows(baseline,metadata,documents),
                bindings={k:metadata[k] for k in self.bindings},documents=documents)
            self.assertEqual(pack['ratios']['current_ratio']['numerator']['change'],'30')
            self.assertEqual(pack['ratios']['quick_ratio']['relative_growth'],'numerator_faster')
            cash=next(c for c in pack['components'] if c['field_name']=='cash')
            if not adversarial:
                self.assertEqual(cash['change'],'5')
                self.assertEqual(pack['component_coverage']['current_assets'],'matched_selected_lines')
                self.assertEqual(cash['sources']['fy_t'][0]['version'],'v2')
            else:
                self.assertIsNone(cash['after'])
                check=next(c for c in pack['component_reconciliations'] if c['group']=='current_assets' and c['period_role']=='fy_t')
                self.assertEqual(check['status'],'overlapping_components')
                self.assertTrue(any('currency mismatch' in value for value in pack['limitations']))


if __name__=='__main__':unittest.main()
