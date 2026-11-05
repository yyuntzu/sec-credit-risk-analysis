"""Canonical commentary, provenance, presentation, and failure-path regressions."""
from copy import deepcopy
from dataclasses import replace
from datetime import date
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
from scripts.mda_commentary import generate_formal_commentary
from scripts.review_outputs import report_payload, write_dashboard
from scripts.review_cloud import ReviewCloud
from scripts.loan_review_sources import prepare_source_inputs
from test_loan_review_sources import request_fixture, extract, entry, rows_of


def inputs():
    request=request_fixture()
    financial=extract({'Revenues':{'units':{'USD':[
        entry(800000,start='2024-01-01',end='2024-12-31',accn='0000000001-25-000001',filed='2025-02-01'),entry()]}}})
    snapshot=dict(schema_version=1,entity=request['entity'],cik=request['cik'],financial_facts=financial)
    report,acceptance=pipeline.report_from_source_bundle(prepare_source_inputs(request,rows_of(financial)))
    documents=[]
    for role,text,filed in [('fy_t_minus_1','Synthetic fixture only. Revenue reflected lower shipment volume.','2025-02-01'),
                            ('fy_t','Synthetic fixture only. Revenue increased because shipment volume rose.','2026-02-01')]:
        period=next(p for p in request['periods'] if p['role']==role)
        documents.append(dict(id='mda:'+role,entity=report.entity,cik=request['cik'],scope=report.scope,
            source_id='SYNTHETIC-'+role,version='v1',document_date=filed,source_url='fixture://'+role,
            section='MD&A',periods=[{k:period[k] for k in ('role','start','end')}],text=text))
    n=report.tables[0].narratives[0]
    claim=dict(table='income',topic='revenue',status='supported',claim_type='cause',
        explanation='營收增加主要來自出貨量提升；此為合成測試示例。',fact_ids=list(n.fact_ids),period_roles=list(n.period_roles),
        citations=[dict(document_id=d['id'],quote=d['text']) for d in documents],
        review=dict(verified_by='Synthetic reviewer',verified_at='2026-02-02',method='checked_against_source'))
    return request,snapshot,report,acceptance,dict(documents=documents,claims=[claim])


