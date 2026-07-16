#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""綜述完整性檢查：8 段是否齊全、是否有簡體、是否過小。不改檔，只回報。"""
import os, glob, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHOOLS = os.path.join(ROOT, "schools")

SECTIONS = ["定位", "代表人物", "核心理論", "著作", "方法", "批評", "13 領域", "缺口"]
# 少量常見簡體字偵測（非窮舉，粗篩）
SIMP = set("们这样对说时会来国过学习实现设计问题头亲书语")

def check(path):
    txt = open(path, encoding="utf-8").read()
    issues = []
    if len(txt) < 400:
        issues.append("過小(<400B)疑失敗")
        return issues
    missing = [s for s in SECTIONS if s not in txt]
    if missing:
        issues.append("缺段:" + "/".join(missing))
    simp = sorted(set(c for c in txt if c in SIMP))
    if simp:
        issues.append("疑簡體:" + "".join(simp))
    return issues

def main():
    bad = 0
    for syn in sorted(glob.glob(os.path.join(SCHOOLS, "*", "synthesis.md"))):
        slug = os.path.basename(os.path.dirname(syn))
        issues = check(syn)
        if issues:
            bad += 1
            print(f"FAIL {slug}: {'; '.join(issues)}")
    if bad == 0:
        print("ALL PASS")
    else:
        print(f"{bad} file(s) with issues")
    sys.exit(0)  # 只回報不擋

if __name__ == "__main__":
    main()
