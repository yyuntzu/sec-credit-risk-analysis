"""Evidence-bound commentary for the formal report; offline inputs never call APIs.

Model output is a proposal. Exact quotes and canonical fact bindings are checked
here; substantive acceptance additionally requires a recorded source review.
"""
from dataclasses import replace
from datetime import date
from decimal import Decimal
import hashlib
from html.parser import HTMLParser
import json
import re

try:
    from .loan_review_contract import Evidence, Narrative, AVAILABLE, validate_report
except ImportError:
    from loan_review_contract import Evidence, Narrative, AVAILABLE, validate_report


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def extract_mda(html, form):
    """Select an actual Item 7/2 body bounded by the following SEC item.

    Never substitute the table of contents or an arbitrary document half.
    Offsets in evidence refer to this normalized, archived section text.
    """
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True); self.parts = []; self.hidden = 0
        def handle_starttag(self, tag, attrs):
            if tag in ('script', 'style', 'head'): self.hidden += 1
        def handle_endtag(self, tag):
            if tag in ('script', 'style', 'head'): self.hidden = max(0, self.hidden - 1)
        def handle_data(self, data):
            if not self.hidden: self.parts.append(data)
    parser = Text(); parser.feed(html)
    text = ' '.join(' '.join(parser.parts).split())
    item = '7' if form.startswith('10-K') else '2'
    start = re.compile(r'\bitem\s+' + item + r'\s*[.:\-–]?\s*management[’\x27]?s\s+discussion', re.I)
    stop = re.compile(r'\bitem\s+(?:7a|8)\s*[.:\-–]?\s*(?:quantitative|financial)' if item == '7'
                      else r'\bitem\s+(?:3|4)\s*[.:\-–]?\s*(?:quantitative|controls)', re.I)
    sections = []
    starts=list(start.finditer(text))
    for index, match in enumerate(starts):
        end = stop.search(text, match.end())
        # A TOC entry without a recognizable TOC terminator must not capture
        # the intervening business/risk sections up to the real MD&A body.
        if end and index+1<len(starts) and starts[index+1].start()<end.start():
            continue
        if end and end.start() - match.start() >= 500:
            sections.append(text[match.start():end.start()])
    if not sections: raise ValueError('A bounded MD&A body was not found; provide a reviewed section snapshot')
    return max(sections, key=len)[:80000]


def collect_sec_documents(client, request):
    """Fetch exact requested report dates, not merely the most recent filing."""
    submissions = client.get_company_submissions(request['entity'])
    if str(submissions.get('cik', '')).zfill(10) != request['cik']:
        raise ValueError('MD&A submissions CIK differs from review request')
    periods = request['periods']; as_of = date.fromisoformat(request['as_of'])
    candidates = []
    def add(data):
        keys = ('accessionNumber','filingDate','reportDate','form','primaryDocument')
        for values in zip(*(data.get(k, []) for k in keys)):
            row = dict(zip(keys, values))
            if row['form'] in ('10-K','10-Q') and date.fromisoformat(row['filingDate']) <= as_of:
                candidates.append(row)
    add(submissions.get('filings', {}).get('recent', {}))
    def matching(p):
        expected = '10-Q' if p['quarter'] is not None else '10-K'
        return [r for r in candidates if r['reportDate'] == p['end'] and r['form'] == expected]
    for archive in submissions.get('filings', {}).get('files', []):
        if all(matching(p) for p in periods): break
        name = archive.get('name', '')
        if not re.fullmatch(r'CIK\d{10}-submissions-\d+\.json', name): continue
        add(client._get('https://data.sec.gov/submissions/' + name))
    documents = []
    for period in periods:
        rows = matching(period)
        if not rows: continue
        row = max(rows, key=lambda r: (r['filingDate'], r['accessionNumber']))
        accn, primary = row['accessionNumber'], row['primaryDocument']
        if not re.fullmatch(r'\d{10}-\d{2}-\d{6}', accn) or not re.fullmatch(r'[A-Za-z0-9_.-]+', primary):
            raise ValueError('Invalid SEC primary document identity')
        url = f"https://www.sec.gov/Archives/edgar/data/{int(request['cik'])}/{accn.replace('-', '')}/{primary}"
        import time
        time.sleep(client.rate_limit)
        response = client.session.get(url, headers={'Host':'www.sec.gov'}, timeout=60)
        response.raise_for_status()
        section = extract_mda(response.text, row['form'])
        documents.append(dict(id='mda:' + accn, entity=request['entity'], cik=request['cik'], scope=request['scope'],
            source_id=accn, version=hashlib.sha256(response.content).hexdigest(), document_date=row['filingDate'],
            source_url=url, section='MD&A', periods=[{k:period[k] for k in ('role','start','end')}], text=section))
    return documents


