#!/usr/bin/env bash
# 持續引擎：逐學派用 claude-m3（MiniMax 月費，零 Claude 配額）產綜述草稿。
# 撞不到 5H 牆；skip-if-exists 可續跑；單篇失敗記 log 續下一篇。
set -uo pipefail

ROOT="C:/claudehome/projects/psychology-schools"
cd "$ROOT" || exit 1
export PYTHONIOENCODING=utf-8
mkdir -p logs
echo $$ > logs/engine.pid
TOKEN="$(cat ~/.minimax-token)"

log(){ echo "[$(date '+%H:%M:%S')] $*" | tee -a logs/engine.log; }
touch logs/engine.heartbeat

gen_one(){
  local slug="$1" prompt="$2"
  printf '%s' "$prompt" | timeout 900 \
    env ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" \
        ANTHROPIC_AUTH_TOKEN="$TOKEN" \
        ANTHROPIC_MODEL="MiniMax-M3" \
        ANTHROPIC_SMALL_FAST_MODEL="MiniMax-M3" \
        claude -p --permission-mode bypassPermissions \
    > "schools/$slug/synthesis.md" 2>> logs/engine.log
}

build_prompt(){
cat <<PROMPT
你是心理學史與臨床心理學的研究者。用**繁體中文**寫一篇關於「$2（$3）」學派的**完整綜述**（非簡介、非概念條列），供一個嚴肅的心理學學派知識庫使用。

所屬大類：$4
代表人物：$5
此學派主要回應的「人的問題」領域（供第 7 段用）：$6

嚴格要求：
- 只輸出 markdown 正文，**不要任何開場白、結尾語、自我說明**。
- 全程繁體中文，禁簡體字。
- **禁**任何圖表、製圖、「見下圖」「如圖」類內容——這是純文字知識庫。
- 具體宣稱（年代 / 「某人主張某事」/ 數字）盡量附來源等級：A原典 / B學術（同儕審查·SEP·學術教科書）/ C百科 / D科普。不確定的標「資料待補」或 🔴，**不要捏造引用或假書目**。
- 確定性標記可用：🔵確定 🟢高 🟡中 🟠低 🔴存疑。
- 避開已知教科書扭曲（例：Maslow 從未畫需求金字塔；Watson 從未去除小 Albert 的制約；Pavlov 多用節拍器而非鈴；Kitty Genovese「38 人旁觀」是失實報導）。若本學派涉及，於第 8 段註明已避開。

嚴格用以下 8 段標題（## 開頭），每段都要有實質內容，空的寫「資料待補」不要留白：

## 1. 定位與歷史脈絡
（何時何地興起、回應什麼問題、承接或反對誰）

## 2. 代表人物
（生卒年 + 各自關鍵貢獻）

## 3. 核心理論主張
（**完整展開**，這是重點；關鍵術語附英文/原文；把這個學派真正在說什麼講清楚，不要只給定義）

## 4. 關鍵著作書目
（書名 / 作者 / 年代；標 PD 公有領域 或 © 有版權）

## 5. 方法與技術
（若為治療取向，寫具體做法；若為理論取向，寫研究方法）

## 6. 批評與後續發展
（學界批評、實證支持程度、後續分支與影響）

## 7. 對接「人從生到死的 13 個問題領域」
（說明此學派主要回應哪些領域、為什麼。領域代號：D1存在與意義 D2自我與認同 D3愛與親密 D4家庭與傳承 D5群體社會公義 D6情緒與內在生活 D7善惡良心品格 D8工作成就召喚 D9苦難疾病身體 D10無常老死失去 D11自由命運改變 D12信仰神聖超越 D13安頓修復平安。先驗建議：$6）

## 8. 已知缺口 / 未驗證 / 爭議
（誠實列出：本篇沒能查證的、學界有爭議的、需後續補的。這段是誠信要求，務必寫實。）
PROMPT
}

log "=== engine start (pid $$) ==="
python -c "import json;[print('\t'.join([e['slug'],e['name_zh'],e['name_en'],e['category'],e['figures'],e['domains']])) for e in json.load(open('scripts/schools.json',encoding='utf-8'))]" \
| while IFS=$'\t' read -r slug name_zh name_en category figures domains; do
    touch logs/engine.heartbeat
    mkdir -p "schools/$slug"
    if [ -f "schools/$slug/synthesis.md" ] && [ "$(wc -c < "schools/$slug/synthesis.md")" -ge 400 ]; then
      log "skip $slug (exists)"; continue
    fi
    log "gen $slug ..."
    prompt="$(build_prompt "$slug" "$name_zh" "$name_en" "$category" "$figures" "$domains")"
    if gen_one "$slug" "$prompt"; then
      sz=$(wc -c < "schools/$slug/synthesis.md" 2>/dev/null || echo 0)
      if [ "$sz" -lt 400 ]; then
        log "WARN $slug output too small ($sz B) — will retry next run"
      else
        log "ok $slug ($sz B)"
      fi
    else
      log "FAIL $slug (m3 call error/timeout)"
    fi
    python tools/write-meta.py "$slug" >> logs/engine.log 2>&1 || true
    python tools/gen-status.py >> logs/engine.log 2>&1 || true
    git add -A >/dev/null 2>&1 || true
    git commit -q -m "draft: $slug 綜述草稿 (claude-m3)" >/dev/null 2>&1 || true
  done

python tools/gen-status.py >> logs/engine.log 2>&1 || true
python tools/build-index.py >> logs/engine.log 2>&1 || true
git add -A >/dev/null 2>&1 || true
git commit -q -m "engine: 全隊列跑完，重生 STATUS + index" >/dev/null 2>&1 || true
log "=== engine done ==="
rm -f logs/engine.pid
