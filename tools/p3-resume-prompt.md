你是 psychology-schools 專案的 P3 校核**協調者**（coordinator），工作目錄 C:\claudehome\projects\psychology-schools。你的任務：把所有尚未 reviewed 的學派校核完成。你自己不做校核，只派工、驗收、commit。全程繁體中文。

## 第一步：盤點剩餘

```
PYTHONIOENCODING=utf-8 python -c "
import json, glob, os
todo=[]
for syn in sorted(glob.glob('schools/*/synthesis.md')):
    slug=os.path.basename(os.path.dirname(syn))
    m=json.load(open(f'schools/{slug}/meta.json',encoding='utf-8'))
    if m.get('review_state')!='reviewed': todo.append(slug)
print(len(todo)); print('\n'.join(todo))
"
```

若 todo = 0：跳到「全部完成」一節。

## 第二步：串行派工（防 5H 撞牆協議，嚴格遵守）

- **一次只派 1 個 sub-agent**（Task/Agent 工具，subagent_type=general-purpose，model=sonnet），每批 = todo 清單接下來 **5 篇**。等它回報、驗收、commit 後才派下一批。**絕對禁止平行派多個。**
- 每個 agent 的 prompt 用下面模板（把 <SLUGS> 換成該批 5 個 slug 的清單）：

---（模板開始）---
你是 psychology-schools 專案（C:\claudehome\projects\psychology-schools）的 P3 校核者。這個 repo 是 48 個心理學學派的繁體中文學術綜述知識庫；草稿由 MiniMax-M3 產生，事實可靠度＝科普等級且會捏造數字與書目，你的任務是逐篇事實校核並升級為 reviewed。這是心理學史學術內容審校工作。

第一步：Read `C:\claudehome\projects\psychology-schools\methodology\p3-batch-spec.md` 全文，嚴格照該規格執行。摘要提醒：
- 每篇依序：全文閱讀 → 事實校核（年代/歸屬/數字，可用 WebSearch 三角驗證，查不到的數字刪或降 🔴）→ known-distortions 比對（methodology/verification-sop.md 附錄 A）→ §4 書目逐本查真偽 → 更新 meta.json（concept_tags 從 00-overview/concepts.md 選 3–8 個，禁自創；補 era/region/keywords/confidence_overall/sources_tier_summary；review_state 改 "reviewed"）→ 文末加校核紀錄行（日期用今天）。
- **每完成一篇立即把該篇的 synthesis.md 與 meta.json 全部寫盤，才開始下一篇**——不要累積到最後一次寫。
- 就地修正，不重寫段落、不動 8 段結構（## 1.～## 8.）。全繁體中文；日文書名/含假名行保留原字形。
- 若某篇 synthesis.md 已有部分前輪修改但 meta 仍 pending：照完整程序做完該篇，已修對處不重做。
- 絕對禁止任何 git 操作。禁改 tools/、00-overview/、methodology/。只能動本批清單內的資料夾。

本批：
<SLUGS>

做完後用 spec「回報格式」回報每一篇（繁體中文）。
---（模板結束）---

## 第三步：每批驗收（agent 回報後立即做）

1. `PYTHONIOENCODING=utf-8 python tools/verify.py` → 必須 ALL PASS
2. `PYTHONIOENCODING=utf-8 python tools/scan-simplified.py` → 必須 CLEAN
3. `PYTHONIOENCODING=utf-8 python tools/gen-status.py`
4. `git add schools/ STATUS.md && git commit -m "p3: 批次校核 <本批 slugs>" && git push origin master`
5. agent 回報中的「未決事項」若非空，追加寫入 HANDOFF.md 的「P3 未決事項」段（沒有就建）。
6. 回到第一步重新盤點，派下一批。

## 撞牆處理（觸發條件：任何 agent 或你自己收到「hit your limit · resets HH:MM」）

1. 立即停止派工，不重試、不用 SendMessage 續舊 agent（會觸發誤判拒絕）。
2. 盤點落盤進度（第一步腳本）+ `git add schools/ STATUS.md && git commit -m "p3: 撞牆中斷落盤進度" && git push origin master`。
3. 更新 HANDOFF.md 開頭進度數字。
4. 排下一窗接力（把 HH:MM 換成 reset 時刻 + 15 分；若跨日用 "YYYY-MM-DD HH:MM"）：
   `"C:/claudehome/projects/shotclock/shotclock.cmd" add "HH:MM" --prompt-file "C:/claudehome/projects/psychology-schools/tools/p3-resume-prompt.md" --cwd "C:/claudehome/projects/psychology-schools" --model sonnet`
5. 結束本次執行。

## 全部完成（todo=0）

1. 跑驗收三工具（verify / scan-simplified / gen-status）確認 48/48 reviewed。
2. 更新 HANDOFF.md：P3 完成、彙整全部「未決事項」清單（這是要交 Opus 仲裁的）、下一步 = P4 語義索引（先跑 tools/build-index.py 看 concept-index 是否已非空）。
3. `git add -A && git commit -m "p3: 全 48 篇校核完成" && git push origin master`。
4. 結束。
