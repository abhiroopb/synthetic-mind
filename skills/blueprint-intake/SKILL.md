---
name: blueprint-intake
description: "Create Blueprint (Roadmap) projects from Slack threads or links. Reads the link, digests requirements and discussion, then creates an Airtable record with all fields populated. Use when asked to add a feature request to Blueprint, create a Blueprint project, or file a feature request."
allowed-tools:
  - Bash(curl *api.airtable.com:*)
  - Bash(source:*)
  - Bash(cat:*)
  - Bash(jq:*)
---

# Blueprint Intake

Creates new Blueprint (Roadmap) projects from Slack threads, links, or other sources. Reads the source material, digests requirements and discussion, generates structured fields, and creates the Airtable record.

## Workflow

### Step 1 — Read and Digest the Source

When the user provides a link (Slack thread, Google Doc, Notion page, etc.):

1. **Read the content** using the appropriate tool (slack skill for Slack links, gdrive for Google Docs, read_web_page for URLs, etc.)
2. **Parse the full discussion** — not just the first message, but all replies, reactions, and context
3. **Extract key information:**
   - What is being requested (the feature/project)
   - Why it's needed (business justification, customer pain, opportunity)
   - Who is asking and who is involved
   - Any timeline mentions or urgency signals
   - Technical details, scope, or constraints discussed
   - Any decisions made in the thread

### Step 2 — Generate Blueprint Fields

Based on the digested content, generate the following fields. **Always preview these to the user before creating.**

| Field | How to determine |
|---|---|
| **Project Name** | Generate a clear, concise title (e.g., "Support Gift Cards on Profiles") |
| **Project Description** | Write a structured description with **What** (outcome/deliverable) and **Why** (business rationale) sections |
| **Work Type** | Default: `Strategic Priority`. Options: `Strategic Priority`, `Refine`, `Functional Priority` |
| **Strategic Priority** | Default: `sellers <> individuals (connected)` → record ID `recrOQGcOpWMrwmjh` |
| **Sub-Priority** | Pick the most relevant. Common choices for Profiles/ECOM work: |
| | - `F&B excellence` → `recaCYoF5AE4o2FYT` (good fallback) |
| | - `6b. Online Ordering Profiles/ Profiles` → `recbcW3qY14je5tWH` |
| | - `$Profile platform/websites/payment links` → `recYdQBLV3wWWkm83` |
| | - `checkout` → `recT3nZgOXD9zQ2Vl` |
| | - `Neighborhood connection` → `rec0tkYLpeZZCsgl2` |
| **Program** | Default: both `$Profiles` (`recZiVY9n0UC5TwcK`) AND `Code Red - Orion` (`recYsM5JQDtzSoMZx`) |
| **DRI(s)** | Default: `Abhi Basu` |
| **Project Status** | Default: `Backlog`. Options: `Not Started`, `In Progress`, `Blocked`, `At Risk`, `Delivered`, `Backlog`, `Cancelled` |
| **Prioritization** | Make a determination: `P0` (critical), `P1` (important), `P2` (nice to have) |
| **3D Phase** | Default: `Declare`. Options: `Declare`, `Discover`, `Develop` |
| **Relevant Documentation** | Add the source link (Slack permalink, doc URL, etc.) |
| **Requesting Organization** | For Profiles work: `reccYcyHVsqMnuhT9` (ECOM > Profiles). For Online: `rect1P4yv4p9ODj9C` (ECOM > Online) |
| **Roadmap Quarter** | Estimate based on discussion. Current quarter options: `2026 - Q1` through `2027 - Q4` |
| **Axes** | Pick if obvious: `X - Autonomy`, `Y - Neighborhoods`, `Z - Sovereignty`, `Constants` |
| **Staffed** | Default: `Not Staffed` unless discussed. Options: `Yes`, `Not Staffed`, `Partial` |
| **Locale** | Default: empty. Add if locale-specific (e.g., `US`, `AU`, `UK`) |

### Step 3 — Preview and Confirm

Present a formatted summary to the user:

```
📋 **New Blueprint Project**

**Title:** [Project Name]
**Description:**
> **What:** [outcome]
> **Why:** [rationale]

**Work Type:** Strategic Priority
**Priority:** sellers <> individuals (connected)
**Sub-Priority:** [chosen sub-priority]
**Program:** $Profiles, Code Red - Orion
**DRI:** Abhi Basu
**Status:** Backlog
**Prioritization:** [P0/P1/P2]
**Phase:** Declare
**Requesting Org:** ECOM > Profiles
**Links:** [source link]

Create this project? (y/n)
```

