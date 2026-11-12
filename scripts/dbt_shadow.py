"""Run-scoped dbt shadow comparison. Never publishes or substitutes report values.

Only raw candidates and a value-free calculation plan enter SQL. Python baseline
results remain local. BigQuery native decimal differences are reported, not waived.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal, getcontext, localcontext
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

from .loan_review_contract import METRICS, AVAILABLE, _dates
from .loan_review_sources import SEC_FIELDS, canonical, load_json, parse_request
from .loan_review_pipeline import (APPROVED_POLICY_VERSION, APPROVED_DEFINITIONS,
    FORMULA_VERSION, STANDARD_EBITDA_BASIS, _supporting_slots, report_from_source_bundle)

PRECISION_VERSION = 'bignumeric-q18-half-even-v1'
STATES = {'sourced', 'calculated', 'missing', 'conflict', 'not_calculable', 'not_applicable'}


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _formula(fact):
    if ':pct:' in fact.id:
        return 'COMMON-SIZE-v1', (fact.metric, 'revenue')
    spec = METRICS[fact.metric]
    if fact.metric == 'ltm_ebitda':
        return 'STANDARD-EBITDA-v1', spec.inputs
    return spec.formula, spec.inputs


def prepare_plan(bundle):
    """Describe slots/dependencies, not adopted values or Python calculation output."""
    if 'base_report' in bundle:
        raise ValueError('dbt shadow currently requires a SEC/snapshot source bundle; workbook is not supported')
    report, _, _ = parse_request(bundle['request'])
    report = _supporting_slots(report)
    roles = [p.role for p in report.periods]
    slots = dict(report.facts)
    # These are metadata-only supporting slots from the source contract.
    for fid, item in bundle['inputs'].items():
        if fid not in slots:
            from .loan_review_contract import Fact, Status
            from .loan_review_sources import day
            slots[fid] = Fact(fid, item['metric'], item['period_role'], Status.MISSING,
                None, item['unit'], METRICS[item['metric']].definition,
                day(item['start']) if item['start'] else None, day(item['end']) if item['end'] else None,
                report.entity, report.scope, currency=item.get('currency'),
                period_kind=item['period_kind'], reason='Unadopted shadow slot')
    plans = []
    for fid, f in sorted(slots.items()):
        formula, metrics = _formula(f)
        ids = []
        for pos, metric in enumerate(metrics):
            role = f.period_role
            if pos == 1 and f.metric in ('revenue_growth', 'operating_margin_change'):
                index = roles.index(role)
                role = (roles[index-1] if index else 'prior_period_not_in_report') if report.mode.value == 'annual' else (
                    'prior_interim' if role == 'current_interim' else 'prior_period_not_in_report')
            candidate = f'{metric}:{role}'
            ids.append(candidate if candidate in slots else f'input:{metric}:{role}')
        expected_start, expected_end = _dates(f.metric, next(p for p in report.periods if p.role == f.period_role))
        plans.append(dict(fact_id=fid, metric=f.metric, period_role=f.period_role,
            expected_start=expected_start, expected_end=expected_end,
            start=f.start, end=f.end, unit=f.unit, currency=f.currency, period_kind=f.period_kind,
            definition=f.definition, pending=list(METRICS[f.metric].pending),
            sec_fields=list(SEC_FIELDS.get(f.metric, ())), formula_id=formula, input_ids=ids,
            formula_version=APPROVED_POLICY_VERSION if f.metric == 'ltm_ebitda' else FORMULA_VERSION,
            # Direct source selection is forbidden for common-size and existing generic formula slots.
            source_allowed=':pct:' not in fid and METRICS[f.metric].formula is None,
            source_unit=report.currency if f.unit == 'money' else f.unit,
            scale='1000000' if f.unit == 'money' else '1'))
    from .shadow_identity import parse_identity_reviews
    reviews, _ = parse_identity_reviews(bundle, plans)
    for plan in plans:
        if plan['fact_id'] in reviews:
            review = reviews[plan['fact_id']]
            plan.update(formula_id=review['formula_id'],formula_version=review['formula_version'],
                input_ids=review['input_ids'],identity_review=review)
    index = {p['fact_id']: p for p in plans}
    def depth(fid, visiting=()):
        if fid in visiting:
            raise ValueError('Calculation plan has a dependency cycle')
        p = index.get(fid)
        if not p or not p['formula_id']:
            return 0
        return 1 + max((depth(i, (*visiting, fid)) for i in p['input_ids']), default=0)
    for p in plans:
        p['depth'] = depth(p['fact_id'])
        if p['depth'] > 4:
            raise ValueError('Shadow plan exceeds supported dependency depth')
    return plans


def code_hash():
    root = Path(__file__).resolve().parents[1]
    files = [root / 'scripts' / name for name in (
        'dbt_shadow.py', 'loan_review_contract.py', 'loan_review_sources.py',
        'loan_review_pipeline.py', 'review_cloud.py', 'shadow_reconciliation.py', 'warehouse_candidate.py',
        'credit_memo_writer.py', 'review_outputs.py', 'review_workflow.py', 'warehouse_commentary.py',
        'shadow_commentary.py', 'ratio_commentary_analysis.py', 'formal_commentary.py', 'filing_commentary_sources.py',
        'warehouse_excel.py','export_loan_review_excel.mjs','shadow_identity.py','warehouse_execution.py','precision_policy.py')]
    files.extend(sorted((root / 'references/dbt/models/shadow').glob('*')))
    files.extend(sorted((root / 'references/dbt/macros').glob('shadow_*.sql')))
    files.extend(sorted((root / 'references/dbt/tests').glob('review_shadow_*.sql')))
    return digest({str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in files if p.is_file()})


def prepare_run(bundle, *, run_id=None, kernels=(), reconciliations=None, commentary_documents=None, with_baseline=True):
    """Freeze raw candidates, calculation metadata and baseline independently."""
    run_id = run_id or uuid.uuid4().hex
    if not re.fullmatch('[a-f0-9]{32}', run_id):
        raise ValueError('Invalid shadow run ID')
    plans = prepare_plan(bundle)
    from .shadow_identity import parse_identity_reviews
    identity_reviews, identity_evidence = parse_identity_reviews(bundle,plans)
    if not with_baseline:
        from dataclasses import replace
        from datetime import date
        from .loan_review_contract import Evidence
        from .loan_review_pipeline import apply_approved_policy
        report, _, _ = parse_request(bundle['request'])
        report, _ = apply_approved_policy(report,{}, {})
        evidence = {**report.evidence,**identity_evidence}
        # Evidence roles are metadata from raw intervals/concepts, never adopted
        # values or Python-selected inputs. SQL still selects every actual value.
        for eid,observation in bundle['evidence'].items():
            roles = sorted({p['period_role'] for p in plans
                if str(p['start'])==str(observation.get('start')) and str(p['end'])==str(observation.get('end'))
                and (observation.get('metric')==p['metric'] or observation.get('origin')=='sec'
                     and observation.get('field_name') in p['sec_fields'])})
            if not roles or (observation['entity'],observation['scope'])!=(report.entity,report.scope):
                continue
            if eid in evidence:raise ValueError('Raw evidence identity collision')
            evidence[eid] = Evidence(eid,observation['entity'],observation['scope'],observation['source_id'],
                observation['version'],date.fromisoformat(str(observation['document_date'])),observation['locator'],
                'fact' if observation['status']=='sourced' else 'review',tuple(roles),'Raw observation; selected only by dbt')
        report = replace(report,evidence=evidence)
        acceptance = None
    elif identity_reviews:
        from dataclasses import replace
        from .loan_review_pipeline import complete_report
        initial, _, _ = parse_request(bundle['request'])
        initial = replace(initial,evidence={**initial.evidence,**identity_evidence})
        kwargs = [dict(fact_id=r['fact_id'],formula_id=r['formula_id'],formula_version=r['formula_version'],
            input_ids=tuple(r['input_ids']),definition_evidence_id=r['evidence']['id'])
            for r in sorted(identity_reviews.values(),key=lambda r:next(p['depth'] for p in plans if p['fact_id']==r['fact_id']))]
        report, acceptance = complete_report(initial,bundle['inputs'],bundle['evidence'],identity_reviews=kwargs)
    else:
        report, acceptance = report_from_source_bundle(bundle)
    from .shadow_reconciliation import prepare_reviews, baseline_reconciliations, baseline_reviewed_cash
    report, checks, review_records = prepare_reviews(report, reconciliations,as_of=bundle['request']['as_of'])
    if with_baseline:
        report = baseline_reviewed_cash(report,checks)
        acceptance = baseline_reconciliations(report, checks, acceptance)
    metadata = dict(run_id=run_id, entity=report.entity, scope=report.scope,
        source_hash=digest(bundle), request=bundle['request'], scale='1000000',
        formula_version=FORMULA_VERSION, policy_version=APPROVED_POLICY_VERSION,
        approved_definitions=APPROVED_DEFINITIONS, standard_ebitda_basis=STANDARD_EBITDA_BASIS,
        precision_version=PRECISION_VERSION, precision_approved=False,
        precision_policy_implementation_approved=True,
        identity_source_hash=digest({k:v for k,v in bundle.items() if k!='identity_reviews'}),
        baseline_context=dict(precision=getcontext().prec, rounding=getcontext().rounding,
            traps=sorted(k.__name__ for k,v in getcontext().traps.items() if v)),
        python_version=sys.version, source_selection='independent-dbt-from-candidates')
    metadata['required_fact_ids'] = sorted({fid for table in report.tables for row in table.cells for fid in row})
    if not with_baseline:
        metadata.pop('baseline_context')
        metadata.update(calculation_mode='dbt-only-candidate',request_hash=digest(bundle['request']),baseline_comparison='not_run')
    source_limits=bundle.get('source_limitations',[])
    if not isinstance(source_limits,list) or not all(isinstance(item,str) and item.strip() for item in source_limits):
        raise ValueError('Source limitations must be explicit nonempty strings')
    metadata['source_limitations'] = sorted(set(source_limits+list((acceptance or {}).get('source_limitations', ()))))
    if acceptance is not None and source_limits:
        acceptance['source_limitations']=metadata['source_limitations']
        acceptance['acceptance_blockers']=sorted(set(acceptance['acceptance_blockers']+source_limits))
        acceptance['substantive_data_ready']=False
    metadata['decisions'] = sorted(report.decisions)
    metadata['excluded_observation_ids'] = sorted(bundle.get('excluded', {}))
    commentary_documents = [] if commentary_documents is None else commentary_documents
    from .formal_commentary import validate_documents
    from .filing_commentary_sources import document_observations
    from .ratio_commentary_analysis import BALANCE_CONCEPTS, TOTAL_CONCEPTS, RATIOS, LIMITATIONS
    validate_documents(report,bundle['request'],commentary_documents)
    document_rows = document_observations(commentary_documents)
    document_ids = [item['id'] for item in document_rows]
    if len(document_ids)!=len(set(document_ids)) or set(document_ids)&set(bundle['evidence']):
        raise ValueError('Duplicate commentary observation identity')
    metadata['commentary_documents_hash'] = digest(commentary_documents)
    try:
        metadata['commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True,
            capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        metadata['commit'] = 'unavailable'
    metadata['plan_hash'] = digest(plans)
    metadata['code_hash'] = code_hash()
    metadata['reconciliations_hash'] = digest(reconciliations)
    records = [('metadata', 'run', metadata)]
    records.extend(('slot', p['fact_id'], p) for p in plans)
    for key, value in sorted(bundle['evidence'].items()):
        observation = dict(value)
        if value.get('value') is not None and value['unit'] != 'text':
            observation['source_quantum'] = str(Decimal(1).scaleb(Decimal(value['value']).as_tuple().exponent))
        records.append(('observation', key, observation))
    records.extend(review_records)
    records.extend(('commentary_observation',item['id'],item) for item in document_rows)
    for tag in sorted(set(BALANCE_CONCEPTS)|set(TOTAL_CONCEPTS)):
        field, group = BALANCE_CONCEPTS.get(tag,(None,None))
        records.append(('commentary_concept',tag,dict(field_name=field,group=group,total_metric=TOTAL_CONCEPTS.get(tag))))
    records.extend(('commentary_ratio',metric,dict(numerator=num,denominator=den)) for metric,(num,den) in RATIOS.items())
    records.extend(('commentary_limitation',str(index),dict(text=text)) for index,text in enumerate(LIMITATIONS))
    records.extend(('kernel_case', c['case_id'], c) for c in kernels)
    baseline = json.loads(canonical(asdict(report))) if with_baseline else None
    return metadata, records, baseline, acceptance


def _exact_bignumeric(value):
    """Fail before a BigQuery cast could silently round an original decimal."""
    d = Decimal(str(value))
    if not d.is_finite():
        raise ValueError("Non-finite source value")
    # Positive boundary is smaller than 2**255 / 10**38; a conservative symmetric envelope.
    with localcontext() as ctx:
        ctx.prec = max(100, len(d.as_tuple().digits) + abs(d.as_tuple().exponent) + 10)
        if not d.is_finite() or abs(d) >= Decimal(2)**255 / Decimal(10)**38:
            raise ValueError('Source outside BIGNUMERIC range')
        if d != d.quantize(Decimal('1e-38')):
            raise ValueError('Source cannot be represented losslessly by BIGNUMERIC')
    return d


def validate_records(records):
    seen = set()
    metadata = next((payload for kind,_,payload in records if kind=='metadata'),{})
    report_scale = Decimal(str(metadata.get('scale','1000000')))
    for kind, key, payload in records:
        if (kind, key) in seen:
            raise ValueError('Duplicate shadow input identity')
        seen.add((kind, key))
        if kind in ('observation','commentary_observation') and payload['unit'] != 'text':
            scale = _exact_bignumeric(payload['scale'])
            if scale <= 0:
                raise ValueError('Source scale must be positive')
            if payload.get('value') is not None:
                value = _exact_bignumeric(payload['value'])
                # Validate raw normalization, not a financial formula. SQL still
                # selects and normalizes independently; no Python result is loaded.
                monetary = re.fullmatch('[A-Z]{3}',payload['unit']) is not None
                target = report_scale if monetary else Decimal(1)
                with localcontext() as context:
                    context.prec = 256
                    _exact_bignumeric(value*scale)
                    _exact_bignumeric(value*scale/target)
                    if payload.get('source_quantum') is not None:
                        quantum = _exact_bignumeric(payload['source_quantum'])
                        _exact_bignumeric(quantum*scale)
                        if monetary:
                            _exact_bignumeric(quantum*scale/target/2)


DIVISION_FORMULAS = frozenset(('CF-01', 'CF-02', 'CF-03', 'CF-04', 'CF-05',
    'CF-06', 'CF-09', 'CF-10', 'CF-11', 'CF-12', 'COMMON-SIZE-v1', 'LEVERAGE-v1'))
EXACT_FORMULAS = frozenset(('CF-16', 'CASH-CHANGE-v1', 'STANDARD-EBITDA-v1',
    'DER-01', 'DER-02', 'DER-03', 'DER-04', 'DER-05', 'DER-06'))


def _difference_classes(details, baseline, actual):
    """Only division or independently checked propagation may be precision-affected.

    This labels unapproved differences; it neither proves an error is small nor
    approves any precision policy. Source and exact-arithmetic defects stay errors.
    """
    index = {r['fact_id']: r for r in details}
    active = set()
    def classify(fid):
        row = index.get(fid)
        if row is None:
            return 'mismatch'
        if 'classification' in row:
            return row['classification']
        if fid in active:
            raise ValueError('Cycle in comparison lineage')
        active.add(fid)
        result = 'mismatch'
        if not row['differing_fields']:
            result = 'equivalent'
        elif row['differing_fields'] == ['value']:
            fact = baseline['facts'][fid]
            formula = fact.get('formula_id')
            if fact['status'] == 'calculated' and formula in DIVISION_FORMULAS:
                # A corrupt source or upstream exact sum cannot be called rounding.
                if all(classify(i) in ('equivalent', 'numeric_difference_unapproved') for i in fact['input_ids']):
                    result = 'numeric_difference_unapproved'
            elif fact['status'] == 'calculated' and formula in EXACT_FORMULAS:
                parents = [classify(i) for i in fact['input_ids']]
                if 'numeric_difference_unapproved' in parents and all(x != 'mismatch' for x in parents):
                    values = [Decimal(str(actual[i]['value'])) for i in fact['input_ids']]
                    with localcontext() as ctx:
                        ctx.prec = max(100, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in values) + 10)
                        if formula == 'STANDARD-EBITDA-v1':
                            computed = sum(values, Decimal(0))
                        elif formula == 'DER-05':
                            computed = values[0] + values[1]
                        else:
                            computed = values[0] - values[1]
                    if computed == Decimal(str(actual[fid]['value'])):
                        result = 'numeric_difference_unapproved'
        row['classification'] = result
        active.remove(fid)
        return result
    for fid in index:
        classify(fid)


def compare_facts(baseline, rows, *, expected_run_id, expected_bindings=None):
    """Exact comparison, including missing/excess rows. No epsilon/auto acceptance."""
    if not isinstance(expected_run_id, str) or not re.fullmatch('[a-f0-9]{32}', expected_run_id):
        raise ValueError('Invalid expected shadow run ID')
    identity = {'run_id': expected_run_id, 'entity': baseline['entity'], 'scope': baseline['scope']}
    if set(expected_bindings or {}) - {'source_hash', 'plan_hash', 'precision_version'}:
        raise ValueError('Unknown warehouse binding field')
    identity.update(expected_bindings or {})
    actual = {}
    for row in rows:
        row = dict(row)
        for field, expected in identity.items():
            if not expected or row.get(field) != expected:
                raise ValueError(f'Warehouse identity mismatch: {field} for fact {row.get("fact_id")}')
        fid = row['fact_id']
        if fid in actual:
            raise ValueError('Duplicate warehouse fact')
        if row['status'] not in STATES:
            raise ValueError('Invalid warehouse fact status')
        actual[fid] = row
    details = []
    for fid in sorted(set(baseline['facts']) | set(actual)):
        expected, found = baseline['facts'].get(fid), actual.get(fid)
        mismatch = []
        if expected is None or found is None:
            mismatch.append('unexpected_fact' if expected is None else 'missing_fact')
        else:
            for key in ('metric','period_role','start','end','unit','currency','period_kind','basis','definition','formula_id','formula_version'):
                left, right = expected.get(key), found.get(key)
                if left != right:
                    mismatch.append(key)
            for key in ('input_ids','evidence_ids'):
                left, right = expected.get(key, []), found.get(key, [])
                if (left != right if key == 'input_ids' else set(left) != set(right) or len(right) != len(set(right))):
                    mismatch.append(key)
            if expected['status'] != found['status']:
                mismatch.append('status')
            if expected['value'] is None or found.get('value') is None:
                if expected['value'] != found.get('value'):
                    mismatch.append('value')
            elif expected['unit'] == 'text':
                if expected['value'] != found['value']:
                    mismatch.append('value')
            elif Decimal(expected['value']) != Decimal(str(found['value'])):
                mismatch.append('value')
            for key in ('original_value', 'original_scale'):
                left, right = expected.get(key), found.get(key)
                if left is None or right is None or expected['unit'] == 'text':
                    same = left == right
                else:
                    same = Decimal(str(left)) == Decimal(str(right))
                if not same:
                    mismatch.append(key)
            if found['status'] not in ('sourced','calculated') and found.get('value') is not None:
                mismatch.append('unavailable_has_value')
        left, right = (expected or {}).get('value'), (found or {}).get('value')
        delta = None
        if left is not None and right is not None and expected and expected['unit'] != 'text':
            with localcontext() as ctx:
                ctx.prec = 100
                delta = str(Decimal(str(right)) - Decimal(left))
        details.append(dict(fact_id=fid, differing_fields=mismatch,
            python_value=left, dbt_value=right, difference=delta, python=expected, dbt=found))
    _difference_classes(details, baseline, actual)
    return dict(precision_version=PRECISION_VERSION, precision_approved=False,
        precision_policy_implementation_approved=True,
        publication_eligible=False, facts_compared=len(details), equivalent=sum(not r['differing_fields'] for r in details),
        numeric_differences=sum(r['classification']=='numeric_difference_unapproved' for r in details),
        mismatches=sum(r['classification']=='mismatch' for r in details), details=details)


class ShadowWarehouse:
    """Isolated, expiring BigQuery dataset. No production writes or publication interface."""
    def __init__(self, project, run_id, *, client=None):
        from google.cloud import bigquery
        if not re.fullmatch(r'[A-Za-z0-9_-]+',project) or not re.fullmatch('[a-f0-9]{32}',run_id):
            raise ValueError('Invalid project/run identity')
        self.project, self.run_id = project, run_id
        self.dataset = 'sec_review_shadow_' + run_id
        self.bq = bigquery
        self.client = client or bigquery.Client(project=project)

    def execute(self, records, directory):
        validate_records(records)
        dataset = self.bq.Dataset(f'{self.project}.{self.dataset}')
        dataset.location = os.environ.get('BQ_LOCATION','US')
        dataset.default_table_expiration_ms = 7 * 24 * 60 * 60 * 1000
        # A fresh dataset owns each attempt. Refuse accidental reuse or concurrent collision.
        self.client.create_dataset(dataset, exists_ok=False)
        schema = [self.bq.SchemaField(k,'STRING',mode='REQUIRED') for k in ('run_id','entity','record_kind','record_id','payload')]
        schema.append(self.bq.SchemaField('created_at','TIMESTAMP',mode='REQUIRED'))
        table = self.bq.Table(f'{self.project}.{self.dataset}.raw_review_shadow_inputs',schema=schema)
        self.client.create_table(table)
        metadata = next(v for k,_,v in records if k == 'metadata')
        stamp = datetime.now(timezone.utc).isoformat()
        rows = [dict(run_id=self.run_id,entity=metadata['entity'],record_kind=k,record_id=key,
            payload=canonical(value),created_at=stamp) for k,key,value in records]
        self.client.load_table_from_json(rows,table.reference,
            job_id='shadow_'+self.run_id,job_config=self.bq.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY')).result()
        from .review_cloud import ReviewCloud
        runner = ReviewCloud(self.project,self.dataset,client=self.client)
        receipt = runner.dbt('shadow', variables={'shadow_run_id':self.run_id}, artifact_dir=directory / 'dbt')
        routine=self.client.get_routine(f'{self.project}.{self.dataset}.review_divide_q18_v1')
        macro=(Path(__file__).resolve().parents[1]/'references/dbt/macros/shadow_precision.sql').read_text()
        expected_body=macro.split('{% macro shadow_precision_body() -%}',1)[1].split('{%- endmacro %}',1)[0].strip()
        if routine.body.strip()!=expected_body or routine.language!='JAVASCRIPT':
            raise ValueError('Warehouse precision routine differs from fixed dbt source')
        receipt['precision_routine']=dict(name=f'{self.project}.{self.dataset}.review_divide_q18_v1',
            body_sha256=hashlib.sha256(routine.body.strip().encode()).hexdigest(),language=routine.language)
        config = self.bq.QueryJobConfig(query_parameters=[self.bq.ScalarQueryParameter('run_id','STRING',self.run_id)])
        result = list(self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_shadow_facts` WHERE run_id=@run_id',job_config=config).result())
        kernels = list(self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_shadow_kernels` WHERE run_id=@run_id',job_config=config).result())
        recs = self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_shadow_reconciliations` WHERE run_id=@run_id',job_config=config).result()
        receipt['reconciliation_rows'] = [dict(r) for r in recs]
        accepted = self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_shadow_acceptance` WHERE run_id=@run_id',job_config=config).result()
        receipt['acceptance_rows'] = [dict(r) for r in accepted]
        commentary = self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_shadow_commentary` WHERE run_id=@run_id',job_config=config).result()
        receipt['commentary_rows'] = [dict(r) for r in commentary]
        return [dict(r) for r in result], [dict(r) for r in kernels], receipt


def run_shadow(bundle, directory, *, project, warehouse=None, prepare_only=False, kernels=(), reconciliations=None,
               candidate_preview=False, commentary_documents=None):
    directory = Path(directory)
    directory.mkdir(parents=True,exist_ok=False)
    metadata, records, baseline, acceptance = prepare_run(bundle,kernels=kernels,reconciliations=reconciliations,
        commentary_documents=commentary_documents)
    metadata.update(status='prepared', publication_eligible=False)
    for name,payload in [('baseline.json',baseline),('baseline_acceptance.json',acceptance),
                         ('source_bundle.json',bundle),('reconciliation_reviews.json',reconciliations),
                         ('commentary_documents.json',[] if commentary_documents is None else commentary_documents),
                         ('shadow_inputs.json',records),('shadow_manifest.json',metadata)]:
        (directory/name).write_text(json.dumps(payload,ensure_ascii=False,default=str,indent=2))
    if prepare_only:
        return dict(metadata,status='prepared',publication_eligible=False)
    try:
        warehouse = warehouse or ShadowWarehouse(project,metadata['run_id'])
        metadata['dataset'] = getattr(warehouse,'dataset',None)
        metadata['project'] = project
        rows, kernel_rows, receipt = warehouse.execute(records,directory)
        if metadata['code_hash'] != code_hash():
            raise ValueError('Source code changed during shadow execution; use a new run')
        (directory/'warehouse_facts.json').write_text(json.dumps(rows,ensure_ascii=False,default=str,indent=2))
        comparison = compare_facts(baseline,rows,expected_run_id=metadata['run_id'],
            expected_bindings={k:metadata[k] for k in ('source_hash','plan_hash','precision_version')})
        from .shadow_reconciliation import compare_reconciliations, compare_acceptance
        reconciliation_rows = receipt.pop('reconciliation_rows')
        acceptance_rows = receipt.pop('acceptance_rows')
        commentary_rows = receipt.pop('commentary_rows')
        (directory/'warehouse_commentary.json').write_text(json.dumps(commentary_rows,default=str,ensure_ascii=False,indent=2))
        from .shadow_commentary import compare_commentary
        commentary_comparison = compare_commentary(bundle,baseline,commentary_rows,comparison,
            bindings={key:metadata[key] for key in ('run_id','entity','scope','source_hash','plan_hash','precision_version')},
            documents=[] if commentary_documents is None else commentary_documents)
        from .precision_policy import canonical_baseline,verify_audits
        reference=canonical_baseline(baseline)
        canonical_comparison=compare_facts(reference,rows,expected_run_id=metadata['run_id'],
            expected_bindings={k:metadata[k] for k in ('source_hash','plan_hash','precision_version')})
        canonical_errors=sum(bool(row['differing_fields']) for row in canonical_comparison['details'])
        audits=verify_audits(reference,rows)
        canonical_commentary=compare_commentary(bundle,reference,commentary_rows,canonical_comparison,
            bindings={key:metadata[key] for key in ('run_id','entity','scope','source_hash','plan_hash','precision_version')},
            documents=[] if commentary_documents is None else commentary_documents,canonical_precision=True)
        comparison['canonical_precision']=dict(policy=PRECISION_VERSION,mismatches=canonical_errors,
            details=canonical_comparison['details'],audits=audits,commentary_mismatches=canonical_commentary['mismatches'],
            commentary_details=canonical_commentary['details'])
        for pack in (comparison,commentary_comparison):
            for item in pack['details']:
                if item['classification']=='numeric_difference_unapproved':item['classification']='legacy_precision_difference'
        comparison['legacy_mismatches']=comparison['mismatches']
        comparison['mismatches']=canonical_errors+audits['mismatches']
        commentary_comparison['legacy_mismatches']=commentary_comparison['mismatches']
        commentary_comparison['mismatches']=canonical_commentary['mismatches']
        (directory/'commentary_comparison.json').write_text(json.dumps(commentary_comparison,default=str,ensure_ascii=False,indent=2))
        (directory/'warehouse_acceptance.json').write_text(json.dumps(acceptance_rows,default=str,ensure_ascii=False,indent=2))
        acceptance_comparison = compare_acceptance(acceptance, acceptance_rows,
            bindings={key:metadata[key] for key in ('run_id','entity','scope','source_hash','plan_hash','precision_version')})
        (directory/'acceptance_comparison.json').write_text(json.dumps(acceptance_comparison,default=str,ensure_ascii=False,indent=2))
        reconciliation_comparison = compare_reconciliations(acceptance,reconciliation_rows,run_id=metadata['run_id'],entity=baseline['entity'])
        (directory/'warehouse_reconciliations.json').write_text(json.dumps(reconciliation_rows,default=str,ensure_ascii=False,indent=2))
        (directory/'reconciliation_comparison.json').write_text(json.dumps(reconciliation_comparison,default=str,ensure_ascii=False,indent=2))
        (directory/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,default=str,indent=2))
        with (directory/'comparison.csv').open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=['fact_id','classification','differing_fields','python_value','dbt_value','difference'])
            writer.writeheader()
            writer.writerows({k:r[k] for k in writer.fieldnames} for r in comparison['details'])
        (directory/'kernel_results.json').write_text(json.dumps(kernel_rows,ensure_ascii=False,default=str,indent=2))
        metadata.update(status='compared',publication_eligible=False,dbt=receipt,
            dataset=getattr(warehouse,'dataset',None),equivalent=comparison['equivalent'],
            mismatches=comparison['mismatches'],reconciliation_mismatches=reconciliation_comparison['mismatches'],
            acceptance_mismatches=acceptance_comparison['mismatches'],numeric_differences=comparison['numeric_differences'])
        metadata.update(commentary_mismatches=commentary_comparison['mismatches'],
            commentary_numeric_differences=commentary_comparison['numeric_differences'])
        metadata['canonical_precision_mismatches']=canonical_errors+audits['mismatches']+canonical_commentary['mismatches']
        from .warehouse_candidate import freeze_receipt
        metadata['calculation_receipt_sha256'] = freeze_receipt(directory, metadata)
        if candidate_preview:
            from .warehouse_candidate import write_preview
            preview = write_preview(directory, directory / 'candidate_preview',
                expected_receipt_sha256=metadata['calculation_receipt_sha256'])
            metadata['candidate_preview_path'] = preview['dashboard_path']
    except Exception as exc:
        metadata.update(status='failed',publication_eligible=False,error=str(exc))
        raise
    finally:
        (directory/'shadow_manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,default=str,indent=2))
    return metadata


def main(argv=None):
    parser=argparse.ArgumentParser(description='Isolated dbt shadow comparison; never publishes')
    parser.add_argument('--source-bundle',required=True)
    parser.add_argument('--output-dir',required=True,help='New directory; must not exist')
    parser.add_argument('--project',default=os.environ.get('GCP_PROJECT_ID','focus-heuristic-438521-v4'))
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--kernel-cases')
    parser.add_argument('--reconciliations',help='Structured checks and review evidence JSON; shadow only')
    parser.add_argument('--candidate-preview',action='store_true',help='Render receipt-bound dbt results as draft MD/JSON/HTML')
    parser.add_argument('--commentary-documents',help='Validated MD&A/Balance Sheet document list JSON, including raw observations')
    args=parser.parse_args(argv)
    result=run_shadow(load_json(args.source_bundle),args.output_dir,project=args.project,
        prepare_only=args.prepare_only,kernels=load_json(args.kernel_cases) if args.kernel_cases else (),
        reconciliations=load_json(args.reconciliations) if args.reconciliations else None,
        candidate_preview=args.candidate_preview,
        commentary_documents=load_json(args.commentary_documents) if args.commentary_documents else None)
    print(json.dumps(result,ensure_ascii=False,default=str,indent=2))
    return 1 if any(result.get(key) for key in ('mismatches','reconciliation_mismatches','acceptance_mismatches','commentary_mismatches')) else 0


if __name__=='__main__':
    sys.exit(main())
