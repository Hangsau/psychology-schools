# psychology-schools — AI 工作守則

> 給未來接手的 Claude / m3 / 其他 AI agent。
> 計畫見 [`PLAN.md`](./PLAN.md)，狀態快照見 [`HANDOFF.md`](./HANDOFF.md)，導航見 [`MAP.md`](./MAP.md)。

## 一句話

心理學學派**完整內容**綜述庫。每學派一個 `schools/<slug>/`，內含 `meta.json` + `synthesis.md`。與 `religions-history` 共用 13 領域對接軸。

## 當前階段

**P3 已完成；P4 語義索引已完成、網站待決；P5 暫停在 32/38；當前＝P6 品質穩定化試點。**

- 48 學派均已有綜述並標為 `reviewed`；此狀態只表示做過 P3 校核，**不表示主張已獲可重現證據保證**。
- 2026-07-20 高風險抽驗確認既有綠燈過度樂觀：抽樣中仍有錯誤書目、人物學歷錯置、術語對應錯誤及把單一／模糊來源標成 🔵🟢 的情形。品質基線見 `HANDOFF.md`。
- P5 canonical 進度看 `methodology/p5-full-queue.md`；剩餘 `play-therapy`、`cultural-historical-psychology`、`narrative-therapy`、`gestalt-therapy`、`biological-psychology`、`humanistic-psychology`。
- `tools/verify.py` 只驗結構／編碼／標題；`scan-simplified.py` 只驗簡繁。`ALL PASS`、30KB+、`reviewed` 均不得寫成「事實已驗證」。
- 引擎與自動接續機制均已退役；後續採 session 內手動工作。
- 原規劃為 P5 凍結後進 P6；因抽驗已證明擴寫會放大污染，2026-07-20 決定暫停 P5、提前做 P6 試點。在 P6–P8 門檻通過前，不得對外標示為 evidence-verified。
- P6 試點為 `cbt`、`psychoanalysis`、`indigenous-psychology`；進度必須以 `claims.jsonl` 與 `meta.json.evidence_state` 為準，執行 `python tools/verify-claims.py --strict --require-claims <slug>` 驗收。

### 中斷恢復（強制）

- 開工前先讀 `HANDOFF.md` 頂端 `ACTIVE WORK`。若 `status` 不是 `validated`，必須先依 `base_commit`、`git status`、`git diff` 判斷半成品，完成或明確處置後才開始新單位。
- 每個小批次採 write-ahead checkpoint：先把篇目、章節／候選範圍、基準 commit、目標檔、預期結果與下一步寫入 `ACTIVE WORK`，再修改正文或證據資料。
- 未同步 `synthesis.md`、`claims.jsonl`、`meta.json` 且未通過 strict validator 前，一律維持 `started`／`in_progress`，不得宣稱完成。
- 模型或作者名稱只記 provenance，不作錯誤歸因。錯誤紀錄必須指向具體文字、commit 與查證證據；不得把 Claude、MiniMax-M3 或任何模型概括為整批問題來源。

## 工作守則

### 1. 寫任何學派綜述前
- 查 `00-overview/classification.md` — 該學派屬哪一大類、思想淵源？
- 查 `00-overview/schools-inventory.md` — 已收哪些？
- 讀 `methodology/verification-sop.md` — 驗證流程強制。

### 2. 綜述標準形式（`schools/<slug>/synthesis.md`）
固定段落：① 定位與歷史脈絡 ② 代表人物 ③ 核心理論主張（完整，非簡介）④ 關鍵著作書目（含年代）⑤ 方法 / 技術 ⑥ 批評與後續發展 ⑦ 對接 13 領域 ⑧ 已知缺口 / 未驗證 / 爭議。
- 全繁體中文；確定性標記 🔵🟢🟡🟠🔴；來源等級 A/B/C/D。
- **禁圖表 / 製圖 / 看圖**類內容（生不出來就省略，不寫假的）。

### 3. 版權界線
- 不貼受版權原典全文進 repo。
- **可以**讀原典來驗證、可以引用短段落 + 出處、可以列書目。

### 4. 驗證（強制，詳見 `methodology/verification-sop.md`）
- 三角驗證：具體宣稱 ≥2 獨立權威一致才收；分歧兩說並列。
- known-distortions：主動比對教科書扭曲清單（見 SOP 附錄）。
- 缺口顯性：不確定寫「資料待補」，不用「我不確定」當免責符。
- **禁捏造引用 / 假書目**：查不到出處的宣稱一律刪或降級 🔴。

### 5. 派工與配額路由
- 批次校核 / 補寫 → **Sonnet 5 sub-agent**（Agent tool，禁 git 操作寫進 prompt，主 session 驗收後才 commit）。
- Opus 只用於仲裁分歧、用戶觸發的判斷工作。
- m3 已退役（額度被 religions-history 佔用）；m3 產物是草稿，會捏造數字，校核一律查證。
- `claude -p`（無 env 覆蓋）走 Pro 訂閱 OAuth＝無額外金錢消費，只吃 5H 訂閱窗。
- 機械性監控一律零 LLM（純 script），禁任何模型排程輪詢。

### 6. commit + 文件對齊
- 每完成一學派即 commit（引擎自動）。
- 結構性改動後更新 `HANDOFF.md` / `MAP.md` / `00-overview/INDEX.md`。

## 環境
- Windows 11 + Git Bash + Python 3.12
- Encoding：console 是 cp950，Python 一律 `PYTHONIOENCODING=utf-8 python ...`
- EOL：`.gitattributes` 強制 LF
- 遠端：`https://github.com/Hangsau/psychology-schools`（public，gh 已登入），改動做完直接 push 不用問

## Anti-pattern（禁止）
- ❌ 硬塞做不到的內容（圖 / 製圖 / 看圖）
- ❌ 引用拼裝、單一來源當定論
- ❌ 教科書扭曲版當事實
- ❌ 捏造引用 / 假書目
- ❌ 簡繁混用
- ❌ 貼受版權原典全文
