import copy
import datetime as dt
import importlib.util
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(skill, script):
    path = ROOT / "skills" / skill / "scripts" / (script + ".py")
    spec = importlib.util.spec_from_file_location(script, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def example(skill, file):
    return json.loads((ROOT / "skills" / skill / "examples" / (file + ".json")).read_text())


VALUATION = module("fundamental-valuation", "valuation")
TECHNICAL = module("technical-signals", "signals")
INSIDERS = module("insider-buying", "insiders")
HOLDINGS = module("institutional-ownership", "holdings")
DILUTION = module("emerging-companies", "dilution")


class ValuationTests(unittest.TestCase):
    def setUp(self):
        self.data = example("fundamental-valuation", "valuation")

    def externalize(self):
        for row in self.data["forecasts"]:
            for metric in ("revenue", "net_income"):
                row[metric]["kind"] = "dated_consensus"

    def test_equity_ratio_is_not_diluted_per_share_return(self):
        out = VALUATION.analyze(self.data)
        base = next(s for s in out["scenarios"] if s["name"] == "base")
        self.assertAlmostEqual(base["future_equity_value"], 1800)
        self.assertAlmostEqual(base["equity_value_ratio"], 1.8)
        self.assertAlmostEqual(base["aggregate_equity_change"], .8)
        self.assertAlmostEqual(base["future_price"], 15)
        self.assertAlmostEqual(base["per_share_price_return"], .5)
        years = (dt.date(2028, 12, 31) - dt.date(2026, 9, 18)).days / 365.25
        self.assertAlmostEqual(base["annualized_price_return"], 1.5 ** (1 / years) - 1)

    def test_model_growth_match_is_separate_from_external_metadata(self):
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "model_or_unverified_metadata_match")
        self.externalize()
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "externally_supported_metadata_match")

    def test_cagr_cannot_hide_one_failed_annual_comparison(self):
        self.externalize()
        for row, revenue in zip(self.data["forecasts"], (1300, 1326, 1723.8)):
            row["revenue"]["value"] = revenue
        out = VALUATION.analyze(self.data)
        self.assertGreater(out["three_year_cagr"]["revenue"], .1)
        self.assertEqual(out["screen_status"], "fails_annual_growth_screen")

    def test_missing_third_year_is_not_a_pass_or_zero(self):
        self.data["forecasts"][-1]["net_income"] = None
        out = VALUATION.analyze(self.data)
        self.assertEqual(out["screen_status"], "incomplete_forecasts")
        self.assertIsNone(out["annual_growth"][-1]["net_income"]["yoy_growth"])

    def test_derived_income_is_not_consensus(self):
        self.externalize()
        self.data["forecasts"][1]["net_income"]["kind"] = "derived_estimate"
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "model_or_unverified_metadata_match")

    def test_loss_base_is_a_turnaround_without_income_cagr(self):
        self.data["base"]["net_income"]["value"] = -100
        out = VALUATION.analyze(self.data)
        self.assertEqual(out["screen_status"], "turnaround_or_nonpositive_income")
        self.assertIsNone(out["three_year_cagr"]["net_income"])

    def test_adjusted_and_reported_bases_are_not_mixed(self):
        self.data["forecasts"][1]["net_income"]["basis"] = "adjusted"
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "incompatible_accounting_bases")

    def test_ten_percent_inclusive_and_strict_differ(self):
        self.externalize()
        for i, row in enumerate(self.data["forecasts"], 1):
            row["revenue"]["value"] = 1000 * 1.1 ** i
            row["net_income"]["value"] = 100 * 1.1 ** i
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "externally_supported_metadata_match")
        self.data["strict_growth"] = True
        self.assertEqual(VALUATION.analyze(self.data)["screen_status"], "fails_annual_growth_screen")

    def test_capitalization_and_share_basis_must_reconcile(self):
        self.data["market_cap"] = 2000
        with self.assertRaises(ValueError):
            VALUATION.analyze(self.data)

    def test_lookahead_source_rejected(self):
        self.data["forecasts"][0]["revenue"]["source_date"] = "2027-01-01"
        with self.assertRaises(ValueError):
            VALUATION.analyze(self.data)

    def test_terminal_loss_has_no_pe_price(self):
        self.data["scenarios"][0]["future_net_income"] = -10
        case = VALUATION.analyze(self.data)["scenarios"][0]
        self.assertFalse(case["pe_applicable"])
        self.assertIsNone(case["future_price"])

    def test_bad_periods_and_nonfinite_values_rejected(self):
        cases = []
        bad = copy.deepcopy(self.data)
        bad["forecasts"][1]["fiscal_year"] += 1
        cases.append(bad)
        bad = copy.deepcopy(self.data)
        bad["forecasts"][0]["revenue"]["value"] = math.nan
        cases.append(bad)
        for data in cases:
            with self.assertRaises(ValueError):
                VALUATION.analyze(data)

    def test_unreported_ended_year_can_remain_an_estimate(self):
        self.data["as_of"] = "2027-01-10"
        out = VALUATION.analyze(self.data)
        self.assertEqual(out["annual_growth"][0]["fiscal_year"], 2026)


