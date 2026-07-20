#!/usr/bin/env python3
"""Inventory paragraphs likely to contain high-risk factual claims.

This is a recall-oriented triage tool, not a truth checker.  A candidate is
"covered" only when an existing claim's exact text_anchor occurs in it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


YEAR = re.compile(r"(?<!\d)(?:18|19|20)\d{2}(?!\d)")
NUMBER = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?\s*(?:%|％|倍|人|年|項|篇|種|國|週|次)")
KEYWORDS = {
    "efficacy": ("療效", "有效", "效果量", "隨機試驗", "後設分析", "系統性回顧", "優於", "相近"),
    "attribution": ("創立", "創始", "提出", "發展", "奠基", "首度", "首次", "最早"),
    "absolute": ("唯一", "所有", "完全", "必然", "迄今", "最大", "最廣", "第一線", "第二線"),
}


def paragraphs(text: str) -> list[tuple[int, str, str]]:
    section = ""
    result = []
    buf: list[str] = []
    start = 1
    for lineno, line in enumerate(text.splitlines() + [""], 1):
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("- "):
            if buf:
                result.append((start, section, " ".join(buf)))
                buf = []
            result.append((lineno, section, line.strip()))
            continue
        if line.strip():
            if line.startswith("#") or line.startswith(">"):
                continue
            if not buf:
                start = lineno
            buf.append(line.strip())
        elif buf:
            result.append((start, section, " ".join(buf)))
            buf = []
    return result


def reasons(section: str, text: str) -> list[str]:
    found = []
    if YEAR.search(text):
        found.append("date")
    if NUMBER.search(text):
        found.append("number")
    for kind, words in KEYWORDS.items():
        if any(word in text for word in words):
            found.append(kind)
    if section.startswith("4.") and (text.startswith("-") or "**_" in text or "**”" in text):
        found.append("bibliographic")
    return sorted(set(found))


def load_anchors(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    anchors = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            anchors.append((item["id"], item["text_anchor"]))
    return anchors


def inventory(root: Path, slug: str) -> dict:
    school = root / "schools" / slug
    text = (school / "synthesis.md").read_text(encoding="utf-8")
    anchors = load_anchors(school / "claims.jsonl")
    candidates = []
    for lineno, section, para in paragraphs(text):
        why = reasons(section, para)
        if not why:
            continue
        covered_by = [claim_id for claim_id, anchor in anchors if anchor in para]
        candidates.append({
            "line": lineno,
            "section": section,
            "reasons": why,
            "covered_by": covered_by,
            "preview": para[:180],
        })
    return {
        "slug": slug,
        "candidate_count": len(candidates),
        "covered_count": sum(bool(c["covered_by"]) for c in candidates),
        "uncovered_count": sum(not c["covered_by"] for c in candidates),
        "candidates": candidates,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("slugs", nargs="+")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    reports = [inventory(args.root, slug) for slug in args.slugs]
    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        for report in reports:
            print(f"{report['slug']}: {report['covered_count']}/{report['candidate_count']} covered; {report['uncovered_count']} uncovered")
            if args.summary_only:
                continue
            for item in report["candidates"]:
                if not item["covered_by"]:
                    why = ",".join(item["reasons"])
                    print(f"  L{item['line']} [{why}] {item['preview']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
