"""Block 2: exact-period source selection and auditable structured supplements.

This produces source inputs, not a calculated/narrated/rendered credit assessment.
No latest-version, alternate-tag priority, missing-to-zero or currency conversion.
See references/loan-review-source-inputs.md for schemas, rollout and test boundaries.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import date
from decimal import Decimal, Inexact, InvalidOperation, localcontext
from pathlib import Path

try:
    from .loan_review_contract import Evidence, Period, METRICS, empty_report, validate_report
except ImportError:
    from loan_review_contract import Evidence, Period, METRICS, empty_report, validate_report


class SourceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise SourceError(message)


def number(value):
    require(not isinstance(value, bool) and value is not None, "Numeric value must be explicit, not bool/null")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise SourceError("Invalid decimal source value") from None
    require(result.is_finite(), "Non-finite source value")
    return result


def normalize_value(value, source_scale, target_scale):
    """Normalize units without silently rounding original financial facts."""
    values = tuple(number(v) for v in (value, source_scale, target_scale))
    try:
        with localcontext() as context:
            context.prec = max(50, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in values) + 10)
            context.traps[Inexact] = True
            return values[0] * values[1] / values[2]
    except Inexact:
        raise SourceError("Monetary scale requires inexact normalization; choose an exact decimal scale") from None


def day(value):
    if type(value) is date:
        return value
    try:
        require(isinstance(value, str), "ISO date required")
        return date.fromisoformat(value)
    except ValueError:
        raise SourceError(f"Invalid ISO date: {value!r}") from None


def text(value):
    return isinstance(value, str) and bool(value.strip())


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load_json(path):
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, f"Duplicate JSON key: {key}")
            out[key] = value
        return out
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_float=Decimal,
                      object_pairs_hook=unique_pairs)


# Only direct statement concepts are mapped. Unknown debt/net-worth/quick-asset
# definitions require reviewed supplements; no stockholders-equity proxy is chosen.
SEC_FIELDS = {
    "revenue": ("revenue", "revenue_alt"),
    "cost_of_revenue": ("cost_of_revenue", "cost_of_revenue_alt"),
    "gross_profit": ("gross_profit",),
    "operating_income": ("operating_income",),
    "operating_expense": ("operating_expense_direct",),
    "interest_expense": ("interest_expense", "interest_expense_alt"),
    "pretax_profit": ("income_before_tax",),
    "income_tax": ("income_tax_expense",),
    "net_income": ("net_income",),
    "beginning_cash": ("cash",), "ending_cash": ("cash",),
    "cfo": ("cfo",), "cfi": ("cfi",), "cff": ("cff",),
    "current_assets": ("current_assets",), "current_liabilities": ("current_liabilities",),
    "total_liabilities": ("total_liabilities",),
    "capitalized_interest": ("capitalized_interest",), "da": ("da",),
}


def parse_request(payload):
    """Parse an explicit fiscal calendar; the contract validates its structure."""
    fields = {"schema_version", "mode", "entity", "cik", "scope", "currency", "scale", "as_of", "periods", "evidence"}
    require(isinstance(payload, dict) and set(payload) == fields, "Source request fields do not match schema v1")
    require(payload["schema_version"] == 1, "Unsupported source request version")
    require(isinstance(payload["cik"], str) and len(payload["cik"]) == 10 and payload["cik"].isdigit(), "10-digit CIK required")
    as_of = day(payload["as_of"])
    evidence = {}
    require(isinstance(payload["evidence"], list), "Evidence must be a list")
    for index, raw in enumerate(payload["evidence"]):
        require(isinstance(raw, dict), f"evidence[{index}]: object required")
        require(set(raw) == {"id", "entity", "scope", "source_id", "version", "document_date", "locator", "kind", "period_roles", "content", "purpose"}, "Calendar evidence fields do not match schema")
        require(all(isinstance(raw[k], str) for k in ("id", "entity", "scope", "source_id", "version", "locator", "kind", "content", "purpose")), f"evidence[{index}]: string fields required")
        require(isinstance(raw["period_roles"], list) and all(text(v) for v in raw["period_roles"]), f"evidence[{index}].period_roles: string list required")
        e = Evidence(**{**raw, "document_date": day(raw["document_date"]), "period_roles": tuple(raw["period_roles"])})
        require(e.id not in evidence, "Duplicate calendar evidence ID")
        require(e.document_date <= as_of, "Calendar evidence is later than review as_of")
        require(e.kind == "calendar", "Request evidence must document the fiscal calendar")
        evidence[e.id] = e
    periods = []
    require(isinstance(payload["periods"], list), "Periods must be a list")
    for index, raw in enumerate(payload["periods"]):
        require(isinstance(raw, dict), f"periods[{index}]: object required")
        require(set(raw) == {"role", "label", "fiscal_year", "start", "end", "ltm_start", "evidence_ids", "quarter", "reason"}, "Period fields do not match schema")
        require(all(isinstance(raw[k], str) for k in ("role", "label", "reason")), f"periods[{index}]: string fields required")
        require(type(raw["fiscal_year"]) is int and (raw["quarter"] is None or type(raw["quarter"]) is int), f"periods[{index}]: integer year/quarter required")
        require(isinstance(raw["evidence_ids"], list) and all(text(v) for v in raw["evidence_ids"]), f"periods[{index}].evidence_ids: string list required")
        p = Period(**{**raw, **{k: day(raw[k]) if raw[k] is not None else None for k in ("start", "end", "ltm_start")}, "evidence_ids": tuple(raw["evidence_ids"])})
        require(p.end is None or p.end <= as_of, "Requested period ends after as_of")
        periods.append(p)
    report = empty_report(payload["mode"], entity=payload["entity"], scope=payload["scope"],
                          currency=payload["currency"], scale=number(payload["scale"]),
                          periods=tuple(periods), evidence=evidence)
    validate_report(report, expected_mode=payload["mode"])
    return report, payload["cik"], as_of


def validate_sec_rows(rows, *, entity, cik):
    """Reject mixed entities and untraceable legacy rows; never synthesize lineage."""
    candidates = {}
    require(isinstance(rows, (list, tuple)), "SEC facts: list required")
    for index, raw in enumerate(rows):
        require(isinstance(raw, dict), f"SEC facts[{index}]: object required")
        row = dict(raw)
        require(row.get("ticker") == entity and row.get("cik") == cik, "Mixed or missing borrower/CIK in SEC facts")
        required = ("fact_id", "scope", "field_name", "namespace", "xbrl_tag", "unit", "period_kind",
                    "accession_number", "source_version", "source_url", "document_url", "source_locator")
        require(all(text(row.get(k)) for k in required), "SEC fact lacks traceable identity/version/unit/locator; migrate legacy rows explicitly or ingest into a clean dataset")
        require(row["scope"] == "entity-wide" and row["namespace"] == "us-gaap", "Unexpected SEC scope/taxonomy")
        start = day(row["period_start"]) if row.get("period_start") is not None else None
        end, filed = day(row.get("period_end")), day(row.get("filed_date"))
        require(row["period_kind"] in ("instant", "duration"), "Invalid SEC period kind")
        require((start is None) if row["period_kind"] == "instant" else (start is not None and start <= end), "Invalid SEC fact interval")
        require("original_value" in row, "Original source value missing")
        value = number(row["original_value"]) if row["original_value"] is not None else None
        # Hash all audit fields/value. Repeated ingestion cannot overwrite a version.
        identity = {k: str(row[k]) if type(row.get(k)) is date else row.get(k) for k in
                    ("ticker", "cik", "scope", "field_name", "namespace", "xbrl_tag", "unit", "period_kind",
                     "period_start", "period_end", "filing_type", "accession_number", "filed_date", "original_value",
                     "source_locator", "filing_fiscal_year", "filing_fiscal_period")}
        expected = "sec:" + hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        require(row["fact_id"] == expected, "SEC fact ID does not match source identity/value")
        item = {
            "id": row["fact_id"], "origin": "sec", "entity": entity, "cik": cik,
            "scope": row["scope"], "field_name": row["field_name"], "metric": None,
            "unit": row["unit"], "scale": "1", "period_kind": row["period_kind"],
            "start": start.isoformat() if start else None, "end": end.isoformat(),
            "status": "sourced" if value is not None else "missing",
            "value": str(value) if value is not None else None,
            "source_id": row["accession_number"], "version": row["source_version"],
            "document_date": filed.isoformat(), "source_url": row["source_url"],
            "document_url": row["document_url"], "locator": row["source_locator"],
            "namespace": row["namespace"], "tag": row["xbrl_tag"],
            "definition": row["xbrl_tag"], "basis": "", "reason": "" if value is not None else "SEC entry has no numeric value",
        }
        require(item["id"] not in candidates or candidates[item["id"]] == item, "Duplicate SEC fact ID with different metadata")
        candidates[item["id"]] = item
    return candidates


def parse_supplement(payload, *, entity, cik, scope):
    """Accept reviewed structured evidence, never an arbitrary historical workbook.

    Review metadata is an audit assertion; authenticity must be checked against the
    supplied document by the reviewer. JSON content never becomes instructions.
    """
    require(isinstance(payload, dict) and set(payload) == {"schema_version", "entity", "cik", "scope", "purpose", "records"}, "Supplement envelope fields do not match schema")
    require(payload["schema_version"] == 1, "Unsupported supplement version")
    require((payload["entity"], payload["cik"], payload["scope"]) == (entity, cik, scope), "Supplement borrower/CIK/scope mismatch")
    require(payload["purpose"] == "current_borrower_evidence", "Historical/style/sample evidence is forbidden")
    require(isinstance(payload["records"], list), "Supplement records must be a list")
    result = {}
    fields = {"metric", "period_kind", "start", "end", "unit", "scale", "value", "status", "reason", "definition", "basis", "source_id", "version", "document_date", "source_uri", "locator", "excerpt", "verification"}
    for raw in payload["records"]:
        require(isinstance(raw, dict) and set(raw) == fields, "Supplement record fields do not match schema")
        require(isinstance(raw["basis"], str) and isinstance(raw["reason"], str), "Supplement basis/reason must be strings")
        metric = raw["metric"]
        require(text(metric) and metric in METRICS, "Unknown supplemental metric")
        require(raw["status"] in ("sourced", "not_disclosed", "not_applicable"), "Invalid supplemental disclosure status")
        require(all(text(raw[k]) for k in ("definition", "source_id", "version", "source_uri", "locator", "excerpt")), "Supplement document identity/definition/locator/excerpt required")
        check = raw["verification"]
        require(isinstance(check, dict) and set(check) == {"verified_by", "verified_at", "method"}, "Explicit verification record required")
        require(text(check["verified_by"]) and check["method"] == "checked_against_source", "Source verification required")
        verified = day(check["verified_at"])
        filed = day(raw["document_date"])
        require(verified >= filed, "Verification predates document")
        start = day(raw["start"]) if raw["start"] is not None else None
        end = day(raw["end"])
        kind = "instant" if METRICS[metric].period_kind in ("instant", "opening") else "duration"
        require(raw["period_kind"] == kind, "Supplement metric period kind mismatch")
        require(start is None if kind == "instant" else start is not None and start <= end, "Invalid supplement interval")
        scale = number(raw["scale"])
        require(scale > 0, "Supplement scale must be positive")
        expected_unit = METRICS[metric].unit
        require(text(raw["unit"]), "Explicit supplemental unit required")
        if expected_unit != "money":
            require(raw["unit"] == expected_unit and scale == 1, "Non-monetary supplemental unit/scale mismatch")
        value = raw["value"]
        if raw["status"] == "sourced":
            if expected_unit == "text":
                require(text(value), "Source basis text required")
            else:
                value = str(number(value))
            if metric in ("ltm_ebitda", "ebitda_basis", "total_leverage"):
                require(text(raw["basis"]), "Source EBITDA basis required")
        else:
            require(value is None and text(raw["reason"]), "Absent/not-applicable disclosure requires null and explicit reviewed scope/reason")
        item = {**raw, "id": "supp:" + digest(raw), "origin": "supplement", "entity": entity,
                "cik": cik, "scope": scope, "field_name": None, "value": value, "scale": str(scale),
                "start": start.isoformat() if start else None, "end": end.isoformat(),
                "document_date": filed.isoformat(), "source_url": raw["source_uri"], "document_url": raw["source_uri"]}
        result[item["id"]] = item
    return result


def prepare_source_inputs(request_payload, sec_rows, supplements=()):
    report, cik, as_of = parse_request(request_payload)
    candidates = validate_sec_rows(sec_rows, entity=report.entity, cik=cik)
    for payload in supplements:
        candidates.update(parse_supplement(payload, entity=report.entity, cik=cik, scope=report.scope))
    eligible = {key: c for key, c in candidates.items() if day(c["document_date"]) <= as_of}
    excluded = {key: "Document version is later than explicit as_of" for key in candidates if key not in eligible}
    inputs = {}

    def select(key, metric, role, start, end, unit):
        fields = SEC_FIELDS.get(metric, ())
        matches = [c for c in eligible.values() if c["scope"] == report.scope
                   and c["start"] == (start.isoformat() if start else None)
                   and c["end"] == (end.isoformat() if end else None)
                   and (c["metric"] == metric or c["origin"] == "sec" and c["field_name"] in fields)]
        expected_unit = report.currency if unit == "money" else unit
        matching_units = [c for c in matches if c["unit"] == expected_unit]
        item = {"metric": metric, "period_role": role, "start": start, "end": end,
                "unit": unit, "currency": report.currency if unit == "money" else None,
                "scale": str(report.scale if unit == "money" else Decimal(1)),
                "definition": METRICS[metric].definition, "pending_decisions": METRICS[metric].pending,
                "period_kind": "instant" if METRICS[metric].period_kind in ("instant", "opening") else "duration",
                "candidate_ids": sorted(c["id"] for c in matches), "evidence_ids": [],
                "status": "missing", "value": None, "basis": "", "reason": "No matching source in the reviewed inputs; not a claim of non-disclosure"}
        if (start is None and METRICS[metric].period_kind not in ("instant", "opening")) or end is None:
            item["reason"] = "Required fiscal dates unavailable"
        elif matches and len(matching_units) != len(matches):
            item.update(status="conflict", reason="Incompatible units; no implicit currency conversion or unit selection")
        elif matching_units:
            signatures = set()
            for c in matching_units:
                value = c["value"]
                if value is not None and unit != "text":
                    value = normalize_value(value, c["scale"], report.scale if unit == "money" else Decimal(1))
                # Multiple bases must not become an apparent operating movement.
                signatures.add((c["status"], value, c["basis"], c["definition"]))
            if len(signatures) != 1:
                item.update(status="conflict", reason="Sources/versions/definitions disagree; no approved selection policy applied")
            else:
                status, value, basis, _ = signatures.pop()
                item.update(status=status, value=str(value) if value is not None and unit != "text" else value,
                            basis=basis, evidence_ids=sorted(c["id"] for c in matching_units),
                            reason="All matching sources retained; no version silently preferred" if status == "sourced" else matching_units[0]["reason"])
        inputs[key] = item

    for key, f in report.facts.items():
        if ":pct:" in key or METRICS[f.metric].formula:
            inputs[key] = {"metric": f.metric, "period_role": f.period_role, "start": f.start, "end": f.end,
                           "unit": f.unit, "currency": f.currency, "scale": str(report.scale if f.unit == "money" else 1),
                           "definition": f.definition, "pending_decisions": METRICS[f.metric].pending,
                           "period_kind": f.period_kind,
                           "status": "not_calculable", "value": None, "basis": "",
                           "candidate_ids": [], "evidence_ids": [], "reason": "Calculation belongs to Block 3; no inferred value"}
        else:
            select(key, f.metric, f.period_role, f.start, f.end, f.unit)
    # Required ratio/EBITDA inputs also exist when absent. Never manufacture zero.
    for p in report.periods:
        for metric in ("capitalized_interest", "da", "current_assets", "current_liabilities", "quick_assets", "net_worth", "total_liabilities"):
            spec = METRICS[metric]
            select(f"input:{metric}:{p.role}", metric, p.role, None if spec.period_kind == "instant" else p.start, p.end, spec.unit)
    return {
        "schema_version": 1, "stage": "source_inputs_only", "mode": report.mode.value,
        "entity": report.entity, "cik": cik, "scope": report.scope, "as_of": as_of.isoformat(),
        "request": request_payload, "inputs": inputs, "evidence": candidates,
        "excluded": excluded, "conflict_count": sum(i["status"] == "conflict" for i in inputs.values()),
        "final_report_accepted": False,
    }


def source_signature(candidate: dict) -> tuple:
    """Exact equivalence, independent of filing/version and display rounding."""
    value = candidate["value"]
    if value is not None and candidate["unit"] != "text":
        value = normalize_value(value, candidate["scale"], 1)
    return (candidate["entity"], candidate["cik"], candidate["scope"],
            candidate["period_kind"], candidate["start"], candidate["end"],
            candidate["unit"], candidate["definition"], candidate["basis"],
            candidate["status"], value)


def prepare_legacy_source_inputs(rows: list[dict], *, entity: str) -> dict:
    """Collapse verified equivalents for legacy reads, retaining every evidence ID.

    SEC observations use base units (scale 1). Missing audit identity, different
    definitions/currencies/scopes or unequal original decimals cannot be selected.
    A representative only supplies transport metadata after equivalence is proven;
    its filing date never decides which financial value is accepted.
    """
    statements = ("income_statement", "balance_sheet", "cash_flow")
    if not rows:
        return {"statements": {s: [] for s in statements}, "evidence": {},
                "adoptions": [], "collapsed": False}
    require(all(isinstance(r, dict) for r in rows), "Legacy source rows must be objects")
    ciks = {r.get("cik") for r in rows if text(r.get("cik"))}
    require(len(ciks) == 1, "Legacy source CIK missing or conflicting")
    evidence = validate_sec_rows(rows, entity=entity, cik=next(iter(ciks)))
    aliases = {field: metric for metric, fields in SEC_FIELDS.items() for field in fields}
    groups = {}
    for row in rows:
        statement = row.get("statement_type")
        require(statement in statements, "Legacy source statement identity missing")
        c = evidence[row["fact_id"]]
        # Alias fields used together by legacy SUM/COALESCE must also be checked.
        key = (statement, aliases.get(c["field_name"], c["field_name"]), c["start"], c["end"])
        groups.setdefault(key, []).append(row)
    selected = {s: [] for s in statements}
    adoptions = []
    for key, group in sorted(groups.items(), key=lambda item: str(item[0])):
        candidates = [evidence[r["fact_id"]] for r in group]
        require(len({source_signature(c) for c in candidates}) == 1,
                f"Legacy source conflict or unconfirmed equivalence: {key}")
        c = candidates[0]
        # Legacy reports are USD-based; no implicit conversion is introduced here.
        require(c["unit"] == ("USD/shares" if c["field_name"].startswith("eps_") else "USD"),
                f"Legacy source unit is unsupported: {key}")
        require(all(r.get("filing_type") in ("10-K", "10-K/A", "10-Q", "10-Q/A") for r in group),
                f"Legacy source filing form is unconfirmed: {key}")
        representative = dict(min(group, key=lambda r: r["fact_id"]))
        c = evidence[representative["fact_id"]]
        representative["period_days"] = (day(c["end"]) - day(c["start"])).days if c["start"] else None
        ids = sorted({r["fact_id"] for r in group})
        forms = sorted({r["filing_type"].removesuffix("/A") for r in group})
        representative.update(value=c["value"], source_forms=forms, evidence_ids=ids)
        selected[key[0]].append(representative)
        adoptions.append({"statement_type": key[0], "metric": key[1],
                          "start": c["start"], "end": c["end"],
                          "value": c["value"], "unit": c["unit"], "status": c["status"],
                          "definition": c["definition"], "evidence_ids": ids,
                          "representative_id": representative["fact_id"], "source_forms": forms})
    return {"statements": selected, "evidence": evidence, "adoptions": adoptions,
            "collapsed": sum(map(len, selected.values())) < len(rows)}


def write_source_bundle(bundle: dict, path: str | Path) -> Path:
    """Publish a complete snapshot in a unique run directory; return its actual path.

    A failed write never replaces an earlier run. Temporary bytes are not exposed
    at the returned JSON filename until flush/fsync and atomic rename complete.
    """
    path = Path(path)
    serialized = json.dumps(bundle, indent=2, ensure_ascii=False, default=str) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix=f"{path.stem}-", dir=path.parent))
    destination = run_dir / path.name
    temporary = run_dir / ".pending"
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except OSError:
        try:
            temporary.unlink(missing_ok=True)
            run_dir.rmdir()
        except OSError:
            pass  # Preserve the original write error; no completed path is returned.
        raise
    return destination
