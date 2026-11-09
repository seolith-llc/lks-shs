# 03 · Self-Healing in System Programming

> Workstream dossier for #Step001 — the OS / kernel / hardware-near layer of self-healing software.
> Scope: kernel live patching, process supervision, watchdogs, memory-error handling (EDAC/MCE), eBPF as
> sensing + actuation, memory safety and fuzzing as prevention, self-healing storage (ZFS, WAL, Raft),
> embedded watchdog tradition, and where AI (pre-LLM and LLM-era) has actually entered systems work.
> Method: primary sources preferred (kernel.org docs, papers, official project docs, engineering blogs);
> every URL below was fetched/verified on 2026-11-09. Items that could not be verified are marked **[UNVERIFIED]**.
> Citation format: `[n] Title — Author/Org, Year — URL (accessed 2026-11-09)`. Numbering runs continuously.

## TL;DR

- **The systems layer has practiced self-healing for decades**, long before AI: hardware ECC corrects bit flips in silicon, watchdog timers reboot hung firmware, Linux live patching swaps buggy kernel functions under a running system (Ksplice proved 88% of kernel security patches need no new code), and ZFS repairs bit rot on every read.
- **Healing is layered**: hardware (ECC, watchdogs) → kernel (livepatch, soft-offline, OOM killer, kdump/kexec reboot) → process (systemd restart policies, software watchdog, `PDEATHSIG`) → storage (ZFS scrub, fsck, WAL replay, Raft re-election) → network (eBPF/XDP). Each layer catches what the one below misses.
- **eBPF is the key modern enabler for the "actuation" half of the loop**: verified, safe kernel instrumentation and enforcement without rebooting or loading crashable modules — the sensing layer (bpftrace/BCC) and the response layer (Cilium/Tetragon) of a self-healing system.
- **Prevention is the cheapest cure**: ~70% of Microsoft CVEs and ~70% of Chromium high-severity bugs are memory-safety issues; Android drove its share from 76% (2019) to 24% (2024) by writing new code in Rust — "healing before the wound" at language level.
- **Fuzzing pipelines already close the loop mechanically**: OSS-Fuzz + ClusterFuzz continuously fuzz 1,000+ OSS projects (36,000+ bugs fixed) with automated triage, bisection and testcase minimization — the plumbing an AI patcher can be bolted onto, and Google has now bolted one on (OSS-Fuzz + CodeMender, 2026).
- **AI repair in systems is not new**: Meta's Getafix/SapFix (2018–19) already auto-generated, validated, and shipped machine-written fixes into production Facebook Android builds — with a human approval gate; Getafix auto-patched 53% of ~2,000 null-call bugs in an Instagram experiment.
- **LLM-era results are real but early**: Google's AI fuzzing found a ~20-year-old OpenSSL bug (CVE-2024-9143) and Big Sleep found the first publicly disclosed AI-agent zero-day (SQLite, 2024); Microsoft's Triangle multi-agent system improved cloud incident triage accuracy by >20% and is deployed for tens of millions of users; but on cloud infrastructure code (SWE-InfraBench, 2026) the best agent solves only ~34% of tasks.
- **Kernel live patching is now commodity infrastructure**: RHEL/kpatch (now deprecated upstream in favor of `klp-build` at Linux 6.19), SUSE KLP (>95% of qualifying fixes shipped live), Ubuntu Livepatch, Oracle Ksplice — all ship CVE fixes without reboot, all bounded by the same rule: patches that change data-structure semantics still need a reboot.
- **The unglamorous mechanisms are the workhorses**: `oom_score_adj`, `panic=N`, `Restart=on-failure`, `WatchdogSec=`, `/dev/watchdog` magic-close, `zpool scrub`, `VACUUM`-free WAL replay — self-healing in production is mostly *policy over primitive*, and the AI frontier is automating the policy, not replacing the primitives.
- **Several rumored items do not exist** as far as verifiable sources show: "SuperHELM" (Microsoft) and "KernelBiologist" (Google) **[UNVERIFIED — no trace found]**; the genuine article behind such names is Microsoft's Triangle/RCACopilot and UIUC's KernelGPT.

## The systems healing toolbox

