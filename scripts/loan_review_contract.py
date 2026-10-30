"""Loan Review v1.0 shared contract and approved calculation API.
The strict pipeline uses these records; legacy formatting remains separate.

Pure standard-library records, fixed layouts and structural validation. No extraction,
prose generation, rendering, or delivery approval happens here. Explicit calculation
uses the existing Fact/Report contract and never approves pending definitions.
Numbers use Decimal; percentages are unscaled fractions (0.25 renders as 25%).
See references/output-format.md for the API, rule mapping and validation limits.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Mapping


class ContractError(ValueError):
    """A rule violation; messages name the failing record and acceptance rule."""


class Mode(str, Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"


class Status(str, Enum):
    SOURCED = "sourced"
    CALCULATED = "calculated"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"
    CONFLICT = "conflict"
    NOT_CALCULABLE = "not_calculable"


AVAILABLE = (Status.SOURCED, Status.CALCULATED)
ANNUAL_ROLES = ("fy_t_minus_3", "fy_t_minus_2", "fy_t_minus_1", "fy_t")
QUARTERLY_ROLES = ("earlier_fy_end", "prior_interim", "latest_fy_end", "current_interim")


@dataclass(frozen=True)
class MetricSpec:
    label: str
    unit: str
    period_kind: str
    definition: str
    rule: str
    formula: str | None = None
    inputs: tuple[str, ...] = ()
    pending: tuple[str, ...] = ()


# Definitions apply to the new report, not to existing shared dashboard KPI names.
METRICS = {
    "revenue": MetricSpec("Revenues", "money", "duration", "Source revenue or net sales", "FMT-A1/FMT-Q1"),
    "cost_of_revenue": MetricSpec("Cost of revenues", "money", "duration", "Source cost of revenue, sales or services", "FMT-A1/FMT-Q1"),
    "gross_profit": MetricSpec("Gross profit", "money", "duration", "Source gross profit; derive only with verified identity", "CALC-14"),
    "operating_expense": MetricSpec("Operating expense", "money", "duration", "Operating expense excluding cost of revenue; verified scope", "CALC-14"),
    "operating_income": MetricSpec("Operating income", "money", "duration", "Source operating profit", "FMT-A1/FMT-Q1"),
    "interest_expense": MetricSpec("Interest expense", "money", "duration", "Gross expensed interest without netting interest income; exclude separately capitalized interest", "FMT-A1/FMT-A4/FMT-Q1", pending=("DEC-05",)),
    "pretax_profit": MetricSpec("Income before taxes", "money", "duration", "Source pre-tax profit; preserve signed tax benefits in identities", "CALC-14"),
    "income_tax": MetricSpec("Income tax expense", "money", "duration", "Signed income tax expense or benefit", "CALC-14"),
    "net_income": MetricSpec("Net income", "money", "duration", "Source net income with consolidation scope", "FMT-A1/FMT-Q1"),
    "beginning_cash": MetricSpec("Beginning balance", "money", "opening", "Cash at start of fiscal period, consistent cash definition", "CALC-15"),
    "cfo": MetricSpec("Operating activities", "money", "duration", "Net cash inflow/outflow from operating activities", "CF-03"),
    "cfi": MetricSpec("Investing activities", "money", "duration", "Net cash inflow/outflow from investing activities", "FMT-A2"),
    "cff": MetricSpec("Financing activities", "money", "duration", "Net cash inflow/outflow from financing activities", "FMT-A2"),
    "ending_cash": MetricSpec("Ending balance", "money", "instant", "Cash at fiscal period end, consistent cash definition", "CALC-15"),
    "cash_change": MetricSpec("Change", "money", "duration", "Ending cash - beginning cash; full FX/restricted-cash bridge required", "CALC-15", "CASH-CHANGE-v1", ("ending_cash", "beginning_cash")),
    "current_ratio": MetricSpec("Current ratio", "percent", "instant", "Current Assets / Current Liabilities", "CF-01", "CF-01", ("current_assets", "current_liabilities")),
    "quick_ratio": MetricSpec("Quick ratio", "percent", "instant", "Quick Assets / Current Liabilities", "CF-02", "CF-02", ("quick_assets", "current_liabilities"), ("DEC-01",)),
    "cash_flow_ratio": MetricSpec("Cash flow ratio", "percent", "duration", "CFO / Current Liabilities", "CF-03", "CF-03", ("cfo", "current_liabilities")),
    "debt_ratio": MetricSpec("Debt ratio", "percent", "instant", "Total Liabilities / Net Worth", "CF-06", "CF-06", ("total_liabilities", "net_worth"), ("DEC-02",)),
    "interest_coverage": MetricSpec("Interest coverage ratio", "multiple", "duration", "(Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest)", "CF-04", "CF-04", ("pretax_profit", "interest_expense", "capitalized_interest"), ("DEC-05",)),
    "total_debt": MetricSpec("Total debt", "money", "instant", "Consolidated interest-bearing borrowings, bonds and finance lease liabilities, including current portions once; exclude operating lease liabilities and trade payables", "CALC-09", pending=("DEC-02",)),
    "debt_service": MetricSpec("Debt service", "money", "duration", "Pending approved debt-service definition; no CapEx proxy", "CALC-10", pending=("DEC-03",)),
    "ltm_ebitda": MetricSpec("LTM EBITDA", "money", "ltm", "Standard EBITDA: Net Income + Interest + Taxes + D&A", "CALC-11/CALC-12", None, ("net_income", "interest_expense", "income_tax", "da"), ("DEC-06",)),
    "ebitda_basis": MetricSpec("EBITDA basis", "text", "ltm", "Source and actual EBITDA definition, including adjustments", "FMT-A4/FMT-Q3", pending=("DEC-06",)),
    "total_leverage": MetricSpec("Total leverage ratio", "multiple", "ltm", "Total debt / applicable LTM EBITDA", "CALC-09", "LEVERAGE-v1", ("total_debt", "ltm_ebitda"), ("DEC-02", "DEC-06")),
    "ebitda_interest": MetricSpec("EBITDA / Interest expense", "multiple", "duration", "(Pre-tax Profit + Interest Expense + D&A) / (Interest Expense + Capitalized Interest)", "CF-05", "CF-05", ("pretax_profit", "interest_expense", "da", "capitalized_interest"), ("DEC-05",)),
    "dscr": MetricSpec("Debt service coverage ratio", "multiple", "duration", "CFADS / Debt Service; CFADS and debt-service components pending confirmation", "CALC-10", pending=("DEC-03",)),
    # Narrative calculations are supporting facts, not extra report rows.
    "revenue_growth": MetricSpec("Revenue growth rate", "percent", "duration", "(Current Year Revenues - Previous Year Revenues) / Previous Year Revenues", "CF-09", "CF-09", ("revenue", "revenue")),
    "gross_margin": MetricSpec("Gross profit margin", "percent", "duration", "Gross Profit / Revenues", "CF-10", "CF-10", ("gross_profit", "revenue")),
    "operating_margin": MetricSpec("Operating profit margin", "percent", "duration", "Operating Profit / Revenues", "CF-11", "CF-11", ("operating_income", "revenue")),
    "pretax_margin": MetricSpec("Pre-tax profit margin", "percent", "duration", "Pre-tax Profit / Revenues", "CF-12", "CF-12", ("pretax_profit", "revenue")),
    "operating_margin_change": MetricSpec("Change in operating profit margin", "percentage_points", "duration", "Current Operating Profit Margin - Previous Operating Profit Margin", "CF-16", "CF-16", ("operating_margin", "operating_margin")),
}
for _key, _label, _kind, _pending in (
    ("current_assets", "Current Assets", "instant", ()),
    ("current_liabilities", "Current Liabilities", "instant", ()),
    ("quick_assets", "Quick Assets", "instant", ("DEC-01",)),
    ("total_liabilities", "Total Liabilities", "instant", ()),
    ("net_worth", "Net Worth", "instant", ("DEC-02",)),
    ("capitalized_interest", "Capitalized Interest", "duration", ("DEC-05",)),
    ("da", "Depreciation & Amortization", "duration", ()),
    ("total_assets", "Total Assets", "instant", ()),
    ("cash_fx", "Cash bridge FX effect", "duration", ()),
    ("cash_other", "Other cash bridge adjustments", "duration", ()),
):
    METRICS[_key] = MetricSpec(_label, "money", _kind, f"Verified source {_label}", "DATA-01", pending=_pending)

INCOME_ROWS = ("revenue", "cost_of_revenue", "gross_profit", "operating_expense", "operating_income", "interest_expense", "pretax_profit", "income_tax", "net_income")
CASH_ROWS = ("beginning_cash", "cfo", "cfi", "cff", "ending_cash", "cash_change")
INCOME_TOPICS = ("revenue", "gross_margin", "operating_margin", "interest_expense", "pretax_margin")


@dataclass(frozen=True)
class TableSpec:
    key: str
    heading: str
    level: int
    columns: tuple[str, ...]  # Metric column is implicit; pct:<role> is common-size.
    rows: tuple[str, ...]
    topics: tuple[str, ...]
    rule: str


def report_layout(mode: Mode | str) -> tuple[TableSpec, ...]:
    """Select only from explicit user mode, never from facts or available rows."""
    mode = _mode(mode)
    if mode == Mode.ANNUAL:
        a, b, c, d = ANNUAL_ROLES
        return (
            TableSpec("income", "YOY (Annual) Income", 3, (a, b, c, f"pct:{c}", d, f"pct:{d}"), INCOME_ROWS, INCOME_TOPICS, "FMT-A1/NAR-01"),
            TableSpec("cash_flows", "Annual Cash Flows", 3, ANNUAL_ROLES, CASH_ROWS, (), "FMT-A2/NAR-02"),
            TableSpec("ratios", "Ratios YOY", 3, ANNUAL_ROLES, ("current_ratio", "quick_ratio", "cash_flow_ratio", "debt_ratio", "interest_coverage"), ("liquidity", "cash_flow_ratio", "debt_ratio", "interest_coverage"), "FMT-A3/NAR-03"),
            TableSpec("leverage", "Leverage YOY", 3, ANNUAL_ROLES, ("total_debt", "debt_service", "interest_expense", "ltm_ebitda", "ebitda_basis", "total_leverage", "ebitda_interest", "dscr"), ("ltm_ebitda", "debt_service", "dscr", "total_debt", "total_leverage"), "FMT-A4/NAR-04"),
        )
    return (
        TableSpec("income", "YTD (Quarterly) Income", 4, ("prior_interim", "pct:prior_interim", "current_interim", "pct:current_interim"), INCOME_ROWS, INCOME_TOPICS, "FMT-Q1/NAR-01"),
        TableSpec("ratios", "Ratios YTD", 4, QUARTERLY_ROLES, ("current_ratio", "quick_ratio", "debt_ratio"), ("liquidity", "debt_ratio"), "FMT-Q2/NAR-05"),
        TableSpec("leverage", "Leverage Analysis YTD", 4, QUARTERLY_ROLES, ("total_debt", "ltm_ebitda", "ebitda_basis", "total_leverage"), ("total_debt", "ltm_ebitda", "total_leverage"), "FMT-Q3/NAR-06"),
    )


def report_headings(mode: Mode | str) -> tuple[tuple[int, str], ...]:
    mode = _mode(mode)
    prefix = ((2, "A. Annual Review"),) if mode == Mode.ANNUAL else ((2, "B. Quarterly Review"), (3, "Financial Analysis"))
    return prefix + tuple((t.level, t.heading) for t in report_layout(mode))


@dataclass(frozen=True)
class Period:
    role: str
    label: str
    fiscal_year: int
    start: date | None  # Fiscal-year start, including for interim slots (YTD).
    end: date | None
    ltm_start: date | None
    evidence_ids: tuple[str, ...] = ()
    quarter: int | None = None
    reason: str = ""  # Required when any date is unavailable; never guess dates.


@dataclass(frozen=True)
class Evidence:
    id: str
    entity: str
    scope: str
    source_id: str
    version: str
    document_date: date
    locator: str
    kind: str  # fact, passage, calendar, review, definition
    period_roles: tuple[str, ...]
    content: str  # Original excerpt/value or documented review scope.
    purpose: str = "borrower"  # Historical/sample/test evidence is not accepted.


@dataclass(frozen=True)
class Fact:
    id: str
    metric: str
    period_role: str
    status: Status
    value: Decimal | str | None
    unit: str
    definition: str
    start: date | None
    end: date | None
    entity: str
    scope: str
    evidence_ids: tuple[str, ...] = ()
    original_value: Decimal | str | None = None
    original_scale: Decimal | None = None
    currency: str | None = None
    formula_id: str | None = None
    formula_version: str | None = None
    input_ids: tuple[str, ...] = ()
    reason: str = ""
    basis: str = ""
    period_kind: str = ""  # instant or duration; independent of display column.


@dataclass(frozen=True)
class Narrative:
    topic: str
    status: str  # supported, missing, not_applicable
    text: str = ""
    claim_type: str = "observation"  # comparison, cause, management, judgment, limitation
    fact_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    period_roles: tuple[str, ...] = ()
    reason: str = ""
    attribution: str = ""


@dataclass(frozen=True)
class Table:
    spec: TableSpec
    # Row -> ordered column cells -> fact ID. No cell values copied independently.
    cells: tuple[tuple[str, ...], ...]
    narratives: tuple[Narrative, ...]
    notes: tuple[Narrative, ...] = ()


@dataclass(frozen=True)
class Report:
    mode: Mode
    entity: str
    scope: str
    currency: str
    scale: Decimal
    periods: tuple[Period, ...]
    headings: tuple[tuple[int, str], ...]
    tables: tuple[Table, ...]
    facts: Mapping[str, Fact] = field(default_factory=dict)
    evidence: Mapping[str, Evidence] = field(default_factory=dict)
    # Decision ID -> evidence ID of explicit approval; empty means unresolved.
    decisions: Mapping[str, str] = field(default_factory=dict)


def _require(ok: bool, rule: str, message: str) -> None:
    if not ok:
        raise ContractError(f"{rule}: {message}")


def _mode(mode: Mode | str) -> Mode:
    try:
        return Mode(mode)
    except (ValueError, TypeError):
        raise ContractError("FMT-01: explicit annual or quarterly mode required") from None


def _number(value: object) -> bool:
    return isinstance(value, Decimal) and value.is_finite()


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _dates(metric: str, period: Period) -> tuple[date | None, date | None]:
    kind = METRICS[metric].period_kind
    if kind == "opening":
        return None, period.start - timedelta(days=1) if period.start else None
    if kind == "instant":
        return None, period.end
    return (period.ltm_start if kind == "ltm" else period.start), period.end


def empty_report(mode: Mode | str, *, entity: str, scope: str, currency: str,
                 scale: Decimal, periods: tuple[Period, ...],
                 evidence: Mapping[str, Evidence] | None = None) -> Report:
    """Construct fixed slots with explicit missing states, not a completed report.

    Periods must be supplied independently of retrieved financial rows. Missing
    dates remain None with a reason. Validation is an explicit separate call.
    """
    mode = _mode(mode)
    by_role = {p.role: p for p in periods}
    roles = ANNUAL_ROLES if mode == Mode.ANNUAL else QUARTERLY_ROLES
    _require(tuple(p.role for p in periods) == roles, "FMT-02", "all four ordered period slots are required")
    facts: dict[str, Fact] = {}
    tables = []
    for spec in report_layout(mode):
        cells = []
        for metric in spec.rows:
            row = []
            for column in spec.columns:
                pct = column.startswith("pct:")
                role = column.removeprefix("pct:")
                key = f"{metric}:{column}"
                start, end = _dates(metric, by_role[role])
                facts[key] = Fact(key, metric, role, Status.MISSING, None,
                                  "percent" if pct else METRICS[metric].unit,
                                  f"{metric} / revenue" if pct else METRICS[metric].definition,
                                  start, end, entity, scope,
                                  currency=currency if not pct and METRICS[metric].unit == "money" else None,
                                  reason="No supporting fact supplied",
                                  period_kind="instant" if METRICS[metric].period_kind in ("instant", "opening") else "duration")
                row.append(key)
            cells.append(tuple(row))
        narratives = tuple(Narrative(topic, "missing", reason="Supporting analysis not supplied") for topic in spec.topics)
        tables.append(Table(spec, tuple(cells), narratives))
    return Report(mode, entity, scope, currency, scale, periods, report_headings(mode), tuple(tables), facts, evidence or {})


def approved_formula_value(formula_id: str, values: tuple[Decimal, ...]) -> Decimal | None:
    """Approved arithmetic only; semantic/period/decision gates belong to Fact validation.

    Fractions remain unscaled (0.25, not 25). None denotes unavailable/zero divisor;
    no conversion of missing inputs, estimates or pending business definitions.
    """
    arity = {"CF-01": 2, "CF-02": 2, "CF-03": 2, "CF-04": 3, "CF-05": 4,
             "CF-06": 2, "CF-09": 2, "CF-10": 2, "CF-11": 2, "CF-12": 2,
             "CF-16": 2, "COMMON-SIZE-v1": 2, "CASH-CHANGE-v1": 2, "LEVERAGE-v1": 2, "STANDARD-EBITDA-v1": 4}
    _require(formula_id in arity, "AUTH-03", "Formula is not an implemented approved calculation")
    _require(len(values) == arity[formula_id], "CALC-02", "Formula input count mismatch")
    if not all(_number(v) for v in values):
        return None
    if formula_id == "STANDARD-EBITDA-v1":
        return sum(values, Decimal(0))
    if formula_id in ("CF-16", "CASH-CHANGE-v1"):
        return values[0] - values[1]
    if formula_id == "CF-04":
        pretax, interest, capitalized = values
        numerator, denominator = pretax + interest, interest + capitalized
    elif formula_id == "CF-05":
        pretax, interest, da, capitalized = values
        numerator, denominator = pretax + interest + da, interest + capitalized
    elif formula_id == "CF-09":
        numerator, denominator = values[0] - values[1], values[1]
    else:
        numerator, denominator = values
    return numerator / denominator if denominator != 0 else None


def calculate_fact(report: Report, fact_id: str, *, input_ids: tuple[str, ...],
                   formula_version: str) -> Report:
    """Calculate an existing slot using approved inputs, preserving all contract gates.

    This explicit step does not alter source-only preparation or add report rows.
    Pending definitions and unavailable inputs retain not_calculable, never zero.
    Conditional statement identities/cash reconciliation require a separate reviewed
    bridge; they are deliberately not inferred by this generic arithmetic step.
    """
    validate_report(report, expected_mode=report.mode)
    _require(fact_id in report.facts, "DATA-01", "Unknown target fact")
    target = report.facts[fact_id]
    spec = METRICS[target.metric]
    formula = "COMMON-SIZE-v1" if ":pct:" in fact_id else ("STANDARD-EBITDA-v1" if target.metric == "ltm_ebitda" else spec.formula)
    _require(_text(formula_version), "CALC-02", "Explicit formula version required")
    _require(formula is not None, "AUTH-03", "No approved generic formula for target")
    _require(target.status not in AVAILABLE, "DATA-01", "Do not overwrite an available source/calculation")
    missing_decisions = set(spec.pending) - set(report.decisions)
    inputs = [report.facts.get(i) for i in input_ids]
    reason = ("Unresolved definitions: " + ", ".join(sorted(missing_decisions)) if missing_decisions else
              "Required inputs unavailable" if any(i is None or i.status not in AVAILABLE for i in inputs) else "")
    if formula == "STANDARD-EBITDA-v1":
        if "DEC-05" not in report.decisions:
            reason = "Gross interest definition approval required"
        basis = report.facts.get('ebitda_basis:' + target.period_role)
        if basis is None or basis.status not in AVAILABLE or basis.value != spec.definition:
            reason = "Verified Standard EBITDA basis required"
        elif target.start is None or any(i is None or (i.start, i.end) != (target.start, target.end) for i in inputs):
            reason = "Complete exact LTM components required; YTD/annualization is not LTM"
        else:
            target = replace(target, basis=spec.definition)
    if formula == "CASH-CHANGE-v1" and not any(report.evidence[eid].kind == "definition" for eid in target.evidence_ids):
        reason = "Reviewed same-basis cash reconciliation required; no automatic cash bridge"
    if formula == "LEVERAGE-v1" and not reason:
        # CALC-12: carry the denominator's verified basis into the calculated ratio.
        target = replace(target, basis=inputs[1].basis)
    if reason:
        updated = replace(target, status=Status.NOT_CALCULABLE, value=None, reason=reason)
    else:
        value = approved_formula_value(formula, tuple(i.value for i in inputs))
        updated = (replace(target, status=Status.CALCULATED, value=value, reason="",
                           formula_id=formula, formula_version=formula_version, input_ids=input_ids)
                   if value is not None else replace(target, status=Status.NOT_CALCULABLE,
                                                     value=None, reason="Zero divisor or nonnumeric input"))
    result = replace(report, facts={**report.facts, fact_id: updated})
    validate_report(result, expected_mode=report.mode)
    return result


def calculate_identity(report: Report, fact_id: str, *, formula_id: str,
                       input_ids: tuple[str, ...], formula_version: str,
                       definition_evidence_id: str) -> Report:
    """DER-01..06 only after a reviewed, complete same-scope identity is supplied.

    The definition evidence documents included/excluded bridge items (including
    tax/discontinued/NCI scope). A tag or matching amount is not such a review.
    """
    validate_report(report, expected_mode=report.mode)
    rules = {
        "DER-01": ("gross_profit", ("revenue", "cost_of_revenue"), -1),
        "DER-02": ("cost_of_revenue", ("revenue", "gross_profit"), -1),
        "DER-03": ("operating_expense", ("gross_profit", "operating_income"), -1),
        "DER-04": ("operating_income", ("gross_profit", "operating_expense"), -1),
        "DER-05": ("pretax_profit", ("net_income", "income_tax"), 1),
        "DER-06": ("net_income", ("pretax_profit", "income_tax"), -1),
    }
    _require(formula_id in rules and fact_id in report.facts, "AUTH-03", "Unsupported identity/target")
    metric, expected, sign = rules[formula_id]
    target = report.facts[fact_id]
    _require(target.metric == metric and target.status not in AVAILABLE, "DATA-01", "Identity target mismatch or available source")
    _require(_text(formula_version), "CALC-02", "Explicit formula version required")
    evidence = report.evidence.get(definition_evidence_id)
    _require(evidence is not None and evidence.kind == "definition" and target.period_role in evidence.period_roles,
             "CALC-14", "Reviewed same-scope complete identity evidence required")
    items = [report.facts.get(i) for i in input_ids]
    _require(len(items) == 2 and all(i is not None for i in items) and tuple(i.metric for i in items) == expected,
             "CALC-02", "Identity components/order mismatch")
    _require(all(i.period_role == target.period_role and (i.start, i.end) == (target.start, target.end)
                 and i.unit == target.unit and i.currency == target.currency for i in items),
             "CALC-03", "Identity period/unit mismatch")
    # A derived gross profit cannot be used to reverse-infer its own cost.
    def depends_on(fid, metric, seen=None):
        seen = set() if seen is None else seen
        if fid in seen: return False
        seen.add(fid)
        item = report.facts[fid]
        return item.metric == metric or any(depends_on(i, metric, seen) for i in item.input_ids)
    _require(not any(depends_on(i.id, target.metric) for i in items), "CALC-02", "Circular/reverse identity")
    if any(i.status not in AVAILABLE or not _number(i.value) for i in items):
        updated = replace(target, status=Status.NOT_CALCULABLE, reason="Identity inputs unavailable")
    else:
        updated = replace(target, status=Status.CALCULATED, value=items[0].value + sign * items[1].value,
                          reason="", formula_id=formula_id, formula_version=formula_version,
                          input_ids=input_ids, evidence_ids=(definition_evidence_id,))
    result = replace(report, facts={**report.facts, fact_id: updated})
    validate_report(result, expected_mode=report.mode)
    return result


def validate_report(report: Report, *, expected_mode: Mode | str) -> None:
    """Validate boundary structure and evidence references; raise ContractError.

    expected_mode must come from the request, independently of report.mode.
    Passing does NOT certify arithmetic, source authenticity, semantic entailment,
    historical writing quality, rendered output, or readiness for final delivery.
    """
    mode = _mode(expected_mode)
    _require(isinstance(report.mode, Mode) and report.mode == mode, "FMT-01", "report mode differs from requested mode")
    _require(all(_text(v) for v in (report.entity, report.scope, report.currency)), "DATA-01", "entity, scope and currency required")
    _require(_number(report.scale) and report.scale > 0, "FMT-05", "positive Decimal monetary scale required")
    roles = ANNUAL_ROLES if mode == Mode.ANNUAL else QUARTERLY_ROLES
    _require(tuple(p.role for p in report.periods) == roles, "FMT-02", "all four ordered period slots must remain")
    periods = {p.role: p for p in report.periods}

    def refs(ids: tuple[str, ...], context: str, period_roles: tuple[str, ...] = ()) -> tuple[Evidence, ...]:
        _require(len(ids) == len(set(ids)), "EVD-01", f"{context}: duplicate evidence IDs")
        result = []
        for eid in ids:
            _require(eid in report.evidence, "EVD-01", f"{context}: unknown evidence {eid}")
            e = report.evidence[eid]
            _require(not period_roles or set(period_roles) <= set(e.period_roles), "EVD-01", f"{context}: evidence period mismatch")
            result.append(e)
        return tuple(result)

    for eid, e in report.evidence.items():
        _require(eid == e.id and all(_text(v) for v in (eid, e.source_id, e.version, e.locator, e.content)), "DATA-01", f"{eid}: incomplete source locator/version/content")
        _require(e.entity == report.entity and e.scope == report.scope and e.purpose == "borrower", "EVD-03", f"{eid}: foreign entity/scope or reference/sample evidence")
        _require(type(e.document_date) is date and e.kind in ("fact", "passage", "calendar", "review", "definition"), "DATA-01", f"{eid}: invalid evidence type/date")
        _require(bool(e.period_roles) and set(e.period_roles) <= set(roles), "EVD-01", f"{eid}: invalid evidence period roles")
    for decision, eid in report.decisions.items():
        _require(decision in {f"DEC-{i:02d}" for i in range(1, 12)}, "AUTH-05", "unknown decision ID")
        _require(refs((eid,), decision)[0].kind == "definition", "AUTH-05", f"{decision}: explicit decision evidence required")

    for p in report.periods:
        _require(_text(p.label) and type(p.fiscal_year) is int, "FMT-03", f"{p.role}: fiscal label/year required")
        for d in (p.start, p.end, p.ltm_start):
            _require(d is None or type(d) is date, "FMT-03", f"{p.role}: date object or None required")
        if any(d is None for d in (p.start, p.end, p.ltm_start)):
            _require(_text(p.reason), "MISS-06", f"{p.role}: missing date reason required")
        if p.start is not None and p.end is not None:
            _require(p.start <= p.end, "FMT-03", f"{p.role}: reversed fiscal interval")
        if any(d is not None for d in (p.start, p.end, p.ltm_start)):
            _require(bool(p.evidence_ids), "DATA-01", f"{p.role}: fiscal calendar evidence required")
            refs(p.evidence_ids, p.role, (p.role,))
        interim = mode == Mode.QUARTERLY and p.role in ("prior_interim", "current_interim")
        _require((type(p.quarter) is int and p.quarter in (1, 2, 3)) if interim else p.quarter is None, "FMT-03", f"{p.role}: invalid fiscal quarter")
        if not interim and p.start and p.end:
            _require((p.end - p.start).days + 1 in (364, 365, 366, 371), "FMT-03", f"{p.role}: full fiscal year required")
        if p.ltm_start and p.end:
            _require((p.end - p.ltm_start).days + 1 in (364, 365, 366, 371), "CALC-11", f"{p.role}: complete 52/53-week or calendar-year LTM required")
        if not interim and p.start and p.ltm_start:
            _require(p.start == p.ltm_start, "CALC-11", f"{p.role}: FY and year-end LTM must agree")
    if mode == Mode.ANNUAL:
        for prev, curr in zip(report.periods, report.periods[1:]):
            _require(curr.fiscal_year == prev.fiscal_year + 1, "FMT-02", "four consecutive fiscal years required")
            if prev.end and curr.start:
                _require(curr.start == prev.end + timedelta(days=1), "FMT-03", "fiscal years must be contiguous")
    else:
        earlier, prior, latest, current = report.periods
        _require(prior.quarter == current.quarter, "FMT-03", "comparable YTD fiscal quarters required")
        if prior.start and prior.end and current.start and current.end:
            prior_days = (prior.end - prior.start).days + 1
            current_days = (current.end - current.start).days + 1
            # Calendar and 52/53-week issuers differ by at most a fiscal week.
            # The broad quarter envelope supports month-end and retail calendars;
            # matching caller-supplied quarter numbers alone proves nothing.
            low, high = {1: (84, 98), 2: (175, 189), 3: (266, 280)}[prior.quarter]
            _require(low <= prior_days <= high and low <= current_days <= high
                     and abs(prior_days - current_days) <= 7,
                     "FMT-03", "YTD fiscal periods are not comparable to the declared quarter")
        _require(earlier.fiscal_year + 1 == prior.fiscal_year == latest.fiscal_year == current.fiscal_year - 1, "FMT-03", "quarterly fiscal-year roles mismatch")
        for prev, curr in ((earlier, prior), (earlier, latest), (latest, current)):
            if prev.end and curr.start:
                _require(curr.start == prev.end + timedelta(days=1), "FMT-03", f"{curr.role}: YTD/FY must start at fiscal-year start")
        for prev, curr in zip(report.periods, report.periods[1:]):
            if prev.end and curr.end:
                _require(prev.end < curr.end, "FMT-03", "quarterly comparison dates out of order")

    _require(report.headings == report_headings(mode), "FMT-07", "incorrect heading hierarchy/order or extra section")
    specs = report_layout(mode)
    _require(tuple(t.spec for t in report.tables) == specs, "FMT-02", "incorrect tables, rows, columns or narrative specifications")
    bound_ids = {fid for table in report.tables for row in table.cells for fid in row}

    for fid, f in report.facts.items():
        _require(fid == f.id and _text(fid) and f.metric in METRICS and f.period_role in periods, "DATA-01", f"{fid}: invalid fact identity/metric/role")
        _require(f.entity == report.entity and f.scope == report.scope, "DATA-01", f"{fid}: wrong entity/scope")
        _require(isinstance(f.status, Status) and _text(f.definition), "DATA-01", f"{fid}: explicit status and definition required")
        spec = METRICS[f.metric]
        common_size = f.formula_id == "COMMON-SIZE-v1" or f.unit == "percent" and spec.unit == "money"
        _require(not common_size or f.metric in INCOME_ROWS, "FMT-05", f"{fid}: common-size only applies to income")
        _require(f.unit == ("percent" if common_size else spec.unit), "FMT-05", f"{fid}: incompatible unit")
        _require(f.currency == (report.currency if f.unit == "money" else None), "FMT-05", f"{fid}: currency mismatch")
        expected_kind = "instant" if spec.period_kind in ("instant", "opening") else "duration"
        _require(f.period_kind == expected_kind, "DATA-01", f"{fid}: instant/duration kind mismatch")
        _require(all(d is None or type(d) is date for d in (f.start, f.end)), "DATA-01", f"{fid}: invalid fact dates")
        _require(f.start is None if f.period_kind == "instant" else not (f.start and f.end) or f.start <= f.end, "DATA-01", f"{fid}: invalid period interval")
        if fid in bound_ids:
            _require((f.start, f.end) == _dates(f.metric, periods[f.period_role]), "DATA-01", f"{fid}: fact period differs from requested fiscal/YTD/instant/LTM period")
        evidence = refs(f.evidence_ids, fid, (f.period_role,))
        if f.status not in AVAILABLE:
            _require(f.value is None and f.original_value is None and not f.input_ids and f.formula_id is None and f.formula_version is None, "MISS-01", f"{fid}: unavailable fact must not carry a value or completed calculation")
            _require(_text(f.reason), "MISS-06", f"{fid}: unavailable reason required")
            if f.status == Status.CONFLICT:
                _require(len({(e.source_id, e.version, e.locator) for e in evidence}) >= 2, "DATA-03", f"{fid}: conflicting sources required")
            if f.status == Status.NOT_APPLICABLE:
                _require(any(e.kind in ("review", "definition") for e in evidence), "MISS-03", f"{fid}: confirmed inapplicability evidence required")
            continue
        _require(f.end is not None and (spec.period_kind in ("instant", "opening") or f.start is not None), "DATA-01", f"{fid}: available value requires known dates")
        _require(_text(f.value) if f.unit == "text" else _number(f.value), "MISS-01", f"{fid}: finite Decimal or basis text required; no null/bool coercion")
        if not common_size:
            _require(set(spec.pending) <= set(report.decisions), "AUTH-05", f"{fid}: unresolved definitions {spec.pending}")
            for decision in spec.pending:
                refs((report.decisions[decision],), fid, (f.period_role,))
            if spec.formula:
                _require(f.definition == spec.definition, "AUTH-03", f"{fid}: definition differs from approved metric")
        if f.metric in ("ltm_ebitda", "ebitda_basis", "total_leverage"):
            _require(_text(f.basis), "CALC-12", f"{fid}: EBITDA basis required")
        if f.status == Status.SOURCED:
            _require(bool(evidence) and any(e.kind == "fact" for e in evidence), "DATA-01", f"{fid}: direct source fact required")
            _require(f.formula_id is None and f.formula_version is None and not f.input_ids, "DATA-01", f"{fid}: direct fact must not carry calculation metadata")
            _require(not common_size, "CALC-01", f"{fid}: common-size must be calculated")
            if f.unit == "text":
                _require(f.original_value == f.value, "DATA-01", f"{fid}: source basis text required")
            else:
                _require(_number(f.original_value) and _number(f.original_scale) and f.original_scale > 0, "DATA-01", f"{fid}: original numeric value/scale required")
                scale = report.scale if f.unit == "money" else Decimal(1)
                _require(f.value * scale == f.original_value * f.original_scale, "MISS-01", f"{fid}: normalization changed source value")
        else:
            _require(_text(f.formula_id) and _text(f.formula_version) and bool(f.input_ids), "CALC-02", f"{fid}: formula/version/input IDs required")
            _require(f.original_value is None and f.original_scale is None, "DATA-01", f"{fid}: calculated fact must not claim an original value")
            expected_formula = "COMMON-SIZE-v1" if common_size else ("STANDARD-EBITDA-v1" if f.metric == "ltm_ebitda" else spec.formula)
            if expected_formula:
                _require(f.formula_id == expected_formula, "AUTH-03", f"{fid}: wrong formula ID")
            else:
                _require(any(e.kind == "definition" for e in evidence), "CALC-14", f"{fid}: verified identity/basis evidence required")
            inputs = []
            expected_inputs = (f.metric, "revenue") if common_size else spec.inputs
            for index, iid in enumerate(f.input_ids):
                _require(iid in report.facts and iid != fid, "CALC-02", f"{fid}: invalid input {iid}")
                item = report.facts[iid]
                input_role = f.period_role
                if f.metric in ("revenue_growth", "operating_margin_change") and index == 1:
                    if mode == Mode.ANNUAL:
                        position = roles.index(f.period_role)
                        _require(position > 0, "CALC-03", f"{fid}: previous fiscal year not in report scope")
                        input_role = roles[position - 1]
                    else:
                        _require(f.period_role == "current_interim", "CALC-03", f"{fid}: comparable YTD pair required")
                        input_role = "prior_interim"
                _require(item.status in AVAILABLE and item.period_role == input_role, "CALC-03", f"{fid}: missing/incompatible input {iid}")
                expected_unit = METRICS[expected_inputs[index]].unit if index < len(expected_inputs) else "money"
                _require(item.unit == expected_unit, "CALC-03", f"{fid}: input unit mismatch")
                inputs.append(item)
            if f.formula_id == "STANDARD-EBITDA-v1":
                _require(f.basis == spec.definition and all((i.start, i.end) == (f.start, f.end) for i in inputs),
                         "CALC-03", "Standard EBITDA needs complete exact LTM components and standard basis")
            if expected_inputs:
                _require(tuple(i.metric for i in inputs) == expected_inputs, "CALC-02", f"{fid}: formula components/order mismatch")
                for item in inputs:
                    _require((item.start, item.end) == _dates(item.metric, periods[item.period_role]), "CALC-03", f"{fid}: input duration/instant is incompatible")

    # Reject cycles even when every referenced ID exists.
    visited, visiting = set(), set()
    def walk(fid: str) -> None:
        _require(fid not in visiting, "CALC-02", f"{fid}: cyclic calculation lineage")
        if fid in visited:
            return
        visiting.add(fid)
        for iid in report.facts[fid].input_ids:
            walk(iid)
        visiting.remove(fid)
        visited.add(fid)
    for fid in report.facts:
        walk(fid)

    def narrative(n: Narrative, context: str) -> None:
        _require(n.status in ("supported", "missing", "not_applicable"), "EVD-01", f"{context}: invalid narrative status")
        _require(set(n.period_roles) <= set(roles), "EVD-01", f"{context}: invalid narrative periods")
        cited = refs(n.evidence_ids, context)  # Individual passages may cover different comparison periods.
        for fid in n.fact_ids:
            _require(fid in report.facts and report.facts[fid].status in AVAILABLE, "EVD-01", f"{context}: unsupported narrative fact")
        covered = {r for e in cited for r in e.period_roles} | {report.facts[f].period_role for f in n.fact_ids}
        _require(set(n.period_roles) <= covered, "EVD-01", f"{context}: citations do not cover claim periods")
        if n.status != "supported":
            _require(not n.text and _text(n.reason), "MISS-04", f"{context}: absent analysis must carry reason, not invented prose")
            if n.status == "not_applicable":
                _require(any(e.kind in ("review", "definition") for e in cited), "MISS-03", f"{context}: inapplicability evidence required")
            return
        _require(_text(n.text) and bool(n.period_roles) and bool(n.fact_ids or cited), "EVD-01", f"{context}: supported prose requires scoped evidence")
        _require(n.claim_type in ("observation", "comparison", "cause", "management", "judgment", "limitation"), "EVD-01", f"{context}: invalid claim type")
        if n.claim_type == "comparison":
            fact_roles = {report.facts[f].period_role for f in n.fact_ids}
            _require(len(n.period_roles) >= 2 and set(n.period_roles) <= fact_roles, "EVD-01", f"{context}: comparison requires both periods' facts")
        if n.claim_type in ("cause", "management"):
            passage_roles = {r for e in cited if e.kind == "passage" for r in e.period_roles}
            _require(set(n.period_roles) <= passage_roles, "MISS-04", f"{context}: causal passage for claim periods required")
        if n.claim_type == "management":
            _require(_text(n.attribution), "EVD-01", f"{context}: management attribution required")
        if n.claim_type == "judgment":
            _require(bool(n.fact_ids) and any(e.kind == "definition" for e in cited), "STYLE-08", f"{context}: data and applicable evaluation basis required")
        if n.claim_type == "limitation":
            _require(any(e.kind == "review" for e in cited), "EVD-02", f"{context}: reviewed-material scope required")

    for table in report.tables:
        spec = table.spec
        _require(len(table.cells) == len(spec.rows), "FMT-02", f"{spec.key}: missing/extra rows")
        for metric, row in zip(spec.rows, table.cells):
            _require(len(row) == len(spec.columns), "FMT-02", f"{spec.key}/{metric}: missing/extra columns")
            for column, fid in zip(spec.columns, row):
                _require(fid in report.facts, "DATA-01", f"{spec.key}: cell references missing fact")
                f = report.facts[fid]
                expected_unit = "percent" if column.startswith("pct:") else METRICS[metric].unit
                _require((f.metric, f.period_role, f.unit) == (metric, column.removeprefix("pct:"), expected_unit), "FMT-02", f"{spec.key}/{metric}/{column}: incorrect cell binding")
        _require(tuple(n.topic for n in table.narratives) == spec.topics, "NAR-01", f"{spec.key}: required topic coverage/order; combine topics only at rendering")
        for n in table.narratives:
            narrative(n, f"{spec.key}/{n.topic}")
        allowed_notes = {"definition", "missing_data", "basis", "reconciliation"}
        if spec.key == "income":
            allowed_notes.add("material_exception")
        for n in table.notes:
            _require(n.topic in allowed_notes, "FMT-07", f"{spec.key}: unrequested note/block")
            narrative(n, f"{spec.key}/{n.topic}")
        if spec.key == "leverage":
            by_metric = dict(zip(spec.rows, table.cells))
            for i, role in enumerate(spec.columns):
                ebitda, basis, leverage = (report.facts[by_metric[m][i]] for m in ("ltm_ebitda", "ebitda_basis", "total_leverage"))
                if ebitda.status in AVAILABLE:
                    _require(basis.status in AVAILABLE and basis.value == ebitda.basis == basis.basis, "CALC-12", f"{role}: EBITDA and displayed basis mismatch")
                if leverage.status in AVAILABLE:
                    _require(ebitda.status in AVAILABLE and leverage.basis == ebitda.basis, "CALC-09", f"{role}: leverage/EBITDA basis mismatch")
