#!/usr/bin/env bash
set -euo pipefail

# Flag Simulator — Evaluate LaunchDarkly flags via the Experiment Relay API
# CLI replacement for go/flag-simulator (console.sqprod.co/flag-simulator)

# --- Defaults ---
PROJECT="PIE"
ENV="production"
FLAG_TYPE="BOOLEAN"
TOKEN_TYPE="MERCHANT"
PLATFORM=""
APP_VERTICAL="SPOS"
APP_VERSION="6.95"
MOBILE_OS="iOS"
DEVICE="COTS"
FLAG_KEY=""
TOKEN=""
DEFAULT_CONTEXT_TYPE="MERCHANT"

# Repeatable args
declare -a ATTRIBUTES=()
declare -a ATTRIBUTES_INT=()
declare -a ATTRIBUTES_BOOL=()
declare -a ATTRIBUTES_DOUBLE=()
declare -a CONTEXTS=()

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --flag-key) FLAG_KEY="$2"; shift 2 ;;
    --token) TOKEN="$2"; shift 2 ;;
    --token-type) TOKEN_TYPE="$2"; shift 2 ;;
    --project) PROJECT="$2"; shift 2 ;;
    --env) ENV="$2"; shift 2 ;;
    --flag-type) FLAG_TYPE="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
    --app-vertical) APP_VERTICAL="$2"; shift 2 ;;
    --app-version) APP_VERSION="$2"; shift 2 ;;
    --mobile-os) MOBILE_OS="$2"; shift 2 ;;
    --device) DEVICE="$2"; shift 2 ;;
    --attribute) ATTRIBUTES+=("$2"); shift 2 ;;
    --attribute-int) ATTRIBUTES_INT+=("$2"); shift 2 ;;
    --attribute-bool) ATTRIBUTES_BOOL+=("$2"); shift 2 ;;
    --attribute-double) ATTRIBUTES_DOUBLE+=("$2"); shift 2 ;;
    --context) CONTEXTS+=("$2"); shift 2 ;;
    --default-context-type) DEFAULT_CONTEXT_TYPE="$2"; shift 2 ;;
    --help)
      echo "Usage: evaluate.sh --flag-key <key> --token <token> [options]"
      echo ""
      echo "Options:"
      echo "  --flag-key KEY            Flag key to evaluate (required)"
      echo "  --token TOKEN             Context token value (required for single-context)"
      echo "  --token-type TYPE         MERCHANT|UNIT|PERSON|SQUARE_MOBILE_DEVICE (default: MERCHANT)"
      echo "  --project PROJECT         PIE|CAPITAL|SQUARE_CONSOLE|TIDAL|SHOP (default: PIE)"
      echo "  --env ENV                 production|staging|sandbox (default: production)"
      echo "  --flag-type TYPE          BOOLEAN|STRING|INTEGER|DOUBLE|JSON (default: BOOLEAN)"
      echo "  --platform PLATFORM       Server|Mobile|\"Dashboard Web\" (default: Server)"
      echo "  --app-vertical VERTICAL   App vertical for Mobile (default: SPOS)"
      echo "  --app-version VERSION     App version for Mobile (default: 6.95)"
      echo "  --mobile-os OS            iOS|Android (default: iOS)"
      echo "  --device DEVICE           X2A|X2B|X2C|T2A|T2B|T3A|COTS (default: COTS)"
      echo "  --attribute KEY=VALUE     String attribute (repeatable)"
      echo "  --attribute-int KEY=VAL   Integer attribute (repeatable)"
      echo "  --attribute-bool KEY=VAL  Boolean attribute (repeatable)"
      echo "  --attribute-double KEY=V  Double attribute (repeatable)"
      echo "  --context TYPE:TOKEN      Multi-context entry (repeatable)"
      echo "  --default-context-type T  Default context type for multi-context (default: MERCHANT)"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$FLAG_KEY" ]]; then
  echo "Error: --flag-key is required" >&2
  exit 1
fi

if [[ -z "$TOKEN" && ${#CONTEXTS[@]} -eq 0 ]]; then
  echo "Error: --token or --context is required" >&2
  exit 1
fi

if [[ -z "$PLATFORM" ]]; then
  echo "Error: --platform is required (Server, Mobile, or \"Dashboard Web\")" >&2
  exit 1
fi

# --- Environment domain mapping ---
get_domain() {
  case "$1" in
    production) echo "experiment-relay.sqprod.co" ;;
    staging)    echo "experiment-relay.stage.sqprod.co" ;;
    sandbox)    echo "sandbox--experiment-relay.sqprod.co" ;;
    *) echo "Error: Unknown environment: $1" >&2; exit 1 ;;
  esac
}

