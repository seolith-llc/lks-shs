# Self-Healing Software for the Seasoned Professional

*One of four articles — [ELI5](eli5.md) · [Entry-level](entry-level.md) · **Professional** · [C-suite](c-suite.md). Every claim is sourced in the [dossiers](../research/README.md) (180 verified references); design choices carry [decision records](../architecture/decisions/001-acronym.md).*

## The engineering claim, precisely

Self-healing was never invented — it was **layered**: ECC → live patching → supervision → resilience patterns → reconciliation → progressive delivery → (now) AI-assisted operations. Every layer runs the same loop; what AI changes is the **decide stage**. Pre-2022, decide was frozen at design time (thresholds, restart policies) and terminated in a paged human. LLMs make diagnosis and repair-synthesis improvisable at runtime — SWE-bench Verified went **1.96% → 87.6% SOTA** in three years, with the median of 48 tracked models at 76.2% and the benchmark itself audited to remove 68.3% unfair/underspecified tasks (D01). The unsolved engineering problem is *transplanting* that capability inside the existing loops' safety envelope rather than beside it.

## The framework in one pass

**PULSE** — Perceive, Understand, Localize, Solve, Evolve — MAPE-K's descendant with localization promoted to a stage (it's where structured pipelines beat agents: Agentless 32% Lite at $0.70/task) and the **Solve→Evolve boundary hardened as a mandatory non-LLM verification gate**. Seven layers, each healing at the lowest sufficient layer, escalating on repeat (that's what MaxR/MaxT and crash-loop backoff *are*). Full component model and binding rules: [reference architecture](../architecture/reference-architecture.md); the six sequences you'd otherwise draw on a whiteboard are [here](../architecture/sequence-diagrams.md).

Three verdicts from the corpus that should shape your designs:

1. **AI-as-builder is production-proven; AI-as-healer is proven only in its observe/diagnose half** plus reversible, pre-authorized actuation. The 2025 product wave (incident.io Investigations, Datadog Bits, PagerDuty SRE Agent, Rootly) converged on exactly that line: autonomous investigation, PR-gated remediation.
2. **Verification-first is the load-bearing pattern.** GitHub re-runs CodeQL on its own autofix; Snyk SAST-screens candidates before display; Meta's TestGen-LLM achieved 73% production acceptance *because* build+test filtered first. If your AI fix pipeline lacks a non-LLM oracle in the loop, you're running the documented anti-pattern.
3. **The one detailed first-party failure is infrastructure-shaped:** an authorized agent deleting ~200 workloads in 90 seconds, remediated with admission webhooks, rate caps, replenishing budgets, an "undo test," and agent-scoped identity — *not* prompts (OWASP LLM06, Excessive Agency). Model your guardrails on that postmortem.

## What I'd actually build (and what the prototype proves)

A supervisor per runtime (OTP semantics: restart strategies, intensity limits), layered oracles (heartbeat for liveness + out-of-band golden request for correctness — self-reported `/health` alone is a self-grading exam; see [DR005](../architecture/decisions/005-verification-oracle.md)), canary-gated delivery with auto-rollback, and an L7 investigation agent that reads telemetry and emits evidence-cited RCAs behind a PR gate. That skeleton — ~600 lines, stdlib-only — runs as [`prototypes/pulse-app`](../../prototypes/pulse-app/README.md): five wound classes, five heals, escalation on restart storms, every event a logged Evolve artifact with MTTR (1.6–7.9s measured). It is deliberately the *boring* 80% that survives contact with production.

## Numbers you'll want in your next design review

- Downtime economics: >$300K/hour for 90%+ of firms (ITIC 2024); $400B/yr across the Global 2000 (Oxford Economics/Splunk) — the FinOps case for healing tooling is trivial; the Gartner >40%-by-2027 agentic-project cancellation rate is the discipline case.
- DORA 2024: each +25% AI adoption correlates with **−7.2% delivery stability** — AI-accelerated change without expanded validation funds its own incident workload.
- Systems layer: 88% of kernel CVEs live-patchable (Ksplice), Android memory-safety share 76%→24% via Rust — prevention still dominates cure where it's applicable.
- Capability trend: agent task horizons (50% reliability) doubling ~every 7 months (METR), but success collapses beyond ~4-hour tasks today. Design the interface for the 2028 agent; grant it the permissions of the 2024 one.

## The research frontier worth your skepticism

Nobody has published: a first-party account of a fully autonomous remediation decision with its audit trail; an independently audited MTTR study of any AI-SRE product; SOC 2/ISO control text covering *agent actions*; or a sub-$100/month agentic IR product. When a vendor claims L4, ask for exactly those four artifacts. The honest roadmap is rung-by-rung (L0→L3) per action class, gated on measured MTTR deltas and audit findings — [the enterprise playbook](../posts/07-the-enterprise-playbook.md) operationalizes it, and the [risk catalog](../posts/08-risks-anti-patterns-road-to-l4.md) maps all eight documented failure modes to controls with precedents.

*Same material for other audiences: [ELI5](eli5.md) · [entry-level](entry-level.md) · [C-suite](c-suite.md).*
