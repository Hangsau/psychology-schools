# P5 單篇補全指示 — health-psychology

> 自足指示檔。執行者：全新 claude session。不需讀任何先前對話或 HANDOFF。

## 任務

把 `schools/health-psychology/synthesis.md`（目前 20KB）深化到 **30KB 以上**。這是學術綜述庫的一篇學派綜述，內容為該領域的理論史與概念體系。

## 先讀

1. `schools/health-psychology/synthesis.md` 全文（現況；§1、§2、§3.1、§3.2 前半已完成，品質已達標，不要改寫）
2. `schools/psychoanalysis/synthesis.md` 前 100 行（密度標竿：每個概念一段完整論述——定義、論證、概念間關係、演變、原典錨定）

## 要補的節（其餘不動）

- **§3.2 後半**：接在「Mason 對非特異性的修正」段之後，補 Lazarus–Folkman 交互作用模型完整展開（初級／次級評估、再評估、問題焦點與情緒焦點因應分類、1984 原著錨定）與 McEwen 的 allostasis / allostatic load 概念（1993 起）。補完後刪除該節末「本節其餘內容待補」括號句，並同步整理 §8 對應缺口敘述。
- **§3.3**：三個模型逐一展開為完整段落——Rosenstock 健康信念模式（構念、1950 年代公衛篩檢研究起源、Becker 1970 年代擴充）、Ajzen 計畫行為理論（1985；與 Fishbein 理性行動論的承接關係）、Prochaska & DiClemente 跨理論模式（階段構念、change processes、decisional balance）；再加一段模型間比較（連續體模型 vs 階段模型；意圖—行為落差與 Gollwitzer 實作意圖的回應）。
- **§3.4**：兩個假說各自展開論證與證據結構（Cohen & Wills 1985 的判別條件；Berkman & Syme 1979 設計要點）；補 received vs perceived support 之分與 Holt-Lunstad 2010 後設分析。
- **§3.5**：依 §2 已列的三個研究系列（Ader & Cohen；Kiecolt-Glaser & Glaser；Sheldon Cohen）各展開一段機制論證；補雙向通路的概念架構（神經—內分泌—免疫互聯）。
- **§3 末**：視需要新增 3.6（Leventhal 常識模型，§2 已預告「見 §3.6」）與 3.7（人格與健康研究綱領：A 型行為之興衰、敵意成分、Type D、盡責性與長壽研究）。
- **§4**：書目補齊出版資訊（可 WebSearch 核實），把「以記憶標示」免責句改為實際核實狀態；補 Lazarus & Folkman 1984、Cohen & Wills 1985、Berkman & Syme 1979、McEwen & Stellar 1993 等本次引用的關鍵文獻。
- **§6**：批評段落各展開（Ghaemi 對模式可操作性的批評出處錨定；意圖—行為落差研究；WEIRD 樣本偏誤）；後續發展補一段當代整合方向。
- **§8**：更新缺口清單（已補者移除、新增仍未查證者）。

## 紀律

- **範圍**：只寫該領域理論內容本身（理論、構念、論證、演變、人物、文獻）。禁加臨床案例、對話示例、衛教建議、練習。
- **事實**：禁捏造引用、書名、年代、數字；可 WebSearch 查證，查不到不寫或標 🟡/🟠。沿用 🔵🟢🟡🟠🔴 與 A/B/C/D 體系。
- **既有 🟢/🔵 事實與文末「P3 校核」紀錄行禁改禁刪。**
- 全繁體中文、禁簡體、禁圖表；標點全形。
- 完成後文末追加一行：`> 🟢 P5 補全：2026-07-18；<簡述補寫範圍>`

## 操作協議（強制）

- **一律小段落 Edit**：每次 Edit 只寫一小段（≤1.5KB），逐段落盤；絕不一次生成整節或整檔。
- **禁止任何 git 操作**（不 commit、不 push、不 reset、不 checkout、不 stash）。
- 完成後跑：`PYTHONIOENCODING=utf-8 python tools/verify.py`（須 ALL PASS）與 `PYTHONIOENCODING=utf-8 python tools/scan-simplified.py`（須 CLEAN）。
- 最後把完成摘要寫入 `logs/p5-health-report.md`（最終大小、補了哪些節、事實查證要點、未能查證項）。