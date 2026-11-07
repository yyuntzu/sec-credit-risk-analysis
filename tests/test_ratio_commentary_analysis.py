"""Synthetic balance-sheet attribution, exact endpoints and shared-output regressions."""
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

from scripts import formal_commentary as commentary
from scripts import loan_review_pipeline as pipeline
from scripts import review_workflow as flow
from scripts.filing_commentary_sources import extract_filing_sections, document_observations
from scripts.loan_review_contract import Fact, METRICS, Status
from scripts.loan_review_sources import prepare_source_inputs, balance_sheet_observations, parse_request
from scripts.mda_commentary import generate_formal_commentary
from scripts.ratio_commentary_analysis import build_ratio_analysis, comparison_roles
from scripts.review_outputs import report_payload
from test_loan_review_contract import fixture, source_fact
from test_loan_review_sources import request_fixture, extract, entry, rows_of


def ratio_report(mode='quarterly'):
    report = fixture(mode)
    approval = replace(report.evidence['calendar'], id='approval', kind='definition', content='Synthetic definition approval')
    report = replace(report, evidence={**report.evidence, 'approval':approval}, decisions={'DEC-01':'approval','DEC-02':'approval'})
    for role, ca, cl, qa, liabilities, worth in zip(comparison_roles(report),
            (2302,2937),(874,1190),(1268,1751),(4011,4605),(2074,2104)):
        period = next(p for p in report.periods if p.role == role)
        for metric, value in [('current_assets',ca),('current_liabilities',cl),('quick_assets',qa),
                              ('total_liabilities',liabilities),('net_worth',worth)]:
            fid='input:'+metric+':'+role
            f=Fact(fid,metric,role,Status.MISSING,None,'money',METRICS[metric].definition,
                   None,period.end,report.entity,report.scope,currency=report.currency,
                   reason='Synthetic source only',period_kind='instant')
            report=replace(report,facts={**report.facts,fid:f})
            report=source_fact(report,fid,D(value))
        for metric,value in [('current_ratio',D(ca)/D(cl)),('quick_ratio',D(qa)/D(cl)),
                             ('debt_ratio',D(liabilities)/D(worth))]:
            report=source_fact(report,metric+':'+role,value)
    return pipeline.build_narratives(report)


def observations(report):
    data=[]
    for tag,values in [('CashAndCashEquivalentsAtCarryingValue',(220,312)),
                       ('AccountsReceivableNetCurrent',(1048,1439)),('AccountsPayableCurrent',(512,815)),
                       ('InventoryNet',(986,1137))]:
        for role,value in zip(comparison_roles(report),values):
            period=next(p for p in report.periods if p.role==role)
            data.append(dict(id=tag+':'+role,entity=report.entity,scope=report.scope,tag=tag,namespace='us-gaap',
                value=str(value),unit='USD',scale='1000000',start=None,end=period.end.isoformat(),period_kind='instant',
                status='sourced',source_id='SYNTHETIC-FILING',version='v1',document_date='2026-01-01',locator='table cell'))
    return data


def filing_html(prior='2024-12-31',current='2025-06-30',cik='1',dimension='',fmt='num-dot-decimal'):
    header='<ix:header>'
    for ctx,endpoint in [('old',prior),('new',current)]:
        header+=f'<xbrli:context id="{ctx}"><xbrli:entity><xbrli:identifier>{cik}</xbrli:identifier>{dimension}</xbrli:entity><xbrli:period><xbrli:instant>{endpoint}</xbrli:instant></xbrli:period></xbrli:context>'
    header+='<xbrli:unit id="usd"><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unit></ix:header>'
    table='<table><tr><th>Consolidated Balance Sheets in millions</th></tr>'
    for label,tag,old,new in [('Total current assets','AssetsCurrent',2302,2937),
                            ('Accounts payable','AccountsPayableCurrent',512,815),
                            ('Total current liabilities','LiabilitiesCurrent',874,1190),
                            ('Total assets','Assets',6085,6709)]:
        table+='<tr><td>'+label+'</td>'
        for context,value in [('old',old),('new',new)]:
            table+=f'<td><ix:nonFraction name="us-gaap:{tag}" contextRef="{context}" unitRef="usd" scale="6" format="ixt:{fmt}">{value:,}</ix:nonFraction></td>'
        table+='</tr>'
    table+='</table>'
    debt='<h2>6) DEBT</h2><p>'+('Synthetic only. Proceeds from new notes and the new loan repaid the old term loan. '*4)+'</p>'
    next_note='<h2>7) INCOME TAXES</h2><p>'+('Unrelated tax details. '*20)+'</p>'
    return header+table+debt+next_note


