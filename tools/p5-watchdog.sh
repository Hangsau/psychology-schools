#!/usr/bin/env bash
# P5 深化管線 watchdog：零 LLM，由 schtasks 每 20 分觸發一次。
# 職責：撞牆後 reset 一過就自動重啟 runner；runner crash 也重啟；佇列清空自刪排程。
# 不做任何 LLM 呼叫、不 poll 模型。
set -u
cd "$(dirname "$0")/.."

QUEUE="methodology/p5-full-queue.md"
HALT="logs/p5-runner.HALT"
LOCK="logs/p5-runner.pid"
WLOG="logs/p5-watchdog.log"
TASK="p5-watchdog"

log() { echo "[wd $(date '+%F %T')] $*" >> "$WLOG"; }

relaunch() {
  log "RELAUNCH: $*"
  rm -f "$HALT" "$LOCK"
  # 用 schtasks //Run 觸發獨立的 on-demand runner 任務，讓 runner 跑在自己的 job object，
  # 不會隨本 watchdog 任務結束被 Task Scheduler 連同 process tree 回收。
  schtasks //Run //TN "p5-runner-launch" >/dev/null 2>&1 \
    && log "  → schtasks Run p5-runner-launch OK" \
    || log "  → schtasks Run FAILED"
}

# 1) 佇列清空 → 收工，移除 watchdog 排程
remaining=$(grep -c '^- \[ \]' "$QUEUE")
if [ "$remaining" -eq 0 ]; then
  log "queue empty — ALL DONE, removing watchdog task"
  schtasks //Delete //TN "$TASK" //F >/dev/null 2>&1
  exit 0
fi

# 2) runner 還活著 → 什麼都不做
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then
  log "runner alive (pid $(cat "$LOCK")), $remaining left — ok"
  exit 0
fi

# 3) runner 不在。有 HALT（撞牆）→ 看 reset 是否已過
if [ -f "$HALT" ]; then
  clock=$(grep -io 'resets[^0-9]*[0-9]\{1,2\}:[0-9]\{2\}[[:space:]]*[ap]m' "$HALT" \
          | grep -io '[0-9]\{1,2\}:[0-9]\{2\}[[:space:]]*[ap]m' | head -1)
  halted=$(grep '^halted_at=' "$HALT" | cut -d= -f2-)
  if [ -z "$clock" ] || [ -z "$halted" ]; then
    log "HALT present but cannot parse (clock='$clock' halted='$halted') — waiting"
    exit 0
  fi
  halted_epoch=$(date -d "$halted" +%s 2>/dev/null)
  hday=$(date -d "$halted" +%Y-%m-%d 2>/dev/null)
  reset_epoch=$(date -d "$hday $clock" +%s 2>/dev/null)
  # reset 是 halted 之後的「下一個」該時刻；若算出來 <= halted 就 +1 天
  if [ -n "$reset_epoch" ] && [ "$reset_epoch" -le "$halted_epoch" ]; then
    reset_epoch=$((reset_epoch + 86400))
  fi
  now=$(date +%s)
  if [ -n "$reset_epoch" ] && [ "$now" -ge "$reset_epoch" ]; then
    relaunch "reset passed (resets $clock)"
  else
    log "waiting for reset ($clock); now=$(date '+%H:%M') target=$(date -d "@$reset_epoch" '+%F %H:%M' 2>/dev/null)"
  fi
  exit 0
fi

# 4) 無 HALT、runner 不在、佇列還有 → 視為 crash，直接重啟
relaunch "no HALT + runner dead + $remaining left (crash recovery)"
exit 0
