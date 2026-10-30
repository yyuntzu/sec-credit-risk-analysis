"""
agent_runner.py — formal Loan Review entrypoint with explicit legacy compatibility.
CLI/HTTP default: review_workflow.run_review(); --legacy opts into the historical path.
變更重點（相較於 v1）：
  + ingest_ticker() 新增 Step 7：下載 10-K / 10-Q HTML 原文 → 存 GCS
  + 新增 download_filing_html()：從 SEC EDGAR 下載單一 filing HTML
  + 新增 read_filing_html_from_gcs()：從 GCS 讀回 HTML 給 credit_memo_writer
  + analyze_ticker() 改呼叫 credit_memo_writer.generate_credit_memo()
    取代舊的 generate_markdown_report()（KPI snapshot only）
  + 保留所有 v1 功能：dbt fallback、inline BQ query、Flask routes、CLI mode
"""

import os
import re
import sys
import json
import logging
import subprocess
import time
import math
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Path fix ──────────────────────────────────────────────────────────────────
_SCRIPTS_DIR = Path(__file__).parent.resolve()
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# ── Flask: only needed for Cloud Run HTTP mode ────────────────────────────────
try:
    from flask import Flask, jsonify, request, Response
    _FLASK_AVAILABLE = True
except ImportError:
    _FLASK_AVAILABLE = False

from sec_client import SECEdgarClient, preload_cik_cache
from bq_loader import BigQueryLoader, FINANCIAL_STATEMENT_SCHEMA
from gcs_loader import GCSLoader
from dashboard_generator import DashboardGenerator
from credit_memo_writer import generate_credit_memo
from mda_commentary import generate_commentary, ALL_METRICS
if __package__:
    from .loan_review_sources import (
        load_json as load_source_json, parse_request, prepare_source_inputs,
        validate_sec_rows, write_source_bundle, prepare_legacy_source_inputs, SourceError,
    )
