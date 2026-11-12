"""Read-only known workpaper extraction into the SQL source contract, no formulas."""
from copy import deepcopy
from datetime import date
from dataclasses import asdict

from .loan_review_sources import parse_request,prepare_source_inputs,canonical
from .loan_review_contract import METRICS,_dates
from .warehouse_candidate import _require


def reconciliation_slots(bundle):
    bundle=deepcopy(bundle);report,_,_=parse_request(bundle['request'])
    for period in report.periods:
        for metric in ('beginning_cash','ending_cash','cfo','cfi','cff','cash_fx','cash_other','total_assets','total_liabilities','net_worth'):
            if metric+':'+period.role in bundle['inputs'] or 'input:'+metric+':'+period.role in bundle['inputs']:continue
            start,end=_dates(metric,period);spec=METRICS[metric]
            bundle['inputs']['input:'+metric+':'+period.role]=dict(metric=metric,period_role=period.role,
                start=str(start) if start else None,end=str(end) if end else None,unit=spec.unit,
                currency=report.currency,scale=str(report.scale),period_kind='instant' if spec.period_kind in ('instant','opening') else 'duration',
                status='missing',value=None,candidate_ids=[],evidence_ids=[],basis='',reason='Unadopted reconciliation source slot')
    return bundle


def workbook_bundle(path,request,*,quarter=None,book=None):
    from .nexstar_workbook_review import read_workbook,build_inputs
    report,cik,as_of=parse_request(request)
    _require(report.entity=='NXST' and report.scope=='consolidated','Known workbook adapter requires NXST consolidated request')
    book=book or read_workbook(path,as_of)
    base,inputs,evidence=build_inputs(book,report.mode.value,quarter)
    _require(len(base.periods)==len(report.periods) and all((a.role,a.start,a.end)==(b.role,b.start,b.end)
        for a,b in zip(base.periods,report.periods)),'Workbook dates differ from fixed request')
    records=[]
    for item in inputs.values():
        if item['status']!='sourced' or item['value'] is None:continue
        for eid in item['evidence_ids']:
            raw=evidence[eid]
            records.append(dict(metric=item['metric'],period_kind=item['period_kind'],start=str(item['start']) if item['start'] else None,
                end=str(item['end']),unit='USD',scale='1000',value=raw['value'],status='sourced',reason='',
                definition=raw['definition'],basis=raw['basis'],source_id=raw['source_id'],version=book['hash'],
                document_date=as_of.isoformat(),source_uri=str(book['path']),locator=raw['locator'],excerpt=raw['excerpt'],
                verification=dict(verified_by='read-only-workbook-label-adapter',verified_at=as_of.isoformat(),method='checked_against_source')))
    supplement=dict(schema_version=1,entity=report.entity,cik=cik,scope=report.scope,purpose='current_borrower_evidence',records=records)
    bundle=prepare_source_inputs(request,[],[supplement])
    bundle['workbook_snapshot']=dict(path=str(book['path']),sha256=book['hash'],
        raw_observations=book.get('observations',[]),adapter='nexstar-label-cell-v1',sec_verified=False)
    bundle['source_limitations']=['Workbook is a reviewed local snapshot, not SEC-verified evidence',
        'Workbook original publication/as-of availability is unknown',
        'Unverified CF periods and Operating Expense composition remain unavailable']
    return reconciliation_slots(bundle)
