# synthetic-mind

## Rules

### Static Site Sync

Whenever content is added or changed in this repo (new thoughts, new skills, updated guides, README changes), **also update the static site under `docs/`** to reflect those changes:

- **New thought/blog post** (`thoughts/*.md`) → Create corresponding `docs/thoughts/<slug>.html` using the article template pattern (see existing thought pages). Also add a card entry in `docs/thoughts/index.html` and the thoughts section of `docs/index.html`.
- **New skill** (`skills/*/SKILL.md`) → Add a skill card to both `docs/skills/index.html` and `docs/index.html` (in the skills grid). Use the appropriate `cat-*` category class and `data-cat` attribute.
- **Updated `amp-setup-guide.md`** → Sync changes to `docs/setup/index.html` and `docs/memory/index.html` as appropriate.
- **Updated `README.md`** → Check if any content referenced on `docs/index.html` needs updating.

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
