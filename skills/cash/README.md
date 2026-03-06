# Cash

> Unified CLI for iOS and Android mobile app developer tasks — build, test, lint, run, and manage modules.

## What it does

Provides a unified command-line interface for common mobile development tasks across both iOS and Android repositories. Auto-detects which platform you're working in and surfaces relevant commands for building, testing, linting, running apps on simulators/emulators, managing modules, and handling platform-specific workflows like snapshot testing, localization, and feature flags.

## Usage

Use when building, testing, linting, or running mobile apps. The CLI auto-detects iOS vs Android based on the repository. Invoke commands directly or ask for help discovering available commands.

Trigger phrases:
- "Build the iOS app"
- "Run tests for this module"
- "Lint the codebase"
- "Run the app on a simulator"

## Examples

- "Build the UIKit module with debug config"
- "Run only changed tests with `--dirty`"
- "Login to the app with test@example.com"

## Why it was created

Mobile development involves many platform-specific build tools and commands. This skill unifies them behind a single CLI that auto-detects context, reducing the need to remember Bazel vs Gradle commands and platform-specific flags.
