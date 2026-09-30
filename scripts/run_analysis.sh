#!/bin/bash
# scripts/run_analysis.sh
# 固定流程：一行指令完成完整 SEC credit analysis
#
# 用法:
#   bash scripts/run_analysis.sh AMZN
#   bash scripts/run_analysis.sh AMZN,META,NVDA
#   bash scripts/run_analysis.sh AMZN --no-html
#   bash scripts/run_analysis.sh AMZN --dbt-only
#
# 輸出: /tmp/sec_reports/{TICKER}_credit_report.md
#       /tmp/sec_reports/{TICKER}_dashboard.html

set -euo pipefail

TICKERS="${1:-}"
MODE="${2:-}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp/sec_reports}"
PYTHON="${PYTHON:-python3}"

if [ -z "$TICKERS" ]; then
  echo "Usage: $0 TICKER [--no-html|--dbt-only]"
  echo "       $0 AMZN,META,NVDA"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "=== SEC Credit Analysis ==="
echo "Tickers : $TICKERS"
echo "Output  : $OUTPUT_DIR"
echo "Mode    : ${MODE:-full}"
echo ""

# Convert comma-separated to space-separated for Python
TICKER_ARGS=$(echo "$TICKERS" | tr ',' ' ')

if [ "$MODE" = "--dbt-only" ]; then
  # Just run dbt, assume data already in BQ
  for T in $TICKER_ARGS; do
    echo "--- Running dbt for $T ---"
    dbt run \
      --select "fct_credit_kpis+" \
      --vars "{\"target_ticker\": \"$T\"}" \
      --profiles-dir "${DBT_PROFILES_DIR:-./dbt}" \
      --project-dir "${DBT_PROJECT_DIR:-./dbt}" \
      --target "${DBT_TARGET:-prod}"
  done
else
  # Full pipeline via agent_runner.py
  HTML_FLAG=""
  if [ "$MODE" = "--no-html" ]; then
    HTML_FLAG="--no-html"
  fi

  $PYTHON scripts/agent_runner.py $TICKER_ARGS $HTML_FLAG
fi

echo ""
echo "=== Done ==="
echo "Reports:"
for T in $TICKER_ARGS; do
  T_UPPER=$(echo "$T" | tr '[:lower:]' '[:upper:]')
  MD="$OUTPUT_DIR/${T_UPPER}_credit_report.md"
  HTML="$OUTPUT_DIR/${T_UPPER}_dashboard.html"
  [ -f "$MD" ]   && echo "  📄 $MD"
  [ -f "$HTML" ] && echo "  📊 $HTML"
done