else:
    from loan_review_sources import (
        load_json as load_source_json, parse_request, prepare_source_inputs,
        validate_sec_rows, write_source_bundle, prepare_legacy_source_inputs, SourceError,
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def _period_to_year(period: str) -> Optional[int]:
    """
    "FY2024" → 2024 / "2024" → 2024 / "FY24" → 2024 / invalid → None
    """
    if not period:
        return None
    s = str(period).strip().upper().replace("FY", "").replace("FY ", "")
    # Handle 2-digit year: FY24 → 2024
    if len(s) == 2 and s.isdigit():
        s = "20" + s
    try:
        yr = int(s)
        if 2000 <= yr <= 2099:
            return yr
    except ValueError:
        pass
    return None


def _parse_periods(periods: Optional[list[str]]) -> Optional[list[str]]:
    """
    Validate and normalise periods list.
    Returns None if empty/invalid (caller will use auto-detect).
    Raises ValueError if periods are provided but malformed.
    """
    if not periods:
        return None

    parsed = []
    for p in periods:
        yr = _period_to_year(p)
        if yr:
            parsed.append(f"FY{yr}")

    if len(parsed) < 2:
        raise ValueError(
            f"Expected 2–4 valid fiscal year periods "
            f"(e.g. FY2024 FY2025), got: {periods}"
        )
    return sorted(parsed)  # always ascending


app = Flask(__name__) if _FLASK_AVAILABLE else None  # type: ignore

# ── Config ────────────────────────────────────────────────────────────────────
GCS_BUCKET       = os.environ.get("GCS_BUCKET_NAME", "")
PROJECT_ID       = os.environ.get("GCP_PROJECT_ID", "focus-heuristic-438521-v4")
BQ_DATASET       = os.environ.get("BQ_DATASET_ID", "sec_raw")
DEFAULT_TICKERS  = os.environ.get("TICKERS", "MSFT,AAPL,WMT").split(",")
#   ⚠️ 真正的 dbt project 在 references/dbt/（有 dbt_project.yml + profiles.yml）。
#   之前預設值指到不存在的 scripts/dbt/，導致 dbt run 每次都直接
#   FileNotFound、被 run_dbt() 吃掉當成 "best-effort skip"，
#   marts 從未真的物化成 BigQuery 表。見 references/troubleshooting.md。
DBT_PROJECT_DIR  = os.environ.get(
    "DBT_PROJECT_DIR", str(_SCRIPTS_DIR.parent / "references" / "dbt")
)
DBT_PROFILES_DIR = os.environ.get("DBT_PROFILES_DIR", DBT_PROJECT_DIR)

# 所有要落地成 BigQuery 實體表、供 Looker/Looker Studio 串接的 mart
DBT_MART_TABLES = [
    "dim_company",
    "dim_filing",
    "fct_credit_kpis",
    "fct_covenant_status",
    "fct_financial_statement_line_items",
]
OUTPUT_DIR       = os.environ.get("OUTPUT_DIR", "/tmp/sec_reports")

# SEC EDGAR base URLs
EDGAR_ARCHIVES = "https://www.sec.gov/Archives/edgar/data"
EDGAR_HEADERS  = {
    "User-Agent": os.environ.get("SEC_USER_AGENT", "sec-analysis-skill contact@example.com"),
    "Accept-Encoding": "gzip, deflate",
}


# ══════════════════════════════════════════════════════════════════════════════
# HTML Filing Download
# ══════════════════════════════════════════════════════════════════════════════

def download_filing_html(
    cik: str,
    accession_number: str,
    primary_document: str,
    session,
) -> Optional[bytes]:
    """
    從 SEC EDGAR Archives 下載單一 filing 的 HTML 原文。

    SEC 的 URL 格式：
      https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodash}/{primary_document}

    Args:
        cik:              公司 CIK（不需補零）
        accession_number: e.g. "0000320193-24-000123"（含 dash 格式）
        primary_document: e.g. "aapl-20240928.htm"（來自 submissions API）
        session:          requests.Session（共用，避免重複建立連線）

    Returns:
        HTML bytes，或 None（下載失敗時）
    """
    # accession number 去掉 dash → 變成資料夾名稱
    accession_nodash = accession_number.replace("-", "")
    cik_int = str(int(cik))  # CIK 不補零（EDGAR Archives 用原始數字）

    url = f"{EDGAR_ARCHIVES}/{cik_int}/{accession_nodash}/{primary_document}"
    logger.info(f"Downloading filing HTML: {url}")

    try:
        time.sleep(0.15)  # respect SEC rate limit
        # Override Host — sec_client.session has Host: data.sec.gov which breaks Archives URLs
        headers = {**EDGAR_HEADERS, "Host": "www.sec.gov"}
        resp = session.get(url, timeout=60, headers=headers)
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        logger.warning(f"Failed to download filing HTML ({url}): {e}")
        return None


def ingest_filing_htmls(
    ticker: str,
    cik: str,
    filings: list[dict],
    gcs_loader: GCSLoader,
    session,
    max_filings: int = 5,
) -> list[dict]:
    """
    批次下載 filing HTML 並存入 GCS。
    每個 filing 下載後立即上傳，不在記憶體中堆積。

    Args:
        ticker:      股票代號
        cik:         公司 CIK
        filings:     get_latest_filings() 回傳的 list（含 accessionNumber, primaryDocument）
        gcs_loader:  GCSLoader instance
        session:     requests.Session
        max_filings: 最多下載幾份（節省時間和費用，預設 5 份）

    Returns:
        list of {accession_number, gcs_uri, filing_date, filing_type, status}
    """
    results = []

    for filing in filings[:max_filings]:
        accession = filing.get("accessionNumber", "")
        primary_doc = filing.get("primaryDocument", "")
        filing_date = filing.get("filingDate", "")
        filing_type = filing.get("form", "")

        if not accession or not primary_doc:
            logger.warning(f"[{ticker}] Skipping filing with missing accession/document")
            continue

        html_bytes = download_filing_html(
            cik=cik,
            accession_number=accession,
            primary_document=primary_doc,
            session=session,
        )

        if html_bytes is None:
            results.append({
                "accession_number": accession,
                "filing_date": filing_date,
                "filing_type": filing_type,
                "status": "download_failed",
            })
            continue

        # 上傳到 GCS
        # 路徑: gs://{bucket}/sec/{TICKER}/raw_filings/{date}/{accession}/{filename}
        try:
            gcs_uri = gcs_loader.upload_raw_filing_html(
                content=html_bytes,
                ticker=ticker,
                accession=accession.replace("-", ""),
                filename=primary_doc,
            )
            results.append({
                "accession_number": accession,
                "filing_date": filing_date,
                "filing_type": filing_type,
                "gcs_uri": gcs_uri,
                "html_size_kb": round(len(html_bytes) / 1024, 1),
                "status": "ok",
            })
            logger.info(f"[{ticker}] {filing_type} {filing_date} → {gcs_uri}")
        except Exception as e:
            logger.error(f"[{ticker}] GCS upload failed for {accession}: {e}")
            results.append({
                "accession_number": accession,
                "filing_date": filing_date,
                "filing_type": filing_type,
                "status": f"upload_failed: {e}",
            })

    return results


# ══════════════════════════════════════════════════════════════════════════════
# Read HTML back from GCS for credit memo writer
# ══════════════════════════════════════════════════════════════════════════════

def read_filing_html_from_gcs(
    gcs_uri: str,
    gcs_loader: GCSLoader,
) -> Optional[str]:
    """
    從 GCS 讀回 filing HTML，回傳純文字（已去除 HTML tags）。

    去除 HTML tags 而非回傳原始 HTML，原因：
      - credit_memo_writer 需要的是文字內容（MD&A、numbers、management commentary）
      - 原始 HTML 含大量 style/script/XBRL tags，干擾文字分析
      - 純文字 token 數量更少，agent 處理更有效率

    Returns:
        純文字字串，或 None（讀取失敗時）
    """
    if not gcs_uri:
        return None

    try:
        # gcs_uri 格式: gs://{bucket}/{blob_path}
        # 去掉 "gs://{bucket}/" 前綴取得 blob path
        bucket_name = gcs_loader.bucket.name
        prefix = f"gs://{bucket_name}/"
        if not gcs_uri.startswith(prefix):
            logger.warning(f"Unexpected GCS URI format: {gcs_uri}")
            return None

        blob_path = gcs_uri[len(prefix):]
        blob = gcs_loader.bucket.blob(blob_path)
        html_bytes = blob.download_as_bytes()
        html_text = html_bytes.decode("utf-8", errors="replace")

        # 清洗 HTML → 純文字
        clean_text = _html_to_text(html_text)
        logger.info(f"Read {len(clean_text):,} chars from {gcs_uri}")
        return clean_text

    except Exception as e:
        logger.warning(f"Failed to read {gcs_uri}: {e}")
        return None


def _html_to_text(html: str) -> str:
    """
    最小化 HTML → 純文字轉換（不依賴 BeautifulSoup）。

    處理順序：
      1. 移除 <script>, <style>, <head> 整個 block
      2. 移除 XBRL namespace tags（<ix:*, <xbrli:*）
      3. 移除所有剩餘 HTML tags
      4. 合併多餘空白行
      5. 截斷至 120,000 字元（避免 context 過長）

    為什麼不用 BeautifulSoup？
      - 避免額外 dependency（requirements.txt 已夠重）
      - SEC 10-K HTML 結構相對規則，regex 足夠
      - 如果需要更精確的 parse，可在 requirements.txt 加 beautifulsoup4
    """
    # 1. 移除 script / style / head blocks（含內容）
    for tag in ("script", "style", "head"):
        html = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", " ", html,
                      flags=re.DOTALL | re.IGNORECASE)

    # 2. 移除 XBRL tags（保留內容）
    html = re.sub(r"</?(?:ix|xbrli|xbrldi|link|label|ref):[^>]*>", " ",
                  html, flags=re.IGNORECASE)

    # 3. 移除所有剩餘 HTML tags
    html = re.sub(r"<[^>]+>", " ", html)

    # 4. HTML entities
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    html = html.replace("&lt;", "<").replace("&gt;", ">")
    html = re.sub(r"&[a-zA-Z]{2,6};", " ", html)

    # 5. 合併多餘空白與空行
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = html.strip()

    # 6. 定位 MD&A body section，截取最多 80k 字元
    #
    # 問題：ITEM 7 在 10-K 目錄裡也出現（"Item 7 ... 21" 這種 TOC entry）。
    # 直接抓第一個 match 會定位到目錄，錯過真正的 MD&A 內文（通常在文件後半段）。
    #
    # 策略（優先順序）：
    #   A. 找 body-specific 句型（"Results of Operations  The following discussion"）
    #   B. 找所有 ITEM 7 / MD&A 出現位置，跳過後面緊跟頁碼的 TOC entry，
    #      取第一個 body entry（後面接的是實質文字，不是數字頁碼）
    #   C. Fallback：取文件後半段
    MAX_CHARS = 80_000
    mda_start = None

    # Strategy A: body-specific patterns
    _BODY_ANCHORS = [
        r"Results\s+of\s+Operations\s{1,5}The\s+following\s+discussion",
        r"(?:Net\s+sales|Total\s+net\s+sales|Revenues?)\s+(?:increased|decreased|grew|were\s+\$)",
        r"(?:fiscal\s+20\d{2}|FY\s*20\d{2})\s+(?:net\s+sales|revenues?)\s+(?:were|increased|decreased)",
    ]
    for pat in _BODY_ANCHORS:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            mda_start = m.start()
            break

    # Strategy B: find ITEM 7 occurrences, skip TOC entries (those followed by page numbers)
    if mda_start is None:
        _TOC_SUFFIX = re.compile(r'^[\s\d.]{1,10}Item\s+7A', re.IGNORECASE)
        for m in re.finditer(r'ITEM\s+7[\s.]+MANAGEMENT', html, re.IGNORECASE):
            after = html[m.end(): m.end() + 60]
            # TOC entries end with " 21" or "\n21" (page number) and then the next item
            if not re.match(r'[\s\S]{0,100}?\b\d{1,3}\s+Item\s', after, re.IGNORECASE):
                mda_start = m.start()
                break

    # Strategy C: fallback to second half of document
    if mda_start is None:
        mid = max(len(html) // 2, len(html) - MAX_CHARS * 2)
        mda_start = mid

    html = html[mda_start: mda_start + MAX_CHARS]
    return html


# ══════════════════════════════════════════════════════════════════════════════
# Core ingestion  (v2: adds HTML download as Step 7)
# ══════════════════════════════════════════════════════════════════════════════

def ingest_ticker(
    ticker: str,
    sec_client: SECEdgarClient,
    bq_loader: BigQueryLoader,
    gcs_loader: Optional[GCSLoader],
) -> dict:
    """
    完整 ingest 一支股票。

    Steps:
      1. company submissions metadata
      2. company metadata → BQ
      3. XBRL financial facts → extract
      4. XBRL JSON → GCS backup
      5. XBRL rows → BQ raw tables
      6. filing metadata list → GCS
      7. [NEW] 10-K / 10-Q HTML 原文 → 下載 → GCS  ← 這是新增的關鍵步驟

    Returns:
        stats dict，包含 filing_htmls key（每份 filing 的 GCS URI）
    """
    ticker = ticker.strip().upper()
    stats: dict = {"ticker": ticker}

    logger.info(f"=== [{ticker}] Starting ingestion (v2) ===")

    # Step 1: Submissions metadata
    submissions = sec_client.get_company_submissions(ticker)
    stats["company_name"] = submissions.get("name", ticker)
    stats["cik"] = submissions.get("cik", "")
    cik = str(submissions.get("cik", ""))

    if gcs_loader:
        stats["submissions_gcs"] = gcs_loader.upload_json(
            submissions, ticker, "submissions"
        )

    # Step 2: Company metadata → BQ
    bq_loader.load_company_metadata(ticker, submissions)

    # Step 3: XBRL facts
    financial_facts = sec_client.extract_financial_facts(ticker)
    stats["xbrl_row_counts"] = {k: len(v) for k, v in financial_facts.items()}
    logger.info(f"[{ticker}] XBRL rows: {stats['xbrl_row_counts']}")

    # Preserve an immutable observation ledger independently of legacy pivots.
    source_rows = [row for rows in financial_facts.values() for row in rows]
    validate_sec_rows(source_rows, entity=ticker, cik=str(cik).zfill(10))
    ledger = {"schema_version": 1, "entity": ticker, "cik": str(cik).zfill(10),
              "financial_facts": financial_facts}
    ledger_path = Path(OUTPUT_DIR) / f"{ticker}_source_facts.json"
    ledger_path = write_source_bundle(ledger, ledger_path)
    stats["source_ledger_path"] = str(ledger_path)

    # Step 4: XBRL JSON → GCS backup
    if gcs_loader:
        for stmt_type, rows in financial_facts.items():
            if rows:
                gcs_loader.upload_json(rows, ticker, stmt_type)

    # Step 5: XBRL rows → BQ
    stats["bq_rows"] = bq_loader.load_financial_data(ticker, financial_facts)

    # Step 6: Filing metadata list (store for reference)
    all_filings: dict[str, list[dict]] = {}
    for ft in ["10-K", "10-Q"]:
        filings = sec_client.get_latest_filings(ticker, ft, count=5)
        all_filings[ft] = filings
        if gcs_loader and filings:
            gcs_loader.upload_json(
                filings, ticker, f"filings_{ft.replace('-', '')}"
            )
        stats[f"latest_{ft}_dates"] = [f.get("filingDate", "") for f in filings]

    # ── Step 7 (NEW): Download HTML filings → GCS ────────────────────────────
    # 只有在 GCS 可用時才下載（無 GCS 設定 = 本機開發模式，跳過）
    if gcs_loader and cik:
        logger.info(f"[{ticker}] Step 7: Downloading HTML filings to GCS")
        filing_htmls: list[dict] = []

        # 優先下載最近 3 份 10-K（年報，最完整）
        ten_k_results = ingest_filing_htmls(
            ticker=ticker,
            cik=cik,
            filings=all_filings.get("10-K", []),
            gcs_loader=gcs_loader,
            session=sec_client.session,
            max_filings=3,
        )
        filing_htmls.extend(ten_k_results)

        # 補充最近 2 份 10-Q（最新季報，有 management discussion）
        ten_q_results = ingest_filing_htmls(
            ticker=ticker,
            cik=cik,
            filings=all_filings.get("10-Q", []),
            gcs_loader=gcs_loader,
            session=sec_client.session,
            max_filings=2,
        )
        filing_htmls.extend(ten_q_results)

        stats["filing_htmls"] = filing_htmls
        ok_count = sum(1 for r in filing_htmls if r.get("status") == "ok")
        logger.info(f"[{ticker}] HTML download complete: {ok_count}/{len(filing_htmls)} succeeded")

        # 把 GCS URIs 做成 {filing_type: [uri, ...]} 的 lookup，
        # 方便 analyze_ticker() 後續傳給 credit_memo_writer
        stats["html_gcs_uris"] = {}
        for r in filing_htmls:
            if r.get("status") == "ok":
                ft = r.get("filing_type", "")
                stats["html_gcs_uris"].setdefault(ft, [])
                stats["html_gcs_uris"][ft].append({
                    "gcs_uri":     r["gcs_uri"],
                    "filing_date": r["filing_date"],
                    "accession":   r["accession_number"],
                })
    else:
        if not gcs_loader:
            logger.info(
                f"[{ticker}] Step 7 skipped: GCS_BUCKET_NAME not set. "
                "HTML filings will not be downloaded. "
                "Credit memo commentary will be derived from XBRL numbers only."
            )
        stats["filing_htmls"] = []
        stats["html_gcs_uris"] = {}

    return stats


# ══════════════════════════════════════════════════════════════════════════════
# dbt integration
# ══════════════════════════════════════════════════════════════════════════════

def run_dbt(ticker: str) -> dict:
    """
    執行 dbt run，把 sec_raw 的 marts 物化成 BigQuery 實體表
    （dim_company, dim_filing, fct_credit_kpis, fct_covenant_status,
    fct_financial_statement_line_items — 見 DBT_MART_TABLES）。

    用 `--select +tag:marts` 而不是 `fct_credit_kpis+`：
      - `fct_credit_kpis+` 只建 fct_credit_kpis 和「它的下游」，
        dim_company / dim_filing / fct_financial_statement_line_items
        不是它的下游，永遠不會被建到 → Looker 缺表可用。
      - `+tag:marts` = 所有標 marts tag 的 model，加上它們的上游
        依賴（staging/intermediate views），一次全部落地。

    若 dbt 不可用或失敗，回傳 {"skipped": true, "reason": "..."}，
    pipeline 繼續走 inline query fallback（best-effort，不中斷報告產出）。
    """
    try:
        check = subprocess.run(
            ["dbt", "--version"], capture_output=True, text=True, timeout=10
        )
        if check.returncode != 0:
            return {"skipped": True, "reason": "dbt not installed"}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"skipped": True, "reason": "dbt not found in PATH"}

    if not os.path.isdir(DBT_PROJECT_DIR):
        return {
            "skipped": True,
            "reason": f"DBT_PROJECT_DIR not found: {DBT_PROJECT_DIR}",
        }

    cmd = [
        "dbt", "run",
        "--select", "+tag:marts",
        "--vars", json.dumps({"target_ticker": ticker}),
        "--profiles-dir", DBT_PROFILES_DIR,
        "--project-dir", DBT_PROJECT_DIR,
        "--target", os.environ.get("DBT_TARGET", "prod"),
    ]
    logger.info(f"[{ticker}] Running dbt: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, cwd=DBT_PROJECT_DIR
        )
        if result.returncode == 0:
            return {"success": True, "stdout": result.stdout[-2000:]}
        return {
            "success": False,
            "error": result.stderr[-1000:],
            "stdout": result.stdout[-1000:],
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "dbt timed out after 300s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def verify_marts_in_bq(ticker: str, bq_loader: "BigQueryLoader") -> dict:
    """
    dbt run 回傳 success 不保證每張 mart 表都真的有這支 ticker 的資料
    （例如某個 model 因為資料缺失自己過濾掉全部 row）。

    這裡直接查 BigQuery，確認每張 mart 表：
      1. 表存在（INFORMATION_SCHEMA.TABLES）
      2. 有這支 ticker 的 row（COUNT）

    回傳 {table_name: {"exists": bool, "row_count": int|None}}，
    讓 SKILL.md 要求的「dbt marts 落地驗證」有明確、可檢查的結果，
    不再是 dbt success/fail 兩個字就結案。
    """
    dataset = f"{PROJECT_ID}.{BQ_DATASET}"
    report: dict = {}

    try:
        existing = {
            row.table_name
            for row in bq_loader.client.query(
                f"SELECT table_name FROM `{dataset}.INFORMATION_SCHEMA.TABLES`"
            ).result()
        }
    except Exception as e:
        logger.warning(f"[{ticker}] Could not read INFORMATION_SCHEMA.TABLES: {e}")
        existing = set()

    for table in DBT_MART_TABLES:
        if table not in existing:
            report[table] = {"exists": False, "row_count": None}
            continue
        try:
            row = list(bq_loader.client.query(
                f"SELECT COUNT(*) AS n FROM `{dataset}.{table}` WHERE ticker = '{ticker}'"
            ).result())[0]
            report[table] = {"exists": True, "row_count": int(row.n)}
        except Exception as e:
            report[table] = {"exists": True, "row_count": None, "error": str(e)}

    missing = [t for t, r in report.items() if not r["exists"]]
    empty   = [t for t, r in report.items() if r["exists"] and r.get("row_count") == 0]
    if missing:
        logger.warning(f"[{ticker}] Mart tables missing from BigQuery: {missing}")
    if empty:
        logger.warning(f"[{ticker}] Mart tables exist but have 0 rows for {ticker}: {empty}")
    if not missing and not empty:
        logger.info(f"[{ticker}] All dbt marts verified in BigQuery: {list(report.keys())}")

    return report


# ══════════════════════════════════════════════════════════════════════════════
# KPI query — mart first, inline fallback
# ══════════════════════════════════════════════════════════════════════════════

def _sf(v) -> Optional[float]:
    if v is None: return None
    try:
        value = float(v)
        return value if math.isfinite(value) else None
    except (ValueError, TypeError, OverflowError):
        return None


def _enrich_rows(rows: list[dict]) -> list[dict]:
    """Legacy adapter: direct values and unambiguous arithmetic only.

    Legacy rows carry no approval/identity evidence. Pending definitions and
    conditional identities must be calculated through the Fact contract instead.
    """
    result = []
    for row in rows:
        r = dict(row)
        ca, cl = _sf(r.get("current_assets_m")), _sf(r.get("current_liabilities_m"))
        r["cost_of_sales_m"] = _sf(r.get("cost_of_revenue_m"))
        # OperatingExpenses may include COGS; no automatic semantic adoption.
        r["operating_expense_m"] = None
        # Do not infer gross profit, pre-tax income, EBITDA, debt or opening cash
        # without scope/bridge/definition evidence. Preserve direct source facts.
        for key in ("gross_profit_m", "income_before_tax_m", "beginning_cash_m"):
            r[key] = _sf(r.get(key))
        r["current_ratio_pct"] = ca / cl * 100 if ca is not None and cl not in (None, 0) else None
        r["net_cash_change_m"] = None  # A same-basis cash bridge is not available.
        for key in ("ebitda_m", "total_debt_m", "quick_ratio_pct", "debt_ratio_pct",
                    "interest_coverage_x", "ebitda_interest_x", "debt_service_m",
                    "debt_service_coverage_x", "leverage_x"):
            r[key] = None
        cfo = _sf(r.get("cfo_m"))
        r["cash_flow_ratio_pct"] = (cfo / cl * 100 if cfo is not None and cl not in (None, 0)
                                    and r.get("period_role", "").startswith("fy_") else None)
        result.append(r)
    return result


def _requested_financial_periods(payload, ticker, mode):
    """Reuse the existing request/calendar contract; labels cannot prove dates."""
    if payload is None:
        raise SourceError("Verified fiscal calendar required: supply the existing source request; FY/Q labels alone cannot establish dates")
    report, cik, as_of = parse_request(payload)
    if report.entity != ticker or (report.mode.value != mode and not (mode == "annual" and report.mode.value == "quarterly")):
        raise SourceError("Fiscal request entity/mode does not match financial query")
    if report.scope != "entity-wide" or report.currency != "USD" or report.scale != 1000000:
        raise SourceError("Legacy financial rows support entity-wide USD millions only; use the source-only path for other presentations")
    periods = tuple(p for p in report.periods if (mode == "annual" and (report.mode.value == "annual" or p.role in ("earlier_fy_end", "latest_fy_end")))
                    or (mode == "quarterly" and p.role in ("prior_interim", "current_interim")))
    if any(p.start is None or p.end is None for p in periods):
        raise SourceError("Verified fiscal start/end dates required; no date inference")
    return periods, as_of


def _period_sql(periods, prefix=""):
    # Dates have already been parsed/validated as date objects by parse_request.
    return "AND (" + " OR ".join(
        f"({prefix}period_start = DATE '{p.start.isoformat()}' AND {prefix}period_end = DATE '{p.end.isoformat()}')"
        for p in periods) + ")"


def _attach_periods(rows, periods):
    indexed = {str(r.get("period_end"))[:10]: dict(r) for r in rows}
    result = []
    for p in periods:
        r = indexed.get(p.end.isoformat(), {})
        r.update(period_start=p.start, period_end=p.end, fiscal_year=p.fiscal_year,
                 period_role=p.role, quarter_label=p.label, fiscal_month=None)
        result.append(r)
    return result


def prepare_legacy_source_query(ticker: str, bq_loader: BigQueryLoader, *, as_of=None, expected_cik=None) -> tuple:
    """Read/validate one snapshot; supply deduplicated query parameters, not raw SUMs."""
    from google.cloud import bigquery
    dataset = f"{PROJECT_ID}.{BQ_DATASET}"
    statements = ("income_statement", "balance_sheet", "cash_flow")
    sql = " UNION ALL ".join(
        f"SELECT '{statement}' AS statement_type, * FROM `{dataset}.raw_{statement}` WHERE ticker = @ticker"
        for statement in statements
    )
    config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("ticker", "STRING", ticker)])
    rows = [dict(row) for row in bq_loader.client.query(sql, job_config=config).result()]
    all_evidence = validate_sec_rows(rows, entity=ticker, cik=expected_cik or rows[0].get("cik")) if rows else {}
    if as_of is not None:
        rows = [r for r in rows if str(r.get("filed_date", ""))[:10] <= as_of.isoformat()]
    bundle = prepare_legacy_source_inputs(rows, entity=ticker)
    if as_of is not None:
        bundle.update(as_of=as_of.isoformat(), excluded={fid: "Later than explicit as_of" for fid, e in all_evidence.items() if e["document_date"] > as_of.isoformat()})
        bundle["evidence"] = all_evidence
    # Persist the exact adopted snapshot and all evidence before consuming its values.
    path = write_source_bundle({"entity": ticker, "stage": "legacy_source_adoptions", **bundle},
                              Path(OUTPUT_DIR) / f"{ticker}_legacy_sources.json")
    if not isinstance(getattr(bq_loader, "loan_review_source_paths", None), list):
        bq_loader.loan_review_source_paths = []
    bq_loader.loan_review_source_paths.append(str(path))
    parameters = []
    relations = {}
    for statement in statements:
        parameter = f"loan_review_{statement}"
        parameters.append(bigquery.ArrayQueryParameter(parameter, "STRING", [
            json.dumps(row, default=str) for row in bundle["statements"][statement]]))
        columns = ", ".join(
            f"CAST(JSON_VALUE(record, '$.{field.name}') AS {field.field_type}) AS {field.name}"
            for field in FINANCIAL_STATEMENT_SCHEMA
        )
        relations[statement] = (f"(SELECT {columns}, JSON_VALUE_ARRAY(record, '$.source_forms') AS source_forms, "
                                f"JSON_VALUE_ARRAY(record, '$.evidence_ids') AS evidence_ids "
                                f"FROM UNNEST(@{parameter}) AS record)")
    return relations, bigquery.QueryJobConfig(query_parameters=parameters), bundle["collapsed"]


