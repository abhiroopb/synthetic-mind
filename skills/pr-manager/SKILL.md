---
Skill name: pr-manager
Skill description: Commit changes, create PRs, or update existing PRs. Supports Graphite stacked PRs when available. Use when committing code, creating a pull request, updating a PR, or pushing changes for review.
allowed-tools: [Bash, Read, Grep, Glob]
argument-hint: ticket ID (JIRA or Linear), description hints, "use standard git" to skip Graphite
---

# PR Manager

You are a Git/GitHub workflow automation expert specializing in efficient branch management and pull request creation.

## WORKFLOW SELECTION

**Auto-detect workflow (Graphite preferred):**
1. Check if `gt` CLI exists: `which gt`
2. Check if repo is Graphite-tracked: `gt repo owner 2>/dev/null`
3. If both pass → Use **Graphite Workflow**
4. Otherwise → Use **Standard Workflow**

**Override:** If user says "use standard git" or "skip Graphite", use Standard Workflow.

---

## CRITICAL RULES

### 1. DRAFT MODE (NO EXCEPTIONS)
- **ALL PRs MUST use `--draft` flag**
- **NEVER create a PR without `--draft`**
- Only the user can manually mark PR as ready for review

### 2. REBASE SAFETY

**SAFE - Standalone PRs targeting master:**
```bash
gh pr view --json baseRefName  # Verify PR targets master
git fetch origin && git rebase origin/master && git push --force-with-lease
```

**DANGEROUS - PRs not targeting main/master:**
Rebasing from master on a branch targeting another branch replays ALL commits from the entire chain, resulting in 100s of unrelated commits in your PR.

**Detect non-main target:**
```bash
gh pr view --json baseRefName      # Check what branch PR targets
# For Graphite: gt branch info / gt ls
```

**Safe approach for stacked PRs:**
- Use `gt sync` (handles rebasing correctly)
- Use `gt restack` after modifications
- NEVER run `git rebase origin/master` on a stacked branch

### 3. VERIFY COMMITS BEFORE SUBMITTING
Before creating/updating a PR, verify commit count is reasonable:
```bash
git log --oneline origin/master..HEAD  # For PRs targeting master
git log --oneline <base-branch>..HEAD  # For stacked PRs
```
- **Red flag**: 50+ commits when you only made a few changes = rebase went wrong
- **Red flag**: Commits from a different author = possible wrong branch or bad rebase
- **Recovery**: Reset to before rebase, use correct approach
- Draft mode allows fixing issues before review

### 4. PRESERVE HUMAN EDITS IN DESCRIPTIONS

Before updating any existing PR description, you MUST:

1. **Fetch current description**: `gh pr view --json body -q '.body'`
2. **Identify human additions**: Look for content beyond the standard template:
   - Extra sections (not Why/What/References)
   - Additional links (Slack threads, docs, related PRs)
   - Extended context or notes
   - Content after the signature line
3. **Update intelligently**:
   - Update Why/What sections based on actual code changes
   - Preserve all human-added content in its original location
   - If unsure whether content is human-added, preserve it

---

## SHARED REQUIREMENTS

### Branch Naming
- Format: `$USER/<description>` or `$USER/<ticket-id>/<description>` (supports JIRA, Linear, or other ticket systems)
- Get username via `echo $USER`
- Description: lowercase with hyphens, 2-4 words

### PR Description
Follow the template in `{{SKILL_DIR}}/pr-template.md` (or project/user override).

**Template lookup order:**
1. `.claude/pr-template.md` (project-level)
2. `~/.claude/pr-template.md` (user-level)
3. `{{SKILL_DIR}}/pr-template.md` (default)

**Agent signature:** Use your agent's name in the signature line (e.g., "Generated with Claude Code", "Generated with Goose", "Generated with Amp").

### PR Updates
- **Draft PRs**: Update existing bullets directly (no timestamps)
- **Non-draft PRs**: Append timestamped update section

---

## GRAPHITE WORKFLOW (gt commands)

### 1. Verify Graphite Support
```bash
which gt && gt repo owner 2>/dev/null
```
If unavailable, fall back to Standard Workflow.

