# P5 全庫深化 pass — 佇列與進度

> 品質標準、事實紀律、操作紀律**全同** `p5-batch-spec.md`（§3 逐概念完整段落、30KB+、只要學派內容本身、禁臨床案例/教學延伸、既有 🟢🔵 與 P3/P4/P5 紀錄行禁改禁刪）。
> 執行模式（2026-07-20 改版）：**在 session 內手動逐篇深化**——直寫 `synthesis.md`（品質規格＝`p5-deepen-brief.md`）→ `PYTHONIOENCODING=utf-8 python tools/verify.py <slug>` + `scan-simplified.py` → commit + push → 佇列打勾。同 cbt / health-psychology 已驗證模式。
> **自動接續管線已於 2026-07-20 移除**：`p5-deepen-runner.sh`（`claude -p` 迴圈）＋ `p5-watchdog` / `p5-runner-launch` schtasks ＋ `p5-run-hidden.py` / `p5-register-watchdog.py` 全數刪除。原因：實測未能推進佇列（07-19→07-20 卡在 19/38 沒動），用戶要求拿掉。Agent tool 派發亦不用（AUP 誤判兩度攔截）。

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
- [x] attachment-theory（30.9→37.1KB，2026-07-19）
- [x] act（31.9→39.3KB，2026-07-19）
- [x] sfbt（31.9→40.7KB，2026-07-19）
- [x] neo-freudian（32.4→37.3KB，2026-07-19）
- [x] mbsr（32.9→44.3KB，2026-07-19）
- [x] cross-cultural-psychology（33.3→48.2KB，2026-07-19）
- [x] psychoanalysis（35.6KB；密度標竿篇本身——缺口已補、免深化，2026-07-20 打勾）
- [x] cognitive-psychology（33.6→37.5KB，2026-07-20；補演繹推理/心智模型、基模腳本語意網路、訊號偵測理論）
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

## 撞牆恢復（手動）

深化在 session 內做，撞 5H 牆時當篇已 commit 的不受影響（逐篇 commit push）。恢復＝下個視窗重開 session，從佇列第一個未勾項繼續。無自動重啟機制。

## 手動深化注意

- **簡繁誤判**：「P5 補全」紀錄行若含簡繁「X→Y」字面對照，被更正字元本身會被 `scan-simplified.py` 掃到→誤報。改寫紀錄行去掉該字元即過（brief 已加禁令，2026-07-19 object-relations 事故）。
