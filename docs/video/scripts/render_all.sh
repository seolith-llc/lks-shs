#!/usr/bin/env bash
# Render every episode script in docs/video/ to its MP4 (Phase 5 pipeline).
# Usage: ./render_all.sh [voice]
set -euo pipefail
cd "$(dirname "$0")/.."
VOICE="${1:-Samantha}"
mkdir -p tmp
for script in [0-9][0-9]-*.md; do
  slug="${script%.md}"
  echo "== $slug"
  scripts/render_episode.py "$script" "$slug.mp4" --voice "$VOICE"
done
echo "All episodes rendered."
