# Decision 007 — Slide Design System & Rasterization Rule

**Status:** ACCEPTED · **Date:** 2026-11-09 · **Trigger:** user feedback — slides were "pathetic." Investigation showed they were not just plain: they were **broken** (see Rasterization, below).

## Context

8 video episodes × 4–7 slides each. Slides are generated as SVG from the episode scripts, rasterized by macOS QuickLook (`qlmanage`), muxed over narration by ffmpeg. The original design was flat navy + text.

## What was wrong

1. **Aesthetic:** flat background, undifferentiated text, no hierarchy, no data emphasis.
2. **Structural (the real bug):** `qlmanage` renders **non-square SVGs at a broken ~1.66× scale, top-left anchored** — content was shifted and clipped at the right/bottom edges of every slide in the first two render passes. A pixel-corner check on the uniform navy background passed while all layout was broken — a lesson in why oracle checks must sample *content*, not just background.

## The design system (v3, accepted)

- **Canvas rule:** author slides on a **1280×1280 square** SVG with the 16:9 band vertically centered (`DY=280`); rasterize at `-s 2560` (2× supersample); ffmpeg `crop=2560:1440,scale=1280:720`. Square SVGs map 1:1 per `-s` unit — verified by marker-rect pixel probes.
- **Visual language:** navy gradient + faint grid + two corner glows; LKS-SHS and EP badges; white 44px titles with gold underline bar; **bullet rows with colored icon chips** (▸●◆✓★ cycling the PULSE stage palette); **big-stat callout cards** (`-! <BIG> | <label>` script syntax — display-only, never spoken); segmented progress bar in the footer; dedicated centered title card (PULSE wordmark + five stage dots).
- **Vertical centering** of the content block so short slides don't hug the top.

## Alternatives considered

1. **Keep flat design, tune typography** — rejected: no data emphasis; and cosmetic tuning while the rasterization bug existed would have polished broken output.
2. **HTML/CSS slides + headless browser screenshots** — richer layout possible; rejected: adds a browser dependency; SVG shares the series' existing design language.
3. **ffmpeg drawtext** — unavailable in this build (Decision 006 context); also weaker typography.
4. **Static PNG slide templates + overlay** — loses script-driven generation and re-renderability.

## Acceptance gate

Two-round visual acceptance via a read-only visual-judge agent (sample slides → fix → re-judge; then real extracted MP4 frames): all slides PASS on hierarchy, balance, clipping, legibility. Evidence frames committed under `docs/video/verification/`.

## Re-render contract

Slide changes never affect narration audio; durations are a pure function of the narration. Re-rendering after visual changes therefore keeps post duration stamps valid (verified: all 8 episodes reproduced their previous durations exactly).
