"""
SEC EDGAR API Client v3 — 動態 CIK 查詢版
改動重點（相較於 v2）:
  1. 移除硬編碼 COMPANY_CIK dict
  2. 新增 resolve_cik(ticker) — 用 EDGAR company search API 動態查詢
  3. CIK 結果 in-memory cache，同一 session 不重複查詢
  4. get_company_submissions / get_company_facts 自動呼叫 resolve_cik
  5. 保留所有 v2 的 period validation / dedup 邏輯
"""

import os
import re
import time
import logging
from datetime import datetime, date
from typing import Optional
import requests

logger = logging.getLogger(__name__)

# ── SEC EDGAR 連線設定 ────────────────────────────────────────────────────────
_USER_AGENT = os.environ.get(
    "SEC_USER_AGENT",
    "sec-analysis-skill contact@example.com",  # SEC 要求真實聯絡資訊
)

EDGAR_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

EDGAR_DATA_HEADERS = {
    **EDGAR_HEADERS,
    "Host": "data.sec.gov",
}

# ── 期間天數範圍 ──────────────────────────────────────────────────────────────
ANNUAL_MIN_DAYS    = 340
ANNUAL_MAX_DAYS    = 380
# 10-Q company facts may contain both discrete-quarter and YTD duration facts.
# Retain all valid Q1/Q2/Q3 durations; downstream Loan Review queries select
# 3M, 6M, or 9M deterministically for the requested quarter.
QUARTERLY_MIN_DAYS = 70
QUARTERLY_MAX_DAYS = 290

# ── Balance Sheet：Point-in-time XBRL tags ───────────────────────────────────
BALANCE_SHEET_TAGS = frozenset({
    "Assets",
    "AssetsCurrent",
    "CashAndCashEquivalentsAtCarryingValue",
    "Liabilities",
    "LiabilitiesCurrent",
    "LongTermDebt",
    "LongTermDebtCurrent",
    "LongTermDebtNoncurrent",
    "LongTermDebtAndFinanceLeaseObligationsCurrent",
    "LongTermDebtAndFinanceLeaseObligationsNoncurrent",
    "LongTermDebtAndFinanceLeaseObligations",
    "DebtAndCapitalLeaseObligations",
    "LongTermDebtAndCapitalLeaseObligations",
    "LongTermDebtAndCapitalLeaseObligationsCurrent",
    "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities",
    "ShortTermNotesPayable",
    "StockholdersEquity",
    "RetainedEarningsAccumulatedDeficit",
})


# ══════════════════════════════════════════════════════════════════════════════
# CIK Resolution
# ══════════════════════════════════════════════════════════════════════════════

# In-memory cache: ticker → zero-padded CIK string
_CIK_CACHE: dict[str, str] = {}


