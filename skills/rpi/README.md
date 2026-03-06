# RPI

> Research, Plan, Implement — a phased methodology for complex codebase changes that manages context by breaking work into focused sessions.

## What it does

RPI is a workflow framework that breaks complex development tasks into four phases: Research (understand the code), Plan (design the change), Implement (execute the plan), and Iterate (adjust based on feedback). Each phase runs in its own fresh session with artifacts (research docs, plan files) bridging between them. This router skill determines which phase you need and loads the corresponding sub-skill.

## Usage

Invoke when you have a complex task that benefits from structured decomposition — large refactors, migrations, new features in unfamiliar code, or multi-step changes. Tell the skill what you need and it will route to the right phase.

**Trigger phrases:**
- "RPI this task"
- "Break down this complex change"
- "I need a structured approach to this refactor"
- "Phase this migration"

## Examples

- `"RPI: I need to refactor the checkout flow to support offline mode"`
- `"Use the RPI approach to plan this database migration"`
- `"I have research done, now I need to plan the implementation"`

## Why it was created

Complex codebase changes fail when you try to research, plan, and implement in a single session — context degrades and important details get lost. RPI enforces phase separation so each step gets full attention, with documented artifacts carrying knowledge forward.
