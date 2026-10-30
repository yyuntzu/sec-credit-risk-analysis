"""
SEC EDGAR API Client v3 — 動態 CIK 查詢版
改動重點（相較於 v2）:
  1. 移除硬編碼 COMPANY_CIK dict
  2. 新增 resolve_cik(ticker) — 用 EDGAR company search API 動態查詢
  3. CIK 結果 in-memory cache，同一 session 不重複查詢
  4. get_company_submissions / get_company_facts 自動呼叫 resolve_cik
  5. Block 2: preserve exact periods, units and all filing versions with source IDs
"""

import os
import re
import time
import logging
import hashlib
import json
from decimal import Decimal
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
    "ShortTermBorrowings",
    "DebtCurrent",
    "InventoryNet",
    "AccountsReceivableNetCurrent",
    "AllowanceForDoubtfulAccountsReceivableCurrent",
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

    raise ValueError(f"Cannot resolve CIK for ticker {ticker!r}")

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
    """Classify by the concept's period kind, never by the filing's form/year.

    A 10-K can repeat quarterly data; a 10-Q can repeat annual comparative data.
    Retain exact intervals for later request-based matching, including amendments.
    """
    if filing_type not in ("10-K", "10-K/A", "10-Q", "10-Q/A"):
        return False
    if _parse_date(entry.get("end")) is None:
        return False
    if xbrl_tag in BALANCE_SHEET_TAGS:
        return entry.get("start") is None
    days = _period_days(entry.get("start"), entry.get("end"))
    return days is not None and days >= 0


def _dedupe_by_period(entries: list[dict], is_point_in_time: bool = False) -> list[dict]:
    """Remove exact repetitions only. Never select latest filing/value silently."""
    seen = {}
    for entry in entries:
        key = json.dumps(entry, sort_keys=True, default=str)
        seen.setdefault(key, entry)
    return list(seen.values())


def financial_fact_id(row: dict) -> str:
    """Immutable observation identity; a changed value/version is a new record."""
    fields = ("ticker", "cik", "scope", "field_name", "namespace", "xbrl_tag",
              "unit", "period_kind", "period_start", "period_end", "filing_type",
              "accession_number", "filed_date", "original_value", "source_locator",
              "filing_fiscal_year", "filing_fiscal_period")
    key = json.dumps({k: row.get(k) for k in fields}, sort_keys=True, default=str)
    return "sec:" + hashlib.sha256(key.encode()).hexdigest()


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
        return json.loads(resp.text, parse_float=Decimal)

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
        保留 instant/duration 真實期間及所有申報版本，不默選最新值。
        """
        ticker = ticker.strip().upper()
        expected_cik = self._resolve(ticker)
        facts_data = self.get_company_facts(ticker)
        actual_cik = str(facts_data.get("cik", "")).zfill(10)
        if not expected_cik or actual_cik != expected_cik:
            raise ValueError("SEC companyfacts entity does not match requested CIK")
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
                "InterestCostsCapitalized":                              "capitalized_interest",
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
                "AccountsReceivableNetCurrent":                "accounts_receivable_net",
                "AllowanceForDoubtfulAccountsReceivableCurrent": "receivables_allowance",
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
                for unit, unit_data in units.items():
                    # Unit is the enclosing companyfacts key, not an entry field.
                    for entry in _dedupe_by_period(unit_data):
                        form = entry.get("form", "")
                        if not _is_valid_period(entry, form, xbrl_tag):
                            continue
                        if not entry.get("accn") or not _parse_date(entry.get("filed")):
                            raise ValueError(f"{ticker}/{xbrl_tag}: missing filing identity")
                        value = entry.get("val")
                        if value is not None:
                            if isinstance(value, bool) or not Decimal(str(value)).is_finite():
                                raise ValueError(f"{ticker}/{xbrl_tag}: invalid numeric value")
                        row = {
                            "ticker": ticker,
                            "cik": actual_cik,
                            "scope": "entity-wide",
                            "field_name": field_name,
                            "namespace": "us-gaap",
                            "xbrl_tag": xbrl_tag,
                            "value": float(value) if value is not None else None,
                            "original_value": str(value) if value is not None else None,
                            "unit": unit,
                            "period_kind": "instant" if xbrl_tag in BALANCE_SHEET_TAGS else "duration",
                            "period_start": entry.get("start"),
                            "period_end": entry["end"],
                            "period_days": _period_days(entry.get("start"), entry["end"]),
                            "filing_type": form,
                            "accession_number": entry["accn"],
                            "filed_date": entry["filed"],
                            "source_version": entry["accn"] + ":" + entry["filed"],
                            "source_url": self.FACTS_URL.format(cik=actual_cik),
                            "document_url": f"https://www.sec.gov/Archives/edgar/data/{int(actual_cik)}/{entry['accn'].replace('-', '')}/{entry['accn']}-index.html",
                            "source_locator": json.dumps({"namespace": "us-gaap", "tag": xbrl_tag, "unit": unit, "entry": entry}, sort_keys=True, default=str),
                            # fy/fp describe the filing context, not necessarily the fact period.
                            "filing_fiscal_year": entry.get("fy"),
                            "filing_fiscal_period": entry.get("fp"),
                            "ingested_at": ingested_at,
                        }
                        row["fact_id"] = financial_fact_id(row)
                        result[statement].append(row)

            logger.info(
                f"[{ticker}] {statement}: extracted {len(result[statement])} rows"
            )

        return result
