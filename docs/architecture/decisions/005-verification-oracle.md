# Decision 005 — The Verification Oracle

**Status:** ACCEPTED · **Date:** 2026-11-09 · **Context:** axiom A6 — "a fix that isn't verified is a guess." What oracle decides that a heal succeeded? This decision defines the prototype's oracle and the general rule.

## Alternatives

1. **Process-alive check only** — `poll() is None` ⇒ healthy.
   *Trade-offs:* free and instant; but zombies and hung processes pass — it measures *existence*, not health (D03 open question 5: watchdogs detect hangs-not-wrongness; here even hangs are missed).
2. **Self-reported health endpoint only** — service says `"status": "HEALTHY"`.
   *Trade-offs:* richer (can expose gauges); but a broken service that still serves /health lies to you — the reporter and the reported are the same process (self-grading failure mode; D04 §risks).
3. **Heartbeat / dead man's switch only** — writer pings a file; stale ⇒ hung.
   *Trade-offs:* catches hangs the above miss (D02[7]; D04[35]); but a process can heartbeat happily while serving garbage — liveness ≠ correctness.
4. **Layered oracle: heartbeat + out-of-band golden request (+ in-band gauges)** — liveness (hb age < 3 s) **and** correctness (an *external* request must return the exact expected token `PULSE-OK`), with `/health` gauges for classification.
   *Trade-offs:* three signals to maintain; a few more lines of code; the oracle itself could fail (mitigated by keeping it in the supervisor — the component whose job is measuring, and which is itself simple enough to trust).
5. **Test-suite execution as oracle** — run the repo's tests after each heal.
   *Trade-offs:* the strongest semantic check (SWE-bench's FAIL_TO_PASS logic, D01[21]); far too slow for a sub-second runtime loop — it belongs at the L2 PR-gate, not the runtime gate.

## Decision

**(4) layered oracle.** Each signal catches a wound class the others miss: exit codes (crash), heartbeat staleness (hang), golden-request failure (errors/hang), gauge breach (leak). The general rule for the framework: **an oracle must be out-of-band relative to the thing it judges** (the supervisor asks, the service answers; the canary cohort answers to the stable cohort's baseline; the PR validates against tests the author didn't write). Option (5) is recorded as the L2-gate oracle, completing the ladder: runtime gate = layered probes; change gate = test suite.
