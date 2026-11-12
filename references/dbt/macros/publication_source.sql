{% macro publication_raw_bundle_body() -%}
// Preserve the exact canonical subdocument bytes; JSON.parse/stringify would
// change object ordering, escaped characters or numeric lexical precision.
if (payload === null || !payload.startsWith('{"bundle": ')) return null;
var start='{"bundle": '.length;
if (payload[start]!=='{') return null;
var depth=0,quoted=false,escaped=false;
for(var i=start;i<payload.length;i++) {
  var c=payload[i];
  if(quoted) {
    if(escaped) escaped=false;
    else if(c==='\\') escaped=true;
    else if(c==='"') quoted=false;
  } else {
    if(c==='"') quoted=true;
    else if(c==='{' || c==='[') depth++;
    else if(c==='}' || c===']') {
      depth--;if(depth===0) return payload.slice(start,i+1);
    }
  }
}
return null;
{%- endmacro %}

{% macro publication_raw_bundle_ddl() -%}
create or replace function `{{ target.project }}.{{ target.schema }}.publication_raw_bundle_v1`
(payload string) returns string deterministic language js as r"""
{{ publication_raw_bundle_body() }}
"""
{%- endmacro %}
