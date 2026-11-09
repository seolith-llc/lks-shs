# Video (`#Step005`)

Pipeline: markdown script → macOS `say` voice track → ffmpeg render → MP4, linked bidirectionally with its post.

- `scripts/` — reusable pipeline scripts (voice + render)
- `scripts/` also holds per-episode narration scripts
- rendered finals committed here as `NN-*.mp4` alongside a poster frame

Voice note: no premium/enhanced voices installed yet; base voices (e.g. Samantha) are used. Installing premium voices in macOS System Settings upgrades quality with zero pipeline changes.
