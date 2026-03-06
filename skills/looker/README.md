# Looker

> Query and manage Looker dashboards, tiles, queries, looks, and explores via a Python CLI.

## What it does

The Looker skill wraps the Looker SDK in a Python CLI, giving you full access to Looker content. You can search for dashboards and looks, run queries (by slug, ID, or ad-hoc explore), inspect and clone dashboard tiles, manage filters and layouts, discover available data models, and check permissions. It supports concurrent dashboard tile execution, pivot queries, and multiple output formats (JSON, CSV, text).

## Usage

Use this skill when working with Looker URLs, dashboard IDs, explore queries, or when you need to search, run, or modify Looker content. Requires VPN and authentication (API credentials or OAuth).

**Trigger phrases:**
- "Run this Looker dashboard"
- "Search Looker for quarterly revenue"
- "What data is available in the explore?"
- "Clone this tile with a modified date range"
- "Check my Looker permissions for this dashboard"

## Examples

- `"Run all tiles on dashboard 456"` — Executes all queries on the dashboard concurrently and returns results.
- `"Search Looker for 'monthly active users'"` — Searches across dashboards, looks, and folders for matching content.
- `"Clone the revenue tile and change the date filter to this year"` — Duplicates the tile with a modified filter expression.

## Why it was created

Navigating Looker's web UI to find data, run queries, and modify dashboards is time-consuming. This skill brings the full Looker workflow to the command line, enabling fast data exploration and dashboard management without context-switching.
