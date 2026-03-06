# Agent Browser

> Fast, token-efficient browser automation for debugging and interaction.

## What it does

Provides a CLI-based browser automation tool for navigating web apps, taking screenshots, filling forms, clicking buttons, and scraping data. It uses a snapshot-and-ref model where interactive elements are assigned refs (`@e1`, `@e2`) that you use for subsequent interactions. Supports both desktop browsers and iOS Simulator (Mobile Safari), using 93% less context than Playwright MCP.

## Usage

Use when you need to debug visual bugs, interact with web apps, automate browser tasks, or test mobile web experiences. The core workflow is: open a URL → snapshot interactive elements → interact using refs → re-snapshot after navigation.

Trigger phrases:
- "Debug this visual bug"
- "Fill out this form"
- "Take a screenshot of this page"
- "Test this on mobile Safari"

## Examples

- "Open localhost:3000 and screenshot the broken layout"
- "Navigate to the login page, fill in credentials, and submit the form"
- "Open this URL in iOS Simulator on iPhone 16 Pro and take a snapshot"

## Why it was created

Traditional browser automation tools consume large amounts of context and are complex to set up for quick ad-hoc tasks. This skill provides a lightweight, token-efficient alternative for debugging and one-off browser interactions.
