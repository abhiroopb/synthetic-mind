# Code Review General

> Address PR code review feedback — fetch comments, make changes, commit, and resolve threads.

## What it does

Fetches review comments from a pull request, prioritizes human feedback over automated bot comments, plans and implements the requested changes, and commits them. For simple fixes it proceeds directly; for complex or ambiguous changes it confirms the plan first. After pushing, it resolves addressed review threads via GitHub's GraphQL API and waits for CI to pass.

## Usage

Use when you need to address code review feedback on a PR. Works with the current branch's open PR.

Trigger phrases:
- "Address the code review"
- "Fix the PR comments"
- "Respond to the reviewer feedback"

## Examples

- "Address all the human review comments on my PR"
- "Fix the code review feedback and push"
- "Go through the PR comments, fix what's needed, and resolve the threads"

## Why it was created

Addressing code review feedback involves reading comments, making changes across files, committing, pushing, and resolving threads — a multi-step process that's easy to automate while keeping judgment calls with the developer.
