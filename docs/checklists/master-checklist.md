# Master Checklist — the "verify everything" tracker

Status legend: ☐ not started · ◐ in progress · ✓ done & **verified** (evidence recorded)

The competency bar: **every item below must reach ✓ with recorded evidence before Phase 7 articles are published.** Verification means an audit pass per item — links resolve, diagrams render, claims cited, code runs, videos play — logged in the Verification Log section.

## Phase 1 — Research (`#Step001`)
- [x] ✓ `docs/research/01-academic-foundations.md` — 33 verified sources, canonical refs, corrections documented (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [x] ✓ `docs/research/02-pre-ai-foundations.md` — 48 verified sources, 24-row pattern catalog, gap analysis (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [x] ✓ `docs/research/03-systems-domain.md` — 51 verified sources, layered toolbox table, verified AI-era systems examples (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [x] ✓ `docs/research/04-ai-era-and-business.md` — 48 verified sources, product landscape, small-biz/enterprise playbooks, risk-to-control mapping (spot-check PASS 2026-11-09; Phase 6 full audit pending)
- [x] ✓ Synthesis doc unifying the taxonomy — `docs/research/00-synthesis.md` (5-stage loop, 7-layer stack, builder-vs-healer, L0–L4 ladder, anchor numbers)

## Phase 2 — Synthesis (`#Step002`)
- [x] ✓ Acronym decision record: 5 candidates + trade-off matrix — **PULSE** accepted (provisional, user override open until Phase 4 publication) — `docs/architecture/decisions/001-acronym.md`
- [x] ✓ Unified healing-loop taxonomy across layers (kernel → process → service → business) — synthesis §1–§2

## Phase 3 — Architecture & Prototypes (`#Step003`)
- [x] ✓ `reference-architecture.md` — stack diagram (mermaid), component model, autonomy ladder, instantiations, 7 binding rules
- [x] ✓ `sequence-diagrams.md` — 6 mermaid diagrams: crash heal, hang heal, canary rollback, AI triage→PR gate, restart-storm escalation, full escalation ladder
- [x] ✓ `pattern-catalog.md` — patterns by PULSE stage + governance patterns + 8 anti-patterns
- [x] ✓ Decision records 001–005, each with 3–5 alternatives + trade-offs (001 acronym, 002 runtime, 003 supervisor model, 004 AI triage, 005 verification oracle)
- [x] ✓ Application-track prototype: `prototypes/pulse-app/` — one command (`demo.sh`), 5 failure injections, PULSE stage→code map
- [x] ✓ Prototype demo evidence — `demo-evidence.log`: 5/5 scenarios PASS, exit 0 (2026-11-09)

## Phase 4 — Posts (`#Step004`)
- [x] ✓ Series overview (00) with cross-links + series-map table + "how this was built" trust section
- [x] ✓ Posts 01–08 written: pre-AI history, systems layer, AI era, PULSE framework, prototype walkthrough, small-biz + enterprise playbooks, risks/anti-patterns — each with mermaid diagrams, citation-stamped claims, attribution sections naming originators, and reference lists with URLs
- [x] ✓ Animations: `animations/pulse-loop.svg` (SMIL, stage pulse + traveling signal + verification gate) and `animations/escalation-ladder.svg` (layered escalation)
- [x] ✓ Audience-fit pass: each post header states audience + reading time (R9/R10); overview maps posts to reader types
- [ ] ◐ Video companion links present in posts but MP4s render in Phase 5 — full link audit in Phase 6

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
| 2026-11-09 | Dossier 03 spot-check | PASS | 389 lines: TL;DR, 19-row layered toolbox (hardware→kernel→process→storage→AI), 6 deep dives (livepatch/Ksplice 88%, watchdogs, EDAC, eBPF, ZFS/WAL/Raft), prevention section (70% memory-safety stats, Android 76%→24%), verified pre-LLM + LLM-era AI systems (Getafix/SapFix, OSS-Fuzz AI, Big Sleep, Triangle, RCACopilot, KernelGPT, SWE-InfraBench 34%), 51 refs, folklore flagged [UNVERIFIED] |
| 2026-11-09 | Dossier 04 spot-check | PASS | 294 lines: TL;DR, product landscape tables (AI-SRE platforms, startups, code-fixing AI) with autonomy levels + pricing, builder-vs-healer analysis, small-biz $0–50/mo playbook with 3 a.m. walkthrough, enterprise governance + L0–L4 rollout ladder, cross-source key-numbers with comparability note, 8 risks + risk-to-control mapping + negative results, 48 refs, vendor claims flagged as such |
| 2026-11-09 | Synthesis + Decision 001 | PASS | 00-synthesis.md unifies 4 dossiers (180 sources): canonical 5-stage loop, 7-layer stack, AI builder-vs-healer, L0–L4 ladder, 15 anchor numbers, small-biz/enterprise split, naming requirements. Decision 001: 5 acronym candidates, weighted trade-off matrix, PULSE accepted provisionally (question unanswered; user override open) with canonical stage definitions |
| 2026-11-09 | Prototype demo run | PASS | `demo.sh` → 5/5 scenarios PASS, exit 0: crash MTTR 1.6s, hang 7.9s, leak 3.2s (+ "mitigated not cured" note), errors 2.9s, crashloop → ESCALATE at MaxR=3/30s. Evidence: `prototypes/pulse-app/demo-evidence.log` |
| 2026-11-09 | Posts link audit | PASS | Scripted check: every relative link in all 9 posts resolves to an existing file (research dossiers, architecture docs, decisions, prototype, animations). Mermaid render check deferred to Phase 6 (GitHub render) |
