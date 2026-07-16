# psychology-schools — 交接狀態

> 狀態快照。即時進度看 [`STATUS.md`](./STATUS.md)（引擎自動更新）。
> 最後更新：2026-07-16（P0/P1 完成，P2 引擎穩定運轉中）

## 現況

- **P0 骨架**：✓ repo + 四份文件 + 方法論 + schema
- **P1 inventory**：✓ classification（13 類 / ~48 學派）+ 三張清單 + 13 領域對接表 + 概念詞彙
- **P2 綜述**：✓ 引擎穩定運轉中 — `tools/run-engine.sh` 用 `claude-m3` 逐學派產草稿，`structuralism` 已完成（乾淨 8 段），其餘隊列跑中。

## 引擎怎麼運作

- `tools/run-engine.sh` 讀 `scripts/schools.json` 隊列，逐一：產 `schools/<slug>/synthesis.md` → `write-meta.py` → `gen-status.py`（更新 `STATUS.md`）→ `git commit`。
- **零 Claude 配額**（走 MiniMax `claude-m3`，token 在 `~/.minimax-token`），撞不到 5H 牆，持續跑到隊列做完（~48 篇 × ~5 分 ≈ 4 小時）。
- **單例鎖**：開頭檢查 `logs/engine.pid`，已有活引擎就直接 exit → watchdog 或手動重啟都不會產生多引擎競爭。
- skip-if-exists（synthesis.md ≥400B 就跳過）→ 可續跑；單篇失敗記 log 續下一篇。
- `tools/watchdog.sh`（schtasks `psych-schools-watchdog` 每 15 分）→ 心跳 >1200s 且隊列未完 → 重啟引擎。

## 這次 session 做過 / 踩過的坑（重要）

- **m3 呼叫 bug 已修**：原本 `env VAR=x command claude` 會爆 `env: 'command': No such file or directory`（`command` 是 bash builtin，`env` 不能 exec）。已改為直接 `claude`（binary 在 `/c/Users/hangs/.local/bin/claude`，在 PATH 上）。
- **preamble 缺陷已修**：m3 初版會在開頭加「已寫入…8 段全齊」自我摘要，並漏掉 `## 1.` 標題（內容裸接）。已在 `build_prompt` 加強：第一字元必須是 `#`、8 段標題一個都不能省。修後 `structuralism` 開頭正是 `## 1. 定位與歷史脈絡`，8 標題齊。
- **多引擎競爭事故**：`nohup ... & disown` 在 Windows 其實會存活（MSYS `ps`/`pkill` 看不到 → 誤判已死 → 重複啟動 → 多引擎搶同檔）。用 PowerShell `Get-CimInstance` + `taskkill /F /T` 才清得掉。之後加了單例鎖防復發。**教訓：查引擎死活用 PowerShell CIM，不要只信 MSYS `ps`。**

## 下次接手先做

1. 看 `STATUS.md` 進度：哪些學派已產草稿、哪些失敗（❌）。
2. `logs/engine.log` 查失敗原因（注意 log 每行會重複兩次，是 `tee` + nohup 雙重導向，無害）。
3. **P3 校核**：m3 草稿全是 🟡 pending-review，逐篇比對 `methodology/verification-sop.md` 校事實（尤其年代 / 歸屬 / 數字）、比對 known-distortions 清單、🟡→🟢 升級。
4. **推 GitHub**：目前只本地 commit。`gh repo create <owner>/psychology-schools --public` 後 push（先問用戶帳號 / repo 名）。
5. 隊列全跑完後引擎自動 exit、watchdog 見「queue complete」不動作 → 系統進 idle，屬正常。

## 已知限制

- m3 草稿事實可靠度＝科普等級，需校核（尤其年代、歸屬、數字；m3 會捏造數字）。
- 部分學派（本土 / 非西方 / 表達性藝術）英文二手資料多於一手，缺口較多，已在各篇「已知缺口」區標。
- 未推遠端；本地 git 是目前唯一真實來源。
- 引擎存活依賴本機開機 + Git Bash + `~/.minimax-token` 有效；MiniMax 月費若到期 m3 會失敗，log 會出現 auth 錯誤。
