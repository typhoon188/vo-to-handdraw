#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="$SKILL_DIR/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: skill venv not found. Run: bash $SKILL_DIR/scripts/bootstrap.sh" >&2
  exit 1
fi
exec "$PY" "$SKILL_DIR/handdraw.py" "$@"
