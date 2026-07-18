# P5 全庫深化 pass — 佇列與進度

> 品質標準、事實紀律、操作紀律**全同** `p5-batch-spec.md`（§3 逐概念完整段落、30KB+、只要學派內容本身、禁臨床案例/教學延伸、既有 🟢🔵 與 P3/P4/P5 紀錄行禁改禁刪）。
> 執行模式：Sonnet sub-agent 串行批次（3–4 篇/批），主 session 驗收後逐篇 commit + push。
> 標 [隔離] 者＝主題詞密度高、有 AUP 誤判前例風險，走「低密度指示檔 + 全新 `claude -p`」模式（參照 `p5-health-brief.md` 前例）。

## 佇列（薄→厚；完成打勾）

- [ ] biopsychosocial-model（26.1KB）[隔離：`p5-bpsm-brief.md`]
- [ ] psychodrama（26.4KB）
- [ ] behaviorism（27.8KB）
- [ ] constructivist-psychotherapy（27.8KB）
- [ ] structuralism（28.5KB）
- [ ] gestalt-psychology（28.8KB）
- [ ] dbt（28.8KB）
- [ ] evolutionary-psychology（28.9KB）
- [ ] person-centered-therapy（29.0KB）
- [ ] social-psychology（30.0KB）
- [ ] reality-therapy（30.1KB）
- [ ] cbt（30.3KB）
- [ ] object-relations（30.6KB）
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
