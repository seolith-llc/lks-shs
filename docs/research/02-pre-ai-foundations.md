# 02 · Self-Healing Before AI: The Industrial Playbook

> **Scope note.** Dossier #02 of the lks-shs research corpus (#Step001). This dossier covers how industry built *self-healing* — automatic detection of, and recovery from, failure — **before the LLM era (roughly 1985–2022)**. "Healing" here means any closed loop that observes a system, decides something is wrong, and acts to restore service *without a human in the loop at decision time*: restart, rollback, reroute, repair, or fail over. LLM-driven healing is deliberately out of scope (covered by later dossiers); it enters this document only at the end, as the answer to the gaps of the pre-AI playbook. All URLs were fetched and verified on 2026-11-09. Anything not directly verifiable is tagged **[UNVERIFIED]**.

## TL;DR

- **Self-healing is not new and not AI.** For four decades industry has run observe→decide→act loops at every layer: process (Erlang supervision), host (systemd), cluster (Kubernetes reconciliation), network (circuit breakers), storage (ZFS), data (WAL replay), and delivery pipeline (canary auto-rollback).
- **Erlang/OTP (2003) is the founding document.** Armstrong's thesis formalized "let it crash," supervision trees, `heart` heartbeats, and hot code loading — and candidly reports that the famous AXD301 "nine nines" (99.9999999%) figure came from a PowerPoint slide whose methodology "was not documented" [1].
- **Resilience patterns are the runtime immune system.** Nygard's *Release It!* (2007/2018) named circuit breaker, bulkhead, timeout, fail-fast; Netflix Hystrix industrialized them, then went into maintenance mode in favor of adaptive concurrency limits and Resilience4j — because static thresholds are brittle [5][6][7][11].
- **Naive retries are dangerous by default.** Retries are "selfish"; a 5-layer call stack with 3 retries each can multiply load on a failing dependency by 243×; hence capped backoff, jitter, and token-bucket retry budgets [9][10].
- **Chaos engineering turned healing from a promise into a tested property.** Netflix's Simian Army (2011) randomly kills production instances; Basiri et al. (IEEE Software 2016) codified the discipline: define steady state, hypothesize, inject real-world failure, try to disprove [12][13][14].
- **Kubernetes is the largest deployed self-healing machine.** Its own docs: "Kubernetes restarts containers that fail… kills containers that don't respond to your user-defined health check"; desired-state reconciliation descends directly from Google Borg (EuroSys 2015) [19][20][21][22].
- **Progressive delivery heals by routing, not repairing.** Blue-green, canary, and feature-flag kill switches remove bad code from the request path in minutes; Argo Rollouts and Flagger automate the observe-metrics-then-promote-or-rollback loop [26][27][28][29][30].
- **Pre-LLM AIOps was correlation, not cognition.** Moogsoft/Dell, Dynatrace's causal-AI Davis, and PagerDuty-class tools compress alert storms and pin root causes — but propose no code-level action [40][41].
- **The closest pre-LLM thing to AI *repair* was at Meta:** Getafix (OOPSLA 2019) learned fix patterns from history and suggested static-analysis fixes; SapFix (2018) generated, tested, and proposed end-to-end patches for crashes — with a human always approving [38][39].
- **Below the app, healing never needed intelligence at all:** ZFS checksums and repairs bad blocks from redundancy, PostgreSQL replays WAL after crash, Raft/etcd re-elects leaders, watchdog timers reboot hung systems [42][43][44][45][46].
- **Why AI enters:** the pre-AI loops restart, reroute, and roll back — they do not *understand*. Recovery beyond a policy, reading a novel stack trace, writing the fix, and triaging alert fatigue all stopped at a human. That boundary is exactly where LLMs are now applied.

## The core idea: healing loops exist everywhere already

Every pre-AI self-healing mechanism is the same shape: **observe** a signal, **decide** via a policy (usually a threshold, timer, or state machine), **act** via a privileged mechanism (restart, reroute, replay, re-elect), and **feed the result back** (the loop re-checks). The only variables are the layer, the signal, and whether the policy was written by a human once (code) or is statistical (pre-LLM ML).

