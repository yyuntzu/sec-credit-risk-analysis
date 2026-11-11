"""Synthetic-only native GCS protocol probes; never alters existing objects."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from google.api_core.exceptions import NotFound
from .delivery_archive import ShadowDeliveryStorage
from .warehouse_candidate import file_hash, _read, _require


def validate(path,pin,output):
    _require(file_hash(path)==pin,'Storage receipt pin mismatch')
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    receipt = _read(path)
    storage = ShadowDeliveryStorage(receipt['project'],receipt['bucket'])
    storage.ensure_bucket()
    original = storage._get(receipt['commit'])
    commit = json.loads(original)
    _require(commit['bindings']['entity']=='SYNTHETIC-ONLY','Native probes require synthetic data')
    cases = []
    for name,expected,error in (
        ('checksum',ValueError,'Delivery object checksum mismatch'),
        ('generation',NotFound,None),('run',ValueError,'Mixed delivery run')):
        bad = deepcopy(receipt)
        if name=='checksum':bad['commit']['sha256']='0'*64
        if name=='generation':bad['commit']['generation']='1'
        if name=='run':bad['run_id']='f'*32
        destination = output/('rejected_'+name)
        try:
            storage.restore(bad,destination)
        except expected as exc:
            _require(error is None or error in str(exc),'Wrong native rejection reason')
            _require(not destination.exists(),'Rejected restore created delivery output')
            cases.append(dict(case=name,rejected=True,reason=error or 'Generation not found'))
        else:
            raise AssertionError('Invalid storage receipt was accepted: '+name)
    # Uploading the same filenames with a changed delivery contract must not
    # replace the final commit, even when every artifact byte is unchanged.
    files = {name:storage._get(obj) for name,obj in commit['objects'].items()}
    body = {k:v for k,v in commit.items() if k!='objects'}
    body['required_excel'] = not body['required_excel']
    from . import delivery_archive
    body['verifier_code_hash'] = file_hash(delivery_archive.__file__)
    try:
        storage.store(body,files)
    except ValueError as exc:
        _require('never overwrite' in str(exc),'Wrong conflicting commit failure')
        cases.append(dict(case='conflicting_delivery_contract',rejected=True,reason='Existing commit differs'))
    else:
        raise AssertionError('Conflicting commit was accepted')
    _require(storage._get(receipt['commit'])==original,'Existing delivery commit changed')
    live = storage.bucket.blob(receipt['commit']['name']);live.reload(timeout=60)
    _require(str(live.generation)==receipt['commit']['generation'],'Live commit generation changed')
    result = dict(status='passed',storage_receipt_sha256=pin,cases=cases,
        original_commit_unchanged=True,precision_approved=False,publication_eligible=False)
    (output/'probe_manifest.json').write_text(json.dumps(result,indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--storage-receipt',required=True)
    parser.add_argument('--storage-receipt-sha256',required=True)
    parser.add_argument('--output-dir',required=True)
    args = parser.parse_args()
    print(json.dumps(validate(args.storage_receipt,args.storage_receipt_sha256,args.output_dir),indent=2))


if __name__=='__main__':main()
