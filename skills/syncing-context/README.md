# Syncing Context

> Refresh the lightweight state layer after a plan change or before a follow-on session.

This skill rebuilds the public AI PM OS state files from the current launch plan. It is the maintenance pass that keeps `system/state/` aligned with `system/today-plan.json`.

## What it does

- rebuilds `system/state/queue.json`
- rebuilds `system/state/now.json`
- mirrors the latest `system/today-plan.json` into `system/state/sources/plan.json`
- summarizes the current top recommendation once the refresh is done

## When to use it

- "sync PM OS"
- "refresh the queue"
- "rebuild the state layer"
- "sync context after I updated the plan"

## Why it matters

The file-backed state layer is what lets the operating system resume cleanly between sessions. This skill gives you a fast way to refresh that layer without rerunning a full start-of-day flow.
