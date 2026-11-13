"""As-reported borrowing adoption and disjoint Total Debt calculations; offline only."""
from copy import deepcopy
from dataclasses import replace
from decimal import Decimal as D
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from zipfile import ZipFile

from scripts import loan_review_pipeline as pipeline
from scripts import review_workflow as workflow
from scripts.loan_review_contract import METRICS, Status, ContractError, calculate_fact, validate_report
from scripts.loan_review_sources import prepare_source_inputs
from scripts.review_cloud import ReviewCloud
from scripts.review_outputs import report_payload
from test_loan_review_sources import request_fixture, entry, extract, rows_of, supplement
from test_loan_review_contract import source_fact


def sources(values, mode='annual', extra_entries=None):
    request=request_fixture(mode)
    tags={}
    for concept,value in values.items():
        records=[]
        for period in request['periods']:
            date=period['end'];quarter=period['quarter']
            records.append(entry(value=value*1000000,start=None,end=date,
                accn='0000000001-26-000001',filed='2026-02-01',form='10-Q' if quarter else '10-K'))
        tags[concept]={'units':{'USD':records}}
    if extra_entries:
        for tag,records in extra_entries.items():tags[tag]['units']['USD']+=records
    return request,extract(tags)


def run(values, mode='annual', supplements=(), extra_entries=None):
    request,financial=sources(values,mode,extra_entries)
    bundle=prepare_source_inputs(request,rows_of(financial),supplements)
    report,acceptance=pipeline.report_from_source_bundle(bundle)
    return request,financial,bundle,report,acceptance


