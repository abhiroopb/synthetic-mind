# Address PR Comments

> Automatically address, commit, and resolve GitHub pull request review comments.

## What it does

Fetches unresolved PR review comments, critically evaluates each piece of feedback (distinguishing human insight from automated noise), makes the requested code changes, and commits per-comment. After changes are pushed, it resolves the review threads via GitHub's GraphQL API — but only after explicit user confirmation.

## Usage

Invoke when you want to address PR review feedback, fix code review comments, or resolve PR threads. The skill auto-detects the current repo and PR from your branch.

Trigger phrases:
- "Address the PR comments"
- "Fix the review feedback"
- "Resolve the PR threads"

## Examples

- "Address the PR comments on my current branch"
- "Go through the unresolved review comments and fix them"
- "There's feedback on my PR — can you address it and resolve the threads?"

## Why it was created

Manually reading, addressing, committing, and resolving PR review threads is tedious and context-switch-heavy. This skill automates the mechanical parts while keeping the human in the loop for judgment calls.
