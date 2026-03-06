---
title: "Building a Persistent Memory System for Amp — From Zero to Cross-Session Intelligence"
date: 2026-03-05
author: Abhi Basu
tags: [amp-plugin, memory-system, sqlite, ai-agents, amp-mem, cross-session]
---

# Building a Persistent Memory System for Amp — From Zero to Cross-Session Intelligence

## TL;DR

I built **amp-mem** — a persistent, cross-session memory system for Amp that automatically captures observations, classifies them with AI, and injects relevant context into future sessions. It's a ~500-line bash CLI backed by SQLite + FTS5, paired with a ~490-line TypeScript plugin that hooks into Amp's event system. Every session I start now has context from what I did yesterday, last week, or last month. Here's how I built it, how it works, and how you can build something similar.

## Context

AI coding agents have a fundamental limitation: amnesia. Every new session starts from scratch. You lose context about decisions you made, bugs you fixed, preferences you expressed, and workflows you established. I was tired of re-explaining things.

I'd seen [claude-mem](https://github.com/skydeckai/claude-mem) solve this for Claude Code and thought: Amp's plugin system should make this possible too. Turns out it does — and the result is something I use every single day.

## The Architecture

amp-mem has two components that work together:

**1. A CLI tool** (`~/bin/amp-mem`) — A bash script backed by SQLite with FTS5 full-text search. This is the storage and query layer. It handles saving observations, searching memory, compacting old entries, managing sessions, and even serving a web viewer.

**2. An Amp plugin** (`~/.config/amp/plugins/amp-mem.ts`) — A TypeScript plugin that hooks into Amp's experimental plugin event system. This is the intelligence layer. It decides *what* to capture, *when* to capture it, and *how* to inject context back into sessions.

Here's how they connect:

```
┌────────────────────────────────────────┐
│           Amp Plugin (TypeScript)       │
│                                         │
│  session.start ──→ init, backup, start  │
│  agent.start   ──→ inject context       │
│  agent.end     ──→ AI-gated capture     │
│  tool.result   ──→ structured extract   │
│                                         │
│  Registered tools:                      │
│    amp_mem_search / save / stats        │
└───────────────┬────────────────────────┘
                │ shells out to
                ▼
┌────────────────────────────────────────┐
│           CLI (Bash + SQLite)           │
│                                         │
│  SQLite DB with FTS5 full-text search   │
│  ~/.amp/memory/amp-mem.db               │
│                                         │
│  Commands: save, search, context,       │
│  compact, timeline, detail, stats,      │
│  serve, decay, distill-*, ingest-thread │
└────────────────────────────────────────┘
```

## How It Works: The Event Loop

The plugin hooks into four Amp lifecycle events. Each one does something specific.

### 1. `session.start` — Setting Up

When a new Amp session begins, the plugin:

