"""Deterministic balance-sheet context for commentary; never changes Report facts.

Components are individual observations, not an additive chart of accounts. Unknown
company tags stay available as filing text rather than receiving guessed categories.
"""
from decimal import Decimal, localcontext

try:
    from .loan_review_contract import AVAILABLE
    from .loan_review_sources import number, normalize_value
except ImportError:
    from loan_review_contract import AVAILABLE
    from loan_review_sources import number, normalize_value

VERSION = 'balance-sheet-commentary-v1'
# One identity per concept; overlapping aggregates are deliberately separate.
BALANCE_CONCEPTS = {
    'CashAndCashEquivalentsAtCarryingValue': ('cash', 'current_assets'),
    'ShortTermInvestments': ('short_term_investments', 'current_assets'),
    'AccountsReceivableNetCurrent': ('accounts_receivable_net', 'current_assets'),
    'InventoryNet': ('inventory', 'current_assets'),
    'PrepaidExpenseAndOtherAssetsCurrent': ('prepaid_and_other_current_assets', 'current_assets'),
    'OtherAssetsCurrent': ('other_current_assets', 'current_assets'),
    'AccountsPayableCurrent': ('accounts_payable', 'current_liabilities'),
    'AccruedIncomeTaxesCurrent': ('income_taxes_payable', 'current_liabilities'),
    'EmployeeRelatedLiabilitiesCurrent': ('accrued_compensation', 'current_liabilities'),
    'OtherLiabilitiesCurrent': ('other_current_liabilities', 'current_liabilities'),
    'OperatingLeaseLiabilityCurrent': ('operating_lease_current', 'current_liabilities'),
    'LongTermDebtCurrent': ('current_maturities_ltd', 'current_liabilities'),
    'LongTermDebtNoncurrent': ('long_term_liabilities', 'total_liabilities'),
    'LongTermDebt': ('long_term_debt_aggregate', 'total_liabilities'),
    'ShortTermBorrowings': ('short_term_loans', 'current_liabilities'),
    'OperatingLeaseLiabilityNoncurrent': ('operating_lease_noncurrent', 'total_liabilities'),
    'OtherLiabilitiesNoncurrent': ('other_noncurrent_liabilities', 'total_liabilities'),
    'StockholdersEquity': ('stockholders_equity', 'net_worth'),
    'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest': ('equity_including_nci', 'net_worth'),
    'RetainedEarningsAccumulatedDeficit': ('retained_earnings', 'net_worth'),
    'TreasuryStockValue': ('treasury_stock', 'net_worth'),
}
TOTAL_CONCEPTS = {
    'AssetsCurrent': 'current_assets', 'LiabilitiesCurrent': 'current_liabilities',
    'Assets': 'total_assets', 'Liabilities': 'total_liabilities',
}
RATIOS = {
    'current_ratio': ('current_assets', 'current_liabilities'),
    'quick_ratio': ('quick_assets', 'current_liabilities'),
    'debt_ratio': ('total_liabilities', 'net_worth'),
}


def comparison_roles(report):
    return ('fy_t_minus_1', 'fy_t') if report.mode.value == 'annual' else ('latest_fy_end', 'current_interim')


def ratio_fact_ids(report, topic):
    metrics = ('current_ratio', 'quick_ratio', 'current_assets', 'quick_assets', 'current_liabilities') if topic == 'liquidity' else (
        'debt_ratio', 'total_liabilities', 'net_worth', 'total_assets', 'total_debt')
    ids = []
    for metric in metrics:
        for role in comparison_roles(report):
            fid = metric + ':' + role
            fid = fid if fid in report.facts else 'input:' + fid
            if fid in report.facts and report.facts[fid].status in AVAILABLE:
                ids.append(fid)
    return ids


def _fact(report, metric, role):
    fact = report.facts.get(metric + ':' + role) or report.facts.get('input:' + metric + ':' + role)
    if fact is None or fact.status not in AVAILABLE:
        return None
    return fact


def _change(before, after):
    if before is None or after is None:
        return dict(before=None if before is None else str(before), after=None if after is None else str(after),
                    change=None, growth=None, status='missing')
    with localcontext() as ctx:
        ctx.prec = 50
        return dict(before=str(before), after=str(after), change=str(after-before),
                    growth=str((after-before)/before) if before > 0 else None, status='available')