| System | Observe | Decide | Act | Feedback / re-check |
|---|---|---|---|---|
| Erlang/OTP supervision tree | Links/monitors deliver `{'EXIT', Pid, Why}` to supervisor | Restart strategy (`one_for_one`, `one_for_all`, `rest_for_one`) + restart intensity | Restart worker from child spec; escalate to parent on intensity breach | Supervisor re-monitors restarted child [1][2] |
| Erlang `heart` | External port program expects heartbeat (default 60 s) | Heartbeat timeout | Execute `HEART_COMMAND` (reboot / start replacement node) | New node comes up under supervision [3] |
| Kubernetes kubelet | Liveness/readiness/startup probes (exec, HTTP, TCP, gRPC) | Probe thresholds × `periodSeconds`; `restartPolicy` | Kill & restart container; backoff 10 s→300 s; don't advertise non-ready pods | Next probe cycle; controller managers re-reconcile [20][21][22] |
| Kubernetes controllers / Operators | Watch current state of pods/CRDs vs declared desired state | Declarative diff (level-triggered reconciliation) | Create/replace/reschedule objects; app-specific ops (backup, failover) | Continuous watch loop drives convergence [19][23] |
| Circuit breaker (Hystrix, Resilience4j, Polly) | Rolling error/latency counts per dependency | Threshold opens breaker for a sleep window | Fail fast; serve fallback; half-open trial probes | Metrics feed re-closes or re-opens breaker [5][6][7][8] |
| Chaos experiment | System steady-state metrics | Human-written hypothesis + abort conditions | Inject failure (kill instance, add latency) | Compare control vs experimental groups; halt on blast-radius breach [12][13][14] |
| Canary / progressive delivery | KPI + error-rate metrics on canary cohort | Metric thresholds (optionally statistical) | Promote stepwise, or auto-rollback to stable | Each step re-measures before proceeding [27][29][30] |
| Feature flag kill switch | Ops dashboards / alerts | Human flips flag (a "manually-managed circuit breaker") | Feature off instantly, no deploy | Flag telemetry shows recovery [28] |
| ZFS | Checksum of every block on read & scrub | Checksum mismatch | Fetch good copy from mirror/RAID-Z parity and **repair in place** | Next scrub verifies [42] |
| PostgreSQL crash recovery | WAL on disk; data pages possibly stale/dirty | Always: replay (REDO) from last checkpoint | Roll-forward until consistent; no torn pages (`full_page_writes`) | Database comes up; recovery completes before accept [43] |
| Raft / etcd | Heartbeat (`AppendEntries`) timeout, randomized 150–300 ms | Majority vote; newer-term wins | Elect new leader; force follower logs to match | New leader re-establishes heartbeats [44][45] |
| Hardware/software watchdog | `/dev/watchdog` pings from userspace; sd_notify `WATCHDOG=1` for systemd | No ping before timeout | Hardware/firmware reboot; systemd SIGABRT + restart | System/service restarts from scratch [25][46] |
| Pre-LLM AIOps | Firehose of monitoring events | Correlation / causal graph clustering | Group alerts into one incident, rank root cause (advice only) | Human acts; system learns thresholds [40][41] |
| Getafix / SapFix | Static-analysis warnings / crash stack traces | Learned fix-pattern ranking / patch templates | Suggest a diff; (SapFix) auto-test candidate patches | Human engineer accepts, edits, or rejects [38][39] |

The pattern to internalize for the AI era: **the actuation mechanisms (restart, rollback, reroute, patch) already existed and were battle-tested by 2010–2020. What was missing was the *decide* stage being anything richer than a hand-written policy.**

## Deep dives

### 1. Erlang/OTP and "let it crash" — healing as a language property

Joe Armstrong's 2003 KTH dissertation, *Making Reliable Distributed Systems in the Presence of Software Errors*, is the founding text of industrial software self-healing [1]. Its central argument: since large programs *will* contain errors, the language and libraries must make it possible to build systems that "behave in a reasonable manner in the presence of software errors." Erlang's answer:

- **Fault isolation via processes.** Lightweight, share-nothing processes, communicating only by async message passing, so "an error in one process cannot affect the operation of other processes" — the process is the unit of service *and* the unit of failure [1]. Armstrong explicitly traces this to Jim Gray's Tandem work (*Why do computers stop and what can be done about it?*, 1985) and Schneider's fail-stop processors [1].
- **"Let it crash."** Section 4.4 of the thesis: workers do not program defensively; if the specification doesn't say what to do, the process crashes and "some other process" does error recovery. Corrected errors are not faults; uncorrected ones propagate as exit signals with reasons [1].
- **Supervision trees.** Supervors monitor workers (and other supervisors), with and/or hierarchies, restart strategies, and a *maximum restart intensity* — the modern OTP supervisor implements `one_for_one`, `one_for_all`, `rest_for_one`, `simple_one_for_one`, and terminates itself ("if more than MaxR restarts occur in the last MaxT seconds, the supervisor terminates all child processes and then itself") so that failure escalates to a higher, hopefully-wiser level [1][2].
- **Heartbeating (`heart`).** An external `heart` port program watches the runtime; if no heartbeat arrives within `HEART_BEAT_TIMEOUT` (default 60 s), it runs `HEART_COMMAND` — i.e., the last resort is *another* process restarting the whole node [3].
- **Hot code loading.** Two versions of a module coexist; fully-qualified tail calls pick up new code, enabling upgrade (and rollback) without stopping the system — Armstrong credits this pattern to NASA's X2000 and the Bluetail Mail Robustifier's four-phase reversible upgrade protocol [1].

**The nine-nines reality check.** The claim "Erlang systems achieve 99.9999999% availability" is repeated everywhere, usually about the Ericsson AXD301 (~1.7 M lines of Erlang). What is *actually documented* is Armstrong's own §8.5: "the only information on the long-term stability of the system came from a power-point presentation showing some figures claiming that a major customer had run an 11 node system with a 99.9999999% reliability, **though how these figures had been obtained was not documented**" [1]. (99.9999999% uptime is ≈31 ms of downtime per year — a figure essentially unmeasurable in practice.) The engineering lesson survives the marketing: the AXD301's 141-node supervision trees and trouble reports show real crashes detected, contained, and recovered in production, with the error log sufficient for post-mortem debugging [1]. Also documented: chief architect Ulf Wiger's finding that **"cascading restarts do not work"** — simple restart often heals; escalating restarts rarely does [1].

**Akka** carried the model to the JVM: parental supervision with restart/resume/stop strategies per exception type, restart limits, and failure bubbling up the actor hierarchy — a direct OTP descendant (now under Akka/`doc.akka.io`, with the Apache-licensed fork Pekko continuing the lineage) [4].

### 2. Resilience patterns: the network-era immune system

