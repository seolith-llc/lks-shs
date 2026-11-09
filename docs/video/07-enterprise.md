# Episode 07 · The Enterprise Playbook

## Self-Healing Software, Part Seven
- The enterprise playbook
- Governance, gates, FinOps
- lks-shs · the PULSE series

Part seven is for platform and S R E leads. The economics are almost absurd; the risk is unmeasured autonomy.

## The economics
- 54% of significant outages cost >$100K (Uptime Institute)
-! >$300K/hr | downtime cost for 90% of firms (ITIC)
-! ~$400B/yr | losses across the Global 2000 (Oxford Economics)

Downtime runs over three hundred thousand dollars an hour for ninety percent of firms. One in five significant outages costs more than a million. Across the Global two thousand, roughly four hundred billion a year. A fifty dollar per user tool that shaves minutes off recovery pays for itself per incident.

## Six governance rules
- human gates at write boundaries (PR review)
- blast-radius limits in infrastructure, not prompts
- read-only by default · agent identity in the audit trail
- non-LLM validators on every AI fix · reviewed postmortems only

Six rules, each with a verified precedent. System changes land as human reviewed pull requests. Blast radius limits live in admission webhooks and rate caps, not prompts. Agents start read only. Agent actions are audit principals on the same immutable trail as humans. Every A I fix passes a validator that is not a model. And only human reviewed postmortems enter the incident memory.

## The rollout ladder
- L0 observe → L1 investigate → L2 propose → L3 bounded actuation → L4
- advance per action class on measured MTTR deltas
- L4 closed loop: nobody verified in production yet

Roll out autonomy like a ladder, not a switch. Observe, then investigate, then propose pull requests, then bounded actuation. Advance one action class at a time, gated on measured recovery deltas and audit findings. Rung four remains unverified anywhere. Design for it; do not claim it.

## FinOps in one example
- 8 on-call users × $50/month = $4,800
- break-even at ~1 incident/month (10 minutes saved)
- caveat: vendor-cited numbers — measure your own deltas

The worked example: eight on call users at fifty dollars a month is forty eight hundred a month. At three hundred thousand an hour, saving ten minutes per incident breaks even once a month. One caveat: those speedup numbers are vendor cited. Measure your own deltas before advancing any rung.

## The audit gap
- no SOC 2 / ISO control text names "actions by an AI agent"
- own it now: agent identity, PR evidence, immutable logs
- don't discover it during an incident review

One gap to plan around: no audit standard yet names actions taken by an A I agent. Vendors certify the platform, not the agent. Until standards catch up, your auditable artifacts are agent identity, pull request evidence trails, and rate cap configs. Own that in your next audit cycle. Next, the finale: risks and anti patterns.
