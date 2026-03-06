# Ralph Loop

> Iterative work-review loop using two AI models with fresh context per iteration for cross-model validation.

## What it does

Ralph Loop is an iterative development pattern that uses two different AI models — one as a worker and another as a reviewer — to complete complex tasks through repeated work-review cycles. Each iteration starts with fresh context to avoid degradation, and state is persisted through files rather than conversation history. The loop continues until the reviewer approves the work or a maximum iteration count is reached.

## Usage

Invoke for complex implementation tasks that benefit from iterative refinement and cross-model review. Originally designed for the Goose AI framework but can be adapted for other agent workflows.

**Trigger phrases:**
- "Use ralph loop for this task"
- "Run this through a work-review cycle"
- "Iterate on this with cross-model validation"

## Examples

- `"Use ralph loop to implement user authentication"`
- `"Run ralph-loop.sh 'refactor the payment module'"`
- `"Set up a work-review loop with Claude as worker and GPT-4 as reviewer"`

## Why it was created

Complex tasks often need multiple revision passes, and a single model can develop blind spots within a long session. Ralph Loop provides structured iteration with cross-model review, ensuring higher quality output through diverse perspectives and fresh context each round.
