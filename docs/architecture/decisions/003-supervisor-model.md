# Decision 003 — Supervisor Architecture

**Status:** ACCEPTED · **Date:** 2026-11-09 · **Context:** the PULSE loop needs an executor. Where does the healer live relative to the healed?

## Alternatives

1. **In-process (threads inside the service)** — simplest possible: a watchdog thread restarts handlers.
   *Trade-offs:* **fatal flaw** — the healer dies with the patient; cannot restart a crashed process. Also violates the corpus's founding pattern: the supervisor must outlive the supervised (Armstrong's whole argument, D02[1]; systemd/kubelet are separate by design, D02[7][20]).
2. **External supervisor process (`subprocess.Popen` + poll loop)** — supervisor.py spawns, watches, kills, respawns the service.
   *Trade-offs:* small amount of process-management code; signals/exit codes to handle; **but** it models the real world exactly (systemd, kubelet, OTP supervisor are all external), makes crash/hang faults genuinely healable, and keeps every PULSE stage visible in one readable file.
3. **Docker / docker-compose with restart policy + healthcheck** — one YAML, very production-shaped.
   *Trade-offs:* delegates the *entire* Decide stage to Docker's fixed policy — the loop becomes opaque exactly where the teaching value is; needs the Docker daemon (heavier, occasionally flaky in sandboxes); backoff/intensity policy not expressible.
4. **k3s Deployment + probes** — the real Kubernetes story (self-healing by declaration, D02[20][21]).
   *Trade-offs:* maximal realism, but ~1 GB of machinery; reconciliation happens inside k8s where you cannot watch it tick; escalation-to-human (MaxR/MaxT) has no first-class knob (CrashLoopBackOff just *waits*).
5. **systemd units (`Restart=on-failure`, `WatchdogSec=`)** — the most authentic Linux lineage (D02[7][25]).
   *Trade-offs:* macOS-hostile (dev machine is darwin); needs root-ish config; the loop's logic is again inside systemd, unreadable.

## Decision

**External supervisor process (2).** It is the only option that simultaneously (a) makes every wound class truly healable, (b) keeps every PULSE stage inspectable in ~250 lines, (c) runs anywhere Python runs, and (d) faithfully mirrors OTP/systemd/kubelet semantics — including capped backoff and MaxR/MaxT escalation, which the container-native options (3, 4) cannot express at all. The prototype README explicitly names the mapping: `supervisor.py` ≈ systemd/kubelet/OTP-supervisor in miniature.
