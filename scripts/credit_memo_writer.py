"""
credit_memo_writer.py v4 — Dual-Format Credit Memo Generator

Format 1 (Quarterly)  — selected by explicit quarterly request mode
  Part 1 : YTD Quarterly Income Statement (Q1=3M, Q2=6M, Q3=9M)
  Part 2 : Ratios YTD  (all periods as M/D/YYYY dates)
  Part 3 : Leverage Analysis YTD

Format 2 (Annual)     — selected by explicit annual request mode
  Part 1 : YOY Annual Income
  Part 2 : Annual Cash Flows
  Part 3 : Ratios YOY
  Part 4 : Leverage YOY
"""

from __future__ import annotations
import re
import logging
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# PeriodColumn  (unchanged contract from v3)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PeriodColumn:
    label:       str
    period_type: str          # "annual" | "quarterly"
    data:        dict
    pct_col:     bool = False
    period_end:  Optional[date] = field(default=None, repr=False)

    def __post_init__(self):
        if self.period_end is None:
            pe = self.data.get("period_end")
            if pe:
                try:
                    self.period_end = pe if hasattr(pe, "year") else date.fromisoformat(str(pe)[:10])
                except (ValueError, TypeError):
                    self.period_end = date.min


def build_columns(
    annual_financials: list[dict],
    quarterly_financials: list[dict],
    periods: Optional[list[str]],
) -> list[PeriodColumn]:
    cols: list[PeriodColumn] = []

    for row in annual_financials:
        yr = int(row.get("fiscal_year", 0))
        label = next((p for p in (periods or []) if str(yr) in p), f"{yr}Y")
        cols.append(PeriodColumn(label=label, period_type="annual", data=row))

    for row in quarterly_financials:
        ql = row.get("quarter_label")
        if not ql:
            yr = int(row.get("fiscal_year", 0))
            mo = int(row.get("fiscal_month", 0))
            ql = str(row.get("period_end", "Unverified fiscal period"))
        cols.append(PeriodColumn(label=ql, period_type="quarterly", data=row))

    cols.sort(key=lambda c: c.period_end or date.min)

    ann = [c for c in cols if c.period_type == "annual"]
    if len(ann) >= 2:
        ann[-2].pct_col = True
        ann[-1].pct_col = True
    elif len(ann) == 1:
        ann[-1].pct_col = True

    return cols


# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def _v(row: dict, *keys) -> Optional[float]:
    for k in keys:
        val = row.get(k)
        if val is not None:
            try: return float(val)
            except: continue
    return None

def _fmt_m(val, null="N/A") -> str:
    """Integer $M: 1,664"""
    if val is None: return null
    return f"{int(round(val)):,}"

def _fmt_x(val, null="N/A") -> str:
    if val is None: return null
    return f"{val:.2f}x"

def _fmt_pct2(val, null="N/A") -> str:
    """Two-decimal percent: 44.38%"""
    if val is None: return null
    return f"{val:.2f}%"

def _pct_change(new, old) -> Optional[float]:
    if new is None or old is None or old == 0: return None
    return (new - old) / old

def _dir(a, b, up="increased", dn="decreased") -> str:
    if a is None or b is None: return "not comparable"
    if a == b: return "unchanged"
    return up if a > b else dn

def _dir_lev(a, b) -> str:
    """For leverage: higher is worse → tightened/improved"""
    if a is None or b is None: return "not comparable"
    if a == b: return "unchanged"
    return "tightened" if a > b else "improved"


# ─────────────────────────────────────────────────────────────────────────────
# Label helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fy_q_label(col: PeriodColumn) -> str:
    """Display the independently supplied fiscal-calendar label verbatim."""
    return col.label


def _date_label(col: PeriodColumn) -> str:
    """period_end → 'M/D/YYYY'"""
    pe = col.period_end
    if pe is None: return col.label
    return f"{pe.month}/{pe.day}/{pe.year}"

def _fy_label(col: PeriodColumn) -> str:
    """Annual label: 'FY2025' → 'FY25', '2025Y' → 'FY25'"""
    m = re.search(r"(\d{4})", col.label)
    return f"FY{m.group(1)[-2:]}" if m else col.label


# ─────────────────────────────────────────────────────────────────────────────
# MD&A commentary lookup
#
# The actual reading of the filing and reasoning about *why* each metric
# moved happens once, upstream, in mda_commentary.generate_commentary()
# (called from agent_runner.py) — an LLM reads the whole MD&A the way a
# human analyst would and returns {metric_key: explanation}. This module
# stays a pure formatter: it only looks values up in that dict.
# ─────────────────────────────────────────────────────────────────────────────

def _cm(commentary: Optional[dict], key: str) -> str:
    s = (commentary or {}).get(key, "")
    return f" {s}" if s else " [refer to MD&A]"


