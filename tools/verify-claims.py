#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""驗證高風險主張證據鏈；預設報告，--strict 時任何錯誤皆非零退出。"""
import argparse
import datetime as dt
import json
import os
import re
import sys

ID_RE = re.compile(r"^[a-z0-9-]+-[0-9]{3}$")
SOURCE_RE = re.compile(r"^(doi:10\.\d{4,9}/\S+|isbn:[0-9Xx-]{10,17}|pmid:\d+|url:https://\S+)$")
TYPES = {"biographical", "bibliographic", "chronological", "quantitative", "causal", "efficacy", "attribution", "absolute"}
VERDICTS = {"unverified", "retrieved", "corroborated", "disputed", "insufficient"}
CONFIDENCE = {"low", "medium", "high"}
INDEPENDENCE = {"none", "single", "dependent", "independent"}
REQUIRED = {"id", "claim", "type", "risk", "source_ids", "source_independence", "verdict", "confidence", "checked_at", "checker", "text_anchor"}
ALLOWED = REQUIRED | {"evidence_quote"}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_claim(obj, slug, synthesis, line_no):
    issues = []
    if not isinstance(obj, dict):
        return [f"L{line_no}: 每行必須是 JSON object"]
    missing = sorted(REQUIRED - set(obj))
    extra = sorted(set(obj) - ALLOWED)
    if missing:
        issues.append(f"L{line_no}: 缺欄位 {','.join(missing)}")
    if extra:
        issues.append(f"L{line_no}: 未知欄位 {','.join(extra)}")
    claim_id = obj.get("id", "")
    if not isinstance(claim_id, str) or not ID_RE.fullmatch(claim_id) or not claim_id.startswith(slug + "-"):
        issues.append(f"L{line_no}: id 格式或 slug 前綴錯誤")
    if obj.get("type") not in TYPES:
        issues.append(f"L{line_no}: type 非法")
    if obj.get("risk") != "high":
        issues.append(f"L{line_no}: 試點只接受 high risk")
    if obj.get("verdict") not in VERDICTS:
        issues.append(f"L{line_no}: verdict 非法")
    if obj.get("confidence") not in CONFIDENCE:
        issues.append(f"L{line_no}: confidence 非法")
    if obj.get("source_independence") not in INDEPENDENCE:
        issues.append(f"L{line_no}: source_independence 非法")
    sources = obj.get("source_ids")
    if not isinstance(sources, list):
        issues.append(f"L{line_no}: source_ids 必須是 array")
        sources = []
    else:
        if len(sources) != len(set(sources)):
            issues.append(f"L{line_no}: source_ids 重複")
        for source in sources:
            if not isinstance(source, str) or not SOURCE_RE.fullmatch(source):
                issues.append(f"L{line_no}: 非法 source_id {source!r}")
    verdict = obj.get("verdict")
    independence = obj.get("source_independence")
    if verdict == "corroborated" and (len(sources) < 2 or independence != "independent"):
        issues.append(f"L{line_no}: corroborated 必須有至少兩個獨立來源")
    if verdict in {"retrieved", "corroborated", "disputed"} and not sources:
        issues.append(f"L{line_no}: {verdict} 不可沒有來源")
    if obj.get("type") == "efficacy" and verdict == "corroborated" and not any(s.startswith(("doi:", "pmid:")) for s in sources):
        issues.append(f"L{line_no}: efficacy corroborated 至少需要 DOI 或 PMID")
    try:
        dt.date.fromisoformat(obj.get("checked_at", ""))
    except (TypeError, ValueError):
        issues.append(f"L{line_no}: checked_at 必須是 YYYY-MM-DD")
    anchor = obj.get("text_anchor")
    if not isinstance(anchor, str) or len(anchor) < 4 or anchor not in synthesis:
        issues.append(f"L{line_no}: text_anchor 無法在 synthesis.md 唯一定位")
    elif synthesis.count(anchor) != 1:
        issues.append(f"L{line_no}: text_anchor 在 synthesis.md 出現不只一次")
    if not isinstance(obj.get("claim"), str) or len(obj.get("claim", "").strip()) < 4:
        issues.append(f"L{line_no}: claim 過短")
    return issues


def validate_school(root, slug, require_claims=False):
    school = os.path.join(root, "schools", slug)
    synthesis_path = os.path.join(school, "synthesis.md")
    meta_path = os.path.join(school, "meta.json")
    claims_path = os.path.join(school, "claims.jsonl")
    issues, claims = [], []
    if not os.path.exists(synthesis_path) or not os.path.exists(meta_path):
        return ["缺 synthesis.md 或 meta.json"], []
    synthesis = open(synthesis_path, encoding="utf-8").read()
    meta = load_json(meta_path)
    state = meta.get("evidence_state", {"stage": "not_started"})
    if not isinstance(state, dict) or state.get("stage") not in {"not_started", "in_progress", "high_risk_claims_covered", "evidence_release"}:
        issues.append("meta evidence_state.stage 非法")
    if not os.path.exists(claims_path):
        if require_claims or state.get("stage") != "not_started":
            issues.append("缺 claims.jsonl")
        return issues, claims
    seen = set()
    with open(claims_path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            if not raw.strip():
                issues.append(f"L{line_no}: 空白行")
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                issues.append(f"L{line_no}: JSON 錯誤 {exc.msg}")
                continue
            issues.extend(validate_claim(obj, slug, synthesis, line_no))
            claim_id = obj.get("id") if isinstance(obj, dict) else None
            if claim_id in seen:
                issues.append(f"L{line_no}: 重複 id {claim_id}")
            seen.add(claim_id)
            claims.append(obj)
    if not claims:
        issues.append("claims.jsonl 不可為空")
    counts = {v: sum(1 for c in claims if c.get("verdict") == v) for v in VERDICTS}
    if isinstance(state, dict) and state.get("stage") != "not_started":
        expected = {
            "high_risk_claims_total": len(claims),
            "corroborated": counts["corroborated"],
            "disputed": counts["disputed"],
            "insufficient": counts["insufficient"],
            "retrieved": counts["retrieved"],
            "unverified": counts["unverified"],
        }
        for key, value in expected.items():
            if state.get(key) != value:
                issues.append(f"meta evidence_state.{key}={state.get(key)!r}，應為 {value}")
        if state.get("stage") in {"high_risk_claims_covered", "evidence_release"} and counts["unverified"]:
            issues.append("覆蓋完成狀態不可含 unverified")
    return issues, claims


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--require-claims", action="store_true")
    args = parser.parse_args()
    schools_root = os.path.join(args.root, "schools")
    slugs = args.slugs or sorted(d for d in os.listdir(schools_root) if os.path.isdir(os.path.join(schools_root, d)))
    bad = 0
    for slug in slugs:
        try:
            issues, claims = validate_school(args.root, slug, args.require_claims)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues, claims = [f"讀取錯誤: {exc}"], []
        if issues:
            bad += 1
            print(f"FAIL {slug}: " + "; ".join(issues))
        elif claims:
            print(f"PASS {slug}: {len(claims)} claims")
    if bad == 0:
        print("CLAIMS ALL PASS")
    else:
        print(f"{bad} school(s) with claims issues")
    return 1 if bad and args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
