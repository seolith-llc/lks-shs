# Part 5 · PULSE in ~600 Lines of Python

*Series: [Overview](00-series-overview.md) · [Part 4](04-the-pulse-framework.md) · **Part 5** · [Part 6](06-the-small-business-playbook.md)*
**Audience:** builders · ~8 min · Video companion: `docs/video/05-prototype-demo.mp4` *(renders in Phase 5)*

> Reading about healing loops is like reading about swimming. Here's water: **clone the repo and run `./demo.sh`** — you get a service you can crash, hang, leak, and enrage, and a supervisor that heals it while narrating every PULSE stage. Stdlib only. Verified: 5/5 scenarios PASS. [Code](../../prototypes/pulse-app/) · [Evidence log](../../prototypes/pulse-app/demo-evidence.log)

## The two actors

**The patient** (`service.py`, ~130 lines): an HTTP service that writes a **heartbeat file** every 0.5 s (dead man's switch — the same pattern as `sd_notify WATCHDOG` and Healthchecks.io), serves `/health` with self-reported gauges, answers `GET /` with the golden token `PULSE-OK`, and accepts four wounds on demand: `crash` (exit 137), `hang` (heartbeat stops + handlers stall), `leak` (each request grows an 8 MB ballast), `errors` (50% of requests 500).

**The healer** (`supervisor.py`, ~250 lines): an *external* supervisor — OTP/systemd/kubelet in miniature — running the loop every 0.3 s:

| Stage | Code | What it actually does |
|---|---|---|
| **P**erceive | `perceive()` | layered oracle (Decision 005): heartbeat age + `/health` gauge + out-of-band golden request |
| **U**nderstand | `understand()` | classify: CRASHED / HUNG / LEAKING / ERRORING |
| **L**ocalize | `LOCALIZATION` | component + layer, e.g. "event loop / heartbeat thread (runtime L3)" |
| **S**olve | `solve()` | kill + restart with 1→2→4→8 s backoff, **or ESCALATE** when 3 restarts land inside 30 s (OTP MaxR/MaxT) |
| **E**volve | `verify()` + `_event()` | verification gate (fresh heartbeat **and** golden `PULSE-OK`), MTTR, triage report, JSONL event log |

`triage.py` is the L1 investigator: deterministic ranked hypotheses + confidence + the human-gate note (the *shape* of an LLM RCA agent, pluggable via `PULSE_TRIAGE_CMD` — see [Decision 004](../architecture/decisions/004-ai-triage.md) for why the demo doesn't call a live model).

## Watch it heal (from the committed evidence log)

```
--- scenario: hang -----------------------------------
[+0.31s] service HEALTHY (fresh heartbeat + golden PULSE-OK) — injecting fault
[+6.93s] PULSE P: alive=True exit=None hb_age=4.87 golden=False
[+6.93s] PULSE U: classified HUNG | PULSE L: event loop / heartbeat thread (runtime layer L3)
[+6.93s] PULSE S: kill + RESTART #1 (backoff 1.0s, capped at 8s — kubelet-style crash-loop damping)
[+8.25s] PULSE E: verification gate → HEALED (heartbeat age 0.26s, golden=PULSE-OK) mttr=7934ms

--- scenario: crashloop ------------------------------
[...crash #1..#3: each healed by restart, backoff 1s→2s→4s...]
[+8.94s] PULSE U: classified CRASHED (crash 4)
[+8.94s] PULSE S: ESCALATE — restart intensity 3 in 30s exceeds MaxR=3 (OTP MaxR/MaxT pattern).
                   Human required. Halting rescheduling.
[+8.94s] outcome: PASS (restart storm bounded by design — the healer refuses to thrash)
```

**Every scenario teaches a finding from the research corpus:**

| Scenario | The lesson it embodies |
|---|---|
| crash | the classic supervised restart (OTP, systemd, kubelet) — actuation solved decades ago |
| hang | **liveness ≠ aliveness** — a process-alive check calls this HEALTHY; only the dead man's switch catches it |
| leak | **restart ≠ repair** — the demo literally logs *"mitigated, not cured — the code fix still needs an L2 human-reviewed PR"* |
| errors | error-budget breach as trigger — canary analysis in miniature |
| crashloop | **the healer must not harm** — bounded intensity, escalate instead of thrash (the 243×-amplification lesson, dramatized) |

## Why it's built this way (the trade-offs)

Every choice has a decision record with 3–5 alternatives:

- **Python stdlib, zero install** — the demo's subject is the loop, not the web stack; one command or nothing (Decision [002](../architecture/decisions/002-prototype-runtime.md))
- **External supervisor process** — the healer must outlive the patient; also the only way MaxR/MaxT escalation is expressible (Decision [003](../architecture/decisions/003-supervisor-model.md))
- **Deterministic triage** — reproducible evidence beats a flaky API call; the LLM hook is one env var away (Decision [004](../architecture/decisions/004-ai-triage.md))
- **Layered oracle** — heartbeat catches hangs, golden request catches wrongness; self-reported health alone would let the patient grade its own exam (Decision [005](../architecture/decisions/005-verification-oracle.md))

## Run it

```bash
cd prototypes/pulse-app
./demo.sh                     # all five scenarios; exit 0 on ALL PASS
python3 supervisor.py --demo hang   # one scenario, watch the loop tick
```

Then read `supervisor.py` top to bottom — it is deliberately the shortest complete implementation of this series' claims: **every wound class, every oracle, every gate, in one file you can hold in your head.**

**Next:** [Part 6 — the small-business playbook: real self-healing for $0–50/month →](06-the-small-business-playbook.md)
