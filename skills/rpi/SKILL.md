---
name: rpi
description: RPI (Research, Plan, Implement) methodology for complex multi-step tasks. Use when the user mentions "rpi", wants to decompose, phase, structure, organize, or break down a complex task, or needs a structured approach to large codebase changes, migrations, or refactors. Routes to the appropriate RPI phase skill.
---

# RPI — Research, Plan, Implement

A workflow framework for complex codebase changes that manages context by breaking work into phases. Each phase runs in its own fresh session, with artifacts bridging between them.

## Phases

| Phase | Skill | When to use | Output |
|---|---|---|---|
| **Research** | `rpi-research` | Understand how existing code works | `thoughts/shared/research/YYYY-MM-DD-description.md` |
| **Plan** | `rpi-plan` | Design the change with phases and success criteria | `thoughts/shared/plans/YYYY-MM-DD-description.md` |
| **Implement** | `rpi-implement` | Execute an approved plan phase by phase | Working code with plan checkboxes updated |
| **Iterate** | `rpi-iterate` | Adjust an existing plan based on feedback | Updated plan file |

## How to proceed

Determine which phase the user needs based on their request, then **load the corresponding skill**:

- If they want to **understand code** → load `rpi-research`
- If they have research and want to **create a plan** → load `rpi-plan`
- If they have an **approved plan** to execute → load `rpi-implement`
- If they need to **update an existing plan** → load `rpi-iterate`
- If **unclear**, ask which phase they need

## Key principle

**One goal per session.** Don't research, plan, and implement in the same session. Each phase should be its own focused session to maintain context quality. The research doc or plan file carries context forward.

## Related Skills

- `rpi-research` — Research phase
- `rpi-plan` — Planning phase
- `rpi-implement` — Implementation phase
- `rpi-iterate` — Iteration phase
