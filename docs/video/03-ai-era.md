# Episode 03 · What Actually Shipped in the AI Era

## Self-Healing Software, Part Three
- The AI era, 2024 to 2026
- What shipped vs what's claimed
- lks-shs · the PULSE series

Part three is the buyer's episode: what actually shipped in the A I era, verified from first party pages, not launch videos.

## 2025: AI SRE becomes a product
- incident.io Investigations · Datadog Bits · PagerDuty SRE Agent · Rootly AI
- autonomous investigation of every alert
- the shared line: investigate autonomously, remediate through human gates

Twenty twenty five was the year A I S R E became a shipping product category. incident dot io, Datadog, PagerDuty, Rootly: all launched agents that investigate alerts and produce evidence cited root cause analyses. And notice how uniform the safety line is: investigate autonomously, remediate through human gates.

## Code-fixing AI went agentic
- GitHub agentic autofix: Copilot fixes CodeQL alerts
- validates by re-running CodeQL before the PR
- Snyk: up to 5 candidates, SAST-screened

On the code side, GitHub's agentic autofix assigns security alerts to Copilot, which explores the repo, writes a fix, and validates it by re running Code Q L before opening a draft pull request. Snyk generates five candidates per issue and never shows one that fails its own security scan.

## AI as builder vs AI as healer
- builder: fix PRs, tests, fuzz targets, runbooks — proven, cheap
- healer: investigation proven; remediation bounded + gated
- Anthropic's own engineer: Claude does not autonomously fix incidents

Keep two roles separate. A I as builder, hardening the machinery before incidents, is production proven and cheap. A I as healer is proven only in its observe and diagnose half, plus reversible pre authorized actions. Even Anthropic's own reliability engineer says it plainly: Claude does not autonomously fix incidents.

## The failure you must know
- Anthropic agent deleted ~200 workloads in 90 seconds
- authorized action, unbounded execution
- fix: rate caps, budgets, undo tests, agent identity — in infrastructure

The most instructive first party story: an Anthropic agent deleted about two hundred workloads in ninety seconds. It was not a hallucination; it was an authorized action executed unboundedly. The fix was not a better prompt. It was infrastructure: deletion rate caps, replenishing budgets, an undo test, agent scoped identity.

## The honest numbers
- SWE-bench: 1.96% (2023) → 87.6% SOTA (2026)
- agent task horizons double every ~7 months (METR)
- DORA: −7.2% delivery stability per +25% AI adoption
- Gartner: >40% of agentic AI projects canceled by 2027

The numbers cut both ways. Benchmark issue resolution went from two percent to nearly ninety in three years, and agent task horizons double every seven months. But each quarter more A I adoption correlates with a seven percent drop in delivery stability, and Gartner expects forty percent of agentic projects canceled by twenty twenty seven. Next episode: the PULSE framework that makes all of this safe.