| Layer | Mechanism | Heals what | Cost / caveat | Ref |
|---|---|---|---|---|
| Hardware | ECC (SECDED, chipkill) | Bit flips in RAM, transparently | Uncorrectable errors still fatal; error storms | [13], [14] |
| Hardware | Watchdog timer (WDT) | Hung firmware/OS — hard reset | Single-user (`/dev/watchdog`); nowayout can brick remote boxes | [9], [10] |
| CPU/RAS | Machine-check handling + EDAC + rasdaemon/mcelog | Classifies CE/UE/deferred errors; predicts failing DIMM/page | UE typically panics; needs ECC reporting | [13]–[15] |
| Memory mgmt | Soft page offlining (`memory_failure`) | Failing page retired, contents migrated, page poisoned | Needs a physical address from the MC | [14] |
| Kernel | Live patching (livepatch/KLP, kpatch, Ksplice) | CVEs in running kernel, no reboot | Function-granularity; data-structure changes still need reboot | [1]–[5] |
| Kernel | OOM killer (`oom_badness`, `oom_score_adj`) | System-wide memory exhaustion | Kills by badness heuristic; can shoot the wrong process | [12] |
| Kernel | `panic=` + kdump/kexec | Unrecoverable panic → controlled dump + fast reboot | Reserves memory; dump I/O takes minutes | [11], [16] |
| Kernel | eBPF programs (verified) | Sensing + enforcement without kernel modules or reboot | Verifier limits; privileged | [17]–[21] |
| Process | Supervisor restart (`Restart=`, start limits) | Crashed/hung daemon | Restart storms need `StartLimitAction=` | [7] |
| Process | Software watchdog (`WatchdogSec=` + `sd_notify("WATCHDOG=1")`) | Hangs (not crashes) — liveness, not just existence | App must be instrumented; ping at ~half interval | [7], [8] |
| Process | `PR_SET_PDEATHSIG` | Orphaned children of a dead supervisor | Fires on parent *thread* death; cleared on setuid exec | [6] |
| Storage | ZFS checksumming + scrub/resilver | Silent bit rot, torn writes; auto-repair from redundancy | No redundancy = detection only; scrub I/O cost | [22], [23] |
| Storage | fsck family (e2fsck, xfs_repair, btrfs check) | Post-crash metadata inconsistency | Offline/journal-limiting; repair can lose data | [24] |
| Storage | Software RAID (md) resync/recover, PPL | Failed disk rebuild; write hole | Dirty+degraded RAID5/6 may hold undetectable corruption | [25] |
| Data | PostgreSQL WAL + full-page writes + CRC-32C | Crash mid-write: torn pages rebuilt from WAL | Assumes honest fsync and ECC RAM | [26] |
| Coordination | Raft leader election (etcd) | Failed leader/member; partitioned minority | Quorum loss = read-only; committed writes never lost | [27], [28] |
| Embedded/industrial | External WDTs, safety watchdogs, ELISA-style certification | Whole-system hangs in long-lived unattended devices | Reboot is the only repair; certification burden | [9], [29] |
| AI (emerging) | Fuzz→triage→patch agents; incident agents | Bug finding/fixing, triage, RCA | Human review still load-bearing; IaC accuracy ~34% | [30]–[41] |

## Deep dives

### 1. Kernel live patching: fixing the OS under its own feet

The Linux kernel's in-tree **livepatch (KLP)** subsystem "allows for function calls to be redirected; thus,
fixing critical functions without a system reboot" [1]. Its **consistency model is a hybrid of kGraft and
kpatch**: it "uses kGraft's per-task consistency and syscall barrier switching combined with kpatch's stack
trace switching" [1]. Patches apply per task when the task is *safe to switch* — primarily checked by stack
scanning of sleeping tasks (requires `HAVE_RELIABLE_STACKTRACE`), falling back to switching tasks at kernel
exit; transitions normally converge "within seconds" and can be monitored via `/sys/kernel/livepatch/*/transition`,
or forced — with the doc's own warning that unauthorized forcing "may cause harm to the system" [1].

Lineage matters here because each distro descends from a different ancestor:

- **Ksplice** (MIT → Oracle, 2009) operates at the **object-code layer**: pre/post differencing of compiled
  objects plus *run-pre matching* to resolve symbols and prove the running kernel matches expectations. In the
  paper's evaluation over **all 64 significant x86-32 Linux kernel security vulnerabilities from May 2005 to
  May 2008**, "56 of 64 require no new code" — i.e., **Ksplice can correct 88% of kernel vulnerabilities
  without rebooting**, with ~17 lines of helper code each for the rest, interrupting normal operation for only
  **~0.7 ms** (its `stop_machine` window) [2]. It became Oracle-only after the 2011 acquisition, powering
  Oracle Linux's rebootless updates (Ksplice client code itself was later re-opened for updating purposes;
  the *generation* side stays with Oracle — the canonical reference remains the EuroSys paper) [2].
- **kpatch** (Red Hat) is "a Linux dynamic kernel patching infrastructure which allows you to patch a running
  kernel without rebooting or restarting any processes": `kpatch-build` diffs pre/post compiled kernels, and
  the resulting patch module registers with the kernel's `CONFIG_LIVEPATCH` infra, redirecting functions via
  **ftrace**. Notably, the README states that starting with **Linux 6.19 kpatch is deprecated and in
  maintenance mode**, with its build tooling being replaced by `klp-build` in the upstream kernel — live
  patching is being absorbed into mainline [3].
- **SUSE** ships KLP as a subscription ("SLE Live Patching"): "Kernel Live Patching (KLP) makes it possible to
  apply the latest security updates to Linux kernels without rebooting"; cumulative `kernel-livepatch-*`
  packages cover CVSS 7+ fixes, and SUSE reports "**over 95% of qualifying fixes are released as live
  patches**" — fixes requiring data-structure changes still need a reboot, and live patches are explicitly a
  bridge "until a proper kernel update and a reboot are performed" [4].
- **Canonical Livepatch** (Ubuntu Pro) "shrinks the exploit window for critical and high severity Linux kernel
  vulnerabilities" by patching between maintenance windows, with a livepatch + security notice issued per CVE
  and automatic application by enabled clients; it covers kernel code only (not userspace libraries) and "is
  not a replacement for rebooting" [5].

The shared limitation is instructive: **all live-patchers refuse (or require hand-written patch code for)
semantic changes to persistent data structures** [1], [2] — the same boundary that makes dynamic software
update hard in general (Gupta 1996 proved transition-function verification undecidable in general, as cited
in [2]).

### 2. Process supervision: restart, watchdog, and the parent-death signal

