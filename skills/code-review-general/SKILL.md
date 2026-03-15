---
Skill name: code-review-general
Skill description: Address PR code review feedback. Fetches review comments, helps prioritize human feedback over automated ones, verifies changes, commits, and resolves threads. Use when asked to address code review, fix PR comments, or respond to reviewer feedback.
---

# Code Review

Your job is to address PR feedback.

Make sure to **prioritize human review comments over automated ones**.

## 1. Get review comments

If you have an existing skill for reading PR comments (e.g., one that maintains thread grouping), prefer using that. Otherwise, use these commands:

```bash
# For current branch's PR - get human inline comments
gh api repos/{owner}/{repo}/pulls/$(gh pr view --json number -q .number)/comments --jq '.[] | "File: \(.path)\nLine: \(.line // .original_line)\nAuthor: \(.user.login)\nBody:\n\(.body)\n---"'

# General PR comments
gh pr view --json comments --jq '.comments[] | "Author: \(.author.login)\nCreated: \(.createdAt)\nBody:\n\(.body)\n---"'

# All comments (automated + human)
gh pr view --comments
```

Replace `{owner}/{repo}` with the actual repository (e.g., `myorg/my-service`).

## 2. Address all human comments

Human comments represent architectural decisions and requirements that automated tools may miss.

Note: Some comments may be informational or acknowledgements requiring no code changes. Check if comments are marked as resolved before addressing them - resolved comments don't need action.

## 3. Plan before making changes

First list all the code review comments you're planning on addressing and explain how you want to address them.

- **For simple/straightforward fixes** (e.g., renaming a variable, fixing a typo, adding a missing null check, small style changes): proceed directly without asking the user for confirmation.
- **For complex or ambiguous changes** (e.g., architectural changes, changes with multiple valid approaches, changes that affect behavior): ask the user if your plan is correct and only proceed if the human confirms.

## 4. Verify changes with sub agent (if available)

Use a sub agent to verify changes BEFORE committing, **but only for non-trivial changes**.

- **Skip sub agent verification** for simple, obvious fixes (typos, renames, small style changes, straightforward one-liner fixes).
- **Use sub agent verification** for complex changes, multi-file refactors, or anything where correctness isn't immediately obvious.
- Pass the sub agent the review comments and the changed files for verification
- Do NOT commit until sub agent confirms the changes address the feedback
- Example sub agent task: "Review these changes to verify they address the code review comments: [list comments]. Check files: [list files]"

## 5. Commit and push

When you're done commit and push the changes. If you have an existing skill for creating/managing PRs, prefer using that. Make separate commits if the change is substantial or several minor changes can be committed together with "Addressed code review" and a list of changes in the body.

## 6. Resolve addressed comments

After pushing, resolve the review threads you addressed:

```bash
# List review threads with their IDs and resolved status
PR_NUMBER=$(gh pr view --json number -q .number)
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes { body path }
          }
        }
      }
    }
  }
}' -f owner={OWNER} -f repo={REPO} -F pr=$PR_NUMBER

# Resolve a specific thread by its ID
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}' -f threadId=<THREAD_ID>
```

Replace `{OWNER}` and `{REPO}` with the actual values.

## 7. Wait for CI

When you're done, wait for CI following the check-ci skill.