def query_kpis_from_bq(ticker: str, bq_loader: BigQueryLoader, *, period_request: Optional[dict] = None) -> list[dict]:
    """
    Layer 1: fct_credit_kpis mart（dbt 產出，完整欄位）
    Layer 2: inline raw query（缺 TTM / YoY / covenant，partial）

    回傳最近 8 期，按 period_end DESC。
    """
    as_of = expected_cik = None
    if period_request is not None:
        report, expected_cik, as_of = parse_request(period_request)
        _requested_financial_periods(period_request, ticker, report.mode.value)
    source_relations, source_config, collapsed = prepare_legacy_source_query(ticker, bq_loader, as_of=as_of, expected_cik=expected_cik)
    dataset = f"{PROJECT_ID}.{BQ_DATASET}"

    # Adopted-source query: revenue, net income and explicit unavailable EBITDA.
    # balance sheet ratios, cfo, fcf.
    # Missing vs mart: TTM rolling, YoY growth flags, covenant status.
    try:
        rows = list(bq_loader.client.query(f"""
        WITH inc AS (
            SELECT ticker, period_start, period_end, MAX(filed_date) AS filed_date, MAX(filing_type) AS filing_type,
                SUM(CASE WHEN field_name IN ('revenue','revenue_alt') THEN value END) / 1e6 AS revenue_m,
                CAST(NULL AS FLOAT64) AS ebitda_m,
                SUM(CASE WHEN field_name = 'net_income'       THEN value END) / 1e6 AS net_income_m
            FROM {source_relations['income_statement']}
            WHERE ticker = '{ticker}'
              AND EXISTS (SELECT 1 FROM UNNEST(source_forms) form WHERE form IN ('10-K','10-Q'))
              AND period_days BETWEEN 70 AND 110
            GROUP BY ticker, period_start, period_end
        ),
        bal AS (
            SELECT ticker, period_end,
                SUM(CASE WHEN field_name = 'cash'                THEN value END)/1e6 AS cash_m,
                SUM(CASE WHEN field_name = 'current_assets'      THEN value END)/1e6 AS current_assets_m,
                SUM(CASE WHEN field_name = 'current_liabilities' THEN value END)/1e6 AS current_liabilities_m,
                SUM(CASE WHEN field_name = 'total_assets'        THEN value END)/1e6 AS total_assets_m,
                SUM(CASE WHEN field_name = 'total_liabilities'   THEN value END)/1e6 AS total_liabilities_m,
                CAST(NULL AS FLOAT64) AS total_debt_m
            FROM {source_relations['balance_sheet']}
            WHERE ticker = '{ticker}'
            GROUP BY 1,2
        ),
        cf AS (
            SELECT ticker, period_start, period_end,
                SUM(CASE WHEN field_name = 'cfo'   THEN value END)/1e6 AS cfo_m,
                ABS(SUM(CASE WHEN field_name = 'capex' THEN value END))/1e6 AS capex_m
            FROM {source_relations['cash_flow']}
            WHERE ticker = '{ticker}'
              AND EXISTS (SELECT 1 FROM UNNEST(source_forms) form WHERE form IN ('10-K','10-Q'))
              AND period_days BETWEEN 70 AND 110
            GROUP BY ticker, period_start, period_end
        )
        SELECT i.ticker, i.period_start, i.period_end, i.filed_date, i.filing_type,
            i.revenue_m, i.ebitda_m, i.net_income_m,
            b.cash_m, b.current_assets_m, b.current_liabilities_m,
            b.total_assets_m, b.total_liabilities_m, b.total_debt_m,
            c.cfo_m, c.capex_m,
            c.cfo_m - c.capex_m                                       AS fcf_m,
            SAFE_DIVIDE(b.current_assets_m, b.current_liabilities_m)  AS current_ratio,
            CAST(NULL AS FLOAT64) AS debt_ratio,
            SAFE_DIVIDE(b.total_debt_m, i.ebitda_m)                   AS total_leverage_ratio,
            SAFE_DIVIDE(i.ebitda_m,    i.revenue_m)                   AS ebitda_margin,
            SAFE_DIVIDE(i.net_income_m, i.revenue_m)                  AS net_margin
        FROM inc i
        LEFT JOIN bal b USING (ticker, period_end)
        LEFT JOIN cf c ON i.ticker=c.ticker AND i.period_start=c.period_start AND i.period_end=c.period_end
        ORDER BY i.period_end DESC LIMIT 8
        """, job_config=source_config).result())
        logger.info(f"[{ticker}] {len(rows)} rows from inline fallback query")
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"[{ticker}] Inline KPI query failed: {e}")
        raise SourceError("Canonical legacy source query failed") from e


