# amp-mem Installation

amp-mem is a persistent cross-session memory system for [Amp](https://ampcode.com). It uses SQLite + FTS5 to store observations, decisions, and discoveries — then recalls them in future sessions.

## Prerequisites

- **Amp CLI** installed and working (`amp --version`)
- **sqlite3** available on PATH (included on macOS, install via `brew install sqlite` or `apt install sqlite3` on Linux)
- **bash** 4.0+ (macOS ships with 3.x — install via `brew install bash` if needed)

## Install

### 1. Clone the repo

```bash
git clone git@github.com:abhiroopb/synthetic-mind.git ~/Development/synthetic-mind
```

### 2. Copy the CLI and plugin

```bash
# Copy the amp-mem CLI to your PATH
cp ~/Development/synthetic-mind/bin/amp-mem ~/bin/amp-mem
chmod +x ~/bin/amp-mem

# Copy the plugin to Amp's plugin directory
mkdir -p ~/.config/amp/plugins
cp ~/Development/synthetic-mind/bin/amp-mem-plugin.ts ~/.config/amp/plugins/amp-mem.ts
```

### 3. Create the database directory and schema

```bash
mkdir -p ~/.amp/memory

# Copy the schema file
cat > ~/.amp/memory/schema.sql << 'SCHEMA'
-- Amp Memory Schema — Persistent cross-session memory

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_url  TEXT,
    started_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    ended_at    TEXT,
    summary     TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    INTEGER REFERENCES sessions(id),
    ts            TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    type          TEXT NOT NULL DEFAULT 'observation',
    topic         TEXT NOT NULL,
    summary       TEXT NOT NULL,
    project       TEXT,
    file_path     TEXT,
    tags          TEXT,
    metadata      TEXT,
    confidence    REAL NOT NULL DEFAULT 1.0,
    access_count  INTEGER NOT NULL DEFAULT 0,
    last_accessed TEXT,
    private       INTEGER NOT NULL DEFAULT 0
);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    topic, summary, project, tags,
    content='observations', content_rowid='id',
    tokenize='porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS observations_ai AFTER INSERT ON observations BEGIN
    INSERT INTO observations_fts(rowid, topic, summary, project, tags)
    VALUES (new.id, new.topic, new.summary, new.project, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS observations_ad AFTER DELETE ON observations BEGIN
    INSERT INTO observations_fts(observations_fts, rowid, topic, summary, project, tags)
    VALUES ('delete', old.id, old.topic, old.summary, old.project, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS observations_au AFTER UPDATE ON observations BEGIN
    INSERT INTO observations_fts(observations_fts, rowid, topic, summary, project, tags)
    VALUES ('delete', old.id, old.topic, old.summary, old.project, old.tags);
    INSERT INTO observations_fts(rowid, topic, summary, project, tags)
    VALUES (new.id, new.topic, new.summary, new.project, new.tags);
END;

CREATE TABLE IF NOT EXISTS summaries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    period_start    TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    summary         TEXT NOT NULL,
    observation_ids TEXT
);

CREATE TABLE IF NOT EXISTS distillations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    observation_count INTEGER NOT NULL,
    notes_produced  INTEGER NOT NULL DEFAULT 0,
    rules_proposed  INTEGER NOT NULL DEFAULT 0,
    summary         TEXT
);

CREATE INDEX IF NOT EXISTS idx_obs_ts ON observations(ts);
CREATE INDEX IF NOT EXISTS idx_obs_type ON observations(type);
CREATE INDEX IF NOT EXISTS idx_obs_project ON observations(project);
CREATE INDEX IF NOT EXISTS idx_obs_session ON observations(session_id);
SCHEMA

# Initialize the database
amp-mem init
```

### 4. Verify

```bash
amp-mem stats
```

You should see:

```
Observations:  0
Sessions:      0
DB size:       12 KB
```

## How it works

Once installed, the plugin activates automatically in every Amp session:

- **Passive capture:** Watches tool results and agent turns. When something is worth remembering (confidence > 0.65), it saves an observation.
- **Context injection:** At session start, recent relevant observations are injected into the agent's context.
- **Search:** Use `amp-mem search "query"` to recall past decisions, discoveries, and workflows.
- **Compact:** Use `amp-mem compact` to distill old observations into knowledge notes.
- **Stats:** Use `amp-mem stats` to check your memory footprint.

## Files

| File | Purpose |
|------|---------|
| `bin/amp-mem` | CLI tool (bash) — search, save, compact, stats |
| `bin/amp-mem-plugin.ts` | Amp plugin — passive capture + context injection |
| `~/.amp/memory/amp-mem.db` | SQLite database (created on first run) |
| `~/.amp/memory/schema.sql` | Database schema |
| `~/.config/amp/plugins/amp-mem.ts` | Plugin (symlinked or copied) |
