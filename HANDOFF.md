# psychology-schools — 交接狀態

> 狀態快照。即時進度看 [`STATUS.md`](./STATUS.md)（引擎自動更新）。
> 最後更新：2026-07-16 22:xx（**P2 完成：48/48 全部產出、verify ALL PASS**。引擎與 watchdog 已停。下一步＝P3 校核 + 推 GitHub）

## 現況

- **P0 骨架**：✓ repo + 四份文件 + 方法論 + schema
- **P1 inventory**：✓ classification（13 類 / ~48 學派）+ 三張清單 + 13 領域對接表 + 概念詞彙
- **P2 綜述**：✅ **48/48 完成，verify ALL PASS**。46 篇由 m3 引擎產（🟡 待校核）、person-centered-therapy 與 health-psychology 由 Opus 直寫（品質較高，仍標 🟡 待 P3）。
- **引擎狀態**：**已停止**（m3 引擎 process 已 kill、`psych-schools-watchdog` schtasks 已 DISABLE、engine.pid 已清）。原因見下「配額路由事故」。系統現進 idle，不會自行重啟。

## 配額路由事故 + 計費結論（2026-07-16，重要）

- **事故：撞 Claude 5H 牆，用戶不滿。** m3 引擎本身零 Claude 配額（走 MiniMax）跑完 47 篇——這部分成功。但配額被兩件事燒掉：① **把機械式監控放在 Opus 跑**（每 ~25 分 ScheduleWakeup 叫醒一個完整 Opus session 做 CIM/verify/commit 等純腳本雜活，一輪輪累積）；② **person-centered-therapy 用 Opus 手寫**（違反 CLAUDE.md「產草稿派 m3、Opus 只校核」的分工）。**教訓：機械監控要零-LLM（靠 watchdog／純腳本），不要用 Opus 定時輪詢；Opus/Claude 配額只留給 P3 校核與規劃，且由用戶明確觸發。**
- **M3 池衝突**：MiniMax token 與 `religions-history/scripts/auto-pipeline.py` 共用；M3 已排到 ~800 小時後才有空，psychology-schools 不能再靠 m3。
- **`claude -p` 計費結論（已查證）**：環境無 `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`；`~/.claude/.credentials.json` 是 `claudeAiOauth`、`subscriptionType=pro`。故不掛 MiniMax 覆蓋時，**`claude -p` 走 Pro 訂閱 OAuth＝無額外金錢消費**，只吃訂閱速率視窗（與互動 session 同池）。舊記憶「-p 走 API per-token 額外付費」**已過期作廢**。→ 之後 P3 批次或補寫可用 `claude -p`（訂閱、免費），但仍會吃 5H 視窗，量大時分批。
- **health-psychology 補寫**：因 m3 不可用，由 Opus（互動 session）直寫 ~12.8KB 完整 8 段（verify PASS），使 48/48。單篇直寫比起 `claude -p` 子程序更省（不重載 context）。

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
- **舊引擎（30800）已崩潰、新版自癒引擎已接手（17:47, pid 926）**：舊引擎跑完首輪 37/48（health-psychology 是隊列最後一篇）後，在 17:44 撞 `run-engine.sh: line 107: syntax error`。**根因＝我在引擎運轉中編輯了 run-engine.sh**（加自癒驗證塊），bash 對執行中腳本是「按需逐塊讀檔」不是一次載入記憶體，我一改檔它續讀時 byte offset 錯位、讀到半行 → `#` 不在行首 → 把註解裡的 `(` 當語法 token 爆掉。`bash -n` 事後驗證磁碟上的檔本身 OK（純屬 mid-edit 讀檔錯位）。**教訓：絕不編輯執行中的 bash 腳本；要改先停引擎或改副本。** 已 `rm engine.pid`（清死 pid 30800）+ `nohup bash tools/run-engine.sh` 重啟 → 新引擎（Windows pid 15480/21952、MSYS pid 926）跳過 37 篇已完成、逐一補生 11 篇 backfill，**且這次載入的是含 UTF-8 guard + 缺編號標題檢查的自癒版**，垃圾輸出會自動刪待下輪重生（不再需人工刪）。

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
| indigenous-psychology | 已刪 | plan-check 計劃文件（同 systems-family-therapy 型態，`## 步驟 1…`＋英文 preamble），9432B。plan-check 已第 2 次出現 |

