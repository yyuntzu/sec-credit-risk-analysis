"""Independent Python baseline/audit for dbt commentary during migration only."""
from dataclasses import replace
from decimal import Decimal, localcontext

from .loan_review_sources import balance_sheet_observations
from .filing_commentary_sources import document_observations
from .ratio_commentary_analysis import build_ratio_analysis
from .warehouse_commentary import assemble_analysis


NUMERIC_FIELDS = {'before','after','change','growth','difference','selected_sum','canonical_total','unexplained_residual'}


def _canonical_pack(value):
    if isinstance(value,dict):
        return {k:_canonical_pack(v) for k,v in value.items()}
    if isinstance(value,list):
        items = [_canonical_pack(v) for v in value]
        if all(isinstance(v,dict) and 'id' in v for v in items):
            return sorted(items,key=lambda v:v['id'])
        if all(isinstance(v,str) for v in items):
            return sorted(items)
        return items
    return value


def compare_commentary(bundle,baseline,rows,fact_comparison,*,bindings,documents=(),canonical_precision=False):
    from .review_workflow import restore_report
    report = restore_report(baseline)
    expected = build_ratio_analysis(report,balance_sheet_observations(bundle)+document_observations(documents),documents)
    if canonical_precision:
        from .precision_policy import canonical_commentary
        expected=canonical_commentary(expected)
    classes = {r['fact_id']:r['classification'] for r in fact_comparison['details']}
    sql_facts = {}
    for item in fact_comparison['details']:
        if item['dbt'] is not None and item['fact_id'] in report.facts:
            fact = report.facts[item['fact_id']]
            raw = item['dbt']['value']
            sql_facts[fact.id] = replace(fact,value=raw if fact.unit=='text' or raw is None else Decimal(str(raw)))
    actual_report = replace(report,facts=sql_facts)
    actual,comparisons = assemble_analysis(actual_report,rows,bindings=bindings,documents=documents)
    details = []
    def difference(path,left,right,classification='mismatch'):
        details.append(dict(path='.'.join(path),python=left,dbt=right,classification=classification))
    def precision_affected(path):
        if len(path)<3 or path[0]!='ratios':
            return False
        entry = expected['ratios'][path[1]]
        metric = entry[path[2]]['metric'] if path[2] in ('numerator','denominator') else path[1]
        return any(classes.get(fid)=='numeric_difference_unapproved' for fid,f in report.facts.items()
                   if f.metric==metric and f.period_role in expected['period_roles'] and ':pct:' not in fid)
    def walk(left,right,path=()):
        if isinstance(left,dict) and isinstance(right,dict):
            for key in sorted(set(left)|set(right)):
                if key not in left or key not in right:
                    difference((*path,key),left.get(key),right.get(key))
                else: walk(left[key],right[key],(*path,key))
        elif isinstance(left,list) and isinstance(right,list):
            if len(left)!=len(right): difference(path,left,right)
            else:
                for i,(a,b) in enumerate(zip(left,right)): walk(a,b,(*path,str(i)))
        elif left!=right:
            numeric = path and path[-1] in NUMERIC_FIELDS and left is not None and right is not None
            if numeric and Decimal(str(left))==Decimal(str(right)): return
            kind = 'numeric_difference_unapproved' if not canonical_precision and numeric and (path[-1]=='growth' or precision_affected(path)) else 'mismatch'
            difference(path,left,right,kind)
    walk(_canonical_pack(expected),_canonical_pack(actual))
    # Exact subtraction and directions must agree with the actual SQL operands.
    # A bogus delta may not be waived merely because its inputs were divisions.
    with localcontext() as ctx:
        ctx.prec = 256
        for key,row in comparisons.items():
            before,after = row['before'],row['after']
            change = str(Decimal(after)-Decimal(before)) if before is not None and after is not None else None
            direction = ('not_comparable' if before is None or after is None else 'unchanged' if Decimal(after)==Decimal(before)
                         else 'increased' if Decimal(after)>Decimal(before) else 'decreased')
            if (change is None)!=(row['change'] is None) or change is not None and Decimal(row['change'])!=Decimal(change):
                difference(('comparisons',key,'change'),change,row['change'])
            if direction!=row['direction']:
                difference(('comparisons',key,'direction'),direction,row['direction'])
        entries = list(actual['components']) + [x for r in actual['ratios'].values() for x in (r,r['numerator'],r['denominator'])]
        for i,row in enumerate(entries):
            before,after = row['before'],row['after']
            value = Decimal(after)-Decimal(before) if before is not None and after is not None else None
            if (value is None)!=(row['change'] is None) or value is not None and Decimal(row['change'])!=value:
                difference(('exact_change',str(i)),str(value) if value is not None else None,row['change'])
    return dict(mismatches=sum(r['classification']=='mismatch' for r in details),
        numeric_differences=sum(r['classification']=='numeric_difference_unapproved' for r in details),
        precision_approved=False,publication_eligible=False,details=details,python=expected,dbt=actual)
