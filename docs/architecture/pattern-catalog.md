# Pattern Catalog — Self-Healing Software

**Status:** v1.0 (`#Step003`) · Organized by PULSE stage, then layer. Full pre-AI detail (24 patterns with limitations) lives in `docs/research/02-pre-ai-foundations.md` (pattern catalog table); this catalog adds the AI-era patterns and indexes everything to the loop stages. Citation shorthand: `D0n[m]` = dossier n, reference m.

## Patterns by PULSE stage

### Perceive (sensing)

| Pattern | Layer | Mechanism | Source |
|---|---|---|---|
| Dead-man's switch / heartbeat | every | writer pings; *absence* of pings is the signal | D02[7][8]; D04[35]; D03[9] |
| Health probes (liveness/readiness/startup) | container | exec/HTTP/TCP/gRPC checks with thresholds | D02[21] |
| Golden signals alerting | service | latency, traffic, errors, saturation | D02[31] |
| Checksum-on-read + scrub | storage | detect bit rot before it matters | D03[22] |
| eBPF sensing | kernel | safe, hot-loadable kernel tracing | D03[17][18][19] |
| Machine-check / EDAC reporting | hardware | classify CE/UE/deferred memory errors | D03[13][14][15] |
| Out-of-band synthetic probe | ops | black-box request from *outside* the system | D02[31]; prototype golden request |

### Understand (classification / RCA)

| Pattern | Layer | Mechanism | Source |
|---|---|---|---|
| Threshold/state classification | every | hand-written decision policy (the pre-AI default) | D02 (unifying table) |
| Event correlation / alert compression | ops | cluster alert storms into one incident | D02[40][41] |
| Causal-AI root cause | ops | root cause on a live dependency map | D02[40] |
| LLM investigator with evidence citations | ops | autonomous triage + ranked hypotheses | D04[2][4]; D03[50] |
| Challenger agent | ops | second agent attacks the first's hypothesis | D04[4][5] |
| Confidence set by code, not model | ops | deterministic confidence from evidence coverage | D04[5] |

### Localize (fault localization)

| Pattern | Layer | Mechanism | Source |
|---|---|---|---|
| Layer/owner routing | every | map fault class → component + layer | prototype `LOCALIZATION` |
| Spectrum-based fault localization | code | rank lines by test-pass/fail correlation | D01[25] |
| Hierarchical repo search | code | coarse→fine localization pipeline | D01[24] |
| AST-aware context retrieval | code | search by structure, not text | D01[25] |
| Deploy-delta localization | delivery | "what changed" as first hypothesis | D02 §5; D3 diagram |

### Solve (remediation portfolio — ordered by cost/reversibility)

| Pattern | Action class | Reversibility | Blast radius | Source |
|---|---|---|---|---|
| Wait (transient faults pass) | none | n/a | none | D02[10] |
| Retry w/ capped backoff + jitter + budget | retry | yes | can amplify 243× if naive | D02[9][10] |
| Fail fast + fallback | degrade | yes | contained | D02[5][6] |
| Circuit breaker | isolate | yes | one dependency | D02[5][6][7][8] |
| Shed load / adaptive concurrency | protect | yes | self | D02[11] |
| Restart w/ backoff + intensity limit | reset state | yes | one process | D02[1][22] |
| Re-elect leader / resync replica | re-coordinate | yes | cluster | D03[27][28] |
| Replay WAL / repair from redundancy | restore state | yes | data extent | D03[22][26] |
| Rollback deployment / flag kill switch | remove change | yes | cohort→all | D02[26][27][28][29][30] |
| Live-patch / hot code load | fix in place | partial | process/kernel | D03[1][2][3]; D02[1] |
| PR-gated AI fix | fix the code | via review | repo | D04[4][17][18] |
| Escalate to human | bounded surrender | n/a | none (by design) | D02[1]; D5 diagram |

### Evolve (verification, learning)

| Pattern | Mechanism | Source |
|---|---|---|
| Non-LLM validation gate | tests / SAST / CodeQL / steady-state metrics must pass before "healed" | D04[17][18][30]; axiom A6 |
| Chaos validation | inject the failure deliberately; the heal must survive it | D02[13][14][15] |
| Healing event log (MTTR + triage) | every heal is a measured, reviewable artifact | prototype `healing-log.jsonl` |
| Human-validated postmortem memory | only reviewed RCAs enter the retrieval store | D03[50]; D04 §risks |
| Self-updating runbooks | incident learnings become the next automation | D04[3] |
| Fine-tuning on repair traces | model-level learning from accepted fixes | D01[20] |
| Prevention as learning (Rust/fuzzing) | remove the fault class from future code | D03[30][31][33][37][38] |

## Cross-cutting governance patterns

| Pattern | Mechanism | Source |
|---|---|---|
| Autonomy ladder w/ evidence gates | advance L0→L4 only on measured MTTR + audit findings | D04 rollout ladder |
| Blast-radius caps in infrastructure | admission webhooks, rate caps, replenishing budgets, undo tests | D04[31] |
| Read-only default | agents earn write access | D04[12] |
| Agent identity as audit principal | agent actions on the same immutable trail as humans | D04[22]; D04 §governance |
| Asymmetric permissions | delete/revoke paths are human-only | D04[31] |
| Layered escalation w/ MaxR/MaxT | refuse to thrash; page instead | D02[1] |

## Anti-patterns (documented failures — cite them when reviewing designs)

| Anti-pattern | Consequence | Source |
|---|---|---|
| Naive retry (no cap/jitter/budget) | 243× amplification on a failing dependency | D02[10] |
| Unbounded restart (no intensity limit) | cascading restarts; crash-loop storms | D02[1] |
| Self-reported health as the only oracle | zombies pass; hangs invisible to liveness checks | Decision 005; D03 §open questions |
| Agent validates its own fix with itself | feedback loops, drifting "fixes" | D04 §risks |
| Autonomous actuation on novel actions | Anthropic's 200-workloads-in-90s deletion | D04[31] |
| Acting on correlation | KV-cache fault "treated" as capacity problem | D04[32] |
| Unreviewed AI postmortems | contaminated incident memory poisons future RCAs | D04 §risks |
| Buying autonomy before audit trails | the procurement anti-pattern | D04 §risks |
