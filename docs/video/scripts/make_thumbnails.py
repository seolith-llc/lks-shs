#!/usr/bin/env python3
"""Render YouTube thumbnails (1280x720 PNG) for the 8 episodes + 4 shorts.

Thumbnail formula: one hook stat or keyword, huge; short title; episode tag.
Uses the same SVG->QuickLook square-canvas rule as the video pipeline
(Decision 007): author 1280x1280 square, band centered, crop at raster time.
Output: publish/youtube/thumbs/NN.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_episode as rv  # reuse defs/backdrop/rasterize helpers

EPISODES = [
    ("01", "SEVENTY YEARS", "of self-healing", None),
    ("02", "88% of kernel CVEs", "patched without reboot", ("88%", "LIVE-PATCHED")),
    ("03", "AI SRE is real", "but gated — what shipped", ("2024–26", "WHAT SHIPPED")),
    ("04", "THE PULSE LOOP", "one framework, every layer", ("P·U·L·S·E", None)),
    ("05", "600 lines of Python", "crash it, watch it heal", ("5/5", "SCENARIOS PASS")),
    ("06", "$0–50/month", "real self-healing, no SRE", ("$0–50", "PER MONTH")),
    ("07", "The enterprise ladder", "L0→L4 autonomy, gated", ("L0→L4", None)),
    ("08", "8 ways healing fails", "and the 8 controls", ("8+8", None)),
]


def thumb_svg(ep: str, title_a: str, title_b: str, stat) -> str:
    big, sub = stat if stat else ("PULSE", None)
    c = "#FFD166" if ep in ("01", "04") else rv.STAGE_COLORS[int(ep) % 5]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="1280" viewBox="0 0 1280 1280">'
        + rv._defs()
        + '<rect width="1280" height="1280" fill="url(#bg)"/>'
          '<rect width="1280" height="1280" fill="url(#grid)"/>'
          '<rect width="1280" height="1280" fill="url(#glowA)"/>'
          '<rect width="1280" height="1280" fill="url(#glowB)"/>'
        + '<g transform="translate(0,280)">'
          f'<rect x="72" y="70" width="150" height="56" rx="14" fill="{c}"/>'
          f'<text x="147" y="110" text-anchor="middle" font-family="{rv.FONT}" font-weight="bold" '
          f'font-size="34" fill="#0B2545">EP {ep}</text>'
          f'<text x="72" y="240" font-family="{rv.FONT}" font-weight="bold" font-size="78" '
          f'fill="{rv.WHITE}">{rv.esc(title_a)}</text>'
          f'<text x="72" y="330" font-family="{rv.FONT}" font-weight="bold" font-size="58" '
          f'fill="{c}">{rv.esc(title_b)}</text>'
          f'<rect x="72" y="418" width="430" height="230" rx="18" fill="{rv.CARD}" '
          f'stroke="{rv.CARD_STROKE}" stroke-width="2"/>'
          f'<rect x="72" y="418" width="12" height="230" rx="6" fill="{c}"/>'
          f'<text x="112" y="565" font-family="{rv.FONT}" font-weight="bold" font-size="108" '
          f'fill="{c}">{rv.esc(big)}</text>'
        + (f'<text x="112" y="612" font-family="{rv.FONT}" font-size="30" fill="{rv.MUTED}">'
           f'{rv.esc(sub)}</text>' if sub else "")
        + f'<text x="72" y="690" font-family="{rv.FONT}" font-size="24" fill="{rv.MUTED}">'
          'github.com/seolith-llc/lks-shs</text>'
          '</g></svg>'
    )


def main() -> None:
    out_dir = os.path.normpath(os.path.join(HERE, "..", "..", "..", "publish", "youtube", "thumbs"))
    os.makedirs(out_dir, exist_ok=True)
    for ep, a, b, stat in EPISODES:
        svg = os.path.join(out_dir, f"{ep}.svg")
        open(svg, "w").write(thumb_svg(ep, a, b, stat))
        rv.rasterize(svg, os.path.join(out_dir, f"{ep}.png"))
        os.remove(svg)
        print(f"  {ep}.png")
    print(f"OK -> {out_dir}")


if __name__ == "__main__":
    main()
