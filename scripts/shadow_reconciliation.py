"""Metadata ingestion and strict comparison for independently evaluated SQL bridges.

Canonical JSON binding hashes preserve reviewed claims without interpreting them
as arithmetic or approvals. SQL checks those bindings, source lineage and bounds.
"""
from dataclasses import replace
from datetime import date
import json
from decimal import Decimal

from .loan_review_contract import Evidence, validate_report, AVAILABLE, Status, calculate_fact
from .loan_review_pipeline import acceptance_result, automatic_reconciliation_checks, verify_reconciliation, FORMULA_VERSION
from .loan_review_sources import canonical, digest


def prepare_reviews(report, envelope, *, as_of=None):
    if envelope is None:
        return report, [], []
    if not isinstance(envelope, dict) or set(envelope) != {'schema_version', 'checks', 'evidence'} or envelope['schema_version'] != 1:
        raise ValueError('Reconciliations require schema_version=1, checks and evidence')
    if not isinstance(envelope['checks'], list) or not isinstance(envelope['evidence'], dict):
        raise ValueError('Invalid reconciliation collection types')
    evidence = dict(report.evidence)
    for key, value in envelope['evidence'].items():
        row = dict(value)
        row['document_date'] = date.fromisoformat(row['document_date'])
        row['period_roles'] = tuple(row['period_roles'])
        item = Evidence(**row)
        if item.id != key or key in evidence:
            raise ValueError('Review evidence identity collides with existing evidence')
        if as_of is not None and item.document_date>date.fromisoformat(str(as_of)):
            raise ValueError('Review evidence is later than analysis as_of')
        evidence[key] = item
    report = replace(report, evidence=evidence)
    validate_report(report, expected_mode=report.mode)
    records, seen = [], set()
    for check in envelope['checks']:
        key = f"{check['kind']}:{check['period_role']}"
        if key in seen:
            raise ValueError('Duplicate reconciliation identity')
        seen.add(key)
        # Structural canonicalization only; no computed amount or PASS is trusted here.
        binding = dict(kind=check['kind'], period_role=check['period_role'], terms=check.get('terms'),
            reported_fact_id=check.get('reported_fact_id'), currency=report.currency,
            scale=str(report.scale), tolerance=str(Decimal(str(check.get('tolerance', 0)))))
        records.append(('reconciliation_review', key, dict(check, binding_hash=digest(binding))))
    for key, item in evidence.items():
        row = dict(id=item.id, entity=item.entity, scope=item.scope,
            kind=item.kind, period_roles=list(item.period_roles), content=item.content,
            source_id=item.source_id, version=item.version, locator=item.locator,document_date=str(item.document_date))
        try:
            parsed = json.loads(item.content)
        except (ValueError, TypeError):
            parsed = None
        row['binding_hash'] = digest(parsed) if isinstance(parsed, dict) else None
        records.append(('review_evidence', key, row))
    return report, envelope['checks'], records


def baseline_reviewed_cash(report, checks):
    """Independent migration baseline; never used by the warehouse reader."""
    for check in checks:
        if check.get('kind')!='cash_bridge' or not verify_reconciliation(report,check).get('verified'):
            continue
        fid = 'cash_change:'+check['period_role']
        target = report.facts.get(fid)
        if target is None or target.status in (*AVAILABLE,Status.CONFLICT,Status.NOT_APPLICABLE):
            continue
        # Definition evidence must bind this complete bridge, not another review.
        binding = dict(kind=check['kind'],period_role=check['period_role'],terms=check['terms'],
            reported_fact_id=check['reported_fact_id'],currency=report.currency,scale=str(report.scale),
            tolerance=str(Decimal(str(check.get('tolerance',0)))))
        definitions = sorted(eid for eid in check['evidence_ids'] if report.evidence[eid].kind=='definition'
            and report.evidence[eid].content and _matches_binding(report.evidence[eid].content,binding))
        ids = ('ending_cash:'+target.period_role,'beginning_cash:'+target.period_role)
        if not definitions or check['reported_fact_id']!=ids[0] or check['terms'][0]['fact_id']!=ids[1]:
            continue
        report = replace(report,facts={**report.facts,fid:replace(target,evidence_ids=tuple(definitions))})
        report = calculate_fact(report,fid,input_ids=ids,formula_version=FORMULA_VERSION)
    return report


def _matches_binding(content,binding):
    try:
        return canonical(json.loads(content))==canonical(binding)
    except (ValueError,TypeError):
        return False


def baseline_reconciliations(report, checks, original_acceptance):
    if not checks:
        return original_acceptance
    merged = {(c['kind'], c['period_role']): c for c in automatic_reconciliation_checks(report)}
    merged.update({(c['kind'], c['period_role']): c for c in checks})
    return acceptance_result(report, list(merged.values()), original_acceptance.get('source_limitations', ()))


def compare_acceptance(baseline, rows, *, bindings):
    """Compare financial readiness separately from unapproved cutover flags."""
    if len(rows) != 1:
        raise ValueError('Expected one warehouse acceptance row')
    row = rows[0]
    if any(row.get(key) != value for key, value in bindings.items()):
        raise ValueError('Warehouse acceptance identity mismatch')
    if any(row.get(key) is not False for key in ('precision_approved', 'final_report_accepted', 'publication_eligible')):
        raise ValueError('Shadow acceptance cannot grant publication')
    expected = dict(substantive_data_ready=baseline['substantive_data_ready'],
        unavailable_fact_ids=sorted(item['fact_id'] for item in baseline['missing_or_pending']),
        acceptance_blockers=sorted(baseline['acceptance_blockers']))
    actual = dict(substantive_data_ready=row['substantive_data_ready'],
        unavailable_fact_ids=sorted(row['unavailable_fact_ids']), acceptance_blockers=sorted(row['acceptance_blockers']))
    differing = [key for key in expected if expected[key] != actual[key]]
    return dict(mismatches=len(differing), differing_fields=differing, python=expected, dbt=actual,
                precision_approved=False, publication_eligible=False)


def compare_reconciliations(baseline, rows, *, run_id, entity):
    expected = {(c['kind'], c['period_role']): c for c in baseline['reconciliations']}
    actual = {}
    for raw in rows:
        row = dict(raw)
        if row.get('run_id') != run_id or row.get('entity') != entity:
            raise ValueError('Reconciliation warehouse identity mismatch')
        key = (row['kind'], row['period_role'])
        if key in actual:
            raise ValueError('Duplicate warehouse reconciliation')
        if row.get('publication_eligible') is not False:
            raise ValueError('Shadow reconciliation cannot grant publication')
        actual[key] = row
    details = []
    for key in sorted(set(expected) | set(actual)):
        left, right = expected.get(key), actual.get(key)
        mismatches = []
        if left is None or right is None:
            mismatches.append('missing_or_unexpected_check')
        else:
            for field in ('status', 'verified'):
                if left.get(field, False) != right.get(field):
                    mismatches.append(field)
            # Invalid/unreviewed checks keep their submitted claims in the Python audit
            # result. Compare numeric results only when both independently verified.
            if left.get('verified') and right.get('verified'):
                for field in ('calculated_value', 'reported_value', 'difference', 'tolerance'):
                    a, b = left.get(field), right.get(field)
                    if a is None or b is None or Decimal(str(a)) != Decimal(str(b)):
                        mismatches.append(field)
        details.append(dict(kind=key[0], period_role=key[1], differing_fields=mismatches,
            python=left, dbt=right))
    return dict(checks_compared=len(details), mismatches=sum(bool(d['differing_fields']) for d in details),
        precision_approved=False, publication_eligible=False, details=details)
