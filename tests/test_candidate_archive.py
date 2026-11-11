"""Atomic snapshot contract, pinned reads and conflicting attempt/run failures."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from google.api_core.exceptions import Conflict,NotFound
from google.cloud import bigquery
from scripts import candidate_archive as storage
from scripts import warehouse_candidate as candidate
from test_warehouse_candidate import saved_candidate

ATTEMPT='1'*32


class FakeClient:
    def __init__(self):
        self.tables={};self.rows={};self.jobs={};self.loads=0;self.duplicate_insert=False;self.typed_rows=[]
    def create_dataset(self,table,exists_ok):pass
    def get_dataset(self,reference):return SimpleNamespace(location='US')
    def create_table(self,table,exists_ok=False):
        key=f'{table.project}.{table.dataset_id}.{table.table_id}'
        if key in self.tables:raise Conflict('table exists')
        self.tables[key]=SimpleNamespace(labels=dict(table.labels or {}),description=table.description,schema=table.schema,num_rows=0)
    def get_table(self,key):return self.tables[key]
    def get_job(self,key,location=None):
        if key not in self.jobs:raise NotFound('job not inserted')
        return self.jobs[key]
    def load_table_from_json(self,rows,reference,*,job_id,location,job_config):
        self.loads+=1
        if self.rows.get(reference):raise AssertionError('Attempted to append or overwrite an existing snapshot')
        self.rows[reference]=deepcopy(rows);self.tables[reference].num_rows=len(rows)
        self.jobs[job_id]=SimpleNamespace(destination=bigquery.TableReference.from_string(reference),
            write_disposition=job_config.write_disposition,labels=job_config.labels,result=lambda:None)
        if self.duplicate_insert:raise Conflict('confirmation lost; original job exists')
        return self.jobs[job_id]
    def query(self,sql,location=None,job_config=None):
        key=sql.split('`')[1]
        if key.endswith('.fct_review_candidate_facts'):
            return SimpleNamespace(result=lambda:deepcopy(self.typed_rows))
        return SimpleNamespace(result=lambda:deepcopy(self.rows[key]))


def prepared(directory,mode='annual'):
    directory.mkdir()
    metadata=saved_candidate(directory,mode=mode,valid_arithmetic=True)
    pinned=candidate.freeze_receipt(directory,metadata)
    return pinned,*storage.prepare_archive(directory,receipt_sha256=pinned,attempt_id=ATTEMPT)


class CandidateArchiveTests(unittest.TestCase):
    def test_full_round_trip_is_idempotent_and_does_not_use_python_financial_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pinned,commit,records=prepared(root/'source')
            client=FakeClient();archive=storage.ShadowCandidateArchive('fixture-project','sec_review_shadow_archive_test',client=client)
            archive.ensure_dataset()
            receipt=archive.store(commit,records)
            # Job metadata may expire; an intact snapshot remains an idempotent retry.
            client.jobs.clear()
            self.assertEqual(archive.store(commit,records),receipt)
            self.assertEqual(client.loads,1)
            with (patch('scripts.loan_review_pipeline.report_from_source_bundle',side_effect=AssertionError('fallback')),
                  patch('scripts.loan_review_pipeline.validate_arithmetic',side_effect=AssertionError('fallback'))):
                report=archive.restore(receipt,root/'restored')
            self.assertEqual(report.entity,'SYNTHETIC-ONLY')
            self.assertFalse((root/'restored/baseline.json').exists())
            self.assertEqual(candidate.file_hash(root/'restored/calculation_receipt.json'),pinned)
            self.assertFalse(receipt['publication_eligible'])

    def test_duplicate_job_confirmation_uses_the_original_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,commit,records=prepared(Path(tmp)/'source')
            client=FakeClient();client.duplicate_insert=True
            archive=storage.ShadowCandidateArchive('fixture-project','sec_review_shadow_archive_test',client=client)
            receipt=archive.store(commit,records)
            self.assertEqual(client.loads,1)
            self.assertIn(receipt['load_job_id'],client.jobs)

    def test_missing_duplicate_foreign_or_modified_rows_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,commit,original=prepared(Path(tmp)/'source')
            cases=[original[:-1],original+[original[0]],
                [dict(original[0],attempt_id='2'*32)]+original[1:],
                [dict(original[0],payload='{}')]+original[1:]]
            changed=deepcopy(original);changed[-1]['payload']=changed[-1]['payload'].replace('candidate-archive-v1','candidate-archive-v2')
            changed[-1]['payload_sha256']=storage.sha(changed[-1]['payload']);cases.append(changed)
            for rows in cases:
                with self.subTest(case=len(rows)),self.assertRaises(ValueError):storage.verify_snapshot(rows,expected=commit)

    def test_run_cannot_change_sources_or_versions_between_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            _,commit,records=prepared(root/'annual')
            _,other,other_rows=prepared(root/'quarterly','quarterly')
            client=FakeClient();archive=storage.ShadowCandidateArchive('fixture-project','sec_review_shadow_archive_test',client=client)
            archive.store(commit,records)
            with self.assertRaisesRegex(ValueError,'Run is already bound'):
                archive.store(other,other_rows)
            self.assertEqual(client.loads,1)

    def test_partial_existing_snapshot_is_not_repaired_by_appending(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,commit,records=prepared(Path(tmp)/'source')
            client=FakeClient();archive=storage.ShadowCandidateArchive('fixture-project','sec_review_shadow_archive_test',client=client)
            receipt=archive.store(commit,records)
            key=f"fixture-project.sec_review_shadow_archive_test.{receipt['table']}"
            client.rows[key].pop()
            with self.assertRaises(ValueError):archive.store(commit,records)
            self.assertEqual(client.loads,1)

    def test_failed_archive_preserves_prepared_plan_and_never_grants_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pinned,_,_=prepared(root/'source')
            archive=SimpleNamespace(ensure_dataset=lambda:None,store=lambda *args:(_ for _ in ()).throw(RuntimeError('load failed')))
            with self.assertRaisesRegex(RuntimeError,'load failed'):
                storage.archive_calculation(root/'source',root/'failed',project='fixture-project',dataset='sec_review_shadow_archive_test',
                    receipt_sha256=pinned,attempt_id=ATTEMPT,archive=archive)
            manifest=json.loads((root/'failed/archive_manifest.json').read_text())
            self.assertEqual(manifest['status'],'failed');self.assertFalse(manifest['publication_eligible'])
            self.assertTrue((root/'failed/archive_records.json').exists())
            self.assertFalse((root/'failed/archive_receipt.json').exists())

    def test_production_namespace_and_unpinned_source_are_not_accepted(self):
        with self.assertRaisesRegex(ValueError,'isolated'):
            storage.ShadowCandidateArchive('fixture-project','sec_raw',client=FakeClient())
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);prepared(root/'source')
            with self.assertRaisesRegex(ValueError,'receipt hash mismatch'):
                storage.prepare_archive(root/'source',receipt_sha256='b'*64,attempt_id=ATTEMPT)

    def test_source_change_during_archive_cannot_claim_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pinned,commit,_=prepared(root/'source')
            archive=SimpleNamespace(ensure_dataset=lambda:None,store=lambda *args:dict(publication_eligible=False))
            with patch.object(storage,'archive_code_hash',side_effect=[commit['archive_code_hash'],'0'*64]):
                with self.assertRaisesRegex(ValueError,'code changed'):
                    storage.archive_calculation(root/'source',root/'changed',project='fixture-project',dataset='sec_review_shadow_archive_test',
                        receipt_sha256=pinned,attempt_id=ATTEMPT,archive=archive)
            self.assertEqual(json.loads((root/'changed/archive_manifest.json').read_text())['status'],'failed')

    def test_typed_reader_rejects_mixed_attempts_or_changed_decimal_without_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            _,commit,records=prepared(Path(tmp)/'source')
            client=FakeClient();archive=storage.ShadowCandidateArchive('fixture-project','sec_review_shadow_archive_test',client=client)
            receipt=archive.store(commit,records)
            for raw in records:
                if raw['record_kind']!='fact':continue
                fact=json.loads(raw['payload'])
                client.typed_rows.append(dict(fact,attempt_id=ATTEMPT,content_sha256=receipt['content_sha256'],
                    calculation_receipt_sha256=receipt['calculation_receipt_sha256'],archive_integrity_passed=True,
                    value_numeric=Decimal(fact['value']) if fact['unit']!='text' and fact['value'] is not None else None,
                    frozen_fact_payload=raw['payload'],publication_eligible=False))
            self.assertEqual(len(archive.read_facts(receipt)),commit['record_counts']['fact'])
            original=deepcopy(client.typed_rows)
            for defect in ('attempt','decimal','field','missing'):
                client.typed_rows=deepcopy(original)
                if defect=='attempt':client.typed_rows[0]['attempt_id']='2'*32
                elif defect=='decimal':next(r for r in client.typed_rows if r['value_numeric'] is not None)['value_numeric']=Decimal('999')
                elif defect=='field':client.typed_rows[0]['definition']='changed definition'
                else:client.typed_rows.pop()
                with self.subTest(defect=defect),self.assertRaises(ValueError):archive.read_facts(receipt)


if __name__=='__main__':unittest.main()
