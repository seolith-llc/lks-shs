# Decision 004 — AI Triage in the Prototype

**Status:** ACCEPTED · **Date:** 2026-11-09 · **Context:** the series' subject is *self-healing with AI*, so the prototype should show where AI goes — but demos must be reproducible (R5, R7).

## Alternatives

1. **No AI at all** — pure mechanics (restart/rollback only).
   *Trade-offs:* honest about L0 but silently drops the project's entire differentiator; the demo wouldn't distinguish itself from `systemd` since 2010.
2. **Deterministic rule-based investigator** — evidence in → ranked hypotheses with confidence → explicit human-gate note; shape mirrors L1 exactly.
   *Trade-offs:* not *actually* intelligent; but reproducible, offline, instant, and the *interface* (JSON in/out) is the real one an LLM would use.
3. **Optional live LLM via env API key** — call an OpenAI-compatible endpoint when `PULSE_LLM_KEY` is set.
   *Trade-offs:* real LLM RCA; but demos become flaky/slow/costly, and unverified network dependence violates the reproducibility bar for evidence logs.
4. **Full agentic loop (LLM decides + acts)** — model picks remediation and executes.
   *Trade-offs:* spectacular when it works; non-reproducible, unverifiable by a non-LLM oracle in-benchmark — and it would misrepresent the verified industry frontier, which stops at PR-gated fixes + bounded actuation (D04 §builder-vs-healer). A demo that overclaims autonomy would contradict our own axiom A6/D04 governance rules.

## Decision

**(2) deterministic investigator with a pluggable external hook (`PULSE_TRIAGE_CMD`).** The prototype demonstrates the *verified* frontier precisely: autonomous-looking diagnosis (L1), gated repair (L2 note), bounded actuation (restart/rollback) — and the README documents how to graft a real LLM without touching the supervisor. Option (4) is deliberately rejected as dishonest for this project's evidence standards: if we later build an L2 PR-gate demo with a live model, it will run behind the same verification-gate discipline the architecture mandates.
