#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""簡體殘留掃描：OpenCC s2t 逐行轉換比對，差異處即疑似簡體字。

原理：對每行做 s2t（簡→繁）轉換，繁體字不動、簡體字被轉換 → diff 出殘留。
比字元清單掃描可靠（清單法會誤報簡繁同形字如「值」）。

用法：
  python tools/scan-simplified.py          # 只回報
  python tools/scan-simplified.py --fix    # 就地以 s2t 建議字修正（僅改 diff 字元）
"""
import os, glob, sys

from opencc import OpenCC
S2T = OpenCC("s2t")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHOOLS = os.path.join(ROOT, "schools")

# OpenCC s2t 字典會把「台灣標準字」轉成舊正字/異體（床→牀、群→羣、台→臺、
# 峰→峯、秘→祕、核→覈…），這些不是簡體殘留，一律忽略。
# 另一類是簡繁一對多的語境字（干/系/了/占/只/里…），台灣文本本來就用，也忽略。
# 2026-07-16 全庫掃描實測 41 種 diff，僅 8 種是真簡體（見 git log），其餘全在此表。
IGNORE = set("床群台峰秘核干布才里欲系灶了占托岩克只伙制借念游征糊局周向雇辟表吃后")
# 注意：内(U+5185)/彦/恒/么/乐/体/强/痴 是真殘留，不在 IGNORE。

def scan_file(path, fix=False):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    findings = []          # (lineno, col, orig, sugg, context, auto_fixable)
    new_lines = []
    for i, line in enumerate(lines, 1):
        # 含假名或日式新字體標記字（観）的行＝逐字引用的日文書名/原文，字形保留不動
        if "観" in line or any("぀" <= ch <= "ヿ" for ch in line):
            new_lines.append(line)
            continue
        conv = S2T.convert(line)
        if len(conv) != len(line):
            # 長度不對齊（罕見，詞級轉換），整行報告、不自動修
            if conv != line:
                findings.append((i, 0, line.strip()[:40], conv.strip()[:40], "", False))
            new_lines.append(line)
            continue
        fixed = list(line)
        for j, (a, b) in enumerate(zip(line, conv)):
            if a != b and a not in IGNORE:
                ctx = line[max(0, j - 10): j + 11]
                findings.append((i, j + 1, a, b, ctx, True))
                if fix:
                    fixed[j] = b
        new_lines.append("".join(fixed))
    if fix and findings:
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(new_lines))
    return findings

def main():
    fix = "--fix" in sys.argv
    total = 0
    for syn in sorted(glob.glob(os.path.join(SCHOOLS, "*", "synthesis.md"))):
        slug = os.path.basename(os.path.dirname(syn))
        findings = scan_file(syn, fix=fix)
        for (ln, col, orig, sugg, ctx, auto) in findings:
            total += 1
            tag = "FIXED" if (fix and auto) else "FOUND"
            print(f"{tag} {slug}:{ln}:{col} {orig}→{sugg}  …{ctx}…")
    print("CLEAN" if total == 0 else f"{total} finding(s)")

if __name__ == "__main__":
    main()
