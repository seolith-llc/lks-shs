# 01 · Academic Foundations of Self-Healing Software

**Scope note.** This dossier maps the intellectual lineage of "self-healing software with AI" for the lks-shs project (#Step001, academic-foundations workstream). It traces three converging streams: (1) classic fault tolerance and recovery (redundancy, checkpointing, N-version programming, transactions, Byzantine tolerance, self-stabilization), (2) the autonomic- and self-adaptive-software movement born of IBM's 2001 manifesto (MAPE-K, SEAMS, models@run.time, Rainbow, control-theoretic adaptation, runtime verification), and (3) automated program repair from its genetic-programming origins through semantic repair into the LLM-agent era benchmarked by SWE-bench. Every citation below was verified by fetching the cited page, DOI resolution, or the Crossref API on 2026-11-09; anything not directly verifiable is explicitly marked [UNVERIFIED]. Corrections to the task brief's assumptions are flagged inline (notably: AlphaRepair is by Xia & Zhang, not "Tu et al."; Salehie & Tahvildari's survey was published in ACM TAAS 2009, not IEEE TSE 2007; Ghosh et al.'s self-healing survey is in Decision Support Systems, not ACM CSUR).

---

## TL;DR

- **Self-healing is older than AI.** Redundancy voting (1956), recovery blocks (1975), N-version programming (1985), WAL-based transaction recovery (1993), Byzantine fault tolerance (1999), and self-stabilization (1974) all treat "healing" as *design-time provision of recovery mechanisms*, not runtime intelligence [10][11][12][14][15][9].
- **The 2001 IBM manifesto reframed healing as autonomy.** Horn argued system complexity was outpacing human administration; Kephart & Chess (2003) operationalized this as the four self-* properties and the MAPE-K loop that still structures the field [1][2].
- **"Healing" decomposes into detect → diagnose → recover → (learn).** This decomposition is stable across all three eras — the fault-tolerance classics, MAPE-K autonomic managers, and modern LLM repair agents all implement some subset of it [2][3][30].
- **A dedicated research community exists.** WOSS '02 (first Workshop on Self-Healing Systems) became SEAMS (ICSE workshop 2006, symposium since 2011), plus the models@run.time workshop series and ACM TAAS [7][3].
- **Rainbow (2004) is the canonical architecture-based self-adaptation framework**: monitor an architectural model at runtime, detect constraint violations, decide via utility theory (Stitch), execute tactics — a literal MAPE-K instance [5].
- **Automated Program Repair went search-based → semantic → neural → agentic.** GenProg fixed 55/105 real bugs for ~$8 each (2012); SemFix (2013) brought symbolic execution; AlphaRepair (2022) brought zero-shot cloze-style LLM repair [16][17][19].
- **SWE-bench (ICLR 2024) reset the field's scoreboard**: given a repo and a GitHub issue, generate a patch that passes the repo's tests. Best models at release solved **1.96%**; by 2026 the leaderboard median sits at **76.2%** with SOTA **87.6%** [21][29].
- **The 2024 "agentic vs. agentless" debate** showed a fixed localize→repair→validate pipeline (Agentless, 32.00% on SWE-bench Lite at $0.70/task) could match elaborate agents at a fraction of cost [24].
- **SWE-bench itself was audited**: 68.3% of original samples were filtered out (underspecified statements 38.3%, unfair tests 61.1%) to create the 500-instance human-validated "Verified" split [22].
- **Runtime verification supplies the "detect" half** of any healing loop: lightweight formal monitoring of execution traces against property specifications, with a mature theory (Leucker & Schallhart) and tool ecosystem [32].
- **The survey literature is thinner than expected.** The dedicated "self-healing systems" surveys live in Decision Support Systems (Ghosh et al. 2007) and Computing (Psaier & Dustdar 2011), not primarily in IEEE TSE/ACM CSUR; the CSUR anchor for the area is Huebscher & McCann's autonomic-computing survey (2008) [30][31][4].
- **Corrections to the brief**: AlphaRepair = Xia & Zhang (ESEC/FSE 2022) [19]; Salehie & Tahvildari = ACM TAAS 4(2) 2009, received May 2007 [3]; an "IEEE TSE 2018 self-healing survey" could not be verified and is treated as [UNVERIFIED].

---

## Timeline: ideas before AI → AI era

| Year | Milestone | Why it matters | Ref |
|---|---|---|---|
| 1956 | von Neumann, *Probabilistic Logics* — majority voting over redundant components (origin of TMR) | Reliability can be *synthesized* from unreliable parts; hardware ancestor of all redundancy-based healing | [10] |
| 1974 | Dijkstra, *Self-Stabilizing Systems in Spite of Distributed Control* (CACM 17(11)) | Any starting state converges to a legitimate state with only local decisions — "self-healing" before the term existed | [9] |
| 1975 | Randell, *System Structure for Software Fault Tolerance* (IEEE TSE) — recovery blocks | Backward error recovery for *software* design faults: acceptance test + alternates + rollback | [11] |
| 1975 | Goodenough, *Exception Handling: Issues and a Proposed Notation* (CACM) | First systematic theory of signaling/handling abnormal conditions in programs | [13] |
| 1985 | Avizienis, *The N-Version Approach to Fault-Tolerant Software* (IEEE TSE) | Design diversity + voting as the software analog of TMR | [12] |
| 1993 | Gray & Reuter, *Transaction Processing* — write-ahead logging, undo/redo | Industrial-strength automatic recovery: the database as the first mass-market self-healing system | [15] |
| 1999 | Castro & Liskov, *Practical Byzantine Fault Tolerance* (OSDI '99) | 3f+1 replicas tolerate arbitrary faults with modest overhead (BFT NFS ran ~3% slower than unreplicated) — healing via replication, alive today in blockchains | [14] |
| 2001 | Horn, *Autonomic Computing* manifesto (IBM) | Complexity crisis framing; systems must manage themselves | [1] |
| 2002 | WOSS '02 — first ACM Workshop on Self-Healing Systems | Field gets its name and venue; Garlan & Schmerl present model-based adaptation for self-healing | [3][30] |
| 2003 | Kephart & Chess, *The Vision of Autonomic Computing* (IEEE Computer) | MAPE-K loop + four self-* properties; ~7,000 citations | [2] |
| 2004 | Garlan et al., *Rainbow* (IEEE Computer 37(10)); Hellerstein et al., *Feedback Control of Computing Systems* (Wiley) | Reusable architecture-based adaptation loop; control theory applied to software management | [5][8] |
| 2006 | First SEAMS workshop (ICSE, Shanghai) | Institutionalization; becomes a symposium in 2011 | [7] |
| 2007 | Ghosh, Sharman, Rao, Upadhyaya, *Self-healing systems — survey and synthesis* (Decision Support Systems) | The reference survey of pre-AI self-healing | [30] |
| 2008 | Huebscher & McCann autonomic computing survey (ACM CSUR 40(3)) | Systematic map of degrees, models, applications | [4] |
| 2009 | Salehie & Tahvildari landscape survey (ACM TAAS 4(2)); Blair/Bencomo/France *Models@run.time* (IEEE Computer); Leucker & Schallhart runtime-verification account (JLAP 78(5)) | Self-adaptation gets its taxonomy, its runtime-model paradigm, and its formal monitoring backbone | [3][6][32] |
| 2009–2012 | GenProg era: GP-based APR scales to real C programs; "Fixing 55 out of 105 bugs for $8 each" (ICSE 2012) | APR becomes an empirical science with cost accounting | [16] |
| 2013 | SemFix (ICSE): symbolic execution + constraint solving for patch synthesis | Semantic (not just search-based) repair | [17] |
| 2018 | Monperrus, *The Living Review on Automated Program Repair* (HAL) | Continuously updated map of the APR field | [18] |
| 2022 | AlphaRepair (ESEC/FSE 2022): zero-shot cloze-style repair with pretrained code models | Neural APR arrives; outperforms prior tools on Defects4J, 3.3× more fixes on Defects4J 2.0 | [19] |
| 2023–24 | SWE-bench (arXiv Oct 2023 → ICLR 2024): 2,294 real GitHub issues; best model solves 1.96% | Repository-level, test-verified repair becomes the benchmark of record | [21] |
| 2024 | SWE-agent 12.5% (NeurIPS); Agentless 32.00% Lite at $0.70/task; AutoCodeRover 19% Lite at $0.43/issue (ISSTA); SWE-bench **Verified** (500 human-validated tasks, Aug 13); GPT-4o = 33.2% Verified | The agentic-software-engineering explosion | [23][24][25][22] |
| 2025 | RepairLLaMA (IEEE TSE): LoRA adapters beat GPT-4-class baselines on Defects4J v2; Claude Opus 4 / Sonnet 4 hit 72.5% / 72.7% Verified (May 22); Claude Opus 4.5 (Nov 24) tops Sonnet 4.5 by 4.3pp at high effort | Instruction-tuned repair models + frontier agents close in on human-level resolution | [20][27][28] |
| 2026 | LLM Registry (48 models): SWE-bench Verified median 76.2%, SOTA 87.6%; official leaderboard defaults to a bash-only mini-SWE-agent scaffold for comparability | Contamination and scaffold confounds become first-class concerns | [29][26] |

---

## Deep dives

### 1. Self-adaptive & self-managing software: the autonomic lineage

IBM's Paul Horn opened the era with an October 2001 "call to action": IT complexity (systems of tens of millions of lines) was outpacing human administrators, and computing should therefore regulate itself the way the autonomic nervous system regulates the body — with high-level objectives set by humans and low-level management automated [1]. Kephart & Chess turned the manifesto into a research agenda in *The Vision of Autonomic Computing* (IEEE Computer, Jan 2003): autonomic systems are self-configuring, self-healing, self-optimizing, and self-protecting, built from *autonomic managers* that run a **Monitor–Analyze–Plan–Execute loop over shared Knowledge (MAPE-K)** [2]. The MAPE-K loop is the single most reused blueprint in the field — every later "monitor-and-adapt" architecture (and arguably every SWE-bench agent that runs tests, reads output, edits code) is a MAPE-K descendant.

Salehie & Tahvildari's landscape survey (ACM TAAS 4(2), 2009 — received May 2007; note: the brief's "2007 survey" refers to this paper's submission year, not a TSE publication) frames self-adaptive software as *closing the loop*: monitor self and context, detect significant changes, decide, act — and organizes the field by the concerns *how / what / when / where* to adapt [3]. Huebscher & McCann's CSUR survey (2008) remains the standard map of autonomic computing "degrees, models, and applications" [4].

Concrete exemplars and paradigms:

- **Rainbow** (Garlan, Cheng, Huang, Schmerl, Steenkiste — IEEE Computer 37(10), 2004) is the canonical architecture-based self-adaptation framework: it maintains a runtime architectural model of the managed system, monitors it against constraints, uses utility theory (the Stitch language, Cheng et al.) to choose among adaptation tactics, and executes them — with reusable infrastructure evaluated on the Znn.com case study [5].
- **models@run.time** (Blair, Bencomo, France — IEEE Computer 42(10), 2009): keep an abstract, *causally connected* self-representation of the running system so reasoning about change happens at the model level; this underpins both Rainbow-style adaptation and modern digital-twin ideas [6].
- **Community**: WOSS '02 (first Workshop on Self-Healing Systems, ACM) seeded the venue; SEAMS began as an ICSE workshop in 2006 (Shanghai) and became a symposium in 2011; ACM TAAS is the field's journal; the self-adaptive.org site anchors the community (books, SEAMS, models@run.time workshops) [7][3].
- **Feedback control in software**: Hellerstein, Diao, Parekh & Tilbury's *Feedback Control of Computing Systems* (Wiley-IEEE, 2004) imported classical control theory (setpoints, controllers, stability) for computing resources — the "control-theoretic adaptation" thread (IBM's database-server and web-server controllers) treats self-management as regulation, complementing the AI/planning thread [8].

### 2. Fault tolerance & recovery classics: the intellectual bedrock

Everything autonomic computing calls "self-healing" descends from a small set of mechanisms engineered long before machine learning:

- **Redundancy & voting.** von Neumann (1956) proved reliable organisms can be synthesized from unreliable components via triplication and majority voting — the origin of TMR, later engineered into real computers by Lyons & Vanderkulk (IBM Journal, 1962) [10].
- **Checkpoint/rollback & recovery blocks.** Randell (IEEE TSE, 1975) structured software fault tolerance as primary block + acceptance test + alternates, rolling back state between attempts — the intellectual root of checkpoint/restart in modern clusters and of retry-based healing [11]. Transaction systems industrialized this: Gray & Reuter's *Transaction Processing* (1993) codified write-ahead logging and undo/redo recovery, making ACID durability — automatic recovery after crash — a mass-market property [15].
- **Design diversity.** Avizienis's N-version programming (IEEE TSE, 1985): independently developed functionally equivalent versions + voter, i.e., TMR moved into software; the direct ancestor of ensemble/diversity ideas in modern AI repair (sampling many patches and validating) [12].
- **Exception-handling theory.** Goodenough (CACM, 1975) gave the first principled treatment of exceptions as a language mechanism — the fine-grained "detect and signal" layer under every healing loop [13].
- **Byzantine fault tolerance.** Castro & Liskov (OSDI '99) made arbitrary-fault tolerance practical: state-machine replication with 3f+1 replicas, ~3% slower than an unreplicated NFS in normal operation — the algorithmic core of "heal by outvoting faulty replicas," later the consensus layer of blockchains [14].
- **Self-stabilization.** Dijkstra (CACM 17(11), 1974, two pages) defined the strongest classical notion of self-healing: from *any* initial state (even corrupted by faults), a distributed protocol must reach a legitimate state in finite time using only local rules — his token-ring example founded a whole subfield of distributed computing [9].

The key conceptual divide: these classics provide **mechanisms** (redundancy, rollback, voting, logging, convergence) chosen at design time; they do not *diagnose novel faults* or *synthesize new fixes* at runtime. That gap is what autonomic computing named and what AI-era repair began to close.

### 3. Automated Program Repair: from genetic search to LLM agents

**Search-based era.** GenProg (Weimer, Nguyen, Le Goues, Forrest, ICSE 2009; systematic study ICSE 2012) represented patches as genetic-programming mutations (crossover of statements from elsewhere in the program) validated against the test suite; the 2012 study fixed **55 of 105 real bugs** in large C programs (PHP, gzip, Wireshark...) at an average of **~$8 per fix**, establishing APR as an empirical discipline with explicit cost accounting [16].

**Semantic era.** SemFix (Nguyen, Qi, Roychoudhury, Chandra — ICSE 2013) replaced stochastic search with symbolic execution + constraint solving: infer repair constraints from passing/failing tests, then *synthesize* a patch satisfying them (predecessor of Angelix) [17]. Monperrus's *Living Review on Automated Program Repair* (HAL, 2018–) continuously catalogues the field, including its central problem — **patch overfitting** to the validating tests [18].

**Neural era.** AlphaRepair (Xia & Zhang — ESEC/FSE 2022; *note: the brief's "Tu et al." attribution is incorrect — the authors are Chunqiu Steven Xia and Lingming Zhang, UIUC*) was the first cloze-style, zero-shot APR technique: mask the buggy line, let a pretrained code model (CodeBERT/CodeT5 class) fill it, no task-specific training. It outperformed state-of-the-art APR on Defects4J and fixed **3.3× more bugs** than the best baseline on Defects4J 2.0 [19]. RepairLLaMA (Silva, Fang, Monperrus — IEEE TSE 2025; arXiv Dec 2023) showed parameter-efficient fine-tuning (LoRA-style "repair adapters") of open LLMs beats GPT-4-class baselines — **144 bugs fixed on Defects4J v2**, plus 109 on HumanEval-Java and 20 on GitBug-Java [20].

**Benchmark & agent era.** SWE-bench (Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan — ICLR 2024) made repair repository-scale: 2,294 issue/PR pairs from 12 Python repos; a solution must produce a patch passing FAIL_TO_PASS and PASS_TO_PASS tests. At release, the best system (Claude 2 with retrieval) resolved **1.96%** — the paper's headline finding of a massive capability gap [21]. The scaffold race followed:

- **SWE-agent** (Yang et al., NeurIPS 2024): a GPT-4 agent over a purpose-built *Agent-Computer Interface* (file navigation/edit/test commands designed for the model) resolved **12.5%** pass@1 on full SWE-bench — the "interface design matters" result [23].
- **Agentless** (Xia, Deng, Dunn, Zhang — arXiv Jul 2024; FSE/PACMSE 2025): a *fixed three-stage pipeline* — hierarchical localization → repair → patch validation — no autonomous planning, no tools; **32.00% on SWE-bench Lite (96 fixes)** at about **US$0.70 per task**, beating costlier agents and sparking the agents-vs-pipelines debate [24].
- **AutoCodeRover** (Zhang, Ruan, Fan, Roychoudhury — ISSTA 2024): AST-guided context retrieval + spectrum-based fault localization + LLM patching; **19% on SWE-bench Lite** at **US$0.43 per issue** in the original abstract [25].

**The Verified correction.** OpenAI + the SWE-bench authors audited the benchmark with 93 professional developers: **38.3%** of samples had underspecified problem statements, **61.1%** had unfair unit tests; **68.3%** of samples were filtered out, yielding **SWE-bench Verified (500 instances, released Aug 13, 2024)**. On it, GPT-4o resolved **33.2%** versus ~16% on the unaudited set — a cautionary tale about benchmark validity for any "healing" claim [22]. The official site now also hosts Lite (300), Multilingual (300, 9 languages), Multimodal (480) splits and evaluates everything under a standardized bash-only mini-SWE-agent scaffold [26].

**Progression of resolution rates (SWE-bench Verified unless noted).** 1.96% best-at-release (Claude 2, full set, 2023) [21] → 12.5% (SWE-agent/GPT-4, full set, May 2024) [23] → 33.2% (GPT-4o, Aug 2024) [22] → 49.0% (upgraded Claude 3.5 Sonnet, Oct 2024 — from 33.4% for the June version; figure corroborated via Anthropic's Oct 22, 2024 announcement and model-card addendum surfacing in search; direct page URL no longer resolves, treat URL as [UNVERIFIED]) → 72.5% Opus 4 / 72.7% Sonnet 4 (May 22, 2025) [27] → Claude Opus 4.5 (Nov 24, 2025): Anthropic reports beating Sonnet 4.5's best by **4.3pp at high effort** with 48% fewer output tokens (absolute score ≈80.9% per LLM Registry) [28][29] → **87.6%** SOTA (LLM Registry, accessed 2026-11-09; "Claude Opus 4.7" listed current SOTA; 48 models tracked, median 76.2%) [29]. Interpretation: within ~3 years, repository-level issue resolution went from a rounding error to near-saturation on the Verified split — while harder splits (e.g., SWE-bench Pro, where 2025 frontier models scored ~23% per LLM-Registry-adjacent reporting [UNVERIFIED for exact figure]) remain open.

### 4. Runtime verification & healing: the monitor-and-adapt loops

Runtime verification (RV) is the formal backbone of the "detect" stage: check a running system against a formal property by monitoring its execution traces — "lightweight formal verification." Leucker & Schallhart's *A brief account of runtime verification* (Journal of Logic and Algebraic Programming 78(5), 2009) is the standard reference, defining monitors synthesized from temporal-logic specifications [32]. (Note: the correct title is "a brief *account*," not "introduction" — corrected from the brief.)

RV plugs into healing in three ways, all visible in the literature:

1. **Monitor-and-adapt loops**: property violations trigger reconfiguration — Rainbow's constraint violations triggering Stitch tactics is exactly this pattern with architectural models as the specification [5].
2. **Control-theoretic adaptation**: treat the system as a plant with sensors and effectors; Hellerstein et al. (2004) built IBM-applied controllers for server throughput/latency regulation with stability guarantees — monitoring becomes feedback, healing becomes setpoint restoration [8]. Earlier threads in the TAAS reference list show the lineage: Kokar/Baclawski's control-theoretic foundations of self-controlling software (IEEE Intelligent Systems 1999) and Abdelwahed et al.'s control-based framework for self-managing distributed systems (WOSS 2004) [3].
3. **Guarantees for adaptive behavior**: monitors provide the runtime evidence (violation traces) needed to decide *when* a healing action is safe — the modern incarnation being test suites as runtime monitors in SWE-bench evaluation (FAIL_TO_PASS/PASS_TO_PASS as the property) [21].

### 5. Self-healing surveys: what the survey literature actually says

The dedicated "self-healing" survey literature is modest and — contrary to the brief's assumption — mostly *outside* IEEE TSE:

- **Ghosh, Sharman, Rao & Upadhyaya**, *Self-healing systems — survey and synthesis*, **Decision Support Systems 42(4):2164–2185, 2007** (Elsevier; DOI 10.1016/j.dss.2006.06.011). The foundational survey; asks whether self-healing is a field or a subclass of fault tolerance, and synthesizes detect/diagnose/recover mechanisms [30].
- **Psaier & Dustdar**, *A survey on self-healing systems: approaches and systems*, **Computing 91(1):43–70, 2011** (Springer; DOI 10.1007/s00607-010-0107-y). Grounds self-healing in the autonomic/self-* principles and catalogs systems [31].
- **Huebscher & McCann**, *A survey of autonomic computing — degrees, models, and applications*, **ACM CSUR 40(3), 2008** — the ACM-survey anchor covering self-healing among the four self-* dimensions [4].
- **Schneider et al.**, *A survey of self-healing systems frameworks* (Software: Practice and Experience, 2015) — comparative framework analysis (search-verified; not fetched: [UNVERIFIED URL]).
- **Weyns et al.**, *Claims and supporting evidence for self-adaptive systems: a literature study* (SEAMS 2012, DOI 10.1109/SEAMS.2012.6224395) — the field's famous self-audit: only a small fraction of claims had strong supporting evidence; a sobering precedent for evaluating AI-healing claims [33].
- A purported "IEEE TSE 2018 survey of self-healing systems for software engineering" surfaced in search but could **not** be verified against any primary record — [UNVERIFIED], excluded.

---

## Taxonomy: the four self-* properties

From IBM autonomic computing (Horn 2001; Kephart & Chess 2003) [1][2]:

| Property | Definition (per the Vision paper) | Fault-tolerance ancestor | AI-era instantiation |
|---|---|---|---|
| **Self-configuration** | Install, set up, and integrate new components automatically; adapt to dynamically changing environments | Plug-and-play discovery; scripted provisioning | Agent scaffolds bootstrapping an environment (SWE-agent's ACI setup) [23] |
| **Self-healing** | Discover, diagnose, and react to disruptions; keep malfunctions local, repair/replace failed components | Recovery blocks, NVP, WAL, BFT, self-stabilization [9][11][12][14][15] | Fault localization + patch synthesis + test validation (APR; SWE-bench agents) [19][21] |
| **Self-optimization** | Continually tune resources and performance to meet goals | Feedback-control regulation [8] | Cost-aware repair selection (Agentless $0.70/task; Opus 4.5 effort/token trade-offs) [24][28] |
| **Self-protection** | Anticipate, detect, identify, and protect against attacks | Byzantine tolerance; intrusion response [14] | Contamination defenses, sandboxed agent execution (bash-only scaffold policy) [26] |

**Where "healing" splits** (synthesis across [2][3][30]):

1. **Detect** — anomalies/violations: acceptance tests (Randell), RV monitors (Leucker & Schallhart), failing test suites (SWE-bench), architectural constraint violations (Rainbow) [11][32][21][5].
2. **Diagnose** — localize root cause: spectrum-based fault localization (AutoCodeRover), hierarchical search (Agentless), model-based diagnosis [25][24].
3. **Recover** — restore service: rollback (recovery blocks, WAL), retry/reconfigure (Stitch tactics), replace (NVP voting), or *repair the code* (GenProg → LLM agents) [11][15][5][16][23].
4. **Learn** — improve future healing: the weakest link historically; autonomic-era answers were reinforcement learning (Tesauro's RL-in-autonomic-computing work, per the TAAS reference list [3]); AI-era answers are fine-tuning on repair traces (RepairLLaMA) and agent memory/iterations [20].

---

## Key numbers

- **55 of 105** real bugs fixed by GenProg at **~US$8 each** (ICSE 2012) [16].
- **3f+1** replicas; PBFT's replicated NFS ran **~3% slower** than unreplicated in normal operation (OSDI '99) [14].
- **2 pages**: Dijkstra's 1974 self-stabilization paper, CACM 17(11):643–644 [9].
- **2,294** task instances across **12** Python repos in SWE-bench full; **1.96%** best resolution at release (Claude 2) [21][26].
- **500** human-validated instances in SWE-bench Verified; **93** professional developers; **38.3%** underspecified statements, **61.1%** unfair tests, **68.3%** of samples filtered out (OpenAI, Aug 13, 2024) [22].
- **33.2%** Verified for GPT-4o (vs ~16% on the unaudited set) at release of Verified [22].
- **12.5%** full-SWE-bench pass@1 for SWE-agent (GPT-4, May 2024) [23].
- **32.00%** SWE-bench Lite (96 fixes) for Agentless at **US$0.70/task** [24].
- **19%** SWE-bench Lite for AutoCodeRover at **US$0.43/issue** (ISSTA 2024 abstract) [25].
- **3.3×** more fixes than the best baseline on Defects4J 2.0 for AlphaRepair (zero-shot) [19].
- **144** Defects4J v2 bugs fixed by RepairLLaMA adapters; 109 HumanEval-Java; 20 GitBug-Java [20].
- **72.5%** (Claude Opus 4) and **72.7%** (Claude Sonnet 4) Verified, released May 22, 2025 [27].
- Claude Opus 4.5 (Nov 24, 2025): beats Sonnet 4.5's best by **4.3pp** at high effort with **48% fewer output tokens**; ≈**80.9%** Verified per LLM Registry [28][29].
- **87.6%** SOTA Verified; **76.2%** median across **48** models (LLM Registry, accessed 2026-11-09) [29].
- Kephart & Chess 2003: ~**6,900+** citations (Semantic Scholar, accessed 2026-11-09) [2].

---

## How it was done before AI vs with AI

| Dimension | Before AI (1956–2015) | With AI (2022–2026) |
|---|---|---|
| **Trigger (detect)** | Pre-placed acceptance tests, watchdogs, assertions, RV monitors, heartbeat failure detectors [11][32] | Same monitors, plus: failing CI test suites as oracle; LLM reads logs/stack traces directly [21][25] |
| **Diagnosis** | Model-based diagnosis; spectrum-based fault localization; expert rules [3][30] | SBFL retained (AutoCodeRover) but fused with LLM code-context retrieval; hierarchical repo search (Agentless) [25][24] |
| **Fix generation** | Enumerated at design time: rollback to checkpoint, switch to alternate version, restart, reconfigure (Rainbow/Stitch tactics) [11][12][5] | *Synthesized at runtime*: GP mutation of existing code (GenProg) → constraint solving (SemFix) → zero-shot cloze (AlphaRepair) → free-form repo edits by agents [16][17][19][23] |
| **Validation** | Acceptance test, voter agreement, invariants [11][12] | Repository test suites: FAIL_TO_PASS + PASS_TO_PASS — cheap, parallel, and gameable (hence Verified's audit) [21][22] |
| **Knowledge** | Explicit models: architectural models at runtime (Rainbow, models@run.time), queuing/control models (Hellerstein) [5][6][8] | Implicit in weights: pretrained code models carry repair priors; explicit knowledge returning as agent scaffolds (ACIs), RAG over repo docs [23] |
| **Guarantees** | Strong: BFT safety/liveness proofs, self-stabilization convergence, control-theoretic stability, ACID durability [14][9][8][15] | Empirical: benchmark resolution rates; correctness proxies (tests pass); formal guarantees largely absent — the open gap |
| **Novelty of faults** | Only anticipated fault classes (design-time provisioning); novel faults → human patch | Novel defects routinely fixed (real GitHub issues); remaining failure modes: multi-file refactors, ambiguous specs [21][22] |
| **Cost frame** | Hardware/time redundancy (3f+1 replicas; N versions) [14][12] | Dollars per issue: $8/fix (2012) → $0.43–$0.70/task (2024) → token-budget "effort" levels (2025) [16][25][24][28] |
| **Learning loop** | Mostly absent (fixed policies); some RL experiments (Tesauro) [3] | Fine-tuning on repair traces (RepairLLaMA); scaffold iteration as de-facto learning [20][26] |

One-sentence synthesis: pre-AI self-healing **engineered recovery in advance** and proved it would work; AI-era self-healing **improvises recovery at runtime** and measures how often it works.

---

## Canonical references

1. Kephart & Chess, *The Vision of Autonomic Computing* — IEEE Computer 36(1):41–50, 2003 — https://doi.org/10.1109/MC.2003.1160055 (accessed 2026-11-09) [2]
2. Horn, *Autonomic Computing: IBM's Perspective on the State of Information Technology* — IBM, 2001 — https://people.scs.carleton.ca/~soma/biosec/readings/autonomic_computing.pdf (accessed 2026-11-09) [1]
3. Salehie & Tahvildari, *Self-adaptive software: Landscape and research challenges* — ACM TAAS 4(2), Art. 14, 2009 — https://dl.acm.org/doi/10.1145/1516533.1516538 (accessed 2026-11-09) [3]
4. Garlan, Cheng, Huang, Schmerl & Steenkiste, *Rainbow: Architecture-Based Self-Adaptation with Reusable Infrastructure* — IEEE Computer 37(10):46–54, 2004 — https://doi.org/10.1109/MC.2004.100 (accessed 2026-11-09) [5]
5. Dijkstra, *Self-stabilizing systems in spite of distributed control* — CACM 17(11):643–644, 1974 — https://dl.acm.org/doi/10.1145/361179.361202 (accessed 2026-11-09) [9]
6. Randell, *System structure for software fault tolerance* — IEEE TSE SE-1(2):220–232, 1975 — https://doi.org/10.1109/TSE.1975.6312840 (accessed 2026-11-09) [11]
7. Castro & Liskov, *Practical Byzantine Fault Tolerance* — OSDI '99:173–186 — https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance (accessed 2026-11-09) [14]
8. Le Goues, Dewey-Vogt, Forrest & Weimer, *A Systematic Study of Automated Program Repair: Fixing 55 out of 105 Bugs for $8 Each* — ICSE 2012 — https://doi.org/10.1109/ICSE.2012.6227211 (accessed 2026-11-09) [16]
9. Jimenez, Yang, Wettig, Yao, Pei, Press & Narasimhan, *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* — ICLR 2024 (arXiv:2310.06770) — https://arxiv.org/abs/2310.06770 (accessed 2026-11-09) [21]
10. Yang, Jimenez, Wettig, Khandre, Lapeyre, Yang, Narasimhan & Khattab, *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* — NeurIPS 2024 (arXiv:2405.15793) — https://arxiv.org/abs/2405.15793 (accessed 2026-11-09) [23]
11. Xia, Deng, Dunn & Zhang, *Agentless: Demystifying LLM-based Software Engineering Agents* — FSE/PACMSE 2025 (arXiv:2407.01489) — https://arxiv.org/abs/2407.01489 (accessed 2026-11-09) [24]
12. Ghosh, Sharman, Rao & Upadhyaya, *Self-healing systems — survey and synthesis* — Decision Support Systems 42(4):2164–2185, 2007 — https://doi.org/10.1016/j.dss.2006.06.011 (accessed 2026-11-09) [30]

---

## Full source list

[1] Autonomic Computing: IBM's Perspective on the State of Information Technology — Paul Horn / IBM, 2001 — https://people.scs.carleton.ca/~soma/biosec/readings/autonomic_computing.pdf (accessed 2026-11-09)
[2] The Vision of Autonomic Computing — J. Kephart & D. Chess, IEEE Computer 36(1):41–50, 2003 — https://doi.org/10.1109/MC.2003.1160055 (accessed 2026-11-09)
[3] Self-adaptive software: Landscape and research challenges — M. Salehie & L. Tahvildari, ACM TAAS 4(2), 2009 (received May 2007) — https://dl.acm.org/doi/10.1145/1516533.1516538 (accessed 2026-11-09)
[4] A survey of autonomic computing—degrees, models, and applications — M. Huebscher & J. McCann, ACM Computing Surveys 40(3), 2008 — https://doi.org/10.1145/1380584.1380585 (accessed 2026-11-09)
[5] Rainbow: Architecture-Based Self-Adaptation with Reusable Infrastructure — D. Garlan, S.-W. Cheng, A.-C. Huang, B. Schmerl, P. Steenkiste, IEEE Computer 37(10):46–54, 2004 — https://doi.org/10.1109/MC.2004.100 (accessed 2026-11-09)
[6] Models@run.time — G. Blair, N. Bencomo, R. France, IEEE Computer 42(10):22–27, 2009 — https://doi.org/10.1109/MC.2009.326 (accessed 2026-11-09)
[7] Software Engineering for Self-Adaptive Systems / SEAMS community site — self-adaptive.org, 2024–2026 — https://self-adaptive.org/ (accessed 2026-11-09)
[8] Feedback Control of Computing Systems — J. Hellerstein, Y. Diao, S. Parekh, D. Tilbury, Wiley-IEEE Press, 2004 (ISBN 0-471-26637-X) — https://www.google.com/books/edition/_/kFeMrgEACAAJ (accessed 2026-11-09)
[9] Self-stabilizing systems in spite of distributed control — E. W. Dijkstra, CACM 17(11):643–644, 1974 — https://dl.acm.org/doi/10.1145/361179.361202 (accessed 2026-11-09)
[10] Probabilistic Logics and the Synthesis of Reliable Organisms from Unreliable Components — J. von Neumann, Automata Studies, Princeton UP, pp. 43–98, 1956 — https://static.ias.edu/pitp/archive/2012files/Probabilistic_Logics.pdf (accessed 2026-11-09)
[11] System Structure for Software Fault Tolerance — B. Randell, IEEE TSE SE-1(2):220–232, 1975 — https://doi.org/10.1109/TSE.1975.6312840 (accessed 2026-11-09)
[12] The N-Version Approach to Fault-Tolerant Software — A. Avizienis, IEEE TSE SE-11(12):1491–1501, 1985 — https://doi.org/10.1109/TSE.1985.231893 (accessed 2026-11-09)
[13] Exception Handling: Issues and a Proposed Notation — J. B. Goodenough, CACM 18(12):683–696, 1975 — https://doi.org/10.1145/512976.512997 (accessed 2026-11-09)
[14] Practical Byzantine Fault Tolerance — M. Castro & B. Liskov, OSDI '99:173–186 — https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance (accessed 2026-11-09)
[15] Transaction Processing: Concepts and Techniques — J. Gray & A. Reuter, Morgan Kaufmann, 1993 (ISBN 1-55860-190-2) — https://www.amazon.com.au/Transaction-Processing-Jim-Gray/dp/1558601902 (accessed 2026-11-09)
[16] A Systematic Study of Automated Program Repair: Fixing 55 out of 105 Bugs for $8 Each — C. Le Goues, M. Dewey-Vogt, S. Forrest, W. Weimer, ICSE 2012 — https://doi.org/10.1109/ICSE.2012.6227211 (accessed 2026-11-09)
[17] SemFix: Program Repair via Semantic Analysis — H. D. T. Nguyen, Z. Qi, A. Roychoudhury, S. Chandra, ICSE 2013:772–781 — https://abhikrc.com/pdf/ICSE13-SEMFIX.pdf (accessed 2026-11-09)
[18] The Living Review on Automated Program Repair — M. Monperrus, HAL hal-01956501, 2018 (living document) — https://hal.science/hal-01956501/document (accessed 2026-11-09)
[19] Less Training, More Repairing Please: Revisiting Automated Program Repair via Zero-shot Learning (AlphaRepair) — C. S. Xia & L. Zhang, ESEC/FSE 2022 (arXiv:2207.08281) — https://arxiv.org/abs/2207.08281 (accessed 2026-11-09)
[20] RepairLLaMA: Efficient Representations and Fine-Tuned Adapters for Program Repair — A. Silva, S. Fang, M. Monperrus, IEEE TSE 2025 (arXiv:2312.15698) — https://arxiv.org/abs/2312.15698 (accessed 2026-11-09)
[21] SWE-bench: Can Language Models Resolve Real-World GitHub Issues? — C. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, K. Narasimhan, ICLR 2024 (arXiv:2310.06770) — https://arxiv.org/abs/2310.06770 (accessed 2026-11-09)
[22] Introducing SWE-bench Verified — OpenAI, Aug 13, 2024 — https://openai.com/index/introducing-swe-bench-verified/ (accessed 2026-11-09)
[23] SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering — J. Yang et al., NeurIPS 2024 (arXiv:2405.15793) — https://arxiv.org/abs/2405.15793 (accessed 2026-11-09)
[24] Agentless: Demystifying LLM-based Software Engineering Agents — C. S. Xia, Y. Deng, S. Dunn, L. Zhang, FSE/PACMSE 2(FSE), 2025 (arXiv:2407.01489) — https://arxiv.org/abs/2407.01489 (accessed 2026-11-09)
[25] AutoCodeRover: Autonomous Program Improvement — Y. Zhang, H. Ruan, Z. Fan, A. Roychoudhury, ISSTA 2024 (arXiv:2404.05427) — https://arxiv.org/abs/2404.05427 (accessed 2026-11-09)
[26] SWE-bench official leaderboards & benchmark variants — swebench.com, 2024–2026 — https://www.swebench.com/ (accessed 2026-11-09)
[27] Claude 4 (Opus & Sonnet) announcement — Anthropic, May 22, 2025 — https://www.anthropic.com/news/claude-4 (accessed 2026-11-09)
[28] Claude Opus 4.5 announcement — Anthropic, Nov 24, 2025 — https://www.anthropic.com/news/claude-opus-4-5 (accessed 2026-11-09)
[29] SWE-bench Verified leaderboard — LLM Registry, 2025–2026 — https://llm-registry.com/benchmark/swe-bench-verified (accessed 2026-11-09)
[30] Self-healing systems — survey and synthesis — D. Ghosh, R. Sharman, H. R. Rao, S. Upadhyaya, Decision Support Systems 42(4):2164–2185, 2007 — https://doi.org/10.1016/j.dss.2006.06.011 (accessed 2026-11-09)
[31] A survey on self-healing systems: approaches and systems — H. Psaier & S. Dustdar, Computing, 2011 — https://doi.org/10.1007/s00607-010-0107-y (accessed 2026-11-09)
[32] A brief account of runtime verification — M. Leucker & C. Schallhart, J. Logic and Algebraic Programming 78(5):293–303, 2009 — https://doi.org/10.1016/j.jlap.2008.08.004 (accessed 2026-11-09)
[33] Claims and supporting evidence for self-adaptive systems: A literature study — D. Weyns et al., SEAMS 2012 — https://doi.org/10.1109/SEAMS.2012.6224395 (accessed 2026-11-09; metadata via search, DOI not resolved directly)

---

## Open questions

1. **Where are the guarantees?** Pre-AI healing came with proofs (BFT safety, self-stabilization convergence, control stability). LLM-era healing is benchmarked, not verified. Can RV-style monitors or control-theoretic wrappers be placed *around* LLM repair agents so their actions carry formal safety conditions? [9][14][32][8]
2. **Does MAPE-K still hold, or does it invert?** In MAPE-K, knowledge is explicit and curated; in agents, "knowledge" is frozen in weights plus whatever context fits the window. Is an LLM agent a MAPE-K loop with an implicit knowledge base, or a genuinely new control architecture? [2][23]
3. **Benchmark validity after saturation.** Verified is frozen (2024), public, and possibly contaminated — GitHub fixes are in training data, and the scaffold (mini-SWE-agent bash-only) is now a confound. What would a *held-out, private, actively refreshed* healing benchmark look like? [22][26][29]
4. **Agents or pipelines?** Agentless showed fixed workflows match agents at lower cost in 2024; by 2026 strong models seem to reduce the scaffold's importance (bash-only evaluation). Is scaffold engineering a temporary crutch or the permanent "ACI" discipline? [24][23][26]
5. **From repairing issues to healing systems.** SWE-bench fixes bugs *offline*. The classical self-healing goal — detect, diagnose, recover *in production, without human intervention* — remains largely untouched by the LLM wave. Who closes the loop from "PR-resolving agent" to "runtime self-healing system" (the lks-shs project's own target)? [1][2][21]
6. **The learn stage.** Fine-tuning on repair traces (RepairLLaMA) works for micro-edits; can agents accumulate durable, transferable "repair memory" across incidents, or does each healing event remain stateless? [20]
7. **Definitions have drifted.** Autonomic "self-healing" assumed component-level faults in managed infrastructure; AI repair assumes specification-level defects in source code. A unified ontology of "what is being healed, from what, to what invariant" is still missing — a prerequisite for evaluating claims (see Weyns et al.'s evidence audit as precedent) [2][30][33].
