# iOS simulator

> Manage iOS simulators — create, start, stop, list, and delete simulator devices for testing.

## What it does

This skill manages iOS simulators on macOS for mobile app testing. It can list available simulators, start and stop devices, create new simulators with specific device types and iOS versions, and delete unused ones. The start command automatically opens the Simulator app so you can see the device visually.

## Usage

Use when you need to create, start, stop, or manage iOS simulators for testing. Requires macOS with Xcode installed.

## Examples

- "List all available iOS simulators"
- "Start an iPhone 15 Pro simulator"
- "Create a new iPad simulator running iOS 18"

## Why it was created

Managing iOS simulators through Xcode's UI is cumbersome when you need to quickly spin up devices for testing. This skill provides simple CLI commands to manage the full simulator lifecycle.
