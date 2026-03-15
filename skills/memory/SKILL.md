---
Skill name: memory
Skill description: Persistent cross-session memory system. Automatically captures observations, generates semantic summaries, and makes them available to future sessions. Use when saving context, recalling past work, searching memory, or at session end to persist learnings.
---

# Memory — Persistent Cross-Session Context

A claude-mem-inspired persistent memory system for Amp. Uses SQLite + FTS5 for storage and search, with a web viewer UI and progressive disclosure.

## Architecture

- **Database**: `~/.amp/memory/amp-mem.db` (SQLite + FTS5 full-text search)
- **CLI**: `~/bin/amp-mem` (all operations)
- **Web viewer**: `amp-mem serve` → http://localhost:37777 (self-contained in CLI, no external files needed)
- **Knowledge file**: `~/.amp/memory/knowledge.md` (also maintained for plain-text access)

## Observation Types

Use these types when saving to enable filtering:

| Type | When to use |
|---|---|
| `observation` | General knowledge learned about the codebase, tools, or systems |
| `decision` | A design decision, approach chosen, or trade-off made |
| `discovery` | A bug found, root cause identified, or non-obvious behavior uncovered |
| `preference` | User preference for how things should be done |
| `bugfix` | A bug fix — what was broken, why, and how it was fixed |
| `session` | End-of-session summary |
| `config` | Configuration, URLs, credentials locations, environment details |
| `workflow` | A new workflow, command sequence, or process established |
| `people` | Team structure, ownership, who to contact |
| `thread` | Ingested Amp thread summary (auto-captured on session start) |

## CLI Reference

### Save an observation
```bash
amp-mem save <type> "<topic>" "<summary>" [--project NAME] [--file PATH] [--tags "a,b,c"] [--session ID] [--private]
```

### Search memory (FTS5 — ranked results, compact index)
```bash
amp-mem search "query" [--type TYPE] [--project PROJECT] [--after DATE] [--before DATE] [--limit N] [--include-private]
```

### Progressive Disclosure (3-layer retrieval)
```bash
# Layer 1: Compact index (~50 tokens/result)
amp-mem search "checkout flow"

# Layer 2: Timeline — chronological context around a result
amp-mem timeline 42 --window 5

# Layer 3: Full details for specific IDs
amp-mem detail 42 43 44
```

### Session priming (recent context for session start)
```bash
amp-mem context --lines 50
```

### Compact old entries (compress into weekly summaries)
```bash
amp-mem compact --older-than 30
```

### Ingest an Amp thread (de-duplicated by thread ID)
```bash
amp-mem ingest-thread <thread_id> "<title>" "<summary>" [--date DATE] [--url URL] [--tags "a,b"]
```

### Other commands
```bash
amp-mem stats                    # Memory statistics
amp-mem export --format json     # Export all memory
amp-mem export --format md       # Export as markdown
amp-mem serve --port 37777       # Start web viewer
amp-mem session-start            # Start a new session (returns ID)
amp-mem session-end --session 1  # End a session
amp-mem migrate                  # Import legacy sessions.jsonl
amp-mem decay                    # Apply confidence decay to aging observations
```

## Auto-Capture Protocol

### What to capture (be selective)

Save a memory entry when something **worth recalling in a future session** occurs:

> **Note:** When the amp-mem plugin (`~/.config/amp/plugins/amp-mem.ts`) is installed, most of this capture happens automatically. The plugin passively captures tool results (Linear, Gmail, Slack, Notion, Google Drive, Bash), batches file edits, and AI-gates observations at agent.end with p>0.65 threshold. Context injection is silent (`display: false`), one-shot per session (duplicate prevention), uses a 60-line budget with smart sentence-boundary truncation, and filters out self-referential amp-mem observations. The protocol below describes what gets captured — you don't need to do it manually.

1. **Significant file edits** — non-trivial changes where the "why" matters (skip typo fixes, formatting)
2. **Revealing bash commands** — commands that expose system state, configuration, or non-obvious behavior (skip routine ls/cat/grep)
3. **Project discovery** — architecture, conventions, setup learned
4. **Decision made** — design decisions, approach chosen, trade-offs
5. **Problem solved** — bug fixed, workaround found, root cause identified
6. **Configuration found** — service URLs, API patterns, file locations
7. **Tool/workflow learned** — new workflow, command sequence, integration pattern
8. **Preference expressed** — how the user wants things done
9. **Context about people/teams** — ownership, contacts, team structures
10. **Session end** — always save a comprehensive session summary

### How to capture efficiently

For rapid-fire observations during a session, batch them:

```bash
# Quick inline save after a tool use
amp-mem save observation "POS receipt locale bug" "ReceiptRenderer.kt was missing locale config for AU region. Fixed by adding Locale.AU to the SUPPORTED_LOCALES map at line 142." --project "checkout-flow" --file "src/receipt/ReceiptRenderer.kt" --tags "bugfix,pos,au"
```

### Session Start Protocol

1. Initialize or ensure DB exists: `amp-mem init` (idempotent)
2. Load recent context: `amp-mem context --lines 50`
3. Optionally start a session: `amp-mem session-start --thread-url <URL>`

### Session End Protocol

1. Save a comprehensive session summary
2. End the session: `amp-mem session-end --summary "..."`
3. Run compaction if needed: `amp-mem compact`

## Web Viewer

Start with `amp-mem serve` to browse memory at http://localhost:37777.

Features:
- **Stream view** — paginated list of all observations, newest first
- **Search** — FTS5 full-text search with type/project filters
- **Stats** — observation counts, breakdowns by type and project
- **Progressive disclosure** — click any observation to expand full details

## Privacy

- All data stays local in `~/.amp/memory/`
- No external APIs or network calls
- User can directly edit/delete entries in the SQLite database
- The knowledge.md file can be manually edited for quick corrections
- **Privacy tags:** When a user's message contains `<private>`, all observations from that turn are saved with `--private` and excluded from context injection and default search
- **Explicit private saves:** Use `amp_mem_save` with `private: true` or `amp-mem save ... --private` to mark specific observations as private
- **Revealing private entries:** Use `amp-mem search <query> --include-private` to include private observations in search results
