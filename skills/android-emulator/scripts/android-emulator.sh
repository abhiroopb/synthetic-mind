#!/bin/bash
# Android Emulator Management Script
# Usage: android-emulator.sh <command> [args...]
#
# Commands:
#   list          - List all AVDs (Android Virtual Devices)
#   list-targets  - List available system images for creation
#   create        - Create a new AVD: create <name> <system-image> [device]
#   delete        - Delete an AVD: delete <name>
#   start         - Start an emulator: start <name> [timeout-seconds]
#   stop          - Stop emulator(s): stop [serial] (omit to stop all)
#   status        - Show running emulators
#   wipe          - Wipe data for an AVD: wipe <name>
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

# Resolve Android SDK path
resolve_sdk() {
    if [ -n "${ANDROID_HOME:-}" ]; then
        echo "$ANDROID_HOME"
    elif [ -n "${ANDROID_SDK_ROOT:-}" ]; then
        echo "$ANDROID_SDK_ROOT"
    elif [ -d "$HOME/Library/Android/sdk" ]; then
        echo "$HOME/Library/Android/sdk"
    elif [ -d "$HOME/Android/Sdk" ]; then
        echo "$HOME/Android/Sdk"
    else
        log_error "Android SDK not found. Set ANDROID_HOME or install Android Studio."
        exit $EXIT_PLATFORM_ERROR
    fi
}

SDK_ROOT="$(resolve_sdk)"
EMULATOR="$SDK_ROOT/emulator/emulator"
AVDMANAGER="$SDK_ROOT/cmdline-tools/latest/bin/avdmanager"
ADB="$SDK_ROOT/platform-tools/adb"

check_tool() {
    local tool="$1"
    local name="$2"
    if [ ! -x "$tool" ]; then
        log_error "$name not found at $tool"
        log_error "Install via Android Studio SDK Manager or sdkmanager CLI"
        exit $EXIT_NOT_FOUND
    fi
}

cmd_list() {
    check_tool "$EMULATOR" "emulator"

    echo "=== Android Virtual Devices ==="
    "$EMULATOR" -list-avds 2>/dev/null | while read -r avd; do
        if [ -n "$avd" ]; then
            echo "  $avd"
        fi
    done

    local count
    count=$("$EMULATOR" -list-avds 2>/dev/null | grep -c . || echo 0)
    if [ "$count" -eq 0 ]; then
        echo "  (none)"
        echo ""
        echo "Create one with: android-emulator.sh create <name> <system-image>"
        echo "Run 'android-emulator.sh list-targets' to see available system images"
    fi

    echo ""
    echo "=== Running Emulators ==="
    if [ -x "$ADB" ]; then
        local found=0
        for serial in $("$ADB" devices 2>/dev/null | grep -oE "emulator-[0-9]+"); do
            local avd_name
            avd_name=$("$ADB" -s "$serial" emu avd name 2>/dev/null | head -1 | tr -d '\r' || echo "unknown")
            local api_level
            api_level=$("$ADB" -s "$serial" shell getprop ro.build.version.sdk 2>/dev/null | tr -d '\r' || echo "?")
            echo "  $serial — $avd_name (API $api_level)"
            found=1
        done
        if [ "$found" -eq 0 ]; then
            echo "  No emulators running"
        fi
    else
        echo "  (adb not available to check)"
    fi
}

cmd_list_targets() {
    check_tool "$AVDMANAGER" "avdmanager"

    echo "=== Installed System Images ==="
    "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" --list 2>/dev/null | grep "system-images" | grep "Installed" | awk '{print "  " $1}' || true

    echo ""
    echo "=== Common System Images ==="
    echo "  system-images;android-35;google_apis_playstore;arm64-v8a   (Android 15, Play Store)"
    echo "  system-images;android-34;google_apis_playstore;arm64-v8a   (Android 14, Play Store)"
    echo "  system-images;android-34;google_apis;arm64-v8a             (Android 14, Google APIs)"
    echo "  system-images;android-33;google_apis_playstore;arm64-v8a   (Android 13, Play Store)"

    echo ""
    echo "Install with:"
    echo "  $SDK_ROOT/cmdline-tools/latest/bin/sdkmanager \"system-images;android-35;google_apis_playstore;arm64-v8a\""

    echo ""
    echo "=== Available Devices ==="
    "$AVDMANAGER" list device -c 2>/dev/null | head -20
    echo "  ..."
    echo ""
    echo "Common devices: pixel_7, pixel_8, pixel_9, medium_phone"
}

