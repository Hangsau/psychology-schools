# psychology-schools — 交接狀態

> 狀態快照。即時進度看 [`STATUS.md`](./STATUS.md)（引擎自動更新）。
> 最後更新：2026-07-16（P0/P1 完成，P2 引擎啟動）

## 現況

- **P0 骨架**：✓ repo + 四份文件 + 方法論 + schema
- **P1 inventory**：✓ classification（13 類 / ~48 學派）+ 三張清單 + 13 領域對接表 + 概念詞彙
- **P2 綜述**：進行中 — `tools/run-engine.sh` 用 `claude-m3` 逐學派產草稿
- **範例錨**：Opus 親寫 2–3 篇黃金範例（引擎模仿模板）

## 引擎怎麼運作

- `tools/run-engine.sh` 讀 `scripts/schools.json` 隊列，逐一：產 `schools/<slug>/synthesis.md` → `git commit` → 跑 `gen-status.py` 更新 `STATUS.md`。
- **零 Claude 配額**（走 MiniMax `claude-m3`），撞不到 5H 牆，持續跑到隊列做完。
- skip-if-exists → 可續跑；單篇失敗記 log 續下一篇，不整個死。
- `tools/watchdog.sh`（schtasks 每 15 分）→ 引擎死了自動重啟。

## 下次接手先做

1. 看 `STATUS.md` 進度：哪些學派已產草稿、哪些失敗。
2. `logs/engine.log` 查失敗原因。
3. **P3 校核**：m3 草稿全是 🟡 pending-review，逐篇比對 `verification-sop.md` 校事實、升級。
4. 推 GitHub：目前只本地 commit（`gh repo create Hangsau/psychology-schools --public` 後 push）。

## 已知限制

- m3 草稿事實可靠度＝科普等級，需校核（尤其年代、歸屬、數字）。
- 部分學派（本土 / 非西方 / 表達性藝術）英文二手資料多於一手，缺口會多，已在各篇「已知缺口」區標。
- 未推遠端；本地 git 是目前唯一真實來源。
