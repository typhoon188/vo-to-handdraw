#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/skills/vo-to-handdraw"
DST="$HOME/.hermes/skills/vo-to-handdraw"
mkdir -p "$HOME/.hermes/skills"
rm -rf "$DST"
cp -R "$SRC" "$DST"
echo "INSTALLED: $DST"
echo "Next: bash $DST/scripts/bootstrap.sh"
