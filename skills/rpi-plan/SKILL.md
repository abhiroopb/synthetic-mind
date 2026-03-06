---
Skill name: rpi-plan
Skill description: Create detailed implementation plans using RPI methodology. Use after research phase when ready to design, architect, outline, specify, or draft an implementation plan. Creates actionable, phased plans with success criteria.
---

# RPI Plan

Planning phase of the RPI (Research, Plan, Implement) methodology. Creates detailed, actionable implementation plans grounded in codebase reality. **The output is a Markdown file** at `thoughts/shared/plans/YYYY-MM-DD-TICKET-description.md`.

**YOUR JOB IS TO PLAN, NOT IMPLEMENT.** When the plan document is complete, you are done. Implementation is a separate step (use `rpi-implement`).

## Process

### 1. Gather Context

- Read all mentioned files (tickets, research docs, JSON) **fully** before doing anything else
- Spawn parallel sub-agents to find related files, trace data flow, and understand current implementation
- Read all files identified by research into main context
- Present your understanding with file:line references, then ask only questions code investigation can't answer

### 2. Research & Align

- If the user corrects a misunderstanding, verify it yourself with new research — don't blindly accept
- Spawn parallel sub-agents for comprehensive investigation
- Wait for ALL sub-agents to complete before proceeding
- Present findings, design options with pros/cons, and open questions
- Align on approach before structuring the plan

### 3. Write the Plan

File naming: `YYYY-MM-DD-TICKET-description.md` (omit TICKET if none).

Use this template:

````markdown
# [Feature/Task Name] Implementation Plan

## Overview
[Brief description of what we're implementing and why]

## Current State Analysis
[What exists now, what's missing, key constraints discovered]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## Desired End State
[Specification of the desired end state and how to verify it]

## What We're NOT Doing
[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach
[High-level strategy and reasoning]

---

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```[language]
// Specific code to add/modify
```

### Success Criteria:
- [ ] Migration applies cleanly: `make migrate`
- [ ] Unit tests pass: `make test`
- [ ] Type checking passes: `npm run typecheck`
- [ ] Linting passes: `make lint`

---

## Phase 2: [Descriptive Name]
[Same structure...]

---

## Testing Strategy

### Unit Tests:
- [What to test, key edge cases]

### Integration Tests:
- [End-to-end scenarios]

### Manual Testing (only if automated testing is truly insufficient):
1. [Step that cannot be automated]

## Performance Considerations
[Any performance implications or optimizations needed]

## Migration Notes
[If applicable, how to handle existing data/systems]

## References
- Original ticket: `thoughts/shared/tickets/eng_XXXX.md`
- Related research: `thoughts/shared/research/[relevant].md`
- Similar implementation: `[file:line]`
````

### 4. Review & Iterate

Present the draft location and iterate until the user is satisfied. Be ready to add phases, adjust approach, clarify criteria, or change scope.

## Guidelines

1. **Be Skeptical** — Question vague requirements. Ask "why" and "what about". Verify with code, don't assume.
2. **Be Interactive** — Don't write the full plan in one shot. Get buy-in at each step. Allow course corrections.
3. **Be Thorough** — Read files completely. Research actual code patterns. Include file:line references. Write measurable success criteria.
4. **Be Practical** — Focus on incremental, testable changes. Consider migration and rollback. Include "what we're NOT doing".
5. **No Open Questions** — If you hit an open question, stop and resolve it immediately. The final plan must be complete and actionable.
6. **Prefer Automated Verification** — Only include manual testing if it truly can't be automated. Place manual checks at the very end.

## Related Skills

- `rpi-research` — Research phase (run before planning)
- `rpi-implement` — Execute the plan this skill produces
- `rpi-iterate` — Update an existing plan based on feedback
