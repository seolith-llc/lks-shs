# Part 6 · The Small-Business Playbook ($0–50/month)

*Series: [Overview](00-series-overview.md) · [Part 5](05-pulse-in-python.md) · **Part 6** · [Part 7](07-the-enterprise-playbook.md)*
**Audience:** 1–20 person shops, no SRE team · ~7 min · Video companion: `docs/video/06-small-business.mp4` *(renders in Phase 5)*

> You cannot buy an AI SRE. Every agentic incident product on the verified market is enterprise-priced or custom-quoted [1][2][3]. What you *can* have — tonight, for roughly the price of one coffee per month — is genuine self-healing: detection that never sleeps, restarts that happen without you, deploys that roll themselves back, and backups you have actually restored. The binding constraint is discipline, not money.

## The stack, tier by tier

| Tier | Tool | What it heals | Cost |
|---|---|---|---|
| **0 · free** | [Uptime Kuma](https://github.com/louislam/uptime-kuma) — HTTP/TCP/ping checks, 20 s cadence, 90+ notifiers | detects outages & keyword regressions | $0 (a $5 VPS) |
| | [Healthchecks.io](https://healthchecks.io/pricing/) — **dead man's switch** | catches silent failures: backups, cron, cert renewal that *stop* running | free: 20 checks |
| | [k3s](https://k3s.io/) — single-binary Kubernetes | restarts/replaces crashed pods for you | $0 |
| | Grafana OSS LGTM stack — Prometheus + Loki | metrics + logs + alerting | $0 self-hosted |
| | [n8n](https://n8n.io/pricing/) — automation glue | restart-on-alert workflows, escalation | $0 self-hosted |
| **1 · ~$20–80/mo** | [Render](https://render.com/docs/zero-downtime-deploys)-style managed platform | **health-check-gated deploys with auto-rollback** — a failed new version never takes traffic | managed pricing |
| **2 · the real healer** | [restic](https://restic.net/) — encrypted, deduplicated, verifiable backups | the only true cure for data loss | $0–5 storage |

## Your 3 a.m., walked through the stack

1. **Bad deploy with a memory leak.** Platform health check fails on the new instance → deploy canceled → **previous version keeps serving**. Zero downtime, zero humans. *This is the single highest-value self-healing a small business can own.*
2. **Slow-burn degradation that passed the health check.** Uptime Kuma keyword check fires on a 20 s interval → you get a Telegram message at 7 a.m., not a silent churned customer base. Detection only — which is why your rollback runbook is pre-written.
3. **Worker OOMs.** k3s restarts the pod; n8n retries the step. Crude, genuine, automatic.
4. **Nightly database backup silently stopped.** No uptime check catches *absence* — the dead man's switch does. *This is the check most shops never install and most regret not having.*
5. **Disk corruption / ransomware.** restic snapshots + last month's **restore drill**. A backup that has never been restored is a hope, not a system.
6. **Mystery 500s.** Copilot-assisted debugging on the collected logs; optionally a bounded LLM summarizer script (evidence gathering, human decides — the Anthropic first-responder pattern, scaled down [4]).

## What not to buy yet (and what to do instead)

- **Autonomous RCA / remediation products** — enterprise-priced today [1][2][3]; and the verified evidence base for unattended actuation is one failure story, not a success story [4][5]. Skip.
- **Do** the DIY bridge: a cron script that collects logs/metrics on alert and asks an API model to summarize candidate causes for the human on call. Cheap, bounded, read-only.
- **Five runbook cards** for your top five failure modes (restart command, rollback command, restore command, DNS/provider contacts, "who do we call"). Cost: one afternoon. This is your L2 gate.

## The honest budget

Roughly **$5–15 hosting + $0–5 backups + $0–20 managed upgrades** per month. The discipline costs more than the money: monthly restore drills, the five runbook cards, alerting simple enough that pages get read.

## References & attribution

Full sourcing: [`docs/research/04-ai-era-and-business.md`](../research/04-ai-era-and-business.md) §small-business playbook

1. Traversal — https://www.traversal.com/ (enterprise pricing model)
2. Resolve AI — https://resolve.ai/ (custom pricing)
3. Rootly pricing — https://rootly.com/pricing (AI SRE custom)
4. S. Malhotra (Anthropic), *Claude on call*, 2026 — https://ai.engineer/speakers/sachin-malhotra
5. OWASP Top 10 for LLM & GenAI 2025 (LLM06 Excessive Agency) — https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/

**Next:** [Part 7 — the enterprise playbook: autonomy ladders, gates, and FinOps →](07-the-enterprise-playbook.md)
