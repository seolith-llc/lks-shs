# 00 · Synthesis: One Framework for Self-Healing Software

**Inputs:** dossiers 01–04 (180 verified sources, all fetched 2026-11-09). **Output:** the unified taxonomy that names the loop, the layers, the autonomy ladder, and the two roles of AI — the intellectual core for the acronym decision (`docs/architecture/decisions/001-acronym.md`), the architecture (Phase 3), and the post series (Phase 4).

Citation shorthand: `D01[n]`, `D02[n]`, `D03[n]`, `D04[n]` = numbered references in the respective dossier files.

---

## 1. The universal healing loop

Four independently-gathered literatures converge on the same shape. The names differ; the stages do not.

| Tradition | Stage names | Source |
|---|---|---|
| IBM autonomic computing (2003) | **M**onitor – **A**nalyze – **P**lan – **E**xecute, over shared **K**nowledge (MAPE-K) | D01[2] |
| Self-healing decomposition | detect – diagnose – recover – (learn) | D01[2][3][30] |
| Industrial playbook | observe – decide – act – re-check | D02 (unifying table) |
| Chaos engineering | steady state – hypothesize – inject – compare | D02[13][14] |
| Canary/progressive delivery | measure – analyze – promote-or-rollback | D02[27][29][30] |
| Runtime verification | monitor property – violation – handler | D01[32] |
| LLM repair agents | localize – repair – validate | D01[24][25] |

**Canonical loop (5 stages), synthesized:**

```
SENSE ──▶ DIAGNOSE ──▶ REMEDIATE ──▶ VERIFY ──▶ LEARN
(signal)  (localize     (restart /     (did the    (postmortem,
           + root cause) rollback /     heal work?  harden, update
                        reroute /      chaos-       policy & models)
                        patch)         validated)
```

Three findings justify this exact decomposition:

