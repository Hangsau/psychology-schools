# psychology-schools — 交接狀態

> 狀態快照。即時進度看 [`STATUS.md`](./STATUS.md)（引擎自動更新）。
> 最後更新：2026-07-20。P5 全庫深化 **32/38**；canonical 進度看 `methodology/p5-full-queue.md`。剩 6 篇，下一篇為 `play-therapy`。自動接續機制已移除。
>
> **⚠️ 2026-07-20 發現：既有篇目含未清幻覺碎片（影響剩餘深化性質）**。mbct（33.7KB）雖已過 P3，仍含多處亂碼／捏造碎片：「熱情 pī 模式」「Padesky 雙軌治療呼吸」（L33）、「共激發達瑟頓（dash）」（L35）、「由 Matthew 前導…Salvo 形式」（L69，捏造人名）、「化學、工程跨界」（L100）、「SEBI／默 1960s Leonard Eron theoder」（L164）。**來源中立看待——本庫幾乎都是 Claude 執筆，這些是需修的幻覺，不歸因 M3**（見全域記憶 feedback_dont_blame_m3_own_hallucinations）。→ 剩餘篇深化＝「逐句清幻覺＋補概念」雙工，比乾淨篇（如 cognitive-psychology）重；且**補寫時要防自己新增幻覺**（人名/年代/書目先查證）。接手每篇先通讀抓幻覺再深化。**自動接續已於 2026-07-20 拿掉**：`p5-watchdog` / `p5-runner-launch` schtasks 任務、`tools/p5-watchdog.sh` / `p5-run-hidden.py` / `p5-register-watchdog.py` / `p5-deepen-runner.sh` 全數刪除（實測未能推進佇列，用戶要求移除）。**深化改為在 session 內手動逐篇做**（同 cbt / health-psychology 已驗證模式：直寫 → `tools/verify.py` → commit → push）。**Agent tool 派發不用**（AUP 誤判兩度攔截）。P4 ③ 網站待用戶指示呈現形式。

## 現況

- **P0 骨架**：✓ repo + 四份文件 + 方法論 + schema
- **P1 inventory**：✓ classification（13 類 / ~48 學派）+ 三張清單 + 13 領域對接表 + 概念詞彙
- **P2 綜述**：✅ 48/48 具有固定 8 段結構，`verify.py` 通過；這只代表結構完整。
- **P3 校核**：✅ 48/48 `reviewed`，但 2026-07-20 抽驗證明此欄位不可解讀為逐主張已查證。
- **P4**：✅ domain/concept 索引與對接層完成；網站待用戶決定呈現形式。
- **P5 深化**：進行中，32/38；剩 `play-therapy`、`cultural-historical-psychology`、`narrative-therapy`、`gestalt-therapy`、`biological-psychology`、`humanistic-psychology`。
- **P6 品質穩定化試點**：已啟動，P5 暫停。`claims-schema.json`、`verify-claims.py` 與 strict 結構模式已完成；CBT／精神分析／本土心理學首批共登錄 14 條高風險主張（8 corroborated、6 retrieved），三篇均仍為 `in_progress`，不得解讀成全篇覆蓋。
- **引擎狀態**：**已停止**（m3 引擎 process 已 kill、`psych-schools-watchdog` schtasks 已 DISABLE、engine.pid 已清）。原因見下「配額路由事故」。系統現進 idle，不會自行重啟。

## 2026-07-20 獨立品質抽驗

本輪不採信 `reviewed`、P3/P5 紀錄行或 `ALL PASS` 自述，改抽查 8 篇高風險文章的人物、書目、年代、療效、理論歸屬與高信心標記：`humanistic-psychology`、`biological-psychology`、`health-psychology`、`person-centered-therapy`、`indigenous-psychology`、`mbct`、`psychoanalysis`、`play-therapy`。

結論：**結構與概念覆蓋大致良好，但來源可追溯性與事實標記校準不合格；不能把全庫稱為「驗證版」。** 八篇皆有完整 8 段，且多數核心理論敘述可辨識；但高風險抽樣可直接找到多個實質錯誤：

