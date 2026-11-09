# Prompt Histories

Every user request and assistant response in this project is archived here, verbatim, as one markdown file per turn.

## Naming

`YYYY-MM-DD_HHMMSS-slug.md` — e.g. `2026-11-09_090411_step000-bootstrap-and-step001-research-kickoff.md`

## File structure

```markdown
---
step: "#Step000"
turn: 1
timestamp: 2026-11-09 09:04 EST
---

# Request
<user message, verbatim>

# Response
<assistant response, verbatim markdown>

# Decisions
<any AskUserQuestion decisions made this turn, or "none">

# Artifacts
<files created / modified this turn>
```

## Maintenance (organize regularly)

- `INDEX.md` is re-generated whenever files are added: turn number, timestamp, step, title, one-line summary.
- Files are never edited after the turn ends (append `## Addendum` if a correction is needed).
- A periodic organization pass checks for gaps (every turn has a file), consistent naming, and a fresh index.
