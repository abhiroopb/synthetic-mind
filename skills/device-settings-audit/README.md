# Device settings audit

> Query device profile change history to investigate who changed what and when.

## What it does

This skill queries the audit log for device profile changes — including creates, updates, and device-to-profile links. It supports filtering by merchant, location, employee, event type, and time range. For update events, it diffs the before/after profiles field by field to show exactly what changed.

## Usage

Use when investigating device profile changes for a merchant — who made them, when they occurred, and what settings were modified. Results are grouped by profile and presented in reverse chronological order with detailed field-level diffs.

## Examples

- "Show me all device profile changes for merchant MLFQVZ8YWP1A6 in the last week"
- "Who updated the tipping settings on this merchant's profiles?"
- "Show the change history for this location's device profiles"

## Why it was created

When merchants report unexpected device behavior, it's critical to trace what settings changed and who changed them. This skill makes audit log queries fast and presents results in a readable, diffed format.
