"""Synthetic native execution proof with Python financial functions disabled."""
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
from unittest.mock import patch

from .loan_review_sources import load_json
from .warehouse_execution import execute_candidate
from .warehouse_candidate import _require

DISABLED = (
    'scripts.precision_policy.formula_value',
    'scripts.precision_policy.q18',
    'scripts.precision_policy.canonical_baseline',
    'scripts.dbt_shadow.report_from_source_bundle',
    'scripts.loan_review_pipeline.report_from_source_bundle',
    'scripts.loan_review_pipeline.complete_report',
    'scripts.loan_review_pipeline.adopt_inputs',
    'scripts.loan_review_pipeline.calculate_report',
    'scripts.loan_review_pipeline.calculate_fact',
    'scripts.loan_review_pipeline.calculate_identity',
    'scripts.loan_review_pipeline.approved_formula_value',
    'scripts.loan_review_pipeline.normalize_value',
    'scripts.loan_review_pipeline.acceptance_result',
    'scripts.loan_review_pipeline.validate_arithmetic',
    'scripts.loan_review_pipeline.verify_reconciliation',
    'scripts.loan_review_pipeline.automatic_reconciliation_checks',
    'scripts.loan_review_contract.calculate_fact',
    'scripts.loan_review_contract.calculate_identity',
    'scripts.loan_review_contract.approved_formula_value',
    'scripts.loan_review_sources.normalize_value',
    'scripts.shadow_reconciliation.calculate_fact',
    'scripts.shadow_reconciliation.baseline_reviewed_cash',
    'scripts.shadow_reconciliation.baseline_reconciliations',
    'scripts.shadow_reconciliation.compare_acceptance',
    'scripts.shadow_reconciliation.compare_reconciliations',
    'scripts.shadow_commentary.compare_commentary',
    'scripts.dbt_shadow.compare_facts',
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-bundle',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--project',default='focus-heuristic-438521-v4')
    parser.add_argument('--reconciliations')
    parser.add_argument('--commentary-documents')
    parser.add_argument('--kernel-cases',required=True)
    args = parser.parse_args(argv)
    bundle = load_json(args.source_bundle)
    _require(bundle['entity']=='SYNTHETIC-ONLY','Native disabled-function proof requires synthetic data')
    with ExitStack() as stack:
        for name in DISABLED:
            stack.enter_context(patch(name,side_effect=AssertionError('Forbidden Python financial call: '+name)))
        result = execute_candidate(bundle,args.output_dir,project=args.project,
            reconciliations=load_json(args.reconciliations) if args.reconciliations else None,
            commentary_documents=load_json(args.commentary_documents) if args.commentary_documents else None,
            kernels=load_json(args.kernel_cases),candidate_preview=True)
    proof = dict(status='passed',run_id=result['run_id'],facts=result['facts'],
        calculation_receipt_sha256=result['calculation_receipt_sha256'],disabled_functions=list(DISABLED),
        baseline_comparison='not_run',precision_approved=False,publication_eligible=False)
    (Path(args.output_dir)/'disabled_functions_proof.json').write_text(json.dumps(proof,indent=2))
    print(json.dumps(proof,indent=2))


if __name__=='__main__':main()
