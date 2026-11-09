---
step: "#Step005 revision — neural narration"
turn: 8
timestamp: 2026-11-09 12:46 EST
---

# Request

The video is still robotic not huuman like

# Response

Diagnosed and fixed: base macOS `say` voices are diphone synthesis — no premium voices were installed (0/185), so Phase 5 rendered with flat-prosody Samantha.

**Fix (Decision 006):** default narration engine switched to **edge-tts** (`en-US-JennyNeural`, Microsoft neural voice) running in a project venv (`docs/video/scripts/.venv`, gitignored). Zero cost, no API key, studio-grade naturalness; `--engine say --voice <name>` retained as fully-offline fallback; cloud-processing trade-off (narration text → Microsoft endpoint) documented in the decision record and video README.

**All 8 episodes re-rendered** with the neural voice; durations changed (now 1:47–2:16), so post duration stamps and the video README table were regenerated from actual ffprobe durations.

Renderer updated: `synth()` engine abstraction (edge mp3 / say aiff), auto-detects venv, `--engine`/`--voice` flags. One leftover-variable bug (`aiff` → `audio`) caught and fixed on first re-render.

Persisted to memory: video narration must be neural/human-like; never silently ship base-voice audio.

# Decisions

- TTS engine: **edge-tts / en-US-JennyNeural** (assistant action per user's quality complaint; documented alternatives: premium macOS voices, piper local, paid APIs — see Decision 006).

# Artifacts

- Updated: `render_episode.py` (engine abstraction), 8 MP4s re-rendered, 8 posts (durations), `docs/video/README.md`, `.gitignore` (venv), memory file, INDEX, this file
- Created: `docs/architecture/decisions/006-tts-engine.md`
- Commit + push to origin (repo is live at github.com/seolith-llc/lks-shs)
