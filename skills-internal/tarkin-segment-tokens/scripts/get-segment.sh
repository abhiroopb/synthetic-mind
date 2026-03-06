#!/usr/bin/env bash
# Fetch a Tarkin segment by ID or name.
# Usage: get-segment.sh <environment> <--id ID | --name NAME>
# environment: "staging" or "production"
set -euo pipefail

ENV="${1:?Usage: get-segment.sh <environment> <--id ID | --name NAME>}"
shift

LOOKUP_KEY=""
LOOKUP_VALUE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)   LOOKUP_KEY="id";   LOOKUP_VALUE="${2:?--id requires a value}"; shift 2 ;;
    --name) LOOKUP_KEY="name"; LOOKUP_VALUE="${2:?--name requires a value}"; shift 2 ;;
    *)      echo "Error: unknown option '$1'" >&2; exit 1 ;;
  esac
done

if [ -z "$LOOKUP_KEY" ]; then
  echo "Error: must specify --id or --name" >&2
  exit 1
fi

if [ "$ENV" = "staging" ]; then
  BASE_URL="https://tarkin.stage.sqprod.co"
elif [ "$ENV" = "production" ]; then
  BASE_URL="https://tarkin.sqprod.co"
else
  echo "Error: environment must be 'staging' or 'production'" >&2
  exit 1
fi

ENCODED_VALUE=$(LOOKUP_VALUE="$LOOKUP_VALUE" python3 -c "import os, urllib.parse; print(urllib.parse.quote(os.environ['LOOKUP_VALUE']))")
sq curl -s "${BASE_URL}/api/v1/segments?${LOOKUP_KEY}=${ENCODED_VALUE}"