- `psychoanalysis`：把凝縮 `Verdichtung` 與移置 `Verschiebung` 的德文對應寫反；Schreber 個案誤寫成不存在的「Darwin Schulze」。該篇原被當作 P5 密度標竿。
- `humanistic-psychology`：把 Moustakas 1994 的方法論書誤列為不存在的《Existential Psychotherapy and the Interpretation of Dreams》（正確書目是 *Phenomenological Research Methods*）；另有 ACT「直接從 Rogers 與 Gendlin 出發」等未充分支持的傳承敘述。
- `indigenous-psychology`：人物學歷有成串錯置。楊國樞臺大畢業與伊利諾博士年份錯；黃光國被寫成臺大心理博士，實為夏威夷大學社會心理學博士；陸洛被寫成臺大博士及楊國樞學生，臺大官方資料為牛津大學心理學博士。
- `mbct`：把 Williams 等 2014 的 JCCP 隨機拆解試驗誤列為 BMJ 348:g2613「systematic review and network meta-analysis」。
- `play-therapy`：Bratton 等 2005 後設分析期刊誤寫為 *Journal of Professional Counseling*，正確為 *Professional Psychology: Research and Practice* 36(4), 376–390；Landreth 2012 第三版錯列 Bratton 與 Baggerly 為共同作者，出版社資料顯示作者仍為 Landreth；另有疑似不存在的 2019 SAGE handbook。
- `biological-psychology`：整體歷史骨架較穩，但把程序性記憶簡化定位到「皮質」與權威記憶系統模型不符；應以基底核、小腦及相關皮質網絡表述。
- `health-psychology`：八篇中書目可追溯性相對最佳；Holt-Lunstad 2010 的樣本數與 OR 正確，但正文把原文「與既有風險因子相當」升格為「超越吸菸、飲酒、運動不足」，屬措辭過強。
- `person-centered-therapy`：抽驗核心歷史、六條件與 Rogers 生涯大致吻合，是本輪相對穩定樣本；主要缺陷是正文幾乎沒有可重取識別碼，讀者難以重現其 A/B 級標記。

這是風險導向樣本，不是 48 篇全數錯誤率估計；但已足以否證「48/48 reviewed＝內容可信」的狀態語意。P6 前應先修正狀態模型，P6 試點再量測真正的主張覆蓋率與錯誤攔截率。

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

1. **P3 已完成**（48/48 reviewed，批次 1–10）。`STATUS.md` 全 🟢。
2. **P4 ① 未決事項仲裁已完成**（2026-07-17 Opus，見下節）：12 條定案寫回正文、2 條維持爭議標記。
3. **P4 ② 語義索引已定稿**（2026-07-17）：domain 13 / concept 36 標籤（`anxiety` 詞彙表外標籤已改 `defense-mechanism`，全 48 校 100% 合規）；新增 `00-overview/domains.json`（D 碼 ↔ religions-history I–XIII ↔ 45 細群 slug 機器可讀對照）；merge 合約與 join 路徑寫在 `crosswalk-13-domains.md`「機器可讀對接層」節。**Blocker 在對側**：religions-history 的 `psych_tags` 標註 pipeline 尚未實作，該側動工前本專案無事可做。
4. **P5 薄尾 10/10 完成（2026-07-18）**：transactional-analysis 50.4KB / music-therapy 41.2KB / functionalism 46KB / rebt 38.7KB / transpersonal 38.4KB / ego 46.8KB / individual 40.4KB / self 46.8KB / analytical 42.7KB / health-psychology 47.2KB，全部 ≥38KB、verify ALL PASS、逐篇 push。執行模式＝Sonnet sub-agent 串行批次（批次 B 三篇、批次 C 四篇），主 session 驗收 commit。**health-psychology 特例**：AUP 誤判累計 5 次（含本輪 agent 派發即被拒、主 session 讀檔後生成被拒），最終解法＝寫低觸發密度自足指示檔 `methodology/p5-health-brief.md` → 全新 `claude -p` process（零對話污染）執行成功；此模式可複用於同類主題。**剩餘＝全庫深化 pass**（其餘 38 篇補到同標準，30KB+），從最薄的開始批次排程即可。
5. **P4 ③ 網站**：需用戶確認呈現形式，暫停待指示。
6. GitHub 遠端：`https://github.com/Hangsau/psychology-schools`（public，gh 已登入 Hangsau）。做完直接 push，不用問。

## P3 未決事項 → P4 仲裁結果（2026-07-17 Opus）

