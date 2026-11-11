"""Assemble warehouse-computed commentary values and prose without arithmetic.

The adapter copies SQL numeric strings, directions, ordering and coverage. Only
the separate shadow comparator recomputes expectations during migration.
"""
from dataclasses import replace
from decimal import Decimal
import json

from .loan_review_contract import METRICS, Narrative, validate_report
from .ratio_commentary_analysis import VERSION, TOTAL_CONCEPTS, RATIOS


def _fact(report,metric,role):
    return report.facts.get(metric+':'+role) or report.facts.get('input:'+metric+':'+role)


def _check_endpoints(report,row,metric,roles):
    for key,role in zip(('before','after'),roles):
        fact = _fact(report,metric,role)
        value = fact.value if fact is not None else None
        actual = row[key]
        if (value is None)!=(actual is None) or value is not None and (not isinstance(actual,str) or Decimal(actual)!=value):
            raise ValueError('Warehouse commentary endpoint differs from canonical Fact')
    expected_status = 'available' if row['before'] is not None and row['after'] is not None else 'missing'
    if row['status']!=expected_status:
        raise ValueError('Warehouse commentary availability mismatch')


def assemble_analysis(report, rows, *, bindings, documents=()):
    roles = ('fy_t_minus_1','fy_t') if report.mode.value == 'annual' else ('latest_fy_end','current_interim')
    periods = {p.role:p for p in report.periods}
    records = {}
    for row in rows:
        if any(row.get(k) != bindings[k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version')):
            raise ValueError('Warehouse commentary binding mismatch')
        if row.get('publication_eligible') is not False:
            raise ValueError('Warehouse commentary cannot grant publication')
        key = row['record_kind'],row['record_id']
        if key in records:
            raise ValueError('Duplicate warehouse commentary record')
        if key[0] not in ('ratio','component','total_check','component_reconciliation','coverage','limitation','comparison'):
            raise ValueError('Unknown warehouse commentary record')
        records[key] = json.loads(row['payload'])
    result = dict(version=VERSION, mode=report.mode.value, entity=report.entity, currency=report.currency,
        scale=str(report.scale), period_roles=list(roles), dates={r:str(periods[r].end) if periods[r].end else None for r in roles},
        ratios={},components=[],source_total_checks=[],limitations=[],document_ids=[d['id'] for d in documents],
        component_coverage={g:'partial_not_reconciled' for g in ('current_assets','current_liabilities','total_liabilities','net_worth')},
        component_reconciliations=[])
    for metric in RATIOS:
        item = dict(records.pop(('ratio',metric)))
        item.pop('metric', None)
        _check_endpoints(report,item,metric,roles)
        expected_ids = [f.id for role in roles if (f:=_fact(report,metric,role)) is not None and f.value is not None]
        if item['fact_ids']!=expected_ids:
            raise ValueError('Warehouse ratio lineage mismatch')
        for key,component in zip(('numerator','denominator'),RATIOS[metric]):
            if item[key]['metric']!=component:
                raise ValueError('Warehouse ratio component mismatch')
            _check_endpoints(report,item[key],component,roles)
        result['ratios'][metric] = item
    for metric in TOTAL_CONCEPTS.values():
        for role in roles:
            result['source_total_checks'].append(records.pop(('total_check',metric+':'+role)))
    for group in ('current_assets','current_liabilities'):
        result['component_coverage'][group] = records.pop(('coverage',group))['status']
        for role in roles:
            result['component_reconciliations'].append(records.pop(('component_reconciliation',group+':'+role)))
    components = sorted((v for (kind,_),v in records.items() if kind=='component'),key=lambda v:v['position'])
    for item in components:
        item = dict(item)
        item.pop('position')
        item['sources'] = {roles[0]:json.loads(item.pop('before_sources_json')),roles[1]:json.loads(item.pop('after_sources_json'))}
        result['components'].append(item)
    result['limitations'] = [v['text'] for (kind,_),v in sorted(records.items()) if kind=='limitation']
    comparisons = {key:v for (kind,key),v in records.items() if kind=='comparison'}
    metrics = {f.metric for f in report.facts.values() if f.unit!='text' and ':pct:' not in f.id}
    if set(comparisons)!={kind+':'+metric for kind in ('income','balance') for metric in metrics}:
        raise ValueError('Incomplete warehouse comparison coverage')
    for key,row in comparisons.items():
        kind,metric = key.split(':')
        pair = roles if kind=='balance' or report.mode.value=='annual' else ('prior_interim','current_interim')
        if (row['kind'],row['metric'],row['before_role'],row['after_role'])!=(kind,metric,*pair):
            raise ValueError('Warehouse comparison period/metric mismatch')
        _check_endpoints(report,row,metric,pair)
        if row['direction'] not in ('not_comparable','unchanged','increased','decreased') or (row['direction']=='not_comparable')!=(row['status']=='missing'):
            raise ValueError('Warehouse comparison direction/status mismatch')
        for position,role in zip(('before','after'),pair):
            fact = _fact(report,metric,role)
            if row[position+'_fact_id']!=(fact.id if fact else None) or row[position+'_status']!=(fact.status.value if fact else None):
                raise ValueError('Warehouse comparison Fact lineage mismatch')
    return result, comparisons


def build_narratives(report, comparisons):
    """Describe SQL endpoints/directions/deltas; presentation scaling only."""
    periods = {p.role:p for p in report.periods}
    directions = {'unchanged':'持平','increased':'上升','decreased':'下降'}
    def fmt(value,unit):
        value = Decimal(value)
        if unit in ('percent','percentage_points'):
            return f'{value * 100:,.2f}%'
        return f'{value:,.2f}' + ('x' if unit=='multiple' else '')
    tables = []
    for table in report.tables:
        kind = 'income' if table.spec.key=='income' else 'balance'
        narratives = []
        for topic in table.spec.topics:
            metrics = ('current_ratio','quick_ratio') if topic=='liquidity' else (topic,)
            texts,ids,used_roles = [],[],[]
            for metric in metrics:
                row = comparisons.get(kind+':'+metric)
                if row is None or row['status']!='available':
                    continue
                before,after = row['before_role'],row['after_role']
                pair = row['before_fact_id'],row['after_fact_id']
                if any(fid not in report.facts for fid in pair):
                    raise ValueError('Warehouse comparison references an unknown Fact')
                if (str(report.facts[pair[0]].value),str(report.facts[pair[1]].value)) != (row['before'],row['after']):
                    # Different SQL string representations may still describe one decimal.
                    if any(Decimal(str(report.facts[fid].value))!=Decimal(value) for fid,value in zip(pair,(row['before'],row['after']))):
                        raise ValueError('Warehouse comparison endpoint differs from canonical Fact')
                text = f'{METRICS[metric].label} 由 {periods[before].label} 的 {fmt(row["before"],row["unit"])} '
                text += f'{directions[row["direction"]]}至 {periods[after].label} 的 {fmt(row["after"],row["unit"])}。'
                if row['unit']=='percent' and metric.endswith('margin'):
                    text += f'變動 {Decimal(row["change"]) * 100:,.2f} 個百分點。'
                if metric=='revenue':
                    growth = report.facts.get('revenue_growth:'+after)
                    if growth is not None and growth.value is not None:
                        text += f'依CF-09計算成長率為 {Decimal(growth.value) * 100:,.2f}%。'
                        ids.append(growth.id)
                texts.append(text);ids.extend(pair);used_roles.extend((before,after))
            narratives.append(Narrative(topic,'supported' if texts else 'missing',
                text=' '.join(texts) + ('所選來源輸入未附可核實的原因證據，本段僅作數值比較。' if texts else ''),
                claim_type='comparison',fact_ids=tuple(dict.fromkeys(ids)),period_roles=tuple(dict.fromkeys(used_roles)),
                reason='缺少可比較的 warehouse 數值；不以 Python 補算。' if not texts else '原因分析仍需來源證據。'))
        tables.append(replace(table,narratives=tuple(narratives)))
    report = replace(report,tables=tuple(tables))
    validate_report(report,expected_mode=report.mode)
    return report
