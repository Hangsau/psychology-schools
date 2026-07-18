# P5 單篇深化指示 — biopsychosocial-model

> 自足指示檔。執行者：全新 claude session。不需讀任何先前對話。

## 任務

把 `schools/biopsychosocial-model/synthesis.md`（目前 26.1KB）深化到 **30KB 以上**。這是學術綜述庫的一篇學派綜述，內容為該理論模型的思想史與概念體系。

## 先讀

1. `schools/biopsychosocial-model/synthesis.md` 全文（現況）
2. `schools/psychoanalysis/synthesis.md` 前 100 行（密度標竿：每個概念一段完整論述——定義、論證、概念間關係、演變、原典錨定）
3. `methodology/p5-batch-spec.md`（品質與事實紀律；本篇沿用全部標準）

## 深化方向（讀現況後自行判斷具體缺口）

- §3 各核心主張逐一展開為完整段落：Engel 1977/1980 兩篇原典的論證結構（對化約論與二元論的批判、von Bertalanffy 系統層級架構、1980 個案應用篇）、模型的科學主張 vs 臨床態度主張之辨、與 Meyer 心理生物學（psychobiology）的思想承接。
- §2 人物條目補深（Engel 傳記脈絡、Romano 合作關係、後繼發展者如 Borrell-Carrió）。
- §6 批評深化：Ghaemi《The Rise and Fall of the Biopsychosocial Model》（2010）論證錨定、「折衷主義」批評與辯護方回應、McLaren 的批評、當代修正提案（如 Bolton & Gillett 2019）。
- §4 書目補齊出版資訊；§8 缺口清單同步更新。

## 紀律

- **範圍**：只寫該模型理論內容本身（理論、論證、演變、人物、文獻）。禁加臨床案例、對話示例、應用指南、練習。
- **事實**：禁捏造引用、書名、年代、數字；可 WebSearch 查證，查不到不寫或標 🟡/🟠。沿用 🔵🟢🟡🟠🔴 與 A/B/C/D 體系。
- **既有 🟢/🔵 事實與文末「P3 校核」等紀錄行禁改禁刪。**
- 全繁體中文、禁簡體、禁圖表；標點全形。
- 完成後文末追加一行：`> 🟢 P5 補全：2026-07-18；<簡述補寫範圍>`

## 操作協議（強制）

- **一律小段落 Edit**：每次 Edit 只寫一小段（≤1.5KB），逐段落盤；絕不一次生成整節或整檔。
- **禁止任何 git 操作**。
- 完成後跑：`PYTHONIOENCODING=utf-8 python tools/verify.py`（須 ALL PASS）與 `PYTHONIOENCODING=utf-8 python tools/scan-simplified.py`（須 CLEAN）。
- 最後把完成摘要寫入 `logs/p5-bpsm-report.md`（最終大小、補了哪些節、事實查證要點、未能查證項）。