def _compute_ltm_ebitda(kpis: list[dict], target_date: Optional[date]) -> Optional[float]:
    """Legacy KPI dictionaries cannot prove a fiscal LTM/approved EBITDA basis.

    LTM belongs to the reviewed Fact calculation path, never renderer fallbacks.
    """
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Shared table builder
# ─────────────────────────────────────────────────────────────────────────────

def _tbl(header_row: list[str], sep_row: list[str], data_rows: list[list[str]]) -> str:
    def pipe(cells): return "| " + " | ".join(cells) + " |"
    lines = [pipe(header_row), pipe(sep_row)] + [pipe(r) for r in data_rows]
    return "\n".join(lines)


# ═════════════════════════════════════════════════════════════════════════════
# FORMAT 1 — QUARTERLY
# ═════════════════════════════════════════════════════════════════════════════

def _q1_income_table(q_cols: list[PeriodColumn]) -> str:
    hdr = ["**YTD (Quarterly) Income Statement**"]
    sep = ["---"]
    for c in q_cols:
        lbl = _fy_q_label(c)
        hdr += [f"**{lbl}**", "**%**"]
        sep += ["---", "---"]

    def row(label, key):
        cells = [f"**{label}**"]
        for c in q_cols:
            val = _v(c.data, key)
            rev = _v(c.data, "revenue_m")
            cells.append(_fmt_m(val))
            if key == "revenue_m" and val is not None and rev not in (None, 0):
                cells.append("100%")
            elif val is not None and rev:
                cells.append(_fmt_pct2(val / rev * 100))
            else:
                cells.append("N/A")
        return cells

    rows = [
        row("Total revenues",       "revenue_m"),
        row("Cost of sales",        "cost_of_sales_m"),
        row("Gross profit",         "gross_profit_m"),
        row("Operating expense",    "operating_expense_m"),
        row("Operating income",     "operating_income_m"),
        row("Interest expense",     "interest_expense_m"),
        row("Income before taxes",  "income_before_tax_m"),
        row("Income tax expense",   "income_tax_m"),
        row("Net income",           "net_income_m"),
    ]
    return _tbl(hdr, sep, rows) + "\n\n> *USD millions. Source: SEC EDGAR XBRL via BigQuery.*"


def _q1_income_commentary(q_cols: list[PeriodColumn], commentary: dict) -> str:
    if len(q_cols) < 2:
        return ""
    prev, curr = q_cols[0], q_cols[1]
    pl, cl = _fy_q_label(prev), _fy_q_label(curr)

    def pct_rev(col, key):
        v = _v(col.data, key); r = _v(col.data, "revenue_m")
        return (v / r * 100) if (v is not None and r) else None

    rev_p, rev_c = _v(prev.data, "revenue_m"), _v(curr.data, "revenue_m")
    gm_p,  gm_c  = pct_rev(prev, "gross_profit_m"),       pct_rev(curr, "gross_profit_m")
    om_p,  om_c  = pct_rev(prev, "operating_income_m"),   pct_rev(curr, "operating_income_m")
    ie_p,  ie_c  = pct_rev(prev, "interest_expense_m"),   pct_rev(curr, "interest_expense_m")
    pt_p,  pt_c  = pct_rev(prev, "income_before_tax_m"),  pct_rev(curr, "income_before_tax_m")

    diff_pt = abs(pt_c - pt_p) if pt_c is not None and pt_p is not None else None
    word5 = ("slightly " if diff_pt is not None and 0 < diff_pt < 2 else "") + _dir(pt_c, pt_p)

    lines = [
        f"1. Total revenues {_dir(rev_c, rev_p)} to ${_fmt_m(rev_c)}M in {cl} from ${_fmt_m(rev_p)}M"
        f" in {pl}, mainly driven by{_cm(commentary, 'revenue')}",

        f"2. Gross margin {_dir(gm_c, gm_p)} to {_fmt_pct2(gm_c)} in {cl}"
        f" from {_fmt_pct2(gm_p)} in {pl}, mainly due to{_cm(commentary, 'gross_profit')}",

        f"3. Operating margin {_dir(om_c, om_p)} to {_fmt_pct2(om_c)} in {cl}"
        f" from {_fmt_pct2(om_p)} in {pl} driven by{_cm(commentary, 'operating_income')}",

        f"4. Interest expense {_dir(ie_c, ie_p)} to {_fmt_pct2(ie_c)} in {cl}"
        f" from {_fmt_pct2(ie_p)} in {pl} due to{_cm(commentary, 'interest_expense')}",

        f"5. Pre-tax margin was {word5} to {_fmt_pct2(pt_c)} in {cl}"
        f" from {_fmt_pct2(pt_p)} in {pl} driven by{_cm(commentary, 'pre_tax')}",
    ]
    q_match = re.match(r"Q(\d)\s+\d{4}", curr.label)
    if q_match and q_match.group(1) in {"2", "3"}:
        lines.append(
            f"6. Full-year target progress based on {cl}:{_cm(commentary, 'guidance')}"
        )
    return "\n".join(lines)


