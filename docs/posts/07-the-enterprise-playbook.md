# Part 7 · The Enterprise Playbook

*Series: [Overview](00-series-overview.md) · [Part 6](06-the-small-business-playbook.md) · **Part 7** · [Part 8](08-risks-anti-patterns-road-to-l4.md)*
**Audience:** platform/SRE leads, engineering directors · ~9 min · Video companion: [`docs/video/07-enterprise.mp4`](../video/07-enterprise.mp4) — 2:05 narrated

> The economics are almost absurd: downtime runs **>$300K/hour for 90%+ of firms** (ITIC 2024) [1], 54% of significant outages cost >$100K and 1-in-5 exceed $1M (Uptime Institute 2025) [2], and the Global 2000 lose an estimated **$400B/year** (Oxford Economics/Splunk) [3]. A $50/user/month tool that shaves minutes off MTTR pays for itself per incident. The risk isn't the spend — it's **unmeasured autonomy**: Gartner expects >40% of agentic AI projects to be canceled by end-2027, mostly on cost, unclear value, and inadequate risk controls [4].

## The six governance rules (each with a verified precedent)

1. **Human gates at write boundaries.** System changes land as human-reviewed PRs — the pattern incident.io states explicitly [5]; Better Stack: "never … without your approval" [6]. PR review reuses the permissioning, audit, and CI you already run.
2. **Blast-radius limits live in infrastructure, not prompts.** After Anthropic's agent deleted ~200 workloads in 90 seconds, the fix was an admission webhook capping deletions per hour/resource-kind/namespace, replenishing write budgets, an "undo test," and infrastructure-assigned identity [7].
3. **Read-only by default.** Agents start as Observers and earn writes (Traversal's default [8]; the OODA framing: superhuman Observe, dangerous Orient [9]).
4. **Agent identity is an audit principal.** Every agent action logged to the same immutable trail auditors already sample; per-session VMs, RBAC/SSO (Devin [10]), zero-retention options (Datadog [11]).
5. **Every AI fix passes a non-LLM validator.** CodeQL re-run [12], SAST pre-screen [13], test execution [14]. Never let a model certify its own fix.
6. **Human-validated postmortems only** enter the incident memory — unreviewed AI RCAs poison future retrieval [15].

## The rollout ladder

| Rung | What ships | Verified precedent | Exit evidence to advance |
|---|---|---|---|
| **L0 Observe** | agent reads telemetry, answers questions | Bits Chat [11]; Rootly MCP [16] | usage + zero write incidents |
| **L1 Investigate** | auto-investigation on every alert, SITREPs w/ evidence | Claude Tag 14-min SITREPs [7] | RCA helpfulness rate vs. human baseline |
| **L2 Propose** | fix PRs, CI + human review + validators mandatory | agentic autofix [12]; Snyk [13] | validator pass-rate, merge rate, regression rate |
| **L3 Act (bounded)** | pre-authorized reversible actions, rate-capped, identity-scoped | Resolve rollbacks [17]; Anthropic's caps [7] | MTTR delta + audit findings per action class |
| **L4 Close the loop** | unattended remediation w/ audit trail | *none verified — announced only* [18] | (design for it; don't claim it) |

**Advance one rung at a time, per action class, on measured evidence.** That discipline is what Gartner's cancellation forecast prices in [4] — and what DORA's −7.2% stability-per-adoption finding demands [19].

## FinOps in one worked example

- Downtime at $300K/hour [1]; on-call team of 8 × $50/user/month AI tooling = **$4,800/month**.
- If agentic investigation saves **10 minutes per incident** (PagerDuty early adopters report "up to 50% faster" — vendor figure [20]; Datadog claims 90% faster restore — vendor [11]; RCACopilot's 0.766 accuracy is the published-research anchor [15]), break-even is **~1 incident/month**. Most enterprises page far more.
- The honest caveat set: vendor-cited MTTR numbers, no independently audited study exists yet (dossier 04 negative results) — so **measure your own MTTR delta per rung** before advancing.

## The audit gap to plan around

No SOC 2 / ISO 27001 control text yet names "actions taken by an AI agent" — vendors certify the *platform*, not the agent's actions. Until standards catch up: agent-as-principal identity, PR-based evidence trails, immutable action logs, and rate-cap configs are your auditable artifacts [7][10]. Own this in your next audit cycle rather than discovering it during an incident review.

## References & attribution

Full sourcing: [`docs/research/04-ai-era-and-business.md`](../research/04-ai-era-and-business.md) §enterprise playbook

1. ITIC, *2024 Hourly Cost of Downtime* — https://itic-corp.com/itic-reports-surveys/
2. Uptime Institute, *Annual Outage Analysis 2025* — https://intelligence.uptimeinstitute.com/resource/annual-outage-analysis-2025
3. Oxford Economics / Splunk, *The Hidden Costs of Downtime*, 2024 — https://www.oxfordeconomics.com/resource/the-hidden-costs-of-downtime-the-400b-problem-facing-the-global-2000
4. Gartner, *>40% of agentic AI projects canceled by 2027*, 2025 — https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027
5. incident.io, *Investigations* — https://incident.io/investigations
6. Better Stack, *AI SRE* — https://betterstack.com/ai-sre
7. S. Malhotra (Anthropic), 2026 — https://ai.engineer/speakers/sachin-malhotra
8. Traversal — https://www.traversal.com/
9. A. Palcuie (Anthropic) via InfoQ, 2026 — https://www.infoq.com/presentations/claude-sre-incidents/
10. Cognition, *Devin* — https://devin.ai
11. Datadog, *Bits AI* — https://www.datadoghq.com/product/ai/
12. GitHub, *Agentic autofix GA*, 2026 — https://github.blog/changelog/2026-10-15-agentic-autofix-for-code-scanning-alerts-general-availability/
13. Snyk, *Agent Fix*, 2025 — https://snyk.io/blog/building-ai-trust-with-snyk-code-and-snyk-agent-fix/
14. Alshahwan et al., *TestGen-LLM*, FSE 2024 — https://arxiv.org/abs/2402.09171
15. Y. Chen et al., *RCACopilot*, EuroSys 2024 — https://arxiv.org/abs/2305.15778
16. Rootly, *Rootly AI* — https://rootly.com/ai
17. Resolve AI — https://resolve.ai/
18. Palo Alto Networks / Cortex AgentiX announcement — see dossier 04 negative results
19. Google Cloud, *2024 DORA Report* — https://cloud.google.com/blog/products/devops/sre/announcing-the-2024-dora-report
20. PagerDuty, *AI agent suite launch*, 2025 — https://www.pagerduty.com/newsroom/2025-fall-productlaunch/

**Next:** [Part 8 — risks, anti-patterns, and the road to L4 →](08-risks-anti-patterns-road-to-l4.md)
