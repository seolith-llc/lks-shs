# Instagram Reels / TikTok — captions for the 4 shorts (paste-ready)

> Videos: `docs/video/shorts/s1–s4` (1080×1920, 46–54 s). The repo URL is burned into every frame; also add link-in-bio.

## S1 · The nine-nines myth
**Caption:**
The most-quoted reliability number in software came from a PowerPoint slide. 📊

"99.9999999% availability" — the Erlang legend. Source, per Joe Armstrong's own thesis: a slide whose methodology "was not documented."

Healing claims are cheap. Evidence is precious.

🔗 Full story (180 sources) — link in bio

**Hashtags:** `#softwareengineering #programming #erlang #reliability #techhistory #sre #learntocode #coding #softwaredeveloper #howitworks`

## S2 · The retry storm
**Caption:**
Your retry logic just DDoSed yourself. 🌀

5 layers deep × 3 retries each = **243× the load** on a service that's already dying.

Fix: capped backoff + jitter + retry budgets. AWS did the math — it's in the repo.

🔗 Link in bio

**Hashtags:** `#backend #systemdesign #microservices #cloudcomputing #awscertified #softwareengineering #coding #distributedsystems #sre #tech`

## S3 · 200 workloads in 90 seconds
**Caption:**
An AI agent deleted 200 workloads in 90 seconds — at an AI lab. ⚠️

Not a hallucination. An authorized action with no speed limit.

The fix wasn't a better prompt: rate caps, budgets, undo tests, agent identity — in infrastructure.

If you're giving agents production access, steal this postmortem. 🔗 bio

**Hashtags:** `#ai #aiagents #devops #platformengineering #security #incidentresponse #llm #aiops #technews #sre`

## S4 · PULSE in 45 seconds
**Caption:**
Every self-healing system ever built runs the same 5 steps. 🫀

Perceive → Understand → Localize → Solve → Evolve.

One rule: nothing is healed until something that ISN'T the healer says so.

There's a prototype you can crash yourself. One command. 🔗 bio

**Hashtags:** `#softwarearchitecture #systemdesign #reliabilityengineering #kubernetes #aiops #programming #techexplained #learntocode #sre #coding`

---

## Instagram carousel option (10 slides, static)
1. "Software that heals itself — 70 years in the making" (PULSE wordmark)
2. 1956–1999: engineered recovery (TMR, recovery blocks, BFT)
3. 2003: IBM names the loop — MAPE-K
4. The myth slide: 99.9999999% ← from a PowerPoint (per Armstrong's thesis)
5. Pre-AI: sensing ✅ actuation ✅ decide ❌ (frozen thresholds + a 3am page)
6. 2023→2026: 1.96% → 87.6% on SWE-bench
7. What shipped: AI investigates; humans still gate the fixes
8. The 200-workloads-in-90-seconds story
9. PULSE: the loop + the one rule (non-AI oracle)
10. "Clone it. Crash it. It heals." → github.com/seolith-llc/lks-shs

(Slides 2–10 can be exported from the video slide generator or the animated SVGs; ask and they render in minutes.)
