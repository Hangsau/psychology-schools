import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "inventory-high-risk.py"
SPEC = importlib.util.spec_from_file_location("inventory_high_risk", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class HighRiskInventoryTests(unittest.TestCase):
    def test_candidates_and_exact_anchor_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            school = root / "schools" / "demo"
            school.mkdir(parents=True)
            school.joinpath("synthesis.md").write_text(
                "## 2. 人物\n\n甲於 1950 年首次提出模型。\n\n"
                "## 6. 成效\n\n後設分析顯示治療有效。\n",
                encoding="utf-8",
            )
            claim = {"id": "demo-001", "text_anchor": "甲於 1950 年首次提出模型"}
            school.joinpath("claims.jsonl").write_text(
                json.dumps(claim, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            report = MODULE.inventory(root, "demo")
            self.assertEqual(report["candidate_count"], 2)
            self.assertEqual(report["covered_count"], 1)
            self.assertEqual(report["uncovered_count"], 1)

    def test_plain_paragraph_is_not_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            school = root / "schools" / "demo"
            school.mkdir(parents=True)
            school.joinpath("synthesis.md").write_text("## 3. 理論\n\n這是一段說明。\n", encoding="utf-8")
            report = MODULE.inventory(root, "demo")
            self.assertEqual(report["candidate_count"], 0)

    def test_each_list_item_is_a_separate_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            school = root / "schools" / "demo"
            school.mkdir(parents=True)
            school.joinpath("synthesis.md").write_text(
                "## 4. 書目\n\n- 甲，1950。\n- 乙，1960。\n", encoding="utf-8"
            )
            report = MODULE.inventory(root, "demo")
            self.assertEqual(report["candidate_count"], 2)

    def test_multiple_risky_sentences_are_separate_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            school = root / "schools" / "demo"
            school.mkdir(parents=True)
            school.joinpath("synthesis.md").write_text(
                "## 2. 人物\n\n甲於 1950 年提出模型。乙於 1960 年發展量表。\n",
                encoding="utf-8",
            )
            report = MODULE.inventory(root, "demo")
            self.assertEqual(report["candidate_count"], 2)


if __name__ == "__main__":
    unittest.main()