# --- Bundle ID mapping ---
get_bundle_id() {
  case "$1" in
    SPOS)            echo "com.squareup.square" ;;
    Invoices)        echo "com.squareup.invoices" ;;
    Appointments)    echo "com.squareup.appointments" ;;
    Restaurants)     echo "com.squareup.restaurant" ;;
    Retail)          echo "com.squareup.retailer" ;;
    Dashboard)       echo "com.squareup.dashboard" ;;
    "Terminal API")  echo "com.squareup.terminalapi" ;;
    Kiosk)           echo "com.squareup.fnbkiosk" ;;
    KDS)             echo "com.squareup.kds" ;;
    "Squid Settings") echo "com.squareup.squidsettings" ;;
    "Local Connect") echo "com.squareup.localconnect" ;;
    OOB)             echo "com.squareup.oob" ;;
    Team)            echo "com.squareup.payroll" ;;
    *) echo "com.squareup.square" ;;
  esac
}

# --- Android device string mapping ---
get_device_string() {
  case "$1" in
    X2A)  echo "Square Square Hodor on msm8916_64 SQUID" ;;
    X2B)  echo "Square Square Hodor on sdm660_64 SQUID" ;;
    X2C)  echo "Square Square X2c SQUID" ;;
    T2A)  echo "Square Square T2 on msm8916_64 SQUID" ;;
    T2B)  echo "Square Square T2 on sdm660_64 SQUID" ;;
    T3A)  echo "Square Square T3a SQUID" ;;
    COTS) echo "samsung samsung SM-A146U1" ;;
    *) echo "samsung samsung SM-A146U1" ;;
  esac
}

# --- Build user-agent for Mobile ---
build_user_agent() {
  local bundle_id
  bundle_id=$(get_bundle_id "$APP_VERTICAL")

  if [[ "$MOBILE_OS" == "iOS" ]]; then
    echo "Mozilla/5.0 (iPhone12,1; CPU iPhone OS 18_1_1 like Mac OS X; en-us) Version/${APP_VERSION} ${bundle_id}/45bcc3d PointOfSaleSDK/${APP_VERSION}"
  else
    local device_string
    device_string=$(get_device_string "$DEVICE")
    echo "${bundle_id}/45bcc3d (Android 10; ${device_string}; en_US) Version/${APP_VERSION} PointOfSaleSDK/${APP_VERSION}"
  fi
}

# --- Build user_attributes JSON array ---
build_user_attributes() {
  local attrs="[]"

  # String attributes
  for attr in "${ATTRIBUTES[@]+"${ATTRIBUTES[@]}"}"; do
    [[ -z "$attr" ]] && continue
    local key="${attr%%=*}"
    local value="${attr#*=}"
    attrs=$(echo "$attrs" | jq --arg k "$key" --arg v "$value" '. + [{"name": $k, "string_value": $v}]')
  done

  # Integer attributes
  for attr in "${ATTRIBUTES_INT[@]+"${ATTRIBUTES_INT[@]}"}"; do
    [[ -z "$attr" ]] && continue
    local key="${attr%%=*}"
    local value="${attr#*=}"
    attrs=$(echo "$attrs" | jq --arg k "$key" --argjson v "$value" '. + [{"name": $k, "int_value": $v}]')
  done

  # Boolean attributes
  for attr in "${ATTRIBUTES_BOOL[@]+"${ATTRIBUTES_BOOL[@]}"}"; do
    [[ -z "$attr" ]] && continue
    local key="${attr%%=*}"
    local value="${attr#*=}"
    attrs=$(echo "$attrs" | jq --arg k "$key" --argjson v "$value" '. + [{"name": $k, "bool_value": $v}]')
  done

  # Double attributes
  for attr in "${ATTRIBUTES_DOUBLE[@]+"${ATTRIBUTES_DOUBLE[@]}"}"; do
    [[ -z "$attr" ]] && continue
    local key="${attr%%=*}"
    local value="${attr#*=}"
    attrs=$(echo "$attrs" | jq --arg k "$key" --argjson v "$value" '. + [{"name": $k, "double_value": $v}]')
  done

  # Dashboard Web auto-injected attributes
  if [[ "$PLATFORM" == "Dashboard Web" ]]; then
    attrs=$(echo "$attrs" | jq '. + [
      {"name": "product", "string_value": "dashboard"},
      {"name": "platform", "string_value": "web"},
      {"name": "server.application", "string_value": "experiment-relay"}
    ]')
  fi

  echo "$attrs"
}

