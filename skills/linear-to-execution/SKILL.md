---
Skill name: linear-to-execution
Skill description: Picks up a Linear issue and prepares an agent for execution. Use when asked to 'work on this issue', 'pick up ISSUE-123', or 'execute this ticket'. Pairs with plan-to-linear skill. Experimental.
---

# Linear to Execution

Reads a Linear issue and prepares an agent to execute the work described in it.

## Status: Experimental

This skill is in early development. Pairs with `plan-to-linear` for a complete planning-to-execution workflow.

## When to Use

- User says "work on this issue" or "pick up ISSUE-123"
- User says "execute this ticket"
- User pastes a Linear issue URL
- Agent is starting work from a Linear backlog

## Prerequisites

1. Load the `linear` skill for issue fetching
2. Ensure `LINEAR_API_KEY` is set

## Workflow

### Phase 1: Fetch the Issue

```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts get-issue-v2 ISSUE-123 \
  --fields identifier,title,description,comments,parents \
  --output-format rich-json
```

If the user provides a Linear URL, extract the issue ID:
- `https://linear.app/team/issue/ENG-123/...` → `ENG-123`

### Phase 2: Parse Issue Structure

Look for structured sections in the description (especially if created by `plan-to-linear`):

| Section | What to Extract |
|---------|-----------------|
| **Context** | Background and why this work matters |
| **Objective** | The core goal to accomplish |
| **Acceptance Criteria** | Checkable definition of done |
| **Relevant Code** | File paths and what needs to change |
| **Dependencies** | Blocked-by issues that must complete first |
| **Plan Reference** | Source thread URL or document |

### Phase 3: Verify Dependencies

If the issue has blocking dependencies:

1. Fetch each blocking issue
2. Check if their status is "Done" or "Completed"
3. If blocked, inform the user and suggest working on blockers first

```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts get-issue BLOCKER-ID
```

### Phase 4: Load Context

If a source thread URL is referenced:
```
Use read_thread tool with the thread ID to get planning context
```

If code paths are listed:
```
Use Read tool to load each referenced file
```

### Phase 5: Create Execution Plan

Based on the parsed issue, create a task_list for execution:

```
task_list action:create title:"[ISSUE-123] Main objective" description:"Full context from issue"
```

Break down acceptance criteria into sub-tasks:
```
task_list action:create title:"Criterion 1" parentID:"main-task-id"
task_list action:create title:"Criterion 2" parentID:"main-task-id"
```

### Phase 6: Begin Execution

1. Update issue status to "In Progress":
```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts update-status ISSUE-123 "In Progress"
```

2. Start working through the task_list

3. As work progresses, add comments to the issue:
```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts add-comment "Started work on X" -i ISSUE-123
```

### Phase 7: Complete

When all acceptance criteria are met:

1. Mark tasks complete in task_list
2. Add completion comment:
```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts add-comment "Completed: [summary of what was done]" -i ISSUE-123
```

3. Update status:
```bash
cd ~/.config/agents/skills/linear && npx tsx linear-cli.ts update-status ISSUE-123 "In Review"
```

## Handling Unstructured Issues

Not all issues follow the `plan-to-linear` template. For unstructured issues:

1. **Extract what you can**: Title, description, any file paths mentioned
2. **Ask clarifying questions** if critical info is missing:
   - "What does 'done' look like for this issue?"
   - "Which files should I focus on?"
3. **Check comments**: Often contain additional context
4. **Check parent issues**: May have broader context

## Example Session

**User**: "Pick up ENG-456"

**Agent**:
1. Fetches ENG-456 via Linear CLI
2. Parses description, finds acceptance criteria and file paths
3. Checks dependencies—none blocking
4. Reads referenced source files
5. Creates task_list with execution plan
6. Updates issue to "In Progress"
7. Begins implementation
8. Adds progress comments as milestones complete
9. On completion, updates to "In Review"

## Integration with plan-to-linear

These skills form a complete loop:

```
Planning Session
      ↓
plan-to-linear → Creates structured Linear issues
      ↓
Linear Backlog
      ↓
linear-to-execution → Agent picks up and executes
      ↓
Completed Work
```

Issues created by `plan-to-linear` are optimized for `linear-to-execution` to parse, but this skill handles any Linear issue.
