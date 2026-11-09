# Episode 08 · Risks, Anti-Patterns, and the Road to L4

## Self-Healing Software, Part Eight
- The finale: how healing fails
- 8 anti-patterns, 8 controls
- lks-shs · the PULSE series

The finale. Every healing mechanism in this series can fail, and most fail in one of eight documented ways. The good news: each has a control with a verified precedent. The bad news: the controls are boring, so organizations skip them.

## The eight anti-patterns
- over-broad write access · acting on correlation
- the model grading its own homework
- velocity eroding stability · human skill atrophy
- contaminated memory · hype whiplash · prompt injection

The eight: over broad write access. Acting on correlation instead of causation. The model grading its own homework. Velocity quietly eroding stability. Human skill atrophy. Contaminated incident memory. Hype whiplash. And prompt injection, which becomes an operational security issue the moment an agent can delete things.

## The canonical failure
- Anthropic's agent: ~200 workloads deleted in 90 seconds
- authorized action, unbounded execution
- controls: rate caps, budgets, undo tests, agent identity

The canonical failure is worth repeating. An agent at Anthropic deleted about two hundred workloads in ninety seconds. Authorized. Not a hallucination. The fix was rate caps per hour and resource kind, replenishing budgets, an undo test before any write grant, and identity assigned by infrastructure. Not one word of prompt engineering.

## Boring controls, multiple risks
- non-LLM validators catch anti-patterns 3 and 4
- least-privilege + allow-lists cover 1 and 8
- human gates cover 2, 5, 6

Notice the pattern: boring controls cover multiple exciting risks. Validators that are not models catch hallucinated fixes and stability drift. Least privilege and allow lists cover both runaway actions and injection. Human gates cover misdiagnosis, atrophy, and poisoned memory.

## The honest L4 checklist
- ❌ first-party autonomous-remediation account w/ audit trail
- ❌ independently audited MTTR study of any AI-SRE
- ❌ audit standards covering agent actions
- ❌ sub-$100/month agentic IR for small business

What nobody has shipped yet: a first party account of a fully autonomous remediation decision with its audit trail. An independently audited recovery study of any A I S R E product. Audit standards that name agent actions. An affordable agentic product for small business. Cross rung four when those turn into check marks, one at a time.

## The series in one sentence
- seventy years of layered healing loops
- one new organ: the AI decide stage
- one rule: nothing is healed until an oracle that isn't the healer says so

The series in one sentence. Seventy years of layered healing loops, one new organ, the A I decide stage, and one non negotiable rule: nothing is healed until an oracle that is not the healer says so. Run the prototype. Read the dossiers. Check our evidence. Thanks for watching.
