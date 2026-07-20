#!/usr/bin/env python3
"""系統級測試：以臨時 repo 驗證空、壞、部分與合法 claims 行為。"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(REPO, "tools", "verify-claims.py")


class EvidenceValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="psych-evidence-")
        self.school = os.path.join(self.tmp, "schools", "demo")
        os.makedirs(self.school)
        with open(os.path.join(self.school, "synthesis.md"), "w", encoding="utf-8") as f:
            f.write("## 1. 定位\n獨特錨點：Beck 於 1976 年出版本書。\n")
        self.state = {
            "stage": "in_progress", "high_risk_claims_total": 1,
            "corroborated": 1, "disputed": 0, "insufficient": 0,
            "retrieved": 0, "unverified": 0, "checked_at": "2026-07-20"
        }
        self.write_meta(self.state)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_meta(self, state):
        with open(os.path.join(self.school, "meta.json"), "w", encoding="utf-8") as f:
            json.dump({"slug": "demo", "evidence_state": state}, f)

    def run_validator(self):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, VERIFY, "--root", self.tmp, "--strict", "--require-claims", "demo"],
            capture_output=True, text=True, encoding="utf-8", env=env
        )

    def valid_claim(self):
        return {
            "id": "demo-001", "claim": "Beck 於 1976 年出版本書", "type": "bibliographic", "risk": "high",
            "source_ids": ["doi:10.1000/alpha", "isbn:978-0-123456-47-2"],
            "source_independence": "independent", "verdict": "corroborated", "confidence": "high",
            "checked_at": "2026-07-20", "checker": "test-v1", "text_anchor": "獨特錨點：Beck 於 1976 年出版本書"
        }

    def write_claims(self, lines):
        with open(os.path.join(self.school, "claims.jsonl"), "w", encoding="utf-8") as f:
            f.write(lines)

    def test_valid_claims_pass(self):
        self.write_claims(json.dumps(self.valid_claim(), ensure_ascii=False) + "\n")
        self.assertEqual(self.run_validator().returncode, 0)

    def test_empty_claims_fail(self):
        self.write_claims("")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_malformed_json_fails(self):
        self.write_claims("{not-json}\n")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_partial_claim_fails(self):
        self.write_claims(json.dumps({"id": "demo-001"}) + "\n")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_duplicate_id_and_bad_source_fail(self):
        claim = self.valid_claim()
        claim["source_ids"] = ["google it"]
        raw = json.dumps(claim, ensure_ascii=False)
        self.write_claims(raw + "\n" + raw + "\n")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_orphan_anchor_fails(self):
        claim = self.valid_claim()
        claim["text_anchor"] = "正文裡不存在的錨點"
        self.write_claims(json.dumps(claim, ensure_ascii=False) + "\n")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_missing_claims_allowed_for_not_started(self):
        self.write_meta({"stage": "not_started"})
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, VERIFY, "--root", self.tmp, "--strict", "demo"],
            capture_output=True, text=True, encoding="utf-8", env=env
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
