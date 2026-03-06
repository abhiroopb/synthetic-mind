# Linear to Execution

> Pick up a Linear issue and execute the work described in it.

## What it does

Linear to Execution reads a Linear issue, parses its structure (context, objectives, acceptance criteria, relevant code paths, dependencies), verifies any blocking issues are resolved, loads referenced source files, creates an execution plan, and begins implementation. It updates the issue status throughout the process and adds progress comments as milestones complete. This skill is optimized to work with issues created by the `plan-to-linear` skill but handles any Linear issue.

## Usage

Use this skill when you want to start working on a specific Linear issue. It's the execution half of the planning-to-execution loop.

**Status:** Experimental

**Trigger phrases:**
- "Work on this issue"
- "Pick up ENG-123"
- "Execute this ticket"
- Pasting a Linear issue URL

## Examples

- `"Pick up ENG-456"` — Fetches the issue, parses acceptance criteria, checks dependencies, creates a task plan, and starts implementation.
- `"Work on this issue: https://linear.app/team/issue/ENG-789/fix-checkout-bug"` — Extracts the issue ID from the URL and begins the full execution workflow.

## Why it was created

Manually reading a Linear issue, understanding its context, and setting up for implementation is tedious. This skill automates the bridge between planning (issues in Linear) and execution (agent doing the work), creating a seamless loop with `plan-to-linear`.