class RatioAnalysisTests(unittest.TestCase):
    def test_both_modes_include_both_liquidity_directions_and_exact_endpoints(self):
        for mode in ('annual','quarterly'):
            report=ratio_report(mode)
            n=next(n for t in report.tables if t.spec.key=='ratios' for n in t.narratives if n.topic=='liquidity')
            self.assertIn('263.39%',n.text);self.assertIn('246.81%',n.text)
            self.assertIn('145.08%',n.text);self.assertIn('147.14%',n.text)
            self.assertIn('下降',n.text);self.assertIn('上升',n.text)
            roles=comparison_roles(report)
            self.assertEqual(n.period_roles,roles)
            self.assertEqual(set(n.fact_ids),{m+':'+r for m in ('current_ratio','quick_ratio') for r in roles})
            original=report_payload(report)
            pack=build_ratio_analysis(report,observations(report))
            self.assertEqual(pack['ratios']['current_ratio']['relative_growth'],'denominator_faster')
            self.assertEqual(pack['ratios']['quick_ratio']['relative_growth'],'numerator_faster')
            self.assertEqual(pack['ratios']['debt_ratio']['numerator']['change'],'594')
            self.assertEqual(pack['ratios']['debt_ratio']['denominator']['change'],'30')
            payable=next(c for c in pack['components'] if c['field_name']=='accounts_payable')
            self.assertEqual(payable['change'],'303')
            self.assertEqual(payable['sources'][roles[1]][0]['version'],'v1')
            self.assertEqual(report_payload(report),original)

    def test_missing_quick_ratio_does_not_discard_current_or_invent_zero(self):
        report=ratio_report();key='quick_ratio:current_interim'
        report=replace(report,facts={**report.facts,key:replace(report.facts[key],status=Status.MISSING,value=None,original_value=None,original_scale=None,reason='No verified quick definition')})
        report=pipeline.build_narratives(report)
        n=next(n for t in report.tables if t.spec.key=='ratios' for n in t.narratives if n.topic=='liquidity')
        self.assertIn('Current ratio',n.text);self.assertIn('Quick ratio',n.reason)
        self.assertNotIn('Quick ratio',n.text)
        self.assertEqual(build_ratio_analysis(report)['ratios']['quick_ratio']['status'],'missing')

    def test_conflicts_partial_coverage_units_and_wrong_dates(self):
        report=ratio_report();rows=observations(report)
        conflicting=dict(rows[-1],id='changed-version',value='999',version='v2')
        wrong_date=dict(rows[0],id='wrong-date',end='2024-06-30',value='9999')
        wrong_currency=dict(rows[1],id='wrong-unit',unit='EUR')
        pack=build_ratio_analysis(report,rows+[conflicting,wrong_date,wrong_currency])
        inventory=next(c for c in pack['components'] if c['field_name']=='inventory')
        self.assertIsNone(inventory['change'])
        self.assertTrue(any('Conflicting' in x for x in pack['limitations']))
        self.assertTrue(any('currency mismatch' in x for x in pack['limitations']))
        self.assertEqual(set(pack['component_coverage'].values()),{'partial_not_reconciled'})
        self.assertEqual(next(c for c in pack['components'] if c['field_name']=='cash')['change'],'92')

    def test_only_explicit_amendment_supersedes_same_concept(self):
        report=ratio_report();rows=observations(report)
        corrected=dict(rows[-1],id='amended',value='1200',version='amended',document_date='2026-02-01',filing_type='10-Q/A')
        pack=build_ratio_analysis(report,rows+[corrected])
        self.assertEqual(next(c for c in pack['components'] if c['field_name']=='inventory')['change'],'214')
        same_day=dict(corrected,id='same-day-conflict',filing_type='10-Q',value='1300')
        pack=build_ratio_analysis(report,rows+[corrected,same_day])
        self.assertIsNone(next(c for c in pack['components'] if c['field_name']=='inventory')['change'])
        corrected['filing_type']='10-Q'
        pack=build_ratio_analysis(report,rows+[corrected])
        self.assertIsNone(next(c for c in pack['components'] if c['field_name']=='inventory')['change'])

    def test_source_total_mismatch_is_explicit_and_never_changes_fact(self):
        report=ratio_report();row=dict(observations(report)[-1],tag='AssetsCurrent',value='9999')
        pack=build_ratio_analysis(report,[row])
        check=next(c for c in pack['source_total_checks'] if c['metric']=='current_assets' and c['period_role']=='current_interim')
        self.assertEqual(check['status'],'conflict')
        self.assertEqual(report.facts['input:current_assets:current_interim'].value,D(2937))

    def test_selected_components_reconcile_and_overlapping_subtotals_are_not_summed(self):
        report=ratio_report();rows=observations(report)
        for template,value in [(rows[-2],48),(rows[-1],49)]:
            rows.append(dict(template,id='prepaid:'+template['end'],tag='PrepaidExpenseAndOtherAssetsCurrent',value=str(value)))
        pack=build_ratio_analysis(report,rows)
        self.assertEqual(pack['component_coverage']['current_assets'],'matched_selected_lines')
        checks=[c for c in pack['component_reconciliations'] if c['group']=='current_assets']
        self.assertTrue(all(c['unexplained_residual']=='0' for c in checks))
        rows.append(dict(rows[-1],id='overlapping-other',tag='OtherAssetsCurrent',value='1'))
        pack=build_ratio_analysis(report,rows)
        check=next(c for c in pack['component_reconciliations'] if c['group']=='current_assets' and c['period_role']=='current_interim')
        self.assertEqual(check['status'],'overlapping_components')
        self.assertIsNone(check['selected_sum'])

    def test_model_gets_supporting_facts_and_computed_analysis(self):
        report=ratio_report();pack=build_ratio_analysis(report,observations(report))
        response=MagicMock(stop_reason='end_turn',content=[MagicMock(type='text',text='{"claims":[]}')])
        with patch('scripts.mda_commentary.anthropic.Anthropic') as api:
            api.return_value.messages.create.return_value=response
            generate_formal_commentary(report,[{'id':'synthetic-document'}],ratio_analysis=pack)
            params=api.return_value.messages.create.call_args.kwargs
        payload=json.loads(params['messages'][0]['content'])
        self.assertEqual(payload['ratio_analysis'],pack)
        self.assertIn('quick_ratio:current_interim',payload['facts'])
        self.assertIn('input:net_worth:current_interim',payload['facts'])
        self.assertIn('gross proceeds',params['system'])
        self.assertIn('balance-sheet',params['system'])

    def test_raw_source_details_survive_source_selection_without_new_contract_metrics(self):
        request=request_fixture();financial=extract({'AccountsPayableCurrent':{'units':{'USD':[
            entry(815000000,start=None)]}}})
        bundle=prepare_source_inputs(request,rows_of(financial))
        rows=balance_sheet_observations(bundle)
        self.assertEqual(rows[0]['field_name'],'accounts_payable')
        self.assertEqual(rows[0]['value'],'815000000')
        later=deepcopy(bundle);later['request']['as_of']='2025-12-31'
        self.assertEqual(balance_sheet_observations(later),[])


