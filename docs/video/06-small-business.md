# Episode 06 · The Small-Business Playbook

## Self-Healing Software, Part Six
- The small-business playbook
- $0–50 per month
- lks-shs · the PULSE series

Part six is for one to twenty person shops with no S R E team. You cannot buy an A I S R E; every agentic product on the verified market is enterprise priced. What you can have, tonight, is genuine self healing.

## Tier zero, free
- Uptime Kuma — checks every 20 seconds
- Healthchecks.io — the dead man's switch
- k3s — restarts crashed pods for you
- Grafana OSS — metrics, logs, alerting

Tier zero costs nothing. Uptime Kuma watches your endpoints every twenty seconds. Healthchecks dot io is the dead man's switch that alerts you when a job silently stops running, which is the check most shops never install and most regret missing. k three s restarts crashed containers, and Grafana's open stack handles metrics and logs.

## Tier one: the highest-value heal
- managed platform, health-check-gated deploys
- new version fails its health check → previous version keeps serving
- zero downtime, zero humans

Tier one is the single highest value self healing a small business can own: a managed platform with health check gated deploys. If the new version fails its health check, it never takes traffic. Your previous version keeps serving. That is a whole class of outages simply deleted.

## Tier two: the real healer
- restic — encrypted, deduplicated, verifiable backups
- restore drills on a schedule
- "a backup never restored is a hope, not a system"

Tier two is the real healer: backups you have actually restored. Restic gives you encrypted, deduplicated, verifiable snapshots. Run a restore drill monthly. A backup that has never been restored is a hope, not a system.

## Your 3 a.m., walked through
- bad deploy → auto-rollback, no human needed
- worker OOMs → pod restarts itself
- backup silently stops → dead man's switch fires
- mystery 500s → collect evidence, human decides

Picture three a.m. The bad deploy rolled itself back. The crashed worker restarted itself. The silent backup failure paged you at a civilized hour because it failed to check in. And the mystery errors? A bounded script can collect the logs and summarize candidate causes for the human who decides.

## The honest budget
- $5–15 hosting + $0–5 backups + $0–20 managed upgrades
- the binding constraint is discipline, not money
- five runbook cards for your top five failures

The whole stack runs five to fifteen dollars a month for hosting plus a few for backups. The binding constraint is discipline: restore drills, five runbook cards, alerting simple enough that pages get read. Next: the enterprise playbook.
