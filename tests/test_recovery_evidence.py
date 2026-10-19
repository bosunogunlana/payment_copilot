"""Verify evidence exercises application boundaries and preserves outcomes."""

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from evals.recovery_evidence import build_report, main


class RecoveryEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()
        cls.cases = {c["case_id"]: c for c in cls.report["cases"]}

    def test_all_failure_categories_have_passing_observed_traces(self):
        required = {
            "unknown_tool", "invalid_arguments", "unauthorized", "payment_not_found",
            "invalid_provider", "malformed_response", "empty_object", "empty_list_success",
            "timeout_recovery", "server_error_recovery", "attempt_exhaustion", "deadline",
            "authorization_revoked", "late_success", "replayed_call_id", "fresh_read",
            "commit_then_timeout",
        }
        self.assertEqual(set(self.cases), required)
        self.assertEqual((self.report["passed"], self.report["total"]), (17, 17))
        for case in self.report["cases"]:
            with self.subTest(case=case["case_id"]):
                self.assertTrue(case["passed"], case["checks"])
                self.assertTrue("recovery" in case or "loop" in case)
        json.dumps(self.report)

    def test_deadline_and_revocation_retain_attempt_evidence(self):
        deadline = self.cases["deadline"]["recovery"]
        self.assertEqual([a["timeout_s"] for a in deadline["attempts"]], [1.0, 0.25])
        self.assertEqual(deadline["stop_reason"], "deadline")
        revoked = self.cases["authorization_revoked"]
        self.assertEqual(revoked["counts"], {"authorize": 2, "read": 1})
        self.assertEqual(revoked["recovery"]["result"]["error"]["code"], "UNAUTHORIZED")

    def test_replay_and_fresh_read_have_different_execution_counts(self):
        self.assertEqual(self.cases["replayed_call_id"]["counts"]["read"], 1)
        self.assertEqual(self.cases["fresh_read"]["counts"]["read"], 2)
        self.assertEqual(self.cases["replayed_call_id"]["loop"]["status"], "repeated_call")

    def test_lost_receipt_replay_has_one_effect_and_original_receipt(self):
        case = self.cases["commit_then_timeout"]
        self.assertEqual(case["effect_count"], 1)
        self.assertEqual(len(case["recovery"]["attempts"]), 2)
        self.assertEqual(case["recovery"]["result"]["data"], case["original_receipt"])
        self.assertEqual(case["conflict"]["code"], "IDEMPOTENCY_CONFLICT")
        self.assertIs(case["conflict"]["retryable"], False)

    def test_cli_saves_artifact_and_refuses_overwrite(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "recovery.json"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--output", str(output)]), 0)
            saved = output.read_bytes()
            self.assertEqual(json.loads(saved)["mode"], "offline-scripted")
            from unittest.mock import patch
            with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                main(["--output", str(output)])
            self.assertEqual(output.read_bytes(), saved)
