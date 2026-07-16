# P3 批次校核規格（Sonnet 5 sub-agent 用）

> 對 48 篇 m3 草稿做事實校核 + meta 補齊，🟡 draft → 🟢 reviewed。
> 執行者：Sonnet 5 sub-agent（Agent tool，`model: "sonnet"`），每批 5–8 篇；第 1 批 = 5 篇 pilot。
> 主 session 負責：派工、逐批驗收（`tools/verify.py` + `tools/scan-simplified.py` + 抽查）、commit、push。
> **sub-agent 絕對禁止任何 git 操作**（add / commit / push / reset / checkout / stash 全禁）。

---

## 每篇校核程序（依序做完才算一篇）

### 1. 全文閱讀
Read `schools/<slug>/synthesis.md` 全文。8 段標題（`## 1.`～`## 8.`）**不可增刪合併**，內文就地修正。

### 2. 事實校核（核心；m3 會捏造數字，所有具體宣稱視為待證）
逐項檢查三類高風險宣稱：
- **年代**：生卒年、出版年、事件年。與你的知識比對；不確定時用 WebSearch 三角驗證（≥2 獨立權威一致才維持 🟢+）。
- **歸屬**：「X 主張 Y」「X 影響了 Z」。查證歸屬是否張冠李戴。
- **數字**：效應量、次數、百分比、「N 週療程」類。m3 已有捏造前科（例：捏造「492 筆」），**查不到出處的數字一律刪或降 🔴**。

處置規則：
- 證實錯誤 → 就地改正，並保留/調整確定性標記。
- 無法證實也無法證偽 → 降級 🟠 或 🔴，或改「資料待補」。
- 兩說分歧 → 兩說並列標 🟡。
- **禁止**為了補洞捏造新引用/新數字。

### 3. known-distortions 比對
對照 `methodology/verification-sop.md` 附錄 A 清單（Maslow 金字塔 / 小 Albert / Pavlov 鈴 / Genovese 38 人 / Milgram / Gage / Piaget 年齡界線 / Freud 冰山）。涉及本學派者：確認正文已避開；若命中扭曲版 → 改校正版並在 §8 註記。

### 4. 書目查核（§4）
逐本檢查：書名 / 作者 / 年代是否為真實存在的文獻。可用 WebSearch。
- 對不上真實文獻 → 刪除或標 🔴 + 「資料待補」。
- 年代錯 → 改正。
- PD / © 標記缺 → 補。

### 5. meta.json 補齊
Read + 更新 `schools/<slug>/meta.json`，填：
- `concept_tags`：讀完全文後，從 `00-overview/concepts.md` 受控詞彙表選 **3–8 個**。**禁止自創標籤**；覺得缺概念 → 寫進回報，不擅自加表。
- `era`：主要活躍年代（如 `"1890s–1920s"`）。
- `region`：起源地區（如 `"德國"`、`"美國"`、`"日本"`）。
- `keywords`：5–10 個中文檢索詞。
- `confidence_overall`：全篇整體信心 `"🟢"` 或 `"🟡"`（多處 🔴 未解 → `"🟡"`）。
- `sources_tier_summary`：一句話，如 `"B 為主，A 書目定錨，D 少量"`。
- `review_state`：校核完成才改 `"reviewed"`（這會讓 STATUS.md 轉 🟢）。
- 其他欄位（slug/name/category/domain_tags/generated_*）**不動**。

### 6. 校核紀錄
在 synthesis.md 文末加一行（§8 之後）：
```
> 🟢 P3 校核：<YYYY-MM-DD> Sonnet 5 批次；修 N 處事實 / 刪 M 條可疑書目 / concept_tags 已填。
```

---

## 邊界與禁令

- ❌ 任何 git 指令。
- ❌ 重寫整段 / 改變 8 段結構 / 大幅刪內容——只做**就地修正**與標記升降。
- ❌ 捏造引用、假書目、湊數字。
- ❌ 自創 concept 標籤。
- ❌ 動 `tools/`、`00-overview/`、`methodology/` 任何檔案。
- ❌ 簡繁混用（改動處全繁體；日文書名/假名行保留原字形）。
- WebSearch 找不到 ≠ 不存在（尤其日文/非英語文獻）；此時降級標記即可，不刪原典級書目。

## 回報格式（每批結束回主 session）

每篇一節：
```
### <slug>
- 事實修正：<條列，含原文→改後；無則「無」>
- 書目處置：<刪 X / 標 🔴 Y / 無問題>
- known-distortions：<涉及哪條、處置；不涉及則「不涉及」>
- concept_tags：<填入的標籤>
- confidence_overall：<🟢/🟡> + 一句理由
- 未決事項：<需 Opus 仲裁或人工查的，無則「無」>
```

## 驗收（主 session，每批）

1. `python tools/verify.py` → ALL PASS
2. `python tools/scan-simplified.py` → CLEAN
3. 抽 1–2 篇 diff 檢查：確認是就地修正非重寫、校核紀錄行存在、meta 欄位合規
4. `python tools/gen-status.py`（🟡→🟢 反映到 STATUS.md）
5. commit + push（訊息格式：`p3: 批次 N 校核 <slugs>`）
6. 「未決事項」彙整，批次全跑完後一次交 Opus 仲裁