systemd turned supervision into declarative policy. Lennart Poettering's classic post [7] lays out the
two-level scheme: systemd itself pings the **hardware watchdog** (`RuntimeWatchdogSec=`, pings at half the
interval; `ShutdownWatchdogSec=` guards reboots) so "the hardware watches systemd, and systemd watches every
service"; and per-service **software watchdogs** — a daemon reads `WATCHDOG_USEC=` from the environment and
"issue[s] `sd_notify("WATCHDOG=1")` calls every half of that interval"; if pings stop, systemd marks the unit
failed and restart policy takes over (`Restart=on-failure` + `StartLimitBurst=`/`StartLimitInterval=`, with
`StartLimitAction=` able to escalate to `reboot-force`) [7]. The `sd_notify(3)` man page defines `WATCHDOG=1`
as "the keep-alive ping that services need to issue in regular intervals if `WatchdogSec=` is enabled" [8].
This is a textbook detect–decide–act loop: the *service itself* is the health sensor, the supervisor is the
actuator.

The kernel-side counterpart is the **watchdog driver API**: "the watchdog activates as soon as /dev/watchdog
is opened and will reboot unless the watchdog is pinged within a certain time"; a normal close disables it,
unless **Magic Close** is supported (the daemon must write `'V'` before closing — anything else is treated as
a dead daemon, so the box reboots) or `CONFIG_WATCHDOG_NOWAYOUT` is set, in which case "there is no way of
disabling the watchdog once it has been started" [10]. This is the embedded tradition: minimal, brutal,
reboot-as-repair.

Two finer-grained primitives complete the picture: `PR_SET_PDEATHSIG` delivers a chosen signal to a child
"when its parent dies" — with the classic trap that "the 'parent' is the creating *thread*", so the signal
fires when the parent's thread exits even if the process lives on; it is also cleared across setuid/capability
`execve` [6]. And when the *system* runs out of memory, the **OOM killer** scores every task
(`oom_badness()`, mostly RSS + swap + page tables) and kills the highest-scoring victim; user space steers it
with `/proc/<pid>/oom_score_adj`, where "acceptable values range from -1000 … to +1000", the value "is added
to the badness score", and −1000 "is equivalent to disabling OOM-killing entirely for that task" [12]. Trade-
off: it is a *last-resort* healer that amputates by heuristic — the alternative designs (fail the allocation,
reboot) are worse for availability but more predictable, which is why memory-critical services either pin
`oom_score_adj` or pre-reserve via cgroups.

### 3. Panic, dump, reboot: healing the unhealable kernel fault

When the kernel itself dies, healing = fast, *informative* restart. The `kernel.panic` sysctl defines the
policy: "if zero, the kernel will loop forever; if negative, the kernel will reboot immediately; if positive,
the kernel will reboot after the corresponding number of seconds" (60 recommended when using the software
watchdog); `panic_on_oops=1` converts any oops into a panic, and `oops_limit` (default 10000) panics after N
oops so a flapping kernel self-terminates rather than limping corrupt [16]. **kdump/kexec** then makes the
reboot diagnostic: "Kdump uses kexec to quickly boot to a dump-capture kernel whenever a dump of the system
kernel's memory needs to be taken"; the crashed kernel's memory is preserved across the kexec reboot, exposed
as `/proc/vmcore`, and analyzable with gdb/crash; triggers live in `panic()`, `die()`, `die_nmi()` and the
sysrq handler (test with `echo c > /proc/sysrq-trigger`) [11]. Pair `panic=N` + kdump and a kernel panic
becomes a bounded MTTR event with a corpse to autopsy — the systems version of "crash-only software".

### 4. EDAC/ECC, machine checks, and page offlining: the hardware–kernel repair path

The kernel's EDAC subsystem classifies memory errors as corrected (CE), uncorrectable-non-fatal (UE),
**deferred** ("an uncorrectable error whose handling is not urgent" — hardware poisoning lets the system run
until the bad data is touched, "preemptive steps like offlining pages may be taken"), and fatal; ECC modes
range from parity to SECDED ("Single bit error correction, Double detection") to chipkill [13]. On x86,
uncorrected machine checks "typically cause a machine check (often with panic), corrected ones cause a
machine check log entry" read from `/dev/mcelog` by banks per CPU [15]. The userspace healing agent is
**mcelog/rasdaemon**, which buckets errors "per DIMM / per Channel / per memory controller / per Socket /
per Page — this is used to automatically offline bad pages" [14]: repeated CEs on the same page trigger
*soft offlining* — migrate contents to a fresh page, poison the old one — a genuine predictive repair at the
page granularity, decades before "AIOps" named the pattern. PostgreSQL's reliability chapter assumes exactly
this foundation: it "does not protect against correctable memory errors and it is assumed you will operate
using RAM that uses industry standard Error Correcting Codes (ECC)" [26].

### 5. eBPF: the sensing + actuation layer for a live kernel

