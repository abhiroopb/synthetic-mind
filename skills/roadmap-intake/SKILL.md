---
name: roadmap-intake
description: "Create roadmap projects from Slack threads or links. Reads the link, digests requirements and discussion, then creates a structured record in your roadmap tool with all fields populated. Use when asked to add a feature request to the roadmap, create a roadmap project, or file a product request."
---

# Roadmap Intake

Creates new roadmap projects from Slack threads, links, or other sources. Reads the source material, digests requirements and discussion, generates structured fields, and creates the record in your roadmap tool (Airtable, Linear, Jira, etc.).

## Workflow

### Step 1 — Read and Digest the Source

When the user provides a link (Slack thread, Google Doc, Notion page, etc.):

1. **Read the content** using the appropriate tool (Slack skill for Slack links, Google Drive for docs, web reader for URLs, etc.)
2. **Parse the full discussion** — not just the first message, but all replies, reactions, and context
3. **Extract key information:**
   - What is being requested (the feature/project)
   - Why it's needed (business justification, customer pain, opportunity)
   - Who is asking and who is involved
   - Any timeline mentions or urgency signals
   - Technical details, scope, or constraints discussed
   - Any decisions made in the thread

### Step 2 — Generate Roadmap Fields

Based on the digested content, generate the following fields. **Always preview these to the user before creating.**

| Field | How to determine |
|---|---|
| **Project Name** | Generate a clear, concise title (e.g., "Support Gift Cards on Profiles") |
| **Project Description** | Write a structured description with **What** (outcome/deliverable) and **Why** (business rationale) sections |
| **Work Type** | Default: `Strategic Priority`. Options: `Strategic Priority`, `Refinement`, `Functional Priority` |
| **Strategic Priority** | Select the most relevant strategic priority from your organization's priorities list |
| **Sub-Priority** | Pick the most relevant sub-priority area |
| **Program** | Select the relevant program(s) the project falls under |
| **DRI(s)** | Default: current user. Set the directly responsible individual |
| **Project Status** | Default: `Backlog`. Options: `Not Started`, `In Progress`, `Blocked`, `At Risk`, `Delivered`, `Backlog`, `Cancelled` |
| **Prioritization** | Make a determination: `P0` (critical), `P1` (important), `P2` (nice to have) |
| **Phase** | Default: `Declare`. Options: `Declare`, `Discover`, `Develop` |
| **Relevant Documentation** | Add the source link (Slack permalink, doc URL, etc.) |
| **Requesting Organization** | Select the appropriate requesting team/org |
| **Roadmap Quarter** | Estimate based on discussion context |
| **Staffed** | Default: `Not Staffed`. Options: `Yes`, `Not Staffed`, `Partial` |
| **Locale** | Default: empty. Add if locale-specific (e.g., `US`, `AU`, `UK`) |

### Step 3 — Preview and Confirm

Present a formatted summary to the user:

```
📋 **New Roadmap Project**

**Title:** [Project Name]
**Description:**
> **What:** [outcome]
> **Why:** [rationale]

**Work Type:** Strategic Priority
**Priority:** [selected priority]
**Sub-Priority:** [chosen sub-priority]
**Program:** [program name(s)]
**DRI:** [user name]
**Status:** Backlog
**Prioritization:** [P0/P1/P2]
**Phase:** Declare
**Requesting Org:** [team name]
**Links:** [source link]

Create this project? (y/n)
```

### Step 4 — Create the Record

Once confirmed, create the record in your roadmap tool via its API:

```bash
# Example using Airtable API
source ~/.config/roadmap-tool/.env

curl -s -X POST "https://api.airtable.com/v0/YOUR_BASE_ID/YOUR_TABLE_ID" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Project Name": "<TITLE>",
      "Project Description": "<DESCRIPTION>",
      "Work Type": "<WORK_TYPE>",
      "Strategic Priority": ["<PRIORITY_RECORD_ID>"],
      "Sub-Priority": ["<SUB_PRIORITY_RECORD_ID>"],
      "Program Name": ["<PROGRAM_RECORD_ID>"],
      "DRI(s)": "<DRI_NAME>",
      "Project Status": "<STATUS>",
      "Prioritization": "<P0|P1|P2>",
      "Phase": "<PHASE>",
      "Relevant Documentation": "<SOURCE_LINK>",
      "Requesting Organization": ["<ORG_RECORD_ID>"],
      "Staffed": "<STAFFED>",
      "Roadmap Quarter": ["<QUARTER>"]
    }
  }'
```

### Step 5 — Report Back

After creation, extract the record ID from the response and provide:
- ✅ Confirmation message
- 🔗 Link to the project in your roadmap tool

## Reference Data

### Configuring Your Roadmap Tool

Set up your tool-specific IDs in `~/.config/roadmap-tool/.env`:

```bash
# API credentials
API_TOKEN=your_token_here

# Airtable IDs (example)
BASE_ID=your_base_id
PROJECTS_TABLE=your_projects_table_id
PROGRAMS_TABLE=your_programs_table_id
PRIORITIES_TABLE=your_priorities_table_id
ORGS_TABLE=your_orgs_table_id
PEOPLE_TABLE=your_people_table_id
```

### Field Value Options

**Work Type:** `Strategic Priority` | `Refinement` | `Functional Priority`
**Project Status:** `Not Started` | `In Progress` | `Blocked` | `At Risk` | `Delivered` | `Backlog` | `Cancelled`
**Prioritization:** `P0` | `P1` | `P2`
**Phase:** `Declare` | `Discover` | `Develop`
**Staffed:** `Yes` | `Not Staffed` | `Partial`

## Notes

- Always read the full Slack thread (not just the first message) — context and decisions live in the replies
- For Slack links, extract the channel ID and message timestamp to fetch the thread
- Rich text fields accept plain text via most APIs
- The `Relevant Documentation` field is a good place to put the source Slack link and any related docs
- If the user provides multiple links, combine all context before generating fields
- When unsure about sub-priority, pick the most relevant or ask the user
