#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生 STATUS.md 刊版：掃 scripts/schools.json 隊列 + schools/ 實況，出進度總表。"""
import json, os, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "scripts", "schools.json")
SCHOOLS = os.path.join(ROOT, "schools")
OUT = os.path.join(ROOT, "STATUS.md")

def load_queue():
    with open(QUEUE, encoding="utf-8") as f:
        return json.load(f)

def school_state(slug):
    d = os.path.join(SCHOOLS, slug)
    syn = os.path.join(d, "synthesis.md")
    meta = os.path.join(d, "meta.json")
    if not os.path.exists(syn):
        return "queued", 0
    size = os.path.getsize(syn)
    review = "draft"
    if os.path.exists(meta):
        try:
            m = json.load(open(meta, encoding="utf-8"))
            if m.get("review_state") == "reviewed":
                review = "reviewed"
        except Exception:
            pass
    # too-small file = likely failed
    if size < 400:
        return "error", size
    return review, size

def main():
    q = load_queue()
    rows, counts = [], {"queued":0,"draft":0,"reviewed":0,"error":0}
    for e in q:
        slug = e["slug"]
        st, size = school_state(slug)
        counts[st] += 1
        icon = {"queued":"⬜","draft":"🟡","reviewed":"🟢","error":"🔴"}[st]
        rows.append(f"| {icon} | `{slug}` | {e['name_zh']} | {e['category']} | {st} | {size//1024 if size else 0}KB |")

    total = len(q)
    done = counts["draft"] + counts["reviewed"]
    pct = int(100*done/total) if total else 0
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    bar = "█"*(pct//5) + "░"*(20-pct//5)

    lines = [
        "# STATUS — 刊版",
        "",
        f"> 引擎自動更新。最後更新：{now}",
        "",
        "## 進度",
        "",
        f"`{bar}` **{done}/{total}** ({pct}%) 已產綜述",
        "",
        f"- 🟢 已校核 reviewed：{counts['reviewed']}",
        f"- 🟡 草稿 draft（待校核）：{counts['draft']}",
        f"- ⬜ 待產 queued：{counts['queued']}",
        f"- 🔴 疑失敗 error（<400B，查 logs/engine.log）：{counts['error']}",
        "",
        "## 明細",
        "",
        "| | slug | 學派 | 大類 | 狀態 | 大小 |",
        "|---|------|------|------|------|------|",
        *rows,
        "",
        "---",
        "> 🟡 草稿由 `claude-m3` 產生，事實需 P3 人工/Opus 校核（見 methodology/verification-sop.md）。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"STATUS.md updated: {done}/{total} ({pct}%)")

if __name__ == "__main__":
    main()
