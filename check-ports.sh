#!/usr/bin/env bash
# Check if Redpanda compose ports are free before starting.
# Usage: ./check-ports.sh

set -e

PORTS=(18081 18082 19092 19644 8080)
NAMES=("Schema Registry" "PandaProxy" "Kafka (external)" "Admin API" "Console")

echo "Checking Redpanda ports..."
echo ""

conflict=0
for i in "${!PORTS[@]}"; do
  p="${PORTS[$i]}"
  name="${NAMES[$i]}"
  if ss -tlnp 2>/dev/null | grep -q ":$p "; then
    echo "  Port $p ($name): in use"
    conflict=1
  else
    echo "  Port $p ($name): free"
  fi
done

echo ""
if [ "$conflict" -eq 1 ]; then
  echo "Some ports are in use. Free them or change compose port mapping before starting."
  exit 1
else
  echo "All ports are free. Safe to start Redpanda."
  exit 0
fi
