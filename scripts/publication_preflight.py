"""Pinned candidate publication diagnostics. Never grants publication authority.

This intentionally has no approval switch: M4 authorization, release identity,
delivery storage and published IAM must exist before a publisher can use it.
"""
import argparse
import json
from pathlib import Path

from .warehouse_candidate import file_hash, read_candidate, _read, _require
from .precision_policy import VERSION as APPROVED_IMPLEMENTATION_POLICY


def inspect_candidate(directory, *, receipt_sha256):
    directory = Path(directory)
    report, receipt = read_candidate(directory, expected_receipt_sha256=receipt_sha256)
    acceptance = _read(directory / 'warehouse_acceptance.json')[0]
    comparison = receipt['comparison']
    approved_policy=receipt['bindings']['precision_version']==APPROVED_IMPLEMENTATION_POLICY
    canonical_verified=approved_policy and comparison.get('canonical_precision_mismatches')==0
    blockers = []
    def block(code, detail):
        blockers.append(dict(code=code, detail=detail))
    if receipt.get('precision_approved') is not True:
        block('precision_release_not_activated' if approved_policy else 'precision_unapproved',
            receipt['bindings']['precision_version'])
    if approved_policy and not canonical_verified:
        block('canonical_precision_validation_missing','This receipt does not establish canonical migration equality')
    if comparison.get('status')=='not_run':
        block('migration_comparison_not_run','This SQL-only execution is not migration comparison evidence')
    if not acceptance['substantive_data_ready']:
        block('financial_acceptance_blocked', acceptance['acceptance_blockers'])
    for key in ('mismatches', 'reconciliation_mismatches', 'acceptance_mismatches', 'commentary_mismatches'):
        if comparison.get(key, 0):
            block('comparison_mismatch', dict(kind=key, count=comparison[key]))
    for key in ('numeric_differences', 'commentary_numeric_differences'):
        if comparison.get(key, 0) and not canonical_verified:
            block('unapproved_precision_differences', dict(kind=key, count=comparison[key]))
    # Shadow receipts cannot assert these gates, even if a caller changes flags.
    for code in ('release_authorization_missing', 'delivery_receipt_missing',
                 'persistent_storage_unverified', 'published_consumer_iam_unverified'):
        block(code, 'Not established by a shadow calculation receipt')
    return dict(schema_version=1, kind='publication-preflight', status='blocked',
                bindings=receipt['bindings'], calculation_receipt_sha256=receipt_sha256,
                checker_code_sha256=file_hash(__file__), facts=len(report.facts),
                financial_readiness=acceptance['substantive_data_ready'], blockers=blockers,
                precision_policy_status='approved-for-shadow-validation' if approved_policy else 'unapproved',
                canonical_precision_verified=canonical_verified,
                legacy_precision_changes={key:comparison.get(key,0) for key in ('numeric_differences','commentary_numeric_differences')},
                publication_eligible=False, publication_receipt=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-dir', required=True)
    parser.add_argument('--receipt-sha256', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args(argv)
    result = inspect_candidate(args.candidate_dir, receipt_sha256=args.receipt_sha256)
    target = Path(args.output_dir)
    _require(not target.exists(), 'Preflight output already exists')
    target.mkdir(parents=True)
    (target / 'publication_preflight.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2  # A diagnostic file is not a successful publication.


if __name__ == '__main__':
    raise SystemExit(main())
