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
BG, ACCENT, WHITE, MUTED = "#0B2545", "#FFD166", "#E0FBFC", "#8DA9C4"
HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(HERE, ".venv", "bin", "python")

STAGE_COLORS = ["#2EC4B6", "#FF9F1C", "#E71D36", "#4CC9F0", "#9EF01A"]
CARD, CARD_STROKE = "#0A1F3D", "#3D5A80"
GLYPHS = ["&#9656;", "&#9679;", "&#9670;", "&#10003;", "&#9733;"]  # ▸ ● ◆ ✓ ★
FONT = "Arial, Helvetica, sans-serif"


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


def _frame(inner: str, index: int, total: int) -> str:
    """Square canvas + backdrop + the 16:9 content band, vertically centered."""
    seg_w, gap = 26, 8
    x0 = W - 72 - total * (seg_w + gap) + gap
    segs = "".join(
        f'<rect x="{x0 + i * (seg_w + gap):.0f}" y="{H - 46}" width="{seg_w}" height="8" rx="4" '
        f'fill="{"#FFD166" if i < index else "#22406B"}"/>'
        for i in range(total))
    footer = (
        f'<text x="72" y="{H - 38}" font-family="{FONT}" font-size="17" fill="{MUTED}">'
        f'LKS-SHS · the PULSE loop — self-healing software, engineered with AI</text>'
        f'<text x="{x0 - 14:.0f}" y="{H - 38}" text-anchor="end" font-family="{FONT}" '
        f'font-size="17" fill="{MUTED}">{index:02d}/{total:02d}</text>{segs}'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SQ}" height="{SQ}" '
        f'viewBox="0 0 {SQ} {SQ}">' + _defs()
        + f'<rect width="{SQ}" height="{SQ}" fill="url(#bg)"/>'
          f'<rect width="{SQ}" height="{SQ}" fill="url(#grid)"/>'
          f'<rect width="{SQ}" height="{SQ}" fill="url(#glowA)"/>'
          f'<rect width="{SQ}" height="{SQ}" fill="url(#glowB)"/>'
        + f'<g transform="translate(0,{DY})">' + inner + footer + "</g></svg>"
    )


def _chip(x: float, y: float, text: str, color: str, size: float = 18) -> str:
    w = 14 + len(text) * size * 0.58
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 18}" rx="12" '
        f'fill="{CARD}" stroke="{CARD_STROKE}"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + size + 5}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{size}" fill="{color}" font-weight="bold">{esc(text)}</text>'
    )


def _title_inner(title: str, episode: str) -> str:
    dots = "".join(
        f'<circle cx="{640 - 2 * 44 + i * 44}" cy="352" r="8" fill="{c}"/>'
        for i, c in enumerate(STAGE_COLORS))
    return (
        _chip(72, 56, "LKS-SHS", MUTED)
        + _chip(W - 72 - (14 + len(episode) * 10.4), 56, episode, "#FFD166")
        + f'<text x="640" y="308" text-anchor="middle" font-family="{FONT}" font-weight="bold" '
          f'font-size="104" letter-spacing="26" fill="{WHITE}">PULSE</text>'
        + dots
        + f'<text x="640" y="428" text-anchor="middle" font-family="{FONT}" font-weight="bold" '
          f'font-size="38" fill="#FFD166">{esc(title)}</text>'
        + f'<text x="640" y="472" text-anchor="middle" font-family="{FONT}" font-size="24" '
          f'fill="{MUTED}">Self-healing software, engineered with AI</text>'
    )


def _content_inner(title: str, bullets: list[str], stats: list[tuple]) -> str:
    p = [_chip(72, 56, "LKS-SHS", MUTED)]

    title_lines = wrap(title, 46)
    y = 148
    for ln in title_lines[:2]:
        p.append(f'<text x="72" y="{y}" font-family="{FONT}" font-weight="bold" font-size="44" '
                 f'fill="{WHITE}">{esc(ln)}</text>')
        y += 52
    p.append(f'<rect x="72" y="{y - 18}" width="88" height="7" rx="3.5" fill="#FFD166"/>')
    body_top, body_bottom = y + 28, H - 62

    shown_bullets = bullets[:4 if stats else 6]
    bullet_h = sum(len(wrap(b, 60)) * 37 + 22 for b in shown_bullets)
    stat_rows = (min(len(stats), 4) + 1) // 2
    stat_h = 0 if not stats else stat_rows * 166 + 14
    block_h = bullet_h + stat_h
    y = body_top + max(0, (body_bottom - body_top - block_h) // 2)

    for i, b in enumerate(shown_bullets):
        color = STAGE_COLORS[i % len(STAGE_COLORS)]
        p.append(f'<rect x="72" y="{y - 25}" width="38" height="38" rx="10" fill="{color}" '
                 f'fill-opacity="0.16" stroke="{color}" stroke-opacity="0.55"/>')
        p.append(f'<text x="91" y="{y + 2}" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="19" fill="{color}">{GLYPHS[i % len(GLYPHS)]}</text>')
        for ln in wrap(b, 60):
            p.append(f'<text x="132" y="{y}" font-family="{FONT}" font-size="27" '
                     f'fill="{WHITE}">{esc(ln)}</text>')
            y += 37
        y += 22

    if stats:
        y = max(y + 6, body_top + bullet_h)
        for i, (big, label) in enumerate(stats[:4]):
            color = STAGE_COLORS[i % len(STAGE_COLORS)]
            col, row = i % 2, i // 2
            cx, cy = 72 + col * 556, y + row * 166
            p.append(f'<rect x="{cx}" y="{cy}" width="532" height="148" rx="14" fill="{CARD}" '
                     f'stroke="{CARD_STROKE}" stroke-width="1.5"/>')
            p.append(f'<rect x="{cx}" y="{cy}" width="7" height="148" rx="3.5" fill="{color}"/>')
            p.append(f'<text x="{cx + 34}" y="{cy + 74}" font-family="{FONT}" font-weight="bold" '
                     f'font-size="50" fill="{color}">{esc(big)}</text>')
            for j, ln in enumerate(wrap(label, 40)[:2]):
                p.append(f'<text x="{cx + 34}" y="{cy + 110 + j * 26}" font-family="{FONT}" '
                         f'font-size="20" fill="{MUTED}">{esc(ln)}</text>')

    return "".join(p)


def slide_svg(title: str, bullets: list[str], stats: list[tuple],
              index: int, total: int, episode: str = "") -> str:
    if index == 1:
        return _frame(_title_inner(title, episode), index, total)
    return _frame(_content_inner(title, bullets, stats), index, total)


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
    args = ap.parse_args()

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
                                       i + 1, total, episode))
        png = os.path.join(work, f"s{i:02d}.png")
        rasterize(svg, png)

        part = os.path.join(work, f"p{i:02d}.ts")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-loop", "1", "-framerate", str(FPS), "-i", png, "-i", audio,
             "-af", "apad=pad_dur=0.8",
             # square 2560x2560 -> center 16:9 band -> supersampled downscale
             "-vf", "crop=2560:1440,scale=1280:720",
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
