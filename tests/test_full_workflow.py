from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch

from scripts.loan_review_sources import canonical,digest
from scripts.loan_review_contract import METRICS
from scripts.loan_review_pipeline import STANDARD_EBITDA_BASIS
from scripts.warehouse_workbook import reconciliation_slots,workbook_bundle
from scripts.warehouse_source import source_envelope,BigQuerySourceStore
from scripts.warehouse_publication import verify_publication,validation_policy
from scripts.dbt_shadow import prepare_run
from test_dbt_shadow import rich_bundle
from test_loan_review_pipeline import fixture_book


def complete_quarterly_fixture():
    """Explicit synthetic LTM observations and hand-balanced bridges; no real data."""
    bundle=reconciliation_slots(rich_bundle('quarterly'))
    prototype=next(iter(bundle['evidence'].values()))
    for period in bundle['request']['periods']:
        for metric,value in (('ltm_ebitda','75'),('ebitda_basis',STANDARD_EBITDA_BASIS)):
            observation=deepcopy(prototype)
            observation.update(metric=metric,value=value,unit='text' if metric=='ebitda_basis' else 'USD',
                scale='1' if metric=='ebitda_basis' else '1000000',definition=METRICS[metric].definition,
                basis=STANDARD_EBITDA_BASIS,start=period['ltm_start'],end=period['end'],
                locator='SYNTHETIC-FULL-LTM:'+metric+':'+period['role'])
            observation['id']='supp:'+digest(observation);bundle['evidence'][observation['id']]=observation
    _,records,_,_=prepare_run(bundle,with_baseline=False)
    slots={row['fact_id']:row for kind,_,row in records if kind=='slot'}
    checks=[];evidence={}
    for period in bundle['request']['periods']:
        role=period['role']
        def fid(metric):return metric+':'+role if metric+':'+role in slots else 'input:'+metric+':'+role
        def source(metric):
            slot=slots[fid(metric)]
            return {key for key,row in bundle['evidence'].items() if row['metric']==metric
                and str(row['start'])==str(slot['start']) and str(row['end'])==str(slot['end'])}
        for kind,reported,terms,amount in (
            ('balance_sheet_equation','total_assets',['total_liabilities','net_worth'],'300'),
            ('cash_bridge','ending_cash',['beginning_cash','cfo','cfi','cff','cash_fx','cash_other'],'20')):
            check=dict(kind=kind,period_role=role,status='matched',
                terms=[dict(fact_id=fid(metric),coefficient='1') for metric in terms],
                reported_fact_id=fid(reported),tolerance='0',calculated_value=amount,reported_value=amount,difference='0')
            eid='review:'+kind+':'+role
            check['evidence_ids']=sorted(set().union(*(source(metric) for metric in [reported]+terms))|{eid})
            binding={key:check[key] for key in ('kind','period_role','terms','reported_fact_id','tolerance')}
            binding.update(currency='USD',scale='1000000')
            evidence[eid]=dict(id=eid,entity='SYNTHETIC-ONLY',scope='entity-wide',source_id='SYNTHETIC-FULL-BRIDGE',
                version='v1',document_date='2026-09-02',locator=kind+':'+role,kind='definition',
                period_roles=[role],content=canonical(binding),purpose='borrower')
            checks.append(check)
    return bundle,dict(schema_version=1,checks=checks,evidence=evidence)


