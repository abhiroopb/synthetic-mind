# Android Emulator

> Manage Android emulators (AVDs) for testing — create, start, stop, list, and wipe.

## What it does

Wraps Android SDK emulator management into simple commands for creating, starting, stopping, listing, and wiping Android Virtual Devices (AVDs). Auto-detects the Android SDK location and provides a clean boot experience. Emulators typically take 60-120 seconds to boot.

## Usage

Use when you need to spin up an Android emulator for testing, manage existing AVDs, or set up a new virtual device. The default device for creation is Pixel 7.

Trigger phrases:
- "Start an Android emulator"
- "List my AVDs"
- "Create a new Android emulator"
- "Stop all emulators"

## Examples

- "List available Android emulators"
- "Start the Pixel 7 emulator for testing"
- "Create a new AVD with the latest system image"

## Why it was created

Managing Android emulators through raw SDK commands is verbose and error-prone. This skill provides a simple wrapper that handles SDK path detection and common workflows in a single command.
