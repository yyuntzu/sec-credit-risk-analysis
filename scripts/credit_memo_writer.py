"""
credit_memo_writer.py v4 — Dual-Format Credit Memo Generator

Format 1 (Quarterly)  — triggered when quarterly_financials is non-empty
  Part 1 : YTD Quarterly Income Statement (Q1=3M, Q2=6M, Q3=9M)
  Part 2 : Ratios YTD  (all periods as M/D/YYYY dates)
  Part 3 : Leverage Analysis YTD

Format 2 (Annual)     — triggered when quarterly_financials is empty
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
            ql = f"Q{(mo-1)//3+1} {yr}"
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
    return (new - old) / abs(old)

def _dir(a, b, up="increased", dn="decreased") -> str:
    return up if (a or 0) >= (b or 0) else dn

def _dir_lev(a, b) -> str:
    """For leverage: higher is worse → tightened/improved"""
    return "tightened" if (a or 0) > (b or 0) else "improved"


# ─────────────────────────────────────────────────────────────────────────────
# Label helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fy_q_label(col: PeriodColumn) -> str:
    """Quarter label with explicit year-to-date duration basis."""
    m = re.match(r"Q(\d)\s+(\d{4})", col.label)
    if m:
        months = {"1": "3M YTD", "2": "6M YTD", "3": "9M YTD"}.get(m.group(1), "YTD")
        return f"FY{m.group(2)[-2:]} Q{m.group(1)} ({months})"
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
    """
    LTM EBITDA as of target_date.

    kpis rows from fct_credit_kpis (mart-first path) already carry
    ttm_ebitda_m — a rolling trailing-12-month figure per row, not a
    single-quarter value — so the right answer is just the most recent one
    on/before target_date, not a sum. Summing 4 of them (the old behavior)
    quadruple-counts up to ~9 months of overlapping quarters between
    adjacent TTM windows and inflates LTM EBITDA ~3-4x.

    Only fall back to summing 4 quarterly ebitda_m values when the mart's
    TTM field isn't present (e.g. the inline raw-table KPI fallback, which
    returns a single-quarter operating-income approximation per row with
    no rolling TTM already applied).
    """
    if not kpis or target_date is None:
        return None

    eligible_ttm, eligible_q = [], []
    for kpi in kpis:
        pe = kpi.get("period_end")
        if pe is None: continue
        kpi_date = pe if hasattr(pe, "year") else date.fromisoformat(str(pe)[:10])
        if kpi_date > target_date:
            continue
        ttm_v = _v(kpi, "ttm_ebitda_m")
        if ttm_v is not None:
            eligible_ttm.append((kpi_date, ttm_v))
        q_v = _v(kpi, "ebitda_m")
        if q_v is not None:
            eligible_q.append((kpi_date, q_v))

    if eligible_ttm:
        eligible_ttm.sort(key=lambda x: x[0], reverse=True)
        return eligible_ttm[0][1]

    eligible_q.sort(key=lambda x: x[0], reverse=True)
    last4 = eligible_q[:4]
    return sum(v for _, v in last4) if last4 else None


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
            if key == "revenue_m":
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

    # fallback for pre-tax margin
    if pt_p is None:
        oi = _v(prev.data,"operating_income_m") or 0
        ie = _v(prev.data,"interest_expense_m") or 0
        r  = _v(prev.data,"revenue_m") or 1
        pt_p = (oi - ie) / r * 100
    if pt_c is None:
        oi = _v(curr.data,"operating_income_m") or 0
        ie = _v(curr.data,"interest_expense_m") or 0
        r  = _v(curr.data,"revenue_m") or 1
        pt_c = (oi - ie) / r * 100

    diff_pt = abs((pt_c or 0) - (pt_p or 0))
    word5 = ("slightly " if diff_pt < 2 else "") + _dir(pt_c, pt_p)

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
        f" from {_fmt_pct2(cr_p)} as of {pd}, indicating"
        f" {'adequate' if (cr_c or 0) >= 150 else 'tightened'} short-term liquidity.{_cm(commentary, 'current_assets')}",

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
                v = _compute_ltm_ebitda(kpis, c.period_end) or _v(c.data, "ebitda_m")
            cells.append(_fmt_m(v))
        return cells

    def lev_row():
        cells = ["**Total leverage ratio**"]
        for c in cols:
            if c.period_type == "annual":
                v = _v(c.data, "leverage_x")
            else:
                td = _v(c.data, "total_debt_m")
                eb = _compute_ltm_ebitda(kpis, c.period_end) or _v(c.data, "ebitda_m")
                v = (td / eb) if (td and eb and eb != 0) else None
            cells.append(_fmt_x(v))
        return cells

    return _tbl(hdr, sep, [debt_row(), ebitda_row(), lev_row()]) + \
           "\n\n> *LTM EBITDA = Operating Income + D&A (trailing 12 months). Total Debt = Short-Term Loans/Notes + Current Maturities of Long-Term Liabilities + Long-Term Liabilities.*"


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
        eb_c = _compute_ltm_ebitda(kpis, curr.period_end) or _v(curr.data, "ebitda_m")
        lv_c = (td_c / eb_c) if (td_c and eb_c and eb_c != 0) else None

    if prev.period_type == "annual":
        eb_p = _v(prev.data, "ebitda_m")
        lv_p = _v(prev.data, "leverage_x")
    else:
        eb_p = _compute_ltm_ebitda(kpis, prev.period_end) or _v(prev.data, "ebitda_m")
        lv_p = (td_p / eb_p) if (td_p and eb_p and eb_p != 0) else None

    eb_pct = _pct_change(eb_c, eb_p)

    return "\n".join([
        f"1. Total debt {_dir(td_c, td_p)} to ${_fmt_m(td_c)}M as of {cd}"
        f" from ${_fmt_m(td_p)}M as of {pd} due to{_cm(commentary, 'total_debt')}",

        f"2. LTM EBITDA {_dir(eb_c, eb_p)} by"
        f" {abs((eb_pct or 0)*100):.1f}% as of {cd}"
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
                if key == "revenue_m":
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

    if pt_p is None:
        oi = _v(prev.data,"operating_income_m") or 0
        ie = _v(prev.data,"interest_expense_m") or 0
        r  = _v(prev.data,"revenue_m") or 1
        pt_p = (oi - ie) / r * 100
    if pt_c is None:
        oi = _v(curr.data,"operating_income_m") or 0
        ie = _v(curr.data,"interest_expense_m") or 0
        r  = _v(curr.data,"revenue_m") or 1
        pt_c = (oi - ie) / r * 100

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
    return _tbl(hdr, sep, rows) + "\n\n> *USD millions. Beginning balance = Ending − (CFO+CFI+CFF). Source: SEC EDGAR XBRL.*"


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
        "\n\n> *Current = CA/CL×100; Quick = (CA−Inv)/CL×100; "
        "Cash flow = CFO/CL×100; Debt = TL/TA×100; "
        "Interest coverage = EBITDA/Interest expense.*"
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
        "\n\n> *\\*EBITDA = Operating Income + D&A. Debt service = Interest + CapEx (proxy). "
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
        f" {'up' if (lv_c or 0) > (lv_p or 0) else 'down'} from {_fmt_x(lv_p)} as of {pd}"
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
) -> str:
    """
    commentary: {metric_key: explanation}, produced upstream by
    mda_commentary.generate_commentary() (called from agent_runner.py) —
    this function only formats it, it never reads filing text itself.
    """
    if not kpis and not annual_financials:
        return (
            f"# Credit Memo: {company_name} ({ticker})\n\n"
            "⚠️ No financial data available.\n"
        )

    quarterly_financials = quarterly_financials or []
    commentary = commentary or {}
    is_quarterly = bool(quarterly_financials)

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
