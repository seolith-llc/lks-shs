# Hacker News / Reddit / Lobsters — launch posts (paste-ready)

## Hacker News — Show HN

**Title:** `Show HN: PULSE – a self-healing software framework with 180 sources and a runnable prototype`
**URL:** `https://github.com/seolith-llc/lks-shs`
**Text (first comment, from the submitter):**

> I spent the past day researching and building this end to end: a 180-source, citation-verified corpus on self-healing software (academic foundations → the pre-AI industrial playbook → the systems layer → the 2024–26 AI-ops market), one framework distilled from it, and a runnable proof.
>
> The framework is PULSE (Perceive–Understand–Localize–Solve–Evolve) — a MAPE-K descendant with two additions the last 20 years forced: explicit fault-localization, and a mandatory non-LLM verification gate between Solve and Evolve. Nothing counts as healed until tests/metrics/golden-requests say so.
>
> The prototype (prototypes/pulse-app) is ~600 lines of stdlib Python: an external supervisor that heals crash/hang/leak/error faults with capped backoff and OTP-style MaxR/MaxT escalation — when the fault is deterministic it refuses to thrash and pages instead, which is deliberately the least "AI" and most defensible part of the design.
>
> Findings that surprised me: the Erlang "nine nines" number is from an undocumented PowerPoint slide (per Armstrong's own thesis); naive retries can amplify load 243×; the entire verified AI-SRE market converges on "investigate autonomously, remediate through human gates"; and nobody has published a first-party account of fully autonomous remediation with an audit trail. Everything is in the dossiers with access dates; unverifiable claims are marked [UNVERIFIED] rather than repeated.
>
> Happy to go deep on any layer — kernel live patching, the MAPE-K lineage, the vendor landscape, or the prototype's escalation policy.

## Reddit — r/SRE (text post)

**Title:** `I researched self-healing software across 180 verified sources and built a working PULSE-loop prototype (crash/hang/leak/rollback, OTP-style escalation) — everything open-sourced`
**Body:** adapt the HN first-comment above, plus one line: "Also wrote four versions of the findings for different audiences (ELI5 → C-suite) in docs/articles/ — the C-suite one includes three questions worth asking any AI-ops vendor before renewal."

## Reddit — r/programming (link post)

**Title:** `Self-healing software, engineered with AI: 180 verified sources, the PULSE framework, and a prototype you can crash in one command`
**URL:** repo link. Keep comments factual, cite dossiers, avoid marketing tone.

## Lobsters

**Title:** `Self-healing software with AI: the PULSE framework and a runnable healing-loop prototype`
**URL:** repo link · **Tags:** `ai, reliability, show, practices`

## Timing & etiquette notes (from the corpus + platform norms)

- Show HN: Tuesday–Thursday morning ET; answer every comment in the first 2 hours; lead with what's verifiable (sources, prototype).
- Reddit: one subreddit at a time, days apart; r/SRE first (most on-topic), then r/programming; tailor titles per sub rules.
- Never post the same URL to multiple HN-adjacent communities the same day.
