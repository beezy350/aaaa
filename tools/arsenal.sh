#!/usr/bin/env bash
# Be Bold arsenal: third-party Claude skills cloned on demand (not vendored).
# Usage: bash tools/arsenal.sh [target_dir]   (default: ~/arsenal)
set -e
T="${1:-$HOME/arsenal}"; mkdir -p "$T"; cd "$T"
while read -r repo use; do
  [ -z "$repo" ] && continue; n=$(basename "$repo")
  if [ -d "$n" ]; then git -C "$n" pull -q --ff-only || true; else git clone -q --depth 1 "https://github.com/$repo" "$n"; fi
  echo "ok  $repo  — $use"
done <<'LIST'
mvanhorn/last30days-skill   trend research: what people said in the last 30 days (Reddit, X, YouTube, TikTok)
D4Vinci/Scrapling           web scraping for research
blader/humanizer            remove AI tells from captions/scripts
DietrichGebert/ponytail     simplest-code engineering mode
nutlope/hallmark            website/page design
pbakaus/impeccable          polish/critique frontend UI
senlindesign/taste-skill    design taste rules
nextlevelbuilder/ui-ux-pro-max-skill  UI/UX design systems, banners, slides
cathrynlavery/diagram-design  branded technical diagrams
LIST