class FullWorkflowSourceTests(unittest.TestCase):
    def test_source_envelope_binds_request_reviews_and_documents(self):
        bundle,reviews=complete_quarterly_fixture()
        envelope=source_envelope(bundle,reconciliations=reviews)
        changed=deepcopy(envelope);changed['reconciliations']['checks'][0]['tolerance']='1'
        self.assertNotEqual(digest(envelope),digest(changed))
        self.assertEqual(envelope['bundle'],json.loads(canonical(bundle)))

    def test_quarterly_has_actual_ltm_and_all_eight_reviewed_bridges(self):
        bundle,reviews=complete_quarterly_fixture()
        metadata,records,baseline,_=prepare_run(bundle,with_baseline=False,reconciliations=reviews)
        self.assertIsNone(baseline);self.assertEqual(len(reviews['checks']),8)
        self.assertTrue(any(row['metric']=='ltm_ebitda' and row['start']=='2024-07-01' for row in bundle['evidence'].values()))
        self.assertTrue(all(any(kind=='slot' and row['metric']==metric for kind,_,row in records)
            for metric in ('beginning_cash','cash_fx','cash_other')))
        shared=[key for key,row in bundle['evidence'].items() if row['metric']=='beginning_cash' and str(row['end'])=='2023-12-31']
        self.assertEqual(len(shared),2)
        review=next(row for row in reviews['checks'] if row['kind']=='cash_bridge' and row['period_role']=='latest_fy_end')
        self.assertTrue(set(shared)<=set(review['evidence_ids']))

    def test_workbook_keeps_raw_cells_and_cannot_claim_historical_sec_availability(self):
        book=fixture_book('E-loan YYYY_Nexstar 2025.xls')
        from scripts.nexstar_workbook_review import build_inputs
        base,_,_=build_inputs(book,'annual')
        from dataclasses import asdict
        evidence=[dict(asdict(value),entity='NXST',purpose='borrower') for value in base.evidence.values()]
        request=dict(schema_version=1,entity='NXST',cik='0001142417',scope='consolidated',mode='annual',currency='USD',
            scale='1000000',as_of='2026-10-24',periods=[asdict(p) for p in base.periods],evidence=evidence)
        request=json.loads(canonical(request))
        bundle=workbook_bundle(book['path'],request,book=book)
        self.assertEqual(bundle['workbook_snapshot']['sha256'],book['hash'])
        self.assertTrue(bundle['source_limitations'])
        metadata,_,baseline,_=prepare_run(bundle,with_baseline=False)
        self.assertEqual(metadata['source_limitations'],sorted(bundle['source_limitations']))
        self.assertIsNone(baseline)
        request['periods'][0]['end']='2022-12-30'
        with self.assertRaises(ValueError):workbook_bundle(book['path'],request,book=book)

    def test_source_reader_detects_changed_and_duplicate_physical_rows(self):
        envelope=source_envelope(rich_bundle());source_id=digest(envelope)
        receipt=dict(format_version='warehouse-source-receipt-v1',project='test-project',dataset='sec_review_shadow_sources',
            table='source_bundle_'+source_id,source_id=source_id,payload_sha256=source_id,entity='SYNTHETIC-ONLY',scope='entity-wide',
            request_hash=digest(envelope['bundle']['request']))
        store=BigQuerySourceStore('test-project','sec_review_shadow_sources',client=object())
        row={key:receipt[key] for key in store.fields if key!='payload'};row['payload']=canonical(envelope)
        with patch.object(store,'_read',return_value=[row]):self.assertEqual(store.load(receipt),envelope)
        for rows in ([dict(row,payload='{}')],[row,row],[]):
            with patch.object(store,'_read',return_value=rows),self.assertRaises(ValueError):store.load(receipt)

    def test_sql_source_extractor_preserves_exact_nested_json_lexical_bytes(self):
        macro=Path('references/dbt/macros/publication_source.sql').read_text()
        body=macro.split('{% macro publication_raw_bundle_body() -%}',1)[1].split('{%- endmacro %}',1)[0]
        bundles=[rich_bundle(),dict(text='nested } ] " \\ 中文',items=[dict(commentary_documents=[1.0,'1.00'])])]
        payloads=[canonical(dict(bundle=value,commentary_documents=[],format_version='warehouse-source-v1')) for value in bundles]
        node='/Users/yuntzuyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
        program='const fs=require("fs");const f=new Function("payload",'+json.dumps(body)+');'+\
            'process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,"utf8")).map(f)));'
        actual=json.loads(subprocess.run([node,'-e',program],input=json.dumps(payloads),text=True,capture_output=True,check=True).stdout)
        self.assertEqual(actual,[canonical(value) for value in bundles])
