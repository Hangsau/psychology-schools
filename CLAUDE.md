# psychology-schools — AI 工作守則

> 給未來接手的 Claude / m3 / 其他 AI agent。
> 計畫見 [`PLAN.md`](./PLAN.md)，狀態快照見 [`HANDOFF.md`](./HANDOFF.md)，導航見 [`MAP.md`](./MAP.md)。

## 一句話

心理學學派**完整內容**綜述庫。每學派一個 `schools/<slug>/`，內含 `meta.json` + `synthesis.md`。與 `religions-history` 共用 13 領域對接軸。

## 當前階段

**P2 完成（48/48，2026-07-16）。當前＝P3 批次校核。**

- 48 學派清單見 `00-overview/schools-inventory.md`；狀態看 `STATUS.md`
- 引擎（`tools/run-engine.sh` + claude-m3）已退役；M3 額度被 religions-history 佔用，本專案不再用 m3
- P3 執行者＝**Sonnet 5 sub-agent 批次**（規格 `methodology/p3-batch-spec.md`），Opus 只仲裁；每批驗收即 commit+push
- 草稿全標 🟡 draft，校核後升級 🟢；`meta.json` 的 `concept_tags` 須在 P3 補齊（P4 前置）

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
