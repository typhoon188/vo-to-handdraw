#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="$SKILL_DIR/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: bootstrap not run" >&2
  exit 1
fi
cd "$SKILL_DIR"
"$PY" tests/test_production.py
mkdir -p /tmp/vo-to-handdraw-verify
bash scripts/run.sh examples/vo/generic_trail.srt /tmp/vo-to-handdraw-verify/trail.mp4 --audit
[[ -s /tmp/vo-to-handdraw-verify/trail.mp4 ]]
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=nw=1 /tmp/vo-to-handdraw-verify/trail.mp4 >/dev/null
echo "VERIFY_OK"
