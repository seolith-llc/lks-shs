# Episode 01 · Seventy Years of Self-Healing

## Self-Healing Software, Part One
- Seventy years of self-healing
- What changed, what didn't
- lks-shs · the PULSE series

Welcome to the series. Self-healing software sounds like an AI-age promise. It isn't. The ideas are seventy years old, and the story of what actually changed is better than the marketing.

## The nine nines myth
- Erlang AXD301: "99.9999999% availability"
- Source: a PowerPoint slide — per Armstrong's own thesis
- Lesson: healing claims are cheap, evidence is precious

Start with a myth-bust. The most quoted reliability number in our field, the nine nines claim for the Ericsson Erlang switch, comes, in Joe Armstrong's own thesis, from a PowerPoint presentation whose methodology, in his words, was not documented. Hold that skepticism through everything.

## Three waves
- 1956–1999 · engineered recovery (TMR, recovery blocks, WAL, BFT)
- 2001–2012 · autonomic computing (MAPE-K, Rainbow, Erlang/OTP)
- 2012–now · improvised repair (GenProg, SWE-bench agents)

The field moved in three waves. First, engineer the healing in advance and prove it works. Then, IBM's autonomic vision: systems that manage themselves through feedback loops. And now, synthesize the fix at runtime and measure how often it works.

## One loop, everywhere
- observe → decide → act → re-check
- Erlang supervisors · circuit breakers · Kubernetes probes · ZFS scrub
- same shape at every layer

Strip the branding, and every mechanism across those seventy years is the same loop. Observe a signal, decide with a policy, act with a privileged mechanism, and check whether it worked. The layers differ in speed and intelligence, never in shape.

## Where it broke before AI
- sensing: solved · actuation: solved
- the decide stage: frozen — thresholds + a paged human
- restart is not repair · naive retry amplifies load 243 times

Before AI, sensing and actuation were solved. What stayed frozen was the decide stage: hand-tuned thresholds ending in a human with a runbook at three a.m. And it failed in documented ways. Restart is not repair; a deterministic bug just crash-loops. Naive retries can multiply load on a failing dependency by two hundred forty three times.

## The thesis
- actuation was already solved
- AI changes the decide stage
- the challenge: transplant intelligence inside the old safety envelope

So here is the thesis of this series. The actuation layer was already solved. What AI changes is the decide stage, for the first time improvising diagnosis and repair at runtime. The engineering challenge is transplanting that intelligence inside the old loop's safety envelope, not bolting it on outside. Next episode: the systems layer, where kernels patch themselves while running.
