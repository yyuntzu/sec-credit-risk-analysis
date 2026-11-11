"""Independent migration oracle. Fraction arithmetic never supplies SQL inputs."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction

VERSION='bignumeric-q18-half-even-v1'
DIVISIONS=frozenset(('CF-01','CF-02','CF-03','CF-04','CF-05','CF-06','CF-09','CF-10','CF-11','CF-12',
    'COMMON-SIZE-v1','LEVERAGE-v1'))
SUBTRACTIONS=frozenset(('CF-16','CASH-CHANGE-v1','DER-01','DER-02','DER-03','DER-04','DER-06'))
MAXIMUM=Fraction((1<<255)-1,10**38)
MINIMUM=Fraction(-(1<<255),10**38)


def fraction(value):return value if isinstance(value,Fraction) else Fraction(Decimal(str(value)))


def decimal_string(value):
    value=Fraction(value);denominator=value.denominator;scale=0
    while (10**scale)%denominator:
        scale+=1
        if scale>200:raise ValueError('Non-terminating exact decimal')
    coefficient=abs(value.numerator)*(10**scale//denominator)
    digits=str(coefficient).rjust(scale+1,'0')
    return ('-' if value<0 else '')+(digits[:-scale]+'.'+digits[-scale:] if scale else digits)


def checked(value):
    value=Fraction(value)
    if not MINIMUM<=value<=MAXIMUM or (value*10**38).denominator!=1:
        raise ValueError('Value cannot be represented losslessly as BIGNUMERIC')
    return value


def q18(value):
    value=Fraction(value);scaled=abs(value)*10**18
    whole,remainder=divmod(scaled.numerator,scaled.denominator)
    if 2*remainder>scaled.denominator or 2*remainder==scaled.denominator and whole%2:
        whole+=1
    return checked(Fraction((-1 if value<0 else 1)*whole,10**18))


def operands(formula,values):
    a,b=values[:2]
    if formula=='CF-04':return checked(a+b),checked(b+values[2])
    if formula=='CF-05':return checked(checked(a+b)+values[2]),checked(b+values[3])
    if formula=='CF-09':return checked(a-b),b
    return a,b


def formula_value(formula,values):
    values=[checked(fraction(v)) for v in values]
    if formula in DIVISIONS:
        numerator,denominator=operands(formula,values)
        return None if denominator==0 else q18(numerator/denominator)
    if formula in SUBTRACTIONS:return checked(values[0]-values[1])
    if formula=='DER-05':return checked(values[0]+values[1])
    if formula=='STANDARD-EBITDA-v1':
        result=values[0]
        for value in values[1:]:result=checked(result+value)
        return result
    raise ValueError('Unknown independent formula: '+formula)


def canonical_baseline(baseline):
    result=deepcopy(baseline);facts=result['facts'];done=set();active=set()
    def visit(fid):
        if fid in done:return facts[fid]
        if fid in active:raise ValueError('Cycle in independent policy reference')
        active.add(fid);fact=facts[fid]
        if fact['status']=='calculated':
            parents=[visit(parent) for parent in fact['input_ids']]
            value=(formula_value(fact['formula_id'],[p['value'] for p in parents])
                if all(p['status'] in ('sourced','calculated') and p['value'] is not None for p in parents) else None)
            fact['value']=None if value is None else decimal_string(value)
            if value is None:
                fact.update(status='not_calculable',formula_id=None,formula_version=None,input_ids=[])
        done.add(fid);active.remove(fid);return fact
    for fid in facts:visit(fid)
    return result


def canonical_commentary(value):
    """Round growth from exact endpoints, never an already rounded 28-digit ratio."""
    if isinstance(value,list):return [canonical_commentary(v) for v in value]
    if not isinstance(value,dict):return value
    result={k:canonical_commentary(v) for k,v in value.items()}
    if {'before','after','growth'}<=set(result):
        before,after=result['before'],result['after']
        if before is None or after is None or fraction(before)<=0:result['growth']=None
        else:result['growth']=decimal_string(q18((fraction(after)-fraction(before))/fraction(before)))
    if {'relative_growth','numerator','denominator'}<=set(result):
        n,d=result['numerator'],result['denominator']
        if all(entry.get(key) is not None and fraction(entry[key])>0 for entry in (n,d) for key in ('before','after')):
            ng,dg=fraction(n['growth']),fraction(d['growth'])
            result['relative_growth']='numerator_faster' if ng>dg else 'denominator_faster' if ng<dg else 'equal'
        else:result['relative_growth']='not_comparable'
    return result


def verify_audits(reference,rows):
    errors=[];checked_count=0
    for row in rows:
        expected=reference['facts'].get(row['fact_id'])
        if not expected or expected['status']!='calculated' or expected['formula_id'] not in DIVISIONS:continue
        checked_count+=1
        import json
        try:
            audit=json.loads(row['precision_audit'])
            numerator,denominator=operands(expected['formula_id'],
                [fraction(reference['facts'][fid]['value']) for fid in expected['input_ids']])
            if (audit['policy']!=VERSION or audit['division'] is not True
                or fraction(audit['numerator'])!=numerator or fraction(audit['denominator'])!=denominator
                or fraction(audit['canonical_value'])!=fraction(expected['value'])
                or fraction(row['value'])!=fraction(expected['value']) or audit['native_value'] is None):
                raise ValueError('Precision audit does not match independent operands/result')
        except (KeyError,ValueError,TypeError) as error:errors.append(dict(fact_id=row['fact_id'],error=str(error)))
    return dict(checked=checked_count,mismatches=len(errors),details=errors)
