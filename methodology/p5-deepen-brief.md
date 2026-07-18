# P5 通用深化指示 — 單篇（slug 由啟動 prompt 指定）

> 自足指示檔。執行者：全新 claude session。不需讀任何先前對話。
> 目標檔案：`schools/<slug>/synthesis.md`，slug 在啟動 prompt 中給定。

## 任務

把目標檔深化到 **30KB 以上**、達密度標準。這是學術綜述庫（48 個心理學學派）的一篇學派綜述。若現況已有部分達標（先前中斷的續作），跳過已完成部分，只補缺。

## 先讀

1. 目標檔全文（現況）
2. `schools/psychoanalysis/synthesis.md` 前 100 行（密度標竿：每個概念一段完整論述——定義、學派實際論證、概念間關係、理論演變、原典錨定）
3. `methodology/p5-batch-spec.md`（品質與事實紀律，全部沿用）

## 深化方向（讀現況後自行判斷具體缺口）

- §3 核心理論主張：概念列點展開成完整理論論述；遺漏的重要概念補上。
- §2 代表人物、§4 關鍵著作書目、§6 批評與後續發展同標準補全；§5 照該學派原有技術體系如實補全。
- 特例：若 slug 為 `psychoanalysis`（標竿篇本身）或檔案已遠超 30KB（如 `biological-psychology`、`humanistic-psychology`），改為查缺模式——對照密度標準只補明確缺口與查證既有 🔴，不大幅改寫。

## 紀律

- **範圍**：只寫學派理論內容本身（理論主張、概念、論證、演變、人物、著作）。**禁止**加入臨床案例、治療對話示例、教學性延伸、練習建議。
- **事實**：禁捏造引用、書名、年代、數字；可 WebSearch 查證，查不到不寫或標 🟡/🟠。沿用 🔵🟢🟡🟠🔴 與 A/B/C/D 體系。
- **既有 🟢/🔵 已核事實與「P3 校核」「P4 仲裁」「P5 補全」紀錄行禁改禁刪。**
- 同篇既有 🔴 逐條查證：查實更正升級，查無刪除並在 §8 註明。
- 全繁體中文、禁簡體、禁圖表；標點全形。
- 完成後文末追加一行：`> 🟢 P5 補全：<今日日期>；<簡述補寫範圍與更正>`

## 操作協議（強制）

- **一律小段落 Edit**：每次 Edit 只寫一小段（≤1.5KB），逐段落盤；絕不一次生成整節或整檔。
- **禁止任何 git 操作**（不 commit、不 push、不 reset、不 checkout、不 stash）。runner 腳本負責 commit。
- 完成後跑：`PYTHONIOENCODING=utf-8 python tools/verify.py`（須 ALL PASS）與 `PYTHONIOENCODING=utf-8 python tools/scan-simplified.py`（須 CLEAN）；未過就修到過。
- 最後把完成摘要 append 到 `logs/p5-deepen-reports.md`（篇名、最終大小、補了哪些節、事實查證要點、未能查證項）。