class EvidenceCommentaryTests(unittest.TestCase):
    def test_model_summary_is_canonical_and_provenance_is_retained(self):
        request,_,report,_,bundle=inputs()
        result=commentary.apply_commentary(report,request,**bundle)
        n=result.tables[0].narratives[0]
        self.assertEqual(n.text,bundle['claims'][0]['explanation'])
        self.assertFalse(commentary.is_reviewed(result,'income',n))
        self.assertEqual(result.facts,report.facts)
        self.assertEqual(len([e for e in result.evidence.values() if e.kind=='passage']),2)
        self.assertFalse(any(g['table']=='income' and g['topic']=='revenue' for g in commentary.commentary_gaps(result)))

    def test_commentary_gaps_are_diagnostics_not_financial_blockers(self):
        _,_,report,acceptance,_=inputs()
        self.assertEqual(report.tables[0].narratives[0].claim_type,'comparison')
        self.assertFalse(acceptance['commentary_complete'])
        self.assertFalse(acceptance['commentary_required_for_acceptance'])
        self.assertFalse(any('commentary' in b for b in acceptance['acceptance_blockers']))

    def test_missing_commentary_does_not_block_otherwise_accepted_financial_report(self):
        from test_pr_review_regressions import accepted_fixture
        report,acceptance=accepted_fixture()
        tables=tuple(replace(t,narratives=tuple(replace(n,status='missing',text='',reason='分析尚未取得')
            for n in t.narratives)) for t in report.tables)
        report=replace(report,tables=tables)
        acceptance=pipeline.acceptance_result(report,acceptance['reconciliations'])
        self.assertEqual(acceptance['acceptance_blockers'],[])
        self.assertTrue(acceptance['substantive_data_ready'])
        self.assertFalse(acceptance['commentary_complete'])
        cloud=ReviewCloud(project='fixture-project',dataset='raw',client=MagicMock())
        with patch.object(cloud,'write') as write,patch.object(cloud,'dbt'):
            cloud.publish('a'*32,report.entity,report_payload(report),{**acceptance,'final_report_accepted':True,'rendered_validation_passed':True})
        write.assert_called_once()

    def test_model_summary_is_visible_without_manual_review(self):
        request,_,report,_,bundle=inputs();bundle['claims'][0].pop('review')
        result=commentary.apply_commentary(report,request,**bundle)
        display=commentary.narrative_display(result,'income',result.tables[0].narratives[0])
        self.assertIn('模型分析',display['text']);self.assertNotIn('待覆核',display['text'])
        self.assertFalse(display['reviewed'])
        self.assertFalse(pipeline.acceptance_result(result)['commentary_complete'])

    def test_invalid_borrower_dates_scope_and_periods_are_rejected(self):
        request,_,report,_,original=inputs()
        for field,value in [('entity','OTHER'),('cik','0000000002'),('scope','parent'),('document_date','2027-01-01')]:
            bundle=deepcopy(original);bundle['documents'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                commentary.apply_commentary(report,request,**bundle)
        bundle=deepcopy(original);bundle['documents'][0]['periods'][0]['start']='2024-02-01'
        with self.assertRaisesRegex(ValueError,'period coverage'):
            commentary.apply_commentary(report,request,**bundle)

    def test_canonical_growth_allows_percentage_display_rounding(self):
        request,_,report,_,bundle=inputs()
        bundle['claims'][0]['explanation']='營收增加25.00%，主因出貨量提升。'
        report=commentary.apply_commentary(report,request,**bundle)
        self.assertIn('25.00%',report.tables[0].narratives[0].text)

    def test_summary_is_not_rejected_by_quote_numeric_or_model_id_matching(self):
        request,_,report,_,original=inputs()
        for mutation in ('quote','facts','coverage','number'):
            bundle=deepcopy(original);claim=bundle['claims'][0]
            if mutation=='quote':claim['citations'][0]['quote']='A paraphrased reference that is not a verbatim quote.'
            if mutation=='facts':claim['fact_ids']=['model-did-not-return-canonical-ids']
            if mutation=='coverage':claim['citations']=claim['citations'][1:]
            if mutation=='number':claim['explanation']='Model summary mentions 999999; financial tables are not changed.'
            with self.subTest(mutation=mutation):
                result=commentary.apply_commentary(report,request,**bundle)
                self.assertEqual(result.tables[0].narratives[0].text,claim['explanation'])
                self.assertEqual(result.facts,report.facts)
                for eid in result.tables[0].narratives[0].evidence_ids:
                    self.assertTrue(any(result.evidence[eid].content in d['text'] for d in bundle['documents']))

    def test_current_period_document_alone_is_sufficient(self):
        request,_,report,_,bundle=inputs()
        bundle['documents']=bundle['documents'][1:]
        bundle['claims'][0]['citations']=bundle['claims'][0]['citations'][1:]
        result=commentary.apply_commentary(report,request,**bundle)
        n=result.tables[0].narratives[0]
        self.assertEqual(n.text,bundle['claims'][0]['explanation'])
        self.assertEqual(len(n.evidence_ids),1)
        self.assertEqual(result.evidence[n.evidence_ids[0]].period_roles,('fy_t',))

    def test_commentary_is_visible_even_when_ratio_inputs_are_missing(self):
        request,_,report,_,bundle=inputs()
        bundle['claims'][0].update(topic='gross_margin',explanation='毛利率分析摘要。',fact_ids=[])
        result=commentary.apply_commentary(report,request,**bundle)
        self.assertEqual(result.tables[0].narratives[1].text,'毛利率分析摘要。')
        self.assertEqual(result.facts,report.facts)

    def test_missing_attribution_does_not_discard_summary(self):
        request,_,report,_,bundle=inputs();bundle['claims'][0]['claim_type']='management'
        result=commentary.apply_commentary(report,request,**bundle)
        self.assertEqual(result.tables[0].narratives[0].text,bundle['claims'][0]['explanation'])

    def test_review_cannot_be_reused_after_text_is_changed(self):
        request,_,report,_,bundle=inputs();report=commentary.apply_commentary(report,request,**bundle)
        table=report.tables[0];n=replace(table.narratives[0],text='Different claim')
        report=replace(report,tables=(replace(table,narratives=(n,)+table.narratives[1:]),)+report.tables[1:])
        self.assertFalse(commentary.is_reviewed(report,'income',n))

    def test_missing_cause_keeps_numeric_comparison_and_explicit_gap(self):
        request,_,report,_,bundle=inputs()
        bundle['claims']=[dict(table='income',topic='revenue',status='missing',reason='MD&A未說明變動原因')]
        report=commentary.apply_commentary(report,request,**bundle)
        n=report.tables[0].narratives[0]
        self.assertEqual(n.claim_type,'comparison');self.assertEqual(n.reason,'MD&A未說明變動原因')
        self.assertFalse(commentary.is_reviewed(report,'income',n))

    def test_automatic_model_response_cannot_supply_a_review_record(self):
        _,_,report,_,bundle=inputs()
        response=MagicMock(stop_reason='end_turn',content=[MagicMock(type='text',text=json.dumps({'claims':bundle['claims']}))])
        with patch('scripts.mda_commentary.anthropic.Anthropic') as api:
            api.return_value.messages.create.return_value=response
            claims=generate_formal_commentary(report,bundle['documents'])
            self.assertNotIn('review',claims[0])
            self.assertIn('canonical',api.return_value.messages.create.call_args.kwargs['system'])

    def test_synthetic_passages_cannot_be_relabelled_as_real_borrower_evidence(self):
        request,_,report,_,bundle=inputs()
        report=replace(report,entity='REAL')
        request={**request,'entity':'REAL'}
        for document in bundle['documents']:document['entity']='REAL'
        with self.assertRaisesRegex(ValueError,'Synthetic MD&A'):
            commentary.validate_documents(report,request,bundle['documents'])

    def test_oversize_source_is_not_silently_truncated_or_sent_to_model(self):
        request,_,report,_,bundle=inputs();bundle['documents'][0]['text']='a'*80001
        with self.assertRaisesRegex(ValueError,'budget'):
            commentary.validate_documents(report,request,bundle['documents'])


class SecDocumentTests(unittest.TestCase):
    def test_extract_actual_bounded_body_and_reject_arbitrary_fallback(self):
        body='Revenue increased because shipment volume rose. '*20
        html='<h1>Item 7. Management’s Discussion</h1> 21 <h2>Item 8 Financial Statements</h2>'+\
             '<h1>Item 7. Management’s Discussion</h1><p>'+body+'</p><h2>Item 7A Quantitative Disclosures</h2>'
        self.assertIn(body.strip(),commentary.extract_mda(html,'10-K'))
        with self.assertRaisesRegex(ValueError,'bounded MD&A'):
            commentary.extract_mda('<p>'+body+'</p>','10-K')

    def test_unterminated_toc_cannot_capture_business_section_as_mda(self):
        html='<p>Item 7. Management’s Discussion</p>'+('UNRELATED BUSINESS SECTION '*80)+\
            '<h1>Item 7. Management’s Discussion</h1>'+('Actual revenue cause discussion. '*25)+\
            '<h2>Item 8 Financial Statements</h2>'
        text=commentary.extract_mda(html,'10-K')
        self.assertIn('Actual revenue',text);self.assertNotIn('UNRELATED BUSINESS',text)

    def test_exact_requested_dates_and_as_of_not_latest_filing(self):
        request=request_fixture();client=MagicMock(rate_limit=0)
        client.get_company_submissions.return_value=dict(cik=1,filings={'recent':dict(
            accessionNumber=['0000000001-26-000001','0000000001-27-000001'],filingDate=['2026-02-01','2027-02-01'],
            reportDate=['2025-12-31','2026-12-31'],form=['10-K','10-K'],primaryDocument=['annual.htm','future.htm'])})
        html='<h1>Item 7. Management’s Discussion</h1>'+('Revenue increased due to volume. '*25)+'<h2>Item 8 Financial Statements</h2>'
        client.session.get.return_value=MagicMock(text=html,content=html.encode())
        documents=commentary.collect_sec_documents(client,request)
        self.assertEqual(len(documents),1)
        self.assertEqual(documents[0]['periods'][0]['role'],'fy_t')
        self.assertIn('annual.htm',client.session.get.call_args.args[0])
        self.assertEqual(documents[0]['document_date'],'2026-02-01')


class WorkflowAndFormatsTests(unittest.TestCase):
    def test_http_accepts_offline_commentary_bundle(self):
        from scripts import agent_runner
        if agent_runner.app is None:self.skipTest('Flask unavailable')
        request,snapshot,_,_,bundle=inputs()
        with agent_runner.app.test_client() as client,tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'OUTPUT_DIR':tmp}):
            response=client.post('/v2/analyze/SYNTHETIC-ONLY',json=dict(review_request=request,source_snapshot=snapshot,
                commentary=bundle,commentary_mode='reviewed',excel=False))
            self.assertEqual(response.status_code,200,response.get_json())
            output=Path(response.get_json()['outputs']['commentary_path'])
            self.assertEqual(json.loads(output.read_text())[0]['explanation'],bundle['claims'][0]['explanation'])

    def test_snapshot_is_offline_and_all_text_formats_share_canonical_content(self):
        request,snapshot,_,_,bundle=inputs()
        with tempfile.TemporaryDirectory() as tmp, patch('scripts.mda_commentary.generate_formal_commentary') as model, \
                patch('scripts.formal_commentary.collect_sec_documents') as sec:
            result=flow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,
                                   commentary=bundle,output_dir=tmp,excel=False)
            self.assertEqual(result['status'],'draft');model.assert_not_called();sec.assert_not_called()
            report,acceptance=pipeline.validate_saved_artifacts(tmp)
            payload=commentary.commentary_payload(report)
            self.assertEqual(payload,json.loads(Path(tmp,'commentary.json').read_text()))
            for filename in ('report.md','dashboard.html'):
                text=Path(tmp,filename).read_text()
                self.assertIn(bundle['claims'][0]['explanation'],text)
                for d in bundle['documents']:self.assertIn(d['text'],text)
            self.assertFalse(acceptance['final_report_accepted'])
            path=Path(tmp,'commentary.json');path.write_text('[]')
            with self.assertRaisesRegex(ValueError,'Stale artifact'):
                pipeline.validate_saved_artifacts(tmp)

    def test_model_failure_preserves_numeric_outputs_without_execution_failure(self):
        request,snapshot,_,_,bundle=inputs();bundle.pop('claims')
        cloud=MagicMock();cloud.stage_bundle.side_effect=lambda run_id,entity,b:b
        with tempfile.TemporaryDirectory() as tmp, patch('scripts.mda_commentary.generate_formal_commentary',side_effect=RuntimeError('model unavailable')):
            result=flow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,commentary=bundle,
                commentary_mode='model',output_dir=tmp,excel=False,execution='cloud',cloud=cloud)
            self.assertEqual(result['status'],'draft');self.assertEqual(result['stages']['commentary'],'failed')
            self.assertTrue(Path(tmp,'report.md').exists());self.assertTrue(Path(tmp,'dashboard.html').exists())
            self.assertIn('model unavailable',result['warnings']['commentary']);cloud.publish.assert_not_called()

    def test_model_failure_does_not_block_financially_accepted_delivery(self):
        from test_pr_review_regressions import accepted_fixture
        request,snapshot,_,_,bundle=inputs();bundle.pop('claims')
        report,acceptance=accepted_fixture()
        for document in bundle['documents']:document['scope']=report.scope
        report=replace(report,tables=tuple(replace(t,narratives=tuple(replace(n,claim_type='observation',
            text='Canonical numeric observation.') for n in t.narratives)) for t in report.tables))
        cloud=MagicMock();cloud.stage_bundle.side_effect=lambda run_id,entity,b:b
        with tempfile.TemporaryDirectory() as tmp,patch.object(flow,'report_from_source_bundle',return_value=(report,acceptance)),\
                patch('scripts.mda_commentary.generate_formal_commentary',side_effect=RuntimeError('model unavailable')):
            result=flow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,commentary=bundle,
                commentary_mode='model',output_dir=tmp,excel=False,execution='cloud',cloud=cloud)
            self.assertEqual(result['status'],'accepted',result)
            self.assertTrue(result['final_report_accepted']);self.assertEqual(result['cloud_status'],'published')
            self.assertNotIn('errors',result);self.assertIn('model unavailable',result['warnings']['commentary'])
            self.assertIn('分析尚未取得',Path(tmp,'report.md').read_text())
            self.assertEqual(json.loads(Path(tmp,'report.json').read_text())['facts'],report_payload(report)['facts'])
            cloud.publish.assert_called_once()

    def test_auto_sec_workflow_calls_source_and_model_adapters(self):
        request,snapshot,_,_,bundle=inputs()
        with tempfile.TemporaryDirectory() as tmp,patch('scripts.agent_runner.prepare_loan_review_source_stage',return_value=
                prepare_source_inputs(request,rows_of(snapshot['financial_facts']))),\
                patch('scripts.formal_commentary.collect_sec_documents',return_value=bundle['documents']) as collect,\
                patch('scripts.mda_commentary.generate_formal_commentary',return_value=[{k:v for k,v in bundle['claims'][0].items() if k!='review'}]) as model:
            result=flow.run_review('SYNTHETIC-ONLY',request,output_dir=tmp,excel=False)
            collect.assert_called_once();model.assert_called_once()
            self.assertEqual(result['status'],'draft');self.assertEqual(result['stages']['commentary'],'incomplete')

    def test_cloud_record_uses_same_canonical_commentary_payload(self):
        from test_pr_review_regressions import accepted_fixture
        report,acceptance=accepted_fixture();acceptance.update(final_report_accepted=True,rendered_validation_passed=True)
        cloud=ReviewCloud(project='fixture-project',dataset='raw',client=MagicMock())
        with patch.object(cloud,'write') as write,patch.object(cloud,'dbt'):
            cloud.publish('a'*32,report.entity,report_payload(report),acceptance)
            records=write.call_args.args[3]
            actual=[value for kind,key,value in records if kind=='commentary']
            self.assertEqual(actual,commentary.commentary_payload(report))

    @unittest.skipUnless(os.environ.get('REVIEW_EXCEL_TEST')=='1','Enable bundled Excel export tests')
    def test_saved_excel_contains_commentary_quotes_and_review_label(self):
        request,snapshot,_,_,bundle=inputs()
        with tempfile.TemporaryDirectory() as tmp:
            result=flow.run_review('SYNTHETIC-ONLY',request,source='snapshot',snapshot=snapshot,
                commentary=bundle,output_dir=tmp)
            self.assertEqual(result['stages']['excel'],'passed',result.get('errors'))
            with ZipFile(Path(tmp,'loan_review.xlsx')) as z:
                # Both inline and shared strings are covered by the archive text scan.
                xml=' '.join(z.read(name).decode() for name in z.namelist() if name.endswith('.xml'))
                self.assertIn(bundle['claims'][0]['explanation'],xml)
                self.assertIn('模型分析',xml)
                for document in bundle['documents']:self.assertIn(document['text'],xml)
            audit=json.loads(Path(tmp,'excel_validation.json').read_text())
            self.assertGreater(audit['commentary_entries'],0)


if __name__=='__main__':unittest.main()
