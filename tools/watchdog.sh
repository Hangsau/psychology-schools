#!/usr/bin/env bash
# 看門狗：引擎心跳超過 20 分沒更新且隊列未跑完 → 重啟引擎（detach）。
# 由 schtasks 每 15 分觸發；引擎 skip-if-exists 使重啟安全。
set -uo pipefail
ROOT="C:/claudehome/projects/psychology-schools"
cd "$ROOT" || exit 1
export PYTHONIOENCODING=utf-8

# 隊列是否全部完成？
remaining=$(python -c "
import json,os
q=json.load(open('scripts/schools.json',encoding='utf-8'))
n=0
for e in q:
    p=os.path.join('schools',e['slug'],'synthesis.md')
    if not (os.path.exists(p) and os.path.getsize(p)>=400): n+=1
print(n)
")
if [ "$remaining" = "0" ]; then
  echo "[watchdog] queue complete, nothing to do"; exit 0
fi

# 心跳新鮮度（秒）
now=$(date +%s)
hb=0
[ -f logs/engine.heartbeat ] && hb=$(stat -c %Y logs/engine.heartbeat 2>/dev/null || echo 0)
age=$(( now - hb ))

if [ "$age" -gt 1200 ]; then
  echo "[watchdog] heartbeat stale (${age}s), $remaining left — relaunching engine"
  nohup bash tools/run-engine.sh >> logs/engine.log 2>&1 &
  disown 2>/dev/null || true
else
  echo "[watchdog] engine alive (heartbeat ${age}s ago), $remaining left"
fi
