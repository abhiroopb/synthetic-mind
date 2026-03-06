---
name: writing-requirements-docs
description: Write crisp, thorough PRDs from rough notes, customer feedback, or raw input using the repo's canonical PRD template. Automatically searches Slack, Airtable, Snowflake, and Glean for internal references to augment the PRD with traced-back evidence.
---

# Writing Requirements Documents

Translate raw input — rough notes, customer feedback, bullet lists, designs, verbal transcripts, Slack threads — into structured, actionable PRDs that conform to this repo's §7.1 PRD template. Before drafting, **automatically search internal Square sources** (Slack, Airtable, Snowflake, Glean) for references related to the feature, and use relevant findings to augment the PRD with linked evidence.

## Differentiation from spec-creator

This skill enforces the **canonical PRD template** defined in AGENTS.md §7.1. It is designed for PMs who start with messy, unstructured input and need a complete, validation-ready PRD. Unlike `spec-creator`, this skill does not use Linear and follows the repo's strict template exactly. It also **automatically searches internal sources** and weaves evidence into the PRD with traceable links.

## Prerequisites

Install the required CLI skills if not already installed:

```bash
sq agents skills add snowflake
sq agents skills add slack
sq agents skills add glean
sq agents skills add airtable
```

**IMPORTANT: You must be connected to Cloudflare WARP VPN.**

Enable your "Snowflake", "Slack", "Glean", and "Airtable" MCPs before proceeding.

## Role

You are an expert Product Manager translating business goals and user needs into clear, testable specifications. You accept any form of raw input, search internal sources for supporting evidence, and produce a PRD that passes the repo's validation checks (§5).

## Accepted Input Types

- Rough notes or bullet points
- Customer feedback (buyer or seller)
- Verbal transcripts or recorded notes
- Design mockups or wireframes
- Slack messages or meeting notes
- Existing docs that need restructuring
- Research findings or data exports
- Competitive analysis

## Internal Source Reference Lookup

### Data Sources

Before generating the PRD, search these internal sources for references related to the feature:

| Source | MCP | What to Look For |
|--------|-----|------------------|
| Slack channels | Slack | Feature discussions, feedback, escalations, decisions |
| Airtable bases | Airtable | Roadmaps, feature trackers, prioritization records, research logs |
| CS Phone Transcripts | Snowflake | Seller complaints or requests related to the feature |
| CS Chat Transcripts | Snowflake | Seller complaints or requests related to the feature |
| AM Gong Calls | Snowflake | Account Manager conversations about the feature |
| Seller Feedback | Snowflake | Direct seller feedback mentioning the feature |
| unitQ Quality Signals | Snowflake | Aggregated quality signals and writeback data |
| AM Product Requests | Snowflake | Account Manager product requests intake and tracking |
| Internal Docs | Glean | PRDs, research, design docs, decision records, strategy docs |

### Slack Channels to Search

Search these channels plus any scope-specific channels the user identifies:

| Channel | Purpose |
|---------|---------|
| `#strategic-seller-churn-threats` | High-value seller churn signals and escalations |
| `#retention-hotline` | Urgent retention cases and seller issues |
| `#sq-seller-feedback-intake` | General seller feedback intake and triage |
| `#shipped` | Shipped features and launches |
| `#square-product-announce` | Product announcements and updates |
| `#seller-feedback` | Seller feedback discussions |
| `#unitq-square-all-alerts` | unitQ quality alerts across Square products |

### Snowflake Tables

