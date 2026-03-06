---
name: create-permission
description: "Creates or modifies Square permissions end-to-end across proto files, permissions maps, and em-permissions config. Use when asked to create a permission, add a permission, modify a permission mapping, update a SAFE mapping, or set up a new permission."
allowed-tools:
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(bazel:*)
  - Bash(bundle:*)
  - Bash(make:*)
  - Bash(go:*)
  - Bash(rbenv:*)
  - Bash(rvm:*)
  - Bash(mise:*)
  - Bash(asdf:*)
  - Bash(source:*)
  - Bash(eval:*)
  - Bash(dig:*)
  - Bash(rg:*)
  - Bash(cp:*)
  - Bash(mkdir:*)
  - Read
  - Grep
  - Glob
  - mcp:notion(notion-fetch)
  - mcp:notion(fetch)
---

# Create Permission

You help engineers create and modify Square permissions. The process spans multiple repos and can involve any combination of:

- **Developer permission**: a proto enum in the Multipass proto, used by Envoy SAFE for API authorization and/or by third-party OAuth apps.
- **Employee permission**: a proto enum in the Employee proto (`EmployeePermissionFlags`), the underlying data model for team-level permissions. A display permission may require multiple employee enums if different access points map to different enums.
- **Display permission**: a UI configuration in em-permissions YAML that surfaces a permission in the seller-facing team permissions UI. A display permission may be backed by one or more employee permission enums, or it may be UI-only with no proto backing.
- **SAFE mapping**: an entry in `multipass-permissions-map.yaml` that maps an employee permission to one or more developer permissions for Envoy SAFE authorization.
- **Employee permission mapping**: a per-access-point mapping in em-permissions that connects a display permission to different employee enums for different surfaces (spos, mpos, dashboard).

This skill is driven by the user's approved Notion intake form. Rather than walking through a fixed questionnaire, you parse the intake form, derive what operations need to happen, confirm the plan with the user, ask only about missing information, and execute.

Use a conversational tone throughout: "I'll help you...", "Let's figure out...", "Next, I need to know...".

## Test Mode

Activate test mode if ANY of the following are true:
- The user says they are testing, doing a test run, or trying out the skill
- Any permission name contains the word `TEST` (case-insensitive)

When test mode is active, add `--draft` and remove `--reviewer` from ALL `gh pr create` commands across both phases. This avoids sending review notifications and creating PR noise for the Permissions team. Tell the user when test mode is activated and why.

## Repos

These repos must be cloned locally. Check each one exists before starting. Do NOT attempt to clone repos — some are very large and will exceed the Bash execution timeout. If any are missing, list the exact `git clone` command for each missing repo and ask the user to run them. Only list the repos that are missing. Wait for the user to confirm all clones are complete before proceeding.

- `~/Development/java` — `git clone org-49461806@github.com:squareup/java.git ~/Development/java`
- `~/Development/go/src/square/up` — `git clone org-49461806@github.com:squareup/go-square.git ~/Development/go/src/square/up`
- `~/Development/em-permissions` — `git clone org-49461806@github.com:squareup/em-permissions.git ~/Development/em-permissions`
- `~/Development/roster-rails` — `git clone org-49461806@github.com:squareup/roster-rails.git ~/Development/roster-rails`
- `~/Development/dashboard` — `git clone org-49461806@github.com:squareup/dashboard.git ~/Development/dashboard`

## Detecting Phase

If the user says "Config Phase for PERMISSION_NAME" (or "Phase 2 for PERMISSION_NAME"), skip to the **Config Phase**. Otherwise, start from the beginning with **Stage 0: Parse Intake**.

## Proto Phase Flow

1. **Stage 0 — Parse Intake**: Ask for the Notion URL, fetch it via MCP, parse into the snapshot schema, confirm with user. Load `references/intake-snapshot-schema.md` for the schema definition.
2. **Stage 1 — Derive Change Plan**: Map snapshot fields to operations, apply guardrails, present plan for confirmation. Load `references/operation-registry.md` for operation definitions and derivation rules.
3. **Stage 2 — Targeted Q&A**: For each operation, ask about missing fields only. Load `references/targeted-qa.md` for the question catalog.
4. **Stage 3 — Execute**: Run git hygiene (load `references/git-hygiene.md`), execute each proto operation, open PRs, save state. Load `references/proto-phase-execution.md` for execution details and `references/state-file.md` for the state file schema.

If the plan has no Proto Phase operations, skip to Config Phase execution in a single pass. See `references/state-file.md` for single-pass flow details.

## Config Phase Flow

Load `references/config-phase.md` for the full Config Phase workflow: state validation, environment pre-flight, all-protos bumps, display permission YAML, templates, backfill guidance, em-permissions PR, Go proto bump, and final summary.

Before any work, run git hygiene on ALL repos (load `references/git-hygiene.md`).

## Reference Files

- `references/git-hygiene.md` — Load at the start of every phase. Repo reset procedure.
- `references/intake-snapshot-schema.md` — Load when parsing the intake form. Canonical data model.
- `references/operation-registry.md` — Load when deriving the change plan. Operation definitions, required fields, plan derivation rules, and guardrails.
- `references/targeted-qa.md` — Load during Stage 2. Missing field questions per operation.
- `references/proto-phase-execution.md` — Load during Stage 3. Execution details for each proto operation, PR creation.
- `references/state-file.md` — Load after proto execution or when handling single-pass flow. State file schema and closing instructions.
- `references/config-phase.md` — Load when entering Config Phase. Full end-to-end Config Phase workflow.
