"""Bounded filing sections and context-qualified inline XBRL for commentary.

No financial values are inferred from visual table column positions. Inline facts
must identify the requested entity, an instant context and a simple currency unit.
Unclassified/custom rows remain readable in the table excerpt for model analysis.
"""
from html.parser import HTMLParser
import re

try:
    from .loan_review_sources import number
    from .ratio_commentary_analysis import BALANCE_CONCEPTS, TOTAL_CONCEPTS
except ImportError:
    from loan_review_sources import number
    from ratio_commentary_analysis import BALANCE_CONCEPTS, TOTAL_CONCEPTS

SECTIONS = ('MD&A', 'Balance Sheet', 'Debt Note', 'Equity Note')
OBSERVATION_FIELDS = {'tag', 'value', 'unit', 'scale', 'end', 'locator'}


class _Filing(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []; self.tables = []; self.table_stack = []; self.table_ids = []; self.table_count = 0
        self.contexts = {}; self.units = {}; self.facts = []
        self.context = None; self.unit = None; self.fact = None; self.leaf = None
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); local = tag.split(':')[-1]
        if tag in ('script', 'style', 'head', 'ix:header'): self.hidden += 1
        if local == 'context': self.context = dict(id=a.get('id'), instant='', identifier='', dimensional=False)
        if local in ('segment', 'scenario', 'explicitmember', 'typedmember') and self.context is not None:
            self.context['dimensional'] = True
        if local == 'unit': self.unit = dict(id=a.get('id'), measures=[], divide=False)
        if local == 'divide' and self.unit is not None: self.unit['divide'] = True
        if local in ('identifier', 'instant', 'measure'): self.leaf = (local, [])
        if tag == 'ix:nonfraction': self.fact = dict(attrs=a, text=[], tables=tuple(self.table_ids))
        if not self.hidden:
            if tag in ('p','div','tr','table','h1','h2','h3','h4','h5','h6','br'):
                self.parts.append('\n')
            if tag == 'table':
                self.table_stack.append([]); self.table_ids.append(self.table_count); self.table_count += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs); self.handle_endtag(tag)

    def handle_data(self, data):
        if self.leaf: self.leaf[1].append(data)
        if self.fact is not None: self.fact['text'].append(data)
        if not self.hidden:
            self.parts.append(data)
            for table in self.table_stack: table.append(data)

    def handle_endtag(self, tag):
        local = tag.split(':')[-1]
        if self.leaf and local == self.leaf[0]:
            key, parts = self.leaf; value = ''.join(parts).strip()
            if key in ('identifier', 'instant') and self.context is not None: self.context[key] = value
            if key == 'measure' and self.unit is not None: self.unit['measures'].append(value)
            self.leaf = None
        if local == 'context' and self.context is not None:
            self.contexts[self.context['id']] = self.context; self.context = None
        if local == 'unit' and self.unit is not None:
            self.units[self.unit['id']] = self.unit; self.unit = None
        if tag == 'ix:nonfraction' and self.fact is not None:
            self.facts.append(self.fact); self.fact = None
        if not self.hidden:
            if tag == 'table' and self.table_stack:
                self.tables.append((self.table_ids.pop(), ' '.join(' '.join(self.table_stack.pop()).split())))
            if tag in ('p','div','tr','table','h1','h2','h3','h4','h5','h6'): self.parts.append('\n')
        if tag in ('script','style','head','ix:header'): self.hidden = max(0, self.hidden-1)


