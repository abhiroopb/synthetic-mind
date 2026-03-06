---
name: ios-simulator
description: Manage iOS simulators - use when user wants to start, stop, create, or manage iOS simulators for testing
roles: [mobile, cash-ios]
allowed-tools:
  - Bash(bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh:*)
  - Bash(uname:*)
---

# iOS Simulator Manager

Manage iOS simulators for testing. Use this skill when the user wants to create, start, stop, or manage iOS simulators.

## Current State

- Platform: !`uname -s`
- Booted simulators: !`xcrun simctl list devices 2>/dev/null | grep -c "(Booted)" || echo "0 (or not on macOS)"`

## Scripts Location

- `~/.agents/skills/ios-simulator/scripts/ios-simulator.sh`

## Quick Commands

### List Devices

```bash
bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh list
```

### Start a Device

```bash
bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh start <simulator-name>
```

### Stop Devices

```bash
# Stop specific or all
bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh stop [udid]
```

### Create New Device

```bash
bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh create <name> <device-type> <ios-version>
```

### Delete Device

```bash
bash ~/.agents/skills/ios-simulator/scripts/ios-simulator.sh delete <udid>
```

## Common Workflow

1. **List available simulators** to find one to use
2. **Start the simulator** and wait for boot to complete
3. **Run your tests** (simulator will be available in Simulator app)
4. **Stop the simulator** when done

## Important

- **The start command automatically opens the Simulator app** so the user can see the device. Do not start simulators in headless mode unless the user explicitly requests it.

## Tips

- iOS simulators typically boot in 10-30 seconds
- iOS simulators must be on macOS with Xcode installed
- The script supports custom boot timeouts as a second argument