cmd_create() {
    local name="${1:-}"
    local system_image="${2:-}"
    local device="${3:-pixel_7}"

    if [ -z "$name" ]; then
        log_error "Missing AVD name"
        echo "Usage: android-emulator.sh create <name> <system-image> [device]"
        echo "Example: android-emulator.sh create \"MyPixel\" \"system-images;android-35;google_apis_playstore;arm64-v8a\" pixel_7"
        exit $EXIT_MISSING_ARG
    fi

    if [ -z "$system_image" ]; then
        log_error "Missing system image"
        echo "Usage: android-emulator.sh create <name> <system-image> [device]"
        echo "Run 'android-emulator.sh list-targets' to see available system images"
        exit $EXIT_MISSING_ARG
    fi

    check_tool "$AVDMANAGER" "avdmanager"

    log_info "Creating AVD: $name"
    log_info "System image: $system_image"
    log_info "Device: $device"

    echo "no" | "$AVDMANAGER" create avd \
        --name "$name" \
        --package "$system_image" \
        --device "$device" \
        --force 2>&1 || {
        log_error "Failed to create AVD"
        exit $EXIT_FAILURE
    }

    log_info "AVD created successfully: $name"
}

cmd_delete() {
    local name="${1:-}"

    if [ -z "$name" ]; then
        log_error "Missing AVD name"
        echo "Usage: android-emulator.sh delete <name>"
        exit $EXIT_MISSING_ARG
    fi

    check_tool "$AVDMANAGER" "avdmanager"

    log_info "Deleting AVD: $name"

    "$AVDMANAGER" delete avd --name "$name" 2>&1 || {
        log_error "Failed to delete AVD: $name"
        exit $EXIT_FAILURE
    }

    log_info "AVD deleted: $name"
}

cmd_start() {
    local name="${1:-}"
    local timeout="${2:-120}"

    if [ -z "$name" ]; then
        log_error "Missing AVD name"
        echo "Usage: android-emulator.sh start <name> [timeout-seconds]"
        echo "Run 'android-emulator.sh list' to see available AVDs"
        exit $EXIT_MISSING_ARG
    fi

    check_tool "$EMULATOR" "emulator"

    # Check if AVD exists
    if ! "$EMULATOR" -list-avds 2>/dev/null | grep -qx "$name"; then
        log_error "AVD not found: $name"
        echo "Available AVDs:"
        "$EMULATOR" -list-avds 2>/dev/null | sed 's/^/  /'
        exit $EXIT_NOT_FOUND
    fi

    # Check if already running
    if [ -x "$ADB" ]; then
        local running_name
        for serial in $("$ADB" devices 2>/dev/null | grep -oE "emulator-[0-9]+"); do
            running_name=$("$ADB" -s "$serial" emu avd name 2>/dev/null | head -1 || true)
            if [ "$running_name" = "$name" ]; then
                log_info "Emulator '$name' is already running on $serial"
                exit $EXIT_SUCCESS
            fi
        done
    fi

    log_info "Starting emulator: $name"
    log_info "Timeout: ${timeout}s"

    # Start emulator in background
    "$EMULATOR" -avd "$name" -no-snapshot-load &
    local emu_pid=$!

    # Wait for boot
    if [ -x "$ADB" ]; then
        log_info "Waiting for emulator to boot..."
        local waited=0
        while [ $waited -lt "$timeout" ]; do
            if "$ADB" devices 2>/dev/null | grep -qE "^emulator-.*device$"; then
                # Check if boot animation has finished
                local boot_complete
                boot_complete=$("$ADB" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || echo "")
                if [ "$boot_complete" = "1" ]; then
                    log_info "Emulator booted successfully"
                    echo ""
                    echo "=== Running Emulator ==="
                    "$ADB" devices 2>/dev/null | grep -E "^emulator-" | awk '{print "  " $1 " (" $2 ")"}'
                    exit $EXIT_SUCCESS
                fi
            fi
            sleep 3
            waited=$((waited + 3))
            echo -n "."
        done
        echo ""

        log_error "Timeout waiting for emulator boot after ${timeout}s"
        log_warn "Emulator may still be starting (PID: $emu_pid)"
        log_warn "Check with: android-emulator.sh status"
        exit $EXIT_TIMEOUT
    else
        log_warn "adb not available — cannot wait for boot. Emulator starting in background (PID: $emu_pid)"
        exit $EXIT_SUCCESS
    fi
}

