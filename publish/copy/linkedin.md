# LinkedIn — launch post (paste-ready)

> Works as a post or an article. First-person, professional register, no thread mechanics.

**Why we published 180 sources, a framework, and a self-healing prototype — for free**

Self-healing software sounds like a 2026 buzzword. It's actually one of the oldest ideas in systems engineering — and the newest AI wave just changed exactly one part of it.

We spent the past period researching this properly:

▪ **180 verified sources** across four dossiers — academic (MAPE-K, automated program repair), industrial (Erlang/OTP, chaos engineering, Kubernetes), systems-level (live patching, eBPF, self-repairing storage), and the 2024–26 AI-ops market.

▪ **One framework**: PULSE — Perceive, Understand, Localize, Solve, Evolve. The same loop at every layer, from ECC memory to incident channels, with one non-negotiable rule: nothing is healed until a non-AI oracle says so.

▪ **A runnable prototype**: ~600 lines of standard-library Python. Crash it, hang it, leak it — it heals (MTTR 1.6–7.9 s), and when the fault is deterministic, it refuses to thrash and escalates to a human instead. That last behavior is borrowed from Erlang's restart-intensity design, and it's the part most "AI ops" demos quietly lack.

The honest finding for anyone buying AI operations tooling this year: autonomous *investigation* is real and shipping (incident.io, Datadog, PagerDuty, Rootly). Autonomous *remediation* is not — the entire verified market gates actions behind human review, and the most instructive public incident is an authorized agent deleting ~200 workloads in 90 seconds. The controls that fixed that were infrastructure, not prompts: rate caps, budgets, undo tests, agent identity.

Everything is open — including the seven decision records that document every alternative we rejected and why, and the full conversation audit trail:

**github.com/seolith-llc/lks-shs**

There's a version for every altitude on your team: ELI5, entry-level, professional, and a C-suite brief with three vendor questions worth asking before any renewal.

If your team runs anything in production, I'd genuinely value your read on the enterprise playbook — and if you clone the prototype, go break it. It can take it.

#SRE #AIOps #SoftwareEngineering #Reliability #PlatformEngineering #OpenSource
