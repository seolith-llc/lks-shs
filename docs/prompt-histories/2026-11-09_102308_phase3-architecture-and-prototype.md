---
step: "#Step003 — architecture & prototypes"
turn: 4
timestamp: 2026-11-09 10:23 EST
---

# Request

continue

# Response

**Phase 3 executed end to end** — architecture deliverables + working prototype:

**1. Application-track prototype (`prototypes/pulse-app/`, stdlib-only, one command):**
- `service.py` — woundable HTTP service: heartbeat dead-man's-switch, `/health` gauges, golden request `GET /` → `PULSE-OK`, four injectable faults (crash / hang / leak / errors)
- `supervisor.py` — external supervisor (OTP/systemd/kubelet in miniature): PULSE loop every 0.3s — perceive (layered oracle), understand (classify CRASHED/HUNG/LEAKING/ERRORING), localize (component+layer), solve (restart w/ 1→2→4→8s backoff, MaxR=3/30s → ESCALATE), evolve (verification gate, MTTR, triage, healing-log.jsonl)
- `triage.py` — deterministic L1 investigator (ranked hypotheses + confidence + human-gate note), pluggable via `PULSE_TRIAGE_CMD`
- **Demo verified: 5/5 scenarios PASS, exit 0** (`demo-evidence.log` committed). Two bugs found & fixed during build: line-continuation syntax error; errors-fault rate raised 20%→50% so the 50% error-rate threshold can actually fire; crashloop stale-window misclassification fixed.
- MTTRs: crash 1.6s · hang 7.9s · leak 3.2s · errors 2.9s · crashloop → escalation

**2. Architecture docs:**
- `docs/architecture/reference-architecture.md` — mermaid stack diagram (7 layers + PULSE loop + verification gate), component model (8 components w/ verified exemplars), L0–L4 ladder as architecture, small-biz/enterprise instantiations, 7 binding rules
- `docs/architecture/sequence-diagrams.md` — 6 mermaid diagrams: D1 crash→restart, D2 hang→dead-man's-switch, D3 canary auto-rollback, D4 AI triage→human-gated PR, D5 restart-storm→escalation, D6 full escalation ladder
- `docs/architecture/pattern-catalog.md` — patterns indexed by PULSE stage + governance patterns + 8 documented anti-patterns

**3. Decision records 002–005** (each 3–5 alternatives + trade-offs): 002 runtime=Python stdlib; 003 supervisor=external process; 004 AI triage=deterministic L1 + pluggable hook; 005 oracle=layered (heartbeat+golden request), test-suite as the L2 gate.

**Tracking updated:** master-checklist Phase 3 all ✓ + verification log; root README status; this history + INDEX.

# Decisions

None from user (continued per standing "proceed"/"continue"). PULSE remains provisional (Decision 001).

# Artifacts

- Created: 4 prototype files + README + evidence log; 3 architecture docs; 4 decision records; this file
- Updated: master-checklist, root README, INDEX
- Next: Phase 4 post series (diagrams/animations/attribution built on the above)
