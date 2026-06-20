#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
PROJECT_PYTHON="$(tr -d '[:space:]' < "$ROOT_DIR/.python-version")"
REAL_QUARTO="${QUARTO_BIN:-}"
LOG_FILE="$ROOT_DIR/.quarto-preview.log"
SERVER_LOG_FILE="$ROOT_DIR/.quarto-preview-server.log"
DEFAULT_PREVIEW_PORT="${QUARTO_PREVIEW_PORT:-4673}"

log_invocation() {
  {
    printf '[%s]\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'cwd: %s\n' "$(pwd)"
    printf 'args:'
    printf ' <%s>' "$@"
    printf '\n\n'
  } >> "$LOG_FILE"
}

project_quarto_pids() {
  local pid
  ps -axo pid=,command= | awk '/quarto\.js preview/ { print $1 }' |
    while read -r pid; do
      if lsof -a -p "$pid" -d cwd 2>/dev/null |
          awk -v root="$ROOT_DIR" 'NR > 1 && index($0, root) { found = 1 } END { exit !found }'; then
        echo "$pid"
      fi
    done
}

project_jupyter_pids() {
  ps -axo pid=,command= | awk -v venv="$VENV_PYTHON" '
    index($0, venv) && (/jupyter\.py serve/ || /ipykernel_launcher/) { print $1 }
  '
}

start_detached_preview() {
  local launcher_python
  launcher_python="$VENV_PYTHON"
  if [ ! -x "$launcher_python" ]; then
    launcher_python="$(command -v python3)"
  fi

  "$launcher_python" -c '
import os
import subprocess
import sys

log_file = sys.argv[1]
argv = sys.argv[2:]
log = open(log_file, "ab", buffering=0)
process = subprocess.Popen(
    argv,
    cwd=os.getcwd(),
    stdout=log,
    stderr=subprocess.STDOUT,
    stdin=subprocess.DEVNULL,
    start_new_session=True,
)
print(process.pid)
' "$SERVER_LOG_FILE" "$REAL_QUARTO" "$@"
}

preview_status() {
  local pids

  echo "== Quarto preview processes for this project =="
  pids="$(project_quarto_pids)"
  if [ -z "$pids" ]; then
    echo "No Quarto preview process found."
  else
    echo "$pids" | xargs ps -o pid=,command= -p
  fi

  echo
  echo "== Project Jupyter kernels/servers =="
  pids="$(project_jupyter_pids)"
  if [ -z "$pids" ]; then
    echo "No project Jupyter kernels or servers found."
  else
    echo "$pids" | xargs ps -o pid=,command= -p
  fi

  echo
  echo "== Listening ports used by Quarto/Jupyter =="
  lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk '
    /deno|python3/ { print }
  ' || true
}

preview_stop() {
  local pids
  pids="$(project_quarto_pids; project_jupyter_pids)"

  if [ -z "$pids" ]; then
    echo "No Quarto preview or project Jupyter processes found."
    return 0
  fi

  echo "Stopping project preview processes:"
  echo "$pids" | sed 's/^/  PID /'
  echo "$pids" | xargs kill 2>/dev/null || true
}

case "${1:-}" in
  preview-watch)
    if [ -z "${2:-}" ]; then
      echo "Usage: $0 preview-watch path/to/file.qmd [extra preview args]" >&2
      exit 2
    fi
    watch_file="$2"
    shift 2
    set -- preview "$watch_file" --no-browser "$@"
    ;;
  preview-status)
    preview_status
    exit 0
    ;;
  preview-stop)
    preview_stop
    exit 0
    ;;
esac

log_invocation "$@"

# Quarto can leave stale kernel transport files when a previous preview
# is interrupted early; clear that cache for fresh preview sessions.
if [ "${1:-}" = "preview" ]; then
  filtered_args=()
  removed_no_watch=0
  has_port=0
  for arg in "$@"; do
    if [ "$arg" = "--no-watch-inputs" ] || [[ "$arg" == --no-watch-inputs=* ]]; then
      removed_no_watch=1
      continue
    fi
    if [ "$arg" = "--port" ] || [[ "$arg" == --port=* ]]; then
      has_port=1
    fi
    filtered_args+=("$arg")
  done
  set -- "${filtered_args[@]}"
  if [ "$has_port" -eq 0 ]; then
    set -- "$@" --port "$DEFAULT_PREVIEW_PORT"
  fi

  echo "Preparing Quarto preview for this project..."
  if [ "$removed_no_watch" -eq 1 ]; then
    echo "Removed --no-watch-inputs so saved changes re-render automatically."
  fi
  if [ "$has_port" -eq 0 ]; then
    echo "Preview URL: http://127.0.0.1:$DEFAULT_PREVIEW_PORT/"
  fi
  echo "Preview log: $SERVER_LOG_FILE"
  echo "Use './scripts/quarto-wrapper.sh preview-stop' to stop this preview."
  preview_stop
  rm -rf "$HOME/Library/Caches/quarto/jt"
fi

if [ ! -x "$VENV_PYTHON" ]; then
  uv sync --python "$PROJECT_PYTHON"
fi

if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then
  # Ensure Quarto's Python-backed execution uses the project environment.
  source "$ROOT_DIR/.venv/bin/activate"
fi

if [ -x "$VENV_PYTHON" ]; then
  export QUARTO_PYTHON="$VENV_PYTHON"
  export JUPYTER_PATH="$ROOT_DIR/.venv/share/jupyter${JUPYTER_PATH:+:$JUPYTER_PATH}"
fi

if [ -z "$REAL_QUARTO" ]; then
  if [ -x "/Applications/quarto/bin/quarto" ]; then
    REAL_QUARTO="/Applications/quarto/bin/quarto"
  else
    REAL_QUARTO="$(command -v quarto || true)"
  fi
fi

if [ -z "$REAL_QUARTO" ] || [ ! -x "$REAL_QUARTO" ]; then
  echo "Error: quarto not found. Install Quarto or set QUARTO_BIN=/path/to/quarto." >&2
  exit 1
fi

if [ "${1:-}" = "preview" ]; then
  : > "$SERVER_LOG_FILE"
  preview_pid="$(start_detached_preview "$@")"
  echo "Started Quarto preview process: PID $preview_pid"

  for _ in $(seq 1 60); do
    if ! kill -0 "$preview_pid" 2>/dev/null; then
      echo "Quarto preview exited early. Last log lines:"
      tail -n 40 "$SERVER_LOG_FILE"
      exit 1
    fi
    if grep -q 'Listening on http://127\.0\.0\.1:' "$SERVER_LOG_FILE"; then
      grep 'Listening on http://127\.0\.0\.1:' "$SERVER_LOG_FILE" | tail -n 1
      exit 0
    fi
    sleep 1
  done

  echo "Preview is still rendering. Open the URL above in a moment, or inspect:"
  echo "  tail -f $SERVER_LOG_FILE"
  exit 0
fi

exec "$REAL_QUARTO" "$@"
