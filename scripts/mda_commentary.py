"""
mda_commentary.py — LLM-based MD&A commentary generation

Replaces the old regex/keyword-search approach that used to live in
credit_memo_writer.py (_METRIC_SYNONYMS / _CAUSAL_RE / _mda_snippet()).

Why: a human credit analyst reads the whole MD&A once and forms a judgment
about why each line item moved — that's semantic understanding + causal
reasoning, not "find a sentence containing this keyword near causal-sounding
words". This module reads the (already-cleaned) MD&A text once per report
and asks the model to do the same thing for every metric the memo needs, in
a single call — not a regex search per metric.

No embedding/retrieval step: the MD&A text (capped at 80,000 chars by
agent_runner.py's _html_to_text()) already fits in any current model's
context window, so there's nothing to retrieve — the whole thing is handed
to the model directly.

No fallback: this module is called from agent_runner.py, not from
credit_memo_writer.py (which stays a pure formatter with zero external
dependencies). If the API call fails — no credentials, network error,
safety refusal — this raises. The caller decides what that means for the
report; it is not silently downgraded to a worse-quality regex match.
"""

from __future__ import annotations

import json
import logging

import anthropic

logger = logging.getLogger(__name__)

MODEL = "claude-opus-5"

# metric key -> what the model should explain for it. Keys match the
# `commentary` dict keys credit_memo_writer.py's Part-2/3 commentary
# functions look up (see _cm() there).
_METRICS: dict[str, str] = {
    "revenue":          "why total revenue increased or decreased",
    "gross_profit":      "why gross margin increased or decreased",
    "operating_income":  "why operating margin increased or decreased",
    "interest_expense":  "why interest expense increased or decreased",
    "pre_tax":           "why pre-tax margin increased or decreased",
    "current_assets":    "why the current ratio / short-term liquidity changed",
    "inventory":         "why the quick ratio changed, focusing on inventory",
    "total_debt":        "why total debt increased or decreased",
    "ebitda":            "why LTM EBITDA increased or decreased",
    "leverage":          "why the total leverage ratio tightened or improved",
    "operating_cash":    "why the cash flow ratio / operating cash flow changed",
    "debt_service":      "why debt service / debt service coverage changed",
    "guidance":          "full-year revenue and EBITDA guidance and, for a Q2 or Q3 filing, YTD achievement versus the guidance lower bound, midpoint, and upper bound; state Not disclosed if guidance is unavailable",
}

ALL_METRICS: list[str] = list(_METRICS.keys())


def generate_commentary(
    filing_text: str,
    metrics: list[str],
    company_name: str,
    period_label: str,
) -> dict[str, str]:
    """
    Read `filing_text` (cleaned MD&A excerpt) once and return a one-to-two
    sentence, analyst-style causal explanation for each requested metric key.

    Args:
        filing_text:  cleaned MD&A text (see agent_runner.py _html_to_text())
        metrics:      subset of ALL_METRICS to explain
        company_name: for context in the prompt
        period_label: e.g. "10-K 2026-02-06" — for context in the prompt

    Returns:
        {metric_key: explanation}. A metric the filing genuinely doesn't
        explain gets a short "not addressed in this filing"-type string
        instead of a fabricated reason — the model is instructed not to
        invent one.

    Raises on any failure — no fallback. Missing/invalid API credentials,
    a network error, or a safety refusal all propagate to the caller.
    """
    if not filing_text:
        raise ValueError("generate_commentary: filing_text is empty")

    unknown = set(metrics) - set(_METRICS)
    if unknown:
        raise ValueError(f"generate_commentary: unknown metric keys: {sorted(unknown)}")
    if not metrics:
        return {}

    schema_props = {
        key: {"type": "string", "description": _METRICS[key]}
        for key in metrics
    }

    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": schema_props,
                    "required": metrics,
                    "additionalProperties": False,
                },
            }
        },
        system=(
            "You are a credit analyst writing the commentary section of a bank "
            "credit memo. Read the MD&A excerpt below the way an analyst would "
            "— once, in full — then explain WHY each requested financial metric "
            "moved. Ground every explanation in what the filing actually says. "
            "One or two sentences per metric, written like a human analyst's "
            "note, not a copy-pasted quote. If the filing does not explain a "
            "metric's movement, say so plainly (e.g. 'Not separately addressed "
            "in this filing.') instead of inventing a reason."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Company: {company_name}\n"
                    f"Filing: {period_label}\n\n"
                    f"MD&A excerpt:\n{filing_text}"
                ),
            }
        ],
    )

    if response.stop_reason == "refusal":
        raise RuntimeError(
            f"generate_commentary: model refused ({response.stop_details})"
        )

    text_block = next(b for b in response.content if b.type == "text")
    result = json.loads(text_block.text)

    logger.info(
        f"generate_commentary: {len(result)} metrics explained "
        f"({response.usage.input_tokens} in / {response.usage.output_tokens} out tokens)"
    )
    return result
