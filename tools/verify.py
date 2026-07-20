#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""綜述完整性檢查：8 段是否齊全、是否有簡體、是否過小。不改檔，只回報。"""
import argparse, os, glob, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHOOLS = os.path.join(ROOT, "schools")

SECTIONS = ["定位", "代表人物", "核心理論", "著作", "方法", "批評", "問題領域", "缺口"]
# 少量常見簡體字偵測（非窮舉，粗篩）
SIMP = set("们这样对说时会来国过学习实现设计问题头亲书语")

def check(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except UnicodeDecodeError as e:
        return [f"編碼錯誤(非UTF-8):{e}"]
    issues = []
    if len(txt) < 400:
        issues.append("過小(<400B)疑失敗")
        return issues
    # 結構檢查：m3 偶爾吐 plan-check 計劃(## 步驟 N)或自我修訂便條(### 8.x)冒充綜述，
    # UTF-8 合法且 8 段關鍵字以子字串藏在內文 → SECTIONS 子字串檢查抓不到，靠標題把關。
    # 要求 `## 1.`～`## 8.` 八個編號標題都在（允許額外附錄標題，如「## 主要出處彙整」）。
    heads = [l.strip() for l in txt.split("\n") if l.startswith("## ")]
    miss_num = [n for n in range(1, 9) if not any(h.startswith(f"## {n}.") for h in heads)]
    if miss_num:
        issues.append("缺編號標題:" + "/".join(f"§{n}" for n in miss_num) + "(疑非綜述/截斷)")
    if not txt.lstrip().startswith("## 1."):
        issues.append("開頭非「## 1.」(疑 preamble/計劃文件)")
    missing = [s for s in SECTIONS if s not in txt]
    if missing:
        issues.append("缺段:" + "/".join(missing))
    simp = sorted(set(c for c in txt if c in SIMP))
    if simp:
        issues.append("疑簡體:" + "".join(simp))
    return issues

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slugs", nargs="*", help="只檢查指定 slug")
    parser.add_argument("--strict", action="store_true", help="有問題時以非零退出碼阻擋")
    args = parser.parse_args()
    bad = 0
    for syn in sorted(glob.glob(os.path.join(SCHOOLS, "*", "synthesis.md"))):
        slug = os.path.basename(os.path.dirname(syn))
        if args.slugs and slug not in args.slugs:
            continue
        issues = check(syn)
        if issues:
            bad += 1
            print(f"FAIL {slug}: {'; '.join(issues)}")
    if bad == 0:
        print("ALL PASS")
    else:
        print(f"{bad} file(s) with issues")
    sys.exit(1 if bad and args.strict else 0)

if __name__ == "__main__":
    main()
