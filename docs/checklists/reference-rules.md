# Reference Rules — how this project builds things

Numbered, binding rules for every artifact in this repo. (v0.1 — enriched during Phase 6 verification.)

- **R1 · Citation discipline.** Every factual claim in a dossier, post, or article cites a primary source (author/org, year, URL, access date). Sources are fetched and verified before citing. Unverifiable claims are marked `[UNVERIFIED]` and never graduate into posts.
- **R2 · Decision discipline.** Every significant design choice is recorded with **3–5 alternatives, trade-offs, and a justified recommendation**. "Why this and why not that" is answered in writing, not implied.
- **R3 · Diagram discipline.** Every diagram declares its abstraction level (layer, scope, time horizon) and its source of truth (which doc/spec it visualizes). Mermaid must render on GitHub.
- **R4 · Attribution.** Ideas are credited to their originators (e.g., MAPE-K → IBM Autonomic Computing; "let it crash" → Joe Armstrong). Adaptation is fine; silent borrowing is not.
- **R5 · Prototype discipline.** Every prototype runs with one command, includes failure injection (no demo without a wound to heal), and links its decision record.
- **R6 · Video discipline.** Every video links to its post and vice versa; narration scripts are committed next to renders.
- **R7 · Verification gates.** No deliverable is marked done in `master-checklist.md` without recorded evidence. Improvement loops continue until the competency bar (all items ✓) is met.
- **R8 · Audit trail.** Every user request and response archived in `docs/prompt-histories/` the same turn; INDEX regenerated; folders organized regularly.
- **R9 · Audience clarity.** Every recommendation states who it is for (small business vs enterprise) and what it costs.
- **R10 · Same facts, four altitudes.** The four audience articles must be factually consistent with each other and with the posts; differences are framing, not facts.
