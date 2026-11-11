"""Receipt-bound candidate delivery storage. No publication or approval API."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile

from .loan_review_sources import canonical
from .warehouse_candidate import (file_hash, _read, _require, read_preview_data,
                                  write_preview, consumer_code_hash)

VERSION = 'candidate-delivery-v1'
BASE = {'report.json','report.md','dashboard.html','commentary.json'}
EXCEL = {'loan_review.xlsx','excel_validation.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare_delivery(calculation, preview, *, calculation_pin, preview_pin,
                     archive_receipt, archive_pin, delivery_id, require_excel=True):
    """Reverify content, not merely producer PASS flags. Returns frozen bytes."""
    _require(re.fullmatch('[a-f0-9]{32}',delivery_id or '') is not None,'Invalid delivery ID')
    calculation,preview = Path(calculation),Path(preview)
    _require(file_hash(archive_receipt)==archive_pin,'Candidate archive receipt pin mismatch')
    archive = _read(archive_receipt)
    report,receipt,analysis = read_preview_data(calculation,expected_receipt_sha256=calculation_pin)
    _require(archive['format_version']=='candidate-archive-v1'
        and archive['calculation_receipt_sha256']==calculation_pin
        and all(archive[k]==receipt['bindings'][k] for k in ('run_id','entity','scope')),
        'Delivery candidate archive binding mismatch')
    _require(re.fullmatch('[a-f0-9]{32}',archive['attempt_id']) is not None,'Invalid archive attempt')
    _require(archive['table']=='review_candidate_'+archive['attempt_id']
        and re.fullmatch('sec_review_shadow_[a-z0-9_]+',archive['dataset']) is not None,
        'Invalid candidate archive target')
    _require(all(archive.get(k) is False for k in ('precision_approved','publication_eligible')),
        'Candidate archive cannot grant publication')
    _require(not (preview/'preview_manifest.json').is_symlink(),'Delivery symlink forbidden')
    _require(file_hash(preview/'preview_manifest.json')==preview_pin,'Preview manifest pin mismatch')
    manifest = _read(preview/'preview_manifest.json')
    _require(manifest['bindings']==receipt['bindings'] and manifest['calculation_receipt_sha256']==calculation_pin,
        'Preview calculation binding mismatch')
    _require(manifest['engine']=='dbt-bigquery-candidate' and manifest['consumer_code_hash']==consumer_code_hash(),
        'Create a preview with the current verified consumer')
    _require(all(manifest.get(k) is False for k in ('precision_approved','publication_eligible','final_report_accepted')),
        'Candidate delivery cannot grant publication')
    names = BASE | ({'ratio_commentary_analysis.json'} if analysis is not None else set())
    has_excel = manifest.get('excel_status')=='passed'
    _require(has_excel or not require_excel,'Required Excel delivery not passed')
    _require(manifest.get('excel_status') in ('passed','not_requested'),'Incomplete or failed Excel delivery')
    expected_names = names | (EXCEL if has_excel else set())
    _require(set(manifest['artifacts'])==expected_names,'Delivery artifact coverage mismatch')
    files = {}
    for name in sorted(expected_names|{'preview_manifest.json'}):
        path = preview/name
        _require(not path.is_symlink() and path.is_file(),'Missing artifact or symlink forbidden')
        data = path.read_bytes()
        _require(name=='preview_manifest.json' or sha(data)==manifest['artifacts'][name],
            'Delivery artifact hash mismatch: '+name)
        files[name] = data
    # Deterministic rerender checks all narrative/HTML/JSON content against SQL.
    with tempfile.TemporaryDirectory() as root:
        rendered = Path(root)/'expected'
        write_preview(calculation,rendered,expected_receipt_sha256=calculation_pin)
        _require(all(files[name]==(rendered/name).read_bytes() for name in names),
            'Delivery content differs from receipt-bound rendering')
    if has_excel:
        from .warehouse_excel import audit_workbook
        audit_workbook(preview/'loan_review.xlsx',report,_read(preview/'excel_validation.json'),receipt_sha256=calculation_pin)
    files['calculation_receipt.json'] = (calculation/'calculation_receipt.json').read_bytes()
    files['candidate_archive_receipt.json'] = Path(archive_receipt).read_bytes()
    body = dict(format_version=VERSION,delivery_id=delivery_id,bindings=receipt['bindings'],
        archive_attempt_id=archive['attempt_id'],calculation_receipt_sha256=calculation_pin,
        candidate_archive_receipt_sha256=archive_pin,preview_manifest_sha256=preview_pin,
        consumer_code_hash=manifest['consumer_code_hash'],verifier_code_hash=file_hash(__file__),
        required_excel=require_excel,excel_included=has_excel,
        artifacts={name:dict(sha256=sha(data),size=len(data)) for name,data in files.items()},
        precision_approved=False,publication_eligible=False)
    return body,files


class ShadowDeliveryStorage:
    """Create-only GCS objects; pin generations and verify all downloaded bytes."""
    def __init__(self,project,bucket,*,client=None):
        _require(re.fullmatch('[a-z][a-z0-9-]+',project) is not None,'Invalid storage project')
        _require(re.fullmatch('sec-review-shadow-[a-z0-9-]+',bucket) is not None,'Isolated shadow bucket required')
        from google.cloud import storage
        self.project,self.name,self.storage = project,bucket,storage
        self.client = client or storage.Client(project=project)
        self.bucket = self.client.bucket(bucket)

    def ensure_bucket(self,*,create=False):
        from google.api_core.exceptions import NotFound,Conflict
        try:
            self.bucket.reload(timeout=60)
        except NotFound:
            _require(create,'Delivery bucket does not exist')
            self.bucket.iam_configuration.uniform_bucket_level_access_enabled = True
            self.bucket.iam_configuration.public_access_prevention = 'enforced'
            self.bucket.labels = {'workflow':'loan-review-shadow','project':self.project}
            self.bucket.add_lifecycle_delete_rule(age=7)
            try:
                self.client.create_bucket(self.bucket,location='US',timeout=60)
            except Conflict:
                self.bucket.reload(timeout=60)
        self.bucket.reload(timeout=60)
        _require(self.bucket.labels.get('workflow')=='loan-review-shadow'
            and self.bucket.labels.get('project')==self.project
            and self.bucket.iam_configuration.uniform_bucket_level_access_enabled
            and self.bucket.iam_configuration.public_access_prevention=='enforced',
            'Bucket isolation or public access policy mismatch')

    def _put(self,name,data):
        from google.api_core.exceptions import PreconditionFailed
        blob = self.bucket.blob(name)
        try:
            blob.upload_from_string(data,content_type='application/octet-stream',
                if_generation_match=0,checksum='crc32c',timeout=60)
        except PreconditionFailed:
            blob.reload(timeout=60)
        generation = int(blob.generation)
        actual = self.bucket.blob(name,generation=generation).download_as_bytes(
            if_generation_match=generation,checksum='crc32c',timeout=60)
        _require(actual==data,'Existing delivery object differs; never overwrite')
        return dict(name=name,generation=str(generation),sha256=sha(data),size=len(data))

    def _get(self,record):
        _require(isinstance(record['generation'],str) and record['generation'].isdigit()
            and int(record['generation'])>0,'Invalid object generation')
        generation = int(record['generation'])
        data = self.bucket.blob(record['name'],generation=generation).download_as_bytes(
            if_generation_match=generation,checksum='crc32c',timeout=60)
        _require(sha(data)==record['sha256'] and len(data)==record['size'],'Delivery object checksum mismatch')
        return data

    @staticmethod
    def _prefix(body):
        return 'candidate-deliveries/'+body['bindings']['run_id']+'/'+body['archive_attempt_id']+'/'+body['delivery_id']+'/'

    def store(self,body,files):
        _require(body['format_version']==VERSION and all(body.get(k) is False for k in ('precision_approved','publication_eligible')),
            'Candidate delivery cannot grant publication')
        for value in (body['bindings']['run_id'],body['archive_attempt_id'],body['delivery_id']):
            _require(re.fullmatch('[a-f0-9]{32}',value) is not None,'Invalid delivery identity')
        _require(set(files)<=BASE|EXCEL|{'ratio_commentary_analysis.json','preview_manifest.json',
            'calculation_receipt.json','candidate_archive_receipt.json'},'Invalid delivery filenames')
        _require(body['verifier_code_hash']==file_hash(__file__),'Delivery verifier changed')
        _require(body['artifacts']=={name:dict(sha256=sha(data),size=len(data)) for name,data in files.items()},
            'Delivery bytes changed after validation')
        prefix = self._prefix(body)
        objects = {name:self._put(prefix+name,data) for name,data in sorted(files.items())}
        _require(body['verifier_code_hash']==file_hash(__file__),'Delivery verifier changed during upload')
        commit = dict(body,objects=objects)
        committed = self._put(prefix+'delivery_commit.json',canonical(commit).encode('utf-8'))
        return dict(format_version=VERSION,project=self.project,bucket=self.name,commit=committed,
            run_id=body['bindings']['run_id'],archive_attempt_id=body['archive_attempt_id'],delivery_id=body['delivery_id'],
            precision_approved=False,publication_eligible=False)

    def restore(self,receipt,directory):
        _require(receipt['format_version']==VERSION and receipt['project']==self.project and receipt['bucket']==self.name,
            'Storage receipt identity mismatch')
        _require(all(receipt.get(k) is False for k in ('precision_approved','publication_eligible')),
            'Delivery receipt cannot grant publication')
        commit = json.loads(self._get(receipt['commit']))
        _require(commit['format_version']==VERSION and all(commit.get(k) is False for k in ('precision_approved','publication_eligible')),
            'Invalid candidate delivery commit')
        for key in ('archive_attempt_id','delivery_id'):
            _require(commit[key]==receipt[key] and re.fullmatch('[a-f0-9]{32}',commit[key]) is not None,'Mixed delivery identity')
        _require(commit['bindings']['run_id']==receipt['run_id'] and re.fullmatch('[a-f0-9]{32}',receipt['run_id']) is not None,
            'Mixed delivery run')
        prefix = self._prefix(commit)
        _require(receipt['commit']['name']==prefix+'delivery_commit.json','Invalid commit object path')
        names = BASE|{'preview_manifest.json','calculation_receipt.json','candidate_archive_receipt.json'}
        if 'ratio_commentary_analysis.json' in commit['artifacts']:names.add('ratio_commentary_analysis.json')
        if commit['excel_included']:names |= EXCEL
        _require(not commit['required_excel'] or commit['excel_included'],'Missing required archived Excel')
        _require(set(commit['objects'])==names and set(commit['artifacts'])==names,'Incomplete archived delivery coverage')
        files = {}
        for name in sorted(names):
            obj = commit['objects'][name]
            _require(obj['name']==prefix+name and all(obj[k]==commit['artifacts'][name][k] for k in ('sha256','size')),
                'Mixed delivery object binding')
            files[name] = self._get(obj)
        _require(sha(files['calculation_receipt.json'])==commit['calculation_receipt_sha256']
            and sha(files['candidate_archive_receipt.json'])==commit['candidate_archive_receipt_sha256']
            and sha(files['preview_manifest.json'])==commit['preview_manifest_sha256'],'Archived receipt pin mismatch')
        for name in ('calculation_receipt.json','preview_manifest.json'):
            _require(json.loads(files[name])['bindings']==commit['bindings'],'Archived cross-run artifact')
        directory = Path(directory)
        directory.mkdir(parents=True,exist_ok=False)
        for name,data in files.items():(directory/name).write_bytes(data)
        return commit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command',required=True)
    store = commands.add_parser('store')
    for name in ('calculation-dir','preview-dir','calculation-receipt-sha256','preview-manifest-sha256',
                 'archive-receipt','archive-receipt-sha256','delivery-id','project','bucket','output-dir'):
        store.add_argument('--'+name,required=True)
    store.add_argument('--create-bucket',action='store_true')
    store.add_argument('--without-excel',action='store_true',help='Explicitly record a non-Excel delivery requirement')
    restore = commands.add_parser('restore')
    for name in ('storage-receipt','storage-receipt-sha256','output-dir'):
        restore.add_argument('--'+name,required=True)
    args = parser.parse_args(argv)
    output = Path(args.output_dir)
    _require(not output.exists(),'Delivery output already exists')
    if args.command=='restore':
        _require(file_hash(args.storage_receipt)==args.storage_receipt_sha256,'Storage receipt pin mismatch')
        receipt = _read(args.storage_receipt)
        storage = ShadowDeliveryStorage(receipt['project'],receipt['bucket'])
        storage.ensure_bucket()
        result = storage.restore(receipt,output)
    else:
        body,files = prepare_delivery(args.calculation_dir,args.preview_dir,
            calculation_pin=args.calculation_receipt_sha256,preview_pin=args.preview_manifest_sha256,
            archive_receipt=args.archive_receipt,archive_pin=args.archive_receipt_sha256,
            delivery_id=args.delivery_id,require_excel=not args.without_excel)
        output.mkdir(parents=True)
        manifest = dict(status='validated',delivery=body,publication_eligible=False)
        (output/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2))
        try:
            storage = ShadowDeliveryStorage(args.project,args.bucket)
            storage.ensure_bucket(create=args.create_bucket)
            result = storage.store(body,files)
            (output/'storage_receipt.json').write_text(json.dumps(result,indent=2))
            manifest['status']='stored'
        except Exception as error:
            manifest.update(status='failed',error=str(error))
            raise
        finally:
            (output/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
