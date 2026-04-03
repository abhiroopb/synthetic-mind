---
name: monitoring-prs
description: "Monitor all open PRs for new review comments and CI failures, then automatically address them. Use when asked to monitor PRs, watch PRs, auto-respond to PR comments, auto-fix CI, keep PRs green, or babysit open pull requests."
metadata:
  status: experimental
---

# Monitor Open PRs

Continuously monitor all open PRs authored by you. Detect new review comments and CI failures, then automatically address them: respond to comments, fix code, commit, and push.

**STOP** — Before proceeding, verify prerequisites:
- Run `gh auth status` to confirm GitHub CLI is authenticated.
- Run `gh api user --jq '.login'` to confirm user identity.

## Step 1: Poll Open PRs

Run the polling script to find PRs with actionable items. This checks for:
- **New unresolved review comments** (from other authors, since last check)
- **CI failures**

If no PRs have actionable items, report "All PRs are clean ✅" and stop.

## Step 2: Process Each PR

### Priority 1: CI Failures

If CI is failing:

1. **Clone/navigate to the repo** — `cd` to the repo if locally available, otherwise clone it
2. **Checkout the PR branch**: `gh pr checkout <PR_URL>`
3. **Load the `check-ci` skill** to analyze and fix CI failures
4. The check-ci skill will loop: analyze → fix → commit → push → re-check until green or max retries
5. After CI is addressed, continue to comments

### Priority 2: Review Comments

For each unresolved comment thread, evaluate and act:

#### Evaluation Guidelines

- **Is the feedback valid?** Not all comments are correct
- **Bot comments** deserve extra scrutiny — automated tools can be pedantic
- **Is there a better approach** that addresses the underlying concern?

#### Action: Fix Code

If the comment requests a valid code change:

1. Read the file and surrounding context
2. Make the fix
3. Verify the change makes sense in context
4. Commit with a descriptive message referencing the feedback

#### Action: Reply to Comment

After fixing, reply to the comment thread:

```bash
gh api "repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments" \
  -f body="Addressed — updated by AI Agent 🤖" \
  -F in_reply_to=<COMMENT_ID>
```

If you disagree with the suggestion, reply with technical reasoning instead.

#### Action: Resolve Thread

After addressing a comment, resolve the thread via GraphQL:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "<THREAD_ID>"}) {
    thread { id }
  }
}'
```

## Step 3: Push Changes

After all comments on a PR are addressed:

```bash
git push
```

Push once after all fixes for a given PR, not after each individual commit.

## Step 4: Report

```
## PR Monitor Summary

### PR #123 — "Add feature support" (org/repo)
- ✅ CI: Fixed compile error, pushed, CI now green
- ✅ Comments: Addressed 3 review comments, replied to 1 question

### PR #456 — "Update checkout flow" (org/repo)
- ✅ Comments: Addressed 2 review comments
- ⏭️ CI: Already passing
```

## Continuous Mode

If asked to "keep monitoring" or "watch continuously":

1. Run the full poll → process → report cycle
2. Sleep 5 minutes
3. Loop back to Step 1
4. Report only **changes** since last cycle
5. Exit after 1 hour or when the user interrupts

## Important Notes

- **One commit per comment** — don't bundle multiple fixes into one commit
- **Always push** — changes aren't useful until pushed
- **Reply signing** — all replies must end with `— AI Agent 🤖`
- **GraphQL for resolution** — REST API doesn't support resolving threads
- **State tracking** — track last-check timestamps to avoid re-processing old comments