def query_annual_financials(
    ticker: str,
    bq_loader: BigQueryLoader,
    periods: Optional[list[str]] = None,
    *, period_request: Optional[dict] = None,
) -> list[dict]:
    """Annual reads require the existing verified annual source request. Text FY labels alone do not establish fiscal dates."""
    requested, as_of = _requested_financial_periods(period_request, ticker, "annual")
    if periods and tuple(_period_to_year(p) for p in periods) != tuple(p.fiscal_year for p in requested):
        raise SourceError("FY labels conflict with explicit fiscal request")
    source_relations, source_config, collapsed = prepare_legacy_source_query(ticker, bq_loader, as_of=as_of, expected_cik=period_request["cik"])
    year_filter = _period_sql(requested)
    requested_sql = " UNION ALL ".join(f"SELECT DATE '{p.start}' AS period_start, DATE '{p.end}' AS period_end" for p in requested)
    limit_clause = ""

    # Layer 2: existing financial SQL over the accepted source snapshot. Filing
    # versions have already been checked and equivalent observations collapsed;
    # the legacy period-selection windows below are not a version policy.
    try:
        rows = list(bq_loader.client.query(f"""
        WITH inc_dedup AS (
            SELECT * FROM {source_relations['income_statement']}
            WHERE ticker = '{ticker}'
              {year_filter}
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        inc AS (
            SELECT ticker, period_start, period_end,
                EXTRACT(YEAR FROM period_end) AS fiscal_year,
                SUM(CASE WHEN field_name IN ('revenue','revenue_alt') THEN value END)/1e6 AS revenue_m,
                SUM(CASE WHEN field_name = 'gross_profit'    THEN value END)/1e6 AS gross_profit_m,
                SUM(CASE WHEN field_name = 'operating_income' THEN value END)/1e6 AS operating_income_m,
                SUM(CASE WHEN field_name = 'net_income'       THEN value END)/1e6 AS net_income_m,
                COALESCE(
                    SUM(CASE WHEN field_name = 'interest_expense'     THEN value END),
                    SUM(CASE WHEN field_name = 'interest_expense_alt' THEN value END)
                )/1e6 AS interest_expense_m,
                SUM(CASE WHEN field_name = 'da'                   THEN value END)/1e6 AS da_m,
                SUM(CASE WHEN field_name = 'capitalized_interest' THEN value END)/1e6 AS capitalized_interest_m,
                SUM(CASE WHEN field_name = 'income_before_tax'    THEN value END)/1e6 AS income_before_tax_m,
                SUM(CASE WHEN field_name = 'income_tax_expense'   THEN value END)/1e6 AS income_tax_m,
                SUM(CASE WHEN field_name IN ('cost_of_revenue','cost_of_revenue_alt') THEN value END)/1e6 AS cost_of_revenue_m,
                SUM(CASE WHEN field_name = 'operating_expense_direct' THEN value END)/1e6 AS operating_expense_direct_m
            FROM inc_dedup
            GROUP BY ticker, period_start, period_end, fiscal_year
        ),
        cf_dedup AS (
            SELECT * FROM {source_relations['cash_flow']}
            WHERE ticker = '{ticker}'
              {year_filter}
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        cf AS (
            SELECT ticker, period_start, period_end,
                SUM(CASE WHEN field_name = 'cfo'   THEN value END)/1e6 AS cfo_m,
                SUM(CASE WHEN field_name = 'cfi'   THEN value END)/1e6 AS cfi_m,
                SUM(CASE WHEN field_name = 'cff'   THEN value END)/1e6 AS cff_m,
                ABS(SUM(CASE WHEN field_name = 'capex' THEN value END))/1e6 AS capex_m
            FROM cf_dedup
            GROUP BY ticker, period_start, period_end
        ),
        bal_dedup AS (
            SELECT * FROM {source_relations['balance_sheet']}
            WHERE ticker = '{ticker}'
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        bal AS (
            SELECT ticker, period_end,
                SUM(CASE WHEN field_name = 'cash'                THEN value END)/1e6 AS cash_m,
                SUM(CASE WHEN field_name = 'total_assets'        THEN value END)/1e6 AS total_assets_m,
                CAST(NULL AS FLOAT64) AS total_debt_m,
                SUM(CASE WHEN field_name = 'current_assets'      THEN value END)/1e6 AS current_assets_m,
                SUM(CASE WHEN field_name = 'current_liabilities' THEN value END)/1e6 AS current_liabilities_m,
                SUM(CASE WHEN field_name = 'total_liabilities'   THEN value END)/1e6 AS total_liabilities_m,
                SUM(CASE WHEN field_name = 'stockholders_equity' THEN value END)/1e6 AS equity_m,
                SUM(CASE WHEN field_name = 'inventory'           THEN value END)/1e6 AS inventory_m,
CAST(NULL AS FLOAT64) AS short_term_debt_m
            FROM bal_dedup
            GROUP BY 1,2
        )
        SELECT
            i.fiscal_year, requested.period_start, requested.period_end,
            i.revenue_m, i.gross_profit_m, i.operating_income_m,
            i.net_income_m, i.interest_expense_m, i.da_m, i.capitalized_interest_m,
            i.income_before_tax_m, i.income_tax_m, i.cost_of_revenue_m,
            i.operating_expense_direct_m,
            cf.cfo_m, cf.cfi_m, cf.cff_m, cf.capex_m,
            b.cash_m, b.total_assets_m, b.total_debt_m,
            b.current_assets_m, b.current_liabilities_m,
            b.total_liabilities_m, b.equity_m, b.inventory_m, b.short_term_debt_m,
            cf.cfo_m - cf.capex_m AS fcf_m,
            SAFE_DIVIDE(b.current_assets_m, b.current_liabilities_m)  AS current_ratio,
            CAST(NULL AS FLOAT64) AS debt_ratio,
            CAST(NULL AS FLOAT64) AS interest_coverage,
            CAST(NULL AS FLOAT64) AS leverage_ratio
        FROM ({requested_sql}) requested
        LEFT JOIN inc i ON requested.period_start = i.period_start AND requested.period_end = i.period_end
        LEFT JOIN cf  ON requested.period_end = cf.period_end AND requested.period_start = cf.period_start
        LEFT JOIN bal b ON i.ticker = b.ticker  AND i.period_end = b.period_end
        ORDER BY requested.period_end ASC
        {limit_clause}
        """, job_config=source_config).result())
        logger.info(f"[{ticker}] {len(rows)} annual rows from raw inline fallback")
        return _attach_periods(rows, requested)
    except Exception as e:
        logger.warning(f"[{ticker}] Annual financials query failed: {e}")
        raise SourceError("Canonical legacy source query failed") from e