cmd_stop() {
    local serial="${1:-}"

    if [ ! -x "$ADB" ]; then
        log_error "adb not found at $ADB"
        exit $EXIT_NOT_FOUND
    fi

    if [ -n "$serial" ]; then
        log_info "Stopping emulator: $serial"
        "$ADB" -s "$serial" emu kill 2>/dev/null || {
            log_warn "Emulator may already be stopped"
        }
        log_info "Emulator stopped: $serial"
    else
        log_info "Stopping all emulators..."
        local found=0
        for emu in $("$ADB" devices 2>/dev/null | grep -oE "emulator-[0-9]+"); do
            "$ADB" -s "$emu" emu kill 2>/dev/null || true
            log_info "Stopped: $emu"
            found=1
        done
        if [ "$found" -eq 0 ]; then
            log_info "No running emulators found"
        else
            log_info "All emulators stopped"
        fi
    fi
}

cmd_status() {
    if [ ! -x "$ADB" ]; then
        log_error "adb not found at $ADB"
        exit $EXIT_NOT_FOUND
    fi

    echo "=== Running Emulators ==="
    local found=0
    for serial in $("$ADB" devices 2>/dev/null | grep -oE "emulator-[0-9]+"); do
        local avd_name
        avd_name=$("$ADB" -s "$serial" emu avd name 2>/dev/null | head -1 | tr -d '\r' || echo "unknown")
        local api_level
        api_level=$("$ADB" -s "$serial" shell getprop ro.build.version.sdk 2>/dev/null | tr -d '\r' || echo "?")
        echo "  $serial — $avd_name (API $api_level)"
        found=1
    done
    if [ "$found" -eq 0 ]; then
        echo "  No emulators running"
    fi
}

cmd_wipe() {
    local name="${1:-}"

    if [ -z "$name" ]; then
        log_error "Missing AVD name"
        echo "Usage: android-emulator.sh wipe <name>"
        exit $EXIT_MISSING_ARG
    fi

    check_tool "$EMULATOR" "emulator"

    log_info "Wiping data for AVD: $name"

    "$EMULATOR" -avd "$name" -wipe-data -no-window -no-boot-anim &
    local pid=$!
    sleep 5
    kill "$pid" 2>/dev/null || true

    log_info "Data wiped for AVD: $name"
}

cmd_help() {
    cat << 'EOF'
Android Emulator Management Script

Usage: android-emulator.sh <command> [args...]

Commands:
  list              List all AVDs and running emulators
  list-targets      List available system images for creation
  create            Create a new AVD
                    Usage: create <name> <system-image> [device]
                    Example: create "MyPixel" "system-images;android-35;google_apis_playstore;arm64-v8a" pixel_7
                    Default device: pixel_7
  delete            Delete an AVD
                    Usage: delete <name>
  start             Start an emulator and wait for boot
                    Usage: start <name> [timeout-seconds]
                    Default timeout: 120 seconds
  stop              Stop emulator(s)
                    Usage: stop [serial]
                    Omit serial to stop all emulators
  status            Show running emulators with details
  wipe              Wipe user data for an AVD
                    Usage: wipe <name>
  help              Show this help message

Requirements:
  - Android SDK with emulator, platform-tools, and cmdline-tools
  - At least one system image installed
  - ANDROID_HOME set or SDK at ~/Library/Android/sdk

Exit Codes:
  0 - Success
  1 - General failure
  2 - Missing required argument
  3 - Timeout waiting for boot
  4 - Required tool or AVD not found
  5 - Platform/SDK not available

Examples:
  android-emulator.sh list
  android-emulator.sh start MyPixel
  android-emulator.sh start MyPixel 180
  android-emulator.sh stop
  android-emulator.sh stop emulator-5554
  android-emulator.sh create "TestDevice" "system-images;android-35;google_apis_playstore;arm64-v8a"
  android-emulator.sh wipe MyPixel
EOF
}

# Main dispatch
case "${1:-help}" in
    list)
        cmd_list
        ;;
    list-targets)
        cmd_list_targets
        ;;
    create)
        cmd_create "${2:-}" "${3:-}" "${4:-pixel_7}"
        ;;
    delete)
        cmd_delete "${2:-}"
        ;;
    start)
        cmd_start "${2:-}" "${3:-120}"
        ;;
    stop)
        cmd_stop "${2:-}"
        ;;
    status)
        cmd_status
        ;;
    wipe)
        cmd_wipe "${2:-}"
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
