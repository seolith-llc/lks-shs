#!/usr/bin/env python3
"""PULSE demo service — a deliberately woundable web service (stdlib only).

Implements the *supervised* side of the PULSE loop (Decision 003: external
supervisor model — this process must be killable and restartable):

  - writes a heartbeat file every 0.5 s (dead-man's-switch, the Perceive feed
    — same pattern as sd_notify WATCHDOG (D02[7][8]) and Healthchecks.io (D04[35]))
  - GET /health  -> self-reported gauge snapshot (memory ballast, active faults)
  - GET /        -> "PULSE-OK" (the golden request used by the verification oracle)
  - POST /inject/{crash|hang|leak|errors} -> fail on demand (demo wounds)
  - POST /clear  -> clear soft faults (leak/errors, resume heartbeat)

Fault semantics:
  crash  -> exit(137) immediately (runtime death)
  hang   -> stop heartbeat AND stall request handlers (liveness death)
  leak   -> each request appends CHUNK_MB to an in-process ballast (slow burn)
  errors -> 50% of requests return HTTP 500 (catastrophic error-rate regression)

Usage: service.py <port> <heartbeat_path>
"""
import json
import os
import random
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CHUNK_MB = int(os.environ.get("PULSE_CHUNK_MB", "8"))
HARD_BALLAST_CAP_MB = 512  # safety valve; the supervisor intervenates far below this


class State:
    def __init__(self, heartbeat_path: str):
        self.heartbeat_path = heartbeat_path
        self.started = time.time()
        self.requests = 0
        self.errors_served = 0
        self.faults: set[str] = set()
        self.ballast: list[bytes] = []
        self.beating = True
        self.lock = threading.Lock()

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "pid": os.getpid(),
                "uptime_s": round(time.time() - self.started, 2),
                "requests": self.requests,
                "errors_served": self.errors_served,
                "ballast_mb": round(sum(map(len, self.ballast)) / (1024 * 1024), 1),
                "faults": sorted(self.faults),
                "heartbeat": self.beating,
            }


def heartbeat_loop(state: State) -> None:
    """Dead-man's-switch writer: supervisor alarms when this file goes stale."""
    while True:
        if state.beating:
            tmp = state.heartbeat_path + ".tmp"
            with open(tmp, "w") as f:
                json.dump({"ts": time.time(), "pid": os.getpid()}, f)
            os.replace(tmp, state.heartbeat_path)
        time.sleep(0.5)


def make_handler(state: State):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):  # keep demo output clean
            pass

        def _send(self, code: int, payload, ctype: str = "application/json") -> None:
            body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _flaky(self) -> bool:
            with state.lock:
                return "errors" in state.faults and random.random() < 0.5

        def do_GET(self):
            with state.lock:
                state.requests += 1
            if self.path == "/health":
                if self._flaky():
                    with state.lock:
                        state.errors_served += 1
                    return self._send(500, {"status": "UNHEALTHY", "reason": "injected flakiness"})
                snap = state.snapshot()
                snap["status"] = "HEALTHY" if not snap["faults"] else "DEGRADED"
                return self._send(200, snap)
            if self.path == "/":
                with state.lock:
                    hang = "hang" in state.faults
                if hang:
                    time.sleep(60)  # stall: no response, heartbeat already stopped
                if self._flaky():
                    with state.lock:
                        state.errors_served += 1
                    return self._send(500, b"INTERNAL", "text/plain")
                with state.lock:
                    if ("leak" in state.faults
                            and sum(map(len, state.ballast)) < HARD_BALLAST_CAP_MB * 1024 * 1024):
                        state.ballast.append(b"\0" * (CHUNK_MB * 1024 * 1024))
                return self._send(200, b"PULSE-OK", "text/plain")
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            if not (self.path.startswith("/inject/") or self.path == "/clear"):
                return self._send(404, {"error": "not found"})
            fault = self.path.rsplit("/", 1)[-1]
            with state.lock:
                if fault == "clear":
                    state.faults.discard("leak")
                    state.faults.discard("errors")
                    state.beating = True
                elif fault in {"crash", "hang", "leak", "errors"}:
                    state.faults.add(fault)
                    if fault == "hang":
                        state.beating = False
                else:
                    return self._send(400, {"error": f"unknown fault {fault}"})
            if fault == "crash":
                self._send(200, {"ok": True, "fault": "crash", "bye": "going down"})
                self.wfile.flush()
                threading.Timer(0.1, lambda: os._exit(137)).start()
                return
            return self._send(200, {"ok": True, "fault": fault})

    return Handler


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8800
    heartbeat_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/pulse-heartbeat.json"
    state = State(heartbeat_path)
    threading.Thread(target=heartbeat_loop, args=(state,), daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(state))
    print(f"[service] pid={os.getpid()} listening on 127.0.0.1:{port} heartbeat={heartbeat_path}",
          flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
