"""Native precision dossier using an existing isolated q18 dbt routine."""
import argparse
import hashlib
import json
from pathlib import Path
import random

from . import precision_policy as policy
from .warehouse_candidate import file_hash,_require


def cases():
    result=[]
    def add(name,n,d):
        expected=None if n is None or d is None or policy.fraction(d)==0 else policy.q18(policy.fraction(n)/policy.fraction(d))
        result.append(dict(case_id=name,numerator=n,denominator=d,
            expected=None if expected is None else policy.decimal_string(expected)))
    for sign in ('','-'):
        for digit in (5,15,25,35):add('tie-'+sign+str(digit),sign+'0.'+str(digit).rjust(19,'0'),'1')
        for name,n in (('above','50000000000000000000.00000000000000000001'),
                       ('tie','50000000000000000000'),('below','49999999999999999999.99999999999999999999')):
            add('double-'+sign+name,sign+n,'1e38')
        add('carry-'+sign,sign+'99999999999999999999.9999999999999999995','1')
    for index,pair in enumerate((('1','3'),('1','-3'),('1e-38','1'),('1e38','1'),('0','1'),
            ('1','0'),(None,'1'),('1',None))):add('special-'+str(index),*pair)
    rng=random.Random(20261111)
    for index in range(200):
        numerator=policy.Fraction(rng.randint(-10**35,10**35),10**rng.randint(0,38))
        denominator=policy.Fraction(rng.randint(1,10**35),10**rng.randint(0,38))
        if policy.MINIMUM<=numerator/denominator<=policy.MAXIMUM:
            add('random-'+str(index),policy.decimal_string(numerator),policy.decimal_string(denominator))
    return result


def validate(calculation,pin,output,*,project):
    from google.cloud import bigquery
    from google.api_core.exceptions import BadRequest
    calculation=Path(calculation);output=Path(output)
    _require(file_hash(calculation/'calculation_receipt.json')==pin,'Boundary source receipt pin mismatch')
    receipt=json.loads((calculation/'calculation_receipt.json').read_text())
    _require(receipt['bindings']['entity']=='SYNTHETIC-ONLY'
        and receipt['bindings']['precision_version']==policy.VERSION,'Synthetic approved precision version required')
    run_id=receipt['bindings']['run_id']
    import re
    _require(re.fullmatch('[a-f0-9]{32}',run_id) is not None and re.fullmatch('[a-z][a-z0-9-]+',project) is not None,
        'Invalid boundary warehouse identity')
    output.mkdir(parents=True,exist_ok=False)
    client=bigquery.Client(project=project);routine=f'{project}.sec_review_shadow_{run_id}.review_divide_q18_v1'
    actual_routine=client.get_routine(routine)
    _require(hashlib.sha256(actual_routine.body.strip().encode()).hexdigest()==receipt['dbt']['precision_routine']['body_sha256'],
        'Precision routine changed after original calculation')
    fixtures=cases();(output/'fixtures.json').write_text(json.dumps(fixtures,indent=2))
    parameters=[bigquery.StructQueryParameter(None,*[bigquery.ScalarQueryParameter(key,'STRING',row[key])
        for key in ('case_id','numerator','denominator','expected')]) for row in fixtures]
    config=bigquery.QueryJobConfig(query_parameters=[bigquery.ArrayQueryParameter('cases','STRUCT',parameters)])
    sql=f'''select *,cast(`{routine}`(numerator,denominator) as bignumeric) as actual,
        safe_divide(cast(numerator as bignumeric),cast(denominator as bignumeric)) as native_value,
        round(safe_divide(cast(numerator as bignumeric),cast(denominator as bignumeric)),18,'ROUND_HALF_EVEN') as naive
        from unnest(@cases)'''
    job=client.query(sql,job_config=config);rows=[dict(row) for row in job.result()]
    _require(len(rows)==len(fixtures) and len({row['case_id'] for row in rows})==len(fixtures),'Boundary coverage mismatch')
    for row in rows:
        _require((row['actual'] is None)==(row['expected'] is None) and
            (row['actual'] is None or policy.fraction(row['actual'])==policy.fraction(row['expected'])),
            'Native exact precision mismatch: '+row['case_id'])
    naive_errors=[row['case_id'] for row in rows if row['actual']!=row['naive']]
    _require('double-above' in naive_errors and 'double--above' in naive_errors,'Double-rounding contrast not reproduced')
    # Canonical parents, exact addition and a denominator rounded to zero.
    chain_job=client.query(f'''with q as (select cast(`{routine}`('1','3') as bignumeric) as third,
        `{routine}`('1e-38','1') as tiny)
        select third,third+third+third as three_thirds,
        cast(`{routine}`(cast(third as string),'2') as bignumeric) as half_third,
        `{routine}`('1',tiny) as zero_parent_division from q''')
    chain=dict(next(iter(chain_job.result())))
    _require(chain['third']==policy.fraction('0.333333333333333333')
        and chain['three_thirds']==policy.fraction('0.999999999999999999')
        and chain['half_third']==policy.fraction('0.166666666666666666')
        and chain['zero_parent_division'] is None,'Canonical parent/zero propagation mismatch')
    rejected=[]
    for n,d in (('1e38','1e-38'),('-1e38','1e-38')):
        query=f"select cast(`{routine}`(@n,@d) as bignumeric) as out_of_range"
        config=bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter('n','STRING',n),
            bigquery.ScalarQueryParameter('d','STRING',d)])
        try:client.query(query,job_config=config).result()
        except BadRequest as error:
            _require('BIGNUMERIC' in str(error).upper(),'Unexpected overflow probe failure')
            rejected.append(dict(numerator=n,denominator=d,error=str(error)))
        else:raise AssertionError('Out-of-range canonical result was silently accepted')
    result=dict(status='passed',precision_version=policy.VERSION,implementation_approved=True,
        calculation_receipt_sha256=pin,source_code_hash=receipt['bindings']['code_hash'],oracle_sha256=file_hash(policy.__file__),
        fixtures_sha256=file_hash(output/'fixtures.json'),routine=receipt['dbt']['precision_routine'],
        job_id=job.job_id,cases=len(rows),mismatches=0,naive_double_rounding_errors=naive_errors,
        chain_job_id=chain_job.job_id,chain=chain,rejected_overflows=rejected,
        precision_release_activated=False,publication_eligible=False)
    (output/'native_results.json').write_text(json.dumps(rows,default=str,indent=2))
    result['native_results_sha256']=file_hash(output/'native_results.json')
    (output/'validation_receipt.json').write_text(json.dumps(result,default=str,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for field in ('calculation','receipt-sha256','output-dir','project'):parser.add_argument('--'+field,required=True)
    args=parser.parse_args();print(json.dumps(validate(args.calculation,args.receipt_sha256,args.output_dir,project=args.project),default=str,indent=2))


if __name__=='__main__':main()
