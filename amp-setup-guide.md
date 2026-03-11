# How to Use Amp: Setup, Skills & Memory

A practical guide to turning [Amp](https://ampcode.com) from a code assistant into a full command center for your workflow — with skills, persistent memory, and an `AGENTS.md` that makes it *yours*.

**By [Abhi Basu](https://github.com/abhiroopb)**

---

## What is Amp?

[Amp](https://ampcode.com) is an AI coding agent that lives in your terminal (or VS Code). Out of the box it can read/write files, run shell commands, and search code. **Skills** are plug-in instruction sets that teach Amp how to use specific tools — Slack, Gmail, Google Calendar, Linear, Snowflake, and more — so it can perform complex, multi-step tasks on your behalf.

Think of skills as "recipes" that give Amp the know-how to operate tools you already use daily. With the right skills installed, Amp becomes a command center for your entire workflow — not just coding.

---

## Amp as Your Command Center

### Start of Day

Just type **"start my day"** and Amp will:

- **Slack** — Surface unread messages and thread replies, with options to reply inline
- **Gmail** — Triage your inbox, draft replies, flag items for follow-up
- **Google Calendar** — Show today's schedule, flag conflicts, let you accept/decline
- **Linear** — Show issues assigned to you, upcoming due dates
- **Notion** — Surface pages with new comments or mentions

All presented in your terminal with action options — no context switching.

### Throughout the Day

| Instead of...                            | Just tell Amp...                                              |
|------------------------------------------|---------------------------------------------------------------|
| Opening Slack, finding a channel         | "search Slack for checkout updates this week"                 |
| Switching to Linear, creating an issue   | "create a Linear issue for the login bug, assign to me"       |
| Opening Google Docs, formatting a PRD    | "write a PRD from these notes about onboarding improvements"  |
| Navigating to Snowflake, writing SQL     | "what's the conversion rate for last month?"                  |
| Opening Looker dashboards                | "run Looker dashboard 1234 and summarize the key metrics"     |

### Multi-Step Workflows

Amp shines when chaining tools together in a single prompt:

- *"Find the latest Slack discussion about tipping, summarize it, and create a Linear issue"*
- *"Check my calendar for conflicts tomorrow and decline the overlapping ones"*
- *"Search feedback about checkout speed, create a Google Doc with findings, and share it with the team"*

---

## How Skills Work

1. **You ask** — e.g., "search Slack for mentions of feature X this week"
2. **Amp loads the matching skill** — automatically with `auto-pilot`, or manually ("use the slack skill")
3. **The skill provides instructions** — tells Amp which CLI tools to call, auth flows, output format
4. **Amp executes** — runs commands, processes results, returns them to you

Skills are just markdown files (`SKILL.md`) stored in `~/.agents/skills/`. They don't contain secrets — your API tokens stay in separate credential files.

---

## Setup

### Prerequisites

| Tool | Install |
|------|---------|
| **Amp CLI** | Install and authenticate via [ampcode.com](https://ampcode.com) |
| **GitHub CLI** | `brew install gh` then `gh auth login` |
| **uv** (for gdrive, gcal skills) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

### Installing Skills

Skills live in GitHub repositories. Install them with:

```bash
amp skill add <repo>/<skill-name>
```

For example:

```bash
# Install a single skill
amp skill add my-org/agent-skills/slack

# Install with overwrite (for updates)
amp skill add my-org/agent-skills/slack --overwrite
```

#### Bulk Install Script

If you maintain a repo of skills, you can write a simple install script:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="your-org/your-skills-repo"
SKILLS=(
  slack gcal gdrive linear notion
  snowflake auto-pilot rpi rpi-research
  rpi-plan rpi-implement
)

echo "📦 Installing ${#SKILLS[@]} skills from $REPO..."
for skill in "${SKILLS[@]}"; do
  printf "  %-40s" "$skill"
  if amp skill add "$REPO/$skill" --overwrite 2>/dev/null; then
    echo "✓"
  else
    echo "✗"
  fi
done
echo "✅ Done! Run 'amp skill list' to verify."
```

### First-Time Authentication

After installing, some skills need one-time auth:

| Tool | Auth command |
|------|-------------|
| Google Drive / Calendar | `cd ~/.agents/skills/gdrive && uv run gdrive-cli.py auth login` |
| Slack | Automatic on first use (opens browser) |
| Snowflake | Uses Okta SSO |
| Linear | Enable the Linear MCP in Amp settings |
| GitHub | `gh auth login` |
| Notion | Enable the Notion MCP in Amp settings |

### Creating Your Own Skills

```bash
# Scaffold a new skill
amp skill create my-skill-name
```

Or just create a `SKILL.md` file in `~/.agents/skills/my-skill-name/`. Look at existing skills for examples of structure and conventions.

### Updating & Removing Skills

```bash
# Re-run install with --overwrite
amp skill add my-org/skills/slack --overwrite

# Remove a skill
amp skill remove slack
```

---

## Skills Catalog

### 🗣️ Communication & Productivity

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `start-of-day` | Morning triage: Slack → Gmail → Calendar | "start my day" |
| `slack` | Search, read, post messages | "search Slack for project updates" |
| `gcal` | Create, update, RSVP, check availability | "what meetings do I have tomorrow?" |
| `reviewing-calendar` | Visual weekly calendar with conflict detection | "review my calendar this week" |
| `gdrive` | Read/write Google Docs, Sheets, Slides | "create a Google Doc titled Q1 Plan" |
| `notion` | Read, search, create, update Notion pages | "search Notion for the roadmap" |
| `reflect` | Guided reflection for performance reviews | "start a reflection" |
| `writing-feedback` | Performance feedback drafting | "draft my self-reflection" |
| `controlling-computer` | macOS control via AppleScript | "turn on dark mode" |
| `viewing-figma-files` | Inspect Figma files, export images | "inspect this Figma frame" |

### 📋 Project & Issue Management

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `linear` | Create, search, update Linear issues | "create a Linear issue for the login bug" |
| `plan-to-linear` | Convert a plan into Linear issues in bulk | "convert this plan into Linear tickets" |
| `linear-to-execution` | Pick up a Linear issue for implementation | "work on PROJ-42" |
| `project-status` | Aggregate status from Slack, Drive, GitHub | "what's the project status?" |
| `historical-info` | Find what you've been working on | "what have I worked on this week?" |
| `logging-feature-requests` | Log feature requests from Slack | "log this as a feature request" |

### 💻 Code & Repository

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `gh-pr-read` | Read and summarize a GitHub PR | "summarize PR #4521" |
| `pr-manager` | Commit and create/update PRs | "commit and create a PR" |
| `push-pr` | Quick push + draft PR | "push pr" |
| `address-pr-comments` | Fix unresolved PR comments | "address PR comments" |
| `code-review-general` | Address code review feedback | "fix the review feedback" |
| `rebasing-git-branches` | Rebase onto upstream | "rebase my branch onto main" |
| `git-worktree` | Manage git worktrees | "create a worktree for the hotfix" |
| `walkthrough` | Explore and visualize codebase architecture | "walk me through the payment flow" |

### 📊 Data & Analytics

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `snowflake` | SQL queries on Snowflake | "query conversion rates" |
| `databricks` | SQL on Databricks Lakehouse | "search for the payments table" |
| `query-expert` | Natural-language to SQL | "how many orders last week?" |
| `looker` | Looker dashboards and explores | "run Looker dashboard 1234" |
| `data-analyst` | Full analysis with charts | "analyze checkout abandonment trends" |
| `airtable` | Manage Airtable bases and records | "search Airtable for Q1 features" |

### 🔧 Infrastructure & DevOps

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `datadog` | Logs, metrics, traces, monitors | "check Datadog for service errors" |
| `launchdarkly-cli` | Create, toggle, list feature flags | "list flags with 'checkout' in the name" |
| `flag-simulator` | Evaluate flag values for a context | "evaluate flag new-feature-v2" |
| `creating-experiments` | Set up A/B experiments | "create experiment for new onboarding" |
| `blockcell` | Deploy static sites | "deploy prototype to Blockcell" |
| `free-disk-space` | Clean up disk space on Mac | "free up disk space" |

### 🧪 Testing & Devices

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `ios-simulator` | Manage iOS simulators | "start an iPhone 15 simulator" |
| `android-emulator` | Manage Android emulators | "list available Android AVDs" |
| `agent-browser` | Browser automation for testing | "open the page and take a screenshot" |
| `testing-party-doc` | Generate QA testing docs | "create testing party doc for feature X" |

### 📝 Product & PM

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `writing-requirements-docs` | Write PRDs with auto-sourced evidence | "write a PRD from these notes" |
| `spec-creator` | Create product specs synced to Linear | "create spec for new feature" |
| `feedback-searcher` | Search user feedback across sources | "what are users saying about onboarding?" |
| `prototype-builder` | Build interactive HTML prototypes | "build prototype for the new flow" |
| `test-plan-creator` | Generate test plans from specs | "create test plan for the redesign" |
| `web-research` | Research competitors, trends, practices | "research competitor onboarding flows" |

### 🧠 Advanced Workflows

| Skill | What it does | Example prompt |
|-------|-------------|----------------|
| `auto-pilot` | Routes any request to the right skill(s) | *(always active)* |
| `rpi` | Research → Plan → Implement for complex tasks | "rpi: refactor the auth module" |
| `rpi-research` | Deep-dive research phase | "research how auth tokens work" |
| `rpi-plan` | Create phased implementation plan | "plan the API redesign" |
| `rpi-implement` | Execute approved plan phase by phase | "implement phase 1" |
| `rpi-iterate` | Update plan based on feedback | "update plan — add rate limiting" |
| `swarm` | Multi-perspective investigation | "investigate the latency spike" |
| `ralph-loop` | Iterative work-review across AI models | *(complex revision tasks)* |
| `memory` | Persistent cross-session memory | "search memory for auth decisions" |
| `kb-distill` | Distill observations into knowledge notes | "distill my recent work" |

---

## Tips for Getting the Most Out of Amp

### 1. Just Ask Naturally

If you have `auto-pilot` installed, you don't need to remember skill names:

- ❌ "Use the slack skill to search for messages about the release"
- ✅ "Search Slack for release updates this week"

### 2. Use RPI for Big Tasks

For complex, multi-step work (refactors, new features, migrations), use the **RPI** framework:

1. **Research** — understand the existing code and systems
2. **Plan** — create a phased plan with success criteria
3. **Implement** — execute one phase at a time

Each phase runs in its own session so context stays fresh.

### 3. Let Amp Remember

With `amp-mem`, Amp remembers context across sessions — workflows you've established, decisions made, people and team structures, and tool configurations. You teach it once, and it remembers forever.

### 4. Configure AGENTS.md

Your `~/AGENTS.md` file is the master configuration. It tells Amp your identity, preferences, and automated behaviors (like running start-of-day on session start). Treat it as your personal operating system for Amp. Just tell Amp to add to this file whenever you want a persistent behavior.

---

## Persistent Memory with amp-mem

### Overview

`amp-mem` gives Amp persistent memory across sessions. It uses **SQLite + FTS5** for storage and search. The key design insight: no vector embeddings needed — the LLM itself is the semantic engine, interpreting FTS5 results with synonym expansion and contextual reasoning.

### Architecture

```
~/.amp/memory/
├── amp-mem.db        # SQLite database (WAL mode)
├── schema.sql        # Database schema
└── knowledge.md      # Plain-text append-only log

~/bin/amp-mem          # CLI tool (21 subcommands)

~/.agents/skills/
├── memory/SKILL.md    # Teaches agents to use amp-mem
└── kb-distill/SKILL.md # Distills observations into knowledge
```

#### amp-mem Plugin

The **amp-mem plugin** (`~/.config/amp/plugins/amp-mem.ts`) wraps the CLI and provides passive memory capture:

- **Passive capture**: Automatically captures observations from Linear, Gmail, Slack, Notion, Google Drive, and Bash tool results
- **Noise filtering**: Ignores read-only tools (Read, Grep, finder, oracle, librarian), orchestration (Task, handoff, skill), and noisy ops (Gmail labels, Slack list)
- **AI gating**: Uses `ctx.ai.ask()` at agent.end to classify turn observations (p>0.65 threshold)
- **File edit batching**: Accumulates file edits per turn and saves as a single observation
- **Privacy tags**: Detects `<private>` in user messages and passes `--private` to all saves from that turn
- **Context injection**: Injects budgeted memory context at agent.start (60-line budget, private observations excluded, silent — hidden from user chat via `display: false`)
- **Duplicate prevention**: Injects context only once per session via a `contextInjected` flag reset on session start
- **Meta-noise filtering**: Excludes self-referential observations (amp-mem architecture, build decisions) from context injection to avoid crowding out real work
- **Smart truncation**: Summaries in context are truncated at sentence boundaries (up to 400 chars) instead of hard cuts
- **Registered tools**: `amp_mem_search`, `amp_mem_save` (with `private` option), `amp_mem_stats`

> **⚠️ Known issue (fixed March 2026):** The original plugin used Amp's experimental `$` tagged template to shell out to the CLI. This silently fails — registered tools return empty results while the CLI works fine. The fix: replace `$` with Node.js `child_process.execFile` (`import { execFile } from 'node:child_process'`) and replace `ctx.$` backup commands with `node:fs` operations. The web viewer is now fully self-contained in the CLI (no `web/` subdirectory needed). See the [complete setup guide](https://docs.google.com/document/d/1K1kASZubj8MiFL3B7qq3FxnUmS0oBCMrR8ioQQiJb38) for details.

### Setup

#### Step 1: Create directories

```bash
mkdir -p ~/.amp/memory
```

#### Step 2: Create the database schema

Save to `~/.amp/memory/schema.sql`:

```sql
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_url TEXT,
    started_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    ended_at TEXT, summary TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER REFERENCES sessions(id),
    ts TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    type TEXT NOT NULL DEFAULT 'observation',
    topic TEXT NOT NULL, summary TEXT NOT NULL,
    project TEXT, file_path TEXT, tags TEXT, metadata TEXT,
    confidence REAL NOT NULL DEFAULT 1.0,
    access_count INTEGER NOT NULL DEFAULT 0,
    last_accessed TEXT,
    private INTEGER NOT NULL DEFAULT 0
);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    topic, summary, project, tags,
    content='observations', content_rowid='id',
    tokenize='porter unicode61'
);
```

> **Note:** The full schema (with triggers, summaries table, distillations table, and indexes) is available in the `amp-mem.db` once initialized.

#### Step 3: Install the CLI

The `amp-mem` CLI is a shell script you place in your `PATH`:

```bash
# Ensure ~/bin is in PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# Place the amp-mem script at ~/bin/amp-mem
chmod +x ~/bin/amp-mem
```

#### Step 4: Initialize

```bash
amp-mem init
```

#### Step 5: Configure AGENTS.md

Add to your `~/AGENTS.md` Session Start section a reference to the amp-mem plugin handling init, backup, context injection, and distill-status checks automatically.

Add a Memory System section covering: passive capture (via the plugin), noise filtering, privacy tags (`<private>` markers), proactive recall, context injection, and implicit pattern learning.

#### Step 6: Verify

```bash
amp-mem init          # "Database initialized"
amp-mem stats         # 0 observations
amp-mem save observation "Test" "Testing memory"
amp-mem search "test" # Finds test observation
amp-mem serve         # Web viewer at localhost:37777
```

### CLI Reference

| Command | Description |
|---------|-------------|
| `init` | Create/migrate database |
| `save` | Save observation |
| `search` | FTS5 full-text search |
| `timeline` | Context around an observation |
| `detail` | Full observation details |
| `context` | Recent context for session priming |
| `compact` | Compress old entries into summaries |
| `session-start` | Begin a session |
| `session-end` | End current session |
| `stats` | Database statistics |
| `export` | Export all memory |
| `serve` | Web viewer at localhost:37777 |
| `distill-dump` | Dump observations for distillation |
| `distill-record` | Record distillation run |
| `distill-status` | Check pending count |
| `decay` | Apply confidence decay to aging observations |
| `ingest-thread` | Ingest an Amp thread (de-duplicated) |

### Observation Types

| Type | When to use |
|------|-------------|
| `observation` | General knowledge about codebase/tools |
| `decision` | Design decisions, trade-offs |
| `discovery` | Bugs found, root causes |
| `preference` | How you want things done |
| `bugfix` | Bug fixes with context |
| `config` | URLs, credential locations, env details |
| `workflow` | New workflows, command sequences |
| `people` | Team structure, ownership, contacts |
| `session` | End-of-session summary |

### How Distillation Works (kb-distill)

Every session, Amp checks `amp-mem distill-status`. If >50 pending observations or >7 days since last run, it auto-distills:

1. **Gather** — dump raw observations since last distillation
2. **Analyze** — cluster by topic, identify repeated patterns
3. **Produce** — save distilled notes, propose `AGENTS.md` rules
4. **Record** — mark distillation complete

Proposed rules are presented for approval — never auto-added to `AGENTS.md`.

### Backup & Restore

```bash
# Database backup
cp ~/.amp/memory/amp-mem.db ~/.amp/memory/amp-mem.db.bak

# Full backup
tar czf ~/amp-mem-backup.tar.gz ~/.amp/memory/ ~/bin/amp-mem

# Restore
tar xzf ~/amp-mem-backup.tar.gz -C /
amp-mem init
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| No vector embeddings | The LLM is the semantic engine — no embedding model needed |
| SQLite + FTS5 | Fast full-text search with porter stemming. Single file, WAL mode |
| Progressive disclosure | `search` → `timeline` → `detail` (3-layer retrieval) |
| On-demand web viewer | No persistent service — start when needed |
| `knowledge.md` alongside SQLite | Plain-text for human readability |
| Distillation | Compresses raw observations into structured knowledge |
| Idempotent init | Safe to run every session start |
| Privacy tags | `<private>` markers exclude observations from context injection and default search |
| Confidence decay | Time-based decay with type-specific half-lives; permanent types never decay |

---

## FAQ

**Q: Do skills have access to my passwords?**
No. Skills are just markdown files. Credentials are stored separately.

**Q: Can I create my own skills?**
Yes! Run `amp skill create my-skill-name` or look at existing skills in `~/.agents/skills/`.

**Q: How do I update skills?**
Re-run the install command with `--overwrite`.

**Q: How do I remove a skill?**
`amp skill remove <skill-name>`

---

## Browse the Skills

All skills referenced in this guide are available in the [`/skills`](./skills) directory of this repository. Each skill folder contains a `SKILL.md` with full instructions.
