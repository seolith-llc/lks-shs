# Sequence Diagrams — the PULSE Framework

**Status:** v1.0 (`#Step003`) · All diagrams mermaid (GitHub-renderable, rule R3). Abstraction level noted per diagram; sources are dossier citations.

---

## D1 · Baseline heal: crash → supervised restart (L0, no AI)

**Level:** single host, process/runtime layer (L3). **Source of truth:** `prototypes/pulse-app/supervisor.py`. **Lineage:** OTP supervision (D02[1]), systemd `Restart=` (D02[7]), kubelet probes (D02[21][22]).

```mermaid
sequenceDiagram
    autonumber
    participant W as Wound (demo)
    participant S as Service (patient)
    participant SUP as Supervisor (healer)
    participant HB as Heartbeat file

    S->>HB: write ts every 0.5s (dead man's switch)
    SUP->>S: golden request GET / (expects PULSE-OK)
    Note over SUP: Perceive: process alive? hb age? golden ok?

    W->>S: POST /inject/crash
    S-->>S: exit(137)
    SUP->>S: poll → not alive, exit=137
    Note over SUP: Understand: CRASHED<br/>Localize: service process (L3)
    SUP->>S: kill (idempotent) + restart after backoff
    Note over SUP: Solve: RESTART #1 (1s→2s→4s→8s capped,<br/>crash-loop damping, D02[22])
    S->>HB: fresh heartbeats resume
    SUP->>S: golden request → PULSE-OK
    Note over SUP: Evolve: verification gate PASSED<br/>log event + MTTR + triage
```

**Why this shape:** the supervisor *outlives* the supervised (Decision 003); the oracle is layered — liveness (heartbeat) **and** correctness (golden request) — because a hung-but-alive process or a zombie that answers nothing are different wounds (Decision 005).

---

## D2 · Hang → dead-man's-switch heal (liveness ≠ aliveness)

**Level:** process layer. **Source of truth:** `service.py` hang fault. **Lineage:** `sd_notify("WATCHDOG=1")` (D02[7][8]), Healthchecks.io (D04[35]), hardware watchdog `/dev/watchdog` (D03[9][10]).

```mermaid
sequenceDiagram
    autonumber
    participant S as Service
    participant HB as Heartbeat file
    participant SUP as Supervisor

    Note over S,HB: healthy: hb age always &lt; 3s
    S->>S: inject hang → heartbeat thread stops,<br/>handlers sleep 60s
    SUP->>HB: read ts → age grows 3s, 3.5s, 4s…
    SUP->>S: golden request → timeout (2s)
    Note over SUP: Perceive: alive=true BUT hb stale + golden dead<br/>Understand: HUNG (not crashed — no exit)<br/>Localize: event loop / heartbeat thread
    SUP->>S: SIGTERM → (1.5s) → SIGKILL → restart
    Note over SUP: Solve→Evolve: same gate as D1
```

**Why this matters:** process-liveness-only monitoring calls this HEALTHY. The dead man's switch is the cheapest oracle that catches it — and it is the *same pattern* at every scale, from systemd services to cron jobs to Raft leader election (D03[28]).

---

## D3 · Deployment regression → canary auto-rollback (Solve = routing, not repair)

**Level:** delivery pipeline (L6). **Lineage:** canary + metric analysis (D02[27]), Argo Rollouts / Flagger (D02[29][30]), Render health-check-gated deploys (D04[39]) — the highest-value self-healing a small business can buy.

```mermaid
sequenceDiagram
    autonumber
    participant CD as Deploy controller
    participant C as Canary cohort (1%)
    participant ST as Stable cohort (99%)
    participant M as Metrics (golden signals)

    CD->>C: deploy vNext behind traffic split
    loop every analysis window
        CD->>M: query error rate / latency for canary vs stable
        M-->>CD: canary error rate 12% vs stable 0.1%
    end
    Note over CD: Understand: regression on cohort<br/>Localize: the deployment (the delta IS the cause)
    CD->>ST: route 100% traffic back to stable
    CD->>C: tear down canary
    Note over CD: Solve: ROLLBACK (reversible, instant)<br/>Evolve: verify golden signals recovered → block vNext,<br/>open postmortem item (the code fix is L2's job)
```