def _q1_ratios_table(cols: list[PeriodColumn]) -> str:
    hdr = ["**Ratios YTD**"] + [f"**{_date_label(c)}**" for c in cols]
    sep = ["---"] + ["---"] * len(cols)

    def row(label, key, fmt=_fmt_pct2):
        return [f"**{label}**"] + [fmt(_v(c.data, key)) for c in cols]

    rows = [
        row("Current ratio",  "current_ratio_pct"),
        row("Quick ratio",    "quick_ratio_pct"),
        row("Debt ratio",     "debt_ratio_pct"),
    ]
    return _tbl(hdr, sep, rows) + "\n\n> *Ratios: Current = Current Assets/Current Liab.; Quick = (CA−Inventory)/CL; Debt = Total Liabilities/Total Assets.*"


def _q1_ratios_commentary(cols: list[PeriodColumn], commentary: dict) -> str:
    if len(cols) < 2:
        return ""
    prev, curr = cols[-2], cols[-1]
    pd, cd = _date_label(prev), _date_label(curr)

    cr_p = _v(prev.data, "current_ratio_pct"); cr_c = _v(curr.data, "current_ratio_pct")
    qr_p = _v(prev.data, "quick_ratio_pct");   qr_c = _v(curr.data, "quick_ratio_pct")
    dr_p = _v(prev.data, "debt_ratio_pct");    dr_c = _v(curr.data, "debt_ratio_pct")

    return "\n".join([
        f"1. Current ratio as of {cd} {_dir(cr_c, cr_p)} to {_fmt_pct2(cr_c)}"
        f" from {_fmt_pct2(cr_p)} as of {pd};"
        f" no approved liquidity adequacy judgment supplied.{_cm(commentary, 'current_assets')}",

        f"2. The Company's quick ratio was {_fmt_pct2(qr_c)} as of {cd}"
        f" compared to {_fmt_pct2(qr_p)} as of {pd} due to{_cm(commentary, 'inventory')}",

        f"3. The debt ratio {_dir(dr_c, dr_p)} to {_fmt_pct2(dr_c)} as of {cd}"
        f" compared to {_fmt_pct2(dr_p)} as of {pd} due to{_cm(commentary, 'total_debt')}",
    ])


def _q1_leverage_table(cols: list[PeriodColumn], kpis: list[dict]) -> str:
    hdr = ["**Leverage Analysis YTD**"] + [f"**{_date_label(c)}**" for c in cols]
    sep = ["---"] + ["---"] * len(cols)

    def debt_row():
        cells = ["**Total debt**"]
        for c in cols:
            cells.append(_fmt_m(_v(c.data, "total_debt_m")))
        return cells

    def ebitda_row():
        cells = ["**LTM EBITDA**"]
        for c in cols:
            if c.period_type == "annual":
                v = _v(c.data, "ebitda_m")
            else:
                v = _compute_ltm_ebitda(kpis, c.period_end)
            cells.append(_fmt_m(v))
        return cells

    def lev_row():
        cells = ["**Total leverage ratio**"]
        for c in cols:
            if c.period_type == "annual":
                v = _v(c.data, "leverage_x")
            else:
                td = _v(c.data, "total_debt_m")
                eb = _compute_ltm_ebitda(kpis, c.period_end)
                v = (td / eb) if (td and eb and eb != 0) else None
            cells.append(_fmt_x(v))
        return cells

    return _tbl(hdr, sep, [debt_row(), ebitda_row(), lev_row()]) + \
           "\n\n> *LTM EBITDA requires a complete fiscal period and approved basis (DEC-06). Total Debt scope remains pending (DEC-02).*"