- Initializes the database (creates it if it doesn't exist)
- Creates a daily backup (keeps 7 days of backups, rotates old ones)
- Starts a new session record linked to the Amp thread URL
- Checks if knowledge distillation is overdue
- Auto-compacts if observations exceed a threshold (100)

```typescript
amp.on('session.start', async (_event, ctx) => {
  await ampMem(ctx.$, ['init'])
  
  // Daily backup
  const today = new Date().toISOString().slice(0, 10)
  // ... backup logic with 7-day rotation ...
  
  // Start session with thread URL linkage
  const threadId = ctx.thread?.id || ''
  const threadUrl = threadId ? `https://ampcode.com/threads/${threadId}` : ''
  const sessionResult = await ampMem(ctx.$, ['session-start', '--thread-url', threadUrl])
  currentSessionId = sessionResult.trim() || null
})
```

### 2. `agent.start` — Injecting Context

This is the magic moment. Before the agent processes each user message, the plugin injects relevant memory context. The agent sees what you've done recently — decisions, preferences, discoveries — without you having to explain anything.

```typescript
amp.on('agent.start', async (event, ctx) => {
  // Save the user's prompt as a session observation
  if (event.message && event.message.length > 20) {
    await ampMem(ctx.$, ['save', 'session', `User prompt: ${promptTopic}`, ...])
  }
  
  // Inject recent memory context
  const context = await ampMem(ctx.$, ['context', '--lines', '20'])
  if (context && context.length > 50) {
    return {
      message: {
        content: `<amp-mem-context>\n${context}\n</amp-mem-context>`,
        display: true,
      },
    }
  }
})
```

The `context` command is itself interesting — it uses a Python script that computes effective confidence scores with time-based decay, allocates line budgets per observation type, and produces a compact, ranked summary. Permanent types (decisions, preferences, configs) never decay. Ephemeral types (sessions, threads) decay with a 7-day half-life.

### 3. `tool.result` — Capturing What You Do

Every time a tool completes, the plugin evaluates whether to capture it. There are three categories:

**Ignored tools** — Pure read-only tools (Read, Grep, glob, finder, web_search) generate zero signal. Skip them.

**File edit tools** — `edit_file` and `create_file` are batched within a turn and saved once at `agent.end`. This prevents noise from 20 individual file edits when refactoring.

**Everything else** — The plugin has structured extractors for high-signal tools:

```typescript
function extractFromTool(event: ToolResultEvent): Extraction | null {
  switch (event.tool) {
    case 'mcp__linear__linear_createIssue':
      return {
        type: 'decision',
        topic: `Created Linear issue: ${input.title}`,
        summary: `Team: ${input.teamId}, Title: ${input.title}...`,
      }
    case 'mcp__slack__slack_post_message':
      return {
        type: 'decision',
        topic: `Posted to Slack: #${input.channel}`,
        summary: `Channel: ${input.channel}\nMessage: ${input.text}`,
      }
    // ... Gmail, Notion, Calendar, Google Drive, Bash ...
  }
}
```

Tools without a dedicated extractor get generic extraction that pulls the most meaningful input parameters.

### 4. `agent.end` — AI-Gated Assessment

This is the most sophisticated part. After each agent turn completes, the plugin uses `ctx.ai.ask()` — Amp's built-in AI assessment API — to evaluate whether the turn contained something worth remembering.

```typescript
const assessment = await ctx.ai.ask(
  `Does this agent conversation turn contain a noteworthy insight worth preserving ` +
  `for future sessions? Classify as: DECISION, DISCOVERY, PREFERENCE, BUGFIX, ` +
  `CONFIG, WORKFLOW, PEOPLE, or OBSERVATION.\n\n` +
  `NOT noteworthy: trivial reads, routine greetings, simple file lookups.\n\n` +
  `Turn summary:\n${turnSummary}`
)

if (assessment.result === 'yes' && assessment.probability > 0.65) {
  // Save with the classified type
  await ampMem(ctx.$, ['save', type, topic, summary])
}
```

The 0.65 probability threshold is the sweet spot I found through iteration. Too low and you capture noise. Too high and you miss useful context. The classification into types (DECISION, DISCOVERY, PREFERENCE, etc.) enables intelligent retrieval later.

## The Storage Layer: SQLite + FTS5

The schema is simple but effective:

```sql
CREATE TABLE observations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    INTEGER REFERENCES sessions(id),
    ts            TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    type          TEXT NOT NULL DEFAULT 'observation',
    topic         TEXT NOT NULL,
    summary       TEXT NOT NULL,
    project       TEXT,
    tags          TEXT,
    confidence    REAL NOT NULL DEFAULT 1.0,
    access_count  INTEGER NOT NULL DEFAULT 0,
    private       INTEGER NOT NULL DEFAULT 0
);

