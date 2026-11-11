"""Pinned, deterministic SQL-candidate runtime packages. Never authorizes release.

Only runtime source/configuration is included; ADC, source bundles and report
outputs remain outside. Installed dependency content is locked, not just labels.
"""
import argparse
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path,PurePosixPath
import platform
import re
import subprocess
import sys
import tempfile
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from .loan_review_sources import canonical
from .warehouse_candidate import file_hash,_require,_read

ROOTS=('dbt-core','dbt-bigquery','google-cloud-bigquery','google-cloud-storage','packaging')
PYTHON_FILES=('dbt_shadow','loan_review_contract','loan_review_sources','loan_review_pipeline','review_cloud',
 'shadow_reconciliation','warehouse_candidate','credit_memo_writer','review_outputs','review_workflow',
 'warehouse_commentary','shadow_commentary','ratio_commentary_analysis','formal_commentary','filing_commentary_sources',
 'warehouse_excel','shadow_identity','warehouse_execution','precision_policy')
PROJECT="""name: sec_credit_analysis
version: '1.2.0'
config-version: 2
profile: sec_credit
model-paths: [models]
macro-paths: [macros]
test-paths: [tests]
data_tests:
  +severity: error
"""
PROFILE="""sec_credit:
  target: prod
  outputs:
    prod:
      type: bigquery
      method: oauth
      project: "{{ env_var('GCP_PROJECT_ID') }}"
      dataset: "{{ env_var('BQ_DATASET_ID') }}"
      location: "{{ env_var('BQ_LOCATION', 'US') }}"
      threads: 4
      timeout_seconds: 300
"""
DBT_ENTRY="""import os,sys
os.execv(sys.executable,[sys.executable,'-I','-B','-X','pycache_prefix='+os.environ['PYTHONPYCACHEPREFIX'],
    '-c','from dbt.cli.main import cli;cli()',*sys.argv[1:]])
"""


def digest(value):return hashlib.sha256(canonical(value).encode()).hexdigest()


def runtime_lock():
    pending=[Requirement(name) for name in ROOTS];distributions={};active={}
    while pending:
        requirement=pending.pop();name=canonicalize_name(requirement.name)
        extras=set(requirement.extras)|{''}
        if name in active and extras<=active[name]:continue
        active.setdefault(name,set()).update(extras)
        distribution=metadata.distribution(name)
        if name not in distributions:
            files={}
            _require(distribution.files is not None,'Distribution has no content inventory: '+name)
            for entry in distribution.files:
                relative=PurePosixPath(str(entry))
                if '..' in relative.parts or relative.suffix in ('.pyc','.pyo'):continue
                path=distribution.locate_file(entry)
                if path.is_file():files[str(relative)]=file_hash(path)
            _require(bool(files),'Empty dependency inventory: '+name)
            distributions[name]=dict(version=distribution.version,content_sha256=digest(files))
        for text in distribution.requires or ():
            requirement=Requirement(text)
            if requirement.marker is None or any(requirement.marker.evaluate({'extra':extra}) for extra in active[name]):
                pending.append(requirement)
    return dict(python=list(sys.version_info[:3]),python_executable_sha256=file_hash(sys.executable),
        platform=sys.platform,machine=platform.machine(),distributions=distributions)


def isolated_prefix(root):
    return [sys.executable,'-I','-B','-X','pycache_prefix='+str(Path(root).parent/'empty-cache'),'-c',
        'import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_module(sys.argv.pop(1),run_name="__main__")',
        str(Path(root).resolve())]


def package_code_hash(root):
    command=[sys.executable,'-I','-B','-c',
        'import sys;sys.path.insert(0,sys.argv[1]);from scripts.dbt_shadow import code_hash;print(code_hash())',str(Path(root).resolve())]
    result=subprocess.run(command,capture_output=True,text=True,check=True,timeout=60)
    value=result.stdout.strip()
    _require(re.fullmatch('[a-f0-9]{64}',value) is not None,'Unexpected packaged code hash')
    return value


