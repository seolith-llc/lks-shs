#!/usr/bin/env python3
"""Deterministic L1 investigator — a stand-in for an LLM root-cause agent.

Per Decision 004: the demo must run offline, reproducibly, with the *shape*
of an L1 investigation (evidence in -> ranked hypotheses -> human gate), not
a live LLM call. The pattern mirrors RCACopilot's evidence-driven
classification (D03[50]) and the challenger/confidence pattern of commercial
AI SREs (D04[4][5]). A real LLM can be plugged in later via PULSE_TRIAGE_CMD
(see prototypes/pulse-app/README.md) without touching the supervisor.
"""
import json
import subprocess
import sys

RULES = {
    "CRASHED": [
        ("process exited (killed / native fault / explicit exit)", 0.90),
        ("unhandled exception on the hot path", 0.60),
    ],
    "HUNG": [
        ("event loop stalled; heartbeat writer stopped", 0.85),
        ("blocking call or deadlock inside a request handler", 0.70),
    ],
    "LEAKING": [
        ("unbounded retention on the request path (grows with traffic)", 0.90),
        ("missing cache/pool bounds in a dependency", 0.50),
    ],
    "ERRORING": [
        ("recent deployment regression (error-rate step change)", 0.80),
        ("dependency outage with amplifying retries", 0.60),
    ],
}


def investigate(fault_class: str, summary: dict | None = None) -> dict:
    """Rank hypotheses. If PULSE_TRIAGE_CMD is set, defer to an external
    (e.g. LLM-backed) command that reads the summary JSON on stdin."""
    env_cmd = __import__("os").environ.get("PULSE_TRIAGE_CMD")
    if env_cmd:
        proc = subprocess.run(
            env_cmd, shell=True, input=json.dumps({"fault_class": fault_class,
                                                   "summary": summary or {}}),
            capture_output=True, text=True, timeout=30)
        return {"investigator": f"external:{env_cmd}", "result": proc.stdout.strip()}

    hyps = [{"cause": c, "confidence": p} for c, p in RULES.get(fault_class, [("unknown", 0.10)])]
    return {
        "investigator": "deterministic-rules (L1 stand-in; pluggable via PULSE_TRIAGE_CMD)",
        "hypotheses": sorted(hyps, key=lambda h: -h["confidence"]),
        "gate": "code-level fixes still require an L2 human-reviewed PR "
                "(Decision 004; D04[4][17]) — diagnosis is autonomous, repair is gated",
    }


if __name__ == "__main__":
    fc = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"
    print(json.dumps(investigate(fc), indent=2))
