# Use-Case Catalog — grounded in shipped code + planned features

**Date:** 2026-11-13 · **Scope:** everything `prototypes/pulse-app/`, `docs/video/scripts/`, and `publish/auto/` actually ships today, plus features that are decision-backed but not yet built. Every ✅ row cites the real function/file that implements it (verified 2026-11-13).

**Status legend:** ✅ **SHIPPED** (in code, demoable) · 🪝 **HOOK-READY** (interface shipped, external component needed) · 🚧 **PLANNED** (designed in a decision record, not built) · 💭 **PROPOSED** (from dossier open questions, no decision yet)

**Actors:** **Operator** (developer at a terminal) · **Supervisor** (the healer process) · **Service** (the supervised patient) · **Investigator** (L1 triage component) · **CI/CD** (pipeline running the demo headless) · **Publisher** (human or automation using the media/publish toolchain) · **External LLM** (optional pluggable component)

---

## A. The healing loop (prototype core)

| # | Use case | Actor → | Main flow (abbreviated) | Status | Evidence |
|---|---|---|---|---|---|
| A1 | Run the whole demo | Operator | `./demo.sh` → 5 scenarios → summary + exit code (0 = ALL PASS) | ✅ | `demo.sh`, `supervisor.py:main` |
| A2 | Run one scenario | Operator | `python3 supervisor.py --demo hang` | ✅ | `supervisor.py:main` (argparse choices) |
| A3 | Perceive layered signals | Supervisor | heartbeat age + `/health` gauge + out-of-band golden request each 0.3 s tick | ✅ | `supervisor.py:perceive` (DR005) |
| A4 | Post a dead-man's-switch heartbeat | Service | heartbeat thread writes timestamped file every 0.5 s; atomic `os.replace` | ✅ | `service.py:heartbeat_loop` |
| A5 | Report self-gauges | Service | `/health` → pid, uptime, requests, ballast_mb, faults, heartbeat flag | ✅ | `service.py:snapshot`, `do_GET` |
| A6 | Serve the golden request | Service | `GET /` → exact token `PULSE-OK` (oracle for correctness) | ✅ | `service.py:do_GET` |
| A7 | Classify a fault | Supervisor | percept → CRASHED / HUNG / LEAKING / ERRORING / HEALTHY by ordered rules | ✅ | `supervisor.py:understand` |
| A8 | Localize a fault | Supervisor | fault class → component + layer (runtime L3 / app logic / delivery L6) | ✅ | `supervisor.py:LOCALIZATION` |
| A9 | Heal by restart w/ capped backoff | Supervisor | kill → backoff 1→2→4→8 s → respawn | ✅ | `supervisor.py:solve` |
| A10 | Bound the healer (MaxR/MaxT) | Supervisor | ≥3 restarts in 30 s → ESCALATE, halt rescheduling, page human | ✅ | `supervisor.py:solve` (`max_restarts_in_window`) |
| A11 | Verify the heal (the gate) | Supervisor | fresh heartbeat **and** golden `PULSE-OK` within 10 s, else FAILED | ✅ | `supervisor.py:verify` |
| A12 | Record the heal (Evolve artifact) | Supervisor | event JSONL: stages, MTTR, triage, config → `healing-log.jsonl` | ✅ | `supervisor.py:_event` |
| A13 | Attach an L1 triage report | Investigator | ranked hypotheses + confidence + human-gate note on every event | ✅ | `triage.py:investigate` |
| A14 | Inject a wound on demand | Operator | `POST /inject/{crash\|hang\|leak\|errors}` | ✅ | `service.py:do_POST` |
| A15 | Clear soft faults | Operator | `POST /clear` → drop leak/errors, resume heartbeat | ✅ | `service.py:do_POST` |
| A16 | Crash-loop escalation drill | Operator | `--demo crashloop` → 4 crashes → ESCALATE verdict = PASS | ✅ | `supervisor.py:_crashloop` |
| A17 | Produce pass/fail evidence | Operator | committed `demo-evidence.log` (5/5 PASS, exit 0; re-verified 2026-11-09) | ✅ | `prototypes/pulse-app/demo-evidence.log` |

## B. Pluggable intelligence (interface shipped, brain optional)

