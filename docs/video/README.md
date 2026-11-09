# Video (`#Step005`)

Eight narrated episode companions to the post series, one per post. Voice: macOS `say` (Samantha — install premium voices in System Settings → Spoken Content for a free quality upgrade with zero pipeline changes).

| Episode | File | Length | Companion post |
|---|---|---|---|
| 01 · Seventy Years of Self-Healing | [`01-seventy-years.mp4`](01-seventy-years.mp4) | 1:47 | `../posts/01-seventy-years-of-self-healing.md` |
| 02 · The Systems Layer | [`02-systems-layer.mp4`](02-systems-layer.mp4) | 1:52 | `../posts/02-the-systems-layer.md` |
| 03 · What Actually Shipped in the AI Era | [`03-ai-era.mp4`](03-ai-era.mp4) | 1:53 | `../posts/03-the-ai-era-what-actually-shipped.md` |
| 04 · The PULSE Framework | [`04-pulse-framework.mp4`](04-pulse-framework.mp4) | 1:34 | `../posts/04-the-pulse-framework.md` |
| 05 · PULSE in ~600 Lines of Python | [`05-prototype-demo.mp4`](05-prototype-demo.mp4) | 1:40 | `../posts/05-pulse-in-python.md` |
| 06 · The Small-Business Playbook | [`06-small-business.mp4`](06-small-business.mp4) | 1:38 | `../posts/06-the-small-business-playbook.md` |
| 07 · The Enterprise Playbook | [`07-enterprise.mp4`](07-enterprise.mp4) | 1:50 | `../posts/07-the-enterprise-playbook.md` |
| 08 · Risks, Anti-Patterns, the Road to L4 | [`08-risks.mp4`](08-risks.mp4) | 1:54 | `../posts/08-risks-anti-patterns-road-to-l4.md` |

## Pipeline (`scripts/`)

`NN-*.md` episode script (slides = `##` headings + bullets; narration = plain paragraphs) →
`render_episode.py` → per slide: `say` narration to AIFF · generate styled SVG slide (same palette/typography as `../posts/animations/`) · QuickLook rasterizes (`qlmanage`) · ffmpeg muxes slide+audio (center-cropped 1280×720) → concat → `NN-*.mp4`.

Notes:
- This machine's ffmpeg build ships without text filters (no drawtext/libass), hence the SVG+QuickLook slide path — which also keeps slide rendering identical across platforms.
- Render everything: `scripts/render_all.sh [voice]` · one episode: `scripts/render_episode.py <script.md> <out.mp4>`.
- Scripts are committed next to renders (rule R6) so narration is reviewable and re-renderable.
