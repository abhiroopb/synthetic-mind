# RPI Implement

> Execute approved RPI implementation plans phase by phase with verification at each step.

## What it does

RPI Implement is the execution phase of the RPI (Research, Plan, Implement) methodology. It takes an approved implementation plan and executes it phase by phase, following the plan's intent while adapting to what it finds in the codebase. After each phase, it runs automated verification checks, updates plan checkboxes, and pauses for manual verification before proceeding. It can also resume partially completed plans by picking up from the first unchecked item.

## Usage

Invoke after you have an approved RPI plan and are ready to start implementing. Provide the path to the plan file.

**Trigger phrases:**
- "Implement this plan"
- "Execute the RPI plan"
- "Start implementing phase 1"
- "Resume implementation from where we left off"

## Examples

- `"Implement the plan at thoughts/shared/plans/2025-03-01-checkout-refactor.md"`
- `"Execute phase 2 of the implementation plan"`
- `"Resume the RPI implementation"`

## Why it was created

Complex implementation plans need disciplined phase-by-phase execution with verification at each step. Doing this manually risks skipping steps or losing track of progress. This skill provides structured execution with automated checks and clear pause points for human review.
