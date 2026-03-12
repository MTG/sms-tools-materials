#!/bin/zsh
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
if [[ -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
  exec "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/launch_gui.py"
else
  exec python3 "$SCRIPT_DIR/launch_gui.py"
fi
