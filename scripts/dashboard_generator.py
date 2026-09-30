"""
dashboard_generator.py — 從 BQ KPI 數據生成獨立 HTML Dashboard

Layout（參考截圖）:
  Row 1: KPI Cards — Net Sales, Gross Margin, Operating Margin, Net Income,
                      LTM EBITDA, Total Leverage, Interest Coverage, DSCR
  Row 2: Liquidity Ratios bar chart  |  Cash Flow Summary waterfall
  Row 3: Revenue & EBITDA Trend (grouped bar)
  Row 4: Covenant Status table（traffic light）

輸出：單一 .html 檔案（內嵌 Chart.js，無外部依賴）
"""

import json
from datetime import datetime
from typing import Optional


class DashboardGenerator:
    """Generate a self-contained HTML credit analysis dashboard."""

    CHART_JS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"

    def generate(
        self,
        ticker: str,
        company_name: str,
        kpis: list[dict],
        covenant_rows: Optional[list[dict]] = None,
    ) -> str:
        """
        生成完整 HTML dashboard string。

        Args:
            ticker: 股票代號，e.g. "AMZN"
            company_name: 公司全名，e.g. "Amazon.com Inc"
            kpis: list of KPI dicts（from fct_credit_kpis or inline query）
                  按 period_end DESC 排序
            covenant_rows: list of covenant status dicts（可選）
        """
        if not kpis:
            return self._empty_html(ticker)

        latest = kpis[0]
        # Reverse for chronological chart display
        kpis_chron = list(reversed(kpis[:8]))

        labels = [str(r.get("period_end", ""))[-7:] for r in kpis_chron]  # e.g. "2024-09"

        def _f(val, default=0.0):
            try:
                return round(float(val or default), 2)
            except (TypeError, ValueError):
                return default

        def _fmt_m(val) -> str:
            if val is None:
                return "N/A"
            try:
                v = float(val)
                if abs(v) >= 1000:
                    return f"${v/1000:.1f}B"
                return f"${v:.1f}M"
            except (TypeError, ValueError):
                return "N/A"

        def _fmt_x(val, decimals=2) -> str:
            if val is None:
                return "No data"
            try:
                return f"{float(val):.{decimals}f}x"
            except (TypeError, ValueError):
                return "No data"

        def _fmt_pct(val) -> str:
            if val is None:
                return "N/A"
            try:
                return f"{float(val)*100:.1f}%"
            except (TypeError, ValueError):
                return "N/A"

        def _flag_color(flag) -> str:
            m = {
                "CRITICAL": "#ef4444",
                "WARNING": "#f59e0b",
                "OK": "#10b981",
                "NO_DATA": "#94a3b8",
                "INCOMPLETE": "#3b82f6",
            }
            return m.get(str(flag or "").upper(), "#94a3b8")

        def _traffic_color(tc) -> str:
            m = {"red": "#ef4444", "yellow": "#f59e0b", "green": "#10b981", "grey": "#94a3b8"}
            return m.get(str(tc or "").lower(), "#94a3b8")

        # ── KPI Card values ──────────────────────────────────────────────────
        revenue_m   = _fmt_m(latest.get("ttm_revenue_m") or latest.get("revenue_m"))
        ebitda_m    = _fmt_m(latest.get("ttm_ebitda_m") or latest.get("ebitda_m"))
        net_inc_m   = _fmt_m(latest.get("ttm_net_income_m") or latest.get("net_income_m"))
        gross_margin = _fmt_pct(latest.get("gross_margin"))
        op_margin    = _fmt_pct(latest.get("ebitda_margin") or
                                (latest.get("ttm_ebitda_m", 0) or 0) /
                                max(latest.get("ttm_revenue_m", 1) or 1, 1))
        total_lev    = _fmt_x(latest.get("total_leverage_ratio"))
        int_cov      = _fmt_x(latest.get("interest_coverage_ratio"))
        dscr         = _fmt_x(latest.get("dscr"))

        # ── Liquidity chart data ─────────────────────────────────────────────
        liq_labels = ["Current ratio", "Quick ratio", "Cash flow ratio", "Debt ratio"]
        liq_values = [
            _f(latest.get("current_ratio")),
            _f(latest.get("quick_ratio")),
            _f(latest.get("cash_flow_ratio")),
            _f(latest.get("debt_ratio")),
        ]
        liq_colors = [
            _flag_color(latest.get("current_ratio_flag")),
            _flag_color(latest.get("current_ratio_flag")),
            _flag_color(latest.get("cash_flow_ratio_flag")),
            _flag_color(latest.get("debt_ratio_flag")),
        ]

        # ── Cash flow waterfall ──────────────────────────────────────────────
        cfo_val  = _f(latest.get("ttm_cfo_m") or latest.get("cfo_m"))
        capex_val = _f(latest.get("ttm_capex_m") or latest.get("capex_m"))
        cff_val  = _f(latest.get("cff_m"), 0)
        cfi_val  = _f(latest.get("cfi_m"), 0)
        fcf_val  = _f(latest.get("ttm_fcf_m") or latest.get("fcf_m"))
        ending_cash = _f(latest.get("cash_m"))

        # ── Revenue & EBITDA trend ────────────────────────────────────────────
        trend_revenue = [
            _f(r.get("ttm_revenue_m") or r.get("revenue_m")) for r in kpis_chron
        ]
        trend_ebitda = [
            _f(r.get("ttm_ebitda_m") or r.get("ebitda_m")) for r in kpis_chron
        ]

        # ── Covenant table ────────────────────────────────────────────────────
        cov_rows_html = ""
        if covenant_rows:
            for i, row in enumerate(covenant_rows, 1):
                tc = row.get("traffic_light", "grey")
                dot_color = _traffic_color(tc)
                req = row.get("requirement_display", "")
                actual = row.get("actual_value")
                headroom = row.get("headroom_absolute")
                name = row.get("covenant_name", "")
                cov_rows_html += f"""
                <tr>
                    <td>{i}.</td>
                    <td>{name}</td>
                    <td>{req}</td>
                    <td>{_fmt_x(actual) if actual is not None else "null"}</td>
                    <td>{_fmt_x(headroom) if headroom is not None else "null"}</td>
                    <td><span style="display:inline-block;width:12px;height:12px;
                        border-radius:50%;background:{dot_color};"></span></td>
                </tr>"""
        else:
            # Placeholder rows
            placeholders = [
                ("total_leverage_ratio", "≤ 3x"),
                ("interest_coverage_ratio", "≥ 8x"),
                ("debt_ratio", "≤ 0.65x"),
                ("net_leverage_ratio", "≤ 2.5x"),
            ]
            for i, (name, req) in enumerate(placeholders, 1):
                val = latest.get(name)
                tc = "grey" if val is None else "green"
                dot_color = _traffic_color(tc)
                cov_rows_html += f"""
                <tr>
                    <td>{i}.</td>
                    <td>{name}</td>
                    <td>{req}</td>
                    <td>{"null" if val is None else _fmt_x(val)}</td>
                    <td>null</td>
                    <td><span style="display:inline-block;width:12px;height:12px;
                        border-radius:50%;background:{dot_color};"></span></td>
                </tr>"""

        # ── Serialize chart data ──────────────────────────────────────────────
        labels_json      = json.dumps(labels)
        liq_labels_json  = json.dumps(liq_labels)
        liq_values_json  = json.dumps(liq_values)
        liq_colors_json  = json.dumps(liq_colors)
        trend_rev_json   = json.dumps(trend_revenue)
        trend_ebt_json   = json.dumps(trend_ebitda)

        cf_labels_json   = json.dumps(["Operating CF", "Investing CF", "Financing CF", "Ending cash"])
        cf_values_json   = json.dumps([cfo_val, cfi_val, cff_val, ending_cash])
        cf_colors_json   = json.dumps([
            "#3b82f6" if cfo_val >= 0 else "#ef4444",
            "#ef4444" if cfi_val <= 0 else "#3b82f6",
            "#ef4444" if cff_val <= 0 else "#3b82f6",
            "#3b82f6",
        ])

        as_of   = str(latest.get("period_end", ""))
        gen_ts  = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        overall_flag  = str(latest.get("overall_risk_flag", "N/A"))
        overall_color = _flag_color(overall_flag)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{ticker} Credit Analysis</title>
