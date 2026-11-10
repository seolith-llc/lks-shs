# Short S3 · 200 workloads in 90 seconds

## An AI agent ran wild
- at Anthropic, of all places
- an authorized cleanup task
- under an engineer's credentials

The most instructive AI failure story in operations happened at Anthropic, the AI company. An agent was doing an authorized cleanup task, running under an engineer's credentials.

## What happened
-! ~200 | workloads deleted in 90 seconds
- not a hallucination — an authorized action, unbounded

It deleted about two hundred workloads in ninety seconds. And here is the twist. It was not a hallucination. It was an authorized action, executing without speed limits.

## The fix wasn't a better prompt
- rate caps per hour and resource kind
- replenishing budgets + an "undo test"
- agent-scoped identity — in infrastructure

The fix was not a better prompt. It was admission webhooks capping deletions, replenishing budgets, an undo test before any write permission, and identity assigned by infrastructure. If you are giving agents production access, steal this postmortem. It is linked at the repo on screen.