def _q1_leverage_commentary(cols: list[PeriodColumn], kpis: list[dict], commentary: dict) -> str:
    if len(cols) < 2:
        return ""
    prev, curr = cols[-2], cols[-1]
    pd, cd = _date_label(prev), _date_label(curr)

    td_p = _v(prev.data, "total_debt_m"); td_c = _v(curr.data, "total_debt_m")

    if curr.period_type == "annual":
        eb_c = _v(curr.data, "ebitda_m")
        lv_c = _v(curr.data, "leverage_x")
    else:
        eb_c = _compute_ltm_ebitda(kpis, curr.period_end)
        lv_c = (td_c / eb_c) if (td_c and eb_c and eb_c != 0) else None

    if prev.period_type == "annual":
        eb_p = _v(prev.data, "ebitda_m")
        lv_p = _v(prev.data, "leverage_x")
    else:
        eb_p = _compute_ltm_ebitda(kpis, prev.period_end)
        lv_p = (td_p / eb_p) if (td_p and eb_p and eb_p != 0) else None

    eb_pct = _pct_change(eb_c, eb_p)

    return "\n".join([
        f"1. Total debt {_dir(td_c, td_p)} to ${_fmt_m(td_c)}M as of {cd}"
        f" from ${_fmt_m(td_p)}M as of {pd} due to{_cm(commentary, 'total_debt')}",

        f"2. LTM EBITDA {_dir(eb_c, eb_p)} by"
        f" {_fmt_pct2(abs(eb_pct) * 100 if eb_pct is not None else None)} as of {cd}"
        f" compared to {pd} due to{_cm(commentary, 'ebitda')}",

        f"3. The {_dir_lev(lv_c, lv_p)} in total leverage to {_fmt_x(lv_c)} as of {cd}"
        f" was driven by{_cm(commentary, 'leverage')}",
    ])


def _generate_quarterly_memo(
    ticker, company_name, kpis, cols,
    ann_cols, q_cols, commentary, filing_text_source, gen_ts,
) -> str:
    col_desc = " | ".join(_date_label(c) for c in cols)
    sections = [
        f"# Credit Memo: {company_name} ({ticker})",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Prepared by | AI Credit Analysis Agent |",
        f"| Report date | {gen_ts} |",
        f"| Analysis columns | {col_desc} |",
        f"| Filing source | {filing_text_source} |",
        "",
        "---",
        "",
        "## Part 1 — YTD (Quarterly) Income Statement",
        "",
        _q1_income_table(q_cols),
        "",
        _q1_income_commentary(q_cols, commentary),
        "",
        "---",
        "",
        "## Part 2 — Ratios YTD",
        "",
        _q1_ratios_table(cols),
        "",
        _q1_ratios_commentary(cols, commentary),
        "",
        "---",
        "",
        "## Part 3 — Leverage Analysis YTD",
        "",
        _q1_leverage_table(cols, kpis),
        "",
        _q1_leverage_commentary(cols, kpis, commentary),
        "",
    ]
    return "\n".join(sections)


# ═════════════════════════════════════════════════════════════════════════════
# FORMAT 2 — ANNUAL
# ═════════════════════════════════════════════════════════════════════════════

def _q2_income_table(ann_cols: list[PeriodColumn]) -> str:
    hdr = ["**YOY (Annual) Income**"]
    sep = ["---"]
    for c in ann_cols:
        lbl = _fy_label(c)
        hdr.append(f"**{lbl}**")
        sep.append("---")
        if c.pct_col:
            hdr.append("**%**")
            sep.append("---")

    def row(label, key):
        cells = [f"**{label}**"]
        for c in ann_cols:
            val = _v(c.data, key)
            rev = _v(c.data, "revenue_m")
            cells.append(_fmt_m(val))
            if c.pct_col:
                if key == "revenue_m" and val is not None and rev not in (None, 0):
                    cells.append("100%")
                elif val is not None and rev:
                    cells.append(_fmt_pct2(val / rev * 100))
                else:
                    cells.append("N/A")
        return cells

    rows = [
        row("Revenues",             "revenue_m"),
        row("Cost of revenues",     "cost_of_sales_m"),
        row("Gross profit",         "gross_profit_m"),
        row("Operating expense",    "operating_expense_m"),
        row("Operating income",     "operating_income_m"),
        row("Interest expense",     "interest_expense_m"),
        row("Income before taxes",  "income_before_tax_m"),
        row("Income tax expense",   "income_tax_m"),
        row("Net income",           "net_income_m"),
    ]
    return _tbl(hdr, sep, rows) + "\n\n> *USD millions. % = common-size (% of revenues). Source: SEC EDGAR XBRL.*"


