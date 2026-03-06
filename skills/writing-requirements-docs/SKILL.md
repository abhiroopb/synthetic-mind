---
Skill name: writing-requirements-docs
Skill description: Write crisp, thorough PRDs from rough notes, customer feedback, or raw input using a canonical PRD template. Automatically searches Slack, project trackers, data warehouse, and knowledge bases for internal references to augment the PRD with traced-back evidence.
---

# Writing Requirements Documents

Translate raw input — rough notes, customer feedback, bullet lists, designs, verbal transcripts, Slack threads — into structured, actionable PRDs that conform to the canonical PRD template. Before drafting, **automatically search internal sources** (Slack, project trackers, data warehouse, knowledge base) for references related to the feature, and use relevant findings to augment the PRD with linked evidence.

## Differentiation from spec-creator

This skill enforces the **canonical PRD template**. It is designed for PMs who start with messy, unstructured input and need a complete, validation-ready PRD. Unlike `spec-creator`, this skill does not use Linear and follows the strict template exactly. It also **automatically searches internal sources** and weaves evidence into the PRD with traceable links.

## Prerequisites

Install the required CLI skills if not already installed:

```bash
# Install skills for your data warehouse, messaging, knowledge base, and project tracker integrations
```

**IMPORTANT: You must be connected to your corporate VPN.**

Enable your data warehouse, messaging, knowledge base, and project tracker MCPs before proceeding.

## Role

You are an expert Product Manager translating business goals and user needs into clear, testable specifications. You accept any form of raw input, search internal sources for supporting evidence, and produce a PRD that passes the validation checks.

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
| Project tracker bases | Project Tracker | Roadmaps, feature trackers, prioritization records, research logs |
| Support Phone Transcripts | Data Warehouse | Customer complaints or requests related to the feature |
| Support Chat Transcripts | Data Warehouse | Customer complaints or requests related to the feature |
| Sales Calls | Data Warehouse | Account Manager conversations about the feature |
| Customer Feedback | Data Warehouse | Direct customer feedback mentioning the feature |
| Quality Signals | Data Warehouse | Aggregated quality signals and writeback data |
| Product Requests | Data Warehouse | Account Manager product requests intake and tracking |
| Internal Docs | Knowledge Base | PRDs, research, design docs, decision records, strategy docs |

### Slack Channels to Search

Search these channels plus any scope-specific channels the user identifies:

| Channel | Purpose |
|---------|---------|
| `#your-churn-alerts-channel` | High-value customer churn signals and escalations |
| `#your-retention-channel` | Urgent retention cases and customer issues |
| `#your-feedback-intake-channel` | General customer feedback intake and triage |
| `#your-shipped-channel` | Shipped features and launches |
| `#your-product-announce-channel` | Product announcements and updates |
| `#your-feedback-channel` | Customer feedback discussions |
| `#your-quality-alerts-channel` | Quality alerts across products |

### Data Warehouse Tables

| Table | Description |
|-------|-------------|
| `YOUR_SUPPORT_SCHEMA.PHONE_TRANSCRIPTS` | Support phone transcripts |
| `YOUR_SUPPORT_SCHEMA.MESSAGING_TRANSCRIPTS` | Support chat transcripts |
| `YOUR_SALES_SCHEMA.DETAILED_CALLS` | Sales call transcripts with AI summaries |
| `YOUR_FEEDBACK_SCHEMA.CUSTOMER_FEEDBACK` | Direct customer feedback |
| `YOUR_QUALITY_SCHEMA.QUALITY_SIGNALS_AGGREGATED` | Aggregated quality signals and writeback data |
| `YOUR_ANALYTICS_SCHEMA.PRODUCT_REQUESTS_INTAKE` | Product requests intake and tracking |

### Relevance Threshold

**Only include a reference if it is at least 80% related to the feature being described.** Err on the side of excluding borderline references. A reference is relevant when it:

- Directly names or describes the feature or a closely related capability
- Contains customer feedback about the specific problem the feature solves
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
- **Slack**: Use the permalink from search results
- **Project Tracker**: Use the record URL
- **Data Warehouse**: `Case ID: <case_id>` or `Sales Call: <metadata_title> (<metadata_started>)` (include the query used)
- **Knowledge Base**: Document title with link returned by search

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

If a step produces no results (e.g., a data warehouse query returns 0 rows), you MUST still report it:
```
  - Data Warehouse / Support Phone Transcripts: ⚠️ 0 results (query executed, no matches for keywords)
```

