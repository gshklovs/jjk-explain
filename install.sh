#!/usr/bin/env bash
# Symlink the /explain skill into Claude Code's user skills dir.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/.claude/skills
if [ -e ~/.claude/skills/explain ] && [ ! -L ~/.claude/skills/explain ]; then
  echo "~/.claude/skills/explain exists and is not a symlink; move it aside first." >&2; exit 1
fi
ln -sfn "$HERE/skills/explain" ~/.claude/skills/explain
ln -sfn "$HERE/skills/explain-iroh" ~/.claude/skills/explain-iroh
command -v ffmpeg >/dev/null || echo "WARNING: ffmpeg not found. macOS: brew install ffmpeg"
python3 -c "import requests" 2>/dev/null || echo "WARNING: pip install -r $HERE/requirements.txt"
[ -f "$HERE/.env" ] || echo "Next: cp $HERE/.env.example $HERE/.env and add your keys."
ls "$HERE"/assets/*.m4a "$HERE"/assets/*.mp3 >/dev/null 2>&1 || echo "Optional: drop a music bed (m4a/mp3) into $HERE/assets/ (any track; the Delirious 1 hour loop is the canonical choice)."
echo "Installed: ~/.claude/skills/explain and explain-iroh -> $HERE/skills/. In Claude Code, run: /explain <concept> or /explain-iroh <concept>"
