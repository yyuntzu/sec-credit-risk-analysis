from copy import deepcopy
from decimal import localcontext,ROUND_DOWN
from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import unittest

from scripts import precision_policy as policy
from scripts.dbt_shadow import prepare_run
from test_dbt_shadow import rich_bundle

ROOT=Path(__file__).resolve().parents[1]
NODE=Path('/Users/yuntzuyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')


def javascript(cases):
    macro=(ROOT/'references/dbt/macros/shadow_precision.sql').read_text()
    body=macro.split('{% macro shadow_precision_body() -%}',1)[1].split('{%- endmacro %}',1)[0]
    command='const fs=require("fs");const divide=new Function("numerator","denominator",'+json.dumps(body)+');'+\
        'process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,"utf8")).map(x=>divide(...x))));'
    result=subprocess.run([str(NODE),'-e',command],input=json.dumps(cases),capture_output=True,text=True,check=True,timeout=30)
    return json.loads(result.stdout)


class PrecisionPolicyTests(unittest.TestCase):
    def test_hand_calculated_signed_ties_and_tiny_values(self):
        for value,expected in (('0.0000000000000000005','0'),('0.0000000000000000015','0.000000000000000002'),
                ('0.0000000000000000025','0.000000000000000002'),('0.0000000000000000035','0.000000000000000004')):
            for sign in ('','-'):
                self.assertEqual(policy.q18(policy.fraction(sign+value)),policy.fraction(sign+expected))
        self.assertEqual(policy.formula_value('CF-01',['1e-38','1']),0)
        self.assertEqual(policy.formula_value('CF-01',['1','0']),None)
        self.assertEqual(policy.formula_value('CF-16',['1e-38','0']),Fraction(1,10**38))

    def test_exact_string_division_matches_independent_fraction_oracle(self):
        cases=[['1','3'],['-2','3'],['1e38','1'],['1e-38','1'],['1','-3'],['0','0'],[None,'1'],['1',None]]
        for sign in ('','-'):
            for tail in ('00000000000000000001','00000000000000000000'):
                cases.append([sign+'50000000000000000000.'+tail,'1e38'])
            cases.extend([[sign+'0.0000000000000000015','1'],[sign+'0.0000000000000000025','1']])
        rng=random.Random(20261111)
        for _ in range(500):
            n=Fraction(rng.randint(-10**35,10**35),10**rng.randint(0,38))
            d=Fraction(rng.randint(1,10**35),10**rng.randint(0,38))
            if policy.MINIMUM<=n/d<=policy.MAXIMUM:cases.append([policy.decimal_string(n),policy.decimal_string(d)])
        actual=javascript(cases)
        for pair,found in zip(cases,actual):
            expected=None if None in pair or policy.fraction(pair[1])==0 else policy.q18(policy.fraction(pair[0])/policy.fraction(pair[1]))
            self.assertEqual(None if found is None else policy.fraction(found),expected,pair)

    def test_double_rounding_counterexample_and_negative_counterpart(self):
        for sign in (1,-1):
            exact=sign*Fraction(5000000000000000000000000000000000000001,10**20)/10**38
            rounded_38=Fraction(sign*5,10**19)
            self.assertNotEqual(policy.q18(exact),policy.q18(rounded_38))
            found=javascript([[( '-' if sign<0 else '')+'50000000000000000000.00000000000000000001','1e38']])[0]
            self.assertEqual(policy.fraction(found),policy.q18(exact))

    def test_canonical_reference_uses_rounded_parents_and_ignores_decimal_context(self):
        baseline=dict(facts={
            'a':dict(status='sourced',value='1'), 'b':dict(status='sourced',value='3'),
            'ratio':dict(status='calculated',formula_id='CF-01',input_ids=['a','b'],value='legacy'),
            'sum':dict(status='calculated',formula_id='DER-05',input_ids=['ratio','ratio'],value='legacy')})
        with localcontext() as context:
            context.prec=2;context.rounding=ROUND_DOWN
            reference=policy.canonical_baseline(baseline)
        self.assertEqual(reference['facts']['ratio']['value'],'0.333333333333333333')
        self.assertEqual(reference['facts']['sum']['value'],'0.666666666666666666')
        self.assertEqual(baseline['facts']['ratio']['value'],'legacy')

    def test_all_formula_kernels_follow_new_policy_and_range_failures_are_errors(self):
        cases=json.loads((ROOT/'tests/fixtures/dbt_shadow/kernel_cases.json').read_text())
        for case in cases:
            expected=policy.formula_value(case['formula_id'],case['values'])
            self.assertEqual(expected,None if case['expected'] is None else policy.fraction(case['expected']),case['case_id'])
        for formula,values in (('CF-01',['1e38','1e-38']),('DER-05',['5e38','5e38']),('CF-16',['1e-39','0'])):
            with self.assertRaises(ValueError):policy.formula_value(formula,values)

    def test_reference_retains_sources_and_rejects_wrong_result_or_audit(self):
        _,_,baseline,_=prepare_run(rich_bundle())
        reference=policy.canonical_baseline(baseline)
        source=next(fid for fid,fact in baseline['facts'].items() if fact['status']=='sourced' and fact['unit']=='money')
        self.assertEqual(reference['facts'][source],baseline['facts'][source])
        fact=next(f for f in reference['facts'].values() if f['status']=='calculated' and f['formula_id'] in policy.DIVISIONS)
        bad=dict(fact_id=fact['id'],value=fact['value'],precision_audit='{}')
        self.assertEqual(policy.verify_audits(reference,[bad])['mismatches'],1)

    def test_commentary_growth_is_rounded_from_exact_endpoints(self):
        original=dict(before='3',after='4',growth='0.3333333333333333333333333333')
        self.assertEqual(policy.canonical_commentary(original)['growth'],'0.333333333333333333')
        self.assertEqual(original['growth'],'0.3333333333333333333333333333')