-- FTS5 full-text search with Porter stemming
CREATE VIRTUAL TABLE observations_fts USING fts5(
    topic, summary, project, tags,
    content='observations', content_rowid='id',
    tokenize='porter unicode61'
);
```

Key design choices:

- **FTS5 with Porter stemming** — Fast full-text search that handles word variations ("configure" matches "configuration")
- **Confidence scores** — Each observation has a confidence value that decays over time for ephemeral types but stays permanent for decisions and preferences
- **Access tracking** — Every search bumps the `access_count`, so frequently-accessed observations get ranked higher in context injection
- **Privacy flag** — Observations marked `private` are excluded from context injection and default searches

### Deduplication

The `save` command includes Jaccard similarity-based deduplication. Before inserting a new observation, it searches FTS5 for candidates with matching topic words and computes word-overlap similarity. If similarity > 0.6, it supersedes the existing observation instead of creating a duplicate — updating the content and boosting confidence by 0.1.

```bash
# Jaccard word-overlap similarity
_jaccard() {
    python3 -c "
import sys
a = set(sys.argv[1].lower().split())
b = set(sys.argv[2].lower().split())
if not a or not b: print('0.0')
else: print(f'{len(a & b) / len(a | b):.3f}')
" "$1" "$2"
}
```

### Confidence Decay

Not all memories age equally. The `decay` command applies type-specific confidence decay:

| Type | Half-life | Rationale |
|------|-----------|-----------|
| decision, preference, config, workflow, people | ∞ (permanent) | Core identity — never forget |
| bugfix | 60 days | Bugs stay relevant for a while |
| discovery | 42 days | Learnings persist |
| observation | 28 days | General notes fade |
| session, thread | 14 days | Ephemeral context |

### Progressive Disclosure

Memory retrieval uses three layers — a pattern borrowed from claude-mem:

1. **Compact index** (~50 tokens/result) — What `search` returns. Just ID, date, type, topic, and a summary preview.
2. **Timeline** — `timeline <id>` shows chronological context around an observation (±5 hours by default).
3. **Full details** — `detail <id>` returns everything: full summary, project, tags, metadata.

This keeps context injection cheap while still making deep recall available on demand.

## Registered Tools: The Agent Interface

The plugin registers three custom tools that the agent can use proactively:

```typescript
amp.registerTool({
  name: 'amp_mem_search',
  description: 'Search persistent cross-session memory.',
  inputSchema: {
    properties: {
      query: { type: 'string', description: 'FTS5 search query (AND, OR, NOT, prefix*)' },
      type: { type: 'string', description: 'Filter by type' },
      limit: { type: 'number', description: 'Max results (default 20)' },
    },
  },
  async execute(input) {
    return await ampMem(amp.$, ['search', input.query])
  },
})
```

This means the agent can *proactively* search its own memory. When I ask "what was that flag we set up for cash rounding?", the agent calls `amp_mem_search` and finds it — even if it was 3 weeks ago in a completely different session.

## The Knowledge Distillation Layer

Raw observations accumulate fast. After ~50, signal-to-noise drops. That's where **kb-distill** comes in — a separate Amp skill that compresses raw observations into structured knowledge notes and proposes behavioral rules for `AGENTS.md`.

It runs in 4 phases:

1. **Gather** — Dump all observations since last distillation
2. **Analyze & Cluster** — Group observations by theme, identify patterns
3. **Produce** — Generate distilled notes (high-signal summaries) and propose AGENTS.md rules for repeated behaviors
4. **Record** — Save the distillation run metadata

The distillation auto-triggers when pending observations exceed 50 or the last run was more than 7 days ago.

## Privacy: Everything Stays Local

This was non-negotiable. All data lives in `~/.amp/memory/amp-mem.db`. No external APIs. No network calls. No telemetry. The FTS5 search runs locally in SQLite. The AI assessment uses Amp's built-in `ctx.ai.ask()` which runs within Amp's own infrastructure — no additional API calls to external services.

Private observations (marked with `--private` or triggered by `<private>` tags in messages) are excluded from context injection and default searches entirely.

## The Web Viewer

For when you want to visually browse your memory, `amp-mem serve` starts a web viewer on `localhost:37777`. It has a stream view (chronological feed), search, stats dashboard, and progressive disclosure — click an observation to expand its full details.

## How to Build Something Similar

If you want to build your own memory system for Amp, here's the recipe:

### Step 1: Create the Storage Layer

Start with a SQLite database and FTS5. You need two core tables:

```sql
CREATE TABLE observations (
    id INTEGER PRIMARY KEY, ts TEXT, type TEXT,
    topic TEXT, summary TEXT, confidence REAL DEFAULT 1.0
);
CREATE VIRTUAL TABLE observations_fts USING fts5(
    topic, summary, content='observations', content_rowid='id'
);
```

Write a CLI that wraps `sqlite3` with commands for `save`, `search`, and `context`.

### Step 2: Create the Plugin

Create `~/.config/amp/plugins/your-plugin.ts`:

```typescript
// @i-know-the-amp-plugin-api-is-wip-and-very-experimental-right-now
import type { PluginAPI } from '@ampcode/plugin'