| # | Use case | Actor → | Flow | Status | Evidence |
|---|---|---|---|---|---|
| B1 | Swap in a live LLM investigator | External LLM | set `PULSE_TRIAGE_CMD` → supervisor defers; command reads `{fault_class, summary}` JSON on stdin, 30 s timeout | 🪝 | `triage.py:investigate` (env hook) |
| B2 | Keep deterministic mode offline | Operator | no env var → rules engine, zero network | ✅ | `triage.py:RULES` (DR004) |
| B3 | L2 human-gated fix flow (PR + non-LLM validators) | Operator + CI/CD | triage → fix branch → tests/CI gate → human review → merge | 🚧 | DR004 (rejected for demo honesty); D04 ladder rung L2 |
| B4 | L3 bounded actuation (restart/rollback/scale classes, rate-capped) | Supervisor | pre-authorized reversible actions w/ budgets | 🚧 | 00-synthesis §4 rung L3; axioms A3/A11 |
| B5 | Canary analysis + auto-rollback | Supervisor | cohort KPI delta → promote/rollback (D3 sequence exists, not coded) | 🚧 | `sequence-diagrams.md` D3 |
| B6 | Multi-service supervision tree | Supervisor | parent supervisors, escalation upward (OTP-style) | 💭 | D02[1]; prototype is single-tier |

## C. Failure-mode coverage (what you can wound today)

| # | Use case | Flow / what it proves | Status | Evidence |
|---|---|---|---|---|
| C1 | Kill it (crash) | liveness death → restart, MTTR ~1.6 s | ✅ | scenario `crash` |
| C2 | Freeze it (hang) | heartbeat stops + handlers stall → only the dead man's switch catches it (liveness ≠ aliveness) | ✅ | scenario `hang`; `service.py` hang fault |
| C3 | Bloat it (leak) | 8 MB/request ballast → gauge > 40 MB → restart logged **"mitigated, not cured"** | ✅ | scenario `leak`; `service.py` ballast; hard cap 512 MB safety |
| C4 | Enrage it (errors) | 50 % 500s → rolling 6-probe error-rate ≥ 50 % → restart | ✅ | scenario `errors`; `supervisor.py` error window |
| C5 | Storm it (crashloop) | deterministic fault → healer refuses to thrash | ✅ | scenario `crashloop` |
| C6 | Starve the host (OOM-kill / cgroup pressure) | oom_score_adj-driven victim selection | 💭 | D03[12]; not coded |
| C7 | Corrupt it (data fault) | checksum mismatch → restore-from-redundancy path | 💭 | D03[22] (ZFS analog) |

## D. Media & publishing toolchain (shipped build system)

| # | Use case | Actor → | Flow | Status | Evidence |
|---|---|---|---|---|---|
| D1 | Render an episode | Publisher | script md → TTS → SVG slides → QuickLook → ffmpeg → MP4 (`--engine edge\|say`) | ✅ | `render_episode.py` |
| D2 | Render vertical shorts | Publisher | `--format vertical` → 1080×1920 MP4 | ✅ | `render_episode.py:Layout` |
| D3 | Batch-render the series | Publisher | `render_all.sh` (per-episode fault tolerance) | ✅ | `docs/video/scripts/render_all.sh` |
| D4 | Generate YouTube thumbnails | Publisher | 8 covers, 1280×720, big-stat design | ✅ | `make_thumbnails.py` |
| D5 | Export dev.to articles | Publisher | posts → front-matter + absolutized links + canonical URL | ✅ | `publish/auto/export_devto.py` |
| D6 | Post a Bluesky thread | Publisher | `bluesky_post.py` (dry-run default; needs `BSKY_*`) | 🪝 | `publish/auto/bluesky_post.py` |
| D7 | Draft a dev.to article via API | Publisher | `devto_publish.py` (unlisted draft; needs `DEVTO_API_KEY`) | 🪝 | `publish/auto/devto_publish.py` |
| D8 | Auto-publish to X / IG / TikTok / YouTube | Publisher | paste-ready assets only | 🚧 (manual by design) | `publish/README.md` |

## E. Verification & governance (project self-audit)

| # | Use case | Flow | Status | Evidence |
|---|---|---|---|---|
| E1 | Re-verify the prototype | run demo → 5/5 PASS, exit 0 | ✅ | last re-run 2026-11-09, logged |
| E2 | Audit repo integrity/links/durations | scripted battery, 24 checks | ✅ | Phase 6 audit (verification log) |
| E3 | Interactive model of the loop | single-file animated HTML page | ✅ (this release) | `docs/animations/pulse-interactive.html` |
| E4 | Continuous audit on every change | CI job re-running E1+E2 | 💭 | natural next step (GitHub Actions) |

---

## Coverage summary

- ✅ 26 shipped · 🪝 3 hook-ready · 🚧 4 decision-backed planned · 💭 5 proposed → **38 use cases total**
- Every ✅ row is demoable from the repo today; every 🚧 row already has its design argued in a decision record (per rule R2) — building any of them starts from a decision, not a blank page.
- Gaps most worth building next (by decision-backing): **B5 canary rollback** (sequence D3 fully specified) → **B3 L2 PR-gate flow** (DR004 + D04) → **E4 CI audit** (evidence exists, needs a workflow file).
