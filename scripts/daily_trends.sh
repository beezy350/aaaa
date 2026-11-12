#!/usr/bin/env bash
# Daily trend research for Be Bold using last30days (no paid keys needed).
set -u
D=$(date -u +%F); OUT="bebold/trends/$D"; mkdir -p "$OUT"
bash tools/arsenal.sh "$HOME/arsenal" >/dev/null
pip install -q yt-dlp >/dev/null 2>&1 || true
L="$HOME/arsenal/last30days-skill/skills/last30days/scripts/last30days.py"
run () { # slug, subreddits, topic
  timeout 600 python3 "$L" --research-only --no-browser-cookies --days 30 \
    --web-backend keyless --subreddits "$2" --emit md --save-dir "" "$3" \
    > "$OUT/$1.md" 2> "$OUT/$1.log" || echo "(failed — see $1.log)" >> "$OUT/$1.md"
}
run stoicism        "Stoicism,philosophy,selfimprovement,getdisciplined" "stoicism"
run kalila_dimna    "mythology,folklore,history,books"                  "ancient fables wisdom stories"
run dark_psychology "psychology,socialskills,DecidingToBeBetter"       "dark psychology"
run money_mindset   "financialindependence,personalfinance,Entrepreneur" "money mindset"
ls -la "$OUT"
