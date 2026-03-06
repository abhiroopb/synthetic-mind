#!/bin/bash
# iOS Simulator Management Script
# Usage: ios-simulator.sh <command> [args...]
#
# Commands:
#   list          - List all simulators with their status
#   list-types    - List available device types for creation
#   list-runtimes - List available iOS runtime versions
#   create        - Create a new simulator: create <name> <device-type> <ios-version>
#   delete        - Delete a simulator: delete <udid>
#   start         - Boot a simulator: start <name-or-udid> [timeout-seconds]
#   stop          - Shutdown simulator(s): stop [udid] (omit to stop all)
#   status        - Show booted simulators
#   help          - Show this help message

set -euo pipefail

# Exit codes
EXIT_SUCCESS=0
EXIT_FAILURE=1
EXIT_MISSING_ARG=2
EXIT_TIMEOUT=3
EXIT_NOT_FOUND=4
EXIT_PLATFORM_ERROR=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

check_macos() {
    if [ "$(uname -s)" != "Darwin" ]; then
        log_error "iOS simulators are only available on macOS"
        log_error "Current platform: $(uname -s)"
        exit $EXIT_PLATFORM_ERROR
    fi
}

# Resolve a simulator name to its UDID
resolve_to_udid() {
    local identifier="$1"

    # Check if already a UDID (UUID format)
    if [[ "$identifier" =~ ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$ ]]; then
        echo "$identifier"
        return
    fi

    # Try to find by name
    local udid
    udid=$(xcrun simctl list devices -j 2>/dev/null | \
        jq -r ".devices[][] | select(.name==\"$identifier\" and .isAvailable==true) | .udid" 2>/dev/null | \
        head -1)

    if [ -z "$udid" ] || [ "$udid" = "null" ]; then
        # Fallback: try without jq using grep/sed
        udid=$(xcrun simctl list devices 2>/dev/null | \
            grep -E "^\s+${identifier}\s+\(" | \
            sed -E 's/.*\(([A-F0-9-]+)\).*/\1/' | \
            head -1)
    fi

    if [ -z "$udid" ]; then
        log_error "Simulator not found: $identifier"
        return 1
    fi

    echo "$udid"
}

cmd_list() {
    check_macos

    echo "=== iOS Simulators ==="
    xcrun simctl list devices -j 2>/dev/null | jq -r '
        .devices | to_entries[] |
        select(.value | length > 0) |
        "\n-- \(.key | split(".") | last | gsub("-"; " ")) --",
        (.value[] | "  \(.name) (\(.udid)) (\(.state))\(if .isAvailable then "" else " (Unavailable)" end)")'

    echo ""
    echo "=== Currently Booted ==="
    local booted
    booted=$(xcrun simctl list devices -j 2>/dev/null | jq -r '[.devices[][] | select(.state == "Booted")] | if length == 0 then empty else .[] | "  \(.name) (\(.udid))" end')
    if [ -z "$booted" ]; then
        echo "No simulators booted"
    else
        echo "$booted"
    fi
}

cmd_list_types() {
    check_macos

    echo "=== Available Device Types ==="
    xcrun simctl list devicetypes 2>/dev/null

    echo ""
    echo "Common device types:"
    echo "  - iPhone 15 Pro"
    echo "  - iPhone 15"
    echo "  - iPhone 14 Pro"
    echo "  - iPad Pro (12.9-inch) (6th generation)"
    echo "  - iPad (10th generation)"
}

cmd_list_runtimes() {
    check_macos

    echo "=== Available iOS Runtimes ==="
    xcrun simctl list runtimes iOS 2>/dev/null || xcrun simctl list runtimes

    echo ""
    echo "To install additional runtimes:"
    echo "  Open Xcode > Settings > Platforms > + button"
}

