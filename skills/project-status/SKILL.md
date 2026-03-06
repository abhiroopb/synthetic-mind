---
name: project-status
description: "Gather project state from Slack history, Google Drive docs, GitHub PRs, LaunchDarkly feature flags, and Airtable (Block Roadmap status updates). Use when asked to summarize project status, get a project overview, check what changed recently, generate a status update or progress report, recap recent activity, assess project health, or review rollout and feature flag state."
argument-hint: project name or keyword, optional repo (e.g. "CCBS" or "auto-mobile repo:user/repo")
allowed-tools:
  - Bash(cd ~/.agents/skills/slack/scripts && uv run:*)
  - Bash(cd ~/.agents/skills/gdrive && uv run:*)
  - Bash(gh pr list:*)
  - Bash(gh search prs:*)
  - Bash(gh issue list:*)
  - Bash(gh repo view:*)
  - Bash(ldcli:*)
  - Bash(jq:*)
  - Bash(curl *api.airtable.com:*)
---

# Project Status

Synthesize the current state of a project by pulling context from six sources: **Slack messages**, **Google Drive documents**, **GitHub pull requests**, **headcount cross-reference**, **LaunchDarkly feature flags**, and **Airtable (Block Roadmap)**. Produce a unified status report.

## Input

The user provides a **project name or keyword** (e.g., "CCBS", "auto-mobile", "card linking"). Optionally they may provide:
- A GitHub repo (`repo:owner/repo`)
- A Slack workspace (`workspace:square`)
- A LaunchDarkly project key (`ld-project:PROJECT_KEY`)
- A specific time window (`days:14`)

Parse these from `$ARGUMENTS`. Defaults: workspace `block`, days `14`, repo auto-detected from CWD if possible.

