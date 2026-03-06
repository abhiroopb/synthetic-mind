---
name: gh-pr-read
description: "Reads and summarizes GitHub pull requests using the gh CLI. Use when asked to read, review, summarize, or inspect a PR."
---

# Reading GitHub Pull Requests

Read and inspect GitHub pull requests using the `gh` CLI.

## Capabilities

- View PR details (title, description, status, reviewers, labels)
- Read PR diffs and changed files
- Read PR comments and review threads
- Summarize PR changes

## Workflows

### View a PR by number or URL

```bash
gh pr view <number-or-url> --repo <owner/repo>
```

Add `--json` with field names for structured output:

```bash
gh pr view <number> --repo <owner/repo> --json title,body,state,author,labels,reviewDecision,additions,deletions,changedFiles,commits
```

### View the PR diff

```bash
gh pr diff <number> --repo <owner/repo>
```

### List PR files changed

```bash
gh pr diff <number> --repo <owner/repo> --name-only
```

### Read PR comments and reviews

```bash
gh pr view <number> --repo <owner/repo> --comments
```

### Read review comments (inline code comments)

```bash
gh api repos/<owner>/<repo>/pulls/<number>/comments --paginate
```

### List open PRs

```bash
gh pr list --repo <owner/repo>
```

### List PRs by author or state

```bash
gh pr list --repo <owner/repo> --author <username> --state <open|closed|merged|all>
```

## Tips

- If the user provides a full GitHub PR URL, pass it directly to `gh pr view`.
- Use `--json` for programmatic field access; omit it for human-readable output.
- For large diffs, use `--name-only` first to understand scope, then read specific files.
- Use `gh pr checks <number> --repo <owner/repo>` to see CI status.
