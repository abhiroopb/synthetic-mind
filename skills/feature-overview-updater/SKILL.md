---
Skill name: feature-overview-updater
Skill description: Scan the features/ directory and regenerate README index tables with current status, owners, and dates.
---

# Feature Overview Updater

You maintain the feature index tables across the repository. You scan `features/` to discover all feature directories and regenerate the README.md index files with accurate, up-to-date information.

## Workflow

### 1) Scan Features

Read all `overview.md` files under `features/` to collect:
- Feature name (from H1 heading)
- Product area (from parent directory)
- Status (from metadata)
- Owner (from metadata)
- Last Updated date (from metadata)

### 2) Check for Staleness

Flag any features where:
- Last Updated is more than 90 days ago
- Status is "Draft" for more than 60 days
- overview.md is missing (feature dir exists but no overview)

Report these to the user before updating.

### 3) Regenerate Index Tables

Update these files:

**`features/README.md`** — Master index with all features across all areas.

**`features/{area}/README.md`** — Area-specific index for each product area.

Preserve the table format:

```markdown
| Feature | Product Area | Status | Owner | Last Updated |
|---------|-------------|--------|-------|--------------|
| [Feature Name](./path/) | Area | Status | Owner | YYYY-MM-DD |
```

### 4) Report Changes

Summarize what changed:
- New features added to index
- Status changes detected
- Stale features flagged
- Any missing overview.md files

## Anti-patterns

- Don't modify feature documents themselves — only update README index files
- Don't guess metadata — if overview.md is missing, flag it rather than inventing values
- Don't remove features from the index — if a directory exists, it should be listed
