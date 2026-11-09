# Part 8 · Risks, Anti-Patterns, and the Road to L4

*Series: [Overview](00-series-overview.md) · [Part 7](07-the-enterprise-playbook.md) · **Part 8** (finale)*
**Audience:** everyone who signs off on autonomy · ~8 min · Video companion: [`docs/video/08-risks.mp4`](../video/08-risks.mp4) — 1:54 narrated

> Every healing mechanism in this series can fail, and most fail in one of eight documented ways. The good news: each has a control with a verified precedent. The bad news: the controls are boring infrastructure, so organizations skip them for prompts.

## The eight anti-patterns

**1 · Over-broad write access.** The canonical failure: Anthropic's own agent — authorized, not hallucinating — deleted **~200 workloads in 90 seconds** because an authorized action ran unboundedly [1]. *Control: rate caps per hour/kind/namespace, replenishing budgets, an undo test before any write grant, agent-scoped identity — in infrastructure, not prompts* [1].

**2 · Acting on correlation.** Claude read a KV-cache failure as a capacity problem because requests and errors rose together; corrections don't generalize [2]. *Control: autonomous Observe, human Decide; challenger agents; confidence set by code, not the model* [2][3][4].

**3 · The model grades its own homework.** An agent that generates and certifies its own fix drifts. *Control: non-LLM validators inside every fix pipeline* — GitHub re-runs CodeQL [5], Snyk re-runs SAST [6], Meta's TestGen-LLM filters through build+test before a human ever sees a suggestion [7].

**4 · Velocity eroding stability.** DORA 2024: each +25% AI adoption correlated with **−7.2% delivery stability** [8] — AI-assisted shipping without expanded validation quietly funds its own incident workload. *Control: track throughput and stability together; grow the gates as adoption grows* (Sonar's AI Code Assurance pattern [9]).

**5 · Skill atrophy.** Without incident pain, juniors miss formative training and seniors lose the incentive to fix root causes — plus a Jevons paradox: cheaper software means more software, means more incidents [2]. Uptime Institute's rising "procedures-not-followed" numbers hint the competence layer is already thin [10]. *Control: keep humans on Decide/Act rungs, run agent-free drills, review incidents for root-cause fixes.*

**6 · Contaminated memory.** Unreviewed AI postmortems poison the incident store that future agents retrieve against [2][11]. *Control: human-validated RCAs before they enter retrieval; "insert a todo for a human" markers on uncertainty* [11].

**7 · Hype-cycle whiplash.** Devin's launch demos vs. independent reproduction; "agent washing"; a crowded AI-SRE category a competitor-CEO expects to compress within two years [12][13]. *Control: procurement rule — **no autonomy before audit trails**; demand first-party evidence, not launch videos.*

**8 · Prompt injection as an ops attack path.** Once an agent can restart, roll back, or delete, injection stops being a chatbot nuisance and becomes an operational-security issue — OWASP keeps Prompt Injection #1 and expanded Excessive Agency (LLM06) precisely for this agentic reason [14]. *Control: least-privilege tool surfaces, allow-listed actions, human approval on writes* — same controls as #1, which is the point: **boring controls cover multiple exciting risks.**

## Risk → control → precedent (the table to steal)

| Risk | Control | Verified exemplar |
|---|---|---|
| authorized action, unbounded | rate caps, budgets, undo tests, agent identity | Anthropic post-incident webhooks [1] |
| wrong root cause at machine speed | diagnose-only defaults, human Decide, challengers | Claude Tag [1]; Rootly challenger agents [3] |
| hallucinated/regression fix | non-LLM validators in-pipeline | CodeQL re-run [5]; SAST screen [6]; TestGen-LLM [7] |
| excessive agency | least-privilege tools, allow-lists, approval on writes | OWASP LLM06 [14]; Better Stack [15] |
| poisoned incident memory | human-validated postmortems only | RCACopilot OCE validation [11] |
| stability drift | DORA-style dual tracking, growing gates | DORA 2024 [8]; Sonar [9] |
| human skill atrophy | humans stay on gates; agent-free drills | Palcuie's atrophy warning [2] |
| unauditable actions | agent-as-principal, PR evidence, immutable logs | Devin audit logs [16] |

## What nobody has shipped yet (the honest L4 checklist)

- ❌ No first-party account of a fully autonomous remediation decision with its audit trail — good *or* bad (the Anthropic deletion remains the only detailed failure account) [1]
- ❌ No independently audited MTTR study of any AI-SRE product — every effectiveness number is vendor- or customer-cited
- ❌ No SOC 2 / ISO control text covering actions taken by an AI agent
- ❌ No sub-$100/month agentic IR product for small businesses
- ❌ No peer-reviewed SRE-skill-atrophy data (first-party testimony only [2])

Cross L4 when those ❌ turn ✓ — one at a time, with evidence. Until then, the frontier is exactly where this series put the verification gate: **AI investigates and drafts; non-AI validators and humans certify; reversible actuation runs rate-capped; everything leaves an audit trail.**

> **The series in one sentence:** seventy years of layered healing loops, one new organ — the AI decide stage — and one non-negotiable rule: nothing is healed until an oracle that isn't the healer says so.

*Start over:* [Series overview](00-series-overview.md) · Run it: [`prototypes/pulse-app/`](../../prototypes/pulse-app/README.md) · Verify our own claims: [`docs/checklists/master-checklist.md`](../checklists/master-checklist.md)

## References & attribution

Full sourcing: [`docs/research/04-ai-era-and-business.md`](../research/04-ai-era-and-business.md) §risks

1. S. Malhotra (Anthropic), *Claude on call* + *Give the Agent a Budget*, 2026 — https://ai.engineer/speakers/sachin-malhotra
2. A. Palcuie (Anthropic), *Can Claude Fix Itself?*, QCon London 2026 via InfoQ — https://www.infoq.com/presentations/claude-sre-incidents/
3. Rootly, *Rootly AI* (challenger agents, code-set confidence) — https://rootly.com/ai
4. incident.io, *Investigations* (adversarial challenger) — https://incident.io/investigations
5. GitHub, *Agentic autofix GA*, 2026 — https://github.blog/changelog/2026-10-15-agentic-autofix-for-code-scanning-alerts-general-availability/
6. Snyk, *Agent Fix*, 2025 — https://snyk.io/blog/building-ai-trust-with-snyk-code-and-snyk-agent-fix/
7. Alshahwan et al., *TestGen-LLM*, FSE 2024 — https://arxiv.org/abs/2402.09171
8. Google Cloud, *2024 DORA Report* — https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
9. SonarSource, *AI Code Assurance*, 2025 — https://docs.sonarsource.com/sonarqube-server/2025.6/ai-capabilities/ai-code-assurance/
10. Uptime Institute, *Annual Outage Analysis 2025* — https://intelligence.uptimeinstitute.com/resource/annual-outage-analysis-2025
11. Y. Chen et al., *RCACopilot*, EuroSys 2024 — https://arxiv.org/abs/2305.15778
12. Techzine on Devin's launch claims, 2024 — https://www.techzine.eu/blogs/devops/117632/devin-is-the-first-ai-software-engineer-should-developers-worry
13. R. Ross, *The AI SRE Startup Landscape*, 2025 — https://www.bobbytables.io/p/the-ai-sre-startup-landscape
14. OWASP, *Top 10 for LLM & GenAI Applications (2025)* — https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/
15. Better Stack, *AI SRE* — https://betterstack.com/ai-sre
16. Cognition, *Devin* — https://devin.ai