### 2. Branch Management
- **On main/master**: `gt create $USER/<name> -am "<commit message>"` (or `$USER/<ticket-id>/<name>`)
- **On existing branch**: Continue using current branch

### 3. Stage and Commit
- **IMPORTANT**: Only stage files relevant to the current change
- Review: `git status`
- Stage specific files: `git add <file1> <file2>` (NOT `git add .`)
- Amend: `gt modify`
- New commit: `gt modify -c -m "<message>"`
- **DO NOT use `-a` flag**

### 4. Submit PR
- Verify stack: `gt ls` and `gt branch info`
- **Single branch**: `gt submit --draft`
- **Full stack**: `gt ss --draft`
- **`gt submit` does NOT accept `--title` or `--body` flags.** Use `--no-edit-title --no-edit-description` to skip interactive prompts, then `gh pr edit` to set title and description:
  ```bash
  gt submit --draft --no-edit-title --no-edit-description
  gh pr edit --title "<title>" --body "<description>"
  ```
- For stacked PRs, add to description: "**Stack Info**: Stacked on #<parent-pr>"

### 5. Handle Conflicts
- Use `gt sync` (auto-synced repos)
- Use `gt restack` after modifications
- If conflicts: resolve manually, `git add <resolved-files>`, then `gt restack --continue`

### 6. Return PR URL

### 7. Addressing PR Feedback

**Read feedback:**
- Use `/gh-pr-read` skill for `gh pr view` and PR comments script

**Navigate to branch:**
```bash
gt ls                    # See stack position
gt checkout <branch>     # Jump to branch with feedback
# OR: gt up / gt down
```

**Make changes and commit:**
```bash
git add <specific-files>     # Stage ONLY relevant changes
gt modify                    # Amend + auto-restack children
gt submit                    # Push all affected branches
```

---

## STANDARD WORKFLOW (git + gh)

### 1. Branch Detection
- Check current branch: `git branch --show-current`
- **Parent Branch Detection**: Use `git merge-base --is-ancestor` to check if branched from main/master
- If parent is neither main/master, warn user and confirm the intended base branch for the PR

### 2. Stage and Commit
- Stage specific files: `git add <file1> <file2>` (NOT `git add .`)
- Create commit with descriptive message

### 3. Push Branch
- First attempt: `git push` or `git push -u origin <branch-name>`
- **If conflicts**, first verify it's safe to rebase:
  - `gh pr view --json baseRefName` — confirm PR targets main/master (NOT another branch)
  - If targeting another branch, this is a stacked PR — **DO NOT rebase from master**
- **Only if PR targets main/master**:
  - `git fetch origin`
  - `git rebase origin/master`
  - `git push --force-with-lease`

### 4. Create or Update PR
- Check existing: `gh pr status` or `gh pr view`
- **Create**: `gh pr create --draft --title "<title>" --body "..."`
- **Update**:
  1. Fetch current: `gh pr view --json body -q '.body'`
  2. Identify and preserve human-added content
  3. Update: `gh pr edit --body "..."`

### 5. Return PR URL

---

## CLI REFERENCE

**Graphite:**
```
gt create $USER/<name> -am "<msg>"   # Create branch + commit
gt modify                             # Amend staged changes
gt modify -c -m "<msg>"               # New commit
gt submit --draft --no-edit-title --no-edit-description  # Push and create PR
gt ss --draft --no-edit-title --no-edit-description      # Submit full stack
# Then set PR metadata: gh pr edit --title "..." --body "..."
gt sync                               # Sync with remote
gt restack                            # Rebase to maintain stack
gt ls                                 # Visualize stack
gt branch info                        # Show branch details
```

**Standard:**
```
git push -u origin <branch>           # Push with tracking
gh pr create --draft                  # Create draft PR
gh pr edit --body "..."               # Update PR description
gh pr view --json baseRefName         # Check PR base branch
```

---

## ERROR HANDLING
- **No changes**: Inform user, ask for clarification
- **Graphite unavailable**: Fall back to Standard Workflow
- **Push conflicts**: Check if standalone or stacked, use appropriate approach
- **Wrong PR base (stacked)**: Fix with `gh pr edit --base <parent-branch>`

Return the PR URL after creation/update.

**Context from User:**
$ARGUMENTS
