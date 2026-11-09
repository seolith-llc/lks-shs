# Episode 04 · The PULSE Framework

## Self-Healing Software, Part Four
- The PULSE framework
- One loop, every layer
- lks-shs · the PULSE series

Part four turns seventy years of evidence into architecture. The framework is called PULSE, and the name is literal.

## PULSE
- Perceive — signals: probes, heartbeats, traces, checksums
- Understand — classify, rank root-cause hypotheses
- Localize — component, line, config, dependency
- Solve — restart, rollback, reroute, patch
- Evolve — verify, postmortem, harden, update policy

Perceive, Understand, Localize, Solve, Evolve. A direct descendant of IBM's MAPE K loop, with two additions the last twenty years forced.

## Why exactly five stages
- Localize is its own stage — it's where 2024 pipelines won
- the verification gate sits between Solve and Evolve
- "a fix that isn't verified is a guess"

Why five stages? Because localization, mapping a hypothesis to the exact component, is where the cheap structured pipelines beat the fancy agents. And because nothing counts as healed until a non A I oracle says so: tests, security scans, steady state metrics, a golden request. GitHub re runs Code Q L. Snyk re runs SAST. Meta's test generator filtered seventy three percent acceptance through build and test first.

## The heartbeat is everywhere
- liveness probes · sd_notify · Raft heartbeats · dead man's switches
- the one health primitive at every layer
- hence: the PULSE loop = the heartbeat of a self-healing system

And why the name? The heartbeat is the one health primitive that exists at every layer of the stack. Liveness probes, watchdog notifications, consensus heartbeats, dead man's switches. The PULSE loop is the heartbeat of a self-healing system.

## Heal low, escalate slowly
- L1 hardware → L2 kernel → L3 process → L5 data → L6 delivery → L7 operations
- heal at the lowest sufficient layer
- escalate only on repeated failure (MaxR/MaxT)

The stack rule: heal at the lowest layer that works, and escalate only on repeated failure. That is exactly what Erlang's restart intensity and Kubernetes crash loop backoff encode. A Is enter at the top of the stack and must earn their way down.

## Autonomy is a ladder
- L0 observe · L1 investigate · L2 propose PRs · L3 bounded actuation
- L4 closed loop: no verified production deployment yet
- advance per action class, on measured evidence

And autonomy is a ladder, not a switch. Observe, investigate, propose, bounded actuation. Rung four, the closed loop, has no verified production deployment anywhere. Advance one action class at a time, on measured evidence. Next: the whole framework running in six hundred lines of Python.
