# synthetic-mind

## Rules

### Static Site Sync

Whenever content is added or changed in this repo (new thoughts, new skills, updated guides, README changes), **automatically update the static site** by running:

```bash
python3 docs/_generate_skill_pages.py
```

This script generates individual skill pages and updates the index from existing markdown files. Avoid manual HTML editing in the `docs/` folder for these items to prevent layout drift.

### Auto-Push

Always commit and push changes to `main` automatically — never ask for confirmation. Use a descriptive commit message. The repo bypasses branch protection for direct pushes.

### Design Pattern

All sub-pages under `docs/` follow this pattern:
- Link to `../style.css` for shared styles
- Google Fonts: Inter + JetBrains Mono
- Fixed nav: brand "🧠 synthetic-mind" → `../`, links for Skills, Memory, Setup, Thoughts, GitHub icon
- Dark theme: `#0a0a0a` background
- `.page-content` wrapper for article pages (max-width 800px)
- Footer: "Built by Abhi Basu · View on GitHub · Powered by Amp"
- Mark the current section's nav link with `class="active"`