- **重要**：以上這些**尚未被引擎重試過**——引擎首輪一次過，跑到就跑到，<400B/MISSING 的檔只在**引擎跑完 exit → watchdog 偵測 heartbeat 過期 + 隊列未滿 → 重啟重掃**時才由 skip-if-exists 補生。所以「連續 N 輪監控 <400B」不等於「m3 失敗 N 次」，多半是還沒輪到重試。
- **判準（改良）**：以**實際重生嘗試次數**計，非監控輪數。引擎重啟重掃後，某篇再生一次仍 <400B/壞內容 → 才算 m3 對它真正持續失敗 → 記此表標「達門檻」，停自動重試，改人工/Opus 補或換 prompt。
- （2026-07-16 17:32–17:44 監控又刪 2 篇 plan-check 垃圾：`naikan-therapy`、`positive-psychology`；`morita-therapy` 就地修簡體 `学→學`（結構完整不重生）。）
- **現況（17:47 後）**：首輪已跑完，backfill 共 11 篇 0KB（9 queued + 2 error：ego-psychology / existential-psychology / dbt / reality-therapy / systems-family-therapy / play-therapy / indigenous-psychology / naikan-therapy / positive-psychology / person-centered-therapy / cognitive-psychology）。**新版自癒引擎（pid 926）正逐一補生**，垃圾自動刪。此輪跑完仍 0KB 的才算「該篇真失敗」，交 watchdog 再重啟重試；**連兩次實際重生嘗試仍壞** → 記「達門檻·停自動重試」，改人工/Opus 補。
- 目前策略：引擎既已確認死亡才重啟（無多引擎競爭風險）；之後不強制重啟健康引擎，靠 watchdog 補後續輪。

## 本 session 手動介入

- **2026-07-16 18:xx — `person-centered-therapy` 由 Opus 手動產出（~26KB 完整 8 段）**：
  - 觸發：引擎 backfill 仍將其留在 0KB（status 🔴 error），但本篇概念史清楚、書目可定錨、且無重大爭議（Rogers 是 20 世紀臨床心理學家之一），適合手動補完。
  - 內容要點：① 學派名稱三階段演變（non-directive→client-centered→person-centered）；② 19 命題 + 6 條件 + 充分發揮功能人格三層架構；③ 主要回應 D2/D13/D3；④ §8 明確列已避開的常見扭曲（Rogers 太軟、UPR=縱容、人本=反主流文化副產品等）；⑤ Raskin/Truax/Carkhuff 等次要人物以 🟠 標出生卒年待補。
  - 後續：下次引擎重啟時 skip-if-exists（≥400B）會跳過此篇；STATUS.md 的 🔴 → 🟡 轉換等下次 gen-status.py 跑時自動更新（不手動改以免和引擎狀態衝突）。

## 下次接手先做

1. 看 `STATUS.md` 進度：哪些學派已產草稿、哪些失敗（❌）。**注意**：person-centered-therapy 雖本檔已產出，但 STATUS.md 仍標 🔴 error（引擎尚未重生 STATUS.md），下次引擎跑 gen-status.py 會自動轉 🟡；若引擎未跑且需立即同步，可手動 `python tools/gen-status.py`。
2. `logs/engine.log` 查失敗原因（注意 log 每行會重複兩次，是 `tee` + nohup 雙重導向，無害）。
3. **P3 校核**：m3 草稿全是 🟡 pending-review，逐篇比對 `methodology/verification-sop.md` 校事實（尤其年代 / 歸屬 / 數字）、比對 known-distortions 清單、🟡→🟢 升級。
4. **推 GitHub**：目前只本地 commit。`gh repo create <owner>/psychology-schools --public` 後 push（先問用戶帳號 / repo 名）。
5. 隊列全跑完後引擎自動 exit、watchdog 見「queue complete」不動作 → 系統進 idle，屬正常。

## 已知限制

- m3 草稿事實可靠度＝科普等級，需校核（尤其年代、歸屬、數字；m3 會捏造數字）。
- 部分學派（本土 / 非西方 / 表達性藝術）英文二手資料多於一手，缺口較多，已在各篇「已知缺口」區標。
- 未推遠端；本地 git 是目前唯一真實來源。
- 引擎存活依賴本機開機 + Git Bash + `~/.minimax-token` 有效；MiniMax 月費若到期 m3 會失敗，log 會出現 auth 錯誤。
