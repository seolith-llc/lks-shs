#!/usr/bin/env python3
"""Render a PULSE episode: markdown script -> neural TTS narration -> SVG slides
-> QuickLook rasterization -> ffmpeg -> MP4.

Script format (see docs/video/[0-9][0-9]-*.md episodes):
    ## Slide title
    - on-screen bullet (display only, never spoken)
    -! <BIG> | <label>          <- stat callout card (display only)
    Narration paragraph — spoken, never shown.

Narration engines (Decision 006):
  --engine edge  (default when available): Microsoft neural voices via edge-tts
                 running in scripts/.venv — studio-grade naturalness, zero cost,
                 no API key; narration text is processed by Microsoft's endpoint.
  --engine say   (offline fallback): macOS `say` voices — fully local, robotic.

Slide rasterization gotcha (hard-won, see Decision 006 addendum / prompt history
turn 9): qlmanage renders NON-square SVGs at a broken ~1.66x scale, top-left
anchored (content clipped). Square SVGs map 1:1 per `-s` unit. Therefore slides
are authored on a 1280x1280 canvas with the 16:9 band vertically centered
(DY=280), rasterized at `-s 2560`, then center-cropped 2560x1440 and scaled to
1280x720 in ffmpeg (2x supersampling = crisper text).

Usage: render_episode.py <script.md> [<out.mp4>] [--engine edge] [--voice en-US-JennyNeural]
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile

W, H, FPS = 1280, 720, 30          # logical slide size (16:9 band)
SQ = 1280                           # SVG canvas (square — see header note)
DY = (SQ - H) // 2                  # vertical offset of the band in the square
VW, VH = 1080, 1920                 # vertical (9:16) short logical size
BG, ACCENT, WHITE, MUTED = "#0B2545", "#FFD166", "#E0FBFC", "#8DA9C4"
HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(HERE, ".venv", "bin", "python")

STAGE_COLORS = ["#2EC4B6", "#FF9F1C", "#E71D36", "#4CC9F0", "#9EF01A"]
CARD, CARD_STROKE = "#0A1F3D", "#3D5A80"
GLYPHS = ["&#9656;", "&#9679;", "&#9670;", "&#10003;", "&#9733;"]  # ▸ ● ◆ ✓ ★
FONT = "Arial, Helvetica, sans-serif"


class Layout:
    """Geometry + type scale for one output format (landscape 16:9 or vertical 9:16)."""

    def __init__(self, vertical: bool):
        self.vertical = vertical
        if vertical:
            self.w, self.h = VW, VH
            self.dx, self.dy = (max(VW, VH) - VW) // 2, 0      # band centered in 1920-square
            self.canvas = max(VW, VH)
            self.title_size, self.body_size = 64, 40
            self.chip, self.stat_big, self.stat_label = 56, 96, 30
            self.margin = 72
        else:
            self.w, self.h = W, H
            self.dx, self.dy = 0, DY
            self.canvas = SQ
            self.title_size, self.body_size = 44, 27
            self.chip, self.stat_big, self.stat_label = 38, 50, 20
            self.margin = 72


def parse_script(path: str) -> list[dict]:
    sections, title, bullets, stats, narration = [], None, [], [], []

    def flush():
        nonlocal title, bullets, stats, narration
        if title is not None:
            sections.append({"title": title, "bullets": bullets, "stats": stats,
                             "narration": re.sub(r"\s+", " ", " ".join(narration)).strip()})
        title, bullets, stats, narration = None, [], [], []

    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("## "):
            flush()
            title = re.sub(r"\*\*(.+?)\*\*", r"\1", line[3:].strip())
        elif line.startswith("-! ") and title is not None:
            big, _, label = line[3:].partition("|")
            stats.append((re.sub(r"`(.+?)`", r"\1", big.strip()),
                          re.sub(r"`(.+?)`", r"\1", label.strip())))
        elif line.startswith("- ") and title is not None:
            b = re.sub(r"\*\*(.+?)\*\*", r"\1", line[2:].strip())
            bullets.append(re.sub(r"`(.+?)`", r"\1", b))
        elif line.strip() and title is not None:
            t = re.sub(r"\*\*(.+?)\*\*", r"\1", line.strip())
            t = re.sub(r"`(.+?)`", r"\1", t)
            t = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", t)
            t = t.replace("→", " to ").replace("—", ", ").replace("·", ", ")
            narration.append(t)
    flush()
    return sections


def wrap(text: str, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def _defs() -> str:
    return (
        "<defs>"
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#16396A"/><stop offset="0.55" stop-color="#0B2545"/>'
        '<stop offset="1" stop-color="#071A31"/></linearGradient>'
        '<radialGradient id="glowA" cx="0.86" cy="0.10" r="0.55">'
        '<stop offset="0" stop-color="#FFD166" stop-opacity="0.12"/>'
        '<stop offset="1" stop-color="#FFD166" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="glowB" cx="0.06" cy="0.96" r="0.55">'
        '<stop offset="0" stop-color="#4CC9F0" stop-opacity="0.10"/>'
        '<stop offset="1" stop-color="#4CC9F0" stop-opacity="0"/></radialGradient>'
        '<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">'
        '<path d="M 44 0 L 0 0 0 44" fill="none" stroke="#FFFFFF" stroke-opacity="0.035"/>'
        "</pattern>"
        "</defs>"
    )


def _frame(inner: str, index: int, total: int, lay: Layout) -> str:
    """Square canvas + backdrop + the content band (16:9 centered vertically,
    9:16 centered horizontally), per the qlmanage square-canvas rule."""
    m = lay.margin
    seg_w, gap = (18, 6) if lay.vertical else (26, 8)
    x0 = lay.w - m - total * (seg_w + gap) + gap
    segs = "".join(
        f'<rect x="{x0 + i * (seg_w + gap):.0f}" y="{lay.h - 46}" width="{seg_w}" height="8" rx="4" '
        f'fill="{"#FFD166" if i < index else "#22406B"}"/>'
        for i in range(total))
    fs = 22 if lay.vertical else 17
    footer = (
        f'<text x="{m}" y="{lay.h - 38}" font-family="{FONT}" font-size="{fs}" fill="{MUTED}">'
        f'github.com/seolith-llc/lks-shs</text>'
        f'<text x="{x0 - 14:.0f}" y="{lay.h - 38}" text-anchor="end" font-family="{FONT}" '
        f'font-size="{fs}" fill="{MUTED}">{index:02d}/{total:02d}</text>{segs}'
    )
    c = lay.canvas
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{c}" height="{c}" '
        f'viewBox="0 0 {c} {c}">' + _defs()
        + f'<rect width="{c}" height="{c}" fill="url(#bg)"/>'
          f'<rect width="{c}" height="{c}" fill="url(#grid)"/>'
          f'<rect width="{c}" height="{c}" fill="url(#glowA)"/>'
          f'<rect width="{c}" height="{c}" fill="url(#glowB)"/>'
        + f'<g transform="translate({lay.dx},{lay.dy})">' + inner + footer + "</g></svg>"
    )


def _chip(x: float, y: float, text: str, color: str, size: float = 18) -> str:
    w = 14 + len(text) * size * 0.58
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 18}" rx="12" '
        f'fill="{CARD}" stroke="{CARD_STROKE}"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + size + 5}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{size}" fill="{color}" font-weight="bold">{esc(text)}</text>'
    )


def _title_inner(title: str, episode: str, lay: Layout) -> str:
    m = lay.margin
    cx = lay.w // 2
    if lay.vertical:
        word_y, dots_y, t_y, s_y = 760, 820, 960, 1030
        word_size, dot_r, dot_gap = 150, 12, 56
    else:
        word_y, dots_y, t_y, s_y = 308, 352, 428, 472
        word_size, dot_r, dot_gap = 104, 8, 44
    dots = "".join(
        f'<circle cx="{cx - 2 * dot_gap + i * dot_gap}" cy="{dots_y}" r="{dot_r}" fill="{c}"/>'
        for i, c in enumerate(STAGE_COLORS))
    ep_w = 14 + len(episode) * 10.4 if not lay.vertical else 20 + len(episode) * 13
    return (
        _chip(m, 56, "LKS-SHS", MUTED, 22 if lay.vertical else 18)
        + _chip(lay.w - m - ep_w, 56, episode, "#FFD166", 22 if lay.vertical else 18)
        + f'<text x="{cx}" y="{word_y}" text-anchor="middle" font-family="{FONT}" font-weight="bold" '
          f'font-size="{word_size}" letter-spacing="{26 if not lay.vertical else 34}" '
          f'fill="{WHITE}">PULSE</text>'
        + dots
        + f'<text x="{cx}" y="{t_y}" text-anchor="middle" font-family="{FONT}" font-weight="bold" '
          f'font-size="{54 if lay.vertical else 38}" fill="#FFD166">{esc(title)}</text>'
        + f'<text x="{cx}" y="{s_y}" text-anchor="middle" font-family="{FONT}" '
          f'font-size="{30 if lay.vertical else 24}" fill="{MUTED}">'
          f'Self-healing software, engineered with AI</text>'
    )


def _content_inner(title: str, bullets: list[str], stats: list[tuple], lay: Layout) -> str:
    m, vertical = lay.margin, lay.vertical
    t_size, b_size = lay.title_size, lay.body_size
    t_lead, b_lead = int(t_size * 1.18), int(b_size * 1.37)
    p = [_chip(m, 56, "LKS-SHS", MUTED, 22 if vertical else 18)]

    title_lines = wrap(title, 44 if not vertical else 30)
    y = 148 if not vertical else 200
    for ln in title_lines[:3 if vertical else 2]:
        p.append(f'<text x="{m}" y="{y}" font-family="{FONT}" font-weight="bold" '
                 f'font-size="{t_size}" fill="{WHITE}">{esc(ln)}</text>')
        y += t_lead
    p.append(f'<rect x="{m}" y="{y - int(t_size * 0.41)}" width="{110 if vertical else 88}" '
             f'height="8" rx="4" fill="#FFD166"/>')
    body_top, body_bottom = y + 34, lay.h - 80

    wrap_w = 60 if not vertical else 36
    shown_bullets = bullets[:(2 if vertical else (4 if stats else 6))]
    bullet_h = sum(len(wrap(b, wrap_w)) * b_lead + (30 if vertical else 22)
                   for b in shown_bullets)
    if vertical:
        stat_h = 0 if not stats else min(len(stats), 3) * 250 + 20
    else:
        stat_rows = (min(len(stats), 4) + 1) // 2
        stat_h = 0 if not stats else stat_rows * 166 + 14
    block_h = bullet_h + stat_h
    y = body_top + max(0, (body_bottom - body_top - block_h) // 2)

    chip = lay.chip
    for i, b in enumerate(shown_bullets):
        color = STAGE_COLORS[i % len(STAGE_COLORS)]
        p.append(f'<rect x="{m}" y="{y - int(chip * 0.66)}" width="{chip}" height="{chip}" '
                 f'rx="{int(chip * 0.26)}" fill="{color}" fill-opacity="0.16" '
                 f'stroke="{color}" stroke-opacity="0.55"/>')
        p.append(f'<text x="{m + chip / 2:.0f}" y="{y + chip * 0.06:.0f}" text-anchor="middle" '
                 f'font-family="{FONT}" font-size="{int(chip * 0.5)}" '
                 f'fill="{color}">{GLYPHS[i % len(GLYPHS)]}</text>')
        for ln in wrap(b, wrap_w):
            p.append(f'<text x="{m + chip + 22}" y="{y}" font-family="{FONT}" '
                     f'font-size="{b_size}" fill="{WHITE}">{esc(ln)}</text>')
            y += b_lead
        y += 30 if vertical else 22

    if stats:
        y = max(y + (10 if vertical else 6), body_top + bullet_h)
        if vertical:
            for i, (big, label) in enumerate(stats[:3]):
                color = STAGE_COLORS[i % len(STAGE_COLORS)]
                cy = y + i * 250
                p.append(f'<rect x="{m}" y="{cy}" width="{lay.w - 2 * m}" height="226" rx="18" '
                         f'fill="{CARD}" stroke="{CARD_STROKE}" stroke-width="2"/>')
                p.append(f'<rect x="{m}" y="{cy}" width="10" height="226" rx="5" fill="{color}"/>')
                p.append(f'<text x="{m + 40}" y="{cy + 118}" font-family="{FONT}" '
                         f'font-weight="bold" font-size="{lay.stat_big}" '
                         f'fill="{color}">{esc(big)}</text>')
                for j, ln in enumerate(wrap(label, 44)[:2]):
                    p.append(f'<text x="{m + 40}" y="{cy + 168 + j * 34}" '
                             f'font-family="{FONT}" font-size="{lay.stat_label}" '
                             f'fill="{MUTED}">{esc(ln)}</text>')
        else:
            for i, (big, label) in enumerate(stats[:4]):
                color = STAGE_COLORS[i % len(STAGE_COLORS)]
                col, row = i % 2, i // 2
                cx, cy = m + col * 556, y + row * 166
                p.append(f'<rect x="{cx}" y="{cy}" width="532" height="148" rx="14" '
                         f'fill="{CARD}" stroke="{CARD_STROKE}" stroke-width="1.5"/>')
                p.append(f'<rect x="{cx}" y="{cy}" width="7" height="148" rx="3.5" '
                         f'fill="{color}"/>')
                p.append(f'<text x="{cx + 34}" y="{cy + 74}" font-family="{FONT}" '
                         f'font-weight="bold" font-size="{lay.stat_big}" '
                         f'fill="{color}">{esc(big)}</text>')
                for j, ln in enumerate(wrap(label, 40)[:2]):
                    p.append(f'<text x="{cx + 34}" y="{cy + 110 + j * 26}" '
                             f'font-family="{FONT}" font-size="{lay.stat_label}" '
                             f'fill="{MUTED}">{esc(ln)}</text>')

    return "".join(p)


def slide_svg(title: str, bullets: list[str], stats: list[tuple],
              index: int, total: int, episode: str = "", vertical: bool = False) -> str:
    lay = Layout(vertical)
    if index == 1:
        return _frame(_title_inner(title, episode, lay), index, total, lay)
    return _frame(_content_inner(title, bullets, stats, lay), index, total, lay)


def sh(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{proc.stderr[-2000:]}")
    return proc.stdout.strip()


def rasterize(svg_path: str, png_path: str) -> None:
    subprocess.run(["qlmanage", "-t", "-s", "2560", "-o",
                    os.path.dirname(png_path) or ".", svg_path],
                   check=True, capture_output=True)
    thumb = svg_path + ".png"
    if not os.path.exists(thumb):
        sys.exit(f"qlmanage produced no thumbnail for {svg_path}")
    os.replace(thumb, png_path)


def synth(text: str, out_audio: str, engine: str, voice: str) -> None:
    if engine == "edge":
        if not os.path.exists(VENV_PY):
            sys.exit("edge-tts venv missing — create it: python3 -m venv scripts/.venv && "
                     "scripts/.venv/bin/pip install edge-tts (or use --engine say)")
        subprocess.run([VENV_PY, "-m", "edge_tts", "--voice", voice,
                        "--text", text, "--write-media", out_audio], check=True)
    else:
        subprocess.run(["say", "-v", voice, "-o", out_audio, text], check=True)


def main() -> None:
    default_engine = "edge" if os.path.exists(VENV_PY) else "say"
    default_voice = "en-US-JennyNeural" if default_engine == "edge" else "Samantha"
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--engine", choices=("edge", "say"), default=default_engine)
    ap.add_argument("--voice", default=default_voice)
    ap.add_argument("--format", dest="fmt", choices=("landscape", "vertical"),
                    default="landscape")
    args = ap.parse_args()
    vertical = args.fmt == "vertical"

    sections = parse_script(args.script)
    if not sections:
        sys.exit("no slides parsed")
    out = args.out or os.path.splitext(args.script)[0] + ".mp4"
    work = tempfile.mkdtemp(prefix="pulse-vid-")
    parts = []
    total = len(sections)
    ext = "mp3" if args.engine == "edge" else "aiff"
    episode = "EP " + os.path.basename(args.script)[:2]

    for i, sec in enumerate(sections):
        audio = os.path.join(work, f"s{i:02d}.{ext}")
        synth(sec["narration"], audio, args.engine, args.voice)
        dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", audio]))

        svg = os.path.join(work, f"s{i:02d}.svg")
        open(svg, "w").write(slide_svg(sec["title"], sec["bullets"], sec["stats"],
                                       i + 1, total, episode, vertical))
        png = os.path.join(work, f"s{i:02d}.png")
        rasterize(svg, png)

        lay = Layout(vertical)
        f = 2560 / lay.canvas                      # rasterization scale factor
        cw, ch = int(lay.w * f) // 2 * 2, int(lay.h * f) // 2 * 2   # even dims for h264
        vf = f"crop={cw}:{ch},scale={lay.w if not vertical else VW}:{lay.h if not vertical else VH}"
        part = os.path.join(work, f"p{i:02d}.ts")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-loop", "1", "-framerate", str(FPS), "-i", png, "-i", audio,
             "-af", "apad=pad_dur=0.8",
             "-vf", vf,
             "-map", "0:v", "-map", "1:a", "-t", f"{dur + 0.8:.2f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "25", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "96k", "-ar", "44100", part],
            check=True)
        parts.append(part)
        print(f"  slide {i + 1}/{total}: {sec['title'][:50]} ({dur:.1f}s)", flush=True)

    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", "-movflags", "+faststart", out], check=True)
    meta = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
               "-of", "default=nw=1", out]).replace("\n", " ")
    print(f"OK {out} [{meta}]")


if __name__ == "__main__":
    main()