class FilingSectionsTests(unittest.TestCase):
    def test_extracts_table_and_bounded_debt_note_with_context_and_scale(self):
        sections=extract_filing_sections(filing_html(),'0000000001',{'2024-12-31','2025-06-30'})
        by_kind={s['section']:s for s in sections}
        self.assertEqual(set(by_kind),{'Balance Sheet','Debt Note'})
        self.assertIn('repaid the old term loan',by_kind['Debt Note']['text'])
        self.assertNotIn('Unrelated tax',by_kind['Debt Note']['text'])
        row=next(o for o in by_kind['Balance Sheet']['observations'] if o['tag']=='AccountsPayableCurrent' and o['end']=='2025-06-30')
        self.assertEqual(row['value'],'815');self.assertEqual(row['scale'],'1000000')

    def test_wrong_entity_dimensions_unsupported_numeric_formats_and_other_tables_are_not_adopted(self):
        for html in [filing_html(cik='2'),filing_html(dimension='<xbrli:segment>Subsidiary</xbrli:segment>'),filing_html(fmt='num-comma-decimal')]:
            sections=extract_filing_sections(html,'0000000001',{'2024-12-31','2025-06-30'})
            self.assertEqual(sections[0]['observations'],[])
        html=filing_html()+'<table><ix:nonFraction name="us-gaap:AccountsPayableCurrent" contextRef="new" unitRef="usd">99999</ix:nonFraction></table>'
        sections=extract_filing_sections(html,'0000000001',{'2024-12-31','2025-06-30'})
        self.assertFalse(any(o['value']=='99999' for o in sections[0]['observations']))

    def test_no_arbitrary_document_fallback(self):
        self.assertEqual(extract_filing_sections('<p>Unrelated text.</p>','0000000001',{'2025-06-30'}),[])

    def test_real_collector_covers_two_requested_dates_and_uses_section_locators(self):
        request=request_fixture('quarterly');report,_,_=parse_request(request)
        client=MagicMock(rate_limit=0)
        client.get_company_submissions.return_value=dict(cik=1,filings={'recent':dict(
            accessionNumber=['0000000001-25-000001'],filingDate=['2025-08-01'],reportDate=['2025-06-30'],form=['10-Q'],primaryDocument=['quarter.htm'])})
        html=filing_html();client.session.get.return_value=MagicMock(text=html,content=html.encode())
        docs=commentary.collect_sec_documents(client,request)
        commentary.validate_documents(report,request,docs)
        bs=next(d for d in docs if d['section']=='Balance Sheet')
        self.assertEqual({p['role'] for p in bs['periods']},{'latest_fy_end','current_interim'})
        claim=dict(table='ratios',topic='debt_ratio',status='supported',explanation='新借款與償還舊貸款需合併考量。',
            citations=[dict(document_id=docs[1]['id'],quote='Synthetic only.')])
        result=commentary.apply_commentary(report,request,docs,[claim])
        n=next(n for t in result.tables if t.spec.key=='ratios' for n in t.narratives if n.topic=='debt_ratio')
        self.assertIn('#Debt Note:char=',result.evidence[n.evidence_ids[0]].locator)
        self.assertEqual(result.facts,report.facts)
        row=deepcopy(bs);row['observations'][0]['end']='2025-08-03'
        with self.assertRaisesRegex(ValueError,'date differs'):commentary.validate_documents(report,request,[row])