Michael Nygard's *Release It!* (Pragmatic Bookshelf; 2nd ed. 2018) named and motivated the stability patterns production systems still use: **circuit breaker**, **bulkhead**, **timeout**, **fail fast**, and **fallback**, born from post-mortems of cascading production failures [5].

- **Hystrix (Netflix).** Industrialized the patterns on the JVM: thread/semaphore isolation per dependency, circuit breakers, fallbacks, and real-time operational dashboards. The README now states it plainly: "Hystrix is no longer in active development, and is currently in maintenance mode" (final release 1.5.18), recommending **Resilience4j** for new projects and pointing at Netflix's own move to "adaptive implementations that react to an application's real time performance" [6]. That pivot is itself a lesson: *static, hand-tuned isolation budgets age badly as systems scale.*
- **Resilience4j** is the de-facto Java successor: composable, lightweight modules for CircuitBreaker, RateLimiter, Retry, TimeLimiter, Bulkhead, Cache, with first-class metrics [7]. **Polly** plays the same role in .NET (retry, circuit breaker, timeout, rate limiter, hedging, fallback; v8 "resilience pipelines"; .NET Foundation project) [8].
- **Adaptive concurrency.** Netflix's `concurrency-limits` replaces fixed thread pools with limits auto-detected from latency signals, using ideas from **TCP congestion control** (Vegas, Gradient2) — the system measures its own queuing and backs off, i.e., a self-tuning bulkhead [11].
- **Retries done carefully.** gRPC's retry design (proposal A6) is the canonical spec: `maxAttempts` (client-capped at 5), exponential backoff with jitter, retryable status codes, hedging, and — crucially — a **per-service token-bucket retry throttle**: once too many RPCs fail, clients stop retrying [9]. AWS's Builders' Library article explains *why*: retries are "selfish," a five-deep call stack with three retries per layer can impose **243×** load on an already-failing dependency, and "retry storms" keep load high long after the original issue resolves — hence capped exponential backoff with full jitter and token-bucket retry budgets [10].

### 3. Chaos engineering: making healing a tested property

Self-healing claims are worthless if the healing path never runs. Netflix's response was to *inject the failure deliberately, in production, during business hours*: the Simian Army blog post (July 19, 2011) introduced Chaos Monkey ("randomly disables our production instances to make sure we can survive this common type of failure without any customer impact"), plus Latency Monkey, Conformity Monkey, Doctor Monkey, Janitor Monkey, Security Monkey, 10-18 Monkey, and Chaos Gorilla (whole-AZ outage) [12]. Chaos Monkey was later open-sourced (GitHub, Go, Spinnaker-integrated) [15].

Basiri et al. (*Chaos Engineering*, IEEE Software 33(3):35–41, 2016; DOI 10.1109/MS.2016.60) named the discipline: experimenting on a distributed system "to build confidence in the system's capability to withstand turbulent conditions in production" [13]. **Principles of Chaos Engineering** codified the method: define steady state as a measurable output, hypothesize it persists, inject real-world variables (crashes, latency, severed connections), and try to *disprove* the hypothesis — with advanced principles demanding production experiments, continuous automation, and minimized blast radius [14]. GameDays — scheduled, whole-team failure drills — are the organizational ritual around the tooling.

The ecosystem matured into products and platforms: **Gremlin** (commercial, enterprise-grade fault injection with blast-radius controls and automatic halting) [16]; **Chaos Mesh** (CNCF incubating; Kubernetes CRDs for pod/network/IO/kernel faults with orchestrated workflows) [17]; and **LitmusChaos** (CNCF incubating; chaos workflows, ChaosHub experiment catalog, steady-state probes) [18].

### 4. Kubernetes and desired-state reconciliation — self-healing as an operating-system primitive

Google's Borg (Verma et al., EuroSys 2015) demonstrated at ~10,000-machine scale that a cluster manager continuously reconciling actual state toward declared state — restarting failed tasks, rescheduling evicted jobs, spreading replicas for fault tolerance — is the right substrate for reliable services [19]. Kubernetes generalized Borg's ideas, and self-healing is stated as a headline property in its own docs: "Kubernetes restarts containers that fail, replaces containers, kills containers that don't respond to your user-defined health check, and doesn't advertise them to clients until they are ready to serve" [20].

The healing machinery, layer by layer:

- **Probes.** *Liveness* probes detect unrecoverable states → kubelet kills and restarts the container; *readiness* probes gate Service traffic (no restart); *startup* probes protect slow-starters with a `failureThreshold × periodSeconds` budget [21].
- **Restart policy & crash-loop damping.** `restartPolicy: Always | OnFailure | Never`, with kubelet restarts **exponentially backed off (10 s, 20 s, 40 s … capped at 300 s)** and reset after 10 healthy minutes — a direct answer to the "cascading restarts do not work" problem [22][1].
- **Reconciliation loops.** Every controller (kubelet, deployment, node, etc.) is a level-triggered watch loop driving current state to desired state — "Kubernetes comprises a set of independent, composable control processes that continuously drive the current state towards the provided desired state" [20].
- **Operators.** The operator pattern packages *human operational knowledge* — deploy, backup/restore, upgrade, failure recovery, leader election — as software: custom resources + a reconcile loop, so healing a database becomes as declarative as healing a webserver; OperatorHub.io catalogs hundreds of them [23][24].
- **The host layer: systemd.** `Restart=always|on-failure|on-watchdog|on-abnormal|on-abort|on-success` gives process-level resurrection, and `WatchdogSec=` + `sd_notify("WATCHDOG=1")` implements a per-service software watchdog: miss the keep-alive interval and systemd kills the service with SIGABRT and restarts it — an in-process analogue of Erlang's `heart` [25][3]. At the kernel/hardware layer, the Linux watchdog core exposes `/dev/watchdog`: "This is the time after which the system will reboot if user space does not send a heartbeat" — the oldest self-healing loop in computing [46].