class TotalDebtTests(unittest.TestCase):
    def test_current_plus_noncurrent_in_both_modes(self):
        for mode in ('annual','quarterly'):
            *_,report,_=run({'DebtCurrent':30,'LongTermDebtNoncurrent':200},mode)
            for p in report.periods:
                f=report.facts['total_debt:'+p.role]
                self.assertEqual(f.value,D(230));self.assertEqual(f.status,Status.CALCULATED)
                self.assertEqual(f.formula_id,'TOTAL-DEBT-v1')
                self.assertEqual(f.input_ids,('input:short_term_debt:'+p.role,'input:long_term_debt:'+p.role))
                self.assertIn('As-reported',f.basis)
            pipeline.validate_arithmetic(report)

    def test_three_components_preserve_current_portion_and_do_not_add_aggregate(self):
        *_,report,_=run({'ShortTermBorrowings':10,'LongTermDebtCurrent':20,
                         'LongTermDebtNoncurrent':200,'LongTermDebt':220})
        f=report.facts['total_debt:fy_t'];self.assertEqual(f.value,D(230))
        current=report.facts['input:short_term_debt:fy_t']
        self.assertEqual(current.value,D(30));self.assertEqual(current.formula_id,'CURRENT-DEBT-v1')
        self.assertNotIn('input:long_term_debt_including_current:fy_t',f.input_ids)

    def test_long_term_aggregate_route_excludes_current_portion_once(self):
        *_,report,_=run({'ShortTermBorrowings':10,'LongTermDebtCurrent':20,'LongTermDebt':220})
        f=report.facts['total_debt:fy_t'];self.assertEqual(f.value,D(230))
        self.assertEqual(f.input_ids,('input:short_term_borrowings:fy_t','input:long_term_debt_including_current:fy_t'))
        self.assertNotIn('input:current_maturities_debt:fy_t',f.input_ids)

    def test_reported_total_is_preferred_over_components(self):
        *_,report,_=run({'DebtAndCapitalLeaseObligations':250,'DebtCurrent':30,'LongTermDebtNoncurrent':200})
        f=report.facts['total_debt:fy_t'];self.assertEqual(f.value,D(250));self.assertEqual(f.status,Status.SOURCED)
        self.assertEqual(f.original_value,D(250000000));self.assertEqual(f.original_scale,D(1))
        self.assertEqual(f.input_ids,());self.assertIn('DebtAndCapitalLeaseObligations',f.basis)

    def test_explicit_zero_is_usable_but_missing_is_not_zero(self):
        *_,report,_=run({'ShortTermBorrowings':0,'LongTermDebt':220})
        self.assertEqual(report.facts['total_debt:fy_t'].value,D(220))
        *_,report,_=run({'LongTermDebt':220})
        self.assertIsNone(report.facts['total_debt:fy_t'].value)
        *_,report,_=run({'Liabilities':500,'LiabilitiesCurrent':50})
        self.assertIsNone(report.facts['total_debt:fy_t'].value)
        self.assertEqual(report.facts['total_debt:fy_t'].status,Status.MISSING)

    def test_finance_lease_aliases_adopt_reported_carrying_amounts(self):
        *_,report,_=run({'ShortTermBorrowings':10,'LongTermDebtAndFinanceLeaseObligationsCurrent':20,
                         'LongTermDebtAndFinanceLeaseObligationsNoncurrent':200})
        self.assertEqual(report.facts['total_debt:fy_t'].value,D(230))
        self.assertIn('lease scope',report.facts['total_debt:fy_t'].basis)
        self.assertIn('FinanceLease',report.facts['input:long_term_debt:fy_t'].basis)

    def test_verified_supplement_total_accepts_different_definition_text(self):
        payload=supplement(metric='total_debt',value='250')
        record=payload['records'][0]
        record.update(period_kind='instant',start=None,definition='Borrowings per debt note, net of issuance costs',basis='Carrying value as reported')
        *_,report,_=run({},supplements=[payload])
        f=report.facts['total_debt:fy_t'];self.assertEqual(f.value,D(250));self.assertEqual(f.status,Status.SOURCED)
        self.assertIn('Borrowings per debt note',f.basis)
        self.assertEqual(report.facts['net_worth:fy_t'].status if 'net_worth:fy_t' in report.facts else report.facts['input:net_worth:fy_t'].status,Status.MISSING)

    def test_explicit_principal_basis_is_labelled_and_not_mixed_with_carrying_values(self):
        payload=supplement(metric='total_debt',value='250')
        payload['records'][0].update(period_kind='instant',start=None,definition='Principal per debt schedule',basis='Principal amount')
        *_,report,_=run({},supplements=[payload])
        self.assertEqual(report.facts['total_debt:fy_t'].value,D(250))
        self.assertIn('As-reported principal amount',report.facts['total_debt:fy_t'].basis)
        payload=supplement(metric='long_term_debt',value='220')
        payload['records'][0].update(period_kind='instant',start=None,definition='Noncurrent loan principal',basis='Principal amount')
        *_,report,_=run({'DebtCurrent':30},supplements=[payload])
        self.assertIsNone(report.facts['total_debt:fy_t'].value)
        self.assertIn('mix principal',report.facts['total_debt:fy_t'].reason)

    def test_negative_borrowing_is_not_automatically_adopted(self):
        *_,report,_=run({'DebtAndCapitalLeaseObligations':-50})
        self.assertIsNone(report.facts['total_debt:fy_t'].value)
        self.assertIn('Negative borrowing',report.facts['total_debt:fy_t'].reason)

    def test_conflicting_full_routes_are_not_silently_selected(self):
        *_,report,_=run({'DebtCurrent':30,'LongTermDebtNoncurrent':200,
                         'ShortTermBorrowings':10,'LongTermDebt':240})
        f=report.facts['total_debt:fy_t'];self.assertIsNone(f.value)
        self.assertIn('routes disagree',f.reason)

    def test_cutoff_versions_currency_and_dates_remain_enforced(self):
        request,financial=sources({'DebtCurrent':30,'LongTermDebtNoncurrent':200})
        # Another non-amended version disagrees for the exact date.
        records=deepcopy(financial)
        new=extract({'DebtCurrent':{'units':{'USD':[entry(40000000,start=None)]}}})
        records['balance_sheet']+=new['balance_sheet']
        report,_=pipeline.report_from_source_bundle(prepare_source_inputs(request,rows_of(records)))
        self.assertIsNone(report.facts['total_debt:fy_t'].value)
        # A future version is excluded rather than replacing the historical one.
        new=extract({'DebtCurrent':{'units':{'USD':[entry(99000000,start=None,filed='2027-02-01',accn='0000000001-27-000001')]}}})
        records=deepcopy(financial);records['balance_sheet']+=new['balance_sheet']
        report,_=pipeline.report_from_source_bundle(prepare_source_inputs(request,rows_of(records)))
        self.assertEqual(report.facts['total_debt:fy_t'].value,D(230))
        # An EUR value is not implicitly converted or added to USD debt.
        new=extract({'DebtCurrent':{'units':{'EUR':[entry(30000000,start=None)]}}})
        records=deepcopy(financial);records['balance_sheet']+=new['balance_sheet']
        report,_=pipeline.report_from_source_bundle(prepare_source_inputs(request,rows_of(records)))
        self.assertIsNone(report.facts['total_debt:fy_t'].value)

    def test_nonoverlap_and_period_lineage_are_revalidated(self):
        *_,report,_=run({'ShortTermBorrowings':10,'LongTermDebt':220,'LongTermDebtCurrent':20})
        f=report.facts['total_debt:fy_t']
        bad=replace(f,input_ids=('input:current_maturities_debt:fy_t','input:long_term_debt_including_current:fy_t'))
        with self.assertRaisesRegex(ContractError,'CALC-02'):
            validate_report(replace(report,facts={**report.facts,f.id:bad}),expected_mode=report.mode)
        bad=replace(f,input_ids=('input:short_term_borrowings:fy_t_minus_1','input:long_term_debt_including_current:fy_t'))
        with self.assertRaisesRegex(ContractError,'CALC-03'):
            validate_report(replace(report,facts={**report.facts,f.id:bad}),expected_mode=report.mode)

    def test_total_leverage_consumes_the_new_total_debt_fact(self):
        *_,report,_=run({'DebtCurrent':30,'LongTermDebtNoncurrent':200})
        report=source_fact(report,'ltm_ebitda:fy_t',D(50))
        report=source_fact(report,'ebitda_basis:fy_t','Synthetic EBITDA basis')
        for fid in ('ltm_ebitda:fy_t','ebitda_basis:fy_t'):
            report=replace(report,facts={**report.facts,fid:replace(report.facts[fid],basis='Synthetic EBITDA basis')})
        report=pipeline.calculate_report(report)
        f=report.facts['total_leverage:fy_t']
        self.assertEqual(f.value,D('4.6'))
        self.assertEqual(f.input_ids,('total_debt:fy_t','ltm_ebitda:fy_t'))
        self.assertEqual(f.basis,'Synthetic EBITDA basis')
        pipeline.validate_arithmetic(report)

    def test_new_debt_policy_keeps_net_worth_gate_and_debt_ratio_definition(self):
        *_,report,_=run({'DebtCurrent':30,'LongTermDebtNoncurrent':200,'StockholdersEquity':100})
        self.assertIsNone(report.facts['debt_ratio:fy_t'].value)
        self.assertEqual(METRICS['debt_ratio'].definition,'Total Liabilities / Net Worth')
        approval=report.evidence[report.decisions['DEC-02']]
        self.assertEqual(approval.document_date.isoformat(),'2026-11-07')
        self.assertIn('as-reported',approval.content)


