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
- **當前運轉引擎 = 加鎖前的舊腳本（pid 30800，13:52 啟動至今）**：它載入的是「修好 m3 呼叫 + 強化 prompt」但**沒有單例鎖 / 沒有 fix-preamble 整合 / 沒有 UTF-8 guard** 的版本。所以：① 監控時**必須手動**跑 `fix-preamble.py` / `verify.py`（引擎不會自動修）；② 它不會自刪非 UTF-8 檔（要手動判刪，如 dbt）。新版腳本（含這些）只在引擎**重啟後**才生效。
- **pid 檔曾殘留錯值**：`logs/engine.pid` 一度是 `515`（已死的短命 process 寫的），但真正在跑的是 30800。舊腳本不寫 pid，故未被覆蓋。**已手動改回 30800**，避免 watchdog 用新（加鎖）腳本重啟時檢查到死 pid 515→誤判可啟動→與 30800 並存競爭。`logs/` 是 gitignore，pid 只是 runtime state。

## 待重生 / 頑固失敗清單（2026-07-16 15:xx 監控快照）

引擎逐一跑一遍後 exit；MISSING / <400B 的檔只在 **watchdog 重啟引擎重掃**時才重生（skip-if-exists 只跳 ≥400B）。目前待重生：

| slug | 狀態 | 失敗型態 |
|------|------|----------|
| ego-psychology | MISSING（已刪） | m3 非 UTF-8 / 截斷，UTF-8 guard 刪除 |
| existential-psychology | MISSING（已刪） | m3 吐 bare 0x85（非 UTF-8） |
| cognitive-psychology | 28B | m3 吐近空 |
| person-centered-therapy | 1B | m3 吐近空 |
| dbt | 已刪 | **新型態**：m3 沒寫正文，改吐「自我修訂便條」（`回頭檢查發現…以下是修訂版`），只有 `### 8.3/8.4` 片段、零 `## 1.` 標題；fix-preamble 抓不到，靠人工刪 |
| reality-therapy | 已刪 | 完整 31776B 草稿但含 bare 0x89（非 UTF-8，位置 31470 近尾端）；舊引擎無 UTF-8 guard 照 commit，verify 抓到後人工刪 |
| systems-family-therapy | 已刪 | **第三種垃圾型態**：m3 誤把 prompt 當「規劃任務」，吐 plan-check 計劃文件（`## 步驟 1｜目標狀態…## 步驟 6`＋`確認後可以說「開始」`），非綜述。14KB 且 UTF-8 合法，**verify.py 舊版抓不到**→已升級「缺編號標題」檢查捕捉。人工刪重生 |
| play-therapy | 已刪 | 截斷：只寫到 §2 代表人物中途（`…以及在`）即停，4830B 缺 §3–§8。升級後 verify 以「缺編號標題 §3–§8」抓到 |

- **重要**：以上這些**尚未被引擎重試過**——引擎首輪一次過，跑到就跑到，<400B/MISSING 的檔只在**引擎跑完 exit → watchdog 偵測 heartbeat 過期 + 隊列未滿 → 重啟重掃**時才由 skip-if-exists 補生。所以「連續 N 輪監控 <400B」不等於「m3 失敗 N 次」，多半是還沒輪到重試。
- **判準（改良）**：以**實際重生嘗試次數**計，非監控輪數。引擎重啟重掃後，某篇再生一次仍 <400B/壞內容 → 才算 m3 對它真正持續失敗 → 記此表標「達門檻」，停自動重試，改人工/Opus 補或換 prompt。
- 目前策略：**不強制重啟健康引擎**（避免多引擎競爭事故重演），讓引擎自然跑完 + watchdog 重啟補生。約 rest-of-queue(~1.5h) + watchdog(~15min) + 補生(~30min) ≈ 完成。

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