def source_files(root,*,dbt_manifest=None,manifest_pin=None):
    root=Path(root)
    paths=[root/'scripts'/(name+'.py') for name in PYTHON_FILES]
    paths += [root/'scripts/export_loan_review_excel.mjs']
    for directory,pattern in (('models/shadow','*'),('macros','shadow_*.sql'),('tests','review_shadow_*.sql')):
        paths += [path for path in sorted((root/'references/dbt'/directory).glob(pattern)) if path.suffix in ('.sql','.yml')]
    paths += [root/'tests/fixtures/dbt_shadow/kernel_cases.json']
    files={str(path.relative_to(root)):path.read_bytes() for path in paths if path.is_file()}
    _require(all(not path.is_symlink() for path in paths),'Runtime source symlink forbidden')
    if dbt_manifest is not None:
        _require(file_hash(dbt_manifest)==manifest_pin,'Historical dbt manifest pin mismatch')
        manifest=_read(dbt_manifest)
        for name in list(files):
            if name.startswith('references/dbt/models/shadow/') and name.endswith('.sql') or name.startswith('references/dbt/tests/review_shadow_'):
                del files[name]
        for node in manifest['nodes'].values():
            name=node.get('original_file_path','')
            if name.startswith('models/shadow/') and name.endswith('.sql') or name.startswith('tests/review_shadow_'):
                _require('..' not in PurePosixPath(name).parts and '\\' not in name,'Unsafe historical source path')
                files['references/dbt/'+name]=(node['raw_code']+'\n').encode()
    files['scripts/__init__.py']=b''
    files['runtime_dbt.py']=DBT_ENTRY.encode()
    files['references/dbt/dbt_project.yml']=PROJECT.encode()
    files['references/dbt/profiles.yml']=PROFILE.encode()
    return files


