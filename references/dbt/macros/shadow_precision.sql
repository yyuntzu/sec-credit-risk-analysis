{% macro shadow_precision_body() -%}
// Integer decimal strings only. Number is used for single digits, never amounts.
if (numerator === null || denominator === null) return null;
function strip(s) { return s.replace(/^0+/, '') || '0'; }
function cmp(a,b) { return a.length !== b.length ? (a.length>b.length?1:-1) : (a===b?0:(a>b?1:-1)); }
function sub(a,b) {
  var out='', borrow=0, j=b.length-1;
  for (var i=a.length-1;i>=0;i--,j--) {
    var digit=Number(a[i])-(j>=0?Number(b[j]):0)-borrow;
    borrow=digit<0?1:0; out=String(digit+10*borrow)+out;
  }
  if (borrow) throw Error('negative unsigned subtraction');
  return strip(out);
}
function inc(s) {
  var out='', carry=1;
  for (var i=s.length-1;i>=0;i--) {
    var digit=Number(s[i])+carry;carry=digit===10?1:0;out=String(digit%10)+out;
  }
  return (carry?'1':'')+out;
}
function decimal(s) {
  var match=/^([+-]?)([0-9]+)(?:\.([0-9]*))?(?:[eE]([+-]?[0-9]+))?$/.exec(s);
  if (!match || s.length>200) throw Error('invalid decimal operand');
  var exponent=Number(match[4]||'0');
  if (Math.abs(exponent)>100) throw Error('decimal exponent out of bounds');
  return {negative:match[1]==='-',digits:strip(match[2]+(match[3]||'')),scale:(match[3]||'').length-exponent};
}
var a=decimal(numerator), b=decimal(denominator);
if (b.digits==='0') return null;
if (a.digits==='0') return '0';
var shift=18+b.scale-a.scale;
var n=a.digits+'0'.repeat(Math.max(shift,0)), d=b.digits+'0'.repeat(Math.max(-shift,0));
var remainder='0', quotient='';
for (var pos=0;pos<n.length;pos++) {
  remainder=strip(remainder+n[pos]);var digit=0;
  while (cmp(remainder,d)>=0) { remainder=sub(remainder,d);digit++; }
  quotient+=String(digit);
}
quotient=strip(quotient);
// Compare 2*remainder with divisor without a machine-sized integer conversion.
var half=cmp(remainder,sub(d,remainder));
if (half>0 || (half===0 && Number(quotient[quotient.length-1])%2===1)) quotient=inc(quotient);
if (quotient==='0') return '0';
quotient=quotient.padStart(19,'0');
return (a.negative!==b.negative?'-':'')+quotient.slice(0,-18)+'.'+quotient.slice(-18);
{%- endmacro %}

{% macro shadow_precision_ddl() -%}
create or replace function `{{ target.project }}.{{ target.schema }}.review_divide_q18_v1`
(numerator string, denominator string) returns string deterministic language js as r"""
{{ shadow_precision_body() }}
"""
{%- endmacro %}

{% macro shadow_division_operands(id, values) -%}
struct(
 case {{ id }}
 when 'CF-04' then {{ values }}[safe_offset(0)]+{{ values }}[safe_offset(1)]
 when 'CF-05' then {{ values }}[safe_offset(0)]+{{ values }}[safe_offset(1)]+{{ values }}[safe_offset(2)]
 when 'CF-09' then {{ values }}[safe_offset(0)]-{{ values }}[safe_offset(1)]
 else {{ values }}[safe_offset(0)] end as numerator,
 case {{ id }}
 when 'CF-04' then {{ values }}[safe_offset(1)]+{{ values }}[safe_offset(2)]
 when 'CF-05' then {{ values }}[safe_offset(1)]+{{ values }}[safe_offset(3)]
 else {{ values }}[safe_offset(1)] end as denominator)
{%- endmacro %}
