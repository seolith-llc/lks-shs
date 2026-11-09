#!/usr/bin/env bash
# LKS-SHS video pipeline smoke test: text -> macOS `say` AIFF -> ffmpeg MP4.
# Usage: ./smoke-test.sh [voice] ["text"]   (defaults: Samantha, standard test line)
# Output: tmp/smoke/smoke.mp4 (tmp/ is gitignored; this script is the durable artifact)
set -euo pipefail

VOICE="${1:-Samantha}"
TEXT="${2:-Self healing software. The healing loop observes, evaluates, acts, and learns. This is the L K S video pipeline smoke test.}"
OUT="tmp/smoke"

mkdir -p "$OUT"
say -v "$VOICE" -o "$OUT/voice.aiff" "$TEXT"
ffmpeg -hide_banner -loglevel error -y \
  -i "$OUT/voice.aiff" \
  -f lavfi -i "color=c=#0B2545:s=1280x720:r=30" \
  -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac \
  "$OUT/smoke.mp4"

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT/smoke.mp4"
echo "OK: $OUT/smoke.mp4"
