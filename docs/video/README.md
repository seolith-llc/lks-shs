# Video (`#Step005`)

Eight narrated episode companions to the post series, one per post. **Voice: `en-US-JennyNeural`** via edge-tts — neural, human-like narration (Decision 006, after user feedback that macOS base voices sounded robotic). The offline `say` fallback remains one flag away: `--engine say --voice Samantha`.

| Episode | File | Length | Companion post |
|---|---|---|---|
| 01 · Seventy Years of Self-Healing | [`01-seventy-years.mp4`](01-seventy-years.mp4) | 2:01 | `../posts/01-seventy-years-of-self-healing.md` |
| 02 · The Systems Layer | [`02-systems-layer.mp4`](02-systems-layer.mp4) | 2:06 | `../posts/02-the-systems-layer.md` |
| 03 · What Actually Shipped in the AI Era | [`03-ai-era.mp4`](03-ai-era.mp4) | 2:04 | `../posts/03-the-ai-era-what-actually-shipped.md` |
| 04 · The PULSE Framework | [`04-pulse-framework.mp4`](04-pulse-framework.mp4) | 1:47 | `../posts/04-the-pulse-framework.md` |
| 05 · PULSE in ~600 Lines of Python | [`05-prototype-demo.mp4`](05-prototype-demo.mp4) | 1:53 | `../posts/05-pulse-in-python.md` |
| 06 · The Small-Business Playbook | [`06-small-business.mp4`](06-small-business.mp4) | 1:54 | `../posts/06-the-small-business-playbook.md` |
| 07 · The Enterprise Playbook | [`07-enterprise.mp4`](07-enterprise.mp4) | 2:05 | `../posts/07-the-enterprise-playbook.md` |
| 08 · Risks, Anti-Patterns, the Road to L4 | [`08-risks.mp4`](08-risks.mp4) | 2:16 | `../posts/08-risks-anti-patterns-road-to-l4.md` |

## Pipeline (`scripts/`)

`NN-*.md` episode script (slides = `##` headings + bullets; narration = plain paragraphs) →
`render_episode.py` → per slide: **neural TTS** (`edge-tts` in `scripts/.venv`, gitignored — narration text is processed by Microsoft's free endpoint; use `--engine say` for fully-local rendering) · generate styled SVG slide (same palette/typography as `../posts/animations/`) · QuickLook rasterizes (`qlmanage`) · ffmpeg muxes slide+audio (center-cropped 1280×720) → concat → `NN-*.mp4`.

Notes:
- This machine's ffmpeg build ships without text filters (no drawtext/libass), hence the SVG+QuickLook slide path — which also keeps slide rendering identical across platforms.
- Render everything: `scripts/render_all.sh` · one episode: `scripts/render_episode.py <script.md> <out.mp4> [--engine edge|say] [--voice <name>]`.
- Scripts are committed next to renders (rule R6) so narration is reviewable and re-renderable.