**At the end of the entire workflow**, print a final summary checklist:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 WORKFLOW COMPLETION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1 — Analyze Input:         ✅ Done
Step 2 — Search Internal Sources:
  - Slack:                      ✅ X messages found / ⚠️ 0 results
  - Project Tracker:            ✅ X records found / ⚠️ 0 results
  - DW (Phone):                 ✅ X transcripts / ⚠️ 0 results
  - DW (Chat):                  ✅ X transcripts / ⚠️ 0 results
  - DW (Sales Calls):           ✅ X calls / ⚠️ 0 results
  - DW (Customer Feedback):     ✅ X entries / ⚠️ 0 results
  - DW (Quality Signals):       ✅ X entries / ⚠️ 0 results
  - DW (Product Requests):      ✅ X entries / ⚠️ 0 results
  - Knowledge Base:             ✅ X docs found / ⚠️ 0 results
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

**Before asking clarifying questions**, search all internal sources in parallel using the keywords and synonyms extracted in Step 1. This ensures you understand the existing context, prior decisions, known pain points, and customer feedback before engaging the user — so your clarifying questions are sharper and informed by real evidence.

Use the Task tool to run parallel searches across all sources simultaneously.

**You MUST search ALL of the following sources. Do not skip any. Report results for each one individually, even if 0 results.**

#### 2a. Execute Parallel Searches

Launch parallel searches across all sources. For each source, use the appropriate MCP:

**Slack** (Slack MCP `search_messages`):
- Search each channel listed above for the feature keywords
- Use `newer_than: "P180D"` (last 6 months) unless the user specifies a different period
- Collect message permalinks for any relevant hits

**Project Tracker** (Project Tracker MCP):
- Search for bases and tables related to the feature's scope area
- Look for roadmap entries, feature requests, prioritization records, and research logs
- Collect record URLs for any relevant hits

**Data Warehouse** (Data Warehouse MCP):
- Query support transcripts for customer mentions of the feature (last 180 days):
  ```sql
  SELECT CASE_ID, START_TIME_UTC, LEFT(TRANSCRIPT, 3000) AS TRANSCRIPT_PREVIEW
  FROM YOUR_SUPPORT_SCHEMA.PHONE_TRANSCRIPTS
  WHERE LOWER(TRANSCRIPT) LIKE '%<keyword>%'
    AND START_TIME_UTC >= DATEADD(day, -180, CURRENT_DATE)
  ORDER BY START_TIME_UTC DESC
  LIMIT 20
  ```
- Query chat transcripts with the same pattern against `YOUR_SUPPORT_SCHEMA.MESSAGING_TRANSCRIPTS`
- Query sales calls:
  ```sql
  SELECT METADATA_ID, METADATA_TITLE, METADATA_STARTED,
    LEFT(CONTENT_BRIEF, 2000) AS CALL_BRIEF
  FROM YOUR_SALES_SCHEMA.DETAILED_CALLS
  WHERE (LOWER(CONTENT) LIKE '%<keyword>%'
    OR LOWER(CONTENT_BRIEF) LIKE '%<keyword>%')
    AND METADATA_STARTED >= DATEADD(day, -180, CURRENT_DATE)::VARCHAR
  ORDER BY METADATA_STARTED DESC
  LIMIT 20
  ```
- Query customer feedback:
  ```sql
  SELECT CUSTOMER_ID, CREATED_AT, FEEDBACK, COUNTRY_CODE, VERTICAL, PLATFORM
  FROM YOUR_FEEDBACK_SCHEMA.CUSTOMER_FEEDBACK
  WHERE (LOWER(FEEDBACK) LIKE '%<keyword>%')
    AND CREATED_AT >= DATEADD(day, -180, CURRENT_DATE)
  ORDER BY CREATED_AT DESC
  LIMIT 20
  ```
- Query quality signals:
  ```sql
  SELECT *
  FROM YOUR_QUALITY_SCHEMA.QUALITY_SIGNALS_AGGREGATED
  WHERE LOWER(TO_VARCHAR(OBJECT_CONSTRUCT(*))) LIKE '%<keyword>%'
  ORDER BY 1 DESC
  LIMIT 20
  ```
- Query product requests:
  ```sql
  SELECT *
  FROM YOUR_ANALYTICS_SCHEMA.PRODUCT_REQUESTS_INTAKE
  WHERE (LOWER(PRODUCT_REQUEST) LIKE '%<keyword>%'
    OR LOWER(REQUEST_DETAILS) LIKE '%<keyword>%'
    OR LOWER(DESCRIPTION) LIKE '%<keyword>%')
  ORDER BY 1 DESC
  LIMIT 20
  ```

**Knowledge Base** (Knowledge Base MCP):
- Search for feature name and synonyms
- Look for PRDs, design docs, research, decision records

#### 2b. Evaluate Relevance

For each result, apply the 80% relevance threshold. Discard borderline references.