**Why rollback before diagnosis:** when the *change* is the failure class (the dominant one — most outages are caused by change, D02 §5), removing the change is faster and safer than diagnosing it. Diagnosis continues offline at L7.

---

## D4 · AI triage → human-gated fix (L1 → L2, the verified 2025–26 pattern)

**Level:** operations (L7). **Lineage:** incident.io Investigations (D04[4]), Bits Investigation (D04[2]), Claude Tag first responder (D04[31]), agentic autofix + CodeQL re-run (D04[17]), Snyk SAST screen (D04[18]).

```mermaid
sequenceDiagram
    autonumber
    participant A as Alert
    participant AG as AI investigator (L1)
    participant EV as Evidence (logs, deploys, metrics)
    participant CH as Challenger agent
    participant CI as Validators (non-LLM)
    participant H as Human on-call
    participant CD as Progressive rollout

    A->>AG: page: checkout latency p99 spike
    AG->>EV: collect: recent deploys, error logs, dependency health
    AG->>AG: hypotheses ranked w/ confidence
    CH->>AG: attack weakest hypothesis (correlation ≠ causation, D04[32])
    AG-->>H: RCA: "deploy a3f9 introduced N+1 in cart service" (0.86)
    AG->>AG: draft fix PR
    AG->>CI: run tests + SAST/CodeQL on the fix
    CI-->>H: validators PASS, PR ready for review
    H->>H: review + merge (the L2 gate — AI never merges)
    H->>CD: canary the fix (D3)
    CD-->>AG: steady state restored
    Note over AG: Evolve: append human-validated postmortem to<br/>incident memory (RCACopilot pattern, D03[50])
```

**Why the gates:** this is exactly where the industry frontier stops — autonomous investigation and drafting are shipping; the merge and any production actuation stay behind human + non-LLM gates (D04 §governance; OWASP LLM06 D04[47]).

---

## D5 · Restart storm → escalation to human (the healer heals itself by refusing)

**Level:** runtime layer, policy stratum. **Source of truth:** `supervisor.py` crashloop scenario (PASS). **Lineage:** OTP MaxR/MaxT (D02[1][2]); "cascading restarts do not work" (Wiger, D02[1]); axiom A3.

```mermaid
sequenceDiagram
    autonumber
    participant S as Service
    participant SUP as Supervisor
    participant H as Human

    loop crash #1..#3 within 30s window
        S->>S: crash (deterministic fault)
        SUP->>S: RESTART #n, backoff 1s→2s→4s
        Note over SUP: each heal "works" — and fails again
    end
    S->>S: crash #4
    Note over SUP: Solve: intensity 3 ≥ MaxR in MaxT<br/>restart cannot be the cure for a deterministic fault
    SUP-->>H: ESCALATE — page a human, stop rescheduling
    Note over SUP,H: Evolve (human half): root-cause fix via L2,<br/>then the loop resumes at L0
```

**Why escalation is a heal:** unbounded retry converts a fault into an outage *plus* load storm (243× amplification math, D02[10]). Refusing to thrash — and paging — is the bounded healer's correct terminal action; it is also where the AI era's L2 loop (D4) picks the work up.

---

## D6 · Layered escalation — the full ladder in one picture

**Level:** whole system. **Summary of D1–D5 plus the research corpus:**

```mermaid
flowchart LR
    F["fault occurs"] --> A["L1-L2 heal attempt<br/>hardware/kernel (µs–s, dumb, certain)"]
    A -->|healed| V1["verify: steady state"]
    A -->|persists| B["L3-L4 heal attempt<br/>restart/rollback (s–min, scripted)"]
    B -->|healed| V2["verify: golden signals"]
    B -->|repeat ≥ MaxR| C["L6-L7 heal attempt<br/>rollback + AI diagnosis (min, smart)"]
    C -->|fix PR merged| D["progressive rollout + verify"]
    C -->|novel/ambiguous| HUMAN["human decides<br/>(the L2 gate is always available)"]
    D --> E["Evolve: postmortem,<br/>harden, update policy &amp; memory"]
    V1 --> E
    V2 --> E
    E --> F
```