def build_package(root,output,*,expected_code_hash,dbt_manifest=None,manifest_pin=None):
    _require(re.fullmatch('[a-f0-9]{64}',expected_code_hash) is not None,'Financial code hash required')
    output=Path(output);_require(not output.exists(),'Package output already exists')
    files=source_files(root,dbt_manifest=dbt_manifest,manifest_pin=manifest_pin)
    with tempfile.TemporaryDirectory() as temporary:
        source=Path(temporary)
        for name,data in files.items():
            path=source/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        # Historical SQL restoration is accepted only if the entire original
        # financial fingerprint is reproduced, including unchanged Python files.
        _require(package_code_hash(source)==expected_code_hash,'Exact financial source unavailable; cannot reconstruct this version')
    lock=runtime_lock()
    manifest=dict(format_version='candidate-runtime-v1',financial_code_hash=expected_code_hash,builder_code_hash=file_hash(__file__),runtime=lock,
        runtime_sha256=digest(lock),files={name:hashlib.sha256(data).hexdigest() for name,data in files.items()},
        precision_approved=False,publication_eligible=False)
    files['runtime_manifest.json']=canonical(manifest).encode()
    output.mkdir(parents=True)
    archive=output/'runtime.zip'
    with ZipFile(archive,'x',compression=ZIP_DEFLATED,compresslevel=9) as package:
        for name,data in sorted(files.items()):
            info=ZipInfo(name,date_time=(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            info.compress_type=ZIP_DEFLATED;package.writestr(info,data,compresslevel=9)
    receipt=dict(format_version='candidate-runtime-v1',package_sha256=file_hash(archive),financial_code_hash=expected_code_hash,
        runtime_sha256=manifest['runtime_sha256'],files=len(manifest['files']),precision_approved=False,publication_eligible=False)
    (output/'package_receipt.json').write_text(json.dumps(receipt,indent=2))
    return receipt


def inspect_package(path,pin):
    _require(file_hash(path)==pin,'Runtime package pin mismatch')
    with ZipFile(path) as archive:
        entries=archive.infolist();names=[entry.filename for entry in entries]
        _require(len(names)==len(set(names)) and len(names)<=256,'Duplicate or excessive runtime entries')
        _require(sum(entry.file_size for entry in entries)<=50_000_000,'Runtime package too large')
        for entry in entries:
            name=PurePosixPath(entry.filename)
            _require(not name.is_absolute() and '..' not in name.parts and '\\' not in entry.filename
                and ':' not in entry.filename and str(name)==entry.filename and not entry.is_dir()
                and (entry.external_attr>>16)&0o170000!=0o120000,'Unsafe runtime archive entry')
        manifest=json.loads(archive.read('runtime_manifest.json'))
        _require(manifest['format_version']=='candidate-runtime-v1'
            and manifest['precision_approved'] is False and manifest['publication_eligible'] is False,'Invalid candidate runtime')
        _require(set(names)==set(manifest['files'])|{'runtime_manifest.json'},'Runtime file coverage mismatch')
        _require({'runtime_dbt.py','scripts/__init__.py'}<=set(manifest['files']),'Missing isolated runtime entrypoint')
        _require(digest(manifest['runtime'])==manifest['runtime_sha256'],'Runtime lock checksum mismatch')
        files={name:archive.read(name) for name in manifest['files']}
        _require(all(hashlib.sha256(data).hexdigest()==manifest['files'][name] for name,data in files.items()),'Runtime file checksum mismatch')
    return manifest,files


def extract_package(path,pin,directory,*,check_environment=True):
    manifest,files=inspect_package(path,pin)
    if check_environment:_require(runtime_lock()==manifest['runtime'],'Installed runtime differs from fixed dependency content')
    directory=Path(directory);_require(not directory.exists(),'Runtime extraction output already exists')
    with tempfile.TemporaryDirectory() as temporary:
        draft=Path(temporary)
        for name,data in files.items():
            target=draft/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        _require(package_code_hash(draft)==manifest['financial_code_hash'],'Extracted financial source fingerprint mismatch')
    directory.mkdir(parents=True)
    for name,data in files.items():
        target=directory/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    return manifest


def run_package(path,pin,source,output,*,project,reconciliations=None,selection=None,commentary_documents=None):
    output=Path(output);_require(not output.exists(),'Packaged execution output already exists')
    output.mkdir(parents=True);calculation=output/'calculation'
    state=dict(status='preparing',package_sha256=pin,precision_approved=False,publication_eligible=False)
    try:
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)/'runtime';manifest=extract_package(path,pin,root)
            if selection is not None:
                # Financial source stays pinned by the ZIP. Current trusted control
                # code is separate, and its exact hashes are recorded in the receipt.
                state['orchestration']={}
                for name in ('candidate_release_control','delivery_archive','selected_runtime_worker'):
                    source_path=Path(__file__).with_name(name+'.py')
                    target=root/'scripts'/(name+'.py')
                    _require(not target.exists(),'Runtime attempts to replace orchestration')
                    target.write_bytes(source_path.read_bytes())
                    state['orchestration'][name]=file_hash(target)
                config=Path(temporary)/'selection.json';config.write_text(json.dumps(selection))
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','DBT_PROJECT_DIR':str(root/'references/dbt'),
                'DBT_PROFILES_DIR':str(root/'references/dbt'),'DBT_TARGET':'prod','DBT_PYTHON':sys.executable,
                'DBT_EXECUTABLE':str(root/'runtime_dbt.py'),'PYTHONPYCACHEPREFIX':str(Path(temporary)/'empty-cache')}
            env.pop('PYTHONPATH',None)
            command=isolated_prefix(root)+['scripts.warehouse_execution','--source-bundle',str(Path(source).resolve()),
                '--output-dir',str(calculation.resolve()),'--project',project,'--candidate-preview',
                '--kernel-cases',str(root/'tests/fixtures/dbt_shadow/kernel_cases.json')]
            if reconciliations:command+=['--reconciliations',str(Path(reconciliations).resolve())]
            if commentary_documents:command+=['--commentary-documents',str(Path(commentary_documents).resolve())]
            if selection is not None:
                index=command.index('scripts.warehouse_execution')
                command[index:index+1]=['scripts.selected_runtime_worker',str(config),file_hash(config)]
            completed=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,timeout=600)
            _require(completed.returncode==0,'Packaged execution failed; no current-code fallback: '+completed.stderr[-2000:])
            _require(package_code_hash(root)==manifest['financial_code_hash'],'Packaged source changed during execution')
        receipt=_read(calculation/'calculation_receipt.json')
        _require(receipt['bindings']['code_hash']==manifest['financial_code_hash'],'Execution did not use selected package code')
        state.update(status='executed',financial_code_hash=manifest['financial_code_hash'],runtime_sha256=manifest['runtime_sha256'],
            calculation_receipt_sha256=file_hash(calculation/'calculation_receipt.json'),run_id=receipt['bindings']['run_id'])
        (output/'package_execution_receipt.json').write_text(json.dumps(state,indent=2))
    except Exception as error:
        state.update(status='failed',error=str(error));raise
    finally:
        (output/'package_execution_manifest.json').write_text(json.dumps(state,indent=2))
    return state


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    build=commands.add_parser('build');build.add_argument('--source-root',default=str(Path(__file__).resolve().parents[1]))
    build.add_argument('--expected-code-hash',required=True);build.add_argument('--dbt-manifest');build.add_argument('--manifest-pin')
    run=commands.add_parser('run')
    for field in ('package','package-sha256','source-bundle','project'):run.add_argument('--'+field,required=True)
    run.add_argument('--reconciliations')
    for command in (build,run):command.add_argument('--output-dir',required=True)
    args=parser.parse_args()
    if args.command=='build':result=build_package(args.source_root,args.output_dir,expected_code_hash=args.expected_code_hash,
        dbt_manifest=args.dbt_manifest,manifest_pin=args.manifest_pin)
    else:result=run_package(args.package,args.package_sha256,args.source_bundle,args.output_dir,project=args.project,
        reconciliations=args.reconciliations)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