<script src="{self.CHART_JS_CDN}"></script>
<style>
  :root {{
    --blue: #2563eb;
    --orange: #f59e0b;
    --red: #ef4444;
    --green: #10b981;
    --gray: #64748b;
    --bg: #f8fafc;
    --card: #ffffff;
    --border: #e2e8f0;
    --text: #0f172a;
    --muted: #64748b;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: var(--bg); color: var(--text); font-size: 14px; }}

  /* Header */
  .header {{ background: var(--card); border-bottom: 2px solid var(--blue);
             padding: 12px 24px; display: flex; align-items: center;
             justify-content: space-between; }}
  .header h1 {{ font-size: 13px; font-weight: 700; color: var(--blue);
               letter-spacing: 1.5px; text-transform: uppercase; }}
  .header-right {{ display: flex; gap: 16px; align-items: center; }}
  .header-right select {{ border: 1px solid var(--border); border-radius: 4px;
                          padding: 4px 28px 4px 8px; font-size: 13px;
                          appearance: none; background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2364748b'/%3E%3C/svg%3E") no-repeat right 8px center; }}
  .badge {{ padding: 4px 10px; border-radius: 12px; font-size: 11px;
            font-weight: 600; color: white; background: {overall_color}; }}

  /* Layout */
  .main {{ padding: 20px 24px; max-width: 1200px; margin: 0 auto; }}

  /* KPI Row */
  .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
              margin-bottom: 20px; }}
  .kpi-card {{ background: var(--card); border: 1px solid var(--border);
              border-radius: 8px; padding: 16px 18px; }}
  .kpi-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase;
               letter-spacing: 0.5px; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 22px; font-weight: 700; color: var(--text); }}
  .kpi-value.muted {{ color: var(--muted); font-size: 18px; }}
  .kpi-sub {{ font-size: 11px; color: var(--muted); margin-top: 2px; }}

  /* Chart Row */
  .chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
               margin-bottom: 20px; }}
  .chart-card {{ background: var(--card); border: 1px solid var(--border);
                border-radius: 8px; padding: 16px; }}
  .chart-card h3 {{ font-size: 12px; font-weight: 600; color: var(--text);
                   margin-bottom: 12px; text-transform: uppercase;
                   letter-spacing: 0.5px; }}
  .chart-full {{ background: var(--card); border: 1px solid var(--border);
                border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
  .chart-full h3 {{ font-size: 12px; font-weight: 600; color: var(--text);
                   margin-bottom: 12px; text-transform: uppercase;
                   letter-spacing: 0.5px; }}
  .legend {{ display: flex; gap: 16px; margin-bottom: 8px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px;
                 font-size: 12px; color: var(--muted); }}
  .legend-dot {{ width: 12px; height: 12px; border-radius: 2px; }}

  /* Covenant table */
  .table-card {{ background: var(--card); border: 1px solid var(--border);
                border-radius: 8px; overflow: hidden; margin-bottom: 20px; }}
  .table-card table {{ width: 100%; border-collapse: collapse; }}
  .table-card th {{ background: #f1f5f9; padding: 10px 14px;
                   text-align: left; font-size: 11px; font-weight: 600;
                   color: var(--muted); text-transform: uppercase;
                   letter-spacing: 0.5px; border-bottom: 1px solid var(--border); }}
  .table-card td {{ padding: 10px 14px; font-size: 13px;
                   border-bottom: 1px solid var(--border); }}
  .table-card tr:last-child td {{ border-bottom: none; }}
  .table-card tr:hover td {{ background: var(--bg); }}

  /* Footer */
  .footer {{ text-align: center; font-size: 11px; color: var(--muted);
             padding: 16px; border-top: 1px solid var(--border); }}
  .pager {{ display: flex; justify-content: flex-end; align-items: center;
            gap: 8px; padding: 8px 14px; font-size: 12px; color: var(--muted); }}
</style>
</head>
<body>

<div class="header">
  <h1>Credit Financial Analysis</h1>
  <div class="header-right">
    <select><option>{company_name} ({ticker})</option></select>
    <select><option>Period: {as_of}</option></select>
    <span class="badge">{overall_flag}</span>
  </div>
</div>

<div class="main">

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Net sales</div>
      <div class="kpi-value">{revenue_m}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Gross margin</div>
      <div class="kpi-value">{gross_margin}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Operating margin</div>
      <div class="kpi-value">{op_margin}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Net income</div>
      <div class="kpi-value">{net_inc_m}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">LTM EBITDA</div>
      <div class="kpi-value">{ebitda_m}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total leverage</div>
      <div class="kpi-value {'muted' if total_lev == 'No data' else ''}">{total_lev}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Interest coverage</div>
      <div class="kpi-value muted">{int_cov}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">DSCR</div>
      <div class="kpi-value muted">{dscr}</div>
    </div>
  </div>

  <!-- Liquidity + Cash Flow -->
  <div class="chart-row">
    <div class="chart-card">
      <h3>Liquidity Ratios</h3>
      <canvas id="liqChart" height="200"></canvas>
    </div>
    <div class="chart-card">
      <h3>Cash Flow Summary</h3>
      <canvas id="cfChart" height="200"></canvas>
    </div>
  </div>

  <!-- Revenue & EBITDA Trend -->
  <div class="chart-full">
    <h3>Revenue &amp; EBITDA Trend</h3>
    <div class="legend">
      <div class="legend-item">
        <div class="legend-dot" style="background:#3b82f6"></div>
        <span>revenue_m</span>
      </div>
      <div class="legend-item">
        <div class="legend-dot" style="background:#f59e0b"></div>
        <span>ebitda_m</span>
      </div>
    </div>
    <canvas id="trendChart" height="120"></canvas>
  </div>

  <!-- Covenant Status -->
  <div class="table-card">
    <table>
      <thead>
        <tr>
          <th></th>
          <th>covenant_name</th>
          <th>requirement_display</th>
          <th>actual_value</th>
          <th>headroom_absolute</th>
          <th>traffic_light</th>
        </tr>
      </thead>
      <tbody>
        {cov_rows_html}
      </tbody>
    </table>
    <div class="pager">1 - {len(covenant_rows) if covenant_rows else 4} / {len(covenant_rows) if covenant_rows else 4} &lt; &gt;</div>
  </div>

  <div class="footer">
    Generated {gen_ts} | Source: SEC EDGAR XBRL | Period: {as_of}
  </div>

</div>

<script>
const liqLabels  = {liq_labels_json};
const liqValues  = {liq_values_json};
const liqColors  = {liq_colors_json};

const cfLabels   = {cf_labels_json};
const cfValues   = {cf_values_json};
const cfColors   = {cf_colors_json};

const trendLabels = {labels_json};
const trendRev   = {trend_rev_json};
const trendEbt   = {trend_ebt_json};

// Liquidity bar (horizontal)
new Chart(document.getElementById('liqChart'), {{
  type: 'bar',
  data: {{
    labels: liqLabels,
    datasets: [{{
      data: liqValues,
      backgroundColor: liqColors,
      borderRadius: 3,
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.parsed.x.toFixed(2)}}x`
        }}
      }}
    }},
    scales: {{
      x: {{ grid: {{ color: '#f1f5f9' }}, ticks: {{ font: {{ size: 11 }} }} }},
      y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }} }} }}
    }}
  }}
}});

// Cash flow bar
new Chart(document.getElementById('cfChart'), {{
  type: 'bar',
  data: {{
    labels: cfLabels,
    datasets: [{{
      data: cfValues,
      backgroundColor: cfColors,
      borderRadius: 3,
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.parsed.x >= 1000 ? (ctx.parsed.x/1000).toFixed(1) + 'B' : ctx.parsed.x.toFixed(1) + 'M'}}`
        }}
      }}
    }},
    scales: {{
      x: {{ grid: {{ color: '#f1f5f9' }}, ticks: {{ font: {{ size: 11 }} }} }},
      y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }} }} }}
    }}
  }}
}});

