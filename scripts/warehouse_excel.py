"""Receipt-bound Excel delivery; binary64 approximation never approves precision.

Review reads immutable warehouse snapshot cells. Sources is an isolated local
trial. Decimal subtraction below audits Excel representation, not financial facts.
"""
from decimal import Decimal, localcontext
import json
from pathlib import Path
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from .warehouse_candidate import read_preview_data, consumer_code_hash, file_hash, _read, _require
from .review_outputs import report_payload
from .formal_commentary import commentary_payload

EXCEL_RELATIVE_LIMIT = Decimal('1e-12')
NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def audit_workbook(path, report, validation, *, receipt_sha256):
    """Verify exact strings, primary cell lineage and every binary64 result."""
    _require(validation.get('passed') is True and validation.get('calculation_receipt_sha256')==receipt_sha256,
             'Excel calculation receipt mismatch')
    _require(validation.get('precision_approved') is False and validation.get('publication_eligible') is False,
             'Excel cannot grant precision approval or publication')
    _require(validation.get('canonical_snapshot_unchanged_after_trial_edit') is True,
             'Excel trial isolation was not verified')
    rows = validation['rows']
    _require(len(rows)==len(report.facts) and {r['fact_id'] for r in rows}==set(report.facts), 'Incomplete Excel Fact coverage')
    expected_ids = [fid for table in report.tables for cells in table.cells for fid in cells]
    bindings = validation['review_bindings']
    _require([b['fact_id'] for b in bindings]==expected_ids and len({b['address'] for b in bindings})==len(bindings),
             'Excel output binding coverage mismatch')
    with ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        _require([s.attrib['name'] for s in workbook.findall('s:sheets/s:sheet',NS)]==['Review','Sources','Warehouse'],
                 'Unexpected candidate workbook structure')
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [''.join(si.itertext()) for si in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        sheets = [ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml')) for i in (1,2,3)]
        cells = [{cell.attrib['r']:cell for cell in sheet.findall('.//s:sheetData/s:row/s:c',NS)} for sheet in sheets]
        def value(address, sheet=2):
            node = cells[sheet].get(address)
            if node is None: return None
            if node.attrib.get('t')=='inlineStr': return ''.join(node.find('s:is',NS).itertext())
            raw = node.find('s:v',NS)
            if raw is None: return None
            return strings[int(raw.text)] if node.attrib.get('t')=='s' else raw.text
        def cached(address,sheet):
            node = cells[sheet].get(address)
            raw = value(address,sheet)
            if node is not None and raw is not None and node.attrib.get('t') in ('n',None):
                return float(raw)
            return raw
        _require(not sheets[2].findall('.//s:f',NS),'Warehouse snapshot must not calculate formulas')
        _require(value('A3')=='計算收據 '+receipt_sha256,'Workbook receipt identity mismatch')
        ledger = {row['fact_id']:row for row in rows}
        for row in rows:
            fact = report.facts[row['fact_id']]
            _require(re.fullmatch(r'B[1-9][0-9]*',row['canonical_address']) is not None,'Invalid canonical cell address')
            suffix = row['canonical_address'][1:]
            _require(value('A'+suffix)==fact.id,'Excel Fact/cell identity mismatch')
            for key,col,expected in (('exact_address','C',fact.value),('original_exact_address','D',fact.original_value),
                                     ('scale_exact_address','E',fact.original_scale)):
                _require(row[key]==col+suffix and value(row[key])==(str(expected) if expected is not None else None),
                         'Excel exact numeric string changed: '+fact.id)
            _require(row['canonical_value']==(str(fact.value) if fact.value is not None else None),'Excel canonical claim mismatch')
            _require(cached(row['canonical_address'],2)==row['canonical_excel_value'],'Saved canonical numeric cell changed')
            _require(re.fullmatch(r'B[1-9][0-9]*',row['source_address']) is not None and
                     cached(row['source_address'],1)==row['trial_value'],'Saved trial numeric cell changed')
        actual_formulas = {c.attrib['r']:c.find('s:f',NS).text for c in sheets[0].findall('.//s:c',NS) if c.find('s:f',NS) is not None}
        expected_formulas = {b['address']:"'Warehouse'!"+ledger[b['fact_id']]['canonical_address'] for b in bindings}
        _require(actual_formulas==expected_formulas,'Review must read only the fixed Warehouse snapshot')
        for binding in bindings:
            _require(cached(binding['address'],0)==ledger[binding['fact_id']]['canonical_excel_value'],
                     'Saved Review cached value differs from warehouse snapshot')
    for row in rows:
        fact = report.facts[row['fact_id']]
        for field in ('canonical_excel_value','trial_value'):
            number = row[field]
            if fact.value is None:
                _require(not isinstance(number,(int,float)),'Unavailable Excel Fact became numeric')
                continue
            if fact.unit=='text':
                _require(number==fact.value,'Excel text basis changed')
                continue
            _require(type(number) in (int,float),'Available Excel Fact is not numeric')
            with localcontext() as context:
                context.prec = 256
                converted = Decimal.from_float(float(number))
                _require(converted.is_finite(),'Nonfinite Excel value')
                difference = converted-fact.value
                limit = EXCEL_RELATIVE_LIMIT*max(Decimal(1),abs(fact.value))
                _require(abs(difference)<=limit,'Excel representation exceeds its delivery bound: '+fact.id)
                row[field+'_exact_binary64_decimal'] = str(converted)
                row[field+'_difference'] = str(difference)
                row[field+'_classification'] = 'exact' if difference==0 else 'binary64_approximation'
    validation.update(excel_relative_limit=str(EXCEL_RELATIVE_LIMIT),
        precision_policy_effect='none; this bound validates Excel delivery only',
        exact_strings_verified=len(rows),review_snapshot_bindings_verified=len(bindings),
        workbook_sha256=file_hash(path),precision_approved=False,publication_eligible=False)
    return validation


def export_candidate_excel(calculation_dir, preview_dir, *, expected_receipt_sha256):
    directory = Path(preview_dir)
    manifest_path = directory/'preview_manifest.json'
    manifest = _read(manifest_path)
    _require(not (directory/'loan_review.xlsx').exists() and not (directory/'excel_validation.json').exists(),
             'Excel outputs already exist; create a new candidate preview')
    try:
        report,receipt,analysis = read_preview_data(calculation_dir,expected_receipt_sha256=expected_receipt_sha256)
        _require(manifest.get('calculation_receipt_sha256')==expected_receipt_sha256 and manifest.get('bindings')==receipt['bindings'],
                 'Preview calculation binding mismatch')
        _require(manifest.get('consumer_code_hash')==consumer_code_hash(),'Preview consumer version changed; create a new preview')
        _require(all(manifest.get(key) is False for key in ('precision_approved','publication_eligible','final_report_accepted')),
                 'Candidate preview cannot grant publication')
        required = {'report.json','report.md','commentary.json','dashboard.html'} | ({'ratio_commentary_analysis.json'} if analysis is not None else set())
        _require(set(manifest['artifacts'])==required,'Incomplete preview artifact coverage')
        for name in required:
            _require(file_hash(directory/name)==manifest['artifacts'][name],'Stale preview artifact: '+name)
        _require(_read(directory/'report.json')==report_payload(report),'Preview Report differs from warehouse results')
        _require(_read(directory/'commentary.json')==commentary_payload(report),'Preview commentary differs from warehouse results')
        from .loan_review_pipeline import validate_rendered_report
        validate_rendered_report(report,(directory/'report.md').read_text(encoding='utf-8'))
        if analysis is not None:
            _require(_read(directory/'ratio_commentary_analysis.json')==analysis,'Preview ratio analysis differs from warehouse results')
        from .review_workflow import _run_excel_exporter
        target = _run_excel_exporter(directory,'--warehouse-candidate',expected_receipt_sha256)
        validation = audit_workbook(target,report,_read(directory/'excel_validation.json'),receipt_sha256=expected_receipt_sha256)
        (directory/'excel_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
        manifest.update(excel_status='passed',precision_approved=False,publication_eligible=False,final_report_accepted=False)
        manifest['artifacts'].update({name:file_hash(directory/name) for name in ('loan_review.xlsx','excel_validation.json')})
    except Exception as error:
        manifest.update(excel_status='failed',excel_error=str(error),precision_approved=False,publication_eligible=False,final_report_accepted=False)
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return str(Path(target).resolve())