1. **Localization is a distinct, hard stage.** The 2024 agent results show hierarchical/AST fault *localization* is where pipelines win (Agentless 32% Lite at $0.70/task; AutoCodeRover's AST search; D01[24][25]). Folding it into "diagnose" hides the hardest problem.
2. **Verification is the non-negotiable gate.** Every production system that ships AI fixes validates them with a *non-LLM* oracle first: GitHub re-runs CodeQL (D04[17]), Snyk re-runs SAST (D04[18]), Meta's TestGen-LLM filters through build+test (73% acceptance into production; D04[30]), SWE-bench requires FAIL_TO_PASS tests (D01[21]). The one documented autonomous-remediation failure — Anthropic's agent deleting ~200 workloads in 90 seconds — was an *authorized action executed without bounds*, not a hallucination (D04[31]). Axiom A6 ("a fix that isn't verified is a guess") is empirically load-bearing.
3. **Learning is the historically weakest stage** — absent in the fault-tolerance classics, RL experiments in the autonomic era (D01[3]), fine-tuning on repair traces today (RepairLLaMA, D01[20]), and incident-memory RAG in products (RCACopilot 0.766 RCA accuracy, D03[50]; Rootly/incident.io memory, D04[4][5]).

**The one-sentence thesis of the whole series** (from D02 §synthesis, confirmed by D01 §open-questions and D04 §builder-vs-healer):

> Self-healing was never invented — it was **layered**, over 70 years, from ECC memory to Kubernetes reconciliation. What AI changes is not the loop but the **decide stage**: for the first time, diagnosis and repair-synthesis can be *improvised at runtime* instead of *enumerated at design time*. The actuation layer was already solved; the intelligence is the new organ — and it must be transplanted inside the old loop's safety envelope (blast radius, verification gates, human approval), not bolted on outside it.

## 2. The layer stack

Every verified healing mechanism lives at exactly one layer, and the layers form a protection stack — each catches what the one below misses (D03 toolbox table; D02 pattern catalog).

| # | Layer | Senses (examples) | Decides | Acts (battle-tested actuators) |
|---|---|---|---|---|
| 1 | **Hardware** | ECC corrected/uncorrected errors, machine checks | EDAC classification, rasdaemon buckets | Correct in silicon; soft-offline failing pages (D03[13][14]) |
| 2 | **OS kernel** | oops, panics, lockups, syscall traces | panic policy, livepatch consistency model | Live patch (88% of kernel CVEs, ~0.7 ms; D03[2]); kdump+kexec reboot (D03[11]); OOM kill (D03[12]) |
| 3 | **Process / runtime** | exit signals, heartbeat gaps | supervision strategy, restart intensity | Restart with backoff (OTP, systemd, kubelet 10s→300s; D02[1][7][22]); hot code load (D02[1]) |
| 4 | **Service / network** | error & latency rates, saturation | circuit-breaker thresholds, adaptive limits | Fail fast + fallback; retry with budget (243× amplification without; D02[9][10]); shed load (D02[5][6][11]) |
| 5 | **Data / storage** | checksums, WAL CRCs, heartbeats | scrub policy, quorum rules | ZFS repair-in-place (D03[22]); WAL REDO replay (D03[26]); Raft re-election (D03[27][28]) |
| 6 | **Delivery pipeline** | canary KPI deltas, health checks | promote/rollback analysis | Auto-rollback (Argo/Flagger, D02[29][30]; Render "previous version keeps serving", D04[39]) |
| 7 | **Operations / org** | alerts, incidents, postmortems | triage + RCA (now: LLM agents) | Human with runbook; PR-gated AI fixes; bounded actuation (this is where AI enters — §3) |

**Rule of thumb for the architecture:** healing should always be attempted at the *lowest sufficient layer* (cheapest, fastest, most predictable), with higher layers as escalation — that is literally what Erlang supervision intensity and systemd start-limits encode (D02[1][7]). AIs enter at layer 7 today and must earn their way down.

## 3. The two roles of AI

Conflated in every vendor pitch; distinct in architecture, risk, and maturity (D04 §builder-vs-healer):

- **AI as builder** (before incidents): generates the healing machinery — fix PRs validated by CodeQL/SAST (D04[16][17][18]), test improvement (TestGen-LLM, D04[30]), self-updating runbooks (D04[3]), fuzz targets (+370k LOC covered, 26 CVEs incl. a ~20-year-old OpenSSL bug; D03[45][46]), syscall specs (KernelGPT, 11 CVEs; D03[49]). **Production-proven and cheap.**
- **AI as healer** (during incidents): autonomous *investigation* is shipping (Datadog Bits, incident.io Investigations, PagerDuty SRE Agent, Rootly AI — all 2025 products; D04[1]–[5]); autonomous *remediation* exists only as bounded, pre-authorized, reversible actions (rollbacks/restarts; D04[3][14]), with PR gates everywhere else (D04[4][10]) — and Rung 4 (closed loop) remains announced-but-unverified (D04[9]; negative results in D04 §"what we did not find").

**Verified verdict for the framework:** *AI-as-builder is production-proven; AI-as-healer is production-proven only in its observe/diagnose half, plus reversible actuation whose safety comes from the action class, not the model's correctness.*

## 4. The autonomy ladder

Five rungs, each observable in at least one shipped system or first-party postmortem (D04 rollout ladder):

| Rung | Name | What ships | Verified exemplar |
|---|---|---|---|
| L0 | **Observe** | reads telemetry, answers questions, zero writes | Bits Chat; Rootly MCP (D04[1][5]) |
| L1 | **Investigate** | auto-triage + evidence-cited RCA | Claude Tag 14-min SITREPs (D04[31]); Bits Investigation (D04[2]) |
| L2 | **Propose** | fix PRs gated by CI + human review + non-LLM validators | Agentic autofix + CodeQL re-run (D04[17]); Snyk SAST screen (D04[18]) |
| L3 | **Act (bounded)** | pre-authorized reversible actions, rate-capped, identity-scoped | Resolve rollbacks (D04[14]); Anthropic's admission-webhook caps (D04[31]) |
| L4 | **Close the loop** | unattended remediation with audit trail | *No verified production deployment yet* (D04[9], negative results) |

Advancement between rungs must be gated on measured MTTR deltas + audit findings — the discipline that Gartner's ">40% of agentic AI projects canceled by 2027" forecast implicitly prices in (D04[44]).

## 5. Numbers that anchor the series

Cross-dossier, all citation-backed in the dossiers:

| Number | Claim | Source |
|---|---|---|
| 1.96% → 87.6% | SWE-bench best/median resolution, 2023 → 2026 (median 76.2% across 48 models) | D01[21][29] |
| 68.3% | Share of original SWE-bench samples the Verified audit filtered out | D01[22] |
| $0.43–0.70 | Cost per task of structured repair pipelines (2024) | D01[24][25] |
| 88% / ~0.7 ms | Kernel CVEs live-patchable with no new code / interruption window | D03[2] |
| ~70% → 24% | Memory-safety share of vulns (Microsoft/Chromium norm → Android 2024, via Rust) | D03[30][31][33] |
| 53% / 12–91% | Getafix: Instagram null-bugs auto-patched / top-1 exact-fix accuracy range | D03[39][40] |
| 34% | Best agent solve rate on cloud infrastructure code (SWE-InfraBench, 2026) | D03[51] |
| 0.766 | RCACopilot RCA accuracy on a year of real Microsoft incidents | D03[50] |
| 73% | TestGen-LLM recommendations accepted into production | D04[30] |
| 243× | Worst-case load amplification from naive retries | D02[10] |
| ~7 months | Doubling period of agent task horizons (METR) | D04[28] |
| >$300K/hr | Downtime cost for 90%+ of firms (ITIC 2024); $400B/yr Global 2000 (Oxford/Splunk) | D04[41][43] |
| −7.2% | Delivery-stability change per +25% AI adoption (DORA 2024) — the hype discount | D04[46] |
| ~200 in 90 s | Workloads deleted by Anthropic's own agent — the cautionary tale for L3+ | D04[31] |
| nine nines | Erlang AXD301 claim, documented by Armstrong himself as from an undocumented slide | D02[1] |

## 6. Small business vs enterprise (one-glance)

| | Small business ($0–50/mo) | Enterprise |
|---|---|---|
| Realistic healing today | Uptime Kuma + dead-man's-switch + k3s restarts + platform auto-rollback + restic restore drills (D04 Tier 0–2) | Full stack + PR-gated AI fixes + bounded actuation (L2–L3) |
| Highest-value single control | Health-check-gated deploy with auto-rollback (D04[39]) | Non-LLM verification gate inside every AI fix pipeline (D04[17][18][30]) |
| Not yet attainable | Trustworthy autonomous RCA; safe autonomous remediation (D04 §small-biz gap) | Audited L4 closed loop; SOC2-style controls for agent actions (D04 negative results) |
| Binding constraint | Discipline (restore drills, runbook cards), not money | Governance & measurement (MTTR deltas, audit), not technology |

## 7. What the acronym must express (input to decision 001)

1. **The 5-stage loop** — sense/diagnose/remediate/verify/learn — ideally with fault-localization and verification visible.
2. **Layer-neutrality** — must name something true at every layer from kernel to org, not just "AI fixing code."
3. **Autonomy-graded trust** — the name should not overclaim L4.
4. **Lineage** — should honor MAPE-K/OTP heritage without cloning it (R3/R4).
5. **Four-altitude clarity** — must survive translation into ELI5, entry-level, professional, and C-suite registers (R10).
