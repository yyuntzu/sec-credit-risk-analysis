"""Loan Review integration: existing source inputs -> Fact -> calculation -> narrative -> QA.

No network, new metric IDs, inferred approvals or missing-to-zero. Artifacts can
pass technical validation while substantive acceptance remains explicitly blocked.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
from datetime import date
from decimal import Decimal
import json
import csv
import re
from pathlib import Path

try:
    from .loan_review_contract import (AVAILABLE, METRICS, Fact, Evidence, Narrative, Status,
        Mode, _dates, calculate_fact, calculate_identity, approved_formula_value, validate_report)
    from .loan_review_sources import parse_request, normalize_value, number, day
except ImportError:
    from loan_review_contract import (AVAILABLE, METRICS, Fact, Evidence, Narrative, Status,
        Mode, _dates, calculate_fact, calculate_identity, approved_formula_value, validate_report)
    from loan_review_sources import parse_request, normalize_value, number, day

FORMULA_VERSION = 'acceptance-v1.0-addendum-2026-10-23'


def adopt_inputs(report, inputs, candidates):
    """Adopt exact source inputs; keep pending source candidates in the audit registry."""
    facts, evidence = dict(report.facts), dict(report.evidence)
    roles_by_candidate = {}
    for item in inputs.values():
        for eid in set(item.get('candidate_ids', ())) | set(item.get('evidence_ids', ())):
            roles_by_candidate.setdefault(eid, set()).add(item['period_role'])
    for eid, roles in roles_by_candidate.items():
        c = candidates[eid]
        if c['entity'] != report.entity or c['scope'] != report.scope:
            raise ValueError('Source candidate entity/scope mismatch')
        evidence[eid] = Evidence(eid, c['entity'], c['scope'], c['source_id'], c['version'],
            day(c['document_date']), c['locator'], 'fact' if c['status'] == 'sourced' else 'review',
            tuple(sorted(roles)), json.dumps({k: c.get(k) for k in ('value', 'unit', 'scale', 'definition', 'basis', 'excerpt', 'source_url', 'reason')}, ensure_ascii=False, default=str))
    for fid, item in inputs.items():
        metric, role = item['metric'], item['period_role']
        spec = METRICS[metric]
        f = facts.get(fid)
        if f is None:
            f = Fact(fid, metric, role, Status.MISSING, None, item['unit'], spec.definition,
                day(item['start']) if item['start'] else None, day(item['end']) if item['end'] else None,
                report.entity, report.scope, currency=item.get('currency'), reason='No adopted input',
                period_kind=item['period_kind'])
        state = item['status']
        state = 'missing' if state == 'not_disclosed' else state
        ids = tuple(item.get('evidence_ids', ()))
        if state == 'conflict':
            ids = tuple(item.get('candidate_ids', ()))
        reason = item.get('reason') or 'Input unavailable'
        pending = tuple(d for d in spec.pending if d not in report.decisions)
        if pending and state == 'sourced':
            state, reason = 'not_calculable', 'Unresolved definitions: ' + ', '.join(pending) + '; source candidate retained in audit'
        elif pending:
            reason += '; Unresolved definitions: ' + ', '.join(pending)
        if state == 'conflict' and len(ids) < 2:
            state, reason = 'not_calculable', 'Unresolved source compatibility: ' + reason
        if state == 'sourced':
            if not ids:
                raise ValueError('Available source input requires evidence')
            originals = [candidates[eid] for eid in ids]
            normalized = {str(normalize_value(c['value'], c['scale'], report.scale if f.unit == 'money' else 1))
                          if f.unit != 'text' else c['value'] for c in originals}
            if len(normalized) != 1 or normalized != {str(item['value'])}:
                # Decimal strings with different trailing zeroes are equivalent.
                if f.unit == 'text' or len({number(v) for v in normalized} | {number(item['value'])}) != 1:
                    raise ValueError('Source selection/value normalization mismatch')
            c = originals[0]  # Value/definition equality was checked by source selection.
            value = item['value'] if f.unit == 'text' else number(item['value'])
            original = c['value'] if f.unit == 'text' else number(c['value'])
            f = replace(f, status=Status.SOURCED, value=value, evidence_ids=ids, reason='',
                        original_value=original, original_scale=None if f.unit == 'text' else number(c['scale']),
                        basis=item.get('basis', ''), definition=c['definition'] if not METRICS[metric].formula else spec.definition)
        else:
            f = replace(f, status=Status(state), value=None, evidence_ids=ids, reason=reason)
        facts[fid] = f
    report = replace(report, facts=facts, evidence=evidence)
    validate_report(report, expected_mode=report.mode)
    return report


def _supporting_slots(report):
    facts = dict(report.facts)
    for p in report.periods:
        for metric in ('revenue_growth', 'gross_margin', 'operating_margin', 'pretax_margin', 'operating_margin_change'):
            fid = f'{metric}:{p.role}'; spec = METRICS[metric]
            start, end = _dates(metric, p)
            facts.setdefault(fid, Fact(fid, metric, p.role, Status.NOT_CALCULABLE, None, spec.unit,
                spec.definition, start, end, report.entity, report.scope, reason='Calculation not yet possible', period_kind='duration'))
    return replace(report, facts=facts)


def calculate_report(report, identity_reviews=()):
    """Explicit existing decisions are required; reviews never become approvals."""
    report = _supporting_slots(report)
    for review in identity_reviews:
        report = calculate_identity(report, **review)
    # Supporting margins precede the change-in-margin fact.
    keys = sorted(report.facts, key=lambda fid: report.facts[fid].metric == 'operating_margin_change')
    roles = [p.role for p in report.periods]
    for fid in keys:
        f = report.facts[fid]; spec = METRICS[f.metric]
        common = ':pct:' in fid
        if f.status in AVAILABLE or (not common and not spec.formula):
            continue
        # Source conflicts are not erased by a second calculation attempt.
        if f.status in (Status.CONFLICT, Status.NOT_APPLICABLE):
            continue
        metrics = (f.metric, 'revenue') if common else spec.inputs
        ids = []
        for n, metric in enumerate(metrics):
            role = f.period_role
            if n == 1 and f.metric in ('revenue_growth', 'operating_margin_change'):
                if report.mode == Mode.ANNUAL:
                    pos = roles.index(role)
                    if pos == 0:
                        role = 'prior_period_not_in_report'
                    else:
                        role = roles[pos - 1]
                else:
                    role = 'prior_interim' if role == 'current_interim' else 'prior_period_not_in_report'
            canonical = f'{metric}:{role}'
            ids.append(canonical if canonical in report.facts else f'input:{metric}:{role}')
        report = calculate_fact(report, fid, input_ids=tuple(ids), formula_version=FORMULA_VERSION)
    return report


def _pair(report):
    return ('fy_t_minus_1', 'fy_t') if report.mode == Mode.ANNUAL else ('prior_interim', 'current_interim')


def build_narratives(report):
    """Only verifiable comparisons. No invented cause, credit judgment or filler."""
    tables = []
    income_metrics = {'revenue': 'revenue', 'gross_margin': 'gross_margin', 'operating_margin': 'operating_margin',
                      'interest_expense': 'interest_expense', 'pretax_margin': 'pretax_margin'}
    for table in report.tables:
        narratives = []
        for topic in table.spec.topics:
            prev, curr = _pair(report)
            metric = income_metrics.get(topic, topic)
            if table.spec.key != 'income':
                prev, curr = ('fy_t_minus_1', 'fy_t') if report.mode == Mode.ANNUAL else ('latest_fy_end', 'current_interim')
                metric = 'current_ratio' if topic == 'liquidity' else {'interest_coverage': 'interest_coverage', 'cash_flow_ratio': 'cash_flow_ratio'}.get(topic, topic)
            ids = (f'{metric}:{prev}', f'{metric}:{curr}')
            items = [report.facts.get(fid) for fid in ids]
            if any(f is None or f.status not in AVAILABLE for f in items):
                reasons = list(dict.fromkeys(f.reason if f else 'Required source fact not present' for f in items if f is None or f.status not in AVAILABLE))
                narratives.append(Narrative(topic, 'missing', reason='; '.join(reasons)))
                continue
            a, b = items
            def fmt(f):
                if f.unit in ('percent', 'percentage_points'): return f'{f.value * 100:,.2f}%'
                if f.unit == 'multiple': return f'{f.value:,.2f}x'
                return f'{f.value:,.2f}'
            direction = '持平' if b.value == a.value else '上升' if b.value > a.value else '下降'
            periods = {p.role: p for p in report.periods}
            text = f'{METRICS[metric].label} 由 {periods[prev].label} 的 {fmt(a)} {direction}至 {periods[curr].label} 的 {fmt(b)}。'
            if a.unit == 'percent' and metric.endswith('margin'):
                text += f'變動 {(b.value - a.value) * 100:,.2f} 個百分點。'
            if metric == 'revenue':
                growth = report.facts.get(f'revenue_growth:{curr}')
                if growth is not None and growth.status in AVAILABLE:
                    text += f'依CF-09計算成長率為 {growth.value * 100:,.2f}%。'
                    ids += (growth.id,)
            if metric == 'operating_margin':
                change = report.facts.get(f'operating_margin_change:{curr}')
                if change is not None and change.status in AVAILABLE: ids += (change.id,)
            text += '所選來源輸入未附可核實的原因證據，本段僅作數值比較。'
            narratives.append(Narrative(topic, 'supported', text=text, claim_type='comparison', fact_ids=ids,
                                        period_roles=(prev, curr)))
        tables.append(replace(table, narratives=tuple(narratives)))
    result = replace(report, tables=tuple(tables))
    validate_report(result, expected_mode=report.mode)
    return result


def validate_arithmetic(report):
    """Independent recomputation at the final boundary, separate from layout checks."""
    validate_report(report, expected_mode=report.mode)
    checked = []
    for f in report.facts.values():
        if f.status != Status.CALCULATED: continue
        values = tuple(report.facts[i].value for i in f.input_ids)
        if f.formula_id.startswith('DER-'):
            rules = {'DER-01': ('gross_profit', ('revenue', 'cost_of_revenue'), -1),
                     'DER-02': ('cost_of_revenue', ('revenue', 'gross_profit'), -1),
                     'DER-03': ('operating_expense', ('gross_profit', 'operating_income'), -1),
                     'DER-04': ('operating_income', ('gross_profit', 'operating_expense'), -1),
                     'DER-05': ('pretax_profit', ('net_income', 'income_tax'), 1),
                     'DER-06': ('net_income', ('pretax_profit', 'income_tax'), -1)}
            if f.formula_id not in rules: raise ValueError('Unapproved identity formula')
            target, components, sign = rules[f.formula_id]
            items = [report.facts[i] for i in f.input_ids]
            if f.metric != target or tuple(i.metric for i in items) != components:
                raise ValueError('Identity formula components mismatch')
            if any((i.start, i.end, i.period_role, i.currency) != (f.start, f.end, f.period_role, f.currency) for i in items):
                raise ValueError('Identity input period/unit mismatch')
            expected = values[0] + sign * values[1]
        else:
            if f.formula_id == 'CASH-CHANGE-v1' and not any(report.evidence[eid].kind == 'definition' for eid in f.evidence_ids):
                raise ValueError('Cash change requires an explicit reviewed same-basis complete bridge')
            expected = approved_formula_value(f.formula_id, values)
        if expected is None or f.value != expected:
            raise ValueError(f'Arithmetic verification failed: {f.id}')
        checked.append(f.id)
    return checked


def validate_rendered_report(report, markdown):
    """Check emitted heading hierarchy, exact table dimensions and bound numbers."""
    headings = tuple((len(m[1]), m[2]) for line in markdown.splitlines()
                     if (m := re.fullmatch(r'(#{1,6}) (.+)', line)))
    if headings != report.headings:
        raise ValueError('Rendered report headings differ from contract')
    groups, current = [], []
    for line in markdown.splitlines() + ['']:
        if line.startswith('|'): current.append(line)
        elif current:
            groups.append(current); current = []
    if len(groups) != len(report.tables): raise ValueError('Rendered table count mismatch')
    for table, lines in zip(report.tables, groups):
        if len(lines) != len(table.spec.rows) + 2: raise ValueError('Rendered row count mismatch')
        cells = [[c.strip() for c in re.split(r'(?<!\\)\|', line)[1:-1]] for line in lines]
        if any(len(row) != len(table.spec.columns) + 1 for row in cells):
            raise ValueError('Rendered column count mismatch')
        periods = {p.role: p for p in report.periods}
        for label, column in zip(cells[0][1:], table.spec.columns):
            period = periods[column.removeprefix('pct:')]
            expected = '% of revenue' if column.startswith('pct:') else (
                period.end.isoformat() if table.spec.key in ('ratios', 'leverage') and period.end else period.label)
            expected = expected.replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')
            if label != expected: raise ValueError('Rendered period binding mismatch')
        for metric, row, ids in zip(table.spec.rows, cells[2:], table.cells):
            expected_label = METRICS[metric].label
            if metric in ('revenue', 'cost_of_revenue'):
                allowed = {'Revenues', 'Net Sales', 'Net sales', 'Operating Cost', 'Cost Of Goods Sold', 'Cost of revenues', 'Cost of sales', 'Cost of services'}
                source_labels = {report.facts[i].definition for i in ids if report.facts[i].status in AVAILABLE and report.facts[i].unit == 'money'}
                if len(source_labels) == 1 and next(iter(source_labels)) in allowed:
                    expected_label = next(iter(source_labels))
            if row[0].split('／', 1)[0] != expected_label:
                raise ValueError('Rendered metric label mismatch')
            for text, fid in zip(row[1:], ids):
                f = report.facts[fid]
                if f.status not in AVAILABLE:
                    if re.fullmatch(r'[+-]?[\d,.]+(?:%|x)?', text):
                        raise ValueError('Rendered unavailable fact as a number')
                    continue
                if f.unit == 'text':
                    if text != str(f.value).replace('|', '\\|').replace('\n', ' '):
                        raise ValueError('Rendered text/basis mismatch')
                else:
                    suffix = '%' if f.unit == 'percent' else 'x' if f.unit == 'multiple' else ''
                    number = f.value * 100 if f.unit == 'percent' else f.value
                    if text != f'{number:,.2f}{suffix}':
                        raise ValueError(f'Rendered value/unit mismatch: {fid}')
    if any(token in markdown for token in ('[value]', '[refer to MD&A]', '{{value}}')):
        raise ValueError('Unfilled template placeholder in rendered report')
    return True


def automatic_reconciliation_checks(report):
    """Report missing reconciliation evidence instead of silently omitting QA.

    Asset/equity composition and full cash/FX definitions cannot be inferred from
    the registered metrics alone. Explicit reviewed source bridges are required.
    """
    checks = []
    for p in report.periods:
        for kind, metrics, reason in (
            ('cash_bridge', ('beginning_cash', 'ending_cash', 'cfo', 'cfi', 'cff'),
             '完整現金／受限制現金口徑、FX及其他調節未核實；不得反推未知項'),
            ('balance_sheet_equation', ('total_liabilities', 'net_worth'),
             '資產與權益／非控制權益完整組成未核實；Net Worth不能自動代理所有權益')):
            ids = [f'{m}:{p.role}' if f'{m}:{p.role}' in report.facts else f'input:{m}:{p.role}' for m in metrics]
            missing = [fid for fid in ids if fid not in report.facts or report.facts[fid].status not in AVAILABLE]
            checks.append({'kind': kind, 'period_role': p.role, 'period': p.label, 'status': 'not_calculable',
                           'reason': reason, 'required_input_ids': ids, 'unavailable_input_ids': missing,
                           'calculated_value': None, 'reported_value': None, 'difference': None})
    return checks


def acceptance_result(report, checks=(), limitations=()):
    checked = validate_arithmetic(report)
    bound = {fid for table in report.tables for row in table.cells for fid in row}
    unavailable = [{'fact_id': f.id, 'metric': f.metric, 'period_role': f.period_role, 'start': f.start, 'end': f.end,
                    'status': f.status.value, 'reason': f.reason, 'evidence_ids': f.evidence_ids}
                   for f in report.facts.values() if f.id in bound and f.status not in AVAILABLE]
    absent_narratives = [{'table': t.spec.key, 'topic': n.topic, 'reason': n.reason}
                         for t in report.tables for n in t.narratives if n.status != 'supported']
    blockers = list(limitations)
    if unavailable: blockers.append('Required report cells are unavailable or definitions unresolved')
    if absent_narratives: blockers.append('Required analytical coverage remains incomplete')
    if 'DEC-08' not in report.decisions: blockers.append('DEC-08 missing-data/delivery policy remains unapproved')
    if 'DEC-09' not in report.decisions: blockers.append('DEC-09 presentation policy remains unapproved')
    # A bare PASS supplied by a caller is not proof of complete reconciliation.
    verified_coverage = set()
    for check in checks:
        eids = check.get('evidence_ids', ())
        cited = [report.evidence[eid] for eid in eids if eid in report.evidence]
        role = check.get('period_role')
        if (check['status'] in ('matched', 'within_precision') and role in {p.role for p in report.periods}
                and len(cited) == len(eids) and any(e.kind == 'fact' for e in cited)
                and any(e.kind in ('review', 'definition') for e in cited)
                and all(role in e.period_roles for e in cited)):
            verified_coverage.add((check['kind'], role))
    expected_coverage = {(kind, p.role) for kind in ('balance_sheet_equation', 'cash_bridge') for p in report.periods}
    if verified_coverage != expected_coverage or any(c['status'] not in ('matched', 'within_precision') for c in checks):
        blockers.append('Reconciliation is incomplete or contains unexplained differences')
    return {'technical_validation_passed': True, 'calculation_fact_ids_verified': checked,
            'final_report_accepted': False, 'substantive_data_ready': not blockers,
            'rendered_validation_passed': False, 'source_limitations': list(limitations), 'acceptance_blockers': blockers,
            'status_counts': dict(Counter(report.facts[fid].status.value for fid in sorted(bound))),
            'missing_or_pending': unavailable,
            'missing_inputs': [{'fact_id': f.id, 'metric': f.metric, 'period_role': f.period_role, 'status': f.status.value, 'reason': f.reason, 'evidence_ids': f.evidence_ids}
                               for f in report.facts.values() if f.id.startswith('input:') and f.status not in AVAILABLE], 'incomplete_narratives': absent_narratives,
            'reconciliations': list(checks)}


def complete_report(report, inputs, candidates, *, checks=(), limitations=(), identity_reviews=()):
    report = adopt_inputs(report, inputs, candidates)
    report = calculate_report(report, identity_reviews)
    report = build_narratives(report)
    return report, acceptance_result(report, checks or automatic_reconciliation_checks(report), limitations)


def report_from_source_bundle(bundle, *, checks=(), limitations=()):
    report, _, _ = parse_request(bundle['request'])
    return complete_report(report, bundle['inputs'], bundle['evidence'], checks=checks, limitations=limitations)


def write_findings(report, acceptance, directory, source_bundle=None):
    """Separate audit artifacts; never add a Data Quality Appendix to the report."""
    directory = Path(directory)
    source_bundle = source_bundle or {}
    inputs, candidates = source_bundle.get('inputs', {}), source_bundle.get('evidence', {})
    periods = {p.role: p for p in report.periods}
    rows = []
    for entry in acceptance['missing_or_pending'] + acceptance['missing_inputs']:
        f = report.facts[entry['fact_id']]
        spec = METRICS[f.metric]
        common = f.unit == 'percent' and spec.unit == 'money'
        required = (f.metric, 'revenue') if common else spec.inputs
        dependencies = []
        for metric in required:
            fid = f'{metric}:{f.period_role}'
            if fid not in report.facts: fid = f'input:{metric}:{f.period_role}'
            fact = report.facts.get(fid)
            dependencies.append(fid + ': ' + (fact.status.value if fact else 'missing'))
        item = inputs.get(f.id, {})
        candidate_ids = item.get('candidate_ids', ()) or f.evidence_ids
        selected = [candidates[eid] for eid in candidate_ids if eid in candidates]
        rows.append({'fact_id': f.id, '科目': spec.label, '期間角色': f.period_role,
            '期間': periods[f.period_role].label, '狀態': f.status.value, '原因': f.reason,
            '必要輸入': '; '.join(dependencies), '待確認定義': '; '.join(d for d in spec.pending if d not in report.decisions),
            '原始候選值_未採入正式報表': '; '.join(str(c.get('value')) + ' [' + str(c.get('unit')) + ', scale=' + str(c.get('scale')) + ']' for c in selected),
            '來源位置': '; '.join(c['locator'] for c in selected)})
    with (directory / 'missing_data.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        columns = list(rows[0]) if rows else ['fact_id', '科目', '期間', '狀態', '原因']
        writer = csv.DictWriter(handle, fieldnames=columns); writer.writeheader(); writer.writerows(rows)
    check_rows = []
    for c in acceptance['reconciliations']:
        check_rows.append({'檢查': c['kind'], '期間': c.get('period', c.get('period_role', '')),
            '狀態': c['status'], '單位': c.get('unit', ''), '幣別': c.get('currency'), 'scale': c.get('scale'),
            '計算值': c.get('calculated_value'), '原檔列示值': c.get('reported_value'), '差額_計算減原檔': c.get('difference'),
            '原因與限制': c.get('reason', ''), '來源位置': '; '.join(c.get('source_locators', ()))})
    with (directory / 'reconciliations.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        columns = list(check_rows[0]) if check_rows else ['檢查', '期間', '狀態', '原因與限制']
        writer = csv.DictWriter(handle, fieldnames=columns); writer.writeheader(); writer.writerows(check_rows)
    lines = ['# 缺少資料、待確認定義與勾稽結果', '',
        '完整項目見同目錄 missing_data.csv；逐項來源、單位與差額見 reconciliations.csv。', '',
        '## 仍未完成的驗收條件', '']
    lines += ['- ' + reason for reason in acceptance['acceptance_blockers']]
    lines += ['', '## 無法勾稽的數值差額', '', '| 檢查 | 期間 | 差額（計算－原檔） | 單位 |', '| --- | --- | ---: | --- |']
    failed = [c for c in acceptance['reconciliations'] if c['status'] == 'unexplained_difference']
    for c in failed:
        lines.append(f"| {c['kind']} | {c.get('period', '')} | {c['difference']:,} | {c.get('currency', '')}, scale={c.get('scale', '')} |")
    if not failed: lines.append('| 尚無可列示的數值差額 | 不代表勾稽已完成 | — | 缺必要資料的項目另列not_calculable |')
    lines += ['', '差額只是已列來源數字的算術比較，原因尚未確定；未知FX、現金定義與其他調節未補0或反推。', '']
    (directory / 'review_findings.md').write_text('\n'.join(lines), encoding='utf-8')


def write_report_artifacts(report, acceptance, directory, *, source_bundle=None):
    try:
        from .credit_memo_writer import render_loan_review
    except ImportError:
        from credit_memo_writer import render_loan_review
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    # Never trust a caller-supplied PASS flag: recompute from the actual report.
    acceptance = acceptance_result(report, acceptance.get('reconciliations', ()), acceptance.get('source_limitations', ()))
    acceptance['final_report_accepted'] = acceptance['substantive_data_ready']
    markdown = render_loan_review(report, acceptance)
    validate_rendered_report(report, markdown)
    acceptance['rendered_validation_passed'] = True
    (directory / 'report.md').write_text(markdown, encoding='utf-8')
    (directory / 'report.json').write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    (directory / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    write_findings(report, acceptance, directory, source_bundle)
    if source_bundle is not None:
        (directory / 'source_inputs.json').write_text(json.dumps(source_bundle, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    return {'report_path': str((directory / 'report.md').resolve()),
            'report_data_path': str((directory / 'report.json').resolve()),
            'acceptance_path': str((directory / 'acceptance.json').resolve()),
            'findings_path': str((directory / 'review_findings.md').resolve()),
            'final_report_accepted': acceptance['final_report_accepted'],
            'technical_validation_passed': acceptance['technical_validation_passed'],
            'rendered_validation_passed': True}
