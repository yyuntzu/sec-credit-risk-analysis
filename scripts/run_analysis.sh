#!/bin/bash
# Formal default. Quoted arguments are forwarded unchanged.
# bash scripts/run_analysis.sh AMZN --request request.json --execution local
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" "$SCRIPT_DIR/agent_runner.py" "$@"
