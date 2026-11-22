---
step: "#Step010 — publication site (built + verified; deploy awaiting user confirmation)"
turn: 14
timestamp: 2026-11-22 14:59 EST
---

# Request

Can we publish these articles?

# Response

**Answer: yes — ready.** Executed everything publishable without user credentials:

**1. Publication site built** — `publish/site/build_site.py` (stdlib static generator, committed; output gitignored & regenerable): index (hero + series cards + four-altitude articles + video pointers), 8 post pages, 4 article pages, the interactive simulator, animated SVGs — same navy/gold design system; mermaid via CDN with `<pre>` fallback; repo-relative links absolutized to GitHub; post↔post links mapped to site pages.

**2. Verified locally:** all routes 200; browser check — mermaid renders as SVG, tables/headings correct. Visual judge round 1 **FAIL** → found one REAL bug: post 04's loop diagram used `**markdown**` bold inside mermaid labels (renders as literal marks) — fixed by converting labels to mermaid markdown-string syntax (also improves GitHub rendering); the other two complaints were capture-mechanics artifacts (2160px viewport cap truncated the page; the table exists in the DOM below the cut). Stage rebuilt, `zcode-site check` → **live/200** (after fixing my own staging slip: files at stage root vs `SITE_DIR=site`).

**3. Deployment NOT executed** — the site-deploy protocol requires an explicit user yes before the first public deploy, and the confirmation question went unanswered. Stage sits ready in `.zcode-site/stage/` (gitignored). Trigger: one word from the user → `zcode-site deploy --new --name "PULSE — Self-Healing Software, Engineered with AI" --prefix pulse-self-healing`.

**4. dev.to:** no `DEVTO_API_KEY` in env — the 8 prepared exports (`publish/articles/devto/`) remain ready for either the manual 2-minute import or the automation once a key is provided (creates unlisted drafts only).

Visual judge round 2 (fixed diagram) launched; verdict will gate the deploy.

# Decisions

- Deployment held pending explicit user confirmation (protocol + outward-facing action; unanswered question ≠ consent).

# Artifacts

- Created: `publish/site/build_site.py`, this file
- Updated: `docs/posts/04` (mermaid markdown-string labels), `.gitignore` (site output, .zcode-site), INDEX, checklist
- Commit + push
