# Self-Healing Software — Axioms (draft)

Working axioms for engineering self-healing systems. Status: **draft** — each axiom gets linked evidence from the research dossiers during Phase 6, or gets dropped. (v0.1)

- **A1 · Everything fails; design for recovery, not perfection.** Perfection is unattainable; fast recovery is. *(evidence: pending — Erlang/OTP, Release It!)*
- **A2 · Healing without learning is just rebooting.** A healed system that doesn't capture why it failed will fail the same way again. *(pending — MAPE-K's Knowledge component, postmortems)*
- **A3 · The healer must not harm the patient.** Autonomous remediation needs blast-radius limits, rate limits, and a circuit breaker on the healer itself. *(pending — retry storms, runaway automation incidents)*
- **A4 · The monitor must not be the disease.** Observability has a cost; an observability outage must not blind healing. *(pending — overhead budgets, health-check storms)*
- **A5 · Fail fast, heal fast.** A quick clean crash with supervision beats a slow zombie limping along. *(pending — crash-only software, "let it crash")*
- **A6 · A fix that isn't verified is a guess.** Every automated repair passes a validation gate before it counts as healed. *(pending — automated program repair, canary analysis)*
- **A7 · Declare health; converge to it.** Desired-state reconciliation beats imperative patch scripts. *(pending — Kubernetes/Borg, control loops)*
- **A8 · Autonomy is earned in levels.** L0 human-in-the-loop → full autonomy, advanced one level at a time with evidence — like self-driving cars. *(pending — automation levels taxonomy)*
- **A9 · Detection without diagnosis is noise.** Alert fatigue kills; every alert must carry enough context to act on. *(pending — AIOps alert-fatigue research)*
- **A10 · Prevention is the cheapest cure.** Memory-safe languages, fuzzing, and tests remove failure modes before they exist. *(pending — memory-safety CVE statistics, OSS-Fuzz)*
- **A11 · The last responsible human is part of the loop.** Enterprise-grade healing keeps humans at the gates that matter, and automates the rest. *(pending — HITL patterns, governance)*
- **A12 · Small businesses heal differently.** What fits an SRE team does not fit a two-person shop; healing must scale down to backups, watchdogs, and managed platforms. *(pending — small-biz stack research)*