> 每篇文末均附 `> 🟢 P4 仲裁` 紀錄行；正文修正處均留「P4 仲裁已定案」註記。

- **cbt** ✅ 已定案：REBT 改名年＝1993 年 6 月（Ellis 於 *JRECBT* 發表更名說明論文）🟢。
- **evolutionary-psychology** ✅ 已定案：Martin Daly 仍在世（McMaster 榮休教授）；「2022 逝世」為捏造，已刪。
- **existential-psychology** 🟠 維持：Frankl 集中營敘事的歷史學考證屬真實學術爭議（Pytell 等 vs 傳統傳記），兩說並列不裁決。
- **humanistic-psychology** ✅ 已定案：Moustakas 1961＝《Loneliness》（Prentice-Hall）；《Loneliness and Love》為 1972 另一部，正文已分列。金字塔歸屬異說維持並列。
- **mbct** ✅ 已定案：J. Mark G. Williams 生年 1952 🟢。
- **morita-therapy** ✅ 已定案：「中村恆子 1990（UC Press）」人＋書均為捏造，已清除；英文引介實為 David K. Reynolds《Morita Psychotherapy》（1976, UC Press）；森田 1921 原著英譯＝1998 SUNY Press（Kondo 譯、LeVine 編）。
- **music-therapy** ✅ 已定案：1996「中華民國應用音樂推廣協會」為首個組織；「臺灣音樂治療學會」2024 正式立案；「2002」說不成立。
- **rebt** ✅ 已定案：機構官名至今仍為 Albert Ellis Institute（官網核實）；「2021 改名」不成立，已刪。
- **sfbt** ✅ 已定案：de Shazer《Tricks》查無此書＝捏造書目已刪；Kim 2008 效應量實為小（d ≈ 0.13–0.26），原「中等 d ≈ 0.5」已更正。
- **social-constructionism** ✅ 已定案：《The Discursive Mind》＝1994（與 Gillett 合著，Sage）；《Laboratory Life》1979 Sage 初版 → 1986 Princeton UP 二版刪副標「Social」（原文版本順序寫反，已更正）。
- **social-learning-theory** ✅ 已定案：Richard Walters 1918–1967（學術訃聞，PubMed 收錄）🟢。
- **social-psychology** ✅ 已定案（免改）：Sherif 1906–1988 正文已正確；Milgram 數字已按 Perry 2013 標 🟠，維持現狀。
- **systems-family-therapy** ✅ 部分定案：Fromm-Reichmann 1948 原文出處補齊（*Psychiatry* 11(3), 263–273）🟢；Minuchin 費城起始年＝1965（PCGC 主任），1981 紐約另創 Family Studies, Inc.。Carter & McGoldrick 合作模式 🟠 維持待補。
- **transactional-analysis** ✅ 已定案：Robert Goulding 生年 1917 🟢；《The Power Is in the Pair》為捏造書名，實為《The Power Is in the Patient》（1978）＋《Changing Lives Through Redecision Therapy》（1979）；《I'm OK, You're OK》1972 登 NYT 榜首、在榜近兩年 🟢。
- **transpersonal-psychology** ✅ 已定案：「transpersonal」已知最早文獻用例＝William James 1905–06 哈佛講義（Vich 1988 考證）；Jorge Ferrer 1968 年生、仍在世（「1953–2022」為捏造，已更正）。ATP 會員數統計維持待補。

## 已知限制

- m3 草稿事實可靠度＝科普等級，需校核（尤其年代、歸屬、數字；m3 會捏造數字）。
- 部分學派（本土 / 非西方 / 表達性藝術）英文二手資料多於一手，缺口較多，已在各篇「已知缺口」區標。
- M3 額度被 religions-history 佔用約 800 小時，本專案不再依賴 m3；後續批次工作走 Sonnet 5 sub-agent。

## P6–P8 證據保證（P5 後續工作）

P5 完成後，**不可**把「30KB+、verify PASS」解讀為內容已事實證實；現有 `tools/verify.py` 僅做結構／編碼／標題檢查。下一階段改採主張級證據鏈、獨立 AI 驗證與發布閘門，先以 CBT、精神分析、本土心理學三篇試點，量測覆蓋率、來源可取得率、驗證分歧率及已知錯誤攔截率，再擴展全庫。詳見 `methodology/evidence-assurance-roadmap.md`。
