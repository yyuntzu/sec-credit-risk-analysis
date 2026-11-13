"""Evidence-bound commentary for the formal report; offline inputs never call APIs.

Model summaries are displayed with source excerpts. Commentary content and review
status do not determine financial acceptance; numeric facts remain unchanged.
"""
from dataclasses import replace
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
import re

try:
    from .loan_review_contract import Evidence, Narrative, AVAILABLE, validate_report
    from .filing_commentary_sources import SECTIONS, extract_filing_sections, validate_observations
    from .ratio_commentary_analysis import comparison_roles, ratio_fact_ids
except ImportError:
    from loan_review_contract import Evidence, Narrative, AVAILABLE, validate_report
    from filing_commentary_sources import SECTIONS, extract_filing_sections, validate_observations
    from ratio_commentary_analysis import comparison_roles, ratio_fact_ids


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
        if index+1<len(starts) and (end is None or starts[index+1].start()<end.start()):
            continue
        section_end=end.start() if end else len(text)
        if section_end-match.start()>=100:
            sections.append(text[match.start():section_end])
    if not sections: raise ValueError('A bounded MD&A body was not found; provide a reviewed section snapshot')
    return max(sections, key=len)[:80000]


def collect_sec_documents(client, request):
    """Fetch exact requested report dates, not merely the most recent filing."""
    submissions = client.get_company_submissions(request['entity'])
    if str(submissions.get('cik', '')).zfill(10) != request['cik']:
        raise ValueError('MD&A submissions CIK differs from review request')
    roles = ('fy_t_minus_1', 'fy_t') if request['mode'] == 'annual' else ('latest_fy_end', 'current_interim')
    periods = [request['periods'][-1]] + [p for p in request['periods'] if p['role'] == roles[0]]
    as_of = date.fromisoformat(request['as_of'])
    candidates = []
    def add(data):
        keys = ('accessionNumber','filingDate','reportDate','form','primaryDocument')
        for values in zip(*(data.get(k, []) for k in keys)):
            row = dict(zip(keys, values))
            if row['form'] in ('10-K','10-Q','10-K/A','10-Q/A') and date.fromisoformat(row['filingDate']) <= as_of:
                candidates.append(row)
    add(submissions.get('filings', {}).get('recent', {}))
    def matching(p):
        expected = '10-Q' if p['quarter'] is not None else '10-K'
        return [r for r in candidates if r['reportDate'] == p['end'] and r['form'] in (expected, expected + '/A')]
    for archive in submissions.get('filings', {}).get('files', []):
        if matching(periods[0]): break  # Older comparison filing is optional.
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
        try:
            response = client.session.get(url, headers={'Host':'www.sec.gov'}, timeout=60)
            response.raise_for_status()
        except Exception:
            if period is periods[0]: raise
            continue  # Prior filing failure must not discard current-period evidence.
        sections = extract_filing_sections(response.text, request['cik'], {p['end'] for p in periods})
        try:
            sections.append(dict(section='MD&A', text=extract_mda(response.text, row['form'])))
        except ValueError:
            pass  # Balance-sheet/note analysis can proceed without MD&A.
        for section in sections:
            observed_dates = {o['end'] for o in section.get('observations', [])}
            covered = [p for p in periods if p is period or p['end'] in observed_dates]
            if sum(len(d['text']) for d in documents) + len(section['text']) > 320000:
                continue
            kind = section['section']
            document = dict(id=('mda' if kind == 'MD&A' else kind.lower().replace(' ', '-')) + ':' + accn,
                entity=request['entity'], cik=request['cik'], scope=request['scope'], source_id=accn,
                version=hashlib.sha256(response.content).hexdigest(), document_date=row['filingDate'],
                source_url=url, filing_type=row['form'], periods=[{k:p[k] for k in ('role','start','end')} for p in covered], **section)
            documents.append(document)
    return documents


