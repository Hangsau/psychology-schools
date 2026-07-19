#!/usr/bin/env bash
# P5 全庫深化 runner：逐篇隔離 claude -p，驗證後自動 commit+push，勾佇列。
# 零 LLM 監控；撞牆（hit your limit）自動停並寫 HALT 檔。
# 用法：nohup bash tools/p5-deepen-runner.sh >> logs/p5-runner.log 2>&1 &
set -u
cd "$(dirname "$0")/.."

QUEUE="methodology/p5-full-queue.md"
BRIEF="methodology/p5-deepen-brief.md"
HALT="logs/p5-runner.HALT"
FAIL_LOG="logs/p5-runner-failures.log"
LOCK="logs/p5-runner.pid"

# 單例鎖
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then
  echo "[runner] already running (pid $(cat "$LOCK")), exit"; exit 0
fi
echo $$ > "$LOCK"
rm -f "$HALT"

log() { echo "[runner $(date '+%H:%M:%S')] $*"; }

while true; do
  slug=$(sed -n 's/^- \[ \] \([a-z0-9-]*\)（.*/\1/p' "$QUEUE" | head -1)
  [ -z "$slug" ] && { log "queue empty — ALL DONE"; break; }

  target="schools/$slug/synthesis.md"
  pre_size=$(stat -c %s "$target" 2>/dev/null || echo 0)
  log "start $slug (pre=${pre_size}B)"

  runlog="logs/p5-run-$slug.log"
  timeout 2400 claude -p "Read methodology/p5-deepen-brief.md and follow it exactly. Target slug: $slug. First read the current state of the target file and skip any part that is already at standard. Work step by step with small edits as the brief instructs." \
    --model claude-sonnet-4-6 --permission-mode bypassPermissions > "$runlog" 2>&1
  rc=$?

  # 撞牆偵測：停整條管線。重啟由獨立 watchdog（tools/p5-watchdog.sh）在 reset 後自動接手。
  if grep -qi "hit your limit" "$runlog"; then
    reset_info=$(grep -io "resets [^\"]*" "$runlog" | head -1)
    log "QUOTA WALL on $slug ($reset_info) — halting (watchdog 將於 reset 後自動重啟)"
    { echo "halted_at=$(date '+%F %T')"; echo "slug=$slug"; echo "$reset_info"; } > "$HALT"
    break
  fi

  post_size=$(stat -c %s "$target" 2>/dev/null || echo 0)
  verify_ok=false
  if PYTHONIOENCODING=utf-8 python tools/verify.py 2>&1 | grep -q "ALL PASS" \
     && PYTHONIOENCODING=utf-8 python tools/scan-simplified.py 2>&1 | grep -q "CLEAN" \
     && [ "$post_size" -ge 30000 ] \
     && grep -q "P5 補全" "$target"; then
    verify_ok=true
  fi

  if $verify_ok; then
    git add "schools/$slug/"
    # 勾佇列
    sed -i "s|^- \[ \] $slug（\([0-9.]*\)KB|- [x] $slug（\1→$(awk "BEGIN{printf \"%.1f\", $post_size/1000}")KB，$(date '+%F')|" "$QUEUE"
    git add "$QUEUE"
    git commit -m "p5: $slug 深化（管線；$(awk "BEGIN{printf \"%.1f\", $post_size/1000}")KB）" >/dev/null
    git push origin master >/dev/null 2>&1 || log "push failed for $slug (will retry next round)"
    log "done $slug (${pre_size}→${post_size}B, rc=$rc)"
  else
    log "FAILED $slug (rc=$rc, size=${post_size}B) — patch saved, file reverted, continue next"
    echo "$(date '+%F %T') $slug rc=$rc size=${post_size}B" >> "$FAIL_LOG"
    # 半成品存 patch 後還原，避免殘留污染後續篇的 repo 級 verify
    git diff -- "schools/$slug/" > "logs/p5-failed-$slug.patch"
    git checkout -- "schools/$slug/"
    # 防止失敗篇無限循環：標記為 [!]
    sed -i "s|^- \[ \] $slug（|- [!] $slug（|" "$QUEUE"
  fi

  sleep 10
done

rm -f "$LOCK"
log "runner exit"