def query_quarterly_financials(
    ticker: str,
    bq_loader: BigQueryLoader,
    quarter_labels: Optional[list[str]] = None,
    *, period_request: Optional[dict] = None,
) -> list[dict]:
    """Comparable YTD reads use the existing quarterly request and exact start/end. No calendar-quarter or duration-window inference."""
    requested, as_of = _requested_financial_periods(period_request, ticker, "quarterly")
    if quarter_labels:
        labels = []
        for label in quarter_labels:
            match = re.fullmatch(r"Q([1-3])(\d{4})|(\d{4})Q([1-3])", label.upper().replace(" ", ""))
            if match is None:
                raise SourceError("Quarter labels cannot be matched to verified fiscal request")
            labels.append((int(match[2]), int(match[1])) if match[1] else (int(match[3]), int(match[4])))
        if tuple(labels) != tuple((p.fiscal_year, p.quarter) for p in requested):
            raise SourceError("Quarter labels conflict with explicit fiscal request")
    source_relations, source_config, collapsed = prepare_legacy_source_query(ticker, bq_loader, as_of=as_of, expected_cik=period_request["cik"])
    where_clause = _period_sql(requested)
    requested_sql = " UNION ALL ".join(f"SELECT DATE '{p.start}' AS period_start, DATE '{p.end}' AS period_end" for p in requested)
    limit_clause = len(requested)

    def _with_quarter_labels(rows):
        return _attach_periods(rows, requested)

    # Layer 2: accepted source snapshot; see query_annual_financials().
    try:
        rows = list(bq_loader.client.query(f"""
        WITH inc_dedup AS (
            SELECT * FROM {source_relations['income_statement']}
            WHERE ticker = '{ticker}'
              {where_clause}
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        inc AS (
            SELECT ticker, period_start, period_end,
                EXTRACT(YEAR  FROM period_end) AS fiscal_year,
                EXTRACT(MONTH FROM period_end) AS fiscal_month,
                SUM(CASE WHEN field_name IN ('revenue','revenue_alt') THEN value END)/1e6 AS revenue_m,
                SUM(CASE WHEN field_name = 'gross_profit'    THEN value END)/1e6 AS gross_profit_m,
                SUM(CASE WHEN field_name = 'operating_income' THEN value END)/1e6 AS operating_income_m,
                SUM(CASE WHEN field_name = 'net_income'       THEN value END)/1e6 AS net_income_m,
                COALESCE(
                    SUM(CASE WHEN field_name = 'interest_expense'     THEN value END),
                    SUM(CASE WHEN field_name = 'interest_expense_alt' THEN value END)
                )/1e6 AS interest_expense_m,
                SUM(CASE WHEN field_name = 'da'                   THEN value END)/1e6 AS da_m,
                SUM(CASE WHEN field_name = 'capitalized_interest' THEN value END)/1e6 AS capitalized_interest_m,
                SUM(CASE WHEN field_name = 'income_before_tax'    THEN value END)/1e6 AS income_before_tax_m,
                SUM(CASE WHEN field_name = 'income_tax_expense'   THEN value END)/1e6 AS income_tax_m,
                SUM(CASE WHEN field_name IN ('cost_of_revenue','cost_of_revenue_alt') THEN value END)/1e6 AS cost_of_revenue_m,
                SUM(CASE WHEN field_name = 'operating_expense_direct' THEN value END)/1e6 AS operating_expense_direct_m
            FROM inc_dedup
            GROUP BY ticker, period_start, period_end, fiscal_year, fiscal_month
        ),
        cf_dedup AS (
            SELECT * FROM {source_relations['cash_flow']}
            WHERE ticker = '{ticker}'
              {where_clause}
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        cf AS (
            SELECT ticker, period_start, period_end,
                SUM(CASE WHEN field_name = 'cfo'   THEN value END)/1e6 AS cfo_m,
                SUM(CASE WHEN field_name = 'cfi'   THEN value END)/1e6 AS cfi_m,
                SUM(CASE WHEN field_name = 'cff'   THEN value END)/1e6 AS cff_m,
                ABS(SUM(CASE WHEN field_name = 'capex' THEN value END))/1e6 AS capex_m
            FROM cf_dedup
            GROUP BY ticker, period_start, period_end
        ),
        bal_dedup AS (
            SELECT * FROM {source_relations['balance_sheet']}
            WHERE ticker = '{ticker}'
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY ticker, period_start, period_end, field_name
                ORDER BY filed_date DESC
            ) = 1
        ),
        bal AS (
            SELECT ticker, period_end,
                SUM(CASE WHEN field_name = 'cash'                THEN value END)/1e6 AS cash_m,
                SUM(CASE WHEN field_name = 'total_assets'        THEN value END)/1e6 AS total_assets_m,
                CAST(NULL AS FLOAT64) AS total_debt_m,
                SUM(CASE WHEN field_name = 'current_assets'      THEN value END)/1e6 AS current_assets_m,
                SUM(CASE WHEN field_name = 'current_liabilities' THEN value END)/1e6 AS current_liabilities_m,
                SUM(CASE WHEN field_name = 'total_liabilities'   THEN value END)/1e6 AS total_liabilities_m,
                SUM(CASE WHEN field_name = 'stockholders_equity' THEN value END)/1e6 AS equity_m,
                SUM(CASE WHEN field_name = 'inventory'           THEN value END)/1e6 AS inventory_m,
CAST(NULL AS FLOAT64) AS short_term_debt_m
            FROM bal_dedup
            GROUP BY 1,2
        )
        SELECT
            i.fiscal_year, i.fiscal_month, requested.period_start, requested.period_end,
            i.revenue_m, i.gross_profit_m, i.operating_income_m,
            i.net_income_m, i.interest_expense_m, i.da_m, i.capitalized_interest_m,
            i.income_before_tax_m, i.income_tax_m, i.cost_of_revenue_m,
            i.operating_expense_direct_m,
            cf.cfo_m, cf.cfi_m, cf.cff_m, cf.capex_m,
            b.cash_m, b.total_assets_m, b.total_debt_m,
            b.current_assets_m, b.current_liabilities_m,
            b.total_liabilities_m, b.equity_m, b.inventory_m, b.short_term_debt_m,
            cf.cfo_m - cf.capex_m AS fcf_m,
            SAFE_DIVIDE(b.current_assets_m, b.current_liabilities_m)  AS current_ratio,
            CAST(NULL AS FLOAT64) AS debt_ratio,
            CAST(NULL AS FLOAT64) AS interest_coverage,
            CAST(NULL AS FLOAT64) AS leverage_ratio
        FROM ({requested_sql}) requested
        LEFT JOIN inc i ON requested.period_start = i.period_start AND requested.period_end = i.period_end
        LEFT JOIN cf  ON requested.period_end = cf.period_end AND requested.period_start = cf.period_start
        LEFT JOIN bal b ON requested.period_end = b.period_end
        ORDER BY requested.period_end ASC
        LIMIT {limit_clause}
        """, job_config=source_config).result())

        result = _with_quarter_labels(rows)
        logger.info(f"[{ticker}] {len(result)} quarterly rows from raw inline fallback")
        return result

    except Exception as e:
        logger.warning(f"[{ticker}] Quarterly financials query failed: {e}")
        raise SourceError("Canonical legacy source query failed") from e


