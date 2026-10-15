#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
IMAGE="self-healing-demo:local"
CONTAINER="self-healing-demo-local"
docker build -t "$IMAGE" .
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" -p 8080:80 "$IMAGE"
printf 'App is starting at http://localhost:8080 (Ctrl+C will not stop the container).\n'
printf 'Stop it with: docker rm -f %s\n' "$CONTAINER"
