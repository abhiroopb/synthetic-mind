---
Skill name: ralph-loop
Skill description: Iterative work-review loop using two AI models with fresh context per iteration. Use for complex tasks requiring multiple revisions with cross-model validation. Based on Geoffrey Huntley's technique found in Goose.
roles: []
---

# Ralph Loop - Multi-Model Iterative Development

Ralph Loop is an iterative development pattern that keeps AI agents working on tasks until completion using a work-review cycle with fresh context each iteration. It employs two different AI models - one as the worker and another as the reviewer - to provide cross-model validation.

## When to Use

- Complex implementation tasks requiring multiple iterations
- Tasks that benefit from iterative refinement and review
- Situations where you want cross-model validation
- When you need to ensure high quality output through review cycles

## How It Works

1. **Worker Phase**: First model executes the task or addresses feedback
2. **Review Phase**: Second model reviews the work and decides SHIP or REVISE
3. **Iteration**: Loop continues with feedback until approved or max iterations reached
4. **Fresh Context**: Each iteration starts with clean state to avoid context degradation

## Architecture

The skill includes three components:

- `ralph-loop.sh` - Bash orchestration script
- `ralph-work.yaml` - Worker phase instructions (Goose recipe format)
- `ralph-review.yaml` - Reviewer phase instructions (Goose recipe format)

**State Management** (`.goose/ralph/` directory):

- `task.md` - Task description
- `iteration.txt` - Current iteration number
- `work-summary.txt` - Worker's progress summary
- `work-complete.txt` - Task completion signal
- `review-result.txt` - "SHIP" or "REVISE" verdict
- `review-feedback.txt` - Feedback for next iteration
- `.ralph-complete` - Success marker
- `RALPH-BLOCKED.md` - Blocked state indicator

## Usage with Goose

If you have [Goose](https://github.com/block/goose) installed, you can use the original implementation:

### Installation

```bash
# Create recipes directory
mkdir -p ~/.config/goose/recipes

# Copy the files from this skill directory
cp ralph-loop.sh ~/.config/goose/recipes/
cp ralph-work.yaml ~/.config/goose/recipes/
cp ralph-review.yaml ~/.config/goose/recipes/
chmod +x ~/.config/goose/recipes/ralph-loop.sh
```

### Running Ralph Loop

```bash
# Basic usage
./ralph-loop.sh "your task description"

# Or with a task file
./ralph-loop.sh /path/to/task.md
```

### Configuration

Set environment variables to skip interactive prompts:

```bash
export RALPH_WORKER_MODEL="claude-sonnet-4.5"
export RALPH_WORKER_PROVIDER="anthropic"
export RALPH_REVIEWER_MODEL="gpt-4"
export RALPH_REVIEWER_PROVIDER="openai"
export RALPH_MAX_ITERATIONS="10"

./ralph-loop.sh "implement user authentication"
```

## Adapting for Claude Code

While this skill packages the Goose implementation, the pattern can be adapted for Claude Code workflows:

### Manual Iteration Pattern

1. **Define the task** clearly in a file or message
2. **Work phase**: Have Claude Code work on the task
3. **Review phase**: Start a new session (or use a different agent) to review
4. **Iterate**: Continue with feedback until satisfied

### State Files Pattern

Create state files to maintain context between iterations:

```bash
# Initialize
mkdir -p .ralph
echo "Your task description" > .ralph/task.md

# After each work session
echo "Summary of changes made" > .ralph/work-summary.txt

# After review
echo "REVISE" > .ralph/review-result.txt
echo "Specific feedback for next iteration" > .ralph/review-feedback.txt
```

## Key Principles

1. **Fresh Context**: Each iteration starts with minimal, focused context
2. **Cross-Model Review**: Different models provide diverse perspectives
3. **State Files**: Persistence through files, not conversation history
4. **Strict Review**: Reviewers reject incomplete work, errors, failing tests
5. **Iteration Limit**: Prevents infinite loops with configurable maximum

## Cost Considerations

Ralph Loop runs multiple iterations with two models:
- Each iteration = 1 worker session + 1 reviewer session
- Maximum cost = `MAX_ITERATIONS × 2 × avg_cost_per_session`
- Default max iterations: 10

The script includes cost warnings and requires confirmation before execution.

## Files Included

- `ralph-loop.sh` - Main orchestration script (215 lines)
- `ralph-work.yaml` - Worker phase recipe
- `ralph-review.yaml` - Reviewer phase recipe

## Credits

Based on Geoffrey Huntley's Ralph Loop technique for the Goose AI agent framework.

Original implementation: https://block.github.io/goose/docs/tutorials/ralph-loop/

## References

- [Goose Documentation](https://block.github.io/goose/)
- [Ralph Loop Tutorial](https://block.github.io/goose/docs/tutorials/ralph-loop/)
- [Geoffrey Huntley's Original Technique](https://ghuntley.com/)
