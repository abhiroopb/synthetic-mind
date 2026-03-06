#!/usr/bin/env bash
# Add or remove tokens from a Tarkin segment.
# Usage: update-segment-tokens.sh <environment> <segment_id> <action> <tokens_comma_separated> [--dry-run]
# environment: "staging" or "production"
# segment_id: numeric segment ID
# action: "add" or "remove"
# tokens: comma-separated list of tokens (e.g. "TOKEN1,TOKEN2,TOKEN3")
# --dry-run: show the payload that would be sent without making any changes
#
# This script first fetches the segment to preserve its name/description/type,
# then issues a PATCH with a cookie jar to handle CSRF authentication.
set -euo pipefail

ENV="${1:?Usage: update-segment-tokens.sh <environment> <segment_id> <action> <tokens> [--dry-run]}"
SEGMENT_ID="${2:?Usage: update-segment-tokens.sh <environment> <segment_id> <action> <tokens> [--dry-run]}"
ACTION="${3:?Usage: update-segment-tokens.sh <environment> <segment_id> <action> <tokens> [--dry-run]}"
TOKENS_CSV="${4:?Usage: update-segment-tokens.sh <environment> <segment_id> <action> <tokens> [--dry-run]}"

DRY_RUN=false
if [ "${5:-}" = "--dry-run" ]; then
  DRY_RUN=true
fi

if [ "$ENV" = "staging" ]; then
  BASE_URL="https://internal-api.example.com"
elif [ "$ENV" = "production" ]; then
  BASE_URL="https://internal-api.example.com"
else
  echo "Error: environment must be 'staging' or 'production'" >&2
  exit 1
fi

if [ "$ACTION" != "add" ] && [ "$ACTION" != "remove" ]; then
  echo "Error: action must be 'add' or 'remove'" >&2
  exit 1
fi

# Convert comma-separated tokens to JSON array
TOKENS_JSON=$(echo "$TOKENS_CSV" | tr ',' '\n' | jq -R . | jq -s .)

# Step 1: Fetch the segment to get current name, description, and type
SEGMENT_JSON=$(internal-cli curl -s "${BASE_URL}/api/v1/segments?id=${SEGMENT_ID}")
SEGMENT_COUNT=$(echo "$SEGMENT_JSON" | jq '.data | length')

if [ "$SEGMENT_COUNT" = "0" ] || [ "$SEGMENT_COUNT" = "null" ]; then
  echo "Error: Segment ${SEGMENT_ID} not found" >&2
  exit 1
fi

NAME=$(echo "$SEGMENT_JSON" | jq -r '.data[0].attributes.name')
DESCRIPTION=$(echo "$SEGMENT_JSON" | jq -r '.data[0].attributes.description // empty')
TYPE=$(echo "$SEGMENT_JSON" | jq -r '.data[0].attributes.type')

echo "Segment: id=${SEGMENT_ID}, name='${NAME}', type=${TYPE}"

# Build token_to_add / token_to_remove based on action
if [ "$ACTION" = "add" ]; then
  TOKEN_TO_ADD="$TOKENS_JSON"
  TOKEN_TO_REMOVE="[]"
  echo "Adding tokens: ${TOKENS_CSV}"
else
  TOKEN_TO_ADD="[]"
  TOKEN_TO_REMOVE="$TOKENS_JSON"
  echo "Removing tokens: ${TOKENS_CSV}"
fi

# Build the JSON payload
PAYLOAD=$(jq -n \
  --arg id "$SEGMENT_ID" \
  --arg name "$NAME" \
  --arg desc "$DESCRIPTION" \
  --arg type "$TYPE" \
  --argjson token_to_add "$TOKEN_TO_ADD" \
  --argjson token_to_remove "$TOKEN_TO_REMOVE" \
  '{
    id: $id,
    name: $name,
    description: (if $desc == "" then null else $desc end),
    type: $type,
    token_to_add: $token_to_add,
    token_to_remove: $token_to_remove
  }')

if [ "$DRY_RUN" = true ]; then
  echo "[dry-run] Payload that would be sent:"
  echo "$PAYLOAD" | jq .
  exit 0
fi

# Step 2: Get a session cookie + CSRF token
COOKIE_JAR=$(mktemp)
trap "rm -f '$COOKIE_JAR'" EXIT

CSRF_TOKEN=$(internal-cli curl -s -c "$COOKIE_JAR" "${BASE_URL}/ui/segments/${SEGMENT_ID}" \
  | grep 'csrf-token' \
  | sed 's/.*content="\([^"]*\)".*/\1/')

if [ -z "$CSRF_TOKEN" ]; then
  echo "Error: Failed to obtain CSRF token" >&2
  exit 1
fi

# Step 3: PATCH the segment
RESPONSE=$(internal-cli curl -s -X PATCH "${BASE_URL}/api/v1/segments" \
  -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -H "X-CSRF-Token: ${CSRF_TOKEN}" \
  -d "$PAYLOAD")

echo "$RESPONSE" | jq .