def _q2_income_commentary(ann_cols: list[PeriodColumn], commentary: dict) -> str:
    if len(ann_cols) < 2:
        return ""
    prev, curr = ann_cols[-2], ann_cols[-1]
    pl, cl = _fy_label(prev), _fy_label(curr)

    def pct_rev(col, key):
        v = _v(col.data, key); r = _v(col.data, "revenue_m")
        return (v / r * 100) if (v is not None and r) else None

    rev_p, rev_c = _v(prev.data,"revenue_m"), _v(curr.data,"revenue_m")
    gm_p,  gm_c  = pct_rev(prev,"gross_profit_m"),      pct_rev(curr,"gross_profit_m")
    om_p,  om_c  = pct_rev(prev,"operating_income_m"),  pct_rev(curr,"operating_income_m")
    ie_p,  ie_c  = pct_rev(prev,"interest_expense_m"),  pct_rev(curr,"interest_expense_m")
    pt_p,  pt_c  = pct_rev(prev,"income_before_tax_m"), pct_rev(curr,"income_before_tax_m")

    return "\n".join([
        f"1. Revenues {_dir(rev_c, rev_p)} to ${_fmt_m(rev_c)}M in {cl}"
        f" from ${_fmt_m(rev_p)}M in {pl}, mainly driven by{_cm(commentary, 'revenue')}",

        f"2. Gross margin {_dir(gm_c, gm_p)} to {_fmt_pct2(gm_c)} in {cl}"
        f" from {_fmt_pct2(gm_p)} in {pl}, mainly driven by{_cm(commentary, 'gross_profit')}",

        f"3. Operating margin {_dir(om_c, om_p)} to {_fmt_pct2(om_c)} in {cl}"
        f" from {_fmt_pct2(om_p)} in {pl}, mainly driven by{_cm(commentary, 'operating_income')}",

        f"4. Interest expense {_dir(ie_c, ie_p)} to {_fmt_pct2(ie_c)} in {cl}"
        f" from {_fmt_pct2(ie_p)} in {pl}, mainly driven by{_cm(commentary, 'interest_expense')}",

        f"5. Pre-tax margin {_dir(pt_c, pt_p)} to {_fmt_pct2(pt_c)} in {cl}"
        f" from {_fmt_pct2(pt_p)} in {pl}, mainly driven by{_cm(commentary, 'pre_tax')}",
    ])


def _q2_cashflow_table(ann_cols: list[PeriodColumn]) -> str:
    hdr = ["**Annual Cash Flows**"] + [f"**{_fy_label(c)}**" for c in ann_cols]
    sep = ["---"] + ["---"] * len(ann_cols)

    def row(label, key):
        return [f"**{label}**"] + [_fmt_m(_v(c.data, key)) for c in ann_cols]

    rows = [
        row("Beginning balance",    "beginning_cash_m"),
        row("Operating activities", "cfo_m"),
        row("Investing activities", "cfi_m"),
        row("Financing activities", "cff_m"),
        row("Ending balance",       "cash_m"),
        row("Change",               "net_cash_change_m"),
    ]
    return _tbl(hdr, sep, rows) + "\n\n> *USD millions. Opening/closing cash requires same-basis source evidence and full reconciliation. Source: SEC EDGAR XBRL.*"


def _q2_ratios_table(ann_cols: list[PeriodColumn]) -> str:
    hdr = ["**Ratios YOY**"] + [f"**{_date_label(c)}**" for c in ann_cols]
    sep = ["---"] + ["---"] * len(ann_cols)

    def row_pct(label, key):
        return [f"**{label}**"] + [_fmt_pct2(_v(c.data, key)) for c in ann_cols]

    def row_x(label, key):
        return [f"**{label}**"] + [_fmt_x(_v(c.data, key)) for c in ann_cols]

    rows = [
        row_pct("Current ratio",           "current_ratio_pct"),
        row_pct("Quick ratio",             "quick_ratio_pct"),
        row_pct("Cash flow ratio",         "cash_flow_ratio_pct"),
        row_pct("Debt ratio",              "debt_ratio_pct"),
        row_x ("Interest coverage ratio",  "interest_coverage_x"),
    ]
    return _tbl(hdr, sep, rows) + (
        "\n\n> *Current = CA/CL×100; Quick = approved Quick Assets/CL×100; "
        "Cash flow = CFO/CL×100; Debt = TL/approved Net Worth×100; "
        "Interest coverage = (Pre-tax + Interest)/(Interest + Capitalized Interest).*"
    )


def _q2_ratios_commentary(ann_cols: list[PeriodColumn], commentary: dict) -> str:
    if len(ann_cols) < 2:
        return ""
    prev, curr = ann_cols[-2], ann_cols[-1]
    pd, cd = _date_label(prev), _date_label(curr)
    pl, cl = _fy_label(prev), _fy_label(curr)

    cr_p = _v(prev.data,"current_ratio_pct"); cr_c = _v(curr.data,"current_ratio_pct")
    qr_p = _v(prev.data,"quick_ratio_pct");   qr_c = _v(curr.data,"quick_ratio_pct")
    cf_p = _v(prev.data,"cash_flow_ratio_pct"); cf_c = _v(curr.data,"cash_flow_ratio_pct")
    dr_p = _v(prev.data,"debt_ratio_pct");    dr_c = _v(curr.data,"debt_ratio_pct")
    ic_p = _v(prev.data,"interest_coverage_x"); ic_c = _v(curr.data,"interest_coverage_x")

    return "\n".join([
        f"1. Current ratio and quick ratio as of {cd} {_dir(cr_c, cr_p)} to"
        f" {_fmt_pct2(cr_c)} and {_fmt_pct2(qr_c)}, compared to"
        f" {_fmt_pct2(cr_p)} and {_fmt_pct2(qr_p)} as of {pd} mainly due to{_cm(commentary, 'current_assets')}",

        f"2. Cash flow ratio {_dir(cf_c, cf_p)} to {_fmt_pct2(cf_c)} as of {cd}"
        f" from {_fmt_pct2(cf_p)} as of {pd}, primarily due to{_cm(commentary, 'operating_cash')}",

        f"3. Debt ratio {_dir(dr_c, dr_p)} to {_fmt_pct2(dr_c)} as of {cd}"
        f" from {_fmt_pct2(dr_p)} as of {pd}, driven by{_cm(commentary, 'total_debt')}",

        f"4. Interest coverage ratio {_dir(ic_c, ic_p)} to {_fmt_x(ic_c)} in {cl}"
        f" from {_fmt_x(ic_p)} in {pl}, primarily due to{_cm(commentary, 'interest_expense')}",
    ])