# --- Build context object for multi-context ---
build_context_object() {
  local ctx_type="$1"
  local ctx_token="$2"

  case "$ctx_type" in
    MERCHANT)
      jq -n --arg t "$ctx_token" '{"type": "MERCHANT", "merchant": {"merchant_token": $t}}'
      ;;
    UNIT)
      jq -n --arg t "$ctx_token" '{"type": "UNIT", "unit": {"unit_token": $t}}'
      ;;
    PERSON)
      jq -n --arg t "$ctx_token" '{"type": "PERSON", "person": {"person_token": $t}}'
      ;;
    SQUARE_MOBILE_DEVICE)
      jq -n --arg t "$ctx_token" '{"type": "SQUARE_MOBILE_DEVICE", "device": {"device_id": $t, "additional_device_attributes": {"user_attributes": []}}}'
      ;;
    *)
      echo "Error: Unknown context type: $ctx_type" >&2
      exit 1
      ;;
  esac
}

# --- Map token type for single_user_context ---
get_api_token_type() {
  case "$1" in
    SQUARE_MOBILE_DEVICE) echo "DEVICE_ID" ;;
    *) echo "$1" ;;
  esac
}

# --- Build the request payload ---
build_payload() {
  local flag_type="$1"
  local user_attrs
  user_attrs=$(build_user_attributes)

  local user_attrs_or_null="null"
  if [[ $(echo "$user_attrs" | jq 'length') -gt 0 ]]; then
    user_attrs_or_null="$user_attrs"
  fi

  if [[ ${#CONTEXTS[@]} -gt 0 ]]; then
    # Multi-context mode
    local contexts_array="[]"
    for ctx in "${CONTEXTS[@]}"; do
      local ctx_type="${ctx%%:*}"
      local ctx_token="${ctx#*:}"
      local ctx_obj
      ctx_obj=$(build_context_object "$ctx_type" "$ctx_token")
      contexts_array=$(echo "$contexts_array" | jq --argjson obj "$ctx_obj" '. + [$obj]')
    done

    # Add fake SQUARE_MOBILE_DEVICE for non-Mobile platforms if user_attributes exist
    if [[ "$PLATFORM" != "Mobile" && $(echo "$user_attrs" | jq 'length') -gt 0 ]]; then
      local has_device=false
      for ctx in "${CONTEXTS[@]}"; do
        if [[ "${ctx%%:*}" == "SQUARE_MOBILE_DEVICE" ]]; then
          has_device=true
          break
        fi
      done
      if [[ "$has_device" == "false" ]]; then
        local fake_device
        fake_device=$(jq -n --argjson attrs "$user_attrs" '{
          "type": "SQUARE_MOBILE_DEVICE",
          "device": {
            "device_id": "fake",
            "additional_device_attributes": {
              "user_attributes": ($attrs + [{"name": "fake", "string_value": "fake"}])
            }
          }
        }')
        contexts_array=$(echo "$contexts_array" | jq --argjson obj "$fake_device" '. + [$obj]')
      fi
    fi

    jq -n \
      --arg project "$PROJECT" \
      --arg flag_key "$FLAG_KEY" \
      --arg flag_type "$flag_type" \
      --arg default_type "$DEFAULT_CONTEXT_TYPE" \
      --argjson contexts "$contexts_array" \
      '{
        "project": $project,
        "flag_key": $flag_key,
        "multi_user_context": {
          "default_type": $default_type,
          "user_contexts": $contexts
        },
        "flag_type": $flag_type
      }'
  else
    # Single-context mode
    local api_token_type
    api_token_type=$(get_api_token_type "$TOKEN_TYPE")

    if [[ "$PLATFORM" != "Mobile" && $(echo "$user_attrs" | jq 'length') -gt 0 ]]; then
      # Need multi_user_context to carry attributes via fake device
      local primary_ctx
      primary_ctx=$(build_context_object "$TOKEN_TYPE" "$TOKEN")
      local fake_device
      fake_device=$(jq -n --argjson attrs "$user_attrs" '{
        "type": "SQUARE_MOBILE_DEVICE",
        "device": {
          "device_id": "fake",
          "additional_device_attributes": {
            "user_attributes": ($attrs + [{"name": "fake", "string_value": "fake"}])
          }
        }
      }')

      jq -n \
        --arg project "$PROJECT" \
        --arg flag_key "$FLAG_KEY" \
        --arg flag_type "$flag_type" \
        --arg default_type "$TOKEN_TYPE" \
        --argjson primary "$primary_ctx" \
        --argjson device "$fake_device" \
        '{
          "project": $project,
          "flag_key": $flag_key,
          "multi_user_context": {
            "default_type": $default_type,
            "user_contexts": [$primary, $device]
          },
          "flag_type": $flag_type
        }'
    else
      jq -n \
        --arg project "$PROJECT" \
        --arg flag_key "$FLAG_KEY" \
        --arg token "$TOKEN" \
        --arg token_type "$api_token_type" \
        --arg flag_type "$flag_type" \
        --argjson user_attrs "$user_attrs_or_null" \
        '{
          "project": $project,
          "flag_key": $flag_key,
          "single_user_context": {
            "user_token": {
              "token": $token,
              "type": $token_type
            },
            "user_attributes": $user_attrs
          },
          "flag_type": $flag_type
        }'
    fi
  fi
}

