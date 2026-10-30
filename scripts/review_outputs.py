"""Present the canonical formal report without a second financial calculation path."""
from dataclasses import asdict
from decimal import Decimal
from html import escape
import json
from pathlib import Path

try:
    from .loan_review_contract import METRICS, AVAILABLE
except ImportError:
    from loan_review_contract import METRICS, AVAILABLE


def report_payload(report):
    return json.loads(json.dumps(asdict(report), default=str, ensure_ascii=False))


def write_dashboard(report, acceptance, directory):
    """Static, self-contained HTML; every displayed cell is bound to a formal Fact."""
    e = lambda value: escape(str(value), quote=True)
    parts = [f'<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>{e(report.entity)} Loan Review</title>',
        '<style>body{font:16px system-ui;margin:32px;color:#243746}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border:1px solid #cbd5e1;padding:10px;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#e8eef4}details{margin:12px 0}.pending{color:#9a3412}small{color:#475569}</style>',
        f'<h1>{e(report.entity)} · Loan Review</h1>',
        f'<p>{e(report.mode.value)} · {e(report.currency)} · scale={e(report.scale)}</p>',
        '<h2>' + ('正式驗收通過' if acceptance['final_report_accepted'] else '待驗收覆核稿') + '</h2>',
        '<ul>' + ''.join(f'<li class="pending">{e(x)}</li>' for x in acceptance['acceptance_blockers']) + '</ul>']
    periods = {p.role: p.label for p in report.periods}
    for table in report.tables:
        parts += [f'<h2>{e(table.spec.heading)}</h2><table><thead><tr><th>科目</th>']
        parts += [f'<th>{e("營收占比 · " + periods[c[4:]] if c.startswith("pct:") else periods[c])}</th>' for c in table.spec.columns]
        parts.append('</tr></thead><tbody>')
        for metric, cells in zip(table.spec.rows, table.cells):
            parts.append(f'<tr><th>{e(METRICS[metric].label)}</th>')
            for fid in cells:
                f = report.facts[fid]
                if f.status in AVAILABLE and f.unit != 'text':
                    value = Decimal(f.value)
                    if f.unit in ('percent', 'percentage_points'): value *= 100
                    label = f'{abs(value):,.2f}'
                    if value < 0: label = '(' + label + ')'
                    label += '%' if f.unit == 'percent' else ' pp' if f.unit == 'percentage_points' else 'x' if f.unit == 'multiple' else ''
                else:
                    label = f.value if f.status in AVAILABLE else f.status.value
                parts.append(f'<td data-fact-id="{e(fid)}" data-status="{e(f.status.value)}" title="{e(f.reason or f.definition)}">{e(label)}</td>')
            parts.append('</tr>')
        parts.append('</tbody></table>')
        for narrative in table.narratives + table.notes:
            parts.append(f'<p>{e(narrative.text or narrative.reason)}</p>')
    parts.append('<h2>來源與計算依據</h2>')
    for f in report.facts.values():
        parts.append(f'<details><summary>{e(f.id)} · {e(f.status.value)}</summary><p>{e(f.definition)}</p><p>{e(f.reason)}</p><p>Formula: {e(f.formula_id or "—")} · Inputs: {e(", ".join(f.input_ids))}</p>')
        for eid in f.evidence_ids:
            evidence = report.evidence[eid]
            parts.append(f'<p>{e(eid)} · {e(evidence.locator)}<br>{e(evidence.content)}</p>')
        parts.append('</details>')
    parts.append('</html>')
    target = Path(directory) / 'dashboard.html'
    target.write_text('\n'.join(parts), encoding='utf-8')
    return str(target.resolve())