def _q2_leverage_table(ann_cols: list[PeriodColumn]) -> str:
    hdr = ["**Leverage YOY**"] + [f"**{_date_label(c)}**" for c in ann_cols]
    sep = ["---"] + ["---"] * len(ann_cols)

    def row_m(label, key):
        return [f"**{label}**"] + [_fmt_m(_v(c.data, key)) for c in ann_cols]

    def row_x(label, key):
        return [f"**{label}**"] + [_fmt_x(_v(c.data, key)) for c in ann_cols]

    rows = [
        row_m("Total debt",                "total_debt_m"),
        row_m("Debt service",              "debt_service_m"),
        row_m("Interest expense",          "interest_expense_m"),
        row_m("LTM EBITDA*",               "ebitda_m"),
        row_x("Total leverage ratio",      "leverage_x"),
        row_x("LTM EBITDA / Interest",     "ebitda_interest_x"),
        row_x("Debt service coverage",     "debt_service_coverage_x"),
    ]
    return _tbl(hdr, sep, rows) + (
        "\n\n> *EBITDA basis pending review (DEC-06). Debt service definition pending (DEC-03). "
        "Use Compliance Certificate for scheduled principal payments.*"
    )


def _q2_leverage_commentary(ann_cols: list[PeriodColumn], commentary: dict) -> str:
    if len(ann_cols) < 2:
        return ""
    prev, curr = ann_cols[-2], ann_cols[-1]
    pd, cd = _date_label(prev), _date_label(curr)
    pl, cl = _fy_label(prev), _fy_label(curr)

    eb_p = _v(prev.data,"ebitda_m");              eb_c = _v(curr.data,"ebitda_m")
    ds_p = _v(prev.data,"debt_service_m");         ds_c = _v(curr.data,"debt_service_m")
    dsc_p= _v(prev.data,"debt_service_coverage_x"); dsc_c= _v(curr.data,"debt_service_coverage_x")
    td_p = _v(prev.data,"total_debt_m");           td_c = _v(curr.data,"total_debt_m")
    lv_p = _v(prev.data,"leverage_x");             lv_c = _v(curr.data,"leverage_x")

    return "\n".join([
        f"1. LTM Consolidated EBITDA {_dir(eb_c, eb_p)} to ${_fmt_m(eb_c)}M in {cl}"
        f" due to{_cm(commentary, 'ebitda')}",

        f"2. Total debt service {_dir(ds_c, ds_p)} to ${_fmt_m(ds_c)}M as of {cd}"
        f" from ${_fmt_m(ds_p)}M as of {pd}, driven by{_cm(commentary, 'debt_service')}",

        f"3. Debt service coverage {_dir(dsc_c, dsc_p)} to {_fmt_x(dsc_c)} in {cl}"
        f" from {_fmt_x(dsc_p)} in {pl}, primarily due to{_cm(commentary, 'debt_service')}",

        f"4. Total debt {_dir(td_c, td_p)} to ${_fmt_m(td_c)}M in {cl}"
        f" from ${_fmt_m(td_p)}M in {pl}, primarily due to{_cm(commentary, 'total_debt')}",

        f"5. Total leverage ratio as of {cd} was {_fmt_x(lv_c)},"
        f" {_dir(lv_c, lv_p, up='up', dn='down')} from {_fmt_x(lv_p)} as of {pd}"
        f" due to{_cm(commentary, 'leverage')}",
    ])


