#!/usr/bin/env bash
# notify-listener.sh
# Simple local listener that turns incoming lines into macOS notifications.

set -euo pipefail

PORT="${1:-7777}"                  # Override: ./notify-listener.sh 8888
BIND_IP="${BIND_IP:-127.0.0.1}"    # Override via env
TITLE="${TITLE:-notify}"            # Override via env
LOG_FILE="${LOG_FILE:-$HOME/.notify.log}"
NOTIFIER_CMD="${NOTIFIER_CMD:-/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier}"  # Fallbacks to osascript if missing
SOUND="${SOUND:-default}"                 # e.g. SOUND="default" (terminal-notifier)

# --- deps & sanity -----------------------------------------------------------
if ! command -v nc >/dev/null 2>&1; then
  echo "nc (netcat) is required on macOS (brew install netcat or use built-in)." >&2
  exit 1
fi

use_terminal_notifier=false
if command -v "$NOTIFIER_CMD" >/dev/null 2>&1; then
  use_terminal_notifier=true
elif ! command -v osascript >/dev/null 2>&1; then
  echo "Need either terminal-notifier or osascript available." >&2
  exit 1
fi

touch "$LOG_FILE" || { echo "Cannot write to $LOG_FILE"; exit 1; }

echo "Listening on ${BIND_IP}:${PORT} — title='${TITLE}'  (Ctrl+C to stop)"
echo "Logging to: $LOG_FILE"

# --- cleanup hints -----------------------------------------------------------
trap 'echo; echo "Shutting down listener..."; exit 0' INT TERM

# --- main loop ---------------------------------------------------------------
# We use -l (listen) -k (keep open). Some macOS nc builds support -N; we don't depend on it.
while true; do
  # For each TCP connection, read lines and notify
  nc -lk "$BIND_IP" "$PORT" | while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -n "${line// }" ]] || continue  # skip empty/whitespace-only
    # Notify
    if $use_terminal_notifier; then
      if [[ -n "$SOUND" ]]; then
        "$NOTIFIER_CMD" -title "$TITLE" -message "$line" -sound "$SOUND" || true
      else
        "$NOTIFIER_CMD" -title "$TITLE" -message "$line" || true
      fi
    else
      # osascript fallback
      /usr/bin/osascript -e "display notification $(printf %q "$line") with title $(printf %q "$TITLE")" || true
    fi
    # Log with timestamp
    printf '%s  %s\n' "$(date '+%F %T')" "$line" >> "$LOG_FILE" || true
  done
done

