"""Trusted orchestration around an isolated, pinned financial runtime."""
import json
from pathlib import Path
import sys

from . import warehouse_execution
from .candidate_release_control import CandidateReleaseControl,GCSCandidateControlStore
from .warehouse_candidate import _require,file_hash


def install_binding(config):
    store=GCSCandidateControlStore(config['project'],config['bucket']);store.ensure()
    control=CandidateReleaseControl(store)
    original=warehouse_execution.ShadowWarehouse
    class BoundWarehouse:
        def __init__(self,project,run_id):
            _require(project==config['project'],'Execution project changed')
            self.project,self.run_id=project,run_id
            self.dataset='sec_review_shadow_'+run_id
        def execute(self,records,directory):
            metadata=next(value for kind,_,value in records if kind=='metadata')
            release=control.validate_snapshot(config['snapshot'])
            _require(release['runtime']==config['runtime'],'Selected runtime reference changed')
            for field in ('code_hash','formula_version','policy_version','precision_version'):
                _require(metadata[field]==release[field],'Execution release contract differs: '+field)
            _require(metadata['run_id']==self.run_id,'Execution run changed')
            record,binding=control.bind_run(self.run_id,**{key:metadata[key] for key in
                ('entity','scope','source_hash','request_hash')},selection_snapshot=config['snapshot'])
            path=Path(config['binding_output'])
            with path.open('x') as handle:json.dump(dict(record=record,body=binding),handle,indent=2)
            # Construct the real client and write warehouse data only after immutable binding.
            return original(self.project,self.run_id).execute(records,directory)
    warehouse_execution.ShadowWarehouse=BoundWarehouse


def main():
    config_path=Path(sys.argv.pop(1));pin=sys.argv.pop(1)
    _require(file_hash(config_path)==pin,'Selected execution configuration pin mismatch')
    config=json.loads(config_path.read_text());install_binding(config)
    warehouse_execution.main()


if __name__=='__main__':main()
