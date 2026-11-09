# Decision 006 — Narration Engine for the Video Series

**Status:** ACCEPTED (supersedes the voice plan in the Phase 5 pipeline) · **Date:** 2026-11-09 · **Trigger:** user feedback — base `say` voice sounded robotic, not human-like.

## Context

The original decision (turn 1) chose "auto-rendered MP4 with macOS voices" over paid TTS APIs (zero cost). The machine has **no premium/enhanced voices installed** (0 of 185), so episode renders used base Samantha — diphone-class synthesis with flat prosody. The user rejected the result: "still robotic, not human-like."

## Alternatives

1. **Install macOS premium voices (GUI download) + keep `say`** — free, local, better than base but still concatenative; requires manual System Settings action per voice; quality ceiling well below neural TTS.
2. **edge-tts (Microsoft neural voices, local CLI hitting Microsoft's free endpoint)** — studio-grade naturalness (Jenny/Aria/Christopher-class voices), zero cost, no API key, `pip install` into a project venv. *Trade-off:* narration text is processed by Microsoft's endpoint (cloud dependency; fine for public series narration, documented).
3. **piper (fully local neural TTS)** — offline, MIT-licensed, good quality. *Trade-off:* noticeably below Azure-class neural voices; model downloads; CPU synthesis time.
4. **ElevenLabs / OpenAI TTS API** — top-tier quality. *Trade-off:* paid per character, API key management — rejected at turn 1 and unchanged.
5. **Prosody-tuned `say` (embedded `[[rate]]/[[pmod]]` commands, pauses)** — free improvement but polishes a fundamentally diphone voice; cannot reach "human-like."

## Decision

**edge-tts (option 2) as the default engine**, voice `en-US-JennyNeural`, with `--engine say --voice <name>` kept as a fully-offline fallback in `render_episode.py` (the venv is gitignored; the renderer auto-detects it). Rationale: it is the only option that satisfies all three constraints simultaneously — human-like quality, zero cost, no API key. The cloud-processing trade-off is documented here and in the video README; anyone needing full offline rendering runs `--engine say` or swaps in piper (option 3) without touching the pipeline.

All 8 episodes re-rendered with the neural voice on 2026-11-09 (durations 1:47–2:16); post duration stamps and the video README updated to match.