def extract_filing_sections(html, cik, dates):
    """Return optional sections; absent sections are absent, never arbitrary text."""
    parser = _Filing(); parser.feed(html)
    matches = [(index, t) for index, t in parser.tables if re.search(r'current\s+assets', t, re.I)
               and re.search(r'current\s+liabilities', t, re.I) and re.search(r'total\s+assets', t, re.I)]
    selected = min(matches, key=lambda item: len(item[1])) if matches else None
    observations = []
    for index, fact in enumerate(parser.facts):
        if selected is None or selected[0] not in fact['tables']: continue
        a = fact['attrs']; concept = a.get('name', '')
        namespace, _, tag = concept.partition(':')
        if namespace != 'us-gaap' or tag not in set(BALANCE_CONCEPTS) | set(TOTAL_CONCEPTS): continue
        context = parser.contexts.get(a.get('contextref')); unit = parser.units.get(a.get('unitref'))
        if not context or context['dimensional'] or context['instant'] not in dates: continue
        if not context['identifier'].isdigit() or context['identifier'].zfill(10) != cik: continue
        if not unit or unit['divide'] or len(unit['measures']) != 1: continue
        if not re.fullmatch(r'iso4217:[A-Z]{3}', unit['measures'][0]): continue
        # Unsupported transforms must not be treated as dot-decimal amounts.
        fmt = a.get('format', '').split(':')[-1]
        if fmt not in ('', 'num-dot-decimal', 'numdotdecimal', 'zerodash', 'zero-dash'): continue
        raw = ''.join(fact['text']).strip().replace('\xa0','').replace(' ','')
        if raw in ('—','–','-') and fmt in ('zerodash','zero-dash'): raw = '0'
        if not re.fullmatch(r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', raw): continue
        if a.get('sign', '') not in ('', '-'): continue
        try:
            exponent = int(a.get('scale', '0'))
            if not -12 <= exponent <= 12: continue
            value = number(raw.replace(',', '')) * (-1 if a.get('sign') == '-' else 1)
            scale = 10 ** exponent if exponent >= 0 else '0.' + '0' * (-exponent-1) + '1'
        except (ValueError, TypeError): continue
        if a.get('xsi:nil') in ('true', '1'): continue
        locator = 'ix:nonFraction[' + str(index) + '];context=' + a['contextref']
        observations.append(dict(tag=tag, value=str(value), unit=unit['measures'][0].split(':')[-1],
                                 scale=str(scale), end=context['instant'], locator=locator))
    sections = []
    if selected:
        text = selected[1]
        if len(text) <= 80000:
            sections.append(dict(section='Balance Sheet', text=text, observations=observations))
    # Preserve plain-text note bodies and stop at the next numbered note. A TOC
    # heading is ignored if the immediately bounded body is too short.
    text = '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
    headings = list(re.finditer(r'(?im)^\s*(?:note\s+)?\d{1,2}\s*[).:\-–]\s*([^\n]{1,120})', text))
    for section, pattern in [('Debt Note',r'\b(debt|borrowings|credit facilit|financing arrangements)'),
                             ('Equity Note',r'\b(equity|stockholders|shareholders|members.? capital)')]:
        candidates = []
        for index, match in enumerate(headings):
            if not re.search(pattern, match.group(1), re.I): continue
            end = headings[index+1].start() if index+1 < len(headings) else len(text)
            body = text[match.start():end]
            if 100 <= len(body) <= 80000: candidates.append(body)
        if candidates: sections.append(dict(section=section, text=max(candidates, key=len)))
    return sections


def validate_observations(document):
    observations = document.get('observations', [])
    if not isinstance(observations, list) or len(observations) > 2000:
        raise ValueError('Bounded balance-sheet observations required')
    if observations and document['section'] != 'Balance Sheet':
        raise ValueError('Structured observations require a Balance Sheet document')
    for row in observations:
        if not isinstance(row, dict) or set(row) != OBSERVATION_FIELDS:
            raise ValueError('Balance-sheet observation schema mismatch')
        if row['tag'] not in set(BALANCE_CONCEPTS) | set(TOTAL_CONCEPTS):
            raise ValueError('Unknown balance-sheet observation concept')
        if not re.fullmatch(r'[A-Z]{3}', row['unit']) or not isinstance(row['locator'],str) or not row['locator'].strip():
            raise ValueError('Observation currency and locator required')
        number(row['value'])
        if number(row['scale']) <= 0: raise ValueError('Positive observation scale required')
        # Raw table dates must match a declared request endpoint exactly.
        if row['end'] not in {p['end'] for p in document['periods']}:
            raise ValueError('Balance-sheet observation date differs from covered endpoints')


def document_observations(documents):
    result = []
    for d in documents:
        validate_observations(d)
        for row in d.get('observations', []):
            result.append(dict(row, id=d['id'] + ':' + row['locator'], namespace='us-gaap',
                entity=d['entity'], scope=d['scope'], status='sourced', start=None, period_kind='instant',
                source_id=d['source_id'], version=d['version'], document_date=d['document_date'],
                source_url=d['source_url'], filing_type=d.get('filing_type')))
    return result