### Step 4 — Create the Airtable Record

Once confirmed, create the record:

```bash
source ~/.agents/skills-archive/airtable/.env

curl -s -X POST "https://api.airtable.com/v0/appjCJr8ew2HFgGiX/tbloMuXIuMAye9UUZ" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Project Name": "<TITLE>",
      "Project Description": "<DESCRIPTION>",
      "Work Type": "<WORK_TYPE>",
      "Strategic Priority": ["<PRIORITY_RECORD_ID>"],
      "Sub-Priority": ["<SUB_PRIORITY_RECORD_ID>"],
      "Program Name": ["<PROGRAM_RECORD_ID_1>", "<PROGRAM_RECORD_ID_2>"],
      "DRI(s)": "<DRI_NAME>",
      "Project Status": "<STATUS>",
      "Prioritization": "<P0|P1|P2>",
      "3D Phase": "<PHASE>",
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
- 🔗 Blueprint URL: `https://roadmap.example.com/blueprint/project/<RECORD_ID>`

## Reference Data

### Airtable IDs

**Use the Product Development base for writes** (Roadmap base is read-only).

- **Base:** `appoAMUCsm6spyACv` (Product Development) — **use this for creating records**
- **Projects Table:** `tbluWMCGq36V7hMkj`
- **Programs Table:** `tblcUoDYxGGJ4W60O`
- **Strategic Priorities Table:** `tblLhsdGqUCXYD5u2`
- **Sub-Priority Table:** `tblofwQwgry8x4AXJ`
- **Organizations Table:** `tblIxNVl9fck6mQCK`
- **People Database:** `tblAU6u0649HmVHSc`
- **Credentials:** `~/.agents/skills-archive/airtable/.env` (source this for `$AIRTABLE_TOKEN`)

> **Note:** Roadmap base (`appjCJr8ew2HFgGiX`) is read-only. Always create in Product Development.

### Frequently Used Record IDs

**Programs (Product Development base):**
- `$Profiles` → `recVwwOuxpNOLWqmt`
- `Code Red - Orion` → `rec2tgtqXvY2SPrAe`

**Strategic Priorities (Product Development base):**
- `sellers <> individuals (connected)` → `rec04gevLVj1JZInZ`
- `7. win more Sellers: SQ Cash App and Afterpay` → `reckyoV43vkCf6pg1`

**Sub-Priorities (Product Development base):**
- `6b. Online Ordering Profiles/ Profiles` → `recgnomccwz9BqlUL`

**Organizations (Product Development base):**
- `ECOM > Profiles` → `rectiPsHwkKXMVKSR`

**People:**
- `Abhi Basu` → `recewpVxckDZLegz7`

### Field Differences from Roadmap Base

- `Strategic Priority - Primary` (not `Strategic Priority`)
- `DRI(s)` is a **linked record** (use People Database record IDs, not free text)
- Additional useful fields: `Roadmap` (singleSelect, e.g., "ECOM"), `Product Area` (multipleSelects), `Audience` (multipleSelects), `Locale` (multipleSelects)

### Field Value Options

**Work Type:** `Strategic Priority` | `Refine` | `Functional Priority`
**Project Status:** `Not Started` | `In Progress` | `Blocked` | `At Risk` | `Delivered` | `Backlog` | `Cancelled`
**Prioritization:** `P0` | `P1` | `P2`
**3D Phase:** `Declare` | `Discover` | `Develop`
**Staffed:** `Yes` | `Not Staffed` | `Partial`
**Axes:** `X - Autonomy` | `Y - Neighborhoods` | `Z - Sovereignty` | `Constants`
**Roadmap Quarter:** `2026 - Q1` | `2026 - Q2` | `2026 - Q3` | `2026 - Q4` | `2027 - Q1` | `2027 - Q2` | `2027 - Q3` | `2027 - Q4`

## Notes

- Always read the full Slack thread (use `slack` skill with `read-thread` or `get-thread`) — not just the first message
- For Slack links, extract the channel ID and message timestamp to fetch the thread
- Rich text fields (`Project Description`, `Relevant Documentation`) accept plain text via the API
- The `Relevant Documentation` field is a good place to put the source Slack link and any related docs
- If the user provides multiple links, combine all context before generating fields
- When unsure about Sub-Priority, default to `F&B excellence` (`recaCYoF5AE4o2FYT`)
