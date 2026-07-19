# P5 全庫深化 pass — 佇列與進度

> 品質標準、事實紀律、操作紀律**全同** `p5-batch-spec.md`（§3 逐概念完整段落、30KB+、只要學派內容本身、禁臨床案例/教學延伸、既有 🟢🔵 與 P3/P4/P5 紀錄行禁改禁刪）。
> 執行模式（2026-07-18 改版）：**全篇走 `tools/p5-deepen-runner.sh` 管線**——逐篇隔離 `claude -p`（通用指示檔 `p5-deepen-brief.md`）→ 腳本自動 verify/scan/size 檢查 → commit + push → 勾佇列。Agent tool 派發已兩度被 AUP 誤判攔截（批次 A 派發即死、批次 D 中途死），棄用；`claude -p` 隔離 3/3 成功。
> 撞牆自動停（寫 `logs/p5-runner.HALT`）；失敗篇標 `[!]`、diff 存 patch、不阻塞後續。
> **自動重啟（2026-07-19 新增）**：`p5-watchdog` schtasks 任務每 20 分跑一次 `tools/p5-watchdog.sh`（零 LLM）——偵測到 runner 不在＋HALT 的 reset 時刻已過就自動重啟；runner crash 也重啟；佇列清空自刪排程。**不再需要手動 `繼續`**。手動重啟仍可：`nohup bash tools/p5-deepen-runner.sh >> logs/p5-runner.log 2>&1 &`；重註冊 watchdog：`python tools/p5-register-watchdog.py`；watchdog 日誌 `logs/p5-watchdog.log`。

## 佇列（薄→厚；完成打勾）

- [x] biopsychosocial-model（26.1→33.1KB，2026-07-18）[隔離：`p5-bpsm-brief.md`]
- [x] psychodrama（26.4→42.1KB，2026-07-18）
- [x] behaviorism（27.8→45.1KB，2026-07-18）
- [x] constructivist-psychotherapy（27.8→38.9KB，2026-07-18）
- [x] structuralism（28.5→31.7KB，2026-07-18）
- [x] gestalt-psychology（28.8→42.0KB，2026-07-19）
- [x] dbt（28.8→33.6KB，2026-07-19）
- [x] evolutionary-psychology（28.9→48.9KB，2026-07-19）
- [x] person-centered-therapy（29.0→36.8KB，2026-07-19）
- [x] social-psychology（30.0→49.5KB，2026-07-19）
- [x] reality-therapy（30.1→36.9KB，2026-07-19）
- [x] cbt（30.3→42.3KB，2026-07-19）
- [x] object-relations（30.6→37.2KB，2026-07-19）
- [ ] attachment-theory（30.9KB）
- [ ] act（31.9KB）
- [ ] sfbt（31.9KB）
- [ ] neo-freudian（32.4KB）
- [ ] mbsr（32.9KB）
- [ ] cross-cultural-psychology（33.3KB）
- [ ] psychoanalysis（33.6KB；密度標竿篇——僅補明確缺口，不改風格）
- [ ] cognitive-psychology（33.6KB）
- [ ] mbct（33.7KB）
- [ ] indigenous-psychology（33.9KB）
- [ ] morita-therapy（34.7KB）
- [ ] art-therapy（35.3KB）
- [ ] social-constructionism（35.9KB）
- [ ] social-learning-theory（36.5KB）
- [ ] multicultural-feminist-therapy（36.9KB）
- [ ] positive-psychology（38.5KB）
- [ ] systems-family-therapy（39.1KB）
- [ ] naikan-therapy（39.3KB）
- [ ] existential-psychology（39.7KB）
- [ ] play-therapy（40.5KB）
- [ ] cultural-historical-psychology（40.7KB）
- [ ] narrative-therapy（42.8KB）
- [ ] gestalt-therapy（43.2KB）
- [ ] biological-psychology（48.0KB；已超尺寸標準——對照密度標準查缺，達標即打勾）
- [ ] humanistic-psychology（57.6KB；同上）

## 批次規劃

- 批次 D：psychodrama / behaviorism / constructivist-psychotherapy
- 批次 E：structuralism / gestalt-psychology / dbt / evolutionary-psychology
- 批次 F：person-centered-therapy / social-psychology / reality-therapy / cbt
- 批次 G：object-relations / attachment-theory / act / sfbt
- 批次 H：neo-freudian / mbsr / cross-cultural-psychology / cognitive-psychology
- 批次 I：mbct / indigenous-psychology / morita-therapy / art-therapy
- 批次 J：social-constructionism / social-learning-theory / multicultural-feminist-therapy / psychoanalysis
- 批次 K：positive-psychology / systems-family-therapy / naikan-therapy / existential-psychology
- 批次 L：play-therapy / cultural-historical-psychology / narrative-therapy / gestalt-therapy
- 批次 M（查缺型）：biological-psychology / humanistic-psychology
- biopsychosocial-model 單獨走隔離 `claude -p`

## 撞牆恢復

任一批回報 hit limit：已完成篇均已逐篇 commit；勾選本檔進度、更新 HANDOFF、shotclock 排 reset+10 分單發恢復（prompt＝「讀 methodology/p5-full-queue.md 從第一個未勾項繼續」）。