# ══════════════════════════════════════════════════════════════════════════════
# Main analysis pipeline
# ══════════════════════════════════════════════════════════════════════════════

def query_loan_review_source_rows(ticker: str, cik: str, bq_loader) -> list[dict]:
    """Read lossless candidates only; never use legacy KPI/pivot fallbacks.

    Query parameters isolate entity; validate_sec_rows independently rejects mixed
    identities or old rows without lineage. Missing staging is an explicit error.
    """
    from google.cloud import bigquery
    config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("ticker", "STRING", ticker),
        bigquery.ScalarQueryParameter("cik", "STRING", cik),
    ])
    sql = f"""
        SELECT * FROM `{bq_loader.dataset_ref}.stg_loan_review_sources`
        WHERE ticker = @ticker AND (cik = @cik OR cik IS NULL)
    """
    rows = [dict(r) for r in bq_loader.client.query(sql, job_config=config).result()]
    validate_sec_rows(rows, entity=ticker, cik=cik)
    return rows


def prepare_loan_review_source_stage(ticker: str, request_payload: dict,
                                     supplements=(), *, snapshot=None,
                                     bq_loader=None, sec_client=None) -> dict:
    """Block 2 entrypoint; no dbt calculations, LLM, legacy enrich or writer."""
    if sum(backend is not None for backend in (snapshot, bq_loader, sec_client)) > 1:
        raise SourceError("Choose one source backend explicitly")
    report, cik, _ = parse_request(request_payload)
    if report.entity != ticker.strip().upper():
        raise SourceError("Requested ticker differs from source request entity")
    if snapshot is not None:
        if (not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1
                or snapshot.get("entity") != report.entity or snapshot.get("cik") != cik):
            raise SourceError("Source snapshot entity/CIK/schema mismatch")
        financial = snapshot.get("financial_facts")
        if not isinstance(financial, dict) or set(financial) != {"income_statement", "balance_sheet", "cash_flow"}:
            raise SourceError("Source snapshot must contain the three statement lists")
        if not all(isinstance(records, list) for records in financial.values()):
            raise SourceError("Source snapshot statement values must be lists")
        rows = [row for records in financial.values() for row in records]
    elif bq_loader is not None:
        rows = query_loan_review_source_rows(report.entity, cik, bq_loader)
    else:
        client = sec_client or SECEdgarClient()
        financial = client.extract_financial_facts(report.entity)
        rows = [row for records in financial.values() for row in records]
    return prepare_source_inputs(request_payload, rows, supplements)


