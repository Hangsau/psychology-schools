# psychology-schools — 導航地圖

> **Legacy archive：本 repo 已由 `psychology-knowledge-atlas` 取代。以下導航只供追溯舊資料；禁止依舊決策索引啟動 P5/P6 或退役引擎。**

> 冷啟動用。要做 X 先查 §2 決策索引 + §4 踩雷點，避免窮舉讀檔。

## 1. 結構

```
psychology-schools/
├── PLAN.md / CLAUDE.md / HANDOFF.md / MAP.md   # 計畫 / 守則 / 狀態 / 導航
├── STATUS.md                                    # ★ 刊版（引擎自動更新，看進度先看這）
├── 00-overview/
│   ├── classification.md          # 13 大類 + ~48 學派分類法（吸收自原始筆記）
│   ├── schools-inventory.md       # 學派總目錄（slug / 類別 / 狀態）
│   ├── figures-inventory.md       # 代表人物總目錄
│   ├── works-inventory.md         # 原典著作書目總目錄
│   ├── concepts.md                # 心理學概念受控詞彙
│   ├── crosswalk-13-domains.md    # ★ 學派 ↔ religions-history 13 領域對接表
│   └── INDEX.md                   # 自動生
├── schools/<slug>/
│   ├── meta.json                  # 結構標籤 + domain_tags/concept_tags
│   ├── synthesis.md               # 完整綜述（8 段固定格式）
│   └── claims.jsonl               # P6 高風險主張證據鏈（試點篇）
├── methodology/verification-sop.md  # ★ 驗證流程（每篇交付前強制）
├── tools/
│   ├── run-engine.sh              # 已退役的 P2 產文引擎（保留歷史）
│   ├── watchdog.sh                # 已停用的舊引擎 watchdog
│   ├── gen-status.py             # 生 STATUS.md 刊版
│   ├── build-index.py            # 生 domain-index / concept-index
│   ├── inventory-high-risk.py     # P6 句級高風險候選盤點
│   ├── verify-claims.py           # P6 claims/meta/anchor 驗證
│   └── verify.py                  # 綜述完整性檢查
└── scripts/
    ├── schools.json              # 引擎隊列（學派 slug + 元資料）
    └── meta_template.json        # meta.json schema
```

## 2. 決策索引（要做 X → 看哪）

| 要做 | 看 |
|------|-----|
| 看目前進度 | `STATUS.md`（引擎自動更新）|
| 中斷後接手 | `HANDOFF.md` 頂端 `ACTIVE WORK` → 比對 base commit + Git diff |
| 做 P6 證據試點 | `methodology/evidence-assurance-roadmap.md` + `methodology/p6-pilot-report.md` + 該篇 `claims.jsonl` |
| 加新學派 | `00-overview/classification.md` + `scripts/schools.json` |
| 寫/校綜述 | `methodology/verification-sop.md` + `CLAUDE.md §2` |
| 對接 religions-history | `00-overview/crosswalk-13-domains.md` |
| 查舊引擎歷史 | `tools/run-engine.sh` + `HANDOFF.md`；不得重啟 |

## 3. 對接軸（一句話）

13 領域（人的問題）= 本專案與 religions-history 的共同脊椎。兩邊都用同一組 `domain_tags`。

## 4. 踩雷點

- **引擎已退役**：P6 不靠引擎、watchdog 或排程推進，不得自行重啟舊管線。
- **既有模型產物不是證據**：不論 provenance 為 MiniMax-M3、Claude 或其他模型，內容均須按主張與來源驗證，不能從模型名稱推定真偽。
- **錯誤歸因看證據**：本庫不同模型與人工階段都曾留下錯誤；只能按具體文字、commit、來源查證記錄問題，不得把整批缺陷概括歸因給某模型。
- **P6 狀態來源**：以 `claims.jsonl` + `meta.json.evidence_state` 為準；`reviewed`、篇幅與 `verify.py` 通過都不代表 evidence-verified。
- **禁製圖類**：模板不含圖表欄位，別後加。
- **版權**：可讀可引短句可列書目，不可貼全文。
- **cp950**：所有 Python 加 `PYTHONIOENCODING=utf-8`。
