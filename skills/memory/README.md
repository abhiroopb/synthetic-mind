# Memory

> Persistent cross-session memory system with full-text search and progressive disclosure.

## What it does

Memory provides a persistent knowledge store that captures observations across sessions and makes them searchable in future sessions. Built on SQLite with FTS5 full-text search, it supports typed observations (decisions, discoveries, preferences, bugfixes, workflows, people context), progressive 3-layer retrieval (compact index → timeline → full detail), session tracking, automatic compaction, and a web viewer. Most capture happens automatically via a plugin that passively observes tool usage.

## Usage

Memory runs passively in the background, but you can interact with it directly for saves, searches, and management.

**Key commands:**
- `amp-mem search "query"` — Search memory with full-text search
- `amp-mem save <type> "<topic>" "<summary>"` — Save an observation
- `amp-mem context --lines 50` — Load recent context for session priming
- `amp-mem compact` — Compress old entries into weekly summaries
- `amp-mem serve` — Start the web viewer at localhost:37777

## Examples

- `amp-mem search "checkout flow bug"` — Finds all observations related to checkout flow bugs, ranked by relevance.
- `amp-mem save decision "Use Regulator for lookups" "Decided to always use Regulator omniSearch first for merchant token lookups"` — Saves a decision for future reference.
- `amp-mem timeline 42 --window 5` — Shows chronological context around observation #42.

## Why it was created

AI agents lose all context between sessions. Memory solves this by persisting observations, decisions, and discoveries locally, so every new session starts with the accumulated knowledge of all previous ones — without relying on external services.