export default function (amp: PluginAPI) {
  // Inject context at the start of each turn
  amp.on('agent.start', async (event, ctx) => {
    const context = await ctx.$`your-cli context`
    return {
      message: { content: context.stdout, display: true }
    }
  })

  // Capture observations at the end of each turn
  amp.on('agent.end', async (event, ctx) => {
    const assessment = await ctx.ai.ask(
      `Does this turn contain something worth remembering?\n${event.message}`
    )
    if (assessment.result === 'yes' && assessment.probability > 0.65) {
      await ctx.$`your-cli save "${assessment.reason}"`
    }
  })

  // Register a search tool
  amp.registerTool({
    name: 'your_search',
    description: 'Search your memory',
    inputSchema: { type: 'object', properties: { query: { type: 'string' } } },
    async execute(input) {
      const result = await amp.$`your-cli search "${input.query}"`
      return result.stdout
    },
  })
}
```

The key Amp plugin APIs used:
- `amp.on('event', handler)` — Hook into lifecycle events
- `ctx.ai.ask(prompt)` — AI-gated assessment (returns `{ result, probability, reason }`)
- `ctx.$\`command\`` — Run shell commands
- `amp.registerTool()` — Register custom tools the agent can call
- Return `{ message: { content, display } }` from `agent.start` to inject context

### Step 3: Tune the Noise Filters

The biggest design challenge is signal-to-noise. You need to decide:

- **Which tools to ignore** — Read-only tools are noise. File edits should be batched.
- **What probability threshold to use** — 0.65 works for me, but experiment.
- **How to handle deduplication** — Jaccard similarity > 0.6 catches most duplicates.
- **When to compact** — I compact observations older than 30 days into weekly summaries.

### Step 4: Add Context Injection Intelligence

Don't dump everything. Use budgets per observation type, rank by confidence × access count, and apply time-based decay. The `context` command should produce ~150 lines max of high-signal context.

## What I Learned

1. **The plugin API is more powerful than it looks.** Four events (`session.start`, `agent.start`, `agent.end`, `tool.result`) plus `ctx.ai.ask()` and `registerTool()` are enough to build a sophisticated system.

2. **AI-gated capture is the key innovation.** Without it, you either capture everything (too noisy) or nothing (useless). The 0.65 threshold with type classification hits the sweet spot.

3. **SQLite + FTS5 is perfect for this.** Fast, local, zero dependencies, great full-text search with Porter stemming. The entire database stays under 1MB even with hundreds of observations.

4. **Progressive disclosure matters.** Context injection needs to be cheap (~50 tokens per observation). Full details should be available on demand but never injected by default.

5. **Confidence decay is essential.** Without it, old session noise drowns out current decisions. With it, permanent knowledge (decisions, preferences) naturally floats to the top while ephemeral context fades.

6. **Building tools with Amp is the best way to build tools with Amp.** The entire system was built iteratively in Amp sessions. Each session where I worked on amp-mem got captured by amp-mem, creating a beautiful feedback loop.

---

*This post was written with Amp — and yes, amp-mem captured the session where I wrote it.*

---

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
