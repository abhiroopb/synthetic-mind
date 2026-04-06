---
name: content-sync
description: Check that README and docs/ static site are updated when content changes
severity-default: medium
tools: [Bash, Read, Grep]
---

## Purpose

synthetic-mind requires two things when content is added: (1) the README "Latest Updates" section should be updated, and (2) the `docs/` static site must be synced. This check flags when either is missing.

## Instructions

1. Get the merge base:
   ```
   git merge-base origin/main HEAD
   ```

2. Get the list of changed files:
   ```
   git diff --name-only --diff-filter=ACM <merge_base> HEAD
   ```

3. Categorize changed files:
   - **Thoughts**: files in `thoughts/*.md`
   - **Skills**: files in `skills/*/SKILL.md`
   - **Setup guide**: `amp-setup-guide.md`
   - **Docs site**: files in `docs/`
   - **README**: `README.md`

4. Apply these rules:

### README check
If any content files (thoughts, skills, setup guide) were added or changed, `README.md` should also be in the changed list.

### Static site sync checks

| Content changed | Expected docs/ update |
|---|---|
| New `thoughts/*.md` | New `docs/thoughts/<slug>.html` + card in `docs/thoughts/index.html` + card in `docs/index.html` |
| New `skills/*/SKILL.md` | Card in `docs/skills/index.html` + card in `docs/index.html` |
| `amp-setup-guide.md` | Changes in `docs/setup/index.html` or `docs/memory/index.html` |
| `README.md` | Check if `docs/index.html` needs updating |

5. For each rule violation, report a finding.

## Reporting

For missing README update:
> **[medium]** `README.md` — Latest Updates section may need updating
>
> New content was added: `<list of added content files>`
>
> **Recommendation:** Update the "Latest Updates" section in README.md to reflect the new content.

For missing docs/ sync:
> **[medium]** `docs/` — Static site not synced
>
> Content was added/changed (`<file>`) but the corresponding docs/ page was not updated.
>
> **Expected:** `<which docs/ files should have been created or updated>`
>
> **Recommendation:** Create or update the static site pages to match. See AGENTS.md for the design pattern and template details.

If everything is in sync:
> No content sync issues found.