| Table | Description |
|-------|-------------|
| `APP_SUPPORT.APP_SUPPORT.PHONE_TRANSCRIPTS_FORMATTED` | CS phone transcripts |
| `APP_SUPPORT.APP_SUPPORT.MESSAGING_TRANSCRIPTS_FORMATTED` | CS chat transcripts |
| `APP_SALES.GONG.GONG_DETAILED_CALLS` | AM/Sales call transcripts with AI summaries |
| `SELLER_FEEDBACK.RAW_OLTP.SELLER_FEEDBACK` | Direct seller feedback |
| `APP_CASH_VOC.PUBLIC.SQUARE_UNITQ_WRITEBACK_AGGREGATED` | unitQ aggregated quality signals and writeback data |
| `FIVETRAN.AM_ANALYTICS.PRODUCT_REQUESTS_INTAKE` | AM product requests intake and tracking |

### Relevance Threshold

**Only include a reference if it is at least 80% related to the feature being described.** Err on the side of excluding borderline references. A reference is relevant when it:

- Directly names or describes the feature or a closely related capability
- Contains seller/buyer feedback about the specific problem the feature solves
- Documents a decision, constraint, or trade-off that directly affects this feature
- Provides data (metrics, volumes, error rates) that quantifies the problem this feature addresses

A reference is **not relevant** when it:

- Mentions the feature in passing within a broader unrelated discussion
- Discusses a different feature in the same product area
- Is outdated and superseded by newer decisions
- Only tangentially relates through shared terminology

### Reference Format

Every included reference MUST have a traceable link so the user can verify the source. Use this format in the PRD:

```markdown
> "[Relevant quote or summary]"
> — [Source type]: [Link or identifier]
```

Link formats by source:
- **Slack**: `https://block.slack.com/archives/<channel_id>/p<message_ts>` (use the permalink from search results)
- **Airtable**: `https://airtable.com/<base_id>/<table_id>/<record_id>` (use the record URL)
- **Snowflake**: `Case ID: <case_id>` or `Gong Call: <metadata_title> (<metadata_started>)` (include the query used)
- **Glean**: Document title with link returned by Glean search

## Step Completion Tracker (MANDATORY)

**Every AI agent running this skill MUST use this tracker.** After completing each workflow step, you MUST print a step completion report to the user before proceeding to the next step. Do NOT skip any step. Do NOT proceed to the next step until you have printed the report for the current step.

