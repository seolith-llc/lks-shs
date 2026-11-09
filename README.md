# LKS-SHS — Self-Healing Software, Engineered with AI

A research, architecture, and content project on **self-healing software**: systems that detect, diagnose, and repair themselves — from kernel-level mechanisms to LLM-driven remediation agents — covering **system programming**, **application programming**, and the needs of **small businesses** and **enterprises**.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/prompt-histories/` | Verbatim log of every request & response — one date-time-named file per turn |
| `docs/research/` | Sourced research dossiers (academic foundations, pre-AI practice, systems domain, AI era & business) |
| `docs/architecture/` | Reference architecture, stack diagrams, sequence diagrams, patterns, trade-off analyses |
| `docs/posts/` | The public post series (cross-post ready, diagrams + animations + attribution) |
| `docs/articles/` | Audience-specific articles (ELI5 → entry-level → professional → C-suite) |
| `docs/checklists/` | Checklists, reference rules, axioms, verification records |
| `docs/video/` | Scripts, storyboards, rendered videos linked to posts |
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
- [ ] Phase 4 — Post series (diagrams, animations, attribution)
- [ ] Phase 5 — Video content linked to posts
- [ ] Phase 6 — Verification & improvement loop (checklist, rules, axioms)
- [ ] Phase 7 — Four audience articles (ELI5 / entry-level / professional / C-level)
