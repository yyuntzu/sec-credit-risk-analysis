"""Isolated synthetic fixtures. Never load these records into borrower reports.

Contract assertions only: these are not arithmetic or end-to-end acceptance tests.
Expected layouts/periods below are independently transcribed from acceptance v1.0.
"""
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
import unittest

from scripts.loan_review_contract import (
    ContractError, Evidence, Fact, Mode, Narrative, Period, Status,
    empty_report, report_layout, validate_report,
)


def fixture(mode="annual"):
    if mode == "annual":
        periods = tuple(Period(role, f"FY{year}", year, date(year, 1, 1),
                               date(year, 12, 31), date(year, 1, 1), ("calendar",))
                        for role, year in zip(
                            ("fy_t_minus_3", "fy_t_minus_2", "fy_t_minus_1", "fy_t"),
                            (2022, 2023, 2024, 2025)))
    else:
        periods = (
            Period("earlier_fy_end", "FY2023", 2023, date(2023, 1, 1), date(2023, 12, 31), date(2023, 1, 1), ("calendar",)),
            Period("prior_interim", "6M YTD 2024", 2024, date(2024, 1, 1), date(2024, 6, 30), date(2023, 7, 1), ("calendar",), 2),
            Period("latest_fy_end", "FY2024", 2024, date(2024, 1, 1), date(2024, 12, 31), date(2024, 1, 1), ("calendar",)),
            Period("current_interim", "6M YTD 2025", 2025, date(2025, 1, 1), date(2025, 6, 30), date(2024, 7, 1), ("calendar",), 2),
        )
    cal = Evidence("calendar", "SYNTHETIC-ONLY", "consolidated", "fixture-calendar",
                   "v1", date(2026, 1, 1), "calendar table", "calendar",
                   tuple(p.role for p in periods), "Synthetic fiscal calendar")
    return empty_report(mode, entity="SYNTHETIC-ONLY", scope="consolidated",
                        currency="USD", scale=D(1000000), periods=periods,
                        evidence={"calendar": cal})


def source_fact(report, fid, value=D(100)):
    """Explicit raw source values, not null-coercing fixture population."""
    facts, evidence = dict(report.facts), dict(report.evidence)
    f = facts[fid]
    eid = "source:" + fid
    scale = report.scale if f.unit == "money" else D(1)
    evidence[eid] = Evidence(eid, report.entity, report.scope, "synthetic-source", "v1",
                             date(2026, 1, 1), fid, "fact", (f.period_role,), str(value))
    facts[fid] = replace(f, status=Status.SOURCED, value=value, original_value=value,
                         original_scale=scale, evidence_ids=(eid,), reason="")
    return replace(report, facts=facts, evidence=evidence)


def complete_fixture(mode):
    """Complete structural fixture; synthetic approvals are not project decisions."""
    r = fixture(mode)
    approval = Evidence("approval", r.entity, r.scope, "synthetic-approval", "v1",
                        date(2026, 1, 1), "fixture-only decisions", "definition",
                        tuple(p.role for p in r.periods), "Synthetic decisions for contract tests only")
    r = replace(r, evidence={**r.evidence, "approval": approval},
                decisions={f"DEC-{i:02d}": "approval" for i in (1, 2, 3, 5, 6)})
    for fid, f in tuple(r.facts.items()):
        if ":pct:" in fid:
            continue
        r = source_fact(r, fid, "Source EBITDA basis" if f.unit == "text" else D(100))
        if f.metric in ("ltm_ebitda", "ebitda_basis", "total_leverage"):
            facts = dict(r.facts)
            facts[fid] = replace(facts[fid], basis="Source EBITDA basis")
            r = replace(r, facts=facts)
    facts = dict(r.facts)
    for fid, f in tuple(facts.items()):
        if ":pct:" in fid:
            facts[fid] = replace(f, status=Status.CALCULATED, value=D(1), reason="",
                                 formula_id="COMMON-SIZE-v1", formula_version="1.0",
                                 input_ids=(f"{f.metric}:{f.period_role}", f"revenue:{f.period_role}"))
    r = replace(r, facts=facts)
    tables = []
    for table in r.tables:
        amount = table.cells[0][-1]
        narratives = tuple(replace(n, status="supported", text="Synthetic observation.",
                                   reason="", fact_ids=(amount,),
                                   period_roles=(r.facts[amount].period_role,))
                           for n in table.narratives)
        tables.append(replace(table, narratives=narratives))
    return replace(r, tables=tuple(tables))


