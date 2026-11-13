"""Optional real bundled-runtime export/recalculation and saved-file checks.

REVIEW_EXCEL_TEST=1 venv/bin/python -m unittest discover -s tests
"""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from scripts import nexstar_workbook_review as workbooks
from scripts.review_workflow import run_review
from test_loan_review_pipeline import fixture_book


@unittest.skipUnless(os.environ.get('REVIEW_EXCEL_TEST') == '1', 'Enable REVIEW_EXCEL_TEST=1 for bundled Node export')
class RealExcelExportTests(unittest.TestCase):
    def test_annual_and_quarterly_export_formulas_and_draft_status(self):
        for mode, fixture, quarter in [('annual', 'E-loan YYYY_Nexstar 2025.xls', None),
                                       ('quarterly', 'E-Loan YQYQ-Nexstar Q2.xls', 2)]:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                book = fixture_book(fixture); book['observations'] = []
                with patch.object(workbooks, 'read_workbook', return_value=book):
                    result = run_review('NXST', source='workbook', workbook='fixture.xls', review_date='2026-10-24',
                        mode=mode, quarter=quarter, output_dir=tmp)
                self.assertEqual(result['status'], 'draft', result.get('errors'))
                self.assertEqual(result['stages']['excel'], 'passed')
                validation = json.loads(Path(tmp, 'excel_validation.json').read_text())
                report = json.loads(Path(tmp, 'report.json').read_text())
                self.assertTrue(validation['passed'])
                self.assertEqual(validation['cells_checked'], len(report['facts']))
                with ZipFile(Path(tmp, 'loan_review.xlsx')) as archive:
                    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    workbook = ET.fromstring(archive.read('xl/workbook.xml'))
                    self.assertEqual([s.attrib['name'] for s in workbook.findall('s:sheets/s:sheet', ns)], ['Review', 'Sources'])
                    review = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
                    formulas = review.findall('.//s:f', ns)
                    self.assertEqual(len(formulas), validation['output_bindings'])
                    self.assertTrue(all('Sources' in f.text for f in formulas))
                    source = ET.fromstring(archive.read('xl/worksheets/sheet2.xml'))
                    self.assertTrue(source.findall('.//s:f', ns))
                self.assertTrue(Path(tmp, 'Review_preview.png').is_file())


if __name__ == '__main__': unittest.main()
