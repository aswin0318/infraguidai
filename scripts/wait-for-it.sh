#!/usr/bin/env sh
set -eu

HOST_PORT="${1:-}"
TIMEOUT="${2:-60}"

if [ -z "$HOST_PORT" ] || ! echo "$HOST_PORT" | grep -q ":"; then
  echo "Usage: wait-for-it.sh host:port [timeout_seconds]" >&2
  exit 1
fi

HOST="$(echo "$HOST_PORT" | cut -d: -f1)"
PORT="$(echo "$HOST_PORT" | cut -d: -f2)"
START="$(date +%s)"

echo "Waiting for $HOST:$PORT..."
while :; do
  if nc -z "$HOST" "$PORT" >/dev/null 2>&1; then
    echo "$HOST:$PORT is available"
    exit 0
  fi
  NOW="$(date +%s)"
  if [ "$((NOW - START))" -ge "$TIMEOUT" ]; then
    echo "Timed out waiting for $HOST:$PORT" >&2
    exit 1
  fi
  sleep 2
done
