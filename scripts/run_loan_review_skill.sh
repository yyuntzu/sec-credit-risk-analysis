#!/usr/bin/env bash
set -euo pipefail
skill_root="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
review_python="${LOAN_REVIEW_PYTHON:-}"
if [[ -z "$review_python" ]]; then
  for candidate in "${VIRTUAL_ENV:-/nonexistent}/bin/python" "$skill_root/venv/bin/python" "$skill_root/.venv/bin/python"; do
    if [[ -x "$candidate" ]]; then review_python="$candidate"; break; fi
  done
fi
if [[ -z "$review_python" ]]; then
  if common_dir="$(git -C "$skill_root" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; then
    candidate="$(dirname "$common_dir")/venv/bin/python"
    if [[ -x "$candidate" ]]; then review_python="$candidate"; fi
  fi
fi
if [[ -z "$review_python" || ! -x "$review_python" ]]; then
  echo 'Set LOAN_REVIEW_PYTHON to the Python environment matching the selected runtime lock.' >&2
  exit 1
fi
cd "$skill_root"
exec "$review_python" -m scripts.loan_review_skill "$@"