None of this is intelligent, and none of it needs to be: the healing policy is *declared*, and the machinery executes it millions of times a day.

### 5. Progressive delivery: healing by routing away from bad code

Most outages are caused by *change*; the cheapest heal is to remove the change from the request path. The pre-AI toolbox:

- **Blue-green deployment** (Fowler, 2010): two identical production environments; flip the router to cut over; "a rapid way to rollback" is the explicit goal [26].
- **Canary release** (Sato, 2014): expose a small cohort first, compare behavior, ramp up or reroute back; Fowler's site notes IMVU's "cluster immune system" — automatic rollback on statistically significant regressions — as early automation of the heal decision [27].
- **Feature flags** (Hodgson, 2017): decouple deploy from release; **ops toggles / kill switches** are "a manually-managed Circuit Breaker" for instantly degrading non-critical features under load. The same article carries the field's cautionary tale — toggle/automation mistakes like **Knight Capital's $460 M loss** — and the doctrine of managing "toggle debt" [28].
- **Argo Rollouts**: a Kubernetes controller + CRDs providing canary and blue-green strategies, metric analysis against providers (Prometheus, Datadog, …), and **automated rollbacks and promotions** — the heal loop automated at the deployment layer [29].
- **Flagger** (Flux/CNCF): an operator that shifts traffic to new versions via mesh/ingress, runs conformance tests, queries metric providers, and "can roll back automatically rather than promote" [30].

This is healing in the strict sense — detection (metrics), decision (thresholds), action (traffic shift/rollback) — aimed at the failure class that causes the most incidents: bad deployments.

### 6. Observability: the sensory system healing depends on

Every healing loop above consumes telemetry; the pre-AI era standardized how it is produced.

