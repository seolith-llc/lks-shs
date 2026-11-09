# Self-Healing Software — Axioms

**Status: all 12 VERIFIED (Phase 6, 2026-11-09).** Each axiom now carries its evidence from the research corpus (D01–D04 = dossiers), the decision records (DR), and/or the runnable prototype. Evidence keys: `D0n[m]` = dossier n, source m · `DRn` = decision record · `proto` = prototypes/pulse-app (5/5 PASS, evidence log).

| # | Axiom | Evidence | Status |
|---|---|---|---|
| A1 | **Everything fails; design for recovery, not perfection.** | Armstrong's thesis: large programs *will* contain errors, so build systems that "behave in a reasonable manner in the presence of software errors" (D02[1]); Nygard's stability patterns from post-mortems (D02[5]); Gray's Tandem finding that most faults are transient (D02[1]) | ✅ verified |
| A2 | **Healing without learning is just rebooting.** | MAPE-K's K (D01[2]); RCACopilot incident memory at 0.766 RCA accuracy (D03[50]); self-updating runbooks (D04[3]); prototype logs every heal as an Evolve artifact with triage + MTTR (proto) | ✅ verified |
| A3 | **The healer must not harm the patient.** | OTP MaxR/MaxT intensity limits (D02[1][2]); kubelet crash-loop backoff 10s→300s (D02[22]); Anthropic's agent deleting ~200 workloads in 90 s → infrastructure rate caps, not prompts (D04[31]); prototype crashloop scenario escalates by design (proto; DR5 symptom in DR007) | ✅ verified |
| A4 | **The monitor must not be the disease — and must not be fooled.** | Naive retries amplify load 243× (D02[10]); alert fatigue drives an entire correlation industry (D02[40][41]); self-reported health alone is a self-grading failure → layered out-of-band oracle (DR005) | ✅ verified |
| A5 | **Fail fast, heal fast.** | "Let it crash" + supervision trees (D02[1]); crash-only reasoning; systemd watchdog kills hangs rather than letting zombies linger (D02[7][25]) | ✅ verified |
| A6 | **A fix that isn't verified is a guess.** | GitHub re-runs CodeQL before the PR (D04[17]); Snyk SAST-screens candidates (D04[18]); TestGen-LLM's 73% acceptance *through* build+test filtering (D04[30]); SWE-bench requires FAIL_TO_PASS (D01[21]); prototype's Solve→Evolve gate refuses "healed" without golden PULSE-OK (proto; DR001) | ✅ verified |
| A7 | **Declare health; converge to it.** | Borg/k8s level-triggered reconciliation (D02[19][20]); ZFS repairs toward the checksummed-correct state (D03[22]); WAL redo converges to consistency (D03[26]) | ✅ verified |
| A8 | **Autonomy is earned in levels.** | The L0–L4 ladder with verified exemplars per rung (D04 §rollout; 00-synthesis §4); no verified L4 deployment exists (D04 negative results) | ✅ verified |
| A9 | **Detection without diagnosis is noise.** | Alert storms → correlation products (D02[40][41]); LLMs "jagged": strong Observe, weak Orient (D04[32]); challenger agents and code-set confidence as countermeasures (D04[4][5]) | ✅ verified |
| A10 | **Prevention is the cheapest cure.** | ~70% of Microsoft/Chromium CVEs are memory-safety (D03[30][31]); Android 76%→24% via Rust (D03[33]); OSS-Fuzz 36k+ bugs (D03[37][38]) | ✅ verified |
| A11 | **The last responsible human is part of the loop.** | PR-gated healing at incident.io/Better Stack (D04[4][10]); SapFix's mandatory engineer approval (D03[41]); human-validated postmortems before memory entry (D04 §risks) | ✅ verified |
| A12 | **Small businesses heal differently.** | The $0–50/mo stack with restore drills as the real healer; agentic IR unavailable below enterprise pricing (D04 §small-business + negative results) | ✅ verified |

## How to use these

The axioms are the review checklist for any self-healing design: walk A1–A12 against the design and be able to cite your own evidence for each. The [reference architecture](../architecture/reference-architecture.md) encodes them as its seven binding rules; the [pattern catalog](../architecture/pattern-catalog.md) anti-patterns are their violation modes.