# --- Strip HTML tags ---
strip_html() {
  sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/"/g; s/&#39;/'"'"'/g'
}

# --- Extract LD link from HTML ---
extract_ld_link() {
  grep -oE 'href="(https://app\.launchdarkly\.com[^"]*)"' | head -1 | sed 's/href="//; s/"$//' || true
}

# --- Error message mapping ---
get_error_message() {
  case "$1" in
    SDK_ERROR)          echo "SDK encountered an error while evaluating the flag." ;;
    INVALID_REQUEST)    echo "Invalid Merchant or Unit Token." ;;
    NOT_FOUND)          echo "Flag not found in project ${PROJECT}." ;;
    WRONG_TYPE)         echo "Flag type mismatch." ;;
    SERVICE_NOT_READY)  echo "LaunchDarkly SDK is not ready." ;;
    MISSING_USER_TOKEN) echo "User authentication token is missing." ;;
    *)                  echo "Unknown error: $1" ;;
  esac
}

# --- Make the API call ---
call_api() {
  local flag_type="$1"
  local domain
  domain=$(get_domain "$ENV")
  local url="https://${domain}/1.0/features/flag-evaluation-details"

  local payload
  payload=$(build_payload "$flag_type")

  local curl_args=(
    -s -X POST "$url"
    -H "Content-Type: application/json"
    -H "Origin: https://${domain}"
    -d "$payload"
  )

  # Add user-agent for Mobile platform
  if [[ "$PLATFORM" == "Mobile" ]]; then
    local ua
    ua=$(build_user_agent)
    curl_args+=(-H "User-Agent: ${ua}")
  fi

  curl "${curl_args[@]}"
}

# --- Format and display the response ---
format_response() {
  local response="$1"

  local status
  status=$(echo "$response" | jq -r '.status // "UNKNOWN"')

  if [[ "$status" != "SUCCESS" ]]; then
    local error_msg
    error_msg=$(get_error_message "$status")
    echo "$response" | jq --arg msg "$error_msg" '{
      status: .status,
      error_message: $msg,
      raw_reason: (.human_readable_evaluation_reason // null)
    }'
    return 1
  fi

  # Extract the value based on flag type
  local reason_html
  reason_html=$(echo "$response" | jq -r '.human_readable_evaluation_reason // ""')
  local reason_text
  reason_text=$(echo "$reason_html" | strip_html)
  local ld_link
  ld_link=$(echo "$reason_html" | extract_ld_link)

  echo "$response" | jq \
    --arg reason "$reason_text" \
    --arg ld_link "$ld_link" \
    '{
      status: .status,
      value: (if .bool_value == true or .bool_value == false then .bool_value elif .string_value != null then .string_value elif .int_value != null then .int_value elif .double_value != null then .double_value elif .json_value != null then .json_value else null end),
      evaluation_reason: $reason,
      launchdarkly_link: (if $ld_link != "" then $ld_link else null end),
      user_attributes: .user_attributes,
      user_context_attributes: .user_context_attributes
    }'
}

# --- Main ---
main() {
  local response
  response=$(call_api "$FLAG_TYPE")

  local status
  status=$(echo "$response" | jq -r '.status // "UNKNOWN"')

  format_response "$response"
}

main