cmd_create() {
    local name="${1:-}"
    local device_type="${2:-}"
    local runtime="${3:-}"

    if [ -z "$name" ]; then
        log_error "Missing simulator name"
        echo "Usage: ios-simulator.sh create <name> <device-type> <ios-version>"
        echo "Example: ios-simulator.sh create \"My iPhone\" \"iPhone 15 Pro\" 17.2"
        exit $EXIT_MISSING_ARG
    fi

    if [ -z "$device_type" ]; then
        log_error "Missing device type"
        echo "Usage: ios-simulator.sh create <name> <device-type> <ios-version>"
        echo "Run 'ios-simulator.sh list-types' to see available device types"
        exit $EXIT_MISSING_ARG
    fi

    if [ -z "$runtime" ]; then
        log_error "Missing iOS version"
        echo "Usage: ios-simulator.sh create <name> <device-type> <ios-version>"
        echo "Run 'ios-simulator.sh list-runtimes' to see available runtimes"
        exit $EXIT_MISSING_ARG
    fi

    check_macos

    log_info "Creating simulator: $name"
    log_info "Device type: $device_type"
    log_info "iOS version: $runtime"

    # Format runtime - convert version to full identifier if needed
    # e.g., "18.0" -> "com.apple.CoreSimulator.SimRuntime.iOS-18-0"
    local runtime_id
    if [[ "$runtime" =~ ^[0-9]+\.[0-9]+$ ]]; then
        # Convert X.Y to iOS-X-Y format
        local version_dashed="${runtime//./-}"
        runtime_id="com.apple.CoreSimulator.SimRuntime.iOS-${version_dashed}"
    elif [[ "$runtime" =~ ^com\.apple\.CoreSimulator ]]; then
        # Already a full identifier
        runtime_id="$runtime"
    else
        # Try as-is (might be "iOS X.Y" format for older Xcode)
        runtime_id="$runtime"
    fi

    local udid
    udid=$(xcrun simctl create "$name" "$device_type" "$runtime_id" 2>&1) || {
        log_error "Failed to create simulator"
        echo "$udid"
        exit $EXIT_FAILURE
    }

    log_info "Simulator created successfully"
    log_info "Name: $name"
    log_info "UDID: $udid"
}

cmd_delete() {
    local identifier="${1:-}"

    if [ -z "$identifier" ]; then
        log_error "Missing simulator UDID or name"
        echo "Usage: ios-simulator.sh delete <udid-or-name>"
        exit $EXIT_MISSING_ARG
    fi

    check_macos

    local udid
    udid=$(resolve_to_udid "$identifier") || exit $EXIT_NOT_FOUND

    log_info "Deleting simulator: $udid"

    # Shutdown first if running
    xcrun simctl shutdown "$udid" 2>/dev/null || true

    xcrun simctl delete "$udid" || {
        log_error "Failed to delete simulator"
        exit $EXIT_FAILURE
    }

    log_info "Simulator deleted: $udid"
}

cmd_start() {
    local identifier="${1:-}"
    local timeout="${2:-60}"

    if [ -z "$identifier" ]; then
        log_error "Missing simulator name or UDID"
        echo "Usage: ios-simulator.sh start <name-or-udid> [timeout-seconds]"
        echo "Run 'ios-simulator.sh list' to see available simulators"
        exit $EXIT_MISSING_ARG
    fi

    check_macos

    local udid
    udid=$(resolve_to_udid "$identifier") || exit $EXIT_NOT_FOUND

    # Check if already booted
    if xcrun simctl list devices -j 2>/dev/null | jq -e ".devices[][] | select(.udid==\"$udid\" and .state==\"Booted\")" > /dev/null 2>&1; then
        log_info "Simulator already booted: $udid"
        open -a Simulator
        exit $EXIT_SUCCESS
    fi

    log_info "Booting simulator: $identifier"
    log_info "UDID: $udid"

    # Boot the simulator
    xcrun simctl boot "$udid" 2>/dev/null || {
        # May fail if already booting - that's ok
        true
    }

    log_info "Waiting for boot (timeout: ${timeout}s)..."

    local waited=0
    while [ $waited -lt $timeout ]; do
        if xcrun simctl list devices -j 2>/dev/null | jq -e ".devices[][] | select(.udid==\"$udid\" and .state==\"Booted\")" > /dev/null 2>&1; then
            log_info "Simulator booted successfully"
            # Open Simulator.app after boot so it shows the device we just booted
            # (opening before boot causes Simulator to auto-boot a default device)
            open -a Simulator
            echo ""
            echo "=== Booted Simulator ==="
            xcrun simctl list devices -j 2>/dev/null | jq -r ".devices[][] | select(.udid==\"$udid\") | \"  \(.name) (\(.udid)) (\(.state))\""
            exit $EXIT_SUCCESS
        fi
        sleep 2
        waited=$((waited + 2))
        echo -n "."
    done
    echo ""

    log_error "Timeout waiting for simulator boot after ${timeout}s"
    log_warn "Simulator may still be starting. Check with: ios-simulator.sh status"
    exit $EXIT_TIMEOUT
}

