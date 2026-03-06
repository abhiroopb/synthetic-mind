# RPI Plan

> Create detailed, phased implementation plans grounded in codebase reality with measurable success criteria.

## What it does

RPI Plan is the planning phase of the RPI (Research, Plan, Implement) methodology. It takes research findings and requirements, investigates the codebase to understand current state, aligns on approach through interactive discussion, and produces a detailed implementation plan. Plans are structured into phases with specific file changes, code snippets, and automated success criteria. The output is a markdown file designed to be directly executable by the `rpi-implement` skill.

## Usage

Invoke after completing RPI research when you're ready to design the implementation approach. The skill is interactive — it gathers context, presents design options, and aligns on approach before writing the full plan.

**Trigger phrases:**
- "Create an implementation plan"
- "Plan the changes for this feature"
- "Design the approach for this refactor"
- "Draft an RPI plan"

## Examples

- `"Create an implementation plan for the checkout refactor based on the research doc"`
- `"Plan the migration from v1 to v2 of the payments API"`
- `"Design a phased approach for adding offline support"`

## Why it was created

Jumping straight from understanding code to implementing changes often leads to missed edge cases and scope creep. This skill produces thorough, interactive plans with explicit phases, success criteria, and out-of-scope declarations — reducing surprises during implementation.