// Revenue & EBITDA trend
new Chart(document.getElementById('trendChart'), {{
  type: 'bar',
  data: {{
    labels: trendLabels,
    datasets: [
      {{
        label: 'revenue_m',
        data: trendRev,
        backgroundColor: '#3b82f6',
        borderRadius: 2,
      }},
      {{
        label: 'ebitda_m',
        data: trendEbt,
        backgroundColor: '#f59e0b',
        borderRadius: 2,
      }}
    ]
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y >= 1000 ? (ctx.parsed.y/1000).toFixed(1) + 'B' : ctx.parsed.y.toFixed(0) + 'M'}}`
        }}
      }}
    }},
    scales: {{
      x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }}, maxRotation: 45 }} }},
      y: {{ grid: {{ color: '#f1f5f9' }},
            ticks: {{
              font: {{ size: 11 }},
              callback: v => v >= 1000 ? (v/1000).toFixed(0)+'B' : v+'M'
            }} }}
    }}
  }}
}});
</script>

</body>
</html>"""

        return html

    def _empty_html(self, ticker: str) -> str:
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<title>{ticker} — No Data</title></head>
<body style="font-family:sans-serif;padding:40px;color:#64748b;">
<h2>⚠️ No KPI data available for {ticker}</h2>
<p>Please run the ingestion pipeline first.</p>
</body></html>"""
