"""Source categories and disjoint sum routes for as-reported Total Debt.

This registry maps borrowing concepts, never total/current liabilities. Long-term
aggregates include their current portion, so they are exclusive of that portion.
"""
import re

VERSION = 'as-reported-debt-2026-11-07'
DEBT_TAGS = {
    'total_debt': {'DebtAndCapitalLeaseObligations'},
    'short_term_debt': {'DebtCurrent'},
    'short_term_borrowings': {'ShortTermBorrowings', 'ShortTermNotesPayable'},
    'current_maturities_debt': {'LongTermDebtCurrent', 'LongTermDebtAndFinanceLeaseObligationsCurrent',
                                'LongTermDebtAndCapitalLeaseObligationsCurrent'},
    'long_term_debt': {'LongTermDebtNoncurrent', 'LongTermDebtAndFinanceLeaseObligationsNoncurrent',
                       'LongTermDebtAndCapitalLeaseObligations'},
    'long_term_debt_including_current': {'LongTermDebt', 'LongTermDebtAndFinanceLeaseObligations',
                                        'LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities'},
}
DEBT_FIELDS = {
    'total_debt': ('long_term_debt_aggregate_alt2',),  # Retained raw-ledger name; tag identifies total debt.
    'short_term_debt': ('debt_current_fallback',),
    'short_term_borrowings': ('short_term_loans', 'short_term_notes_payable'),
    'current_maturities_debt': ('current_maturities_ltd', 'current_maturities_ltd_alt', 'current_maturities_ltd_alt2'),
    'long_term_debt': ('long_term_liabilities', 'long_term_liabilities_alt', 'long_term_liabilities_alt2'),
    'long_term_debt_including_current': ('long_term_debt_aggregate', 'long_term_debt_aggregate_alt', 'long_term_debt_aggregate_alt3'),
}
DEBT_SUM_INPUTS = (('short_term_debt', 'long_term_debt'),
                   ('short_term_borrowings', 'long_term_debt_including_current'))
WORKBOOK_DEBT_LABELS = {'total_debt': 'Total Debt', 'short_term_debt': 'Short-term Debt', 'long_term_debt': 'Long-term Debt'}


def supported_debt_source(candidate, metric):
    """Category/provenance checks replace literal definition-text equality."""
    if metric not in DEBT_TAGS:
        return False
    if candidate.get('origin') == 'sec':
        return candidate.get('namespace') == 'us-gaap' and candidate.get('tag') in DEBT_TAGS[metric]
    if candidate.get('origin') == 'supplement':
        return candidate.get('metric') == metric and candidate.get('verification', {}).get('method') == 'checked_against_source'
    return (candidate.get('source_id', '').startswith('workbook:')
            and candidate.get('definition') == WORKBOOK_DEBT_LABELS.get(metric))


def debt_amount_basis(candidate):
    basis = candidate.get('basis', '').lower()
    principal = 'principal' in basis or '本金' in basis
    if not basis:
        principal = 'principal' in candidate.get('definition', '').lower() or '本金' in candidate.get('definition', '')
    return 'principal' if principal else 'carrying'


def compatible_debt_bases(facts):
    bases = {basis for f in facts for basis in re.findall(r'As-reported (carrying|principal) amount', f.basis)}
    return len(bases) <= 1


def reported_debt_basis(candidates):
    labels = sorted({c.get('tag') or c.get('definition', '') for c in candidates})
    bases = {debt_amount_basis(c) for c in candidates}
    kind = next(iter(bases)) if len(bases) == 1 else 'mixed'
    return ('As-reported ' + kind + ' amount; lease scope follows disclosed borrowing lines; '
            'no gross-up. Sources: ' + '; '.join(labels))
