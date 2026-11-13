---
step: "#Step009 — use-case catalog, state/workflow model, interactive HTML"
turn: 13
timestamp: 2026-11-13 08:29 EST
---

# Request

do all three in order: (1) the complete use-case list grounded in the actual shipped code + planned features, (2) the state/workflow model, (3) a single self-contained animated HTML page. Writing the use-case catalog first.

# Response

**All three delivered in order** (2026-11-13):

**(1) Use-case catalog** — `docs/architecture/use-case-catalog.md`: 38 use cases across 5 groups (A healing loop, B pluggable intelligence, C failure modes, D media/publishing toolchain, E verification). Status taxonomy: 26 ✅ SHIPPED / 3 🪝 HOOK-READY / 4 🚧 PLANNED / 5 💭 PROPOSED. Every ✅ row cites the implementing function+file (anchors grep-verified against source this turn). Named next-builds: canary rollback (B5, fully specified by D3), L2 PR-gate (B3, DR004+D04), CI audit (E4).

**(2) State/workflow model** — `docs/architecture/state-workflow-model.md`: two coupled state machines (patient: STARTING/HEALTHY/DEGRADED/FAULTED_{CRASHED,HUNG,LEAKING,ERRORING}; healer: PERCEIVING/SOLVING/RESTARTING/VERIFYING/HEALED/ESCALATED/FAILED) as mermaid stateDiagrams + tables with code anchors; the four stateful subtleties (restart-window-as-escalation-state, evidence-before-threshold windows, stale-heartbeat false-positives, escalation-is-a-heal); the full CONFIG timing model; the healing-log.jsonl event schema; workflow↔use-case↔page map.

**(3) Interactive page** — `docs/animations/pulse-interactive.html`, one self-contained file (no deps, no network): animated PULSE ring + traveling signal, wound buttons (crash/hang/leak/errors + clear + crashloop drill), patient meters (heartbeat/ballast/error-rate), supervisor panel (state, restart meter vs MaxR, backoff, MTTR, heals/escalations), live state-machine diagram, escalation ladder, streaming healing log formatted like the real demo, ×1/×4 speed.

**Verification (in-browser, via local HTTP server + browser automation):**
- Functional sweep: hang→classified HUNG→restart→gate→HEALED; leak→heal; errors→heal; crashloop→recurring crash→**ESCALATED**→banner→reset→heal.
- **4 real bugs found & fixed during testing:** (a) hidden-tab timer throttling froze the clock → catch-up virtual clock (delta-based, capped so it slows gracefully instead of teleporting); (b) instant simulated probes let ERRORING beat HUNG in a hang (real probes block on their 2 s timeout) → probe-completion gating; (c) classification transition-guard blocked re-detection after heal → gate success re-arms to HEALTHY; (d) crashloop drill fired once and healed → deterministic fault now recurs after every heal.
- Visual acceptance: round 1 failed (viewport-truncated capture), round 2 failed (broken full-page stitch in the in-app browser), round 3 **PASS** on a tall-viewport single frame (evidence committed as `pulse-interactive-evidence.png`).

**Wired in:** series overview "Try it live" section; README layout + Phase 9; master-checklist Phase 9 ✓ + verification log. Committed & pushed (repo public).

# Decisions

None from user beyond the three-item order (followed).

# Artifacts

- Created: use-case-catalog.md, state-workflow-model.md, pulse-interactive.html, evidence PNG, this file
- Updated: 00-series-overview.md, README.md, master-checklist.md, INDEX.md
