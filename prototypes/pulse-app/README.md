# PULSE Application-Track Prototype

A deliberately woundable web service + an external supervisor that heals it — a runnable demonstration of every PULSE stage and of the discipline rules from the research corpus. **Stdlib only, one command** (rule R5):

```bash
./demo.sh            # runs all 5 scenarios, prints the healing timeline, exits 0 on ALL PASS
python3 supervisor.py --demo hang   # single scenario: crash | hang | leak | errors | crashloop
```

Verified evidence: [`demo-evidence.log`](demo-evidence.log) (run of 2026-11-09, all scenarios PASS, exit 0).

## What each scenario demonstrates

| Scenario | Wound | Detection (P·U) | Heal (S) | Teaching point |
|---|---|---|---|---|
| `crash` | process exits 137 | liveness poll | restart w/ backoff | the classic supervised-restart loop (OTP, systemd, kubelet; D02[1][7][22]) |
| `hang` | heartbeat stops, handlers stall | **dead-man's-switch** heartbeat age > 3s | SIGTERM→restart | liveness ≠ aliveness — the same signal as `sd_notify WATCHDOG` (D02[7]) and Healthchecks.io (D04[35]) |
| `leak` | each request grows an 8 MB ballast | self-reported memory gauge crosses 40 MB | restart + **"mitigated, not cured"** note | restart ≠ repair; the code fix still needs an L2 human-gated PR (D02 gap analysis) |
| `errors` | 50% of requests 500 | rolling golden-probe error rate ≥ 50% (6-window) | restart | error-budget breach as trigger — canary analysis in miniature (D02[29][30]) |
| `crashloop` | crash ×4 in <30s | each crash | **ESCALATE** after MaxR=3/MaxT=30s | the healer refuses to thrash — OTP restart-intensity pattern (D02[1][2]); axiom A3 |

## PULSE stage → code map

| Stage | Where | What it does |
|---|---|---|
| **P**erceive | `supervisor.py: perceive()` + `service.py: heartbeat_loop()` | layered oracle (Decision 005): heartbeat file (dead man's switch) + `/health` gauge + out-of-band golden request `GET /` |
| **U**nderstand | `supervisor.py: understand()` | classify: CRASHED / HUNG / LEAKING / ERRORING / HEALTHY |
| **L**ocalize | `supervisor.py: LOCALIZATION` | name component + stack layer (runtime L3 / application / delivery L6) |
| **S**olve | `supervisor.py: solve()` | restart with capped exponential backoff (1→2→4→8s, kubelet-style D02[22]) **or** escalate on restart intensity |
| **E**volve | `supervisor.py: verify()` + `_event()` | verification gate (fresh heartbeat **and** golden `PULSE-OK`), MTTR measurement, triage report attached, event appended to `healing-log.jsonl` |

The **Solve→Evolve boundary is the verification gate** (Decision 001): nothing is logged as healed until a non-AI oracle confirms it.

## AI integration (Decision 004)

`triage.py` is a deterministic L1 investigator (ranked hypotheses + confidence + the human-gate note) — the *shape* of an LLM RCA agent (RCACopilot D03[50]; challenger agents D04[4][5]) without network or API-key dependence. To plug a real LLM in:

```bash
export PULSE_TRIAGE_CMD='python3 my_llm_triage.py'   # reads {fault_class, summary} JSON on stdin
./demo.sh
```

Code-level fixes are deliberately **not** automated: the prototype stops where the verified industry frontier stops (L2 — human-reviewed PR; D04 §builder-vs-healer).

## Design decisions

- [002](../../docs/architecture/decisions/002-prototype-runtime.md) — service runtime: Python stdlib
- [003](../../docs/architecture/decisions/003-supervisor-model.md) — external supervisor process (not in-process)
- [004](../../docs/architecture/decisions/004-ai-triage.md) — deterministic L1 investigator, pluggable LLM hook
- [005](../../docs/architecture/decisions/005-verification-oracle.md) — layered oracle: heartbeat + golden request

## Files

- `service.py` — the patient (woundable HTTP service, stdlib)
- `supervisor.py` — the healer (PULSE loop, escalation policy, event log)
- `triage.py` — L1 investigator (deterministic stand-in)
- `demo.sh` — one-command demo
- `demo-evidence.log` — verified run output