**→ Print Step 2 completion report (listing each source, results found, and key insights) before proceeding.**

### 3. Ask Clarifying Questions

Now that you have evidence from internal sources, ask **informed** clarifying questions. Reference findings where relevant:

> "I found 12 support transcripts mentioning [feature]. The main complaints are [X] and [Y]. Should the PRD address both, or are we scoping to [X] only?"

**→ Print Step 3 completion report before proceeding.**

### 4. Generate the PRD

Using the template below, write each section. Weave in internal references where they add value:

- **Problem Statement (§1)**: Use customer feedback quotes and support data to validate the problem.
- **Users and Use Cases (§4)**: Reference customer feedback or sales call summaries to illustrate pain points and workarounds.
- **Requirements (§5)**: Reference prior decisions or RFCs from Slack/Knowledge Base that inform scope.
- **Logging & Analytics Events (§7)**: PRD §7 links to a separate `EVENT-LOGGING.md` file in the same folder. See Step 5b for generating it.
- **Risks & Mitigations (§11)**: Reference churn threats or escalations that highlight urgency.
- **Appendix (§13)**: List all internal references used, grouped by source, with links.

**→ Print Step 4 completion report (listing all 13 PRD sections generated) before proceeding.**

### 5. Save the PRD

Save to `requirements/<scope>/<feature>/PRD.md` following the org structure.

If the feature directory doesn't exist, create it.

**→ Print Step 5 completion report (with file path) before proceeding.**

### 5b. Generate EVENT-LOGGING.md

**After saving the PRD**, create `requirements/<scope>/<feature>/EVENT-LOGGING.md` with the event logging dictionary. Walk through every step in the UX flows defined in PRD §6 and generate a corresponding logging event row. Every user action (tap, click, view, dismiss, submit) and system outcome MUST have an event.

Use the **EVENT-LOGGING.md template** below. The format matches standard event logging conventions:

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
  - Prototype: [TBD — deploy using prototype deployment skill]
  - Architecture: ../../architecture/<scope>/<feature>/ARCHITECTURE.md
  - Tracking: <Issue tracker link>

## 1. Problem Statement
What user/business problem are we solving? Include context and why now.
Frame from the user's perspective. Be specific — avoid vague "improve the experience" language.
Include data, customer quotes, or research that validates the problem.

## 2. Goals (Measurable)
List 3–7 measurable goals. Each goal must be testable (metric, threshold, timeframe).
Example: "Reduce customer checkout time by 30% within 90 days of launch."

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
- Prototype URL: [TBD]
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

**Project Tracker**
- [Summary] — [record URL]

**Support Transcripts (Data Warehouse)**
- [Summary] — Case ID: <id>

**Sales Calls (Data Warehouse)**
- [Summary] — Call: <title> (<date>)

**Customer Feedback (Data Warehouse)**
- [Summary] — Customer: <id> (<date>)

**Quality Signals (Data Warehouse)**
- [Summary] — Quality record

**Product Requests (Data Warehouse)**
- [Summary] — Request record

**Internal Docs (Knowledge Base)**
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

> **Note:** Assumes `customer_id`, `session_token`, `timestamp`, `device_info` are logged for each event.

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
- **Use MUST/SHOULD/MAY** for requirements.
- **Frame from the user's perspective.** What the user experiences, not what the system does.
- **Prioritize ruthlessly.** Not everything is P0. If everything is critical, nothing is.
- **Quantify where possible.** Metrics, targets, and thresholds over vague qualifiers.
- **No secrets.** Describe how to obtain access via internal systems; never include credentials.

## Validation Before Saving

Before saving, verify:

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
- [ ] Internal source search was performed (Slack, Project Tracker, Data Warehouse, Knowledge Base)
- [ ] All included references have traceable links
- [ ] Appendix §13 lists all internal references grouped by source
- [ ] Only references ≥80% relevant to the feature are included

If a check fails, either fix it or add a clearly labeled **Open Questions** entry explaining what blocks compliance.

## Anti-patterns

- Don't ask clarifying questions before searching internal sources — always search first so questions are informed by evidence
- Don't generate the PRD without asking clarifying questions first
- Don't skip the internal source search — always search Slack, project tracker, data warehouse, and knowledge base before drafting
- Don't include references without traceable links — every reference needs a permalink, record URL, case ID, or doc link
- Don't include borderline references — if a reference is not at least 80% related to the feature, exclude it
- Don't make business decisions — help the user articulate theirs clearly
- Don't write vague requirements like "improve the experience"
- Don't skip sections — mark them `[TBD]` with an owner if information is missing
- Don't assume information not provided — ask for it
- Don't include implementation details or code — that belongs in architecture
