"""Standard-library tests for the opportunity evaluator.

Run from repo root:
python -m unittest discover -s tests -p 'test_opportunity_evaluator.py'
"""
import json
import tempfile
import unittest
from pathlib import Path
from strategy.evaluate import parse_config, parse_signals, evaluate, report_md

HERE = Path(__file__).resolve().parents[1]


class ModelEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.config = parse_config(HERE / "strategy" / "models.json")

    def test_provisional_default_is_digital_products(self):
        result = evaluate(self.config, [])
        self.assertEqual(result["selection"], "digital_products")
        self.assertEqual(result["selection_status"], "provisional_experiment_choice")
        self.assertIsNone(result["verified_revenue"])
        self.assertIn("NOT validated product demand", report_md(result))

    def test_actual_records_can_change_ranking_without_claiming_verified_sales(self):
        signal = {
            "model": "ai_services",
            "kind": "paid_order",
            "observed_at": "2026-11-11",
            "source": "example-internal-reference",
        }
        result = evaluate(self.config, [signal])
        self.assertEqual(result["selection"], "ai_services")
        self.assertIsNone(result["verified_revenue"])
        self.assertEqual(result["selection_status"], "provisional_experiment_choice")

    def test_missing_signal_file_is_not_reported_as_zero_sales(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(parse_signals(Path(tmp) / "not-there.json"), [])

    def test_reject_uncited_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.json"
            path.write_text(json.dumps([{
                "model": "digital_products",
                "kind": "paid_order",
                "observed_at": "2026-11-11",
            }]))
            with self.assertRaises(ValueError):
                parse_signals(path)


if __name__ == "__main__":
    unittest.main()
