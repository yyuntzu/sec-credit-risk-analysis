"""Value-free, source-bound identity review contract for shadow calculations."""
from dataclasses import asdict
from datetime import date
import json

from .loan_review_contract import Evidence
from .loan_review_sources import digest, canonical

RULES = {
    'DER-01': ('gross_profit', ('revenue', 'cost_of_revenue')),
    'DER-02': ('cost_of_revenue', ('revenue', 'gross_profit')),
    'DER-03': ('operating_expense', ('gross_profit', 'operating_income')),
    'DER-04': ('operating_income', ('gross_profit', 'operating_expense')),
    'DER-05': ('pretax_profit', ('net_income', 'income_tax')),
    'DER-06': ('net_income', ('pretax_profit', 'income_tax')),
}


def parse_identity_reviews(bundle, plans):
    """Validate claims and references only; no source adoption or arithmetic."""
    envelope = bundle.get('identity_reviews')
    if envelope is None:
        return {}, {}
    if not isinstance(envelope, dict) or set(envelope) != {'schema_version','source_hash','reviews'} \
            or envelope['schema_version'] != 1 or not isinstance(envelope['reviews'], list):
        raise ValueError('Invalid identity review envelope')
    original = {key:value for key,value in bundle.items() if key!='identity_reviews'}
    if envelope['source_hash'] != digest(original):
        raise ValueError('Identity review source binding mismatch')
    index = {p['fact_id']:p for p in plans}
    reviews, evidence = {}, {}
    for review in envelope['reviews']:
        if not isinstance(review,dict) or set(review) != {'fact_id','formula_id','formula_version','input_ids','evidence'}:
            raise ValueError('Invalid identity review fields')
        fid, formula = review['fact_id'], review['formula_id']
        if fid in reviews or fid not in index or formula not in RULES:
            raise ValueError('Duplicate or unsupported identity target/formula')
        target = index[fid]
        ids = review['input_ids']
        metric, metrics = RULES[formula]
        if target['metric'] != metric or not isinstance(ids,list) or len(ids)!=2 \
                or any(i not in index or i==fid for i in ids) or tuple(index[i]['metric'] for i in ids)!=metrics:
            raise ValueError('Identity components/order mismatch')
        if not isinstance(review['formula_version'],str) or not review['formula_version'].strip():
            raise ValueError('Identity formula version required')
        for iid in ids:
            if any(index[iid][k] != target[k] for k in ('period_role','start','end','unit','currency','period_kind')):
                raise ValueError('Identity period/unit mismatch')
        row = dict(review['evidence'])
        row['document_date'] = date.fromisoformat(str(row['document_date']))
        row['period_roles'] = tuple(row['period_roles'])
        item = Evidence(**row)
        reserved = {e['id'] for e in bundle['request'].get('evidence',[])}
        if item.id in evidence or item.id in bundle['evidence'] or item.id in reserved \
                or item.id.startswith(('approval:','policy-basis:')) or item.kind!='definition' \
                or item.entity!=bundle['request']['entity'] or item.scope!=bundle['request']['scope'] \
                or target['period_role'] not in item.period_roles \
                or item.document_date>date.fromisoformat(str(bundle['request']['as_of'])) \
                or not all(isinstance(v,str) and v.strip() for v in (item.id,item.source_id,item.version,item.locator)):
            raise ValueError('Invalid identity definition evidence')
        claim = dict(source_hash=envelope['source_hash'], entity=item.entity, scope=item.scope,
            fact_id=fid, formula_id=formula, formula_version=review['formula_version'], input_ids=ids,
            period_role=target['period_role'], start=target['start'], end=target['end'],
            currency=target['currency'], unit=target['unit'], complete=True)
        # Canonical serialization may vary, but every field/value must match.
        if canonical(json.loads(item.content)) != canonical(claim):
            raise ValueError('Identity definition evidence claim mismatch')
        reviews[fid] = dict(review,evidence=asdict(item))
        evidence[item.id] = item
    return reviews,evidence
