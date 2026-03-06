# Free disk space

> Survey and clean up disk space on macOS developer machines by targeting known storage-heavy locations.

## What it does

This skill scans known locations where storage accumulates on developer machines — Gradle caches, Xcode derived data, npm/yarn caches, Android emulators, Homebrew downloads, Bazel caches, and more. It categorizes each location by safety level (safe to delete, use caution, keep), shows exact cleanup commands, and executes only with explicit user approval.

## Usage

Use when your disk is full, running low on space, or you want to reclaim storage. The skill surveys, categorizes, presents options with sizes, and waits for your approval before deleting anything.

## Examples

- "How much disk space can I reclaim?"
- "Clean up my Xcode and Gradle caches"
- "Survey my disk and show me what's safe to delete"

## Why it was created

Developer machines accumulate gigabytes of caches, build artifacts, and unused simulators over time. This skill knows exactly where to look and what's safe to remove, saving you from manually hunting for space.