def analyze_ticker(
    ticker: str,
    periods: Optional[list[str]] = None,
    quarter_labels: Optional[list[str]] = None,
    generate_html: bool = True,
    source_request: Optional[dict] = None,
    supplemental_evidence: tuple = (),
    source_snapshot: Optional[dict] = None,
    period_request: Optional[dict] = None,
    formal_report: bool = False,
    report_output_dir: Optional[str] = None,
) -> dict:
    """
    Low-level compatibility API. New integrations should call review_workflow.run_review().

    完整分析一支股票。

    Args:
        ticker:         股票代號，e.g. "WMT"
        periods:        四個會計年度，e.g. ["FY2022","FY2023","FY2024","FY2025"]
                        用來 filter BQ query 和作為 credit memo 欄位標題。
                        None = 自動取最近四年。
        quarter_labels: 選填，插入表格的季度欄位，e.g. ["Q1 2025", "Q1 2026"]
                        None = 純年度 YOY 格式（向下相容）
                        提供時，credit memo 欄位變成：
                          2022Y | 2023Y | Q1 2025 | 2024Y | Q1 2026 | 2025Y
                          （annual 和 quarterly 按 period_end 排序交錯）
        generate_html:  是否輸出 HTML dashboard

    Pipeline:
      1–7  ingest_ticker()            XBRL + HTML → BQ + GCS
      8    run_dbt()                  best-effort，失敗不中斷
      9    query_kpis_from_bq()       季度 KPI（TTM 比率等）
      10a  query_annual_financials()  年度數據（YOY 報表，按 periods filter）
      10b  query_quarterly_financials() 季度數據（混合欄位，按 quarter_labels）
      11   read_filing_html_from_gcs() 讀最新 10-K 原文給 commentary
      12   generate_credit_memo()     8 sections credit memo
      13   DashboardGenerator()       HTML dashboard
    """
    ticker = ticker.strip().upper()
    if formal_report and source_request is None:
        raise SourceError("Formal report requires the existing explicit source request")
    if source_request is None and (supplemental_evidence or source_snapshot is not None):
        raise SourceError("Supplement/snapshot requires an explicit source request")
    if source_request is not None:
        bundle = prepare_loan_review_source_stage(
            ticker, source_request, supplemental_evidence, snapshot=source_snapshot)
        path = Path(OUTPUT_DIR) / f"{ticker}_loan_review_sources.json"
        path = write_source_bundle(bundle, path)
        if formal_report:
            if __package__:
                from .loan_review_pipeline import report_from_source_bundle, write_report_artifacts
            else:
                from loan_review_pipeline import report_from_source_bundle, write_report_artifacts
            report, acceptance = report_from_source_bundle(bundle)
            directory = report_output_dir or str(Path(OUTPUT_DIR) / (ticker + "_" + bundle["mode"] + "_review"))
            artifacts = write_report_artifacts(report, acceptance, directory, source_bundle=bundle)
            return {"ticker": ticker, "status": "report_review_prepared", "mode": bundle["mode"],
                    "source_inputs_path": str(path), "acceptance_blockers": acceptance['acceptance_blockers'], **artifacts}
        return {"ticker": ticker, "status": "source_inputs_prepared", "mode": bundle["mode"],
                "source_inputs_path": str(path), "conflict_count": bundle["conflict_count"],
                "final_report_accepted": False}
    try:
        requested_mode = period_request.get("mode") if isinstance(period_request, dict) else None
        _requested_financial_periods(period_request, ticker, requested_mode or "annual")
        if quarter_labels and requested_mode != "quarterly":
            raise SourceError("Quarter labels conflict with explicit annual mode")
    except (ValueError, TypeError) as exc:
        return {"ticker": ticker, "status": "error", "error": str(exc), "final_report_accepted": False}
    periods = _parse_periods(periods)  # normalise + validate
    output: dict = {"ticker": ticker, "periods": periods, "status": "running",
                    "final_report_accepted": False, "report_path_type": "legacy_unvalidated"}

    # Initialize clients
    sec_client = SECEdgarClient(rate_limit_seconds=0.15)
    bq_loader  = BigQueryLoader(project_id=PROJECT_ID, dataset_id=BQ_DATASET)
    gcs_loader = GCSLoader(bucket_name=GCS_BUCKET) if GCS_BUCKET else None

    # Ensure BQ infrastructure
    bq_loader.ensure_dataset()
    for table in ["raw_income_statement", "raw_balance_sheet",
                  "raw_cash_flow", "raw_company"]:
        bq_loader.ensure_table(table)

    # Steps 1–7: Ingest (XBRL + HTML)
    try:
        ingest_stats = ingest_ticker(ticker, sec_client, bq_loader, gcs_loader)
        output["ingest"] = ingest_stats
        company_name = ingest_stats.get("company_name", ticker)
        cik          = ingest_stats.get("cik", "")
        html_uris    = ingest_stats.get("html_gcs_uris", {})
    except Exception as e:
        logger.error(f"[{ticker}] Ingestion failed: {e}", exc_info=True)
        output["status"] = "error"
        output["error"]  = f"Ingestion failed: {e}"
        return output

    # Step 8: dbt (best-effort) — materializes marts as real BigQuery tables
    output["dbt"] = run_dbt(ticker)
    output["dbt_marts"] = verify_marts_in_bq(ticker, bq_loader)

    try:
        # Step 9: Quarterly KPIs
        kpis = query_kpis_from_bq(ticker, bq_loader, period_request=period_request)
        output["kpi_rows"] = len(kpis)

        # Step 10a: Annual financials (for YOY tables, filtered by periods)
        annual = _enrich_rows(query_annual_financials(ticker, bq_loader, periods=periods, period_request=period_request))
        output["annual_rows"] = len(annual)

        # Step 10b: Quarterly financials (optional — only when quarter_labels specified)
        quarterly: list[dict] = []
        if requested_mode == "quarterly":
            quarterly = _enrich_rows(query_quarterly_financials(
                ticker, bq_loader, quarter_labels=quarter_labels, period_request=period_request
            ))
            output["quarterly_rows"] = len(quarterly)
            logger.info(f"[{ticker}] Quarterly cols: {[r.get('quarter_label') for r in quarterly]}")

    except Exception as exc:
        output.update(status="error", error=f"Legacy source validation/query failed: {exc}")
        return output
    output["source_adoption_paths"] = bq_loader.loan_review_source_paths

    # Step 11: Match narrative to the review basis. Quarterly Loan Reviews
    # need current YTD MD&A and guidance from the latest 10-Q.
    filing_text: Optional[str] = None
    filing_text_source: str = "none"

    if gcs_loader:
        filing_priority = ["10-Q", "10-K"] if requested_mode == "quarterly" else ["10-K", "10-Q"]
        for ft in filing_priority:
            uri_list = html_uris.get(ft, [])
            if uri_list:
                # uri_list 已按 filing_date 排序（ingest_filing_htmls 保持原順序）
                # 第一個 = 最新
                latest_uri = uri_list[0]["gcs_uri"]
                filing_text = read_filing_html_from_gcs(latest_uri, gcs_loader)
                if filing_text:
                    filing_text_source = f"{ft} {uri_list[0]['filing_date']}"
                    logger.info(
                        f"[{ticker}] Filing text loaded: {filing_text_source} "
                        f"({len(filing_text):,} chars)"
                    )
                    break

    if not filing_text:
        logger.warning(
            f"[{ticker}] No filing HTML available. "
            "Credit memo commentary will be based on XBRL numbers only."
        )

    # Step 11b: LLM reads the MD&A once and explains every metric the memo
    # needs — replaces the old regex/keyword-search approach that used to
    # live in credit_memo_writer.py. No fallback: if this fails (no API
    # credentials, network error, safety refusal), it raises and the ticker
    # is reported as an error by the caller, same as an ingestion failure —
    # we don't silently degrade to a worse-quality memo.
    commentary: dict[str, str] = {}
    if filing_text:
        commentary = generate_commentary(
            filing_text=filing_text,
            metrics=ALL_METRICS,
            company_name=company_name,
            period_label=filing_text_source,
        )
        logger.info(f"[{ticker}] MD&A commentary generated for {len(commentary)} metrics")

    # Step 12: Generate full credit memo (8 sections)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    memo = generate_credit_memo(
        ticker=ticker,
        company_name=company_name,
        kpis=kpis,
        annual_financials=annual,
        quarterly_financials=quarterly,
        periods=periods,
        commentary=commentary,
        filing_text_source=filing_text_source,
        mode=requested_mode,
    )

    memo_path = Path(OUTPUT_DIR) / f"{ticker}_credit_memo.md"
    memo_path.write_text(memo, encoding="utf-8")
    output["memo_path"]   = str(memo_path)
    output["memo_chars"]  = len(memo)
    output["filing_text_source"] = filing_text_source

    # Step 13: HTML dashboard
    if generate_html and kpis:
        try:
            gen  = DashboardGenerator()
            html = gen.generate(ticker=ticker, company_name=company_name, kpis=kpis)
            html_path = Path(OUTPUT_DIR) / f"{ticker}_dashboard.html"
            html_path.write_text(html, encoding="utf-8")
            output["html_path"]    = str(html_path)
            output["html_size_kb"] = round(len(html) / 1024, 1)
        except Exception as e:
            logger.error(f"[{ticker}] Dashboard failed: {e}", exc_info=True)
            output["html_error"] = str(e)

    output["status"] = "success"
    return output


def run_ingestion(tickers: list[str], requests=None, **options) -> dict:
    """Formal batch entrypoint; each ticker requires its own explicit request."""
    try:
        from .review_workflow import run_review
    except ImportError:
        from review_workflow import run_review
    summary = {}
    for ticker in tickers:
        try:
            summary[ticker] = run_review(ticker, (requests or {}).get(ticker), **options)
        except Exception as e:
            logger.error(f"Failed: {ticker}: {e}", exc_info=True)
            summary[ticker] = {"status": "error", "error": str(e)}
    return summary


def formal_http_review(ticker, body):
    """Use the same formal workflow as CLI; reject ambiguous/ignored options."""
    try:
        from .review_workflow import run_review
    except ImportError:
        from review_workflow import run_review
    if not isinstance(body, dict): raise ValueError('JSON object required')
    allowed = {'review_request', 'period_request', 'source_request', 'source', 'source_snapshot',
               'supplements', 'execution', 'html', 'excel', 'source_run_id'}
    unknown = set(body) - allowed
    if unknown: raise ValueError('Unsupported options: ' + ', '.join(sorted(unknown)))
    requests = [body[k] for k in ('review_request', 'period_request', 'source_request') if k in body]
    if len(requests) != 1: raise ValueError('Provide exactly one review_request object with verified fiscal dates')
    for key in ('html', 'excel'):
        if key in body and not isinstance(body[key], bool): raise ValueError(key + ' must be boolean')
    if not isinstance(body.get('supplements', []), list): raise ValueError('supplements must be an array')
    return run_review(ticker, requests[0], source=body.get('source', 'snapshot' if 'source_snapshot' in body else 'sec'),
        snapshot=body.get('source_snapshot'), supplements=tuple(body.get('supplements', ())),
        execution=body.get('execution', 'local'), html=body.get('html', True), excel=body.get('excel', True),
        source_run_id=body.get('source_run_id'))