- **Doctrine.** Google's SRE book, ch. 6 (Ewaschuk, 2017): alert on *symptoms* not causes, prefer white-box monitoring for imminent failures and black-box for user-visible ones, and track the **four golden signals** — latency, traffic, errors, saturation [31].
- **Metrics.** Prometheus (born at SoundCloud in 2012, CNCF's second hosted project after Kubernetes in 2016): multi-dimensional time series, PromQL, pull-based collection, Alertmanager — the default actuation *source* for k8s-native healing loops [32]. **Grafana** unified visualization across metrics/logs/traces with 150+ data-source plugins and alerting [33].
- **Traces & logs.** **OpenTelemetry** merged OpenTracing and OpenCensus into the vendor-neutral API/SDK/Collector standard for the classic "three pillars" — traces, metrics, logs — that Flagger/Argo analysis and every runbook consume [34].
- **eBPF observability** added a kernel-native sense organ without instrumentation: ebpf.io describes sandboxed kernel programs "without requiring to change kernel source code or load kernel modules," used for networking, tracing, and security [35]; **bpftrace** provides the high-level one-liner language for kernel tracing [36]; **Cilium** applies eBPF to Kubernetes networking/observability/security [37].

Observability is context here, not subject: it is the *observe* stage that every actuation loop — and every future LLM healer — reads from.

### 7. Pre-LLM AIOps: correlation, anomaly detection, and the first real AI repair

"AIOps" (algorithmic IT operations) was the pre-LLM attempt to automate the *decide* stage with classical ML:

- **Event correlation & alert compression.** Moogsoft built the archetype: cluster alert storms into situational incidents, cut noise, prioritize — its 2023 acquisition by Dell ("an AI-driven provider of intelligent monitoring solutions that support DevOps and ITOps"; now Dell APEX AIOps Incident Management) shows the category consolidating into platform vendors [41].
- **Causal AI.** Dynatrace's positioning is explicit: correlational ML predicts, but **causal AI "determines the precise root cause of an issue"** from a live dependency map, powering automated root-cause analysis and even "automated remediation (server restarts, code rollbacks)" — though the action catalog remains fixed, pre-programmed remediations [40].
- **The milestone: AI that fixes code.** Meta's **Getafix** (Bader, Scott, Pradel, Chandra; OOPSLA 2019) learns fix patterns from past human fixes (hierarchical clustering + AST transformation) and suggests fixes for Infer static-analysis warnings at Facebook — "the first industrially deployed automated bug-fixing tool that learns fix patterns from past human fixes," predicting the exact human fix as top suggestion 12–91% of the time depending on bug category [38]. **SapFix** (Jia, Mao, Harman; Facebook Engineering, 2018) went end-to-end: take a crash found by Sapienz search-based testing, localize with Infer, generate candidate patches (revert / human templates / AST mutations), auto-test them, and propose to an engineer "for approval and deployment to production" — deployed against Facebook's Android app, and framed as "the first such use of AI-powered testing and debugging tools in production at this scale" [39]. Human approval was mandatory: the AI proposed, engineers disposed.

These two systems matter for the project's thesis: they are the boundary of pre-LLM *healing of the code itself* — narrow, template/learning-based, and human-gated.

### 8. Classic fault tolerance: healing that never needed a model

The deepest stratum of the playbook predates everything above and heals without any notion of intelligence:

- **RAID** (Patterson, Gibson, Katz, *A Case for Redundant Arrays of Inexpensive Disks (RAID)*, SIGMOD 1988) established redundancy-at-the-block-layer — mirrored/parity-protected data surviving disk loss **[UNVERIFIED — canonical paper; URL not fetched in this pass]**.
- **ZFS self-healing.** Oracle's own documentation: "ZFS provides self-healing data in a mirrored or RAID-Z configuration. When a bad data block is detected, not only does ZFS fetch the correct data from another redundant copy, but it also repairs the bad data by replacing it with the good copy" — detection via per-block checksums (on every read and during scrubs), repair via redundancy: a literal detect→decide→act→verify loop in the filesystem [42].
- **PostgreSQL WAL.** "Changes to data files … must be written only after those changes have been logged"; on crash, "any changes that have not been applied to the data pages can be redone from the WAL records (roll-forward recovery, also known as REDO)," with `full_page_writes` defending against torn pages — the database heals itself to consistency on every unclean shutdown, by design [43].
- **Consensus: Raft & etcd.** Ongaro & Ousterhout's Raft (USENIX ATC 2014) is self-healing as group protocol: randomized-timeout leader election (150–300 ms), log forced to converge to the leader's, a 5-node cluster tolerating 2 failures, safety independent of timing — "the servers appear to form a single, highly reliable state machine" [44]. etcd implements Raft as "a strongly consistent, distributed key-value store" — the healing substrate beneath Kubernetes' own state [45].
- **Watchdog timers.** From embedded controllers to industrial PLCs to Linux: if the software stops feeding `/dev/watchdog`, hardware reboots the machine — the blunt, provable heal of last resort [46][25].

## Pattern catalog

| # | Pattern | Layer | Detects | Heals by | Limitation without AI |
|---|---|---|---|---|---|
| 1 | Let-it-crash worker | Process/runtime | Unhandled exception, spec deviation | Crash fast; state discarded [1] | Heals *symptom*; bug persists; crash-loop if deterministic fault |
| 2 | Supervision tree | Process/runtime | Exit signals w/ reason | Restart per strategy; escalate on intensity [1][2] | Restart policy fixed at design time; "cascading restarts do not work" [1] |
| 3 | `heart` / node heartbeat | Node | Heartbeat timeout (60 s) | Reboot node / start replacement [3] | Total state loss; no diagnosis |
| 4 | Hot code loading / reversible release | Runtime | Operator-triggered | Swap module version; rollback (BMR 4-phase) [1] | Human decides *when* and *what*; forward/backward compatibility is manual |
| 5 | Akka supervision | Actor system (JVM) | Exception in actor | Restart/resume/stop child, rate-limited [4] | Same as OTP: policy is static |
| 6 | Circuit breaker | Service call | Error/latency rate over window | Fail fast + fallback; probe half-open [5][6][7][8] | Thresholds hand-tuned; degrades silently as traffic patterns drift |
| 7 | Bulkhead | Execution | Resource exhaustion of a dependency | Isolate pools so one consumer can't starve others [5][7] | Pool sizes static (see adaptive concurrency, #9) |
| 8 | Retry w/ backoff + jitter + budget | RPC | Transient error codes | Re-attempt idempotent call, capped [9][10] | Wrong retry policy amplifies outage (243×) [10]; can't tell transient from permanent |
| 9 | Adaptive concurrency limit | RPC | Self-induced latency divergence (Vegas/Gradient2) | Shrink concurrency to stop queuing [11] | Only protects against overload; no root-cause insight |
| 10 | Chaos experiment | Whole system | Hypothesis violation (steady-state delta) | Nothing itself — *validates* healing loops [12][13][14] | Experiments human-authored; coverage bounded by imagination |
| 11 | Liveness probe + restart | Container | Deadlock, unrecoverable state | Kill & restart container, exp. backoff to 300 s [21][22] | Restart ≠ repair; live-locks pass probes; false positives kill healthy pods |
| 12 | Desired-state reconciliation | Cluster | Drift actual ≠ declared | Converge: create/replace/reschedule [19][20] | Can only reach states expressible in the spec; bugs in spec = healed-into-wrong-state |
| 13 | Operator / CRD controller | Application (on k8s) | CR status drift, app-specific failures | Backup/restore, failover, upgrade — codified runbook [23][24] | Ops knowledge must be hand-coded per app; novel failure needs new operator code |
| 14 | Blue-green cut-over | Deployment | Bad new version (human/metrics) | Flip router back to old env [26] | Doubled infra; DB migrations break symmetry |
| 15 | Canary + metric analysis | Deployment | KPI/error regression on cohort | Auto-rollback (Argo/Flagger) [27][29][30] | Threshold/statistical windows hand-chosen; slow-burn damage passes canary |
| 16 | Feature-flag kill switch | Feature | Ops judgment / alerts | Flag off, no deploy [28] | Human decides; toggle debt + automation risk (Knight Capital) [28] |
| 17 | Event correlation (AIOps) | Operations | Alert storms, duplicates | Compress into incident + rank causes [40][41] | Advice only; no actuation; correlations brittle to topology change |
| 18 | Causal-AI root cause (Davis) | Operations | Anomaly on dependency map | Pinpoint root cause; trigger pre-set remediation [40] | Remediation catalog fixed; explanation shallow outside mapped topology |
| 19 | Learned fix suggestion (Getafix) | Code | Static-analysis warning | Suggest diff learned from past fixes (human applies) [38] | Only recurring, pattern-shaped bugs; context-blind beyond AST |
| 20 | Automated crash repair (SapFix) | Code | Crash from automated testing | Generate+test+propose patch end-to-end [39] | Narrow bug classes; human gate; no reasoning about novel failures |
| 21 | WAL crash recovery | Storage/DB | Unclean shutdown | REDO replay to consistent point [43] | Only heals *state*, never the fault; bounded by what was committed |
| 22 | Checksum self-repair (ZFS) | Filesystem | Checksum mismatch (bit rot) | Reconstruct block from redundancy, repair in place [42] | Needs redundancy; silent beyond pool boundary; no fix for logic errors |
| 23 | Consensus re-election (Raft/etcd) | Coordination | Leader heartbeat timeout | Elect new leader; converge logs [44][45] | Availability only with live majority; partitioned minority stalls |
| 24 | Watchdog timer | Firmware/OS | No heartbeat from software | Hard reboot / service SIGABRT [25][46] | Dumbest possible heal; loses volatile state; can mask deep faults |

## Key numbers

- **99.9999999% ("nine nines")** — AXD301 availability claim. Documented *by Armstrong himself* as originating from a PowerPoint slide about an 11-node customer system, "though how these figures had been obtained was not documented" [1]. (≈31 ms downtime/year — treat as folklore with a real system behind it.)
- **AXD301 scale:** >1.7 M lines of Erlang; studied snapshot 1,136,150 lines across 2,248 modules; supervision forest of 141 nodes / 191 behaviour instances — 122 `gen_server`, 36 `gen_event`, 20 supervisors, 10 `gen_fsm`, 6 applications [1].
- **Bluetail Mail Robustifier:** availability target "downtime … a few minutes per decade"; built by ~5–10 people in ~6 months, 36,285 lines / 108 modules, with fully reversible 4-phase software upgrades [1].
- **Telecom baseline that motivated Erlang:** switches designed for "less than two hours of down-time in 40 years" (Kuhn, quoted in [1]).
- **Retry-storm math:** 5-layer call chain × 3 retries per layer = up to **243×** amplified load on the failing bottom dependency; AWS SDKs added token-bucket retry budgets in 2016 to cap this [10]. gRPC clients cap `maxAttempts` at **5** by default and stop retrying when the per-service token bucket falls to half [9].
- **Kubelet restart backoff:** 10 s → 20 s → 40 s … capped at **300 s**, reset after 10 clean minutes [22].
- **Chaos Monkey cadence:** designed to run "in the middle of a business day … with engineers standing by" so that "next time an instance fails at 3 am on a Sunday, we won't even notice" [12].
- **Getafix accuracy:** predicts the *exact* human fix as top-1 suggestion **12–91%** of the time depending on bug category, across 1,268 evaluated human fixes [38].
- **Outage cost (industry):** 90% of firms report hourly downtime cost > **$300,000** (ITIC 2024) [47]; 54% of operators say their most recent significant outage cost > **$100,000**, and 16% > **$1 million** (Uptime Institute Annual Outage Analysis 2024) [48].
- **Cost of failed change/automation:** **$460 M** lost by Knight Capital in 45 minutes (2012), cited in the feature-toggle literature as the canonical kill-switch/automation failure [28].
- **Prometheus pedigree:** started 2012; CNCF's **second** hosted project after Kubernetes itself (2016) [32].
- **Raft's timing envelope:** typical election timeout 150–300 ms; broadcastTime ≪ electionTimeout ≪ MTBF; 5-member cluster survives 2 arbitrary node failures [44].

## How the pre-AI playbook falls short

1. **Restart is not repair.** Every runtime loop (OTP, kubelet, systemd, watchdog) heals by *state reset*. It works because, as Gray conjectured (quoted in [1]), most production faults are transient and soft — but deterministic bugs crash-loop (hence CrashLoopBackOff backoff caps [22]), and Wiger's AXD301 experience already showed escalating restarts failing [1]. The defect that caused the failure ships again tomorrow.
2. **The decide stage is frozen at design time.** Thresholds, restart strategies, canary windows, breaker settings — all hand-written by engineers who must *anticipate* the failure. Adaptive concurrency [11] and causal-AI root cause [40] stretched this, but neither writes new policy, let alone new code, in response to a novel failure.
3. **The last mile is a human with a runbook.** Operators codify routine action [23], and SRE doctrine organizes on-call [31], but anything beyond restart/rollback/reroute — interpreting an unfamiliar stack trace, correlating a cross-service anomaly, authoring the hotfix — stops at a paged engineer. At 3 a.m. This is precisely the labor LLMs now target.
4. **Alert fatigue is structural.** Distributed systems emit event storms; correlation/compression tools exist precisely because paging humans doesn't scale [40][41]. A healer that must *read* telemetry faster than humans is the natural next step after a healer that merely counts.
5. **Change is the dominant failure source, and canaries are myopic.** Progressive delivery automates rollback [29][30], but only for regressions visible in the chosen metrics within the analysis window — slow-burn damage, data corruption, and config-level bugs sail through. Knight Capital shows what happens when the flag/automation layer itself errs [28].
6. **Pre-LLM "AI healing" was narrow and human-gated.** Getafix handles recurring static-analysis patterns [38]; SapFix handles specific crash classes with mandatory engineer approval [39]. Neither reads incident context, nor reasons across services, nor writes novel code — the exact capabilities LLMs now claim.
7. **Even the measurements are shaky.** The flagship reliability number of the pre-AI era is, by its author's own account, an undocumented slide [1]. If we could barely *measure* healing, automating its verification (did the heal actually restore invariants?) remains an open problem any AI healer must solve for itself.

**The synthesis for this project:** the pre-AI era left us (a) battle-tested actuation APIs at every layer — restart, rollback, reroute, re-elect, replay, repair-in-place; (b) a mature sensory system — logs, metrics, traces, eBPF; and (c) a hard boundary where policy ran out and humans took over. LLM-era self-healing is best understood not as a new invention but as **replacing the hand-written decide stage of these existing loops** — and the engineering discipline (blast radius, steady-state validation, human gates) that chaos engineering taught is the safety envelope that AI healers must inherit.

## Canonical references

1. Making Reliable Distributed Systems in the Presence of Software Errors (PhD thesis) — Joe Armstrong, KTH Royal Institute of Technology, 2003 — https://erlang.org/download/armstrong_thesis_2003.pdf (accessed 2026-11-09)
2. Supervision Principles — Erlang/OTP System Documentation — https://www.erlang.org/doc/design_principles/sup_princ.html (accessed 2026-11-09)
3. heart — Erlang/OTP Reference Manual — https://www.erlang.org/doc/man/heart.html (accessed 2026-11-09)
4. Fault Tolerance (Typed Akka) — Akka / Lightbend — https://doc.akka.io/docs/akka/current/typed/fault-tolerance.html (accessed 2026-11-09)
5. Release It! Design and Deploy Production-Ready Software (2nd ed.) — Michael T. Nygard, Pragmatic Bookshelf, 2018 — https://pragprog.com/titles/mnee2/release-it-second-edition/ (accessed 2026-11-09)
6. Hystrix: latency and fault tolerance library (maintenance mode) — Netflix, GitHub — https://github.com/Netflix/Hystrix (accessed 2026-11-09)
7. Resilience4j Documentation — resilience4j.org — https://resilience4j.readme.io/docs (accessed 2026-11-09)
8. Polly: .NET resilience and transient-fault handling library — App-vNext / .NET Foundation, GitHub — https://github.com/App-vNext/Polly (accessed 2026-11-09)
9. gRPC Retry Design (Proposal A6) — grpc/proposal, GitHub — https://github.com/grpc/proposal/blob/master/A6-client-retries.md (accessed 2026-11-09)
10. Timeouts, retries, and backoff with jitter — Marc Brooker, AWS Builders' Library, 2019 — https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ (accessed 2026-11-09)
11. concurrency-limits: adaptive concurrency limits — Netflix, GitHub — https://github.com/Netflix/concurrency-limits (accessed 2026-11-09)
12. The Netflix Simian Army — Yury Izrailevsky & Ariel Tseitlin, Netflix TechBlog, 2011 — https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116 (accessed 2026-11-09)
13. Chaos Engineering — A. Basiri, N. Behnam, R. de Rooij, L. Hochstein, L. Kosewski, J. Reynolds, C. Rosenthal, IEEE Software 33(3):35–41, 2016 — https://arxiv.org/abs/1702.05843 (DOI 10.1109/MS.2016.60) (accessed 2026-11-09)
14. Principles of Chaos Engineering — principlesofchaos.org — https://principlesofchaos.org/ (accessed 2026-11-09)
15. Chaos Monkey — Netflix, GitHub — https://github.com/Netflix/chaosmonkey (accessed 2026-11-09)
16. Gremlin: reliability/chaos engineering platform — Gremlin, Inc. — https://www.gremlin.com/ (accessed 2026-11-09)
17. Chaos Mesh: cloud-native chaos engineering — Chaos Mesh / CNCF (incubating) — https://chaos-mesh.org/ (accessed 2026-11-09)
18. LitmusChaos: open-source chaos engineering platform — LitmusChaos / CNCF (incubating) — https://litmuschaos.io/ (accessed 2026-11-09)
19. Large-scale cluster management at Google with Borg — A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, J. Wilkes, EuroSys 2015 — https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/ (accessed 2026-11-09)
20. Kubernetes Documentation: What is Kubernetes — CNCF/kubernetes.io — https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/ (accessed 2026-11-09)
21. Configure Liveness, Readiness and Startup Probes — kubernetes.io — https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ (accessed 2026-11-09)
22. Pod Lifecycle (restartPolicy, crash-loop backoff) — kubernetes.io — https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (accessed 2026-11-09)
23. Operator pattern — kubernetes.io — https://kubernetes.io/docs/concepts/extend-kubernetes/operator/ (accessed 2026-11-09)
24. OperatorHub.io: the registry for Kubernetes Operators — CNCF/Red Hat et al. — https://operatorhub.io/ (accessed 2026-11-09)
25. systemd.service(5) — systemd / freedesktop.org — https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html (accessed 2026-11-09)
26. Blue Green Deployment — Martin Fowler, 2010 — https://martinfowler.com/bliki/BlueGreenDeployment.html (accessed 2026-11-09)
27. Canary Release — Danilo Sato, martinfowler.com, 2014 — https://martinfowler.com/bliki/CanaryRelease.html (accessed 2026-11-09)
28. Feature Toggles (aka Feature Flags) — Pete Hodgson, martinfowler.com, 2017 — https://martinfowler.com/articles/feature-toggles.html (accessed 2026-11-09)
29. Argo Rollouts Documentation — Argo / CNCF — https://argo-rollouts.readthedocs.io/en/stable/ (accessed 2026-11-09)
30. Flagger Documentation — fluxcd/flagger (CNCF) — https://docs.flagger.app/ (accessed 2026-11-09)
31. Monitoring Distributed Systems (Site Reliability Engineering, ch. 6) — Rob Ewaschuk, Google/O'Reilly, 2017 — https://sre.google/sre-book/monitoring-distributed-systems/ (accessed 2026-11-09)
32. Prometheus Documentation: Overview — prometheus.io — https://prometheus.io/docs/introduction/overview/ (accessed 2026-11-09)
33. Grafana OSS: open-source visualization & monitoring — Grafana Labs — https://grafana.com/oss/grafana/ (accessed 2026-11-09)
34. OpenTelemetry Documentation — CNCF/opentelemetry.io — https://opentelemetry.io/docs/ (accessed 2026-11-09)
35. What is eBPF? — ebpf.io (Cilium/community) — https://ebpf.io/what-is-ebpf/ (accessed 2026-11-09)
36. bpftrace: high-level tracing language for Linux eBPF — bpftrace.org — https://bpftrace.org/ (accessed 2026-11-09)
37. Cilium: eBPF-based networking, observability, security — Cilium — https://cilium.io/ (accessed 2026-11-09)
38. Getafix: Learning to Fix Bugs Automatically — J. Bader, A. Scott, M. Pradel, S. Chandra, OOPSLA/PACMPL 3, 2019 — https://arxiv.org/abs/1902.06111 (accessed 2026-11-09)
39. Finding and fixing software bugs automatically with SapFix and Sapienz — Yue Jia, Ke Mao, Mark Harman, Facebook Engineering Blog, 2018 — https://engineering.fb.com/2018/09/13/developer-tools/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/ (accessed 2026-11-09)
40. Causal AI use cases for modern observability — Bipin Singh, Dynatrace Blog, 2024 — https://www.dynatrace.com/news/blog/causal-ai-use-cases-for-modern-observability/ (accessed 2026-11-09)
41. Dell Technologies Announces Intent to Acquire Moogsoft — Dell Technologies / PR Newswire, 2023 — https://www.prnewswire.com/news-releases/dell-technologies-announces-intent-to-acquire-moogsoft-301881557.html (accessed 2026-11-09)
42. Self-Healing Data in a Redundant Configuration — Oracle Solaris ZFS Administration Guide — https://docs.oracle.com/cd/E36784_01/html/E36835/gazch.html (accessed 2026-11-09)
43. Reliability and the Write-Ahead Log — PostgreSQL Documentation (current) — https://www.postgresql.org/docs/current/wal-intro.html (accessed 2026-11-09)
44. In Search of an Understandable Consensus Algorithm (Extended Version) — Diego Ongaro & John Ousterhout, Stanford, 2014 — https://raft.github.io/raft.pdf (accessed 2026-11-09)
45. etcd: distributed, consistent key-value store — CNCF — https://etcd.io/ (accessed 2026-11-09)
46. The Linux WatchDog Timer Driver Core kernel API — kernel.org — https://docs.kernel.org/watchdog/watchdog-kernel-api.html (accessed 2026-11-09)
47. ITIC Reports & Surveys — 2024 Hourly Cost of Downtime ("exceeds $300,000 for 90% of firms") — Information Technology Intelligence Consulting, 2024 — https://itic-corp.com/itic-reports-surveys (accessed 2026-11-09)
48. Annual Outage Analysis 2024 — Uptime Institute, 2024 — https://uptimeinstitute.com/resources/research-and-reports/annual-outage-analysis-2024 (accessed 2026-11-09)

*Not fully verified: the RAID founding paper (Patterson, Gibson, Katz, "A Case for Redundant Arrays of Inexpensive Disks (RAID)," SIGMOD 1988) is referenced conceptually and marked [UNVERIFIED] in the text because no URL for it was fetched during this pass. The 54%-over-$100K / 16%-over-$1M Uptime Institute figures were confirmed via the report landing page and search-indexed summaries of the (gated) full report [48].*

## Open questions

1. **Which layer yields first to LLM healers?** The loops nearest rich text (runbooks, incident channels, stack traces) vs. those with cheap actuation (k8s restart/rollback APIs) — where is the first production-grade, audited AI decide stage?
2. **What replaces the hand-written policy?** Adaptive concurrency learned from latency [11]; causal AI learned from topology [40]; can a policy *learned by an LLM from incident history* be trusted inside a supervision tree — and how would we prove it (chaos-engineering style steady-state validation [14])?
3. **The SapFix line: human approval.** Pre-LLM repair kept engineers in the loop [38][39]. Is approval-then-deploy the right permanent contract for AI-generated hotfixes, or does blast-radius math (à la chaos engineering) justify autonomy below a reversible-action threshold?
4. **Measurement.** If the canonical reliability number of the era was an undocumented slide [1], what does an honest benchmark for AI healing look like — MTTR deltas against the pre-AI loops in this dossier, on comparable outage-cost baselines [47][48]?
5. **Does "let it crash" get stronger or weaker with LLMs?** Cheap crash-restart plus cheap *code repair* might finally complete the loop Armstrong sketched (heal the software, not just the process) — or might make systems so stateful-and-smart that crashing destroys precious learned context.
6. **Operator-pattern write-back.** Operators encode human ops knowledge [23]; can an AI healer *author operator code / runbooks* as its output artifact, turning one-shot heals into permanent loop upgrades — and who reviews that diff?
