---
name: plan-to-linear
description: "Convert structured plans into Linear issues and projects. Use when creating, filing, converting, transforming, decomposing, splitting, or breaking down a plan into Linear tickets, issues, or projects. Also use when bulk-creating Linear issues from a task list, document, or conversation."
metadata:
  status: experimental
---

# Plan to Linear

Converts structured plans into well-formed Linear issues that another agent can pick up and execute.

**STOP** — Before proceeding, load the `linear` skill and verify setup is complete. See [SETUP.md](SETUP.md) for prerequisites. If the user hasn't specified a team, ask before continuing.

## Workflow

### Phase 1: Gather Plan Context

Collect the plan from one of these sources:

1. **task_list**: Use `task_list action:list` to get current tasks
2. **Document**: Read a planning doc the user references
3. **Conversation**: Extract from the current thread discussion

For each planned item, capture:
- Title/summary
- Detailed description of what needs to be done
- Acceptance criteria (what "done" looks like)
- File paths, function names, or code locations involved
- Dependencies on other items

### Phase 2: Structure Issues for Agent Execution

Each Linear issue must be **self-contained** enough for a future agent to execute without the original planning context. Each issue description should include:

- **Context**: Why this work is needed (1-2 paragraphs)
- **Objective**: Clear statement of what to accomplish
- **Acceptance Criteria**: Specific, testable checkboxes
- **Relevant Code**: File paths and what needs to change
- **Dependencies**: Blocked-by / blocks references

### Phase 3: Resolve the Team

Use `list-teams` or `get-team` to resolve the identifier:

```bash
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts list-teams
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts get-team TEAM-KEY
```

### Phase 4: Create a Project (optional)

If the plan represents a cohesive body of work, create a Linear project to group the issues:

```bash
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts create-project \
  --name "Project Name" \
  --team "TEAM" \
  --description "Project description" \
  --lead me
```

### Phase 5: Create Issues

Create issues in parallel where possible for speed:

```bash
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts create-issue \
  --title "Issue title" \
  --description "Full description" \
  --team "TEAM" \
  --assignee me \
  --labels "agent-created,from-plan"
```

If a project was created in Phase 4, add the issues to it:

```bash
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts add-to-project \
  --issues "TEAM-1,TEAM-2,TEAM-3" \
  --project "Project Name"
```

### Phase 6: Link Issues

After creation:
1. Update issues with cross-references (blocked-by/blocks)
2. Add the source thread URL as an attachment if available:
```bash
cd {{SKILL_DIR}}/../linear && npx tsx linear-cli.ts add-link ISSUE-123 "https://source-url" -t "Source Plan"
```

## Reference Files

| File | Load when |
|------|-----------|
| [references/issue-template.md](references/issue-template.md) | Need a full markdown template or tips for writing good issues |
| [SETUP.md](SETUP.md) | First-time setup, prerequisites |

## Related Skills

- **linear** — Core Linear CLI for issue/project operations (required dependency)
- **linear-to-execution** — Pick up Linear issues and execute them (pairs with this skill)
