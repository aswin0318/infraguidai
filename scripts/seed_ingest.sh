#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for backend..."
until curl -s http://localhost:8000/api/health > /dev/null; do
  sleep 2
done

echo "Triggering knowledge base ingestion..."
curl -X POST http://localhost:8000/api/admin/ingest
echo
echo "Ingestion triggered."