def validate_documents(report, request, documents):
    result = {}
    if not isinstance(documents,list): raise ValueError('MD&A documents must be a list')
    for document in documents:
        required = {'id','entity','cik','scope','source_id','version','document_date','source_url','section','periods','text'}
        if not isinstance(document, dict) or not required <= set(document) or set(document) - required - {'observations', 'filing_type'}:
            raise ValueError('MD&A document fields do not match schema')
        if (document['entity'],document['cik'],document['scope']) != (report.entity,request['cik'],report.scope):
            raise ValueError('MD&A borrower/CIK/scope mismatch')
        if date.fromisoformat(document['document_date']) > date.fromisoformat(request['as_of']):
            raise ValueError('MD&A document is later than as_of')
        if document['section'] not in SECTIONS or any(not isinstance(document[k], str) or not document[k].strip()
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
        if document.get('filing_type', '10-K') not in ('10-K','10-Q','10-K/A','10-Q/A'):
            raise ValueError('Invalid commentary filing type')
        validate_observations(document)
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
    return [dict(table=t.spec.key,topic=n.topic,reason=n.reason or '分析尚未取得')
            for t in report.tables for n in t.narratives if n.status!='supported' or n.claim_type not in ('cause','management')]


def narrative_display(report, table, narrative):
    """Shared visible text and sources for every delivery format."""
    reviewed=is_reviewed(report,table,narrative)
    label='模型分析' if narrative.claim_type in ('cause','management') else '數值比較／分析限制'
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


def commentary_targets(report):
    """Canonical context for the model; model-returned financial IDs are ignored."""
    result=[]
    for table in report.tables:
        for n in table.narratives:
            roles=n.period_roles or ((report.periods[-2].role,report.periods[-1].role)
                if report.mode.value=='annual' or table.spec.key=='income' else ('latest_fy_end','current_interim'))
            if report.mode.value=='quarterly' and table.spec.key=='income':
                roles=('prior_interim','current_interim')
            if table.spec.key == 'ratios' and n.topic in ('liquidity', 'debt_ratio'):
                roles = comparison_roles(report)
            ids = (ratio_fact_ids(report, n.topic) if table.spec.key == 'ratios' and n.topic in ('liquidity', 'debt_ratio')
                   else [fid for fid in n.fact_ids if report.facts[fid].status in AVAILABLE])
            result.append(dict(table=table.spec.key,topic=n.topic,
                fact_ids=ids,
                period_roles=list(roles),comparison=n.text))
    return result


def apply_commentary(report, request, documents, claims):
    """Display model summaries without semantic, numerical, or reviewer gates.

    Source excerpts always come from the supplied source text. An approximate or
    absent model quote falls back to a real source excerpt, never a fabricated quote.
    Canonical financial facts and calculation metadata are never modified.
    """
    docs=validate_documents(report,request,documents)
    if not isinstance(claims,list):raise ValueError('Commentary claims must be a list')
    supplied={(c.get('table'),c.get('topic')):c for c in claims if isinstance(c,dict)}
    targets={(t['table'],t['topic']):t for t in commentary_targets(report)}
    evidence=dict(report.evidence);tables=[]
    for table in report.tables:
        narratives=[]
        for original in table.narratives:
            key=(table.spec.key,original.topic);target=targets[key];claim=supplied.get(key,{})
            text=claim.get('explanation','')
            roles=tuple(target['period_roles'])
            if claim.get('status')=='missing' or not isinstance(text,str) or not text.strip():
                reason=claim.get('reason') or '分析尚未取得：財報來源未提供此項分析或模型未回傳摘要。'
                narratives.append(replace(original,reason=str(reason)));continue
            # Only document identity/context is checked. No both-period quote,
            # exact phrase, numerical token, or manual review requirement.
            relevant=[d for d in docs.values() if set(p['role'] for p in d['periods']) & set(roles)]
            if not relevant:
                narratives.append(replace(original,reason='分析尚未取得：缺少對應財報來源原文。'));continue
            citations=claim.get('citations',[])
            selected=[]
            if isinstance(citations,list):
                for citation in citations:
                    if not isinstance(citation,dict):continue
                    document=docs.get(citation.get('document_id'))
                    if document in relevant:selected.append((document,citation.get('quote','')))
            if not selected:
                # Prefer the current period; prior source material is optional.
                document=next((d for d in relevant if roles[-1] in [p['role'] for p in d['periods']]),relevant[-1])
                selected=[(document,'')]
            eids=[]; excerpt_fallback=False
            for document,proposed_quote in selected:
                source=document['text']
                exact=isinstance(proposed_quote,str) and bool(proposed_quote) and proposed_quote in source
                quote=proposed_quote[:1000] if exact else source[:1000]
                excerpt_fallback |= not exact
                offset=source.index(quote)
                eid='passage:'+digest([document['id'],document['version'],offset,quote])
                evidence[eid]=Evidence(eid,report.entity,report.scope,document['source_id'],document['version'],
                    date.fromisoformat(document['document_date']),document['source_url']+'#'+document['section']+':char='+str(offset),
                    'passage',tuple(p['role'] for p in document['periods']),quote)
                eids.append(eid)
            attribution=claim.get('attribution','')
            attribution=attribution if isinstance(attribution,str) else ''
            claim_type='management' if claim.get('claim_type')=='management' and attribution else 'cause'
            narratives.append(Narrative(original.topic,'supported',text=text,claim_type=claim_type,
                fact_ids=tuple(target['fact_ids']),period_roles=roles,evidence_ids=tuple(dict.fromkeys(eids)),
                attribution=attribution,
                reason='參考原文為財報節錄；模型未提供可直接定位的逐字引述。' if excerpt_fallback else ''))
        tables.append(replace(table,narratives=tuple(narratives)))
    result=replace(report,tables=tuple(tables),evidence=evidence)
    validate_report(result,expected_mode=report.mode)
    return result
