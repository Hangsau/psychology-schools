# P5 內容補全 pass — 自足執行規格

> 給恢復窗的 claude -p session 或 Sonnet sub-agent。本文件自足：不需要讀先前對話。
> 專案根：`C:\claudehome\projects\psychology-schools`。工作守則見 `CLAUDE.md`，當前狀態見 `HANDOFF.md`。

## 目標

48 篇學派綜述中薄尾篇目內容不足（只有概念列點，缺完整理論展開）。逐篇補全至 psychoanalysis 密度標準，同篇清 🔴。

## 待處理清單（依優先序，逐篇處理）

1. `schools/health-psychology/synthesis.md`（12.8KB，前次擴寫中斷已還原，重做）
2. `schools/transactional-analysis/synthesis.md`（19.6KB）
3. `schools/music-therapy/synthesis.md`（21.0KB）
4. `schools/functionalism/synthesis.md`（23.1KB）
5. `schools/rebt/synthesis.md`（23.6KB）
6. `schools/transpersonal-psychology/synthesis.md`（24.3KB）
7. `schools/ego-psychology/synthesis.md`（24.3KB）
8. `schools/individual-psychology/synthesis.md`（24.7KB）
9. `schools/self-psychology/synthesis.md`（24.7KB）
10. `schools/analytical-psychology/synthesis.md`（25.4KB）

## 開工前檢查

- `git status`：若有未 commit 的髒 `synthesis.md`（上次中斷的截斷殘留），先 `git checkout -- <該檔>` 還原，該篇重做。
- 先 Read `schools/psychoanalysis/synthesis.md` 全文作為密度標竿。

## 品質標準

- §3 每個核心概念一個完整段落：定義、學派實際論證、概念間關係、理論演變、原典錨定；遺漏的重要概念補上。
- §2 代表人物、§4 關鍵著作、§6 批評與後續發展同標準補全。§5 照該學派原有技術體系如實補全。
- 目標每篇 30KB 以上。
- **範圍紀律（用戶明確要求）**：只要學派內容本身。**禁止加入**臨床案例、治療對話示例、教學性延伸、練習建議。

## 事實紀律（最重要）

- 禁捏造引用、書名、年代、數字。可 WebSearch 查證；查不到不寫，或標 🟡/🟠。
- 沿用 🔵🟢🟡🟠🔴 標記與 A/B/C/D 來源等級。
- **既有 🟢/🔵 已核事實、「P3 校核」「P4 仲裁」註記與文末紀錄行一律保留，禁改禁刪**。
- 同篇 🔴 條目逐條查證：查實更正升級，查無刪除並在 §8 註明。
- 全繁體中文、禁簡體、禁圖表。

## 操作紀律（防中斷損失）

每篇完成後立即依序執行，才進下一篇：

1. `PYTHONIOENCODING=utf-8 python tools/verify.py`（須 ALL PASS）
2. `PYTHONIOENCODING=utf-8 python tools/scan-simplified.py`（須 CLEAN）
3. `git add schools/<slug>/ && git commit -m "p5: <slug> 內容補全" && git push origin master`

遇「hit your limit」立即停止：已完成的篇目均已逐篇 commit，不需補救；更新 `HANDOFF.md` 剩餘清單後結束。

## 全部完成後

- `PYTHONIOENCODING=utf-8 python tools/gen-status.py`，更新 `HANDOFF.md`（P5 薄尾完成，剩餘＝全庫深化 pass 待排），commit + push。