eBPF lets you "safely and efficiently extend the capabilities of the kernel without requiring to change
kernel source code or load kernel modules"; the **verifier** "ensures that the eBPF program is safe to run"
— it must terminate, never touch uninitialized memory or read out of bounds, and cannot access arbitrary
kernel memory [17]. Why this matters for self-healing: it converts kernel observation and response from
"write a module and risk panicking the box" into a *safe, hot-loadable* capability — the sense→actuate loop
can run continuously in production. BCC's README quotes Ingo Molnár's framing of eBPF as "user-defined
instrumentation on a live kernel image that can never crash, hang or interfere with the kernel", and BCC
ships the sensor suite (`memleak`, `oomkill`, `runqlat`, `tcpretrans`, `ext4dist`, …) [18]; **bpftrace** is
the "high-level tracing language for Linux" making one-liner eBPF observability programs accessible [19].
On the actuation side, **Cilium** rebuilds K8s networking/security/observability on eBPF [20], and
**Tetragon** provides "flexible Kubernetes-aware security observability and runtime enforcement … directly
with eBPF": "synchronous monitoring, filtering, and enforcement are performed entirely within the kernel",
which "blocks malicious activities at the kernel level, closing the window for exploitation" and avoiding
TOCTOU races — e.g., killing or preventing execution from `/tmp` in real time [21]. That is a self-healing
*response* primitive with no reboot and no agent in the data path. (Caveat kept honest: eBPF is not a
live-patcher — it observes and filters events, it does not replace buggy kernel code.)

### 6. Self-healing storage and data

**ZFS** is the canonical self-healing filesystem: "Every read verifies the block's checksum", and on mismatch
a redundant pool (mirror/raidz/draid/`copies>1`) "fetch[es] a good copy and rewrite[s] the bad one"; without
redundancy, "checksums without a second copy only tell you what you have already lost". A **scrub** "walks
all data in the pool and verifies each block's checksum, repairing damage where redundancy allows", catching
latent bit rot "while it is still repairable" (monthly for consumer disks, quarterly enterprise cadence);
a **resilver** is the same machinery restricted to known-stale data (e.g., replaced drive), and CKSUM error
clusters often indict cabling, controllers, or RAM rather than disks [22]. Contrast with the **fsck** family:
`fsck` is "simply a front-end for the various filesystem checkers", running them in parallel across disks
with additive exit codes — offline repair after a crash, not continuous healing [24]; and with **md** software
RAID, whose `resync`/`recover` sync actions rebuild redundancy after unclean shutdown or disk replacement,
with `ppl` (Partial Parity Log) "used to close the write hole" — while a dirty+degraded RAID5/6 "could have
undetectable data corruption", which is precisely the class ZFS checksums catch and md parity cannot [25].
(This is the standard argument that ZFS wants direct disks, not a hardware RAID card hiding redundancy from
the checksum layer.)

**PostgreSQL** heals transactional state after any crash via WAL: committed data must reach nonvolatile
storage; **full-page writes** guard against torn pages ("during crash recovery PostgreSQL can restore
partially-written pages from WAL"); every WAL record carries a **CRC-32C** checksum "checked during crash
recovery, archive recovery and replication"; data-page checksums are on by default — the caveat being that
none of this survives lying hardware (write-back caches without batteries) [26]. **etcd/Raft** heals
*coordination* state: on leader failure "the etcd cluster … automatically elects a new leader" within roughly
an election timeout, uncommitted writes may drop but "no committed writes are ever lost"; a majority loss
makes the cluster read-only until quorum returns; after a partition "the minority side automatically
recognizes the leader from the majority side and recovers its state" [27]. Raft itself is the consensus
substrate: "multiple servers agree on values" with a majority — "5 servers can survive 2 failures" — keeping
replicated state machines consistent through leader election and log replication [28]. The pattern across all
three: **checkpointed intent log + idempotent replay + redundancy** = repair without a human.

## Prevention vs cure in systems code ("healing before the wound")

The cheapest self-healing is the bug that cannot exist. The empirical case is stark: MSRC reported in July
2019 that "the root cause of approximately 70% of security vulnerabilities that Microsoft fixes and assigns a
CVE … are due to memory safety issues" — "despite mitigations including intense code review, training, static
analysis, and more" [30]. Chromium independently found "around 70% of our high severity security bugs are
memory unsafety problems", about half of them use-after-free, and concluded the fix is source-level: adopt a
memory-safe language (Rust/Swift/…) rather than more sandboxing [31]. CISA repeated both figures in its 2023
call for memory-safety roadmaps [32]. The payoff is now measured: **Android**'s memory-safety share fell from
"76% of Android vulnerabilities in 2019" to "24% in 2024" — "well below the 70% industry norm" — correlating
"closely with the development language that's used for new code" (Rust), exploiting the fact that
vulnerability rates decay with code age, so *new* code in safe languages dominates the trend [33].

In-kernel prevention: **Rust for Linux** is "the project adding support for the Rust language to the Linux
kernel" (merged 6.1, 2022), with mainline Rust drivers listed on its hub — Android Binder, Nova and Tyr GPU
drivers, the null-block driver — plus out-of-tree users (Apple AGX GPU, NVMe, PuzzleFS) [34]; the kernel's
Rust quick-start notes CONFIG_RUST appears only when a suitable toolchain is found, with the complete LLVM
toolchain "the best supported setup" [35].

Runtime prevention and triage tooling: **AddressSanitizer** is a compiler-instrumentation + runtime-malloc
detector for "use after free, heap/stack/global buffer overflow … memory leaks" at ~2× average slowdown,
in-tree since LLVM 3.1 / GCC 4.8 — cheap enough to run in CI and even production canary classes (UBSan/TSan
cover UB and data races in the same family) [36]. Continuous fuzzing industrializes the finding side:
**OSS-Fuzz** (free Google service, launched post-Heartbleed 2016) reports 10,000+ vulnerabilities and 36,000+
bugs fixed across 1,000+ projects (Aug 2023 figures) [37], powered by **ClusterFuzz** — "a scalable fuzzing
infrastructure that finds security and stability issues in software", ~27,000 bugs in Google's own products,
running the OSS-Fuzz instance "on 100,000 VMs", with crash dedup, automated bug filing, testcase
minimization and regression bisection [38]. That triage/automation plumbing is what makes an *AI fixer*
attachable: a minimized repro + a bisection commit is exactly the context a repair model needs.

## Where AI is entering systems work (verified examples only)

### Pre-LLM era (2018–2022): learned repair and classical ML on incidents

- **Getafix (Facebook, 2018–19)** — "the first industrially-deployed automated bug-fixing tool that learns
  fix patterns" from past human fixes: hierarchical clustering + anti-unification mine abstract patterns
  with "holes", which are instantiated and ranked for new Infer null-safety warnings; on 1,268 real fixes the
  top suggestion matched the human patch 12–91% by bug category, and top-5 suggestions fixed 526/1,268 [40].
  In production: on ~2,000 Instagram null-method-call bugs it "successfully automatically patched 1,077
  (about 53 percent)"; ~80% of its candidate fixes passed all tests, and it supplied about half of SapFix's
  valid candidates [39].
- **SapFix (Facebook, 2018)** — automated *end-to-end* repair for Sapienz-found crashes: revert, templated
  fixes, or AST mutation strategies; autonomous validation (compile, crash gone, no new crashes, tests pass);
  then a human reviewer — "SapFix can't implement its own proposed fixes" — and Meta called it "the first
  time that a machine-generated fix — with automated end-to-end testing and repair" was deployed at Facebook
  scale, with patches landing in the Facebook Android app [41]. (The companion ICSE'19 SEIP paper by
  Marginean et al. exists; its arXiv ID could not be verified and is deliberately not cited [UNVERIFIED: arXiv
  ID].)
- **DeepCT / incident triage ML (Microsoft, 2019)** — Junjie Chen et al., "Continuous Incident Triage for
  Large-Scale Online Service Systems" (ASE 2019, DOI 10.1109/ASE.2019.00042 as printed in [42]'s
  bibliography) — CNN/GRU triage of incidents, the pre-LLM baseline later beaten by Triangle. This is the
  real paper behind vague references to "Chen et al. on incident triage"; **"SuperHELM" does not appear to
  exist** [UNVERIFIED].
