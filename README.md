# LKS-SHS — Self-Healing Software, Engineered with AI

**Repository:** https://github.com/seolith-llc/lks-shs

A research, architecture, and content project on **self-healing software**: systems that detect, diagnose, and repair themselves — from kernel-level mechanisms to LLM-driven remediation agents — covering **system programming**, **application programming**, and the needs of **small businesses** and **enterprises**.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/prompt-histories/` | Verbatim log of every request & response — one date-time-named file per turn |
| `docs/research/` | Sourced research dossiers (academic foundations, pre-AI practice, systems domain, AI era & business) |
| `docs/architecture/` | Reference architecture, stack diagrams, sequence diagrams, patterns, trade-off analyses |
| `docs/posts/` | The public post series (cross-post ready, diagrams + animations + attribution) |
| `docs/animations/` | Interactive single-file PULSE simulator (`pulse-interactive.html`) + animated SVGs + acceptance evidence |
| `docs/articles/` | Audience-specific articles (ELI5 → entry-level → professional → C-suite) |
| `docs/checklists/` | Checklists, reference rules, axioms, verification records |
| `docs/video/` | Scripts, storyboards, rendered videos (8 episodes + 4 vertical shorts) linked to posts |
| `docs/articles/` | Audience-specific articles (ELI5 → entry-level → professional → C-suite) |
| `publish/` | Distribution pack: platform copy, YouTube metadata + thumbnails, dev.to exports, automation stubs |
| `prototypes/` | Runnable prototype code |

## Conventions

1. **Prompt history.** Every user request and assistant response is archived verbatim in `docs/prompt-histories/` as `YYYY-MM-DD_HHMMSS-slug.md` (see that folder's README). The folder is re-organized regularly and indexed in `INDEX.md`.
2. **Citation discipline.** Research claims cite primary sources (author/org, year, URL, access date). Anything unverifiable is marked `[UNVERIFIED]`.
3. **Decision discipline.** Design choices are documented as **3–5 alternatives with trade-offs** and a justified recommendation.
4. **Steps.** Work proceeds in numbered steps: `#Step000` bootstrap, `#Step001` research, `#Step002` synthesis, … recorded in each prompt-history file.

## Status

- [x] Phase 0 — Repository bootstrap (`#Step000`)
- [x] Phase 1 — Research (`#Step001`) — 4 dossiers, 180 verified sources
- [x] Phase 2 — Synthesis: **PULSE** loop (provisional) + unified taxonomy
- [x] Phase 3 — Architecture, patterns, prototypes — reference architecture, 6 sequence diagrams, pattern catalog, decisions 001–005, PULSE prototype (5/5 PASS)
- [x] Phase 4 — Post series — 9 posts + animated SVGs, link-audited
- [x] Phase 5 — Video — 8 narrated episodes (neural voice + slide design system, decisions 006–007)
- [x] Phase 6 — Verification loop — 24/24 audit PASS, axioms A1–A12 verified, URLs live
- [x] Phase 7 — Four audience articles (ELI5 / entry-level / professional / C-level), consistency-checked
- [x] Phase 8 — Distribution pack: 4 vertical shorts, YouTube thumbnails + metadata, platform copy, dev.to exports, credential-gated automation (`publish/`)
- [x] Phase 9 — Use-case catalog, state/workflow model, interactive single-file simulator (`docs/animations/pulse-interactive.html`)