class DebtOutputsTests(unittest.TestCase):
    def test_workflow_roundtrip_and_saved_formulas(self):
        request,financial=sources({'ShortTermBorrowings':10,'LongTermDebtCurrent':20,'LongTermDebtNoncurrent':200})
        snapshot=dict(schema_version=1,entity=request['entity'],cik=request['cik'],financial_facts=financial)
        with tempfile.TemporaryDirectory() as tmp:
            result=workflow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,
                output_dir=tmp,excel=False,commentary_mode='off')
            self.assertEqual(result['status'],'draft',result)
            report,_=pipeline.validate_saved_artifacts(tmp)
            self.assertEqual(report.facts['total_debt:fy_t'].value,D(230))
            for filename in ('report.md','dashboard.html'):
                text=Path(tmp,filename).read_text();self.assertIn('Total Debt 口徑',text)
            payload=json.loads(Path(tmp,'report.json').read_text())
            self.assertEqual(payload['facts']['total_debt:fy_t']['formula_id'],'TOTAL-DEBT-v1')
            self.assertEqual(payload['facts']['input:short_term_debt:fy_t']['formula_id'],'CURRENT-DEBT-v1')

    @unittest.skipUnless(os.environ.get('REVIEW_EXCEL_TEST')=='1','Enable bundled Excel verification')
    def test_real_excel_uses_the_same_addition_chain(self):
        for mode in ('annual','quarterly'):
            request,financial=sources({'ShortTermBorrowings':10,'LongTermDebtCurrent':20,'LongTermDebtNoncurrent':200},mode)
            snapshot=dict(schema_version=1,entity=request['entity'],cik=request['cik'],financial_facts=financial)
            with tempfile.TemporaryDirectory() as tmp:
                result=workflow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,
                    output_dir=tmp,commentary_mode='off')
                self.assertEqual(result['stages']['excel'],'passed',result)
                audit=json.loads(Path(tmp,'excel_validation.json').read_text());self.assertTrue(audit['passed'])
                with ZipFile(Path(tmp,'loan_review.xlsx')) as archive:
                    xml=archive.read('xl/worksheets/sheet2.xml').decode()
                self.assertIn('+',xml);self.assertIn('lease scope',xml)


if __name__=='__main__':unittest.main()