def build_ratio_analysis(report, observations=(), documents=()):
    """Compare exact endpoints and rank individual movements without inventing totals.

    observations come from the validated source bundle or validated filing documents.
    Conflicting concepts/versions remain unusable; explicit amendments alone may
    supersede the same concept. Partial component coverage is always labelled.
    """
    roles = comparison_roles(report)
    periods = {p.role: p for p in report.periods}
    result = dict(version=VERSION, mode=report.mode.value, entity=report.entity, currency=report.currency,
                  scale=str(report.scale), period_roles=list(roles),
                  dates={r: periods[r].end.isoformat() if periods[r].end else None for r in roles},
                  ratios={}, components=[], source_total_checks=[], limitations=[], document_ids=[d['id'] for d in documents])
    for metric, (num, den) in RATIOS.items():
        values = [_fact(report, metric, r) for r in roles]
        entry = _change(*(f.value if f else None for f in values))
        entry['fact_ids'] = [f.id for f in values if f]
        entry['numerator'] = dict(metric=num, **_change(*((_fact(report, num, r).value if _fact(report, num, r) else None) for r in roles)))
        entry['denominator'] = dict(metric=den, **_change(*((_fact(report, den, r).value if _fact(report, den, r) else None) for r in roles)))
        entry['definition'] = next((f.definition for f in values if f), '')
        if all(f and f.value > 0 for f in [_fact(report, num, roles[0]), _fact(report, num, roles[1]),
                                          _fact(report, den, roles[0]), _fact(report, den, roles[1])]):
            ng = number(entry['numerator']['growth']); dg = number(entry['denominator']['growth'])
            entry['relative_growth'] = 'numerator_faster' if ng > dg else 'denominator_faster' if ng < dg else 'equal'
        else:
            entry['relative_growth'] = 'not_comparable'
        result['ratios'][metric] = entry

    grouped = {}
    for observation in observations:
        concept = observation.get('tag', '')
        # Custom taxonomy concepts have no approved component classification.
        if observation.get('namespace') != 'us-gaap' or concept not in set(BALANCE_CONCEPTS) | set(TOTAL_CONCEPTS):
            continue
        if observation.get('status') != 'sourced' or observation.get('start') is not None or observation.get('period_kind') != 'instant':
            continue
        if observation.get('entity') != report.entity or observation.get('scope') != report.scope:
            continue
        if observation.get('unit') != report.currency:
            result['limitations'].append('Component currency mismatch: ' + concept)
            continue
        for role in roles:
            if observation.get('end') == result['dates'][role] and observation.get('end') is not None:
                grouped.setdefault((concept, role), []).append(observation)
    selected = {}
    for key, candidates in grouped.items():
        latest = max(c['document_date'] for c in candidates)
        latest_candidates = [c for c in candidates if c['document_date'] == latest]
        if all(c.get('filing_type') in ('10-K/A', '10-Q/A') for c in latest_candidates):
            candidates = latest_candidates
        values = {normalize_value(c['value'], c['scale'], report.scale) for c in candidates}
        if len(values) != 1:
            result['limitations'].append('Conflicting source values: ' + key[0] + '/' + key[1])
            continue
        selected[key] = (next(iter(values)), candidates)
    for concept, metric in TOTAL_CONCEPTS.items():
        for role in roles:
            source = selected.get((concept, role)); canonical = _fact(report, metric, role)
            difference = source[0] - canonical.value if source and canonical else None
            result['source_total_checks'].append(dict(metric=metric, period_role=role,
                status='missing' if difference is None else 'matched' if difference == 0 else 'conflict',
                difference=None if difference is None else str(difference)))
    for concept in sorted({key[0] for key in grouped if key[0] in BALANCE_CONCEPTS}):
        pair = [selected.get((concept, r)) for r in roles]
        field, group = BALANCE_CONCEPTS[concept]
        entry = dict(concept=concept, field_name=field, group=group,
                     **_change(*(p[0] if p else None for p in pair)),
                     sources={r: [dict(id=c['id'], source_id=c['source_id'], version=c['version'],
                         locator=c['locator'], document_date=c['document_date']) for c in p[1]] if p else []
                         for r, p in zip(roles, pair)})
        result['components'].append(entry)
    result['components'].sort(key=lambda c: (c['change'] is None, -abs(number(c['change'])) if c['change'] is not None else Decimal(0), c['concept']))
    result['component_coverage'] = {group: 'partial_not_reconciled' for group in ('current_assets', 'current_liabilities', 'total_liabilities', 'net_worth')}
    result['component_reconciliations'] = []
    # Only the two current groups have a bounded component set here. Noncurrent
    # debt/equity aggregates are never added to their own underlying subaccounts.
    for group in ('current_assets', 'current_liabilities'):
        checks = []
        for role in roles:
            canonical = _fact(report, group, role)
            lines = [(concept, value[0]) for (concept, r), value in selected.items()
                     if r == role and concept in BALANCE_CONCEPTS and BALANCE_CONCEPTS[concept][1] == group]
            concepts = {c for c, _ in lines}
            overlap = {'PrepaidExpenseAndOtherAssetsCurrent', 'OtherAssetsCurrent'} <= concepts
            total_conflict = any(c['metric'] == group and c['period_role'] == role and c['status'] == 'conflict'
                                 for c in result['source_total_checks'])
            amount = sum((v for _, v in lines), Decimal(0)) if lines and not overlap else None
            residual = canonical.value - amount if canonical and amount is not None else None
            status = ('conflict' if total_conflict else 'overlapping_components' if overlap else
                      'matched_selected_lines' if residual == 0 else 'partial_not_reconciled')
            checks.append(status)
            result['component_reconciliations'].append(dict(group=group, period_role=role, status=status,
                selected_concepts=sorted(concepts), selected_sum=None if amount is None else str(amount),
                canonical_total=str(canonical.value) if canonical else None,
                unexplained_residual=None if residual is None else str(residual)))
        if all(c == 'matched_selected_lines' for c in checks):
            result['component_coverage'][group] = 'matched_selected_lines'

    result['limitations'].extend([
        'Components are ranked individually. Only the explicitly listed current-group lines enter component_reconciliations; other aggregates/subtotals may overlap. A zero residual confirms arithmetic for selected lines, not an exhaustive chart of accounts.',
        'Quick assets follow canonical facts and their approved definition; cash/receivables are not automatically assumed to equal quick assets or be unrestricted.',
        'Balance-sheet arithmetic explains composition, not the business cause. Cite a note or management statement for transaction/event attribution.',
        'Debt ratio is total liabilities / net worth, distinct from interest-bearing total debt. Explain both liabilities and equity; new debt proceeds are not net debt growth.',
    ])
    return result
