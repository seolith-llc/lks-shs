# Decision 001 — The Framework Acronym

**Status:** PROPOSED (awaiting decision) · **Date:** 2026-11-09 · **Rule:** R2 (3–5 alternatives, trade-offs, justified recommendation)

## Context

The series needs a name for the canonical 5-stage loop defined in `docs/research/00-synthesis.md` (sense → diagnose → remediate → verify → learn). Requirements from synthesis §7: express the loop stages; work at every layer (kernel → org); not overclaim autonomy (no verified L4 exists); honor MAPE-K/OTP lineage; survive four audience altitudes. The repo/project umbrella stays **LKS-SHS (Self-Healing Software)** regardless — this decision names *the loop/framework* that lives inside it.

## Alternatives considered

### A. PULSE — **P**erceive · **U**nderstand · **L**ocalize · **S**olve · **E**volve

- **Pros:** complete 5-stage mapping with localization explicit (the stage where 2024 pipelines won, D01[24][25]); "pulse" is the literal health primitive at every layer — sd_notify heartbeats, liveness probes, Raft heartbeats, dead-man's-switches (D02[7][8], D03[7], D04[35]); vital-signs metaphor spans all four altitudes ("check the system's pulse" is ELI5-comprehensible); pronounceable, brandable, verb-able ("the system PULSEs").
- **Cons:** doesn't literally say "repair"; verification is implicit at the Solve→Evolve boundary rather than a letter (must be documented — Solve always ends with a verification gate); minor name collisions (PulseAudio) — mitigated by "the PULSE loop" phrasing.

### B. REPAIR — **R**eceive · **E**stimate · **P**atch · **A**ssess · **I**ntegrate · **R**ecord

- **Pros:** the word *is* the topic — zero explanation needed; 6 stages include explicit Assess (verification) and Record (learning); strong C-suite register ("we REPAIR in production").
- **Cons:** expansion is contrived (Receive/Estimate read forced); "Patch" narrows healing to code changes — restarts, rollbacks, re-elections aren't patches (misleading for systems programming); 6 stages harder to remember; generic word = weak search/brand distinctiveness; overclaims (most real systems stop at rollback).

### C. HEAL — **H**ealth-sense · **E**valuate · **A**ct · **L**earn

- **Pros:** the topic word itself; cleanest MAPE-K descendant (4 stages, direct Monitor→Health-sense lineage); shortest; friendly at ELI5 altitude.
- **Cons:** only 4 stages — no explicit localization *or* verification, which contradicts axiom A6 and the strongest empirical finding (non-LLM verification gates are what make AI fixes shippable); maximally generic (unownable); "heal" overstates what today's systems do (they mitigate).

### D. CURE — **C**heck · **U**nderstand · **R**emediate · **E**volve

- **Pros:** evocative medical metaphor with a *built-in taxonomy* — triage (restart) vs. treatment (rollback) vs. cure (fix the code) — which is genuinely the series' core distinction (D02: "restart is not repair"); 4 stages, clean.
- **Cons:** "cure" overclaims even harder than "heal" (a verified cure is exactly what nobody has); no explicit verification; medical metaphor may tire over a long series; some audiences read "CURE" as healthtech.

### E. No loop acronym — descriptive only ("the self-healing loop" inside SHS)

- **Pros:** most honest; zero branding risk; nothing to explain.
- **Cons:** unownable and unmemorable — every post, diagram, and video would carry a generic phrase; fails R10's four-altitude test (no handle for the C-suite to remember); wastes the series' naming opportunity.

## Trade-off matrix

| Criterion (weight) | PULSE | REPAIR | HEAL | CURE | none |
|---|---|---|---|---|---|
| Loop-stage completeness (×3) | ★★★ | ★★★ | ★ | ★★ | — |
| Verification explicit (×3) | ★★ (documented gate) | ★★★ | ★ | ★ | — |
| Cross-layer truth (×2) | ★★★ | ★★ ("patch") | ★★★ | ★★ | ★★★ |
| Memorable/brandable (×2) | ★★★ | ★★ | ★★ | ★★ | ★ |
| Four-altitude clarity (×2) | ★★★ | ★★ | ★★★ | ★★ | ★ |
| Honesty (no overclaim) (×2) | ★★★ | ★★ | ★★ | ★ | ★★★ |
| Lineage nod (×1) | ★★ (heartbeat/OTP) | ★ | ★★★ (MAPE-K) | ★ | ★★ |

## Recommendation

**PULSE.** It is the only candidate that keeps all five synthesized stages visible (including localization), names a mechanism that literally exists at every layer of the stack (the heartbeat), and does not overclaim autonomy — while remaining translatable from ELI5 ("feeling the system's pulse") to C-suite ("PULSE-gated autonomy"). Its one real gap (verification as an implicit gate) is addressed by *defining* the Solve→Evolve boundary as the mandatory verification gate in every diagram — turning the weakness into a teaching moment. **SHS remains the umbrella**: "the PULSE loop is the heartbeat of a Self-Healing System."

## Decision

_(recorded after user selection)_
