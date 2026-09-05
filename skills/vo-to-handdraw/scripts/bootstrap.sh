#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

command -v python3 >/dev/null || { echo "ERROR: python3 is required" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg is required (macOS: brew install ffmpeg)" >&2; exit 1; }
command -v ffprobe >/dev/null || { echo "ERROR: ffprobe is required (installed with ffmpeg)" >&2; exit 1; }

if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "BOOTSTRAP_OK"
