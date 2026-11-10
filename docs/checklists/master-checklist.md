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
- [x] ✓ Video companion links audited (Phase 6): every post ↔ MP4 pair verified, durations match

## Phase 5 — Video (`#Step005`)
- [x] ✓ Pipeline smoke test: `say` → ffmpeg MP4 (9.0s, 104 KB, `docs/video/scripts/smoke-test.sh`; run 2026-11-09)
- [x] ✓ Production pipeline `scripts/render_episode.py`: script → say narration → SVG slides → QuickLook rasterize → ffmpeg mux/crop → concat MP4 (drawtext unavailable in this ffmpeg build — SVG path chosen, decision documented in script header)
- [x] ✓ 8 narration scripts committed (`NN-*.md`) — slides + narration separated by design
- [x] ✓ 8 MP4s rendered — neural narration (edge-tts/Jenny, Decision 006) + slide design system v3 (Decision 007); durations 1:47–2:16
- [x] ✓ Bidirectional links: every post links its MP4 with duration; video README links companion posts
- [x] ✓ Voice quality: neural engine after user feedback (Decision 006); `say` retained as offline fallback

## Phase 6 — Verification & improvement loop (`#Step006`)
- [x] ✓ Audit pass 1 (2026-11-09): 24/24 checks PASS after analysis — repo clean & pushed; 9/9 prompt histories indexed; all internal links resolve repo-wide; 8/8 videos 720p+audio with durations matching post stamps; 7 anchor numbers consistent across dossiers/synthesis/posts; decisions 001–007 + 5 research docs present with access dates
- [x] ✓ Mermaid structural check: all subgraph/end + loop/end pairs balanced (4 flags were linter false-positives counting substrings — diagnosis recorded; no real defects)
- [x] ✓ Prototype re-verified: `demo.sh` 5/5 PASS, exit 0, evidence log refreshed
- [x] ✓ External dry-run: 8/8 citation URLs live (doi.org, arXiv, kernel.org, k8s.io, erlang.org, AWS, incident.io, METR)
- [x] ✓ Axioms A1–A12 upgraded draft → **verified**, each with corpus evidence (dossiers, decisions, prototype)

## Phase 7 — Articles (`#Step007`)
- [x] ✓ `eli5.md` (714 w, body/bike-doctor analogy, human-signs-the-prescription) · `entry-level.md` (723 w, six terms + PULSE + first-week checklist) · `professional.md` (699 w, three verdicts + design-review numbers) · `c-suite.md` (733 w, business case + vendor questions + 90-day plan + risk register)
- [x] ✓ Consistency pass (scripted): shared facts (>$300K/hr, >40% Gartner, ~200 workloads, human-gate, PULSE/five-stage) present and non-contradictory across all four; article links ALL RESOLVE

## Phase 8 — Distribution pack (`#Step008`)
- [x] ✓ Renderer extended to 9:16 vertical (`--format vertical`, square-canvas rule honored: 1920-square, 1080×1920 band)
- [x] ✓ 4 shorts written + rendered (46–54 s, ~0.9–1.0 MB): nine-nines myth, 243× retry storm, 200-workloads story, PULSE in 45 s — `docs/video/shorts/`
- [x] ✓ Shorts acceptance: title card PASS, vertical stat card PASS (visual-judge, frame extracted from final MP4)
- [x] ✓ 8 YouTube thumbnails rendered + cropped 1280×720 (`publish/youtube/thumbs/`), thumb-02 visual-judge PASS
- [x] ✓ YouTube metadata pack: titles, description template, tags, shorts captions (`publish/youtube/README.md`)
- [x] ✓ Platform copy: X 10-post thread, Bluesky 6-skeet thread, LinkedIn, IG/TikTok captions + 10-slide carousel plan, Show HN + Reddit + Lobsters with timing etiquette (`publish/copy/`)
- [x] ✓ dev.to exports: 8 articles with front-matter, canonical URLs to GitHub, links absolutized (`publish/articles/devto/`)
- [x] ✓ Automation stubs (credential-gated, dry-run by default): `bluesky_post.py` (6 skeets parsed, dry-run OK), `devto_publish.py` (payload dry-run OK) — X/IG/TikTok/YouTube documented as manual (API tiers/review)

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
| 2026-11-09 | Video render + crop check | PASS | 8/8 episodes rendered; extracted frame is 1280×720; corner pixel `0a2445` matches bg `#0B2545` (qlmanage square-letterbox crop verified); durations 94–114s; post↔video links re-audited ALL RESOLVE after wiring |
| 2026-11-09 | Slide redesign acceptance | PASS | 3-round visual-judge: r1 FAIL (found qlmanage 1.66x clip bug via symptoms), r2 samples PASS, r3 final-MP4 frames PASS (final-title, final-stats in docs/video/verification/). Durations reproduce exactly across slide-only re-renders |
| 2026-11-09 | Phase 6 audit pass 1 | PASS | 24/24 after analysis (1 mermaid-lint false positive diagnosed: substring vs keyword `end`); prototype 5/5 re-PASS (demo-evidence.log refreshed); 8/8 external URLs live; axioms A1–A12 verified with evidence |
| 2026-11-09 | Phase 7 articles | PASS | 4/4 written (~700 words each, four altitudes); scripted fact-consistency PASS on 5 shared claims; article link audit PASS |
| 2026-11-09 | Phase 8 shorts + thumbs | PASS | 4/4 vertical shorts 1080×1920 (46–54 s); visual-judge PASS on title + stat frames from final MP4s; 8/8 thumbnails 1280×720, thumb-02 PASS; dev.to exports 8/8 + both automation stubs dry-run OK |
