---
name: check-ci
description: "Use when checking, analyzing, investigating, debugging, triaging, polling, waiting for, rebuilding, or canary-building CI builds, build failures, or test failures. Fixes code and loops until CI is green via a CI analysis API. Works with multiple CI systems."
metadata:
  status: experimental
---

# Check CI Build

Analyze CI build failures, fix code issues, and **loop until CI turns green** via a CI analysis API. Works with multiple CI systems (e.g., Buildkite, Jenkins, GitHub Actions).

**STOP** if required CLI tools (`gh`) are not available.

## CRITICAL: Fix-and-Recheck Loop

This skill operates in a **continuous loop** until CI passes or the retry limit is reached. After every fix attempt, you MUST re-poll CI and check results again. Do NOT stop after a single fix.

```
LOOP (max 5 iterations):
  1. Fetch CI analysis (Step 2)
  2. If RUNNING → poll until complete (Step 3)
  3. If PASSED → report success and EXIT loop
  4. If FAILED → analyze failures, then:
     a. Check change relevance of each failure (Step 5a.1)
     b. For change-related code issues → fix code, build/test locally, commit, push
     c. For unrelated code issues → report to user, do NOT fix
     d. If every remaining failure is unrelated → report and EXIT loop
     e. For flaky tests → rebuild failed parts (Step 4)
     f. For infra issues → report to user and EXIT loop
  5. After fix is pushed or rebuild triggered → go back to step 1
  6. If iteration limit reached → report remaining failures and EXIT loop
```

Track the current iteration count and report it: "CI check attempt 2/5..."

## Step 0: Verify Commit is Pushed

Before checking CI, confirm the current commit exists on the remote.

```bash
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$(git rev-parse --abbrev-ref HEAD) 2>/dev/null || echo "none")
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "HEAD ($LOCAL) not pushed. Run: git push"
fi
```

## Step 1: Identify the Build

### From a PR (most common)

```bash
gh pr view [PR_URL] --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.context == "CI Results") | {context, targetUrl, state}'
```

Save the exact PR URL or number as `TARGET_PR`.

### Fallback: No CI Results check found

Summarize all checks:

```bash
gh pr view [PR_URL] --json statusCheckRollup \
  --jq '.statusCheckRollup[] | "\(.context // .name): \(.state // .conclusion)"'
```

## Step 2: Fetch Analysis

Call your CI analysis API with the build identifier to retrieve:

- `build.state` — `SUCCEEDED`, `FAILED`, `RUNNING`
- `build.web_url` — link to CI console
- `build.jobs[]` — individual jobs with `id`, `step_name`, `state`, `web_url`
- `issues[]` — analyzed build issues with `type`, `normalized_log_snippet`, `step_name`
- `test_results[]` — failed tests with `test_name`, `class_name`, `normalized_stack_trace`

## Step 3: Polling (if build is still running)

```bash
sleep 180  # 3 minutes between polls
# Re-run Step 2
```

## Step 4: Rebuild Failed Parts

Trigger a rebuild of only failed jobs (useful for flaky tests or transient infrastructure failures) via the CI API.

## Step 5: Fix-and-Recheck Loop

### 5a. Analyze Failures

| Category | Indicators | Action |
|---|---|---|
| **Code issue (change-related)** | Failure in files/modules changed by the PR | Fix the code (Step 5b) |
| **Code issue (unrelated)** | Failure in files/modules NOT changed by the PR | Report to user, do NOT auto-fix |
| **Flaky test** | Timeouts, non-deterministic assertions, infra errors in test logs | Rebuild failed parts (Step 4) |
| **Infrastructure** | OOM, network errors, CI agent issues | Report to user and stop |

### 5a.1. Check Change Relevance

Before fixing any code issue, determine if the failure is related to the PR:

1. Get the changed files:
   ```bash
   gh api "repos/$OWNER/$REPO/pulls/$PR_NUMBER/files" --paginate --jq '.[].filename'
   ```
2. For each failure, check if the failing file is in the changed files list or references modified symbols
3. If **UNRELATED**: report it, explain why, suggest rebuild or separate investigation
4. Only proceed to Step 5b for clearly related failures

### 5b. Fix Code Issues (change-related only)

1. **Read the failing code** — understand the test or source file that failed
2. **Make the fix** — edit the relevant source files
3. **Verify locally** — build and/or run the failing tests
4. **Commit and push** the fix

### 5c. Re-poll CI After Fix

After pushing a fix or triggering a rebuild, **loop back**:

1. Wait for the new build to start (sleep 30 seconds, then begin polling)
2. Re-run Steps 1-3 to identify and fetch the new build
3. If **passed** → report success and exit
4. If **failed** → analyze new failures and repeat from 5a

### 5d. Iteration Limits

- **Maximum 5 iterations** of the fix-and-recheck loop
- Track and report: `"🔄 CI check attempt 2/5..."`
- If same failure persists after 2 fix attempts, report to user instead of retrying

## Output Format

After each iteration, report the attempt number, what was fixed, and current status. Separately report unrelated failures. Always include the CI console link.
