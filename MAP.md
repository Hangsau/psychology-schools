# psychology-schools — 導航地圖

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
│   └── synthesis.md               # 完整綜述（8 段固定格式）
├── methodology/verification-sop.md  # ★ 驗證流程（每篇交付前強制）
├── tools/
│   ├── run-engine.sh              # ★ 持續引擎（claude-m3，零 Claude 配額）
│   ├── watchdog.sh               # 引擎死了自動重啟
│   ├── gen-status.py             # 生 STATUS.md 刊版
│   ├── build-index.py            # 生 domain-index / concept-index
│   └── verify.py                 # 綜述完整性檢查
└── scripts/
    ├── schools.json              # 引擎隊列（學派 slug + 元資料）
    └── meta_template.json        # meta.json schema
```

## 2. 決策索引（要做 X → 看哪）

| 要做 | 看 |
|------|-----|
| 看目前進度 | `STATUS.md`（引擎自動更新）|
| 加新學派 | `00-overview/classification.md` + `scripts/schools.json` |
| 寫/校綜述 | `methodology/verification-sop.md` + `CLAUDE.md §2` |
| 對接 religions-history | `00-overview/crosswalk-13-domains.md` |
| 改引擎行為 | `tools/run-engine.sh`（函式內嵌，改此檔）|
| 引擎停了 | `logs/engine.log` + `tools/watchdog.sh` |

## 3. 對接軸（一句話）

13 領域（人的問題）= 本專案與 religions-history 的共同脊椎。兩邊都用同一組 `domain_tags`。

## 4. 踩雷點

- **引擎不吃 Claude 配額**：`claude-m3` 走 MiniMax 月費，撞不到 5H。改成 `claude -p` 會吃 Claude 配額 + 撞牆，別改。
- **m3 產物是草稿**：全標 🟡 pending-review，事實需人工/Opus 校核；m3 會捏造數字。
- **禁製圖類**：模板不含圖表欄位，別後加。
- **版權**：可讀可引短句可列書目，不可貼全文。
- **cp950**：所有 Python 加 `PYTHONIOENCODING=utf-8`。
