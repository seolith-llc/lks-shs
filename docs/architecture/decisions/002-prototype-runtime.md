# Decision 002 — Prototype Service Runtime

**Status:** ACCEPTED · **Date:** 2026-11-09 · **Context:** the application-track prototype needs a woundable web service (`prototypes/pulse-app/service.py`). The demo's subject is the *healing loop*, not the web stack.

## Alternatives

1. **Python stdlib `http.server`** — zero dependencies, one command, fully readable in one file; runs on the Python 3.14 already on the machine.
   *Trade-offs:* not a "real" web framework — nobody ships `http.server` to production; single-file simplicity caps realism (no middleware, DB, etc.).
2. **Python + FastAPI/Flask + uvicorn** — realistic framework, middleware, typing; familiar to the target audience.
   *Trade-offs:* requires `pip install` (breaks the one-command rule R5), dependency drift over the repo's lifetime, and framework ceremony hides the loop logic the demo exists to show.
3. **Node/Express** — equally realistic; async model matches modern services.
   *Trade-offs:* npm install + lockfile; the supervisor (which must be a *separate process*, Decision 003) would need a second runtime or a process manager, complicating the story.
4. **Go (net/http)** — single static binary, born-for-supervision stdlib (exec, signals), great systems flavor.
   *Trade-offs:* compile step; more boilerplate per feature; slower to iterate for a documentation-heavy project.
5. **Rust (axum)** — maximum memory-safety narrative tie-in (D03[30]–[34]).
   *Trade-offs:* heaviest iteration cost; the compile loop fights the "wound it, watch it heal" demo rhythm; overkill when the `leak` fault *deliberately* simulates the memory bug Rust prevents (the point is the healing, not the prevention).

## Decision

**Python stdlib.** R5 (one command, no install) dominates: the demo must run for a reader in thirty seconds. The "not production-realistic" objection is answered in the README — the *service* is intentionally boring; the *loop* is the product. If a second, framework-realistic prototype is ever added (systems track or L2 PR-gate demo), Decision 002 gets revisited for that prototype only.