Use this exact format after each step:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ STEP [N] COMPLETE: [Step Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What I did:
  - [Bullet list of every action taken]

What I found:
  - [Bullet list of key findings/outputs]

What I'm carrying forward:
  - [Key context for next steps]

Next: Step [N+1] — [Next Step Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If a step produces no results (e.g., a Snowflake query returns 0 rows), you MUST still report it:
```
  - Snowflake / CS Phone Transcripts: ⚠️ 0 results (query executed, no matches for keywords)
```

**At the end of the entire workflow**, print a final summary checklist:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 WORKFLOW COMPLETION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1 — Analyze Input:         ✅ Done
Step 2 — Search Internal Sources:
  - Slack:                      ✅ X messages found / ⚠️ 0 results
  - Airtable:                   ✅ X records found / ⚠️ 0 results
  - Snowflake (Phone):          ✅ X transcripts / ⚠️ 0 results
  - Snowflake (Chat):           ✅ X transcripts / ⚠️ 0 results
  - Snowflake (Gong):           ✅ X calls / ⚠️ 0 results
  - Snowflake (Seller FB):      ✅ X entries / ⚠️ 0 results
  - Snowflake (unitQ):          ✅ X entries / ⚠️ 0 results
  - Snowflake (AM Requests):    ✅ X entries / ⚠️ 0 results
  - Glean:                      ✅ X docs found / ⚠️ 0 results
Step 3 — Clarifying Questions:  ✅ Asked & answered
Step 4 — Generate PRD:          ✅ All 13 sections written
Step 5 — Save PRD:              ✅ Saved to <path>
Step 5b — Event Logging:        ✅ Saved to <path>
Step 6 — Validation:            ✅ All checks passed / ⚠️ N issues noted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If any step was skipped or failed, mark it with ❌ and explain why.** Never silently skip a step.

## Workflow

### 1. Analyze Input

Read everything the user provides. Identify:
- Core product concept
- Target users (buyer, seller, internal)
- Business objectives and motivation
- Existing constraints or dependencies
- **Search keywords**: Extract 3–5 keywords and synonyms to use for internal source searches

**→ Print Step 1 completion report before proceeding.**

### 2. Search Internal Sources

**Before asking clarifying questions**, search all internal sources in parallel using the keywords and synonyms extracted in Step 1. This ensures you understand the existing context, prior decisions, known pain points, and seller feedback before engaging the user — so your clarifying questions are sharper and informed by real evidence.

Use the Task tool to run parallel searches across all sources simultaneously.

**You MUST search ALL of the following sources. Do not skip any. Report results for each one individually, even if 0 results.**

#### 3a. Execute Parallel Searches

Launch parallel searches across all sources. For each source, use the appropriate MCP:

**Slack** (Slack MCP `search_messages`):
- Search each channel listed above for the feature keywords
- Use `newer_than: "P180D"` (last 6 months) unless the user specifies a different period
- Collect message permalinks for any relevant hits

**Airtable** (Airtable MCP):
- Search for bases and tables related to the feature's scope area
- Look for roadmap entries, feature requests, prioritization records, and research logs
- Collect record URLs for any relevant hits

**Snowflake** (Snowflake MCP):
- Query CS transcripts for seller mentions of the feature (last 180 days):
  ```sql
  SELECT CASE_ID, START_TIME_UTC, LEFT(TRANSCRIPT, 3000) AS TRANSCRIPT_PREVIEW
  FROM APP_SUPPORT.APP_SUPPORT.PHONE_TRANSCRIPTS_FORMATTED
  WHERE LOWER(TRANSCRIPT) LIKE '%<keyword>%'
    AND START_TIME_UTC >= DATEADD(day, -180, CURRENT_DATE)
  ORDER BY START_TIME_UTC DESC
  LIMIT 20
  ```
- Query chat transcripts with the same pattern against `MESSAGING_TRANSCRIPTS_FORMATTED`
- Query AM Gong calls:
  ```sql
  SELECT METADATA_ID, METADATA_TITLE, METADATA_STARTED,
    LEFT(CONTENT_BRIEF, 2000) AS CALL_BRIEF
  FROM APP_SALES.GONG.GONG_DETAILED_CALLS
  WHERE (LOWER(CONTENT) LIKE '%<keyword>%'
    OR LOWER(CONTENT_BRIEF) LIKE '%<keyword>%')
    AND METADATA_STARTED >= DATEADD(day, -180, CURRENT_DATE)::VARCHAR
  ORDER BY METADATA_STARTED DESC
  LIMIT 20
  ```
- Query seller feedback:
  ```sql
  SELECT MERCHANT_TOKEN, CREATED_AT, FEEDBACK, COUNTRY_CODE, VERTICAL, PLATFORM
  FROM SELLER_FEEDBACK.RAW_OLTP.SELLER_FEEDBACK
  WHERE (LOWER(FEEDBACK) LIKE '%<keyword>%')
    AND CREATED_AT >= DATEADD(day, -180, CURRENT_DATE)
  ORDER BY CREATED_AT DESC
  LIMIT 20
  ```
- Query unitQ quality signals:
  ```sql
  SELECT *
  FROM APP_CASH_VOC.PUBLIC.SQUARE_UNITQ_WRITEBACK_AGGREGATED
  WHERE LOWER(TO_VARCHAR(OBJECT_CONSTRUCT(*))) LIKE '%<keyword>%'
  ORDER BY 1 DESC
  LIMIT 20
  ```
- Query AM product requests:
  ```sql
  SELECT *
  FROM FIVETRAN.AM_ANALYTICS.PRODUCT_REQUESTS_INTAKE
  WHERE LOWER(TO_VARCHAR(OBJECT_CONSTRUCT(*))) LIKE '%<keyword>%'
  ORDER BY 1 DESC
  LIMIT 20
  ```

**Glean** (Glean MCP):
- Use `search_block_knowledge_base` with the feature name and key terms
- Read the top 3–5 most relevant documents using `read_documents_from_block_knowledge_base`
- Collect document titles and links

#### 2b. Self-Check: Did I Search Everything?

**Before moving on, verify you executed ALL of the following searches. Check each one off:**

- [ ] Slack — searched all 7 channels listed above
- [ ] Airtable — searched for relevant bases/tables
- [ ] Snowflake — `PHONE_TRANSCRIPTS_FORMATTED` (CS phone)
- [ ] Snowflake — `MESSAGING_TRANSCRIPTS_FORMATTED` (CS chat)
- [ ] Snowflake — `GONG_DETAILED_CALLS` (AM Gong calls)
- [ ] Snowflake — `SELLER_FEEDBACK` (direct seller feedback)
- [ ] Snowflake — `SQUARE_UNITQ_WRITEBACK_AGGREGATED` (unitQ signals)
- [ ] Snowflake — `PRODUCT_REQUESTS_INTAKE` (AM product requests)
- [ ] Glean — searched internal docs

**If any search was not executed, go back and execute it now before proceeding.** Do NOT skip Snowflake tables — this is the most commonly missed step.

**→ Print Step 2 completion report (with per-source result counts) before proceeding.**

#### 3b. Filter for Relevance

After all searches return, apply the **80% relevance threshold**:

1. For each result, assess: _Does this directly relate to the feature being described?_
2. Discard anything that only mentions the feature in passing or relates to a different feature in the same area
3. Keep results that provide direct evidence: feedback, decisions, metrics, or prior work on this feature
4. When in doubt, **exclude the reference**

#### 3c. Compile Reference Summary

Before generating the PRD, compile the relevant references into a brief summary for the user:

```markdown
### Internal References Found

**Slack** (X relevant messages):
- [Summary of finding] — [permalink]

**Airtable** (X relevant records):
- [Summary of finding] — [record URL]

**Snowflake / CS Transcripts** (X relevant transcripts):
- [Summary of finding] — Case ID: <id>

**Snowflake / AM Calls** (X relevant calls):
- [Summary of finding] — Gong Call: <title> (<date>)

**Snowflake / Seller Feedback** (X relevant entries):
- [Summary of finding] — Merchant: <token> (<date>)

**Snowflake / unitQ Quality Signals** (X relevant entries):
- [Summary of finding] — unitQ record

**Snowflake / AM Product Requests** (X relevant entries):
- [Summary of finding] — Request record

**Glean / Internal Docs** (X relevant documents):
- [Document title](link) — [Summary of finding]

**Excluded**: Y results were found but excluded as below the 80% relevance threshold.
```

Present this summary to the user alongside your clarifying questions (Step 3).

**→ Print Step 2 reference summary (above format) before proceeding.**

### 3. Ask Clarifying Questions

**After reviewing internal sources**, ask 3–5 targeted questions to fill remaining gaps. Use what you learned from the internal search to make questions more specific and to pre-fill answers where the evidence is clear. Only ask where the answer is genuinely unclear from the input **and** the internal sources.

Focus on:
- Who is the target user and what pain point does this solve?
- What does success look like? How will it be measured?
- What is explicitly out of scope?
- Are there technical constraints, dependencies, or integrations?
- What is the timeline or release target?
- Which org area does this belong to? (See AGENTS.md §3 for org structure)

When internal sources already answer a question, state what you found and ask the user to confirm rather than asking from scratch. For example:

> _"Based on Slack discussions in #seller-feedback, the primary pain point appears to be [X]. Does that match your understanding, or is there a different angle?"_

Make questions easy to answer:
- Use numbered questions with lettered options
- Suggest reasonable defaults and mark them clearly
- Include a fast-path response (e.g., reply `defaults` to accept all defaults)
- Keep it to one pass — don't ask questions for the sake of it

```text
1) Who is the primary user?
   a) Sellers (merchants)
   b) Buyers (end customers)
   c) Internal operations
   d) Multiple segments

2) What org area does this fall under?
   a) Buyers, Online & Staff
   b) Core Product
   c) Platform & Foundations
   d) Other: [specify]

3) Do you have success metrics in mind?
   a) Yes - I'll share them
   b) No - suggest some based on the problem
   c) Not sure yet

4) What's the timeline?
   a) Urgent - this quarter
   b) Next quarter
   c) Long-term / exploratory
   d) Not sure

Reply with: defaults (or 1a 2c 3b 4b)
```

**→ Print Step 3 completion report (listing questions asked) before proceeding. Wait for user answers before moving to Step 4.**

### 4. Generate the PRD

Once you have sufficient clarity and internal references, produce the PRD using the **exact template** below. This template matches AGENTS.md §7.1.

**Augment the PRD with internal references:**
- **Problem Statement (§1)**: Cite CS transcripts, seller feedback, or Slack escalations that validate the problem. Include quoted evidence with links.
- **Goals (§2)**: Use Snowflake metrics or Airtable data to ground targets in real numbers.
- **Users and Use Cases (§4)**: Reference seller feedback or AM call summaries to illustrate pain points and workarounds.
- **Requirements (§5)**: Reference prior decisions or RFCs from Slack/Glean that inform scope.
- **Logging & Analytics Events (§7)**: PRD §7 links to a separate `EVENT-LOGGING.md` file in the same folder. See Step 5b for generating it.
- **Risks & Mitigations (§11)**: Reference churn threats or escalations that highlight urgency.
- **Appendix (§13)**: List all internal references used, grouped by source, with links.

**→ Print Step 4 completion report (listing all 13 PRD sections generated) before proceeding.**

### 5. Save the PRD

Save to `requirements/<scope>/<feature>/PRD.md` following the org structure in AGENTS.md §3.

If the feature directory doesn't exist, create it.

**→ Print Step 5 completion report (with file path) before proceeding.**

### 5b. Generate EVENT-LOGGING.md

**After saving the PRD**, create `requirements/<scope>/<feature>/EVENT-LOGGING.md` with the event logging dictionary. Walk through every step in the UX flows defined in PRD §6 and generate a corresponding logging event row. Every user action (tap, click, view, dismiss, submit) and system outcome MUST have an event.

Use the **EVENT-LOGGING.md template** below. The format matches Square's standard event logging convention (see OCR event logging as reference):

- Group events by UX flow (one table per flow)
- Each row has: Priority, `event_name` (`click_feature` or `view_feature`), `feature_name`, `event_description` (PascalCase action name), trigger description, `action_item`, `sub_action_item`, `additional_properties` (JSON schema), `is_task_completed`
- All `additional_properties` MUST include the primary entity ID (e.g., `order_id`, `invoice_id`) for correlation across the user journey
- Use `click_feature` for user actions, `view_feature` for impressions and system outcomes
- No UX step should be missing a logging event

**→ Print Step 5b completion report (with file path and number of events generated) before proceeding.**

### 6. Final Validation & Workflow Summary

Run through the Validation Before Saving checklist (below). Print the **WORKFLOW COMPLETION SUMMARY** (from the Step Completion Tracker section above) showing the status of every step and every source searched.

## Output Template

Use this exact structure. Every section is required. Use MUST/SHOULD/MAY language for requirements.

```markdown
# <Feature Name> PRD

- Scope: `<scope>`
- Feature: `<feature>`
- Status: Draft
- Owners:
  - Product: <name/team>
  - Engineering: <name/team>
  - Design/UX: <name/team>
- Last updated: YYYY-MM-DD
- Links:
  - Prototype (Blockcell): [TBD — deploy using deploying-prd-prototypes skill]
  - Architecture: ../../architecture/<scope>/<feature>/ARCHITECTURE.md
  - Tracking: <Jira/Linear link>

## 1. Problem Statement
What user/business problem are we solving? Include context and why now.
Frame from the user's perspective. Be specific — avoid vague "improve the experience" language.
Include data, customer quotes, or research that validates the problem.

## 2. Goals (Measurable)
List 3–7 measurable goals. Each goal must be testable (metric, threshold, timeframe).
Example: "Reduce seller checkout time by 30% within 90 days of launch."

## 3. Non-Goals / Out of Scope
Explicitly list what is not being built. Be specific to prevent scope creep.

## 4. Users and Use Cases
- Primary users:
- Secondary users:
- Key scenarios:

For each user segment, describe:
- Who they are
- Their pain points
- Current workarounds
- How this feature changes their experience

## 5. Requirements
### 5.1 Functional Requirements
Numbered list. Use MUST/SHOULD/MAY language.

| # | Priority | Description |
|---|----------|-------------|
| 1 | P0 | [Must-have — launch blocker] |
| 2 | P1 | [Should-have — initial release if feasible] |
| 3 | P2 | [Nice-to-have — fast-follow] |
| 4 | P3 | [Future consideration] |

### 5.2 Non-Functional Requirements
Performance, reliability, security, privacy, compliance, accessibility, localization.

### 5.3 Constraints and Assumptions
Dependencies, platform constraints, policy constraints, timelines.

## 6. UX / Flows
- Wireframes/mock links:
- Key flows:

## 7. Logging & Analytics Events

See [EVENT-LOGGING.md](EVENT-LOGGING.md) for the full event dictionary.

## 8. Prototype
- Blockcell URL: [TBD]
- Access notes (no secrets): <how to access>
- What to test:
  1.
  2.
- Known limitations:

## 9. Success Metrics & Monitoring
| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| [Primary metric] | [Specific target] | [How it's tracked] |
| [Guardrail metric] | [Threshold] | [How it's tracked] |

## 10. Rollout / Launch Plan
- Rollout strategy (flags, cohorts, geos):
- Compatibility / migration considerations:
- Comms (support, ops, sales):

## 11. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Plan] |

## 12. Open Questions
| # | Question | Owner | Due Date |
|---|----------|-------|----------|
| 1 | [Unresolved question] | [Who] | [When] |

## 13. Appendix

### Internal References
All internal sources used to inform this PRD, grouped by source:

**Slack**
- [Summary] — [permalink]

**Airtable**
- [Summary] — [record URL]

**CS Transcripts (Snowflake)**
- [Summary] — Case ID: <id>

**AM Calls (Snowflake)**
- [Summary] — Gong Call: <title> (<date>)

**Seller Feedback (Snowflake)**
- [Summary] — Merchant: <token> (<date>)

**unitQ Quality Signals (Snowflake)**
- [Summary] — unitQ record

**AM Product Requests (Snowflake)**
- [Summary] — Request record

**Internal Docs (Glean)**
- [Document title](link) — [Summary]

### Other Links
Additional links, notes, related initiatives.
```

## EVENT-LOGGING.md Template

Save to `requirements/<scope>/<feature>/EVENT-LOGGING.md` alongside the PRD. Generate one table per UX flow from PRD §6. Every UX step MUST have a corresponding event row.

```markdown
# <Feature Name> — Event Logging

- Feature: `<feature>`
- Namespace: TBD (<feature_snake_case>)
- Last updated: YYYY-MM-DD

> **Note:** Assumes `merchant_token`, `session_token`, `timestamp`, `device_info` are logged for each event.

## <Flow Name 1>

| Events added by Eng | Priority | event_name | feature_name | event_description | When is this triggered? | action_item | sub_action_item | additional_properties | is_task_completed |
|---|---|---|---|---|---|---|---|---|---|
| | P0 | click_feature | <feature> | <PascalCaseAction> | <trigger description> | <action_group> | <sub_action> | `{<primary_id>: string, ...}` | FALSE |
| | P0 | view_feature | <feature> | <PascalCaseView> | <trigger description> | <action_group> | <sub_action> | `{<primary_id>: string, ...}` | FALSE |

## <Flow Name 2>

| Events added by Eng | Priority | event_name | feature_name | event_description | When is this triggered? | action_item | sub_action_item | additional_properties | is_task_completed |
|---|---|---|---|---|---|---|---|---|---|
| | P0 | click_feature | <feature> | <PascalCaseAction> | <trigger description> | <action_group> | <sub_action> | `{<primary_id>: string, ...}` | FALSE |
```

**Column reference:**

| Column | Description |
|--------|-------------|
| Events added by Eng | Completion status (blank until eng implements) |
| Priority | P0 (launch blocker), P1 (should-have), P2 (nice-to-have) |
| event_name | `click_feature` (user actions) or `view_feature` (impressions/outcomes) |
| feature_name | Feature identifier in `snake_case` |
| event_description | PascalCase action name (e.g., `BeginSplitPayment`, `ViewWarningModal`) |
| When is this triggered? | Human-readable trigger description (not included in schema) |
| action_item | Logical group for the action (e.g., `split_payment_warning`) |
| sub_action_item | Specific sub-action (e.g., `confirm_warning`, `click_retry`) |
| additional_properties | JSON schema of event-specific properties |
| is_task_completed | `FALSE` until eng implements and verifies |

## Writing Standards

- **Be specific.** "Reduce checkout time by 30%" not "make checkout faster."
- **Be concise.** Every sentence earns its place. Cut filler.
- **Use active voice.** "The system sends a notification" not "a notification is sent."
- **Use MUST/SHOULD/MAY** for requirements per AGENTS.md §8.
- **Frame from the user's perspective.** What the user experiences, not what the system does.
- **Prioritize ruthlessly.** Not everything is P0. If everything is critical, nothing is.
- **Quantify where possible.** Metrics, targets, and thresholds over vague qualifiers.
- **No secrets.** Describe how to obtain access via internal systems; never include credentials.

## Validation Before Saving

Before saving, verify against AGENTS.md §5:

- [ ] File is at `requirements/<scope>/<feature>/PRD.md`
- [ ] No folders deeper than `<scope>/<feature>`
- [ ] PRD contains all 13 sections from the template
- [ ] PRD contains success metrics
- [ ] `EVENT-LOGGING.md` exists in the same folder with events mapped to each UX flow step
- [ ] PRD contains non-goals / out of scope
- [ ] PRD contains rollout / launch considerations
- [ ] Prototype section exists (can be `[TBD]` initially)
- [ ] `<scope>` and `<feature>` are kebab-case
- [ ] Last updated date is set
- [ ] Internal source search was performed (Slack, Airtable, Snowflake, Glean)
- [ ] All included references have traceable links
- [ ] Appendix §13 lists all internal references grouped by source
- [ ] Only references ≥80% relevant to the feature are included

If a check fails, either fix it or add a clearly labeled **Open Questions** entry explaining what blocks compliance.

## Anti-patterns

- Don't ask clarifying questions before searching internal sources — always search first so questions are informed by evidence
- Don't generate the PRD without asking clarifying questions first
- Don't skip the internal source search — always search Slack, Airtable, Snowflake, and Glean before drafting
- Don't include references without traceable links — every reference needs a permalink, record URL, case ID, or doc link
- Don't include borderline references — if a reference is not at least 80% related to the feature, exclude it
- Don't make business decisions — help the user articulate theirs clearly
- Don't write vague requirements like "improve the experience"
- Don't skip sections — mark them `[TBD]` with an owner if information is missing
- Don't assume information not provided — ask for it
- Don't include implementation details or code — that belongs in architecture