**Input sanitization:** Reject project keywords containing shell metacharacters (`;`, `|`, `&`, `` ` ``, `$`). Only alphanumeric characters, hyphens, underscores, spaces, and slashes are valid.

## Workflow

Run the six data-gathering steps **in parallel** (they are independent), then synthesize.

### Step 1 — Slack History

Use the `slack` skill's CLI to search for recent conversations.

```bash
cd ~/.agents/skills/slack/scripts && uv run slack-cli.py search-messages \
  --query "<PROJECT_KEYWORD>" \
  -w <WORKSPACE> \
  --sort timestamp --sort-dir desc
```

Also search for rollout/maintenance-specific terms:
```bash
cd ~/.agents/skills/slack/scripts && uv run slack-cli.py search-messages \
  --query "<PROJECT_KEYWORD> rollout OR beta OR incident OR maintenance OR deprecat OR migrate" \
  -w <WORKSPACE> \
  --sort timestamp --sort-dir desc
```

Extract from results:
- Key discussion topics and decisions
- Open questions or blockers mentioned
- People actively involved
- **Rollout/beta status** — any feature flags, staged rollouts, percentages, or beta cohorts mentioned
- **Incidents or regressions** — anything broken, reverted, or hotfixed
- **Maintenance concerns** — tech debt, deprecations, migration timelines, upgrade pressure

### Step 2 — Google Drive Docs

Use the `gdrive` skill's CLI to find recently modified documents.

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py search "<PROJECT_KEYWORD>" --limit 10
```

For the top 3-5 most relevant docs, read their content:
```bash
uv run gdrive-cli.py read <file-id>
```

Extract from results:
- Design docs, RFCs, or specs and their status
- Meeting notes or decision logs
- Any OKRs or project plans
- **Rollout plans** — launch timelines, feature flag configs, staged rollout docs
- **Maintenance/migration docs** — upgrade guides, deprecation notices, EOL timelines

### Step 3 — GitHub Pull Requests

Use `gh` CLI to find recent PRs. If a repo is provided, scope to it; otherwise search across the org.

```bash
# If repo is known:
gh pr list --repo <REPO> --search "<PROJECT_KEYWORD>" --state all --limit 20 \
  --json number,title,state,author,createdAt,updatedAt,url,labels,isDraft

# If no repo, search across org:
gh search prs "<PROJECT_KEYWORD>" --owner <ORG> --sort updated --limit 20 \
  --json repository,number,title,state,author,updatedAt,url
```

Also check for open issues (bugs, feature requests, maintenance):
```bash
gh issue list --repo <REPO> --state open --limit 15 \
  --json number,title,state,author,createdAt,updatedAt,url,labels
```

Extract from results:
- Open PRs (in-progress work)
- Recently merged PRs (completed work)
- Draft PRs (upcoming work)
- Any PRs with review requests pending
- **Dependency upgrade PRs** — Dependabot/Snyk/Renovate PRs piling up signal maintenance burden
- **Open issues** — bugs, feature requests, and especially anything labeled security, critical, or breaking

### Step 4 — Headcount Cross-Reference (go/people)

After gathering people from Steps 1-3, cross-reference against the company directory spreadsheet (go/people) to identify anyone who has left or is no longer active.

Read the directory and filter to only the names identified in Steps 1-3 to minimize data exposure:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py sheets read \
  13vPMH2tznuU2VYQ6e1wT1rIHXeEZW6yvVQgq_a5ahBo \
  --range "Directory!A1:G6732" 2>/dev/null | \
  python3 ~/.agents/skills/project-status/filter-directory.py <LAST_NAME_1> <LAST_NAME_2> ...
```

Replace `<LAST_NAME_1> <LAST_NAME_2> ...` with last names from the key contributors identified in Steps 1-3 (e.g., `parcel alaniz gannon`). Only matching rows are output — the full directory is not retained.

For each person:
- If they **appear** on the roster, note their org and function — they are confirmed active
- If they are **not found**, flag them as potentially departed
- Assess the **impact** of each departure: what workstreams they owned, what PRs/reviews are now orphaned, and any knowledge gaps created

Include findings in the **👥 Key People** and **⚠️ Blockers & Open Questions** sections of the report.

### Step 5 — LaunchDarkly Feature Flags

Use the `launchdarkly-cli` skill's `ldcli` CLI to find feature flags related to the project. If `ldcli` is not installed or authentication fails, **skip this step** and note in the report that LaunchDarkly data was unavailable. Do not block the rest of the report.

**Discover the project key** — LD project keys are often non-obvious (e.g., `pie` not `square-dashboard`). If `ld-project` was provided, use it. Otherwise, ask the user. If no project key can be determined, **skip this step**.

```bash
ldcli projects list -o json | jq '.[].key'
```

**Search for flags** matching the project keyword. Always use `--filter` — some projects have 25k+ flags. LD queries with spaces return unreliable results, so pick the most distinctive single token from the project name (e.g., `"checkout applet mobile"` → `checkout`). Hyphens and underscores are interchangeable in LD keys, so try both if needed:

```bash
ldcli flags list --project <LD_PROJECT_KEY> --filter "query:<DISTINCTIVE_TOKEN>" -o json
```

If the single-token search returns too many results, narrow with additional searches using other tokens.

For each matching flag, inspect its state:

```bash
ldcli flags get --project <LD_PROJECT_KEY> --flag <FLAG_KEY> -o json
```

Extract from results:
- **Active flags** — flags that are `on: true` with their current targeting rules and rollout percentages
- **Flags serving unexpected values** — flags that are "on" but serving `false` via fallthrough (a common misconfiguration)
- **Recently created flags** — signals upcoming launches or experiments
- **Stale flags** — flags that have been 100% rolled out for a long time but never cleaned up (tech debt)
- **Flags with complex targeting** — percentage rollouts, user segment targeting, or multi-variate flags indicating active experimentation

### Step 6 — Airtable (Block Roadmap & Status Updates)

Use the Airtable API to find the project in the Block Roadmap and pull its metadata and recent status updates. Credentials are stored in `~/.claude/skills/airtable/.env`.

```bash
source ~/.claude/skills/airtable/.env
```

**Search for the project** in the Block Roadmap base (`appjCJr8ew2HFgGiX`), Projects table (`tbloMuXIuMAye9UUZ`):

```bash
curl -s -G "https://api.airtable.com/v0/appjCJr8ew2HFgGiX/tbloMuXIuMAye9UUZ" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=FIND('<PROJECT_KEYWORD>',LOWER({Project Name}))" \
  -d "pageSize=10"
```

Also check the Square Product Development base (`appoAMUCsm6spyACv`), Projects table (`tbluWMCGq36V7hMkj`):

```bash
curl -s -G "https://api.airtable.com/v0/appoAMUCsm6spyACv/tbluWMCGq36V7hMkj" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=FIND('<PROJECT_KEYWORD>',LOWER({Project Name}))" \
  -d "pageSize=10"
```

**Fetch status updates** for matching projects. Status Updates are in a linked table — use the record IDs from the `Status Updates` field:

Block Roadmap Status Updates table: `tblF1O17YozszUXj0`
Square Product Development Status Updates table: `tblgBokQjqQd6QzAW`

```bash
curl -s -G "https://api.airtable.com/v0/appjCJr8ew2HFgGiX/tblF1O17YozszUXj0/<RECORD_ID>" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

Extract from results:
- **Project metadata** — status, priority (P0–P4), roadmap quarter, 3D phase, DRI(s), requesting org
- **Recent status updates** — what was reported, when, any risks or blockers called out
- **Staffing** — whether the project is marked as staffed
- **Timeline** — expected completion date, development start date

If Airtable auth fails or no `.env` file exists, **skip this step** and note in the report that Airtable data was unavailable.

## Synthesis

Combine findings into a structured report:

```
## 📊 Project Status: <PROJECT_NAME>
*As of <DATE> — covering the last <N> days*

### 🔄 Active Work (PRs)
- List open/draft PRs with authors and status

### ✅ Recently Completed
- List recently merged PRs

### 📋 Roadmap Status (Airtable)
- Project priority, 3D phase, roadmap quarter, staffing status
- DRI(s) and requesting organization
- Recent status updates with dates and any risks/blockers flagged
- Expected completion date vs. current progress

### 🚀 Rollouts & Betas
- Feature flags from LaunchDarkly with their current state (on/off, rollout %, targeting rules)
- Flags that are "on" but serving false — potential misconfigurations to investigate
- Staged rollouts, beta cohorts, and their current percentages
- Upcoming launches with timelines
- Any rollbacks or paused rollouts

### 💬 Key Discussions (Slack)
- Summarize key threads, decisions, and open questions

### 📄 Key Documents
- List relevant docs with links and brief descriptions

### 👥 Key People
- List people most active across all five sources
- Flag anyone not found on the go/people roster and assess impact on workstreams

### 🔧 Maintenance & Tech Debt
- Stale dependency upgrade PRs (Dependabot/Snyk/Renovate backlog)
- Stale feature flags — flags at 100% rollout that should be cleaned up
- Open deprecation warnings or migration deadlines
- Known tech debt items discussed in Slack or docs
- Security advisories or CVEs requiring attention

### ⚠️ Blockers & Open Questions
- Anything flagged as blocked, waiting, or unresolved

### 📋 Summary
- 2-3 sentence high-level summary of project state
- Call out the biggest rollout risk and the most urgent maintenance item
```

## Data Sensitivity

- **Never include** credentials, API keys, tokens, or secrets found in Slack messages or Drive docs in the status report.
- **Employee roster data** is PII — only include names and org assignments relevant to the project. Do not reproduce the full directory output.
- **Slack messages** and **Drive documents** may contain confidential business information. Summarize findings rather than quoting sensitive content verbatim.

## Tips

- If Slack auth fails, run the auth flow and retry.
- If Google Drive auth fails, run `uv run gdrive-cli.py auth login` and retry.
- If no GitHub repo is specified, try `gh repo view --json nameWithOwner -q .nameWithOwner` from CWD.
- Prioritize recent activity — weight the last 7 days more heavily.
- When searching Slack, try alternate keywords if the first search yields few results (e.g., acronyms, full names, channel names).
- If `ldcli` auth fails, run `ldcli login` (opens browser for OAuth) and retry.
- LD flag keys in code (e.g., `service/flag-name`) may differ from LD keys (e.g., `service-flag-name`). Use `ldcli flags list --filter` to resolve canonical keys.
- A flag with `on: true` may still serve `false` if the fallthrough points to the false variation — always inspect the `fallthrough` field.
