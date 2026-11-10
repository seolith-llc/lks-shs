# X / Twitter — launch thread (10 posts, paste-ready)

> Post 1 first, then reply-chain the rest. Thread text ≤280 chars each. Pin after posting.

**1/** Software doesn't get patched by magic — it heals itself, and it has for 70 years.

I spent a day building the full picture: 180 verified sources, one framework, a runnable prototype you can crash.

This thread is the whole story. 🧵

**2/** Self-healing predates AI. 1956: von Neumann proves reliable systems can be built from unreliable parts. 1974: Dijkstra's self-stabilization. 1999: Byzantine fault tolerance. 2003: IBM names it — MAPE-K.

The loop was always: observe → decide → act → check.

**3/** Erlang people love the "nine nines" story (99.9999999% availability on the AXD301 switch).

The origin, in Joe Armstrong's own thesis: a PowerPoint slide, "how these figures had been obtained was not documented."

Healing claims are cheap. Evidence is precious.

**4/** The pre-AI playbook solved sensing and actuation: heartbeats, checksums, restarts, rollbacks, re-elections, repair-in-place. Kubernetes restarts containers that fail. ZFS repairs bit rot on every read.

What stayed frozen: the DECIDE stage. Thresholds + a paged human at 3am.

**5/** 2024–26 changed the decide stage. SWE-bench issue resolution: 1.96% (2023) → 87.6% SOTA (2026).

And "AI SRE" became a product category: incident.io, Datadog Bits, PagerDuty SRE Agent, Rootly — all converged on the same line:

Investigate autonomously. Remediate through human gates.

**6/** The most instructive failure: an AI agent at Anthropic deleted ~200 workloads in 90 seconds. Authorized action. No speed limit.

The fix wasn't a better prompt — rate caps, budgets, undo tests, agent identity. In infrastructure.

**7/** So we distilled everything into one framework: PULSE.

Perceive → Understand → Localize → Solve → Evolve.

Nothing is healed until a non-AI oracle (tests, metrics, golden request) says so. That's the one rule.

**8/** And it's not theory. There's a working prototype: ~600 lines of stdlib Python. Crash it, hang it, leak it — watch it heal (MTTR 1.6–7.9s), and when it crashloops, it refuses to thrash and escalates instead.

One command: ./demo.sh

**9/** There's something for every altitude:
- ELI5 article (bodies and bike falls)
- entry-level (6 terms + a checklist)
- pro (the three corpus verdicts)
- C-suite (3 numbers, 3 vendor questions, a 90-day plan)

**10/** Everything is open: 180-source research corpus, 7 decision records (every rejected alternative), 9-part series, 8 narrated episodes, 4 shorts, the prototype.

github.com/seolith-llc/lks-shs

Go break it. Report what heals. 🫀