cmd_stop() {
    local identifier="${1:-}"

    check_macos

    if [ -n "$identifier" ]; then
        local udid
        udid=$(resolve_to_udid "$identifier") || exit $EXIT_NOT_FOUND

        log_info "Shutting down simulator: $udid"
        xcrun simctl shutdown "$udid" 2>/dev/null || {
            log_warn "Simulator may already be shut down"
        }
        log_info "Simulator shutdown complete"
    else
        log_info "Shutting down all simulators..."
        xcrun simctl shutdown all 2>/dev/null || true

        # Give simulators time to shut down
        sleep 2

        # Verify shutdown
        local remaining
        remaining=$(xcrun simctl list devices -j 2>/dev/null | jq '[.devices[][] | select(.state == "Booted")] | length')
        if [ "$remaining" -eq 0 ]; then
            log_info "All simulators shut down"
        else
            log_warn "$remaining simulator(s) may still be shutting down"
        fi
    fi
}

cmd_status() {
    check_macos

    echo "=== Booted Simulators ==="
    local booted
    booted=$(xcrun simctl list devices -j 2>/dev/null | jq -r '[.devices[][] | select(.state == "Booted")] | if length == 0 then empty else .[] | "  \(.name) (\(.udid))" end')
    if [ -z "$booted" ]; then
        echo "No simulators booted"
    else
        echo "$booted"
    fi
}

cmd_help() {
    cat << 'EOF'
iOS Simulator Management Script

Usage: ios-simulator.sh <command> [args...]

Commands:
  list              List all simulators and their status
  list-types        List available device types for creation
  list-runtimes     List available iOS runtime versions
  create            Create a new simulator
                    Usage: create <name> <device-type> <ios-version>
                    Example: create "My iPhone" "iPhone 15 Pro" 17.2
  delete            Delete a simulator
                    Usage: delete <udid-or-name>
  start             Boot a simulator and wait for it to be ready
                    Usage: start <name-or-udid> [timeout-seconds]
                    Default timeout: 60 seconds
  stop              Shutdown simulator(s)
                    Usage: stop [udid-or-name]
                    Omit identifier to stop all simulators
  status            Show currently booted simulators
  help              Show this help message

Requirements:
  - macOS with Xcode installed
  - Xcode Command Line Tools (xcode-select --install)

Exit Codes:
  0 - Success
  1 - General failure
  2 - Missing required argument
  3 - Timeout waiting for boot
  4 - Required tool or simulator not found
  5 - Platform not supported (not macOS)

Examples:
  ios-simulator.sh list
  ios-simulator.sh start "iPhone 15 Pro"
  ios-simulator.sh start "iPhone 15 Pro" 90
  ios-simulator.sh stop
  ios-simulator.sh stop "iPhone 15 Pro"
  ios-simulator.sh create "Test Phone" "iPhone 15 Pro" 17.2
EOF
}

# Main dispatch
case "${1:-help}" in
    list)
        cmd_list
        ;;
    list-types)
        cmd_list_types
        ;;
    list-runtimes)
        cmd_list_runtimes
        ;;
    create)
        cmd_create "${2:-}" "${3:-}" "${4:-}"
        ;;
    delete)
        cmd_delete "${2:-}"
        ;;
    start)
        cmd_start "${2:-}" "${3:-60}"
        ;;
    stop)
        cmd_stop "${2:-}"
        ;;
    status)
        cmd_status
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        cmd_help
        exit $EXIT_FAILURE
        ;;
esac
