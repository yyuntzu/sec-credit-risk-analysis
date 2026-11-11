"""Execute the selected candidate package; no production authority or fallback."""
import argparse
import json
from pathlib import Path
import tempfile

from .candidate_release_control import CandidateReleaseControl,GCSCandidateControlStore,candidate_release
from .runtime_package import inspect_package,run_package
from .warehouse_candidate import _require,file_hash


class RuntimeStorage:
    def __init__(self,storage):self.storage=storage
    def store(self,path,pin):
        manifest,_=inspect_package(path,pin)
        record=self.storage._put('candidate-runtime/'+pin+'.zip',Path(path).read_bytes())
        return dict(kind='candidate-runtime-reference-v1',object=record,package_sha256=pin,
            code_hash=manifest['financial_code_hash'],runtime_sha256=manifest['runtime_sha256'],
            precision_approved=False,publication_eligible=False)
    def fetch(self,reference,path):
        _require(reference['kind']=='candidate-runtime-reference-v1' and reference['precision_approved'] is False
            and reference['publication_eligible'] is False,'Invalid candidate runtime reference')
        record=reference['object'];pin=reference['package_sha256']
        _require(record['name']=='candidate-runtime/'+pin+'.zip' and record['sha256']==pin,
            'Runtime storage identity mismatch')
        data=self.storage._get(record)
        path=Path(path)
        with path.open('xb') as handle:handle.write(data)
        manifest,_=inspect_package(path,pin)
        _require(manifest['financial_code_hash']==reference['code_hash']
            and manifest['runtime_sha256']==reference['runtime_sha256'],'Runtime reference contract mismatch')
        return manifest


def register_runtime_release(control,release,reference):
    with tempfile.TemporaryDirectory() as temporary:
        RuntimeStorage(control.store.storage).fetch(reference,Path(temporary)/'runtime.zip')
    _require(reference['code_hash']==release['code_hash'],'Release runtime code mismatch')
    return control.register(dict(release,runtime=reference))


def execute_selected(control,source,output,*,project,reconciliations=None,commentary_documents=None,
                     expected_precision_version=None):
    output=Path(output);_require(not output.exists(),'Selected execution output already exists')
    output.mkdir(parents=True)
    state=dict(status='preparing',precision_approved=False,publication_eligible=False)
    try:
        snapshot=control.current();_require(snapshot[1] is not None,'No candidate release selected')
        release=control.validate_snapshot(snapshot)
        if expected_precision_version is not None:
            _require(release['precision_version']==expected_precision_version,'Selected precision policy differs from requested skill policy')
        _require('runtime' in release,'Selected release has no executable runtime')
        reference=release['runtime']
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)/'runtime.zip'
            RuntimeStorage(control.store.storage).fetch(reference,package)
            _require(reference['code_hash']==release['code_hash'],'Selected release/runtime code mismatch')
            config=dict(project=project,bucket=control.store.storage.name,snapshot=snapshot,runtime=reference,
                binding_output=str((output/'run_binding.json').resolve()))
            state.update(release_id=release['release_id'],selection=snapshot,package_sha256=reference['package_sha256'])
            result=run_package(package,reference['package_sha256'],source,output/'execution',
                project=project,reconciliations=reconciliations,selection=config,commentary_documents=commentary_documents)
        bound=json.loads((output/'run_binding.json').read_text())
        binding=control.store.load(bound['record'])
        _require(binding==bound['body'] and binding['run_id']==result['run_id']
            and binding['code_hash']==result['financial_code_hash'] and binding['release']==snapshot[1]['release']
            and binding['event']==snapshot[1]['event'],'Selected execution binding mismatch')
        calculation=output/'execution/calculation/calculation_receipt.json'
        receipt=json.loads(calculation.read_text())
        _require(all(binding[key]==receipt['bindings'][key] for key in
            ('run_id','entity','scope','source_hash','request_hash','code_hash')),'Calculation run identity mismatch')
        state.update(status='executed',run_binding=bound,execution=result,
            package_execution_receipt_sha256=file_hash(output/'execution/package_execution_receipt.json'))
        with (output/'selected_execution_receipt.json').open('x') as handle:json.dump(state,handle,indent=2)
    except Exception as error:
        state.update(status='failed',error=str(error));raise
    finally:
        (output/'selected_execution_manifest.json').write_text(json.dumps(state,indent=2))
    return state


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True);parser.add_argument('--bucket',required=True)
    parser.add_argument('--output-dir',required=True)
    commands=parser.add_subparsers(dest='command',required=True)
    store=commands.add_parser('store');store.add_argument('--package',required=True);store.add_argument('--package-sha256',required=True)
    register=commands.add_parser('register');register.add_argument('--release-id',required=True)
    register.add_argument('--runtime-reference',required=True);register.add_argument('--reference-sha256',required=True)
    register.add_argument('--case',action='append',nargs=2,required=True)
    run=commands.add_parser('run');run.add_argument('--source-bundle',required=True);run.add_argument('--reconciliations')
    args=parser.parse_args();control=CandidateReleaseControl(GCSCandidateControlStore(args.project,args.bucket))
    control.store.ensure()
    if args.command=='run':
        result=execute_selected(control,args.source_bundle,args.output_dir,project=args.project,reconciliations=args.reconciliations)
    else:
        output=Path(args.output_dir);_require(not output.exists(),'Runtime control output already exists')
        if args.command=='store':result=RuntimeStorage(control.store.storage).store(args.package,args.package_sha256)
        else:
            _require(file_hash(args.runtime_reference)==args.reference_sha256,'Runtime reference receipt pin mismatch')
            reference=json.loads(Path(args.runtime_reference).read_text())
            release=candidate_release(args.release_id,args.case)
            record=register_runtime_release(control,release,reference);result=dict(record=record,body=dict(release,runtime=reference))
        output.mkdir(parents=True);(output/'receipt.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
