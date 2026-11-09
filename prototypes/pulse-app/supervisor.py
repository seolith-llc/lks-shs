#!/usr/bin/env python3
"""PULSE supervisor — an external healing loop around the demo service.

The supervisor is the *healer*; the service is the *patient*. It runs the
canonical PULSE loop (Decision 001) every tick:

  Perceive   : heartbeat age, process liveness, /health gauge, golden request
  Understand : classify the failure (CRASHED / HUNG / LEAKING / ERRORING)
  Localize   : name the component+layer responsible
  Solve      : restart with capped backoff, OR escalate to a human when the
               restart intensity limit is exceeded (OTP MaxR/MaxT pattern, D02[1][2])
  Evolve     : verify the heal (fresh heartbeat + golden PULSE-OK), measure MTTR,
               attach an L1 triage report, append the event to healing-log.jsonl

Design decisions: see docs/architecture/decisions/002-005.md.
Verification oracle is layered (Decision 005): dead-man's-switch heartbeat
(catches hangs) + out-of-band golden request (catches wrongness).

Usage: supervisor.py --demo all|crash|hang|leak|errors|crashloop [--keep]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICE = os.path.join(HERE, "service.py")
sys.path.insert(0, HERE)
import triage  # noqa: E402  (L1 investigator, deterministic stand-in)

CONFIG = dict(
    tick_s=0.3,
    heartbeat_timeout_s=3.0,
    golden_timeout_s=2.0,
    leak_limit_mb=40,             # threshold on the self-reported ballast gauge
    error_window=6,               # golden probes considered for error-rate math
    error_rate_threshold=0.5,
    backoff_schedule=(1.0, 2.0, 4.0, 8.0),
    max_restarts_in_window=3,     # OTP-style MaxR ...
    restart_window_s=30.0,        # ... within MaxT
    detect_budget_s=15.0,
    ready_timeout_s=10.0,
)

SCENARIOS = ("crash", "hang", "leak", "errors", "crashloop")


def ts() -> str:
    return time.strftime("%H:%M:%S")


class Supervisor:
    """One supervisor instance heals one fault scenario end to end."""

    def __init__(self, port: int, run_dir: str, label: str, log_path: str):
        self.port = port
        self.label = label
        self.log_path = log_path
        self.hb_path = os.path.join(run_dir, f"heartbeat-{port}.json")
        self.proc: subprocess.Popen | None = None
        self.golden_window: deque[bool] = deque(maxlen=CONFIG["error_window"])
        self.restart_times: list[float] = []
        self.t0 = time.time()

    # ---- helpers -------------------------------------------------------

    def say(self, msg: str) -> None:
        print(f"[{ts()} +{time.time() - self.t0:6.2f}s] [{self.label}] {msg}", flush=True)

    def http(self, path: str, timeout: float, method: str = "GET"):
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(url, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except Exception as e:  # refused / reset / timeout
            return None, f"{type(e).__name__}:{e}".encode()

    # ---- PULSE stages --------------------------------------------------

    def spawn(self) -> None:
        self.proc = subprocess.Popen([sys.executable, SERVICE, str(self.port), self.hb_path])

    def kill_child(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1.5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

    def heartbeat_age(self) -> float | None:
        try:
            with open(self.hb_path) as f:
                return time.time() - json.load(f)["ts"]
        except Exception:
            return None

    def perceive(self) -> dict:
        alive = self.proc is not None and self.proc.poll() is None
        exit_code = self.proc.returncode if self.proc else None
        hb_age = self.heartbeat_age()
        hcode, hbody = self.http("/health", CONFIG["golden_timeout_s"])
        health = None
        if hcode == 200:
            try:
                health = json.loads(hbody)
            except Exception:
                pass
        gcode, gbody = self.http("/", CONFIG["golden_timeout_s"])
        golden_ok = gcode == 200 and gbody.strip() == b"PULSE-OK"
        self.golden_window.append(golden_ok)
        return dict(alive=alive, exit_code=exit_code, hb_age=hb_age, health=health,
                    golden_ok=golden_ok, golden_code=gcode)

    def understand(self, p: dict) -> str:
        if not p["alive"]:
            return "CRASHED"
        if p["hb_age"] is None or p["hb_age"] > CONFIG["heartbeat_timeout_s"]:
            return "HUNG"
        if p["health"] and p["health"].get("ballast_mb", 0) > CONFIG["leak_limit_mb"]:
            return "LEAKING"
        if len(self.golden_window) == CONFIG["error_window"]:
            rate = 1 - sum(self.golden_window) / len(self.golden_window)
            if rate >= CONFIG["error_rate_threshold"]:
                return "ERRORING"
        return "HEALTHY"

    LOCALIZATION = {
        "CRASHED": "service process (runtime layer L3)",
        "HUNG": "event loop / heartbeat thread (runtime layer L3)",
        "LEAKING": "request-handler allocation path (application logic)",
        "ERRORING": "recent change or dependency (delivery layer L6 / service L4)",
    }

    def solve(self, fault_class: str) -> str:
        """Returns the action taken: RESTART #n, or ESCALATE (human required)."""
        now = time.time()
        self.restart_times = [t for t in self.restart_times
                              if now - t < CONFIG["restart_window_s"]]
        if len(self.restart_times) >= CONFIG["max_restarts_in_window"]:
            self.say(f"PULSE S: ESCALATE — restart intensity {len(self.restart_times)} in "
                     f"{CONFIG['restart_window_s']:.0f}s exceeds MaxR={CONFIG['max_restarts_in_window']} "
                     f"(OTP MaxR/MaxT pattern, D02[1]). Human required. Halting rescheduling.")
            return "ESCALATE"
        self.kill_child()
        backoff = CONFIG["backoff_schedule"][min(len(self.restart_times),
                                                 len(CONFIG["backoff_schedule"]) - 1)]
        self.restart_times.append(now)
        self.say(f"PULSE S: kill + RESTART #{len(self.restart_times)} "
                 f"(backoff {backoff:.1f}s, capped at {CONFIG['backoff_schedule'][-1]:.0f}s — "
                 f"kubelet-style crash-loop damping, D02[22])")
        time.sleep(backoff)
        self.spawn()
        return f"RESTART#{len(self.restart_times)}"

    def verify(self) -> tuple[bool, float]:
        deadline = time.time() + CONFIG["ready_timeout_s"]
        while time.time() < deadline:
            age = self.heartbeat_age()
            if age is not None and age < CONFIG["heartbeat_timeout_s"]:
                code, body = self.http("/", CONFIG["golden_timeout_s"])
                if code == 200 and body.strip() == b"PULSE-OK":
                    return True, age
            time.sleep(CONFIG["tick_s"])
        return False, -1.0

    # ---- scenario driver ----------------------------------------------

    def run_scenario(self, name: str) -> dict:
        self.say(f"spawn service (port {self.port}) and wait for readiness")
        self.spawn()
        ok, _ = self.verify()
        if not ok:
            return self._event(name, fault_class="NEVER_READY", action="NONE",
                               detected=False, healed=False, note="service never became ready")
        self.say("service HEALTHY (fresh heartbeat + golden PULSE-OK) — injecting fault")

        inject_t = time.time()
        if name == "crashloop":
            outcome = self._crashloop(inject_t)
            return outcome

        code, _ = self.http(f"/inject/{name}", CONFIG["golden_timeout_s"], method="POST")
        if code != 200:
            return self._event(name, fault_class="INJECT_FAILED", action="NONE",
                               detected=False, healed=False, note=f"inject http={code}")

        fault_class, p = self._await_detection(inject_t)
        if fault_class is None:
            self.kill_child()
            return self._event(name, fault_class="UNDETECTED", action="NONE", detected=False,
                               healed=False, note="detection budget exhausted (axiom A9 violation!)")

        self.say(f"PULSE U: classified {fault_class} | PULSE L: {self.LOCALIZATION[fault_class]}")
        action = self.solve(fault_class)
        if action == "ESCALATE":
            return self._event(name, fault_class=fault_class, action=action, detected=True,
                               healed=False, escalated=True, inject_t=inject_t,
                               note="escalation is the *correct* heal for a crash loop")
        healed, hb_age = self.verify()
        mttr_ms = int((time.time() - inject_t) * 1000)
        note = ""
        if fault_class == "LEAKING":
            note = ("mitigated, not cured — restart reclaims memory; the code fix still "
                    "needs an L2 human-reviewed PR ('restart is not repair', D02 gap-analysis)")
        self.say(f"PULSE E: verification gate → {'HEALED' if healed else 'FAILED TO HEAL'} "
                 f"(heartbeat age {hb_age:.2f}s, golden=PULSE-OK) mttr={mttr_ms}ms"
                 + (f" | {note}" if note else ""))
        self.kill_child()
        return self._event(name, fault_class=fault_class, action=action, detected=True,
                           healed=healed, inject_t=inject_t, mttr_ms=mttr_ms, note=note)

    def _crashloop(self, inject_t: float) -> dict:
        """Crash the service repeatedly; expect ESCALATE once MaxR is hit."""
        action = ""
        fault_class = "CRASHED"
        for i in range(CONFIG["max_restarts_in_window"] + 1):
            self.golden_window.clear()  # stale probe failures would misclassify the crash
            self.http("/inject/crash", CONFIG["golden_timeout_s"], method="POST")
            deadline = time.time() + 3.0  # wait for the actual exit (crash fires ~0.1s later)
            while self.proc.poll() is None and time.time() < deadline:
                time.sleep(0.1)
            fc, _ = self._await_detection(time.time())
            if fc is None:
                fc = "CRASHED"
            self.say(f"PULSE U: classified {fc} (crash {i + 1})")
            action = self.solve(fc)
            if action == "ESCALATE":
                return self._event("crashloop", fault_class=fault_class, action=action,
                                   detected=True, healed=False, escalated=True,
                                   inject_t=inject_t,
                                   note="restart storm bounded by design — the healer refuses "
                                        "to thrash (axiom A3: the healer must not harm)")
            ok, _ = self.verify()
            if not ok:
                return self._event("crashloop", fault_class=fc, action=action, detected=True,
                                   healed=False, inject_t=inject_t, note="respawn failed")
        return self._event("crashloop", fault_class=fault_class, action=action, detected=True,
                           healed=False, inject_t=inject_t, note="escalation never triggered?!")

    def _await_detection(self, since: float):
        deadline = since + CONFIG["detect_budget_s"]
        while time.time() < deadline:
            p = self.perceive()
            fc = self.understand(p)
            if fc != "HEALTHY":
                self.say(f"PULSE P: alive={p['alive']} exit={p['exit_code']} "
                         f"hb_age={p['hb_age'] if p['hb_age'] is None else round(p['hb_age'], 2)} "
                         f"golden={p['golden_ok']}")
                return fc, p
            time.sleep(CONFIG["tick_s"])
        return None, None

    def _event(self, scenario: str, fault_class: str, action: str, detected: bool,
               healed: bool, escalated: bool = False, inject_t: float | None = None,
               mttr_ms: int | None = None, note: str = "") -> dict:
        passed = detected and (healed or escalated)
        event = {
            "scenario": scenario,
            "fault_class": fault_class,
            "localized": self.LOCALIZATION.get(fault_class, "n/a"),
            "action": action,
            "detected": detected,
            "healed": healed,
            "escalated": escalated,
            "mttr_ms": mttr_ms,
            "outcome": "PASS" if passed else "FAIL",
            "note": note,
            "triage": triage.investigate(fault_class),
            "config": {k: v for k, v in CONFIG.items() if k != "backoff_schedule"},
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        self.say(f"outcome: {event['outcome']}"
                 + (f" ({note})" if note else ""))
        return event


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--demo", default="all", choices=SCENARIOS + ("all",))
    args = ap.parse_args()

    scenarios = SCENARIOS if args.demo == "all" else (args.demo,)
    run_dir = tempfile.mkdtemp(prefix="pulse-demo-")
    log_path = os.path.join(run_dir, "healing-log.jsonl")
    print(f"== PULSE application-track prototype ==\n"
          f"run dir: {run_dir}\n")

    events = []
    for i, name in enumerate(scenarios):
        print(f"--- scenario: {name} " + "-" * (40 - len(name)))
        sup = Supervisor(port=8810 + i, run_dir=run_dir, label=name, log_path=log_path)
        try:
            events.append(sup.run_scenario(name))
        finally:
            sup.kill_child()

    print("\n=== summary ===")
    fails = 0
    for e in events:
        mttr = f"{e['mttr_ms']}ms" if e.get("mttr_ms") else "-"
        print(f"  {e['scenario']:<10} {e['outcome']}  class={e['fault_class']:<9} "
              f"action={e['action']:<10} mttr={mttr}")
        fails += e["outcome"] == "FAIL"
    print(f"\nhealing log (Evolve artifact): {log_path}")
    print("ALL PASS" if fails == 0 else f"{fails} FAILURE(S)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
