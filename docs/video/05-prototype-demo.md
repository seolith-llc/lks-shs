# Episode 05 · PULSE in ~600 Lines of Python

## Self-Healing Software, Part Five
- The prototype
- Wound it. Watch it heal.
- lks-shs · the PULSE series

Reading about healing loops is like reading about swimming. Part five is water: a runnable prototype, standard library only, one command.

## Two actors
- the patient: a web service you can crash, hang, leak, enrage
- the healer: an external supervisor running the PULSE loop every 0.3s
- heartbeat file + /health gauge + golden request "PULSE-OK"

Two actors. The patient is a small web service that writes a heartbeat file every half second, reports its own gauges, and answers a golden request with the token PULSE O K. The healer is an external supervisor, the same shape as systemd or an Erlang supervisor, running the loop every three hundred milliseconds.

## Five wounds, five lessons
- crash → supervised restart (the classic)
- hang → dead man's switch (liveness ≠ aliveness)
- leak → restart = mitigated, not cured
- errors → error-rate breach, canary logic in miniature
- crashloop → escalate instead of thrash

You can inject five wounds, and each one teaches a finding from the research. Crash it, and the supervisor restarts it with capped backoff. Hang it, and only the dead man's switch catches it, because a process alive check would call this healthy. Leak memory, and the demo heals it while logging, honestly, mitigated, not cured; the code fix still needs a human reviewed pull request.

## The crashloop scenario
- 3 restarts inside 30s → ESCALATE
- page a human, halt rescheduling
- the healer must not harm

The best scenario is the crashloop. Crash the service faster than the restart window allows, and after the third restart the supervisor refuses to reschedule. It escalates and pages a human instead of thrashing. That is Erlang's restart intensity pattern, and it is the healer protecting the patient from the healer.

## Verified evidence
- demo run: 5/5 scenarios PASS
- MTTRs: crash 1.6s · hang 7.9s · leak 3.2s · errors 2.9s
- every event logged with stages, triage, MTTR

This is not a mockup. The committed evidence log shows five out of five scenarios passing, with mean time to recovery between one point six and seven point nine seconds, and every healing event logged as an evolve artifact.

## Run it yourself
- repo: lks-shs, prototypes/pulse-app
- one command: ./demo.sh
- then read supervisor.py — the whole loop in one file

Clone the repository, run demo dot sh, then read the supervisor. It is deliberately the shortest complete implementation of this series' claims: every wound class, every oracle, every gate, in one file you can hold in your head. Next: the small business playbook.
