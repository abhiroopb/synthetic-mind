---
Skill name: android-emulator
Skill description: Manage Android emulators (AVDs) - use when user wants to start, stop, create, list, or manage Android emulators for testing
allowed-tools:
  - Bash(bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh:*)
  - Bash(uname:*)
---

# Android Emulator Manager

Manage Android emulators (AVDs) for testing. Use this skill when the user wants to create, start, stop, or manage Android emulators.

## Scripts Location

- `~/.agents/skills/android-emulator/scripts/android-emulator.sh`

## Quick Commands

### List AVDs

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh list
```

### List Available System Images

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh list-targets
```

### Start an Emulator

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh start <avd-name>
```

### Stop Emulators

```bash
# Stop specific or all
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh stop [serial]
```

### Create New AVD

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh create <name> <system-image> [device]
```

### Delete AVD

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh delete <name>
```

### Wipe AVD Data

```bash
bash ~/.agents/skills/android-emulator/scripts/android-emulator.sh wipe <name>
```

## Common Workflow

1. **List available AVDs** to find one to use
2. **Start the emulator** and wait for boot to complete
3. **Run your tests** (emulator will be visible in a window)
4. **Stop the emulator** when done

## Important

- Android emulators typically take 60-120 seconds to boot
- The script auto-detects the Android SDK at `ANDROID_HOME`, `ANDROID_SDK_ROOT`, or `~/Library/Android/sdk`
- Default device for creation is `pixel_7`; use `list-targets` to see available devices and system images
- The start command uses `-no-snapshot-load` for a clean boot
