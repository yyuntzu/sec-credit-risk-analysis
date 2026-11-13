"""Independent v1.0 layout expectations; tests the boundary, not legacy rendering."""
from dataclasses import replace
from pathlib import Path
import unittest

from scripts.loan_review_contract import ContractError, METRICS, Narrative, report_layout, validate_report
from test_loan_review_contract import fixture


class FormatTests(unittest.TestCase):
    def test_annual_exact_layout_AT01(self):
        r = fixture()
        self.assertEqual(r.headings, (
            (2, "A. Annual Review"), (3, "YOY (Annual) Income"),
            (3, "Annual Cash Flows"), (3, "Ratios YOY"), (3, "Leverage YOY")))
        self.assertEqual([len(t.spec.columns) + 1 for t in r.tables], [7, 5, 5, 5])
        self.assertEqual(r.tables[0].spec.columns, (
            "fy_t_minus_3", "fy_t_minus_2", "fy_t_minus_1", "pct:fy_t_minus_1", "fy_t", "pct:fy_t"))
        self.assertEqual(r.tables[1].spec.rows, (
            "beginning_cash", "cfo", "cfi", "cff", "ending_cash", "cash_change"))
        self.assertEqual(r.tables[2].spec.rows, (
            "current_ratio", "quick_ratio", "cash_flow_ratio", "debt_ratio", "interest_coverage"))
        self.assertEqual(r.tables[3].spec.rows, (
            "total_debt", "debt_service", "interest_expense", "ltm_ebitda", "ebitda_basis",
            "total_leverage", "ebitda_interest", "dscr"))

    def test_quarterly_exact_layout_AT02(self):
        r = fixture("quarterly")
        self.assertEqual(r.headings, (
            (2, "B. Quarterly Review"), (3, "Financial Analysis"),
            (4, "YTD (Quarterly) Income"), (4, "Ratios YTD"), (4, "Leverage Analysis YTD")))
        self.assertEqual([len(t.spec.columns) + 1 for t in r.tables], [5, 5, 5])
        self.assertEqual(r.tables[0].spec.columns,
                         ("prior_interim", "pct:prior_interim", "current_interim", "pct:current_interim"))
        self.assertEqual(r.tables[1].spec.columns,
                         ("earlier_fy_end", "prior_interim", "latest_fy_end", "current_interim"))
        self.assertEqual(r.tables[1].spec.rows, ("current_ratio", "quick_ratio", "debt_ratio"))
        self.assertEqual(r.tables[2].spec.rows, ("total_debt", "ltm_ebitda", "ebitda_basis", "total_leverage"))

    def test_common_income_rows_and_topics(self):
        for mode in ("annual", "quarterly"):
            spec = report_layout(mode)[0]
            self.assertEqual(spec.rows, ("revenue", "cost_of_revenue", "gross_profit", "operating_expense",
                                         "operating_income", "interest_expense", "pretax_profit", "income_tax", "net_income"))
            self.assertEqual(spec.topics, ("revenue", "gross_margin", "operating_margin", "interest_expense", "pretax_margin"))

    def test_every_output_cell_has_metric_period_definition_unit_rule(self):
        for mode in ("annual", "quarterly"):
            r = fixture(mode)
            for table in r.tables:
                self.assertTrue(table.spec.rule)
                for row in table.cells:
                    for fid in row:
                        f = r.facts[fid]
                        spec = METRICS[f.metric]
                        self.assertTrue(spec.definition and spec.rule and spec.unit and spec.period_kind)
                        self.assertIn(f.period_role, {p.role for p in r.periods})

    def test_extra_sections_forbidden_FMT07(self):
        for mode in ("annual", "quarterly"):
            for heading in ("Summary", "Guidance", "Covenants", "Enterprise Value Analysis", "Data Quality Notes"):
                r = fixture(mode)
                with self.subTest(mode=mode, heading=heading), self.assertRaisesRegex(ContractError, "FMT-07"):
                    validate_report(replace(r, headings=r.headings + ((3, heading),)), expected_mode=mode)

    def test_wrong_row_order_and_extra_annual_rows_rejected(self):
        r = fixture("quarterly")
        t = r.tables[-1]
        for rows in (tuple(reversed(t.spec.rows)), t.spec.rows + ("debt_service",)):
            changed = replace(t, spec=replace(t.spec, rows=rows))
            with self.assertRaisesRegex(ContractError, "FMT-02"):
                validate_report(replace(r, tables=r.tables[:-1] + (changed,)), expected_mode="quarterly")

    def test_wrong_table_order_and_column_binding_rejected(self):
        r = fixture()
        with self.assertRaisesRegex(ContractError, "FMT-02"):
            validate_report(replace(r, tables=tuple(reversed(r.tables))), expected_mode="annual")
        t = r.tables[0]
        wrong = replace(t, cells=(tuple(reversed(t.cells[0])),) + t.cells[1:])
        with self.assertRaisesRegex(ContractError, "FMT-02"):
            validate_report(replace(r, tables=(wrong,) + r.tables[1:]), expected_mode="annual")

    def test_no_guidance_or_summary_hidden_in_notes(self):
        r = fixture()
        t = replace(r.tables[0], notes=(Narrative("guidance", "missing", reason="Not provided"),))
        with self.assertRaisesRegex(ContractError, "FMT-07"):
            validate_report(replace(r, tables=(t,) + r.tables[1:]), expected_mode="annual")

    def test_no_extra_narrative_quota(self):
        r = fixture("quarterly")
        self.assertEqual(tuple(n.topic for n in r.tables[1].narratives), ("liquidity", "debt_ratio"))
        self.assertEqual(tuple(n.topic for n in r.tables[2].narratives), ("total_debt", "ltm_ebitda", "total_leverage"))
        self.assertEqual(fixture().tables[1].narratives, ())

    def test_documented_headings_match_executable_contract(self):
        # Detect documentation/layout drift, separately from behavioral assertions.
        doc = (Path(__file__).resolve().parents[1] / "references/output-format.md").read_text()
        for mode in ("annual", "quarterly"):
            for level, title in fixture(mode).headings:
                self.assertIn("#" * level + " " + title, doc.splitlines())


if __name__ == "__main__":
    unittest.main()