def _generate_annual_memo(
    ticker, company_name, kpis, cols, ann_cols,
    commentary, filing_text_source, gen_ts,
) -> str:
    col_desc = " | ".join(_date_label(c) for c in ann_cols)
    sections = [
        f"# Credit Memo: {company_name} ({ticker})",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Prepared by | AI Credit Analysis Agent |",
        f"| Report date | {gen_ts} |",
        f"| Analysis columns | {col_desc} |",
        f"| Filing source | {filing_text_source} |",
        "",
        "---",
        "",
        "## Part 1 — YOY (Annual) Income",
        "",
        _q2_income_table(ann_cols),
        "",
        _q2_income_commentary(ann_cols, commentary),
        "",
        "---",
        "",
        "## Part 2 — Annual Cash Flows",
        "",
        _q2_cashflow_table(ann_cols),
        "",
        "---",
        "",
        "## Part 3 — Ratios YOY",
        "",
        _q2_ratios_table(ann_cols),
        "",
        _q2_ratios_commentary(ann_cols, commentary),
        "",
        "---",
        "",
        "## Part 4 — Leverage YOY",
        "",
        _q2_leverage_table(ann_cols),
        "",
        _q2_leverage_commentary(ann_cols, commentary),
        "",
    ]
    return "\n".join(sections)


# ═════════════════════════════════════════════════════════════════════════════
# Entry point
# ═════════════════════════════════════════════════════════════════════════════

def generate_credit_memo(
    ticker: str,
    company_name: str,
    kpis: list[dict],
    annual_financials: list[dict],
    quarterly_financials: Optional[list[dict]] = None,
    periods: Optional[list[str]] = None,
    commentary: Optional[dict[str, str]] = None,
    filing_text_source: str = "none",
    *, mode: Optional[str] = None,
) -> str:
    """
    commentary: {metric_key: explanation}, produced upstream by
    mda_commentary.generate_commentary() (called from agent_runner.py) —
    this function only formats it, it never reads filing text itself.
    """
    if mode not in ("annual", "quarterly"):
        raise ValueError("Explicit annual/quarterly mode required")
    if not kpis and not annual_financials:
        return (
            f"# Credit Memo: {company_name} ({ticker})\n\n"
            "⚠️ No financial data available.\n"
        )

    quarterly_financials = quarterly_financials or []
    commentary = commentary or {}
    is_quarterly = mode == "quarterly"

    cols     = build_columns(annual_financials, quarterly_financials, periods)
    ann_cols = [c for c in cols if c.period_type == "annual"]
    q_cols   = [c for c in cols if c.period_type == "quarterly"]
    gen_ts   = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    fmt = "quarterly" if is_quarterly else "annual"
    logger.info(
        f"[{ticker}] Credit memo v4: format={fmt}, "
        f"columns={[c.label for c in cols]}, "
        f"commentary={'yes (' + filing_text_source + ')' if commentary else 'no'}"
    )

    if is_quarterly:
        return _generate_quarterly_memo(
            ticker, company_name, kpis, cols,
            ann_cols, q_cols, commentary, filing_text_source, gen_ts,
        )
    else:
        return _generate_annual_memo(
            ticker, company_name, kpis, cols, ann_cols,
            commentary, filing_text_source, gen_ts,
        )