def validate_documents(report, request, documents):
    result = {}
    if not isinstance(documents,list): raise ValueError('MD&A documents must be a list')
    for document in documents:
        required = {'id','entity','cik','scope','source_id','version','document_date','source_url','section','periods','text'}
        if not isinstance(document, dict) or set(document) != required:
            raise ValueError('MD&A document fields do not match schema')
        if (document['entity'],document['cik'],document['scope']) != (report.entity,request['cik'],report.scope):
            raise ValueError('MD&A borrower/CIK/scope mismatch')
        if date.fromisoformat(document['document_date']) > date.fromisoformat(request['as_of']):
            raise ValueError('MD&A document is later than as_of')
        if document['section'] != 'MD&A' or any(not isinstance(document[k], str) or not document[k].strip()
                for k in ('id','source_id','version','source_url','text')):
            raise ValueError('Explicit MD&A text and source identity required')
        if not document['source_url'].startswith(('https://','fixture://')):
            raise ValueError('MD&A source URL must identify a document')
        if document['source_url'].startswith('fixture://') and report.entity!='SYNTHETIC-ONLY':
            raise ValueError('Synthetic MD&A evidence cannot support a real borrower')
        if len(document['text']) > 80000:
            raise ValueError('MD&A section exceeds the bounded document budget')
        if document['id'] in result: raise ValueError('Duplicate MD&A document ID')
        if not isinstance(document['periods'], list) or not document['periods']:
            raise ValueError('Explicit MD&A fiscal period coverage required')
        for covered in document['periods']:
            if not isinstance(covered,dict): raise ValueError('MD&A period coverage must be an object')
            period = next((p for p in report.periods if p.role == covered.get('role')), None)
            if period is None or covered != {'role':period.role,'start':period.start.isoformat() if period.start else None,
                                             'end':period.end.isoformat() if period.end else None}:
                raise ValueError('MD&A fiscal period coverage differs from canonical request')
            if period.end and period.end > date.fromisoformat(document['document_date']):
                raise ValueError('MD&A document predates its covered financial period')
        result[document['id']] = document
    if sum(len(d['text']) for d in result.values()) > 320000:
        raise ValueError('MD&A document set exceeds the report context budget')
    return result


def review_binding(table, narrative):
    return dict(table=table, topic=narrative.topic, text=narrative.text,
                claim_type=narrative.claim_type, fact_ids=list(narrative.fact_ids),
                period_roles=list(narrative.period_roles), evidence_ids=[e for e in narrative.evidence_ids if not e.startswith('commentary-review:')])


def is_reviewed(report, table, narrative):
    if narrative.status != 'supported' or narrative.claim_type not in ('cause','management'):
        return False
    if not narrative.evidence_ids: return False
    for eid in narrative.evidence_ids:
        evidence = report.evidence[eid]
        if evidence.kind != 'review': continue
        try:
            review = json.loads(evidence.content)
            if (review['binding'] == review_binding(table, narrative)
                    and review['method'] == 'checked_against_source'
                    and isinstance(review['verified_by'],str) and review['verified_by'].strip()
                    and date.fromisoformat(review['verified_at']) >= evidence.document_date):
                return True
        except (ValueError, KeyError, TypeError): pass
    return False


def commentary_gaps(report):
    return [dict(table=t.spec.key,topic=n.topic,reason=n.reason or 'Source-based cause analysis has not been independently reviewed')
            for t in report.tables for n in t.narratives if not is_reviewed(report,t.spec.key,n)]


def narrative_display(report, table, narrative):
    """Shared visible text and sources for every delivery format."""
    reviewed=is_reviewed(report,table,narrative)
    label=('原因分析（已覆核）' if reviewed else '原因分析（待覆核）') if narrative.claim_type in ('cause','management') else '數值比較／分析限制'
    text=label+'：'+(narrative.text if narrative.status=='supported' else narrative.reason)
    if narrative.status=='supported' and narrative.reason:text+='；限制：'+narrative.reason
    if narrative.attribution:text+='（歸屬：'+narrative.attribution+'）'
    sources=[dict(evidence_id=eid,source_id=report.evidence[eid].source_id,
                  document_date=report.evidence[eid].document_date.isoformat(),
                  locator=report.evidence[eid].locator,quote=report.evidence[eid].content)
             for eid in narrative.evidence_ids if report.evidence[eid].kind=='passage']
    return dict(text=text,sources=sources,reviewed=reviewed)


def commentary_payload(report):
    return [dict(id=f'{t.spec.key}:{kind}:{i}',kind=kind,table=t.spec.key,topic=n.topic,status=n.status,
                 claim_type=n.claim_type,explanation=n.text,reason=n.reason,attribution=n.attribution,
                 fact_ids=list(n.fact_ids),evidence_ids=list(n.evidence_ids),period_roles=list(n.period_roles),
                 display=narrative_display(report,t.spec.key,n))
            for t in report.tables for kind,items in (('narrative',t.narratives),('note',t.notes))
            for i,n in enumerate(items)]


