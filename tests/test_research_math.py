"""Offline financial-behavior checks using explicitly synthetic inputs."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/stock-opportunity-scanner/scripts/research_math.py'
EXAMPLES = ROOT / 'examples/stock-opportunity-scanner'
SPEC = importlib.util.spec_from_file_location('research_math', SCRIPT)
MATH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATH)


def example(name):
    return json.loads((EXAMPLES / (name + '.json')).read_text(encoding='utf-8'))


class ResearchMathTests(unittest.TestCase):
    def test_offering_distinguishes_ownership_and_economic_dilution(self):
        result = MATH.dilution(example('dilution'))
        self.assertAlmostEqual(result['share_count_expansion'], 0.20)
        self.assertAlmostEqual(result['old_holder_ownership_dilution'], 1 / 6)
        self.assertAlmostEqual(result['theoretical_ex_issue_price'], 18.633333333333333)
        self.assertEqual(result['post_cash'], 186)
        self.assertEqual(result['post_debt'], 150)
        self.assertEqual(result['post_enterprise_value'], 1884)

    def test_profit_growth_can_coexist_with_eps_decline(self):
        result = MATH.forecast(example('forecast'))['scenarios']['base']
        self.assertAlmostEqual(result['revenue_cagr'], 0.15)
        self.assertAlmostEqual(result['net_income_cagr'], 0.15)
        self.assertAlmostEqual(result['eps_cagr'], -1 / 24)
        self.assertLess(result['terminal_price'], 20)

    def test_losses_and_missing_equity_bridge_do_not_get_invented_values(self):
        result = MATH.forecast(example('forecast'))['scenarios']
        self.assertIsNone(result['bear']['terminal_price'])
        self.assertIsNone(result['bear']['eps_cagr'])
        self.assertIsNone(result['base']['years'][-1]['book_equity'])
        self.assertAlmostEqual(result['bull']['years'][-1]['book_equity'], 1119.8)

    def test_split_does_not_count_as_accumulation_or_incomplete_table_as_exit(self):
        rows = MATH.holdings(example('holdings'))['rows']
        indexed = {(r['security_id'], r['instrument']): r for r in rows}
        self.assertEqual(indexed['ABC', 'SHARE']['status'], 'unchanged_disclosed_quantity')
        self.assertEqual(indexed['ABC', 'CALL']['status'], 'newly_disclosed')
        self.assertEqual(indexed['ZZZ', 'SHARE']['status'], 'unknown_current')

    def test_grants_duplicates_and_unreviewed_notes_are_separated(self):
        result = MATH.insiders(example('insiders'))
        self.assertEqual(len(result['purchase_candidates']), 2)
        self.assertEqual(len(result['excluded']), 2)
        first, second = result['purchase_candidates']
        self.assertEqual(first['venue'], 'private')
        self.assertEqual(first['cash_value'], 12000)
        self.assertEqual(second['venue'], 'unknown')
        self.assertFalse(second['ready_for_primary_source_assertion'])

    def test_loss_to_profit_cagr_and_financial_sector_leverage_are_not_comparable(self):
        first, bank = MATH.screen(example('screen'))['rows']
        self.assertAlmostEqual(first['revenue_cagr'], 0.20)
        self.assertIsNone(first['eps_cagr'])
        self.assertAlmostEqual(first['fcf_yield'], 1 / 30)
        self.assertIsNone(bank['trailing_pe'])
        self.assertIsNone(bank['net_debt_ebitda'])

    def test_impossible_offering_inputs_are_rejected(self):
        for key, value in [('fees', 1000), ('pre_shares', 0), ('debt_repaid', 500)]:
            with self.subTest(field=key):
                data = example('dilution')
                data[key] = value
                with self.assertRaises(ValueError):
                    MATH.dilution(data)

    def test_duplicate_holdings_require_resolution(self):
        data = example('holdings')
        data['current'].append(copy.deepcopy(data['current'][0]))
        with self.assertRaises(ValueError):
            MATH.holdings(data)

    def test_documented_command_line_examples_run(self):
        for command in ('screen', 'forecast', 'dilution', 'holdings', 'insiders'):
            with self.subTest(command=command):
                run = subprocess.run(
                    [sys.executable, str(SCRIPT), command, str(EXAMPLES / (command + '.json'))],
                    capture_output=True, text=True, check=True,
                )
                self.assertIsInstance(json.loads(run.stdout), dict)


if __name__ == '__main__':
    unittest.main()