class ContractTests(unittest.TestCase):
    def valid(self, report, mode=None):
        validate_report(report, expected_mode=mode or report.mode)

    def invalid(self, report, rule, mode=None):
        with self.assertRaisesRegex(ContractError, rule):
            validate_report(report, expected_mode=mode or report.mode)

    def mutate_fact(self, r, key="revenue:fy_t", **changes):
        return replace(r, facts={**r.facts, key: replace(r.facts[key], **changes)})

    def test_complete_annual_and_quarterly_payloads_AT01_AT02(self):
        # Structural completeness does not claim arithmetic or semantic acceptance.
        for mode in ("annual", "quarterly"):
            with self.subTest(mode=mode):
                self.valid(complete_fixture(mode), mode)

    def test_all_missing_retains_requested_mode_AT03(self):
        for mode in ("annual", "quarterly"):
            r = fixture(mode)
            self.valid(r, mode)
            self.assertEqual(r.mode.value, mode)
            self.assertTrue(all(f.value is None for f in r.facts.values()))

    def test_mode_required_FMT01(self):
        for bad in (None, "", "auto", "Annual", False):
            with self.subTest(mode=bad), self.assertRaises(ContractError):
                report_layout(bad)

    def test_quarterly_cannot_be_annual_even_with_no_data_AT03(self):
        self.invalid(fixture("annual"), "FMT-01", "quarterly")
        self.invalid(replace(fixture("quarterly"), mode=Mode.ANNUAL), "FMT-01", "quarterly")

    def test_missing_year_cannot_remove_slot_or_column_AT03(self):
        r = fixture()
        self.invalid(replace(r, periods=r.periods[1:]), "FMT-02")
        t = r.tables[0]
        self.invalid(replace(r, tables=(replace(t, cells=tuple(row[1:] for row in t.cells)),) + r.tables[1:]), "FMT-02")

    def test_missing_year_kept_between_available_years_AT03(self):
        r = source_fact(source_fact(fixture(), "revenue:fy_t_minus_3"), "revenue:fy_t_minus_1")
        self.valid(r)
        self.assertIsNone(r.facts["revenue:fy_t_minus_2"].value)
        self.assertEqual(len(r.tables[0].cells[0]), 6)

    def test_unknown_is_not_zero_AT06(self):
        for status in (Status.MISSING, Status.NOT_CALCULABLE, Status.CONFLICT, Status.NOT_APPLICABLE):
            with self.subTest(status=status):
                self.invalid(self.mutate_fact(fixture(), status=status, value=D(0)), "MISS-01")

    def test_sourced_zero_requires_original_zero_AT06(self):
        r = source_fact(fixture(), "revenue:fy_t", D(0))
        self.valid(r)
        self.invalid(self.mutate_fact(r, original_value=None), "DATA-01")
        self.invalid(self.mutate_fact(r, original_value=D(100)), "MISS-01")

    def test_non_decimal_nan_bool_null_rejected(self):
        r = source_fact(fixture(), "revenue:fy_t")
        for value in (None, False, 0, 0.0, "0", D("NaN"), D("Infinity")):
            with self.subTest(value=value):
                self.invalid(self.mutate_fact(r, value=value), "MISS-01")

    def test_unavailable_reason_required_MISS06(self):
        self.invalid(self.mutate_fact(fixture(), reason=""), "MISS-06")

    def test_not_calculable_is_representable_without_value(self):
        self.valid(self.mutate_fact(fixture(), status=Status.NOT_CALCULABLE, reason="Missing approved definition"))

    def test_inapplicability_needs_evidence_MISS03(self):
        self.invalid(self.mutate_fact(fixture(), status=Status.NOT_APPLICABLE), "MISS-03")

    def test_conflict_needs_two_source_versions_AT22(self):
        r = fixture()
        self.invalid(self.mutate_fact(r, status=Status.CONFLICT), "DATA-03")
        e = replace(r.evidence["calendar"], id="e1", kind="fact", source_id="statement", content="100")
        e2 = replace(e, id="e2", version="restated", content="200")
        r = replace(r, evidence={**r.evidence, "e1": e, "e2": e2})
        self.valid(self.mutate_fact(r, status=Status.CONFLICT, evidence_ids=("e1", "e2")))

    def test_entity_scope_and_historical_evidence_rejected_AT16_AT19(self):
        r = source_fact(fixture(), "revenue:fy_t")
        eid = "source:revenue:fy_t"
        for changes in ({"entity": "OLD-BORROWER"}, {"scope": "parent-only"}, {"purpose": "historical"}, {"purpose": "test"}):
            with self.subTest(changes=changes):
                self.invalid(replace(r, evidence={**r.evidence, eid: replace(r.evidence[eid], **changes)}), "EVD-03")

    def test_missing_or_wrong_period_evidence_AT16(self):
        r = source_fact(fixture(), "revenue:fy_t")
        self.invalid(self.mutate_fact(r, evidence_ids=("nonexistent",)), "EVD-01")
        eid = "source:revenue:fy_t"
        self.invalid(replace(r, evidence={**r.evidence, eid: replace(r.evidence[eid], period_roles=("fy_t_minus_1",))}), "EVD-01")

    def test_source_version_and_locator_required_DATA01(self):
        r = fixture()
        for changes in ({"version": ""}, {"locator": ""}, {"source_id": ""}):
            with self.subTest(changes=changes):
                self.invalid(replace(r, evidence={"calendar": replace(r.evidence["calendar"], **changes)}), "DATA-01")

    def test_quarter_is_not_ytd_AT05(self):
        r = fixture("quarterly")
        r = source_fact(r, "revenue:current_interim")
        self.invalid(self.mutate_fact(r, "revenue:current_interim", start=date(2025, 4, 1)), "DATA-01")
        periods = list(r.periods)
        periods[-1] = replace(periods[-1], start=date(2025, 4, 1))
        self.invalid(replace(r, periods=tuple(periods)), "FMT-03")

    def test_non_calendar_fiscal_dates_AT04(self):
        r = fixture("quarterly")
        values = ((2023, 2, 1, 2024, 1, 31, 2023, 2, 1),
                  (2024, 2, 1, 2024, 7, 31, 2023, 8, 1),
                  (2024, 2, 1, 2025, 1, 31, 2024, 2, 1),
                  (2025, 2, 1, 2025, 7, 31, 2024, 8, 1))
        periods = tuple(replace(p, start=date(*v[:3]), end=date(*v[3:6]), ltm_start=date(*v[6:])) for p, v in zip(r.periods, values))
        r = empty_report("quarterly", entity=r.entity, scope=r.scope, currency=r.currency,
                         scale=r.scale, periods=periods, evidence=r.evidence)
        self.valid(r)
        self.assertEqual(r.facts["revenue:current_interim"].start, date(2025, 2, 1))
        self.assertEqual(r.facts["ltm_ebitda:current_interim"].start, date(2024, 8, 1))
        self.assertIsNone(r.facts["total_debt:current_interim"].start)

    def test_53_week_fiscal_year_AT04(self):
        r = fixture()
        intervals = ((date(2022, 1, 2), date(2022, 12, 31)),
                     (date(2023, 1, 1), date(2023, 12, 30)),
                     (date(2023, 12, 31), date(2025, 1, 4)),
                     (date(2025, 1, 5), date(2026, 1, 3)))
        periods = tuple(replace(p, start=s, end=e, ltm_start=s) for p, (s, e) in zip(r.periods, intervals))
        self.valid(empty_report("annual", entity=r.entity, scope=r.scope, currency=r.currency,
                                scale=r.scale, periods=periods, evidence=r.evidence))

    def test_incomplete_ltm_metadata_AT13(self):
        r = fixture("quarterly")
        periods = r.periods[:-1] + (replace(r.periods[-1], ltm_start=date(2025, 1, 1)),)
        self.invalid(replace(r, periods=periods), "CALC-11")

    def test_missing_calendar_preserves_slots_but_blocks_values(self):
        r = fixture()
        p = replace(r.periods[-1], start=None, end=None, ltm_start=None,
                    reason="Calendar source not supplied", evidence_ids=())
        r = empty_report("annual", entity=r.entity, scope=r.scope, currency=r.currency,
                         scale=r.scale, periods=r.periods[:-1] + (p,), evidence=r.evidence)
        self.valid(r)
        self.invalid(source_fact(r, "revenue:fy_t"), "DATA-01")

    def test_pending_definition_blocks_plausible_value_AT09_AT11(self):
        for metric in ("quick_ratio", "total_debt", "debt_service", "dscr", "ltm_ebitda"):
            with self.subTest(metric=metric):
                self.invalid(source_fact(fixture(), metric + ":fy_t"), "AUTH-05")

    def test_units_and_currency_FMT05(self):
        r = fixture()
        self.invalid(self.mutate_fact(r, unit="multiple"), "FMT-05")
        self.invalid(self.mutate_fact(r, currency="EUR"), "FMT-05")
        self.invalid(replace(r, scale=D(0)), "FMT-05")

    def test_common_size_requires_revenue_input_and_no_missing_zero_AT08(self):
        r = complete_fixture("annual")
        key = "net_income:pct:fy_t"
        self.invalid(self.mutate_fact(r, key, input_ids=("net_income:fy_t",)), "CALC-02")
        r = self.mutate_fact(r, "revenue:fy_t", status=Status.MISSING, value=None,
                             original_value=None, reason="missing")
        self.invalid(r, "CALC-03")

    def test_coverage_contract_keeps_capitalized_interest_AT07(self):
        # Definition/input assertions only, not the later arithmetic acceptance.
        from scripts.loan_review_contract import METRICS
        self.assertEqual(METRICS["interest_coverage"].inputs,
                         ("pretax_profit", "interest_expense", "capitalized_interest"))
        self.assertEqual(METRICS["ebitda_interest"].inputs,
                         ("pretax_profit", "interest_expense", "da", "capitalized_interest"))
        self.assertEqual(METRICS["debt_ratio"].definition, "Total Liabilities / Net Worth")

    def test_formula_metadata_and_wrong_formula_rejected(self):
        r = complete_fixture("annual")
        key = "revenue:pct:fy_t"
        self.invalid(self.mutate_fact(r, key, formula_id="GROWTH"), "AUTH-03")
        self.invalid(self.mutate_fact(r, key, formula_version=None), "CALC-02")
        self.invalid(self.mutate_fact(r, key, input_ids=("unknown",)), "CALC-02")

    def test_sourced_ratio_cannot_declare_alternative_definition_AT10(self):
        r = complete_fixture("annual")
        self.invalid(self.mutate_fact(r, "debt_ratio:fy_t",
                                      definition="Total Liabilities / Total Assets"), "AUTH-03")

    def test_same_end_different_duration_inputs_remain_distinct_AT05(self):
        r = source_fact(fixture("quarterly"), "revenue:current_interim")
        original = r.facts["revenue:current_interim"]
        quarter = replace(original, id="standalone-quarter", start=date(2025, 4, 1))
        r = replace(r, facts={**r.facts, quarter.id: quarter})
        self.valid(r)
        self.assertNotEqual(r.facts[quarter.id].start, original.start)
        # The supporting quarter record is permitted but cannot replace the YTD cell.
        t = r.tables[0]
        wrong_row = t.cells[0][:2] + (quarter.id,) + t.cells[0][3:]
        t = replace(t, cells=(wrong_row,) + t.cells[1:])
        self.invalid(replace(r, tables=(t,) + r.tables[1:]), "DATA-01")

    def test_common_size_rejects_standalone_quarter_input_AT05(self):
        r = complete_fixture("quarterly")
        f = replace(r.facts["revenue:current_interim"], id="quarter-revenue", start=date(2025, 4, 1))
        r = replace(r, facts={**r.facts, f.id: f})
        self.invalid(self.mutate_fact(r, "net_income:pct:current_interim",
                                      input_ids=("net_income:current_interim", f.id)), "CALC-03")

    def test_cyclic_lineage_is_rejected_CALC02(self):
        r = complete_fixture("annual")
        for metric, dependency in (("gross_profit", "operating_income"), ("operating_income", "gross_profit")):
            r = self.mutate_fact(r, metric + ":fy_t", status=Status.CALCULATED,
                                 original_value=None, original_scale=None,
                                 formula_id="verified-identity", formula_version="1",
                                 input_ids=(dependency + ":fy_t",), evidence_ids=("approval",))
        self.invalid(r, "cyclic calculation lineage")

    def test_unknown_fact_status_rejected(self):
        self.invalid(self.mutate_fact(fixture(), status="estimated"), "DATA-01")

    def test_management_passage_requires_attribution_EVD01(self):
        r = complete_fixture("annual")
        e = replace(r.evidence["calendar"], id="passage", kind="passage",
                    content="Synthetic management explanation")
        r = replace(r, evidence={**r.evidence, e.id: e})
        n = replace(r.tables[0].narratives[0], claim_type="management", evidence_ids=(e.id,))
        t = replace(r.tables[0], narratives=(n,) + r.tables[0].narratives[1:])
        r = replace(r, tables=(t,) + r.tables[1:])
        self.invalid(r, "attribution")
        n = replace(n, attribution="Management stated")
        t = replace(t, narratives=(n,) + t.narratives[1:])
        self.valid(replace(r, tables=(t,) + r.tables[1:]))

    def test_wrong_period_passage_cannot_hide_behind_current_fact_AT16(self):
        r = complete_fixture("annual")
        e = replace(r.evidence["calendar"], id="old-passage", kind="passage",
                    period_roles=("fy_t_minus_1",), content="Prior-year explanation")
        n = replace(r.tables[0].narratives[0], claim_type="cause", evidence_ids=(e.id,))
        t = replace(r.tables[0], narratives=(n,) + r.tables[0].narratives[1:])
        self.invalid(replace(r, evidence={**r.evidence, e.id: e}, tables=(t,) + r.tables[1:]), "MISS-04")

    def test_narrative_growth_retains_comparable_ytd_inputs(self):
        from scripts.loan_review_contract import METRICS
        r = complete_fixture("quarterly")
        p = r.periods[-1]
        growth = Fact("growth", "revenue_growth", "current_interim", Status.CALCULATED,
                      D(0), "percent", METRICS["revenue_growth"].definition, p.start, p.end,
                      r.entity, r.scope, formula_id="CF-09", formula_version="1.0",
                      input_ids=("revenue:current_interim", "revenue:prior_interim"),
                      period_kind="duration")
        r = replace(r, facts={**r.facts, growth.id: growth})
        self.valid(r)
        self.invalid(self.mutate_fact(r, "growth", input_ids=("revenue:current_interim", "revenue:current_interim")), "CALC-03")

    def test_narrative_margin_support_is_not_an_extra_table_row(self):
        from scripts.loan_review_contract import METRICS
        r = complete_fixture("annual")
        p = r.periods[-1]
        margin = Fact("margin", "gross_margin", "fy_t", Status.CALCULATED,
                      D(1), "percent", METRICS["gross_margin"].definition, p.start, p.end,
                      r.entity, r.scope, formula_id="CF-10", formula_version="1.0",
                      input_ids=("gross_profit:fy_t", "revenue:fy_t"), period_kind="duration")
        r = replace(r, facts={**r.facts, margin.id: margin})
        self.valid(r)
        self.assertEqual(len(r.tables[0].cells), 9)

    def test_ebitda_basis_is_required_and_consistent_AT17(self):
        r = complete_fixture("quarterly")
        self.invalid(self.mutate_fact(r, "ltm_ebitda:current_interim", basis=""), "CALC-12")
        self.invalid(self.mutate_fact(r, "ltm_ebitda:current_interim", basis="Different definition"), "CALC-12")
        self.invalid(self.mutate_fact(r, "total_leverage:current_interim", basis="Different definition"), "CALC-09")

    def test_supported_cause_needs_passage_AT15(self):
        r = source_fact(fixture(), "revenue:fy_t")
        n = Narrative("revenue", "supported", "Sales changed due to demand.", "cause",
                      ("revenue:fy_t",), period_roles=("fy_t",))
        t = replace(r.tables[0], narratives=(n,) + r.tables[0].narratives[1:])
        self.invalid(replace(r, tables=(t,) + r.tables[1:]), "MISS-04")

    def test_comparison_needs_two_period_facts_AT16(self):
        r = complete_fixture("annual")
        n = replace(r.tables[0].narratives[0], claim_type="comparison")
        t = replace(r.tables[0], narratives=(n,) + r.tables[0].narratives[1:])
        self.invalid(replace(r, tables=(t,) + r.tables[1:]), "EVD-01")

    def test_missing_topic_does_not_allow_filler_MISS04(self):
        r = fixture()
        n = replace(r.tables[0].narratives[0], text="Liquidity is healthy.")
        t = replace(r.tables[0], narratives=(n,) + r.tables[0].narratives[1:])
        self.invalid(replace(r, tables=(t,) + r.tables[1:]), "MISS-04")


if __name__ == "__main__":
    unittest.main()
