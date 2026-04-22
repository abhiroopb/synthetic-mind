# Closing Day

> Wrap the day with a short carry-forward snapshot so tomorrow starts from a real handoff.

This skill is the end-of-day counterpart to a start-of-day workflow. It reads today's note plus the lightweight state layer, adds a compact `## End Of Day` section when needed, and captures the few things that matter tomorrow.

## What it does

- reads today's note in `notes/daily/`
- checks `system/state/now.json` and `system/state/queue.json` when available
- appends a short `## End Of Day` section if it's missing
- captures what moved, what carries forward, what is waiting, and what to start with tomorrow

## When to use it

- "end of day"
- "close of day"
- "wrap the day"
- "leave me a snapshot for tomorrow"

## Why it matters

The point is not journaling. The point is continuity. This turns a fuzzy memory of the day into a concrete next-starting point for the next session.