- **Predictive mitigation (Microsoft Azure, 2020–22)** — e.g., Levy et al., "Predictive and Adaptive Failure
  Mitigation to Avert Production Cloud VM Interruptions" (OSDI'20) and RESIN for memory-leak mitigation in
  production (OSDI'22) — both corroborated via the bibliography of [42]; *titles/venues verified there, URLs
  not individually fetched.*
- **Netflix ML for streaming quality (2018)** — device anomaly detection across 1,000+ device types: a model
  trained on human-labeled alert outcomes "predict[s] the likelihood that a given set of measured conditions
  constitutes a real problem", with statistical covariate control separating ISP vs. firmware vs. A/B causes,
  yielding "large reductions in overall alert volume" at acceptable false-negative rates [43].
- **Kernel-fuzzing infrastructure intelligence (2018)** — Moonshine (USENIX Security'18) distilled 2.8M real
  syscalls into seeds preserving call dependencies, improving Syzkaller's kernel coverage ~13% and finding 14
  unknown kernel bugs — the intelligence here is program analysis, not learning, but it is the substrate
  LLM-fuzzers build on [44].

### LLM era (2023–2026): agents that fuzz, triage, diagnose — and, carefully, patch

- **AI-powered fuzzing (Google OSS-Fuzz, 2023–24)** — LLMs write and repair fuzz targets end-to-end
  (oss-fuzz-gen, open-sourced Jan 2024; max line-coverage gain +29% over human targets, 30 bugs, 160 projects
  at first report) [45]. By Nov 2024: automated coverage gains in 272 C/C++ projects, +370k lines covered
  (one project 77 → 5,434 lines), **26 new vulnerabilities** including **CVE-2024-9143 in OpenSSL**, "likely
  present for two decades and … not discoverable with existing fuzz targets written by humans"; the LLM now
  executes the first four steps of the developer workflow (draft, fix compile errors, fix runtime issues,
  triage crashes — correctly blaming the fuzz driver vs. the project), with agent-based patch generation
  named as the next step [46].
- **From finding to fixing (Google, July 2026)** — OSS-Fuzz combined with **CodeMender**, "Google DeepMind's
  advanced AI agent for automated code security": "instead of just reporting a security issue, OSS-Fuzz's
  automated pipeline works to find the root cause, develop a fix, and deliver a high quality patch" — while
  honoring projects' AI-contribution policies (withholding patches where restricted) because "open source
  maintainers are overwhelmed with AI submissions"; during beta "Google engineers personally review proposed
  patches" [47]. This is the closest thing today to a closed sense→diagnose→patch loop in infrastructure code.
- **Big Sleep (Project Zero + DeepMind, Oct 2024)** — an LLM agent performing variant analysis found "an
  exploitable stack buffer underflow in SQLite" — "the first public example of an AI agent finding a
  previously unknown exploitable memory-safety issue" in real-world software, a bug that remained
  "undiscovered after 150 CPU-hours" of targeted fuzzing; authors caveat these are "highly experimental
  results" [48].
- **KernelGPT (ASPLOS'25)** — LLMs "automatically infer the [syzlang syscall] specifications, and further
  debug and repair them based on validation feedback" for Syzkaller; "24 new unique bugs in Linux kernel,
  with 12 fixed and 11 assigned with CVE numbers", and generated specs already merged upstream into
  Syzkaller [49]. (Names circulating in this space such as "KernelBiologist" could not be found anywhere
  **[UNVERIFIED]**.)
- **RCACopilot (Microsoft, EuroSys'24 / arXiv 2023)** — LLM-powered on-call copilot that matches incidents to
  handlers, extracts evidence, and "predicts the incident's root cause category", reaching RCA accuracy up to
  0.766 on a year of real Microsoft incidents; its evidence-collection component "has been successfully in
  use at Microsoft for over four years" [50].
- **Triangle (Microsoft + Tsinghua, FSE'25)** — multi-LLM-agent end-to-end incident triage: semantic
  distillation of heterogeneous incident text, per-team "Team Manager" agents that query monitoring databases
  to enrich context, and a voting/negotiation loop across team agents (max 5 hops). On 15 months of
  production data from a system serving tens of millions of users: hop-1 triage accuracy 54.7% vs. 43.4% for
  the pre-LLM SOTA (DeepCT), 91.7% by hop 5, time-to-engage reduced by 24.58 "time units" vs. manual triage;
  deployed in production [42].
- **SWE-InfraBench (2026)** — reality check for agent capability on *infrastructure-as-code*: LLM agents
  editing real AWS CDK repositories from natural-language instructions pass the tests only 34% of the time
  (best model, Sonnet 3.7; DeepSeek R1 24%) — "even state-of-the-art systems struggle with many tasks" [51].
- **Getafix/SapFix lineage, revisited** — worth stressing that the 2018 Facebook pipeline already had every
  component of the 2026 loop (detector → localizer → patch generator → validator → human gate → deploy);
  the LLM era's genuinely new contributions are natural-language incident channels, transfer to arbitrary
  codebases without mined fix history, and tool-using agents (debuggers, monitors, syzlang) [39]–[42], [46].

## Key numbers

- **88%** — share of the 64 significant x86-32 Linux kernel security vulns (2005–2008) Ksplice could hot-patch with zero new code; **~0.7 ms** stop-machine cost [2].
- **>95%** — qualifying SUSE kernel fixes shipped as live patches; live patches cover CVSS 7+ and are a bridge until reboot [4].
- **~70%** — Microsoft CVEs that are memory-safety issues (MSRC, 2019), "despite mitigations" [30]; **~70%** of Chromium high-severity security bugs, ~half use-after-free [31]; both repeated by CISA [32].
- **76% → 24%** — Android vulnerabilities that were memory-safety issues, 2019 → 2024, attributed to Rust for new code [33].
- **10,000+ / 36,000+ / 1,000+** — OSS-Fuzz vulnerabilities / bugs fixed / projects (Aug 2023) [37]; ClusterFuzz: ~27,000 bugs in Google, OSS-Fuzz instance "runs on 100,000 VMs" [38].
- **26 new vulns, 272 projects, +370k LOC covered** — AI-generated fuzz targets by Nov 2024, incl. CVE-2024-9143 (OpenSSL, ~2 decades old); one project went 77 → 5,434 covered lines; +29% max line-coverage gain per oss-fuzz-gen [45], [46].
- **1,077 of ~2,000 (53%)** — Instagram null-call bugs auto-patched by Getafix in one experiment; ~80% of its candidates passed all tests; paper: top-1 exact-match 12–91% by category, top-5 fixed 526/1,268 [39], [40].
- **54.7% vs 43.4% / 91.7% vs 67.6% / −24.58 units** — Triangle vs. DeepCT incident-triage accuracy (hop-1 and hop≤5) and time-to-engage reduction; deployed at tens of millions of users [42]. RCACopilot RCA accuracy up to **0.766** [50].
- **24 bugs / 11 CVEs** — KernelGPT's LLM-generated syscall specs for Syzkaller; specs merged upstream [49].
- **34% / 24%** — best-agent solve rates on cloud IaC tasks (SWE-InfraBench, 2026) [51].
- **0.766** — RCACopilot root-cause-category accuracy on a year of Microsoft incidents [50].
- **150 CPU-hours** — fuzzing that failed to find the SQLite zero-day Big Sleep's agent found (Oct 2024) [48].
- **~2×** — ASan average slowdown; the price of memory-bug visibility in CI [36].
- **10000** — default `oops_limit` before a flapping kernel panics itself [16].

## Canonical references

1. [1] Livepatch — The Linux Kernel Documentation, 2024 — https://docs.kernel.org/livepatch/livepatch.html (accessed 2026-11-09)
2. [2] Ksplice: Automatic Rebootless Kernel Updates — Jeff Arnold & M. Frans Kaashoek, MIT (EuroSys 2009) — https://ksplice.oracle.com/doc/ksplice.pdf (accessed 2026-11-09)
3. [3] kpatch — dynup/kpatch README — https://github.com/dynup/kpatch (accessed 2026-11-09)
4. [4] Kernel Live Patching on SUSE Linux Enterprise Server — SUSE — https://documentation.suse.com/smart/systems-management/html/klp/index.html (accessed 2026-11-09)
5. [5] Canonical Livepatch Service — Canonical/Ubuntu — https://ubuntu.com/security/livepatch (accessed 2026-11-09)
6. [6] PR_SET_PDEATHSIG(2const) — Linux man-pages project — https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html (accessed 2026-11-09)
7. [7] systemd for Administrators, Part XV: Watchdogs — Lennart Poettering, 2012 — https://0pointer.net/blog/projects/watchdog (accessed 2026-11-09)
8. [8] sd_notify(3) — systemd — https://man.archlinux.org/man/sd_notify.3 (accessed 2026-11-09)
9. [9] The Linux Watchdog Driver API — kernel.org — https://www.kernel.org/doc/html/latest/watchdog/watchdog-api.html (accessed 2026-11-09)
10. [10] Watchdog Support index — kernel.org — https://www.kernel.org/doc/html/latest/watchdog/ (accessed 2026-11-09)
11. [11] Documentation for Kdump: The kexec-based Crash Dumping Solution — kernel.org — https://docs.kernel.org/admin-guide/kdump/kdump.html (accessed 2026-11-09)
12. [12] proc_pid_oom_score_adj(5) — Linux man-pages project — https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html (accessed 2026-11-09)
13. [13] EDAC Devices — Linux Kernel Documentation — https://www.kernel.org/doc/html/latest/driver-api/edac.html (accessed 2026-11-09)
14. [14] mcelog: Memory Errors — mcelog.org — https://www.mcelog.org/memory.html (accessed 2026-11-09)
15. [15] Machine Checks — Linux Kernel Documentation (x86) — https://docs.kernel.org/arch/x86/x86_64/machinecheck.html (accessed 2026-11-09)
16. [16] Sysctl: /proc/sys/kernel — kernel.org — https://docs.kernel.org/admin-guide/sysctl/kernel.html (accessed 2026-11-09)
17. [17] What is eBPF? — ebpf.io / Cilium project — https://ebpf.io/what-is-ebpf/ (accessed 2026-11-09)
18. [18] BCC (BPF Compiler Collection) — iovisor — https://github.com/iovisor/bcc (accessed 2026-11-09)
19. [19] bpftrace — bpftrace.org — https://bpftrace.org/ (accessed 2026-11-09)
20. [20] Cilium Documentation — Cilium — https://docs.cilium.io/en/stable/ (accessed 2026-11-09)
21. [21] Tetragon — Cilium/tetragon — https://tetragon.io/ (accessed 2026-11-09)
22. [22] Scrub and Resilver — OpenZFS Documentation — https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Operations/Scrub%20and%20Resilver.html (accessed 2026-11-09)
23. [23] File System Check — fsck(8) — Linux man-pages project — https://man7.org/linux/man-pages/man8/fsck.8.html (accessed 2026-11-09)
24. [24] RAID (md) — kernel.org — https://docs.kernel.org/admin-guide/md.html (accessed 2026-11-09)
25. [25] ZFS vs md-raid comparison is a synthesis of [22] and [24]; see also the OpenZFS Checksums wiki (not independently fetched) [secondary]
26. [26] Reliability and the Write-Ahead Log — PostgreSQL 28 Documentation — https://www.postgresql.org/docs/current/wal-reliability.html (accessed 2026-11-09)
27. [27] Failure Modes — etcd v3.5 docs — https://etcd.io/docs/v3.5/op-guide/failures/ (accessed 2026-11-09)
28. [28] Raft (In Search of an Understandable Consensus Algorithm) — raft.github.io — https://raft.github.io/ (accessed 2026-11-09)
29. [29] ELISA: Enabling Linux in Safety Applications — The Linux Foundation — https://elisa.tech/ (accessed 2026-11-09)
30. [30] We Need a Safer Systems Programming Language — MSRC (Ryan Levick, Sebastian Fernandez), 2019 — https://web.archive.org/web/2024/https://msrc.microsoft.com/blog/2019/07/we-need-a-safer-systems-programming-language/ (accessed 2026-11-09; original msrc.microsoft.com URL now redirects)
31. [31] Memory Safety — Chromium Security — https://www.chromium.org/Home/chromium-security/memory-safety/ (accessed 2026-11-09)
32. [32] The Urgent Need for Memory Safe Software Products — CISA, 2023 — https://www.cisa.gov/news-events/news/urgent-need-memory-safety-software-products (accessed 2026-11-09)
33. [33] Eliminating Memory Safety Vulnerabilities at the Source — Google (Android Security), 2024 — https://security.googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html (accessed 2026-11-09)
34. [34] Rust for Linux — RFL project — https://rust-for-linux.com/ (accessed 2026-11-09)
35. [35] Rust Quick Start — Linux Kernel Documentation — https://docs.kernel.org/rust/quick-start.html (accessed 2026-11-09)
36. [36] AddressSanitizer — google/sanitizers wiki — https://github.com/google/sanitizers/wiki/AddressSanitizer (accessed 2026-11-09)
37. [37] OSS-Fuzz Documentation — Google — https://google.github.io/oss-fuzz/ (accessed 2026-11-09)
38. [38] ClusterFuzz — google/clusterfuzz — https://github.com/google/clusterfuzz (accessed 2026-11-09)
39. [39] Getafix: How Facebook Tools Learn to Fix Bugs Automatically — Meta Engineering, 2018 — https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/ (accessed 2026-11-09)
40. [40] Getafix: Learning to Fix Bugs Automatically — Bader, Scott, Pradel, Chandra (arXiv:1902.06111, Onward!/SPLASH 2019) — https://arxiv.org/abs/1902.06111 (accessed 2026-11-09)
41. [41] Finding and Fixing Software Bugs Automatically with SapFix and Sapienz — Meta AI, 2018 — https://ai.meta.com/blog/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz/ (accessed 2026-11-09)
42. [42] Triangle: Empowering Incident Triage with Multi-LLM-Agents — Yu, Ma, et al. (Microsoft/Tsinghua, FSE 2025) — https://www.microsoft.com/en-us/research/wp-content/uploads/2025/02/TRIANGLE_FSE25.pdf (accessed 2026-11-09)
43. [43] Using Machine Learning to Improve Streaming Quality at Netflix — Netflix Technology, 2018 — https://netflixtechblog.com/using-machine-learning-to-improve-streaming-quality-at-netflix-9651263ef09f (accessed 2026-11-09)
44. [44] Optimizing OS Fuzzer Seed Selection with Trace Distillation (Moonshine) — Pailoor, Aday, Jana (USENIX Security 2018) — https://www.usenix.org/conference/usenixsecurity18/presentation/pailoor (accessed 2026-11-09)
45. [45] oss-fuzz-gen — google/oss-fuzz-gen — https://github.com/google/oss-fuzz-gen (accessed 2026-11-09)
46. [46] Leveling Up Fuzzing: Finding More Vulnerabilities with AI — Google Open Source Security Team, 2024 — https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html (accessed 2026-11-09)
47. [47] From Finding to Fixing: Reducing Maintainer Burden with Automated Patches — Google (Alex Kilian, Dustin Ingram), 2026 — https://blog.google/security/from-finding-to-fixing-reducing-maintainer-burden-with-automated-patches/ (accessed 2026-11-09)
48. [48] From Naptime to Big Sleep: Using Large Language Models To Catch Vulnerabilities In Real-World Code — Google Project Zero / DeepMind, 2024 — https://projectzero.google/2024/10/from-naptime-to-big-sleep.html (accessed 2026-11-09)
49. [49] KernelGPT: Enhanced Kernel Fuzzing via Large Language Models — Yang, Zhao, Zhang (ASPLOS 2025, arXiv:2401.00563) — https://arxiv.org/abs/2401.00563 (accessed 2026-11-09)
50. [50] Automatic Root Cause Analysis via Large Language Models for Cloud Incidents (RCACopilot) — Yinfang Chen et al. (EuroSys 2024, arXiv:2305.15778) — https://arxiv.org/abs/2305.15778 (accessed 2026-11-09)
51. [51] SWE-InfraBench: Evaluating Language Models on Cloud Infrastructure Code — Tarasova et al., 2026 — https://arxiv.org/abs/2606.05249 (accessed 2026-11-09)

Additional primary sources cited in text but not numbered above: Kdump trigger details [11]; `sd_event_set_watchdog(3)` — freedesktop.org, 2024 — https://www.freedesktop.org/software/systemd/man/sd_event_set_watchdog.html (accessed 2026-11-09, existence confirmed via search listing; page not fully fetched [secondary]). DeepCT (Chen et al., ASE 2019, DOI 10.1109/ASE.2019.00042) and RESIN/Levy et al. (OSDI'20/'22) verified via the bibliography of [42] [secondary].

## Open questions

1. **Who closes the loop, and who is liable?** Google's CodeMender pipeline gates AI patches behind engineer review during beta; Meta's SapFix did the same in 2018. Does any principal operator today let an AI *auto-deploy* a fix to kernel-adjacent production code without a human gate — and what incident data would justify flipping that switch?
2. **Can LLM agents live-patch?** Live patching is bounded by "no semantic changes to data structures" [1], [2]. Can an agent reliably *classify* whether a given CVE patch is live-patchable (distros do this by hand today), and generate the transition code when it is not? No verified public system does this yet.
3. **eBPF actuation vs. repair:** eBPF observes and enforces, but cannot replace buggy kernel code. Is there a verified production case of an eBPF-based *mitigation* (e.g., Tetragon policy) deployed as an immediate response while a live patch was prepared — an automated two-stage heal?
4. **Does prevention actually shrink the healing workload?** Android's 76%→24% is per-language-cohort evidence [33]; nobody has published the equivalent "incident tax" delta for, e.g., Rust drivers in the Linux kernel. Rust-for-Linux is now past the "experimental" phase per its maintainers — incident-rate data would settle the cost-benefit argument.
5. **Watchdog staleness:** hardware watchdogs detect hangs, not *wrongness* (a kernel that pings happily while corrupting data passes). Distributed "software watchdogs" (etcd leases, Raft elections) check liveness-by-participation — is there a verified unification of health *checking* with health *proving* (attestation, consensus on observed state) in the embedded/safety world (ELISA-adjacent)?
6. **Benchmark mismatch:** SWE-bench-style agents reach 34% on IaC tasks [51], yet OSS-Fuzz's agents find 20-year-old OpenSSL bugs [46]. Why do agents excel at *finding* in systems code but still struggle with *routine* infrastructure edits — is it the natural-language spec, the blast-radius asymmetry, or the test signal quality?
7. **Attribution hygiene:** "SuperHELM" and "KernelBiologist" circulate in AI-for-systems discussions but leave no verifiable trace **[UNVERIFIED]**. The field needs the discipline of citing deployed systems by paper/blog (Triangle, RCACopilot, KernelGPT, oss-fuzz-gen) rather than folklore names.
