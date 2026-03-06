# Git Hygiene (MANDATORY — DO THIS FIRST)

Immediately after verifying repos exist and BEFORE doing any other work (including reading files, searching, or grepping), reset every repo that this phase will touch to a clean latest main. This is critical because the repos may be on leftover branches from previous runs, which means searches and reads will return stale or incorrect results.

For the Proto Phase, always reset `~/Development/java` upfront. If the plan includes OAuth operations, also reset `~/Development/go/src/app/up`. If the plan includes display permission operations, also reset `~/Development/permissions-config`.

For the Config Phase, reset ALL repos: `java`, `go/src/app/up`, `permissions-config`, `roster-rails`, `dashboard`.

Before running any reset commands, check each repo for uncommitted changes:

```bash
cd REPO_PATH
git status --porcelain
```

If any repos have uncommitted changes, list which repos are dirty and summarize what's there (e.g., "2 modified files, 1 untracked file"). Then ask the user: "I need to reset these repos to clean latest main before proceeding. I can stash the changes automatically, or you can handle them yourself (commit, stash, discard, etc.) and let me know when you're ready. What would you prefer?"

Wait for the user's response before touching any repo. If the user wants to handle it themselves, wait for them to confirm all repos are clean. If no repos have changes, proceed silently.

For each repo, run:

```bash
cd REPO_PATH
git stash --include-untracked -q 2>/dev/null
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
git checkout -q "$DEFAULT_BRANCH"
git reset --hard "origin/$DEFAULT_BRANCH" -q
git clean -fd -q
git pull -q
```

This does a hard reset to match the remote exactly and removes untracked files. Do NOT use `git clean -fdx` — the `-x` flag deletes gitignored files like IDE configuration (e.g., `.ijwb/`, `.idea/`), which cannot be recovered from the stash and will break the user's IDE setup.

The `java` and `go` monorepos use `master`. Other repos may use `main`. The command above detects the correct default branch automatically — never hardcode `main` or `master`.

Do NOT skip this step. Do NOT defer it until you're about to edit files. Do it now, before anything else.
