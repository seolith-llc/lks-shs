# Master Checklist — the "verify everything" tracker

Status legend: ☐ not started · ◐ in progress · ✓ done & **verified** (evidence recorded)

The competency bar: **every item below must reach ✓ with recorded evidence before Phase 7 articles are published.** Verification means an audit pass per item — links resolve, diagrams render, claims cited, code runs, videos play — logged in the Verification Log section.

## Phase 1 — Research (`#Step001`)
- [x] ✓ `docs/research/01-academic-foundations.md` — 33 verified sources, canonical refs, corrections documented (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [x] ✓ `docs/research/02-pre-ai-foundations.md` — 48 verified sources, 24-row pattern catalog, gap analysis (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [ ] ◐ `docs/research/03-systems-domain.md` — ≥20 verified sources, layered toolbox
- [ ] ◐ `docs/research/04-ai-era-and-business.md` — ≥25 verified sources, product landscape
- [ ] ☐ Synthesis doc unifying the taxonomy (Phase 2 input)

## Phase 2 — Synthesis (`#Step002`)
- [ ] ☐ Acronym decision record: 3–5 candidates, trade-off table, recommendation, decision
- [ ] ☐ Unified healing-loop taxonomy across layers (kernel → process → service → business)

## Phase 3 — Architecture & Prototypes (`#Step003`)
- [ ] ☐ `reference-architecture.md` with stack diagram
- [ ] ☐ `sequence-diagrams.md` (mermaid, at least: heal-loop, human-gated heal, canary rollback, AI triage)
- [ ] ☐ `pattern-catalog.md`
- [ ] ☐ Decision records: **every** major choice with 3–5 alternatives + trade-offs
- [ ] ☐ Application-track prototype: one-command run, failure injection, healing demonstrable
- [ ] ☐ Prototype demo evidence (run log / recording)

## Phase 4 — Posts (`#Step004`)
- [ ] ☐ Series overview with cross-links + per-post attribution sections
- [ ] ☐ Each post: mermaid diagrams render on GitHub, animations work, all claims cross-reference dossiers
- [ ] ☐ Audience-fit pass (which post serves which reader)

## Phase 5 — Video (`#Step005`)
- [x] ✓ Pipeline smoke test: `say` → ffmpeg MP4 (9.0s, 104 KB, `docs/video/scripts/smoke-test.sh`; run 2026-11-09)
- [ ] ☐ Premium/enhanced voice install (optional upgrade; base voice fallback verified)
- [ ] ☐ Per-post narration scripts
- [ ] ☐ Rendered MP4s linked bidirectionally with posts

## Phase 6 — Verification & improvement loop (`#Step006`)
- [ ] ☐ Audit pass 1 over all artifacts; defects logged and fixed; repeat until zero blocking defects
- [ ] ☐ Axioms & rules: every draft axiom upgraded to *verified* (evidence linked) or dropped
- [ ] ☐ External dry-run: diagrams/citations spot-checked in a clean render

## Phase 7 — Articles (`#Step007`)
- [ ] ☐ `eli5.md` · ☐ `entry-level.md` · ☐ `professional.md` · ☐ `c-suite.md`
- [ ] ☐ Consistency pass: same facts, four altitudes, no contradictions

## Continuous
- [x] ✓ Prompt history every turn + INDEX current (protocol: `docs/prompt-histories/README.md`)
- [x] ✓ Git milestone commits

## Verification Log

| Date | Item | Verdict | Evidence |
|---|---|---|---|
| 2026-11-09 | Video pipeline | PASS | `tmp/smoke/smoke.mp4` 8.99s / 103,835 B via `smoke-test.sh` |
| 2026-11-09 | Toolchain | PASS | ffmpeg 9.0.1, python 3.14.7, node, docker present; 185 macOS voices (0 premium installed) |
| 2026-11-09 | Dossier 01 spot-check | PASS | ~330 lines: TL;DR, timeline (1956→2026), 5 deep dives, self-* taxonomy with detect/diagnose/recover/learn, key numbers, before/after-AI table, 12 canonical + 33 full sources, 7 open questions; [UNVERIFIED] discipline observed; 3 brief corrections verified |
| 2026-11-09 | Dossier 02 spot-check | PASS | ~250 lines: TL;DR, unifying healing-loop table (15 systems × observe/decide/act/feedback), 8 deep dives, 24-row pattern catalog, cited key numbers (243× retry math, nine-nines debunk, outage costs), 7-point gap analysis, 48-entry source list, 6 open questions; RAID paper honestly [UNVERIFIED] |
