#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修 m3 間歇缺陷：開頭塞 self-summary preamble 且把「## 1. 定位與歷史脈絡」標題吃掉。
偵測：檔案不以 `## 1.` 開頭。修法：
  - 若第一個標題就是 `## 1.`（preamble 在標題前）→ 砍掉標題前所有行。
  - 若第一個標題是 `## 2.`（§1 標題被吃）→ 砍掉開頭 preamble 段落，補回 `## 1. 定位與歷史脈絡`。
用法：python tools/fix-preamble.py [slug]  # 無 slug = 掃全部。只回報有改的。
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIG = re.compile(r"synthesis\.md|已寫入|寫入 `|寫入了|[0-9]+\s*段|字；|字，|KB）|KB\)|行 /|行/|綜述已|已完成|以下是|已為|全齊|齊全")

def fix_one(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except UnicodeDecodeError:
        return False  # 非 UTF-8 交給 verify.py 報告 / 由監控刪除重生
    lines = txt.split("\n")
    if lines and lines[0].lstrip().startswith("## 1."):
        return False
    hidx = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
    if hidx is None:
        return False
    first_h = lines[hidx].strip()
    if first_h.startswith("## 1."):
        new = lines[hidx:]
    elif first_h.startswith("## 2."):
        block, rest = lines[:hidx], lines[hidx:]
        j = 0
        while j < len(block) and block[j].strip() == "":
            j += 1
        # 砍掉開頭符合 preamble 特徵的段落（到空行為止）
        if j < len(block) and SIG.search(block[j]):
            while j < len(block) and block[j].strip() != "":
                j += 1
            while j < len(block) and block[j].strip() == "":
                j += 1
        sec1 = block[j:]
        new = ["## 1. 定位與歷史脈絡", ""] + sec1 + rest
    else:
        return False
    out = "\n".join(new)
    if out != txt:
        open(path, "w", encoding="utf-8").write(out)
        return True
    return False

def main():
    if len(sys.argv) > 1:
        paths = [os.path.join(ROOT, "schools", sys.argv[1], "synthesis.md")]
    else:
        paths = sorted(glob.glob(os.path.join(ROOT, "schools", "*", "synthesis.md")))
    fixed = 0
    for p in paths:
        if os.path.exists(p) and os.path.getsize(p) >= 400 and fix_one(p):
            fixed += 1
            print("fixed", os.path.basename(os.path.dirname(p)))
    print(f"{fixed} file(s) fixed" if fixed else "nothing to fix")

if __name__ == "__main__":
    main()
