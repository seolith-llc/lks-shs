#!/usr/bin/env bash
# One-command PULSE demo (rule R5): wounds the service, watches it heal.
# Scenarios: crash · hang · leak · errors · crashloop (restart-storm escalation).
set -euo pipefail
cd "$(dirname "$0")"
exec python3 supervisor.py --demo all
