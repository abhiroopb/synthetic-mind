# Feature overview updater

> Scan the features directory and regenerate README index tables with current status, owners, and dates.

## What it does

This skill scans all feature directories to collect metadata (name, product area, status, owner, last updated) from overview files, then regenerates master and area-specific README index tables. It flags stale features — those not updated in 90+ days, stuck in draft for 60+ days, or missing overview files — and reports all changes made.

## Usage

Use when you need to refresh the feature index tables after adding, updating, or archiving features. The skill only modifies README index files, never the feature documents themselves.

## Examples

- "Update the feature overview index"
- "Scan features and flag any stale entries"
- "Regenerate the README tables for all product areas"

## Why it was created

Manually maintaining feature index tables is tedious and they quickly drift out of date. This skill automates the scan-and-rebuild process so the index always reflects the current state of all features.