class TechnicalTests(unittest.TestCase):
    def setUp(self):
        self.data = example("technical-signals", "bars")

    def test_cross_and_prior_only_volume_and_high_windows(self):
        out = TECHNICAL.analyze(self.data)
        self.assertTrue(out["moving_averages"]["200"]["cross_up"])
        self.assertAlmostEqual(out["relative_volume"], 3)
        self.assertEqual(out["extremes"]["prior_high"], 101)
        self.assertTrue(out["extremes"]["new_intraday_high"])
        self.assertAlmostEqual(out["daily_return"], .2)

    def test_already_above_average_is_not_a_new_cross(self):
        self.data["bars"][-2].update(open=110, high=111, low=109, close=110)
        out = TECHNICAL.analyze(self.data)
        self.assertFalse(out["moving_averages"]["200"]["cross_up"])

    def test_short_history_produces_unknown_not_false_long_signals(self):
        self.data["bars"] = self.data["bars"][-10:]
        out = TECHNICAL.analyze(self.data)
        self.assertIsNone(out["moving_averages"]["200"]["cross_up"])
        self.assertIsNone(out["relative_volume"])
        self.assertIsNone(out["extremes"]["new_intraday_high"])

    def test_zero_volume_baseline_produces_no_infinite_ratio(self):
        for bar in self.data["bars"][:-1]:
            bar["volume"] = 0
        self.assertIsNone(TECHNICAL.analyze(self.data)["relative_volume"])

    def test_partial_session_and_mixed_adjustments_rejected(self):
        for field, value in (("completed", False), ("price_basis", "dividend_adjusted"), ("volume_basis", "raw")):
            data = copy.deepcopy(self.data)
            data[field] = value
            with self.assertRaises(ValueError):
                TECHNICAL.analyze(data)

    def test_invalid_ohlc_and_duplicate_dates_rejected(self):
        for change in ("range", "date"):
            data = copy.deepcopy(self.data)
            if change == "range":
                data["bars"][-1]["high"] = 1
            else:
                data["bars"][-1]["date"] = data["bars"][-2]["date"]
            with self.assertRaises(ValueError):
                TECHNICAL.analyze(data)

    def test_future_session_is_rejected(self):
        self.data["as_of"] = "2025-01-01"
        with self.assertRaises(ValueError):
            TECHNICAL.analyze(self.data)


class MigratedCalculatorTests(unittest.TestCase):
    def test_insider_grants_duplicates_private_and_unknown_venue(self):
        out = INSIDERS.insiders(example("insider-buying", "insiders"))
        self.assertEqual(len(out["purchase_candidates"]), 2)
        self.assertEqual(len(out["excluded"]), 2)
        first, second = out["purchase_candidates"]
        self.assertEqual(first["cash_value"], 12000)
        self.assertEqual(first["venue"], "private")
        self.assertEqual(second["venue"], "unknown")
        self.assertFalse(second["ready_for_primary_source_assertion"])

    def test_split_options_and_missing_table_not_buy_sell(self):
        out = HOLDINGS.holdings(example("institutional-ownership", "holdings"))
        rows = {(r["security_id"], r["instrument"]): r for r in out["rows"]}
        self.assertEqual(rows["ABC", "SHARE"]["share_change"], 0)
        self.assertEqual(rows["ABC", "CALL"]["status"], "newly_disclosed")
        self.assertEqual(rows["ZZZ", "SHARE"]["status"], "unknown_current")

    def test_duplicate_holdings_must_be_reconciled(self):
        data = example("institutional-ownership", "holdings")
        data["current"].append(copy.deepcopy(data["current"][0]))
        with self.assertRaises(ValueError):
            HOLDINGS.holdings(data)

    def test_primary_issuance_cash_and_ownership_differ(self):
        out = DILUTION.dilution(example("emerging-companies", "dilution"))
        self.assertEqual(out["post_shares"], 120)
        self.assertAlmostEqual(out["share_count_expansion"], .2)
        self.assertAlmostEqual(out["old_holder_ownership_dilution"], 1/6)
        self.assertEqual(out["net_proceeds"], 236)
        self.assertEqual(out["post_cash"], 186)
        self.assertEqual(out["post_debt"], 150)
        self.assertAlmostEqual(out["theoretical_ex_issue_price"], 2236/120)

    def test_impossible_financing_inputs_rejected(self):
        for key, value in (("fees", 1000), ("pre_shares", 0), ("debt_repaid", 500)):
            data = example("emerging-companies", "dilution")
            data[key] = value
            with self.assertRaises(ValueError):
                DILUTION.dilution(data)

    def test_all_documented_calculator_commands_execute(self):
        cases = [("insider-buying", "insiders", ["insiders"], "insiders"),
                 ("institutional-ownership", "holdings", ["holdings"], "holdings"),
                 ("emerging-companies", "dilution", ["dilution"], "dilution"),
                 ("fundamental-valuation", "valuation", [], "valuation"),
                 ("technical-signals", "signals", [], "bars")]
        for skill, script, command, sample in cases:
            with self.subTest(skill=skill):
                folder = ROOT / "skills" / skill
                run = subprocess.run([sys.executable, str(folder / "scripts" / (script + ".py")),
                                      *command, str(folder / "examples" / (sample + ".json"))],
                                     capture_output=True, text=True, check=True)
                self.assertIsInstance(json.loads(run.stdout), dict)


if __name__ == "__main__":
    unittest.main()
