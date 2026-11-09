#!/usr/bin/env bash
# Render every episode script in docs/video/ to its MP4 (Phase 5 pipeline).
# Usage: ./render_all.sh   (engine auto-detected; pass flags through by editing)
set -uo pipefail   # no -e: one failed episode shouldn't kill the batch
cd "$(dirname "$0")/.."
mkdir -p tmp
FAILED=0
for script in [0-9][0-9]-*.md; do
  slug="${script%.md}"
  echo "== $slug"
  if ! scripts/render_episode.py "$script" "$slug.mp4"; then
    echo "FAILED: $slug" >&2
    FAILED=1
  fi
done
[ "$FAILED" -eq 0 ] && echo "All episodes rendered." || exit 1
