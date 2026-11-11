"""Pinned Excel inputs, saved-cell audits and isolated local trial regression."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from scripts import warehouse_candidate as candidate
from scripts.warehouse_excel import export_candidate_excel,audit_workbook
from test_warehouse_candidate import saved_candidate


def preview_fixture(root,mode='annual'):
    calculation=root/'calculation';calculation.mkdir()
    metadata=saved_candidate(calculation,mode=mode,valid_arithmetic=True)
    pinned=candidate.freeze_receipt(calculation,metadata)
    preview=root/'preview'
    candidate.write_preview(calculation,preview,expected_receipt_sha256=pinned)
    return calculation,preview,pinned


class ExcelBoundaryTests(unittest.TestCase):
    def test_modified_or_foreign_preview_is_rejected_before_builder(self):
        for defect in ('artifact','updated_hash','receipt','publish','markdown'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as tmp:
                calculation,preview,pinned=preview_fixture(Path(tmp))
                manifest=json.loads((preview/'preview_manifest.json').read_text())
                if defect in ('artifact','updated_hash'):
                    report=json.loads((preview/'report.json').read_text())
                    report['facts']['revenue:fy_t']['value']='999'
                    (preview/'report.json').write_text(json.dumps(report))
                    if defect=='updated_hash':manifest['artifacts']['report.json']=candidate.file_hash(preview/'report.json')
                elif defect=='receipt':manifest['calculation_receipt_sha256']='b'*64
                elif defect=='publish':manifest['publication_eligible']=True
                else:
                    text=(preview/'report.md').read_text().replace('120.00','999.00')
                    (preview/'report.md').write_text(text)
                    manifest['artifacts']['report.md']=candidate.file_hash(preview/'report.md')
                (preview/'preview_manifest.json').write_text(json.dumps(manifest))
                with patch('scripts.review_workflow._run_excel_exporter') as builder:
                    with self.assertRaises(ValueError):export_candidate_excel(calculation,preview,expected_receipt_sha256=pinned)
                    builder.assert_not_called()
                result=json.loads((preview/'preview_manifest.json').read_text())
                self.assertEqual(result['excel_status'],'failed');self.assertFalse(result['publication_eligible'])

    def test_requested_excel_failure_keeps_rendered_draft_and_does_not_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);calculation=root/'calculation';calculation.mkdir()
            pinned=candidate.freeze_receipt(calculation,saved_candidate(calculation,valid_arithmetic=True))
            preview=root/'preview'
            with patch('scripts.review_workflow._run_excel_exporter',side_effect=RuntimeError('runtime unavailable')):
                with self.assertRaisesRegex(RuntimeError,'runtime unavailable'):
                    candidate.write_preview(calculation,preview,expected_receipt_sha256=pinned,excel=True)
            manifest=json.loads((preview/'preview_manifest.json').read_text())
            self.assertEqual(manifest['excel_status'],'failed')
            self.assertFalse(manifest['precision_approved']);self.assertFalse(manifest['publication_eligible'])
            self.assertTrue((preview/'report.md').exists());self.assertTrue((preview/'dashboard.html').exists())

    def test_existing_workbook_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            calculation,preview,pinned=preview_fixture(Path(tmp))
            (preview/'loan_review.xlsx').write_bytes(b'preserve original attempt')
            with self.assertRaisesRegex(ValueError,'already exist'):
                export_candidate_excel(calculation,preview,expected_receipt_sha256=pinned)
            self.assertEqual((preview/'loan_review.xlsx').read_bytes(),b'preserve original attempt')


@unittest.skipUnless(os.environ.get('REVIEW_EXCEL_TEST')=='1','Enable bundled Excel verification')
class RealCandidateExcelTests(unittest.TestCase):
    def test_saved_annual_and_quarterly_snapshot_and_local_trial(self):
        for mode in ('annual','quarterly'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
                calculation,preview,pinned=preview_fixture(Path(tmp),mode)
                with (patch('scripts.loan_review_pipeline.validate_arithmetic',side_effect=AssertionError('Python fallback')),
                      patch('scripts.ratio_commentary_analysis.build_ratio_analysis',side_effect=AssertionError('Python fallback'))):
                    export_candidate_excel(calculation,preview,expected_receipt_sha256=pinned)
                report,_,_=candidate.read_preview_data(calculation,expected_receipt_sha256=pinned)
                validation=json.loads((preview/'excel_validation.json').read_text())
                self.assertEqual(validation['exact_strings_verified'],len(report.facts))
                self.assertTrue(validation['canonical_snapshot_unchanged_after_trial_edit'])
                self.assertFalse(validation['publication_eligible'])
                target=preview/'loan_review.xlsx'
                with ZipFile(target) as archive:
                    files={name:archive.read(name) for name in archive.namelist()}
                # Deliberate saved-file corruption: neither a cache nor a formula
                # may be substituted while keeping the pre-export audit claims.
                ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                sheet=ET.fromstring(files['xl/worksheets/sheet3.xml'])
                row=next(r for r in validation['rows'] if report.facts[r['fact_id']].unit=='money' and r['canonical_value'] is not None)
                cell=next(c for c in sheet.findall('.//s:c',ns) if c.attrib['r']==row['canonical_address'])
                cell.find('s:v',ns).text='999'
                corrupt=Path(tmp)/'corrupt.xlsx'
                with ZipFile(corrupt,'w') as archive:
                    for name,data in files.items():archive.writestr(name,ET.tostring(sheet) if name=='xl/worksheets/sheet3.xml' else data)
                with self.assertRaisesRegex(ValueError,'numeric cell changed'):
                    audit_workbook(corrupt,report,validation,receipt_sha256=pinned)


if __name__=='__main__':unittest.main()