def resolve_cik(ticker: str, session: Optional[requests.Session] = None) -> str:
    """
    動態查詢 ticker 對應的 CIK（10 位數字，前補零）。

    策略（依序嘗試）：
      1. In-memory cache（同 process 內不重查）
      2. EDGAR company_tickers.json（SEC 官方 ticker→CIK 映射，最快最準）
      3. EDGAR full-text search API（fallback）

    Returns:
        Zero-padded 10-digit CIK string, e.g. "0000789019"

    Raises:
        ValueError: 找不到對應 CIK 時
    """
    ticker = ticker.upper().strip()

    # 1. Cache hit
    if ticker in _CIK_CACHE:
        logger.debug(f"[{ticker}] CIK cache hit: {_CIK_CACHE[ticker]}")
        return _CIK_CACHE[ticker]

    sess = session or requests.Session()
    sess.headers.update(EDGAR_HEADERS)

    # 2. 官方 company_tickers.json（最可靠，包含所有上市公司）
    try:
        time.sleep(0.15)
        resp = sess.get(
            "https://www.sec.gov/files/company_tickers.json",
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        for entry in data.values():
            if entry.get("ticker", "").upper() == ticker:
                cik = str(entry["cik_str"]).zfill(10)
                _CIK_CACHE[ticker] = cik
                logger.info(f"[{ticker}] Resolved CIK via company_tickers.json: {cik}")
                return cik

        logger.debug(f"[{ticker}] Not found in company_tickers.json, trying search API")

    except Exception as e:
        logger.warning(f"[{ticker}] company_tickers.json lookup failed: {e}")

    # 3. EDGAR full-text search API（fallback）
    try:
        time.sleep(0.15)
        search_url = "https://efts.sec.gov/LATEST/search-index"
        params = {
            "q": f'"{ticker}"',
            "dateRange": "custom",
            "startdt": "2020-01-01",
            "forms": "10-K",
        }
        resp = sess.get(search_url, params=params, timeout=15)
        resp.raise_for_status()
        hits = resp.json().get("hits", {}).get("hits", [])

        for hit in hits:
            src = hit.get("_source", {})
            entity_id = src.get("entity_id", "")
            tickers = src.get("tickers", [])
            if ticker in [t.upper() for t in tickers] and entity_id:
                # entity_id 格式為 "CIK0000789019" 或純數字
                raw = re.sub(r"[^0-9]", "", entity_id)
                if raw:
                    cik = raw.zfill(10)
                    _CIK_CACHE[ticker] = cik
                    logger.info(f"[{ticker}] Resolved CIK via search API: {cik}")
                    return cik

    except Exception as e:
        logger.warning(f"[{ticker}] Search API lookup failed: {e}")

    

def preload_cik_cache(tickers: list[str], session: Optional[requests.Session] = None) -> dict[str, str]:
    """
    批次預載 CIK，利用 company_tickers.json 一次拿全部（比逐個查快）。
    回傳 {ticker: cik} dict，並更新 global cache。
    """
    sess = session or requests.Session()
    sess.headers.update(EDGAR_HEADERS)

    upper_tickers = {t.upper() for t in tickers}
    result: dict[str, str] = {}

    try:
        time.sleep(0.15)
        resp = sess.get(
            "https://www.sec.gov/files/company_tickers.json",
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        for entry in data.values():
            t = entry.get("ticker", "").upper()
            if t in upper_tickers:
                cik = str(entry["cik_str"]).zfill(10)
                _CIK_CACHE[t] = cik
                result[t] = cik

        missing = upper_tickers - set(result.keys())
        if missing:
            logger.warning(f"CIK not found in bulk lookup for: {missing}")

        logger.info(f"Preloaded {len(result)} CIKs: {result}")
        return result

    except Exception as e:
        logger.warning(f"Bulk CIK preload failed: {e}, will fall back to individual lookups")
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# Helper functions（保留 v2 原版邏輯）
# ══════════════════════════════════════════════════════════════════════════════

def _parse_date(d: Optional[str]) -> Optional[date]:
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return None


def _period_days(start: Optional[str], end: Optional[str]) -> Optional[int]:
    s = _parse_date(start)
    e = _parse_date(end)
    if s and e:
        return (e - s).days
    return None


def _is_valid_period(entry: dict, filing_type: str, xbrl_tag: str = "") -> bool:
    if xbrl_tag in BALANCE_SHEET_TAGS:
        return True

    days = _period_days(entry.get("start"), entry.get("end"))
    if days is None:
        return False

    if filing_type == "10-K":
        return ANNUAL_MIN_DAYS <= days <= ANNUAL_MAX_DAYS

    if filing_type == "10-Q":
        return QUARTERLY_MIN_DAYS <= days <= QUARTERLY_MAX_DAYS

    return False


def _dedupe_by_period(
    entries: list[dict],
    is_point_in_time: bool = False,
) -> list[dict]:
    seen: dict[tuple, dict] = {}
    for e in entries:
        key = (e.get("end"),) if is_point_in_time else (e.get("start"), e.get("end"))
        existing = seen.get(key)
        if not existing:
            seen[key] = e
        else:
            e_date  = _parse_date(e.get("filed"))        or date.min
            ex_date = _parse_date(existing.get("filed")) or date.min
            if e_date > ex_date:
                seen[key] = e
    return list(seen.values())


# ══════════════════════════════════════════════════════════════════════════════
# Main Client
# ══════════════════════════════════════════════════════════════════════════════

class SECEdgarClient:
    SUBMISSION_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
    FACTS_URL      = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    def __init__(self, rate_limit_seconds: float = 0.15):
        self.session = requests.Session()
        self.session.headers.update(EDGAR_DATA_HEADERS)
        self.rate_limit = rate_limit_seconds

    def _get(self, url: str) -> dict:
        time.sleep(self.rate_limit)
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _resolve(self, ticker: str) -> str:
        """Resolve ticker to CIK, using shared session for efficiency."""
        return resolve_cik(ticker, session=self.session)

    # ── Public API ────────────────────────────────────────────────────────────

    def get_company_submissions(self, ticker: str) -> dict:
        """Fetch company submissions metadata. Dynamically resolves CIK."""
        cik = self._resolve(ticker)
        return self._get(self.SUBMISSION_URL.format(cik=cik))

    def get_company_facts(self, ticker: str) -> dict:
        """Fetch XBRL company facts. Dynamically resolves CIK."""
        cik = self._resolve(ticker)
        return self._get(self.FACTS_URL.format(cik=cik))

    def get_latest_filings(
        self,
        ticker: str,
        filing_type: str = "10-K",
        count: int = 5,
    ) -> list[dict]:
        submissions = self.get_company_submissions(ticker)
        recent = submissions.get("filings", {}).get("recent", {})

        keys = ["accessionNumber", "filingDate", "reportDate", "form", "primaryDocument"]
        lists = [recent.get(k, []) for k in keys]

        if not all(lists):
            logger.warning(f"[{ticker}] Missing filing fields in submissions response")
            return []

        rows = [dict(zip(keys, row)) for row in zip(*lists) if row[3] == filing_type]
        return rows[:count]

    def extract_financial_facts(self, ticker: str) -> dict:
        """
        從 companyfacts API 提取結構化財務數據。
        保留 v2 所有 point-in-time / duration 驗證邏輯。
        """
        facts_data = self.get_company_facts(ticker)
        us_gaap    = facts_data.get("facts", {}).get("us-gaap", {})

        metrics_map: dict[str, dict[str, str]] = {
            "income_statement": {
                "Revenues":                                              "revenue",
                "RevenueFromContractWithCustomerExcludingAssessedTax":   "revenue_alt",
                "GrossProfit":                                           "gross_profit",
                "OperatingIncomeLoss":                                   "operating_income",
                "NetIncomeLoss":                                         "net_income",
                "EarningsPerShareBasic":                                 "eps_basic",
                "EarningsPerShareDiluted":                               "eps_diluted",
                "InterestExpense":                                       "interest_expense",
                # Some filers (e.g. AMZN) stopped tagging InterestExpense and
                # switched to InterestExpenseNonoperating instead — same concept,
                # different tag over time. Same pattern as revenue/revenue_alt.
                "InterestExpenseNonoperating":                           "interest_expense_alt",
                "DepreciationDepletionAndAmortization":                  "da",
                "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest": "income_before_tax",
                "IncomeTaxExpenseBenefit":                               "income_tax_expense",
                "CostOfRevenue":                                         "cost_of_revenue",
                "CostOfGoodsAndServicesSold":                            "cost_of_revenue_alt",
                # Filers with no COGS line (e.g. Coinbase) report a single
                # "Total operating expenses" figure under this tag instead of
                # going through Revenue -> COGS -> GrossProfit. Not to be
                # confused with CostsAndExpenses, whose scope includes COGS
                # (see references/architecture.md).
                "OperatingExpenses":                                     "operating_expense_direct",
            },
            "balance_sheet": {
                "Assets":                                     "total_assets",
                "AssetsCurrent":                              "current_assets",
                "CashAndCashEquivalentsAtCarryingValue":      "cash",
                "Liabilities":                                "total_liabilities",
                "LiabilitiesCurrent":                         "current_liabilities",
                "LongTermDebt":                               "long_term_debt_aggregate",
                "LongTermDebtCurrent":                        "current_maturities_ltd",
                "LongTermDebtAndFinanceLeaseObligationsCurrent": "current_maturities_ltd_alt",
                "LongTermDebtNoncurrent":                     "long_term_liabilities",
                "LongTermDebtAndFinanceLeaseObligationsNoncurrent": "long_term_liabilities_alt",
                "LongTermDebtAndFinanceLeaseObligations":          "long_term_debt_aggregate_alt",
                "DebtAndCapitalLeaseObligations":                  "long_term_debt_aggregate_alt2",
                "LongTermDebtAndCapitalLeaseObligations":          "long_term_liabilities_alt2",
                "LongTermDebtAndCapitalLeaseObligationsCurrent":   "current_maturities_ltd_alt2",
                "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities": "long_term_debt_aggregate_alt3",
                "StockholdersEquity":                         "stockholders_equity",
                "RetainedEarningsAccumulatedDeficit":         "retained_earnings",
                "ShortTermBorrowings":                        "short_term_loans",
                "ShortTermNotesPayable":                      "short_term_notes_payable",
                "DebtCurrent":                                "debt_current_fallback",
                "InventoryNet":                               "inventory",
            },
            "cash_flow": {
                "NetCashProvidedByUsedInOperatingActivities":  "cfo",
                "NetCashProvidedByUsedInInvestingActivities":  "cfi",
                "NetCashProvidedByUsedInFinancingActivities":  "cff",
                "PaymentsToAcquirePropertyPlantAndEquipment":  "capex",
                "PaymentsForRepurchaseOfCommonStock":          "buybacks",
                "PaymentsOfDividendsCommonStock":              "dividends_paid",
                "RepaymentsOfDebt":                            "debt_repayment",
                "RepaymentsOfLongTermDebt":                    "debt_repayment_lt",
            },
        }

        result: dict[str, list[dict]] = {}
        ingested_at = datetime.utcnow().isoformat()

        for statement, metrics in metrics_map.items():
            result[statement] = []

            for xbrl_tag, field_name in metrics.items():
                if xbrl_tag not in us_gaap:
                    logger.debug(f"[{ticker}] XBRL tag not found: {xbrl_tag}")
                    continue

                tag_data  = us_gaap[xbrl_tag]
                units     = tag_data.get("units", {})
                unit_data: list[dict] = units.get("USD") or units.get("USD/shares") or []

                if not unit_data:
                    continue

                is_pit = xbrl_tag in BALANCE_SHEET_TAGS

                for target_form in ["10-K", "10-Q"]:
                    form_entries = [e for e in unit_data if e.get("form") == target_form]
                    valid_entries = [
                        e for e in form_entries
                        if _is_valid_period(e, target_form, xbrl_tag=xbrl_tag)
                    ]

                    if not valid_entries:
                        continue

                    deduped = _dedupe_by_period(valid_entries, is_point_in_time=is_pit)

                    for entry in deduped:
                        days = _period_days(entry.get("start"), entry.get("end"))
                        result[statement].append({
                            "ticker":           ticker,
                            "field_name":       field_name,
                            "xbrl_tag":         xbrl_tag,
                            "value":            entry.get("val"),
                            "unit":             entry.get("unit", "USD"),
                            "period_start":     entry.get("start"),
                            "period_end":       entry.get("end"),
                            "period_days":      days,
                            "filing_type":      target_form,
                            "accession_number": entry.get("accn"),
                            "filed_date":       entry.get("filed"),
                            "ingested_at":      ingested_at,
                        })

            logger.info(
                f"[{ticker}] {statement}: extracted {len(result[statement])} rows"
            )

        return result
