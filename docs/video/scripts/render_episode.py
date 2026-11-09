#!/usr/bin/env python3
"""Render a PULSE episode: markdown script -> macOS `say` narration -> SVG slides
-> QuickLook rasterization -> ffmpeg -> MP4.

Script format (see docs/video/[0-9][0-9]-*.md episodes):
    ## Slide title
    - on-screen bullet (display only, never spoken)
    Narration paragraph — spoken, never shown.

Why SVG+qlmanage instead of ffmpeg drawtext: this machine's ffmpeg build has
no text filters (no libfreetype/libass), and the SVG route is fully portable
anyway — the slide generator below shares its palette and typography with the
series' animated SVGs (docs/posts/animations/).

Usage: render_episode.py <script.md> [<out.mp4>] [--voice Samantha]
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile

W, H, FPS = 1280, 720, 30
BG, ACCENT, WHITE, MUTED = "#0B2545", "#FFD166", "#E0FBFC", "#8DA9C4"


def parse_script(path: str) -> list[dict]:
    sections, title, bullets, narration = [], None, [], []

    def flush():
        nonlocal title, bullets, narration
        if title is not None:
            sections.append({"title": title, "bullets": bullets,
                             "narration": re.sub(r"\s+", " ", " ".join(narration)).strip()})
        title, bullets, narration = None, [], []

    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("## "):
            flush()
            title = re.sub(r"\*\*(.+?)\*\*", r"\1", line[3:].strip())
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


def slide_svg(title: str, bullets: list[str], index: int, total: int) -> str:
    y = 132
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<rect x="72" y="66" width="72" height="8" rx="4" fill="{ACCENT}"/>',
        f'<text x="72" y="{y}" font-family="Arial, Helvetica, sans-serif" font-weight="bold" '
        f'font-size="42" fill="{ACCENT}">{esc(title)}</text>',
    ]
    y += 62
    for b in bullets[:5]:
        for j, ln in enumerate(wrap(b, 62)):
            prefix = '<tspan fill="#FF9F1C">&#8226;</tspan>  ' if j == 0 else "    "
            parts.append(
                f'<text x="72" y="{y}" font-family="Arial, Helvetica, sans-serif" '
                f'font-size="28" fill="{WHITE}">{prefix}{esc(ln)}</text>')
            y += 40
        y += 16
    parts.append(
        f'<text x="72" y="{H - 40}" font-family="Arial, Helvetica, sans-serif" font-size="18" '
        f'fill="{MUTED}">LKS-SHS · the PULSE loop — self-healing software, engineered with AI</text>')
    parts.append(
        f'<text x="{W - 72}" y="{H - 40}" text-anchor="end" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="18" fill="{MUTED}">{index:02d} / {total:02d}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def sh(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{proc.stderr[-2000:]}")
    return proc.stdout.strip()


def rasterize(svg_path: str, png_path: str) -> None:
    subprocess.run(["qlmanage", "-t", "-s", str(W), "-o",
                    os.path.dirname(png_path) or ".", svg_path],
                   check=True, capture_output=True)
    thumb = svg_path + ".png"
    if not os.path.exists(thumb):
        sys.exit(f"qlmanage produced no thumbnail for {svg_path}")
    os.replace(thumb, png_path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--voice", default="Samantha")
    args = ap.parse_args()

    sections = parse_script(args.script)
    if not sections:
        sys.exit("no slides parsed")
    out = args.out or os.path.splitext(args.script)[0] + ".mp4"
    work = tempfile.mkdtemp(prefix="pulse-vid-")
    parts = []
    total = len(sections)

    for i, sec in enumerate(sections):
        aiff = os.path.join(work, f"s{i:02d}.aiff")
        subprocess.run(["say", "-v", args.voice, "-o", aiff, sec["narration"]], check=True)
        dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", aiff]))

        svg = os.path.join(work, f"s{i:02d}.svg")
        open(svg, "w").write(slide_svg(sec["title"], sec["bullets"], i + 1, total))
        png = os.path.join(work, f"s{i:02d}.png")
        rasterize(svg, png)

        part = os.path.join(work, f"p{i:02d}.ts")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-loop", "1", "-framerate", str(FPS), "-i", png, "-i", aiff,
             "-af", "apad=pad_dur=0.8",
             "-vf", f"crop={W}:{H}",  # qlmanage letterboxes into a square canvas
             "-map", "0:v", "-map", "1:a", "-t", f"{dur + 0.8:.2f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p",
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
