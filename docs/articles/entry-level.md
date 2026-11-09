# Self-Healing Software for the Entry-Level Programmer

*One of four articles — [ELI5](eli5.md) · **Entry-level** · [Professional](professional.md) · [C-suite](c-suite.md). Claims trace to [dossiers](../research/README.md); the demo runs in one command.*

You've written a service, deployed it, and had it die at 2 a.m. This article gives you the vocabulary, the mental model, and a runnable toy where *you* cause the failures.

## The six terms that matter

1. **Liveness vs. correctness.** "Is the process up?" and "is it answering *correctly*?" are different questions. A hung process is *alive but wrong*. A zombie is up but useless. Good monitoring checks both.
2. **Heartbeat / dead man's switch.** The service periodically proves it exists (writes a file, calls an endpoint). *Absence* of the ping is the signal. Same idea from systemd services to cron-job monitors ([Healthchecks.io](https://healthchecks.io)) to Raft leader election.
3. **Supervisor.** A *separate* process whose job is watching yours and restarting it — because a healer that dies with the patient heals nothing. Erlang/OTP built this into the language; systemd and Kubernetes kubelet do it for everything else.
4. **Restart ≠ rollback ≠ repair.** Restart reclaims state (fixes transient faults). Rollback removes a bad *change* (most outages are caused by change). Repair fixes the *code* — the only one that removes the cause, and the only one that should require tests + human review.
5. **Crash-loop backoff + restart intensity.** When a deterministic bug crashes your service, restarting fast just hammers the corpse. So supervisors back off exponentially (kubelet: 10s→300s) and, after N restarts in T seconds, *give up and page a human* (OTP's MaxR/MaxT). That's not failure — it's the design working.
6. **The verification gate.** Nothing counts as healed until something that *isn't the fixer* says so: a health check, a golden request ("GET / must return the exact token"), a test suite. This is the one rule you should internalize above all others.

## The mental model: PULSE

**P**erceive (signals) → **U**nderstand (classify) → **L**ocalize (find the component/line/config) → **S**olve (restart/rollback/patch — *always through the verification gate*) → **E**volve (postmortem, harden, update the rules). It's IBM's classic MAPE-K loop (Kephart & Chess, 2003) with two modern additions: localization and verification, because those turned out to be the hard parts.

Two facts to keep you humble:

- Retries without a budget can multiply load on a failing dependency by **243×** (a 5-layer call stack with 3 retries each). Backoff + jitter + retry budgets are not optional polish.
- The famous Erlang "nine nines" reliability number came from a PowerPoint slide whose methodology "was not documented" — per Armstrong's own thesis. Ask *how anyone measured that* about every reliability claim, including your own.

## Run the demo (yes, you)

```bash
git clone https://github.com/seolith-llc/lks-shs && cd lks-shs/prototypes/pulse-app
./demo.sh
```

You'll watch five scenarios: a **crash** (supervisor restarts it), a **hang** (only the heartbeat catches it — liveness checks alone would call it healthy), a **memory leak** (restarted, and honestly logged *"mitigated, not cured"*), an **error storm** (error-rate threshold trips), and a **crashloop** (the supervisor refuses to thrash and escalates instead). Then read `supervisor.py` — the whole loop in one readable file. [Full walkthrough](../posts/05-pulse-in-python.md).

## Where AI actually fits (so you don't over-believe the ads)

- **Proven today:** AI that *investigates* (reads logs, ranks likely causes), AI that *drafts fixes as pull requests* — validated by re-running the linter/security scanner before a human reviews, and AI that writes fuzz tests that found real 20-year-old bugs.
- **Not proven:** AI that autonomously fixes production. Even the vendors that hint at it gate every action behind human review, because acting on a wrong diagnosis at machine speed is how bad nights get worse.
- Your career-relevant skill: **build the loop, the oracles, and the gates.** The AI plugs into the middle of that, and someone has to understand the middle.

## Your first-week checklist for any service you own

- [ ] Health endpoint + out-of-band uptime check
- [ ] Dead man's switch on every cron/backup job
- [ ] Restart policy with backoff (and know your MaxR/MaxT)
- [ ] Deploy pipeline that rolls back on failed health checks
- [ ] Backups — and one *practiced* restore
- [ ] One golden request you can assert from outside

*Ready for the deep end? The [professional article](professional.md) and the [9-part series](../posts/00-series-overview.md) have the full architecture.*
