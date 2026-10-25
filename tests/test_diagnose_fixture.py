"""Offline acceptance checks for the documented local diagnosis command."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from app.models.diagnosis import Diagnosis


class DiagnoseFixtureTest(unittest.TestCase):
    def run_command(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "evals.diagnose_fixture", *arguments],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def test_default_case_produces_a_typed_success(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        diagnosis = Diagnosis.model_validate_json(result.stdout)
        self.assertEqual(diagnosis.category, "successful_payment")

    def test_missing_events_produce_safe_uncertainty(self):
        result = self.run_command("--case-id", "case-003")
        self.assertEqual(result.returncode, 0, result.stderr)
        diagnosis = Diagnosis.model_validate_json(result.stdout)
        self.assertEqual(diagnosis.category, "unknown")
        self.assertEqual(diagnosis.recommended_action, "escalate_to_human")
        self.assertIsNone(diagnosis.likely_cause)
        self.assertLess(diagnosis.confidence, 0.5)

    def test_unknown_case_is_an_explicit_cli_error(self):
        result = self.run_command("--case-id", "does-not-exist")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_saved_result_matches_stdout_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "diagnosis.json"
            result = self.run_command("--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            original = output.read_text(encoding="utf-8")
            self.assertEqual(json.loads(original), json.loads(result.stdout))
            repeated = self.run_command("--output", str(output))
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), original)
