#!/usr/bin/env bash
# Install the Ontology Engine agent skill discovery stub into your local AI client.
#
# The actual skill content lives inside the ontology CLI itself
# (pip install ontology-cli). This script installs the discovery stub (ontology)
# that points an AI client at the CLI; from then on the agent fetches
# everything else via ontology skills get / ontology ask.
#
# Usage:
#   ./install.sh                # install the discovery stub from this clone
#   ./install.sh --force        # overwrite an existing install
#
# v0: local clone only. Do not download from Canner/WrenAI.

set -euo pipefail

DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
SKILL="ontology"

FORCE=false
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=true ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "/dev/stdin" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

install_skill() {
  local src="$1" dest_dir="$2"
  if [ "$FORCE" = false ] && [ -d "$dest_dir" ]; then
    echo "  Skipping $SKILL (already exists). Use --force to overwrite."
    return
  fi
  rm -rf "$dest_dir"
  cp -r "$src" "$dest_dir"
  echo "  Installed $SKILL"
}

mkdir -p "$DEST"

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/$SKILL" ]; then
  echo "Installing from local repo: $SCRIPT_DIR"
  echo "Destination: $DEST"
  echo ""
  install_skill "$SCRIPT_DIR/$SKILL" "$DEST/$SKILL"
else
  echo "Public skill download is not published yet (v0)."
  echo "Run this script from a local Ontology Engine clone so skills/ontology exists."
  exit 1
fi

echo ""
echo "Done. Invoke the skill in your AI client:"
echo "  /$SKILL"
