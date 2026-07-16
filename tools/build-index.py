#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從各 schools/<slug>/meta.json 反向構建 domain-index / concept-index。"""
import json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHOOLS = os.path.join(ROOT, "schools")
OV = os.path.join(ROOT, "00-overview")

def main():
    domain, concept = {}, {}
    for meta in glob.glob(os.path.join(SCHOOLS, "*", "meta.json")):
        try:
            m = json.load(open(meta, encoding="utf-8"))
        except Exception:
            continue
        slug = m.get("slug") or os.path.basename(os.path.dirname(meta))
        for t in m.get("domain_tags", []):
            domain.setdefault(t, []).append(slug)
        for t in m.get("concept_tags", []):
            concept.setdefault(t, []).append(slug)
    json.dump(domain, open(os.path.join(OV, "domain-index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)
    json.dump(concept, open(os.path.join(OV, "concept-index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)
    print(f"domain-index: {len(domain)} tags; concept-index: {len(concept)} tags")

if __name__ == "__main__":
    main()