class RatioWorkflowTests(unittest.TestCase):
    def run_snapshot(self, mode, tmp, excel=False):
        request=request_fixture(mode)
        date=request['periods'][-1]['end']
        previous=request['periods'][-2]['end']
        html=filing_html(prior=previous,current=date)
        sections=extract_filing_sections(html,request['cik'],{previous,date})
        docs=[dict(id=s['section'],entity=request['entity'],cik=request['cik'],scope=request['scope'],
            source_id='SYNTHETIC-ONLY',version='v1',document_date='2026-02-01',source_url='fixture://filing',
            periods=[{k:p[k] for k in ('role','start','end')} for p in request['periods'][-2:]],**s) for s in sections]
        explanation='流動比率與速動比率分別檢視資產及負債明細；應付帳款增加，借款須連同償還舊債解讀。'
        claims=[dict(table='ratios',topic=topic,status='supported',explanation=explanation,
            citations=[dict(document_id=d['id'],quote=d['text'][:100]) for d in docs]) for topic in ('liquidity','debt_ratio')]
        snapshot=dict(schema_version=1,entity=request['entity'],cik=request['cik'],financial_facts={k:[] for k in ('income_statement','balance_sheet','cash_flow')})
        with patch('scripts.formal_commentary.collect_sec_documents') as network:
            result=flow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,
                commentary=dict(documents=docs,claims=claims),excel=excel,output_dir=tmp)
            network.assert_not_called()
        return result,explanation

    def test_both_modes_save_analysis_and_share_text_with_json_markdown_html_and_cloud_payload(self):
        for mode in ('annual','quarterly'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
                result,text=self.run_snapshot(mode,tmp)
                self.assertEqual(result['status'],'draft',result)
                analysis=json.loads(Path(tmp,'ratio_commentary_analysis.json').read_text())
                self.assertEqual(analysis['mode'],mode)
                self.assertEqual(next(c for c in analysis['components'] if c['field_name']=='accounts_payable')['change'],'303')
                report,_=pipeline.validate_saved_artifacts(tmp)
                for filename in ('report.md','dashboard.html','commentary.json'):
                    self.assertIn(text,Path(tmp,filename).read_text())
                self.assertEqual(commentary.commentary_payload(report),json.loads(Path(tmp,'commentary.json').read_text()))
                self.assertIn('ratio_commentary_analysis_path',result['outputs'])

    @unittest.skipUnless(os.environ.get('REVIEW_EXCEL_TEST')=='1','Enable bundled Excel verification')
    def test_ratio_analysis_text_reaches_real_excel(self):
        with tempfile.TemporaryDirectory() as tmp:
            result,text=self.run_snapshot('quarterly',tmp,excel=True)
            self.assertEqual(result['stages']['excel'],'passed',result)
            with ZipFile(Path(tmp,'loan_review.xlsx')) as archive:
                xml=' '.join(archive.read(n).decode() for n in archive.namelist() if n.endswith('.xml'))
            self.assertIn(text,xml)


if __name__=='__main__':unittest.main()