def render_loan_review(report, acceptance) -> str:
    """Render the existing strict contract. No numeric fallbacks or new sections."""
    if __package__:
        from .loan_review_contract import AVAILABLE, METRICS, Mode, validate_report
        from .loan_review_pipeline import validate_arithmetic
    else:
        from loan_review_contract import AVAILABLE, METRICS, Mode, validate_report
        from loan_review_pipeline import validate_arithmetic
    validate_report(report, expected_mode=report.mode)
    validate_arithmetic(report)
    chinese = {
        'revenue': '營業收入', 'cost_of_revenue': '營業成本', 'gross_profit': '毛利',
        'operating_expense': '營業費用', 'operating_income': '營業利益', 'interest_expense': '利息費用',
        'pretax_profit': '稅前利益', 'income_tax': '所得稅費用／利益', 'net_income': '稅後淨利',
        'beginning_cash': '期初現金', 'cfo': '營業活動現金流', 'cfi': '投資活動現金流',
        'cff': '籌資活動現金流', 'ending_cash': '期末現金', 'cash_change': '現金變動',
        'current_ratio': '流動比率', 'quick_ratio': '速動比率', 'cash_flow_ratio': '現金流量比率',
        'debt_ratio': '負債比率', 'interest_coverage': '利息保障倍數', 'total_debt': '總債務',
        'debt_service': '債務清償額', 'ltm_ebitda': '最近完整年度 EBITDA', 'ebitda_basis': 'EBITDA 計算口徑',
        'total_leverage': '總槓桿倍數', 'ebitda_interest': 'EBITDA／利息', 'dscr': '償債保障倍數',
        'gross_margin': '毛利率', 'operating_margin': '營業利益率', 'pretax_margin': '稅前淨利率', 'liquidity': '流動性'}
    status = {'missing': '缺少資料', 'not_calculable': '無法計算／待確認', 'conflict': '來源衝突', 'not_applicable': '經確認不適用'}
    periods = {p.role: p for p in report.periods}
    def esc(value):
        return str(value).replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')
    def human_reason(text):
        for source, translated in (
            ('Unresolved definitions:', '定義待確認：'),
            ('source candidate retained in audit', '原始候選值保留於來源清單'),
            ('Required inputs unavailable', '必要輸入尚未取得或尚未核實'),
            ('Required formula inputs/definitions not yet verified', '公式必要輸入／定義尚未核實'),
            ('Reviewed same-basis cash reconciliation required; no automatic cash bridge', '須先核實相同現金口徑與完整調節，不自動反推'),
            ('No matching source in the reviewed inputs; not a claim of non-disclosure', '所選來源尚無相符資料；不代表整份申報未揭露'),
            ('Zero divisor or nonnumeric input', '分母為0或輸入不是可用數值')):
            text = text.replace(source, translated)
        return text
    def value(f):
        if f.status not in AVAILABLE: return status[f.status.value]
        if f.unit == 'text': return esc(f.value)
        def display(number, suffix=''):
            text = f'{abs(number):,.2f}{suffix}'
            return f'({text})' if number < 0 else text
        if f.unit == 'percent': return display(f.value * 100, '%')
        if f.unit == 'percentage_points': return f'{f.value * 100:,.2f} 個百分點'
        if f.unit == 'multiple': return display(f.value, 'x')
        return display(f.value)
    lines = []
    for level, heading in report.headings:
        lines += ['#' * level + ' ' + heading, '']
        matching = next((t for t in report.tables if t.spec.heading == heading), None)
        if matching is None: continue
        if matching is report.tables[0]:
            lines += [f'{esc(report.entity)}；範圍：{esc(report.scope)}；金額：{report.currency}，每單位 {report.scale:,}。',
                      '驗收狀態：' + ('已完成實質驗收。' if acceptance['final_report_accepted'] else '格式與計算驗證通過；資料及定義仍待確認，尚未完成實質驗收。'), '']
            if acceptance.get('source_limitations'):
                lines += ['> 來源限制：' + esc('；'.join(acceptance['source_limitations'])), '']
        headers = ['Metric／科目']
        for col in matching.spec.columns:
            role = col.removeprefix('pct:')
            p = periods[role]
            if col.startswith('pct:'): headers.append('% of revenue')
            elif matching.spec.key in ('ratios', 'leverage'): headers.append(p.end.isoformat() if p.end else p.label)
            else: headers.append(p.label)
        lines += ['| ' + ' | '.join(map(esc, headers)) + ' |', '| ' + ' | '.join(['---'] + ['---:'] * (len(headers)-1)) + ' |']
        for metric, ids in zip(matching.spec.rows, matching.cells):
            label = METRICS[metric].label
            # Only source-verified row labels, not guessed tag translations.
            if metric in ('revenue', 'cost_of_revenue'):
                allowed = {'Revenues', 'Net Sales', 'Net sales', 'Operating Cost', 'Cost Of Goods Sold', 'Cost of revenues', 'Cost of sales', 'Cost of services'}
                source_labels = {report.facts[i].definition for i in ids if report.facts[i].status in AVAILABLE and report.facts[i].unit == 'money'}
                if len(source_labels) == 1 and next(iter(source_labels)) in allowed: label = next(iter(source_labels))
            lines.append('| ' + ' | '.join([esc(label + '／' + chinese[metric])] + [value(report.facts[i]) for i in ids]) + ' |')
        lines.append('')
        unavailable = [report.facts[i] for row in matching.cells for i in row if report.facts[i].status not in AVAILABLE]
        reasons = list(dict.fromkeys(f.reason for f in unavailable))
        if reasons:
            lines += ['> 本表限制：' + esc(human_reason('；'.join(reasons))), '']
        for n in matching.narratives:
            text = n.text
            for metric, name in chinese.items():
                if metric in METRICS and text.startswith(METRICS[metric].label + ' '):
                    text = name + text[len(METRICS[metric].label):]
                    break
            lines.append('- ' + (esc(text) if n.status == 'supported' else esc(chinese.get(n.topic, n.topic) + '：尚未完成分析；' + human_reason(n.reason))))
        if matching.narratives: lines.append('')
        for n in matching.notes:
            lines += ['> ' + esc(n.text if n.status == 'supported' else n.reason), '']
        if matching.spec.key == 'cash_flows':
            failed = [c for c in acceptance.get('reconciliations', ()) if c['status'] not in ('matched', 'within_precision')]
            if failed:
                lines += ['> 現金／資產勾稽仍有未解釋項目；完整來源、差額及原因列於獨立驗收清單，未以調節數補平。', '']
    return '\n'.join(lines).rstrip() + '\n'
