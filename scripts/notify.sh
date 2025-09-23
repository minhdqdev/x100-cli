#!/usr/bin/env bash

set -euo pipefail

# Defaults
status="finished"

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --status)
      # Next arg should be the value
      shift || true
      if [[ $# -gt 0 ]]; then
        status="$1"
        shift || true
      fi
      ;;
    --status=*)
      status="${arg#*=}"
      ;;
    -h|--help)
      echo "Usage: $0 [--status <finished|succeeded|failed>]" >&2
      exit 0
      ;;
    *)
      # ignore unknown args to keep backward compatible
      ;;
  esac
done

# Normalize status to lowercase
status=$(printf '%s' "$status" | tr '[:upper:]' '[:lower:]')

# Build message based on status
case "$status" in
  succeeded)
    message="Codex has succeeded"
    ;;
  failed)
    message="Codex has failed"
    ;;
  finished)
    message="Codex has finished"
    ;;
  *)
    message="Codex status: $status"
    ;;
esac

printf '{"title":"AI Agent","message":"%s","status":"%s"}\n' "$message" "$status" | nc 127.0.0.1 7777
