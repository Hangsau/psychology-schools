#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生 STATUS.md 刊版：掃隊列、正文與 P5 checklist，輸出分層狀態。"""
import json, os, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "scripts", "schools.json")
SCHOOLS = os.path.join(ROOT, "schools")
OUT = os.path.join(ROOT, "STATUS.md")
P5_QUEUE = os.path.join(ROOT, "methodology", "p5-full-queue.md")

def p5_counts():
    """P5 checklist 是深化進度的 canonical source；缺檔時明確回傳未知。"""
    try:
        text = open(P5_QUEUE, encoding="utf-8").read()
    except OSError:
        return None, None
    return text.count("- [x] "), text.count("- [ ] ")

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

def evidence_summary(queue):
    stages = {"not_started": 0, "in_progress": 0, "high_risk_claims_covered": 0, "evidence_release": 0}
    verdicts = {"total": 0, "corroborated": 0, "disputed": 0, "insufficient": 0, "retrieved": 0, "unverified": 0}
    for entry in queue:
        meta = os.path.join(SCHOOLS, entry["slug"], "meta.json")
        state = {"stage": "not_started"}
        try:
            loaded = json.load(open(meta, encoding="utf-8"))
            if isinstance(loaded.get("evidence_state"), dict):
                state = loaded["evidence_state"]
        except (OSError, ValueError):
            pass
        stage = state.get("stage", "not_started")
        stages[stage if stage in stages else "not_started"] += 1
        verdicts["total"] += state.get("high_risk_claims_total", 0) or 0
        for key in ("corroborated", "disputed", "insufficient", "retrieved", "unverified"):
            verdicts[key] += state.get(key, 0) or 0
    return stages, verdicts

def main():
    q = load_queue()
    rows, counts = [], {"queued":0,"draft":0,"reviewed":0,"error":0}
    for e in q:
        slug = e["slug"]
        st, size = school_state(slug)
        counts[st] += 1
        icon = {"queued":"⬜","draft":"🟡","reviewed":"🟦","error":"🔴"}[st]
        rows.append(f"| {icon} | `{slug}` | {e['name_zh']} | {e['category']} | {st} | {size//1024 if size else 0}KB |")

    total = len(q)
    done = counts["draft"] + counts["reviewed"]
    pct = int(100*done/total) if total else 0
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    bar = "█"*(pct//5) + "░"*(20-pct//5)
    p5_done, p5_left = p5_counts()
    evidence_stages, evidence_verdicts = evidence_summary(q)
    p5_line = (
        f"- P5 全庫深化：**{p5_done}/{p5_done + p5_left}**（剩 {p5_left} 篇）"
        if p5_done is not None else
        "- P5 全庫深化：未知（找不到 methodology/p5-full-queue.md）"
    )

    lines = [
        "# STATUS — 刊版",
        "",
        f"> 引擎自動更新。最後更新：{now}",
        "",
        "## 進度",
        "",
        f"`{bar}` **{done}/{total}** ({pct}%) 已產綜述",
        "",
        f"- 🟦 P3 已校核 reviewed：{counts['reviewed']}（不等同證據已驗證）",
        f"- 🟡 草稿 draft（待校核）：{counts['draft']}",
        f"- ⬜ 待產 queued：{counts['queued']}",
        f"- 🔴 疑失敗 error（<400B，查 logs/engine.log）：{counts['error']}",
        p5_line,
        (f"- P6 主張級證據試點：{evidence_stages['in_progress']} 篇進行中；"
         f"{evidence_stages['high_risk_claims_covered']} 篇高風險覆蓋完成；"
         f"{evidence_stages['evidence_release']} 篇達發布門檻；"
         f"{evidence_stages['not_started']} 篇未開始"),
        (f"- 已登錄高風險主張：{evidence_verdicts['total']}（corroborated {evidence_verdicts['corroborated']} / "
         f"retrieved {evidence_verdicts['retrieved']} / disputed {evidence_verdicts['disputed']} / "
         f"insufficient {evidence_verdicts['insufficient']} / unverified {evidence_verdicts['unverified']}）"),
        "",
        "## 明細",
        "",
        "| | slug | 學派 | 大類 | 狀態 | 大小 |",
        "|---|------|------|------|------|------|",
        *rows,
        "",
        "---",
        "> ⚠️ `reviewed`、30KB+ 與 `tools/verify.py` ALL PASS 只表示流程／結構門檻；2026-07-20 高風險抽驗仍發現錯誤書目、人物學歷錯置與過強主張。P6 前不得稱為 evidence-verified，詳見 HANDOFF.md。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"STATUS.md updated: {done}/{total} ({pct}%)")

if __name__ == "__main__":
    main()