def apply_commentary(report, request, documents, claims):
    """Adopt validated source-cited proposals; keep numeric comparisons on failure."""
    docs = validate_documents(report, request, documents)
    evidence = dict(report.evidence); tables = []; seen = set(); supplied = {}
    if not isinstance(claims,list): raise ValueError('Commentary claims must be a list')
    for claim in claims:
        if not isinstance(claim,dict): raise ValueError('Commentary claim must be an object')
        key = (claim.get('table'),claim.get('topic'))
        if key in seen: raise ValueError('Duplicate commentary topic')
        seen.add(key); supplied[key] = claim
    allowed = {(t.spec.key,n.topic) for t in report.tables for n in t.narratives}
    if set(supplied) - allowed: raise ValueError('Unknown commentary table/topic')
    for table in report.tables:
        narratives = []
        for original in table.narratives:
            claim = supplied.get((table.spec.key,original.topic))
            if claim is None or claim.get('status') == 'missing':
                reason = claim.get('reason','MD&A does not explain this topic') if claim else 'No source-based cause commentary supplied'
                if not isinstance(reason,str) or not reason.strip(): raise ValueError('Missing commentary requires an explicit reason')
                narratives.append(replace(original, reason=reason)); continue
            if original.status != 'supported':
                raise ValueError('Commentary cannot substitute for missing canonical comparison facts')
            if claim.get('status') != 'supported' or claim.get('claim_type') not in ('cause','management'):
                raise ValueError('Explicit causal/management commentary status required')
            if claim.get('fact_ids') != list(original.fact_ids) or claim.get('period_roles') != list(original.period_roles):
                raise ValueError('Commentary facts/periods differ from canonical comparison')
            text = claim.get('explanation')
            if not isinstance(text,str) or not text.strip() or len(text)>1500:
                raise ValueError('A concise commentary explanation is required (maximum 1500 characters)')
            citations = claim.get('citations')
            if not isinstance(citations,list) or not citations: raise ValueError('Commentary requires exact source quotes')
            eids=[]; covered=set(); quotations=[]
            for citation in citations:
                if not isinstance(citation,dict) or set(citation)!={'document_id','quote'}:
                    raise ValueError('Explicit document ID and source quote required')
                document=docs[citation['document_id']]; quote=citation['quote']
                if not isinstance(quote,str) or not 12<=len(quote.strip())<=2000 or quote not in document['text']:
                    raise ValueError('Commentary quote is not an exact source passage')
                roles=tuple(p['role'] for p in document['periods'])
                if not set(roles) <= set(original.period_roles): raise ValueError('Commentary citation covers unrelated periods')
                covered.update(roles);quotations.append(quote)
                offset=document['text'].index(quote)
                eid='passage:'+digest([document['id'],document['version'],offset,quote])
                evidence[eid]=Evidence(eid,report.entity,report.scope,document['source_id'],document['version'],
                    date.fromisoformat(document['document_date']),document['source_url']+'#MD&A:char='+str(offset),
                    'passage',roles,quote)
                eids.append(eid)
            if set(original.period_roles) - covered: raise ValueError('Commentary source quotes do not cover both comparison periods')
            # New numerical assertions must occur in canonical facts or cited text.
            numbers=lambda value:{Decimal(v) for v in re.findall(r'[+-]?\d+(?:\.\d+)?',value.replace(',',''))}
            allowed_numbers=numbers(' '.join(quotations))
            for fid in original.fact_ids:
                fact=report.facts[fid]
                if fact.unit!='text':
                    value=fact.value*100 if fact.unit in ('percent','percentage_points') else fact.value
                    allowed_numbers.update((value,abs(value)))
            for role in original.period_roles:
                period=next(p for p in report.periods if p.role==role)
                allowed_numbers.update(numbers(period.label))
            if not numbers(text) <= allowed_numbers: raise ValueError('Commentary introduces unsupported numerical claims')
            attribution=claim.get('attribution','')
            if not isinstance(attribution,str): raise ValueError('Commentary attribution must be text')
            if claim['claim_type']=='management' and not attribution: raise ValueError('Management commentary requires attribution')
            n=Narrative(original.topic,'supported',text=text,claim_type=claim['claim_type'],fact_ids=original.fact_ids,
                period_roles=original.period_roles,evidence_ids=tuple(dict.fromkeys(eids)),
                reason='Source-cited commentary proposal; independent review pending',attribution=attribution)
            review=claim.get('review')
            if review is not None:
                if (not isinstance(review,dict) or set(review)!={'verified_by','verified_at','method'}
                        or review['method']!='checked_against_source' or not isinstance(review['verified_by'],str)
                        or not review['verified_by'].strip()): raise ValueError('Invalid commentary source-review record')
                reviewed=date.fromisoformat(review['verified_at'])
                if reviewed < max(evidence[e].document_date for e in eids): raise ValueError('Commentary review predates cited source')
                eid='commentary-review:'+digest([review_binding(table.spec.key,n),review])
                evidence[eid]=Evidence(eid,report.entity,report.scope,'commentary-review',digest(review),reviewed,
                    'review://'+review['verified_by'],'review',original.period_roles,
                    json.dumps(dict(binding=review_binding(table.spec.key,n),**review),ensure_ascii=False))
                n=replace(n,evidence_ids=n.evidence_ids+(eid,),reason='')
            narratives.append(n)
        tables.append(replace(table,narratives=tuple(narratives)))
    result=replace(report,tables=tuple(tables),evidence=evidence)
    validate_report(result,expected_mode=report.mode)
    return result
