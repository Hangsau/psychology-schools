#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從 schools.json 為單一 slug 寫 meta.json（domain_tags 由 domains 欄解析）。"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug = sys.argv[1]
queue = json.load(open(os.path.join(ROOT, "scripts", "schools.json"), encoding="utf-8"))
tmpl = json.load(open(os.path.join(ROOT, "scripts", "meta_template.json"), encoding="utf-8"))
entry = next((e for e in queue if e["slug"] == slug), None)
if not entry:
    print(f"no entry for {slug}", file=sys.stderr); sys.exit(1)

m = dict(tmpl)
m.update({
    "slug": slug,
    "name_zh": entry["name_zh"],
    "name_en": entry["name_en"],
    "category": entry["category"],
    "figures": [x.strip() for x in entry["figures"].replace("、", ",").split(",") if x.strip() and x.strip() != "—"],
    "domain_tags": [d for d in entry["domains"].split() if d],
    "status": "draft",
    "review_state": "pending",
    "generated_by": "claude-m3 (MiniMax-M3)",
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
})
d = os.path.join(ROOT, "schools", slug)
os.makedirs(d, exist_ok=True)
json.dump(m, open(os.path.join(d, "meta.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"meta.json written for {slug}")