# ══════════════════════════════════════════════════════════════════════════════
# Flask routes
# ══════════════════════════════════════════════════════════════════════════════

if _FLASK_AVAILABLE and app is not None:

    @app.route("/run", methods=["POST", "GET"])
    def trigger_ingestion():
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or set(body) != {'reviews'} or not isinstance(body['reviews'], list) or not body['reviews']:
            return jsonify({'error': 'Provide a nonempty reviews array with ticker and review_request per item'}), 400
        results = []
        for item in body['reviews']:
            if not isinstance(item, dict) or not isinstance(item.get('ticker'), str):
                return jsonify({'error': 'Each review requires a ticker string'}), 400
        for item in body['reviews']:
            try: results.append(formal_http_review(item['ticker'], {k: v for k, v in item.items() if k != 'ticker'}))
            except (ValueError, TypeError) as exc: return jsonify({'error': str(exc), 'completed': results}), 400
        return jsonify({'result': results, 'success': all(r['status'] == 'accepted' for r in results)}), 500 if any(r['status'] == 'failed' for r in results) else 200

    @app.route("/analyze/<ticker>", methods=["GET", "POST"])
    def analyze_single(ticker: str):
        try: result = formal_http_review(ticker.upper(), request.get_json(silent=True))
        except (ValueError, TypeError) as exc: return jsonify({'error': str(exc)}), 400
        return jsonify(result), 500 if result['status'] == 'failed' else 200

    @app.route("/memo/<ticker>", methods=["GET"])
    def get_memo(ticker: str):
        p = Path(OUTPUT_DIR) / f"{ticker.upper()}_credit_memo.md"
        if p.exists():
            return Response(p.read_text(encoding="utf-8"), mimetype="text/plain")
        return jsonify({"error": f"No memo for {ticker}"}), 404

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "project": PROJECT_ID,
                        "dataset": BQ_DATASET, "gcs": bool(GCS_BUCKET)}), 200


def run_source_cli(argv: list[str]) -> Optional[int]:
    """Parse source options before dispatch, including argparse's --option=value."""
    import argparse
    probe = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    probe.add_argument("--source-request")
    probe.add_argument("--source-snapshot")
    probe.add_argument("--supplement", action="append", default=[])
    options, _ = probe.parse_known_args(argv)
    if not any(v is not None for v in (options.source_request, options.source_snapshot)) and not options.supplement:
        return None
    parser = argparse.ArgumentParser(description="Loan Review Block 2: prepare auditable source inputs only", allow_abbrev=False)
    parser.add_argument("ticker")
    parser.add_argument("--source-request", required=True)
    parser.add_argument("--source-snapshot", help="Offline extracted ledger; omit to read SEC")
    parser.add_argument("--supplement", action="append", default=[])
    opts = parser.parse_args(argv)
    try:
        result = analyze_ticker(
            opts.ticker, source_request=load_source_json(opts.source_request),
            source_snapshot=load_source_json(opts.source_snapshot) if opts.source_snapshot else None,
            supplemental_evidence=tuple(load_source_json(p) for p in opts.supplement))
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


def run_report_cli(argv: list[str]) -> Optional[int]:
    """Full strict report pipeline, reusing the source request/snapshot/supplements."""
    import argparse
    probe = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    probe.add_argument("--report-request")
    options, _ = probe.parse_known_args(argv)
    if options.report_request is None:
        return None
    parser = argparse.ArgumentParser(description="Calculate, render and validate the Loan Review contract", allow_abbrev=False)
    parser.add_argument("ticker")
    parser.add_argument("--report-request", required=True)
    parser.add_argument("--source-snapshot")
    parser.add_argument("--supplement", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    opts = parser.parse_args(argv)
    try:
        result = analyze_ticker(opts.ticker, source_request=load_source_json(opts.report_request),
            source_snapshot=load_source_json(opts.source_snapshot) if opts.source_snapshot else None,
            supplemental_evidence=tuple(load_source_json(p) for p in opts.supplement),
            formal_report=True, report_output_dir=opts.output_dir, generate_html=False)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get('final_report_accepted') else 2 if result.get('technical_validation_passed') else 1


def run_period_cli(argv: list[str]) -> Optional[int]:
    """Reuse source-request schema for explicit legacy periods; no new data contract."""
    import argparse
    probe = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    probe.add_argument("--period-request")
    options, _ = probe.parse_known_args(argv)
    if options.period_request is None:
        return None
    parser = argparse.ArgumentParser(description="Legacy report with verified fiscal periods (not final acceptance)", allow_abbrev=False)
    parser.add_argument("ticker")
    parser.add_argument("--period-request", required=True, help="Existing annual/quarterly source-request JSON schema")
    parser.add_argument("--no-html", action="store_true")
    opts = parser.parse_args(argv)
    try:
        result = analyze_ticker(opts.ticker, period_request=load_source_json(opts.period_request), generate_html=not opts.no_html)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and '--legacy' not in sys.argv and not any(a.split('=')[0] == '--source-request' for a in sys.argv):
        try:
            from .review_workflow import cli
        except ImportError:
            from review_workflow import cli
        sys.exit(cli(sys.argv[1:]))
    if '--legacy' in sys.argv:
        sys.argv.remove('--legacy')
    report_exit = run_report_cli(sys.argv[1:])
    if report_exit is not None:
        sys.exit(report_exit)
    source_exit = run_source_cli(sys.argv[1:])
    if source_exit is not None:
        sys.exit(source_exit)
    period_exit = run_period_cli(sys.argv[1:])
    if period_exit is not None:
        sys.exit(period_exit)
    if len(sys.argv) > 1:
        # CLI usage:
        #   python agent_runner.py WMT --periods FY2022 FY2023 FY2024 FY2025
        #   python agent_runner.py AMZN META --no-html
        args = sys.argv[1:]
        generate_html = "--no-html" not in args
        args = [a for a in args if a != "--no-html"]

        # Parse --periods FY2022 FY2023 FY2024 FY2025
        periods_cli: Optional[list[str]] = None
        if "--periods" in args:
            idx = args.index("--periods")
            period_values = []
            for a in args[idx + 1:]:
                if a.startswith("--"):
                    break
                period_values.append(a)
            if period_values:
                periods_cli = period_values
            args = [a for i, a in enumerate(args) if i != idx and a not in period_values]

        # Parse --quarters "Q4 2024" "Q4 2025"
        quarters_cli: Optional[list[str]] = None
        if "--quarters" in args:
            idx = args.index("--quarters")
            quarter_values = []
            for a in args[idx + 1:]:
                if a.startswith("--"):
                    break
                quarter_values.append(a)
            if quarter_values:
                quarters_cli = quarter_values
            args = [a for i, a in enumerate(args) if i != idx and a not in quarter_values]

        tickers_arg = [t for t in args if not t.startswith("--")]

        if not tickers_arg:
            print("Usage: python agent_runner.py TICKER [TICKER2] --periods FY2022 FY2023 FY2024 FY2025")
            sys.exit(1)

        if periods_cli is None:
            print("Verified fiscal dates are required: use --period-request REQUEST.json. FY labels alone do not establish dates.")
            print("   To specify: --periods FY2022 FY2023 FY2024 FY2025")

        logger.info(f"CLI: tickers={tickers_arg}  periods={periods_cli}  html={generate_html}")

        preload_cik_cache(tickers_arg)
        results = {}
        for t in tickers_arg:
            try:
                results[t] = analyze_ticker(
                    t,
                    periods=periods_cli,
                    quarter_labels=quarters_cli,
                    generate_html=generate_html,
                )
            except ValueError as e:
                print(f"❌ {t}: {e}")
                results[t] = {"status": "error", "error": str(e)}
            except Exception as e:
                logger.error(f"Failed: {t}: {e}", exc_info=True)
                results[t] = {"status": "error", "error": str(e)}

        for t, r in results.items():
            print(f"\n{'='*60}\n  {t}: {r.get('status')}")
            if r.get("periods"):
                print(f"  Periods      → {' '.join(r['periods'])}")
            if r.get("memo_path"):
                print(f"  Credit Memo  → {r['memo_path']}")
            if r.get("html_path"):
                print(f"  Dashboard    → {r['html_path']}")
            if r.get("filing_text_source") and r.get("filing_text_source") != "none":
                print(f"  Filing text  → {r['filing_text_source']}")
            if r.get("dbt_marts"):
                ok = [t for t, s in r["dbt_marts"].items() if s.get("exists") and s.get("row_count")]
                bad = [t for t in r["dbt_marts"] if t not in ok]
                print(f"  dbt marts    → {len(ok)}/{len(r['dbt_marts'])} landed in BigQuery"
                      + (f"  (missing/empty: {bad})" if bad else ""))
    elif _FLASK_AVAILABLE and app:
        app.run(host="0.0.0.0", port=8080, debug=True)
    else:
        print("Usage: python agent_runner.py TICKER --periods FY2022 FY2023 FY2024 FY2025 [--quarters 'Q1 2025' 'Q1 2026']")
