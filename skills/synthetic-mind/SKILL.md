---
name: synthetic-mind
description: Post thoughts, processes, skills, and landing-page updates to the synthetic-mind repo. Use when asked to "post a thought", "document a process", "update synthetic-mind", "publish" something publicly, or keep the markdown and static site versions in sync.
---

# synthetic-mind Publisher

You help publish content to the [synthetic-mind](https://github.com/abhiroopb/synthetic-mind) repository — a public showcase of AI-augmented work.

**Repo location:** `/Users/abhiroop/Development/synthetic-mind`

## Durable Publishing Rules

These rules are mandatory for this repo. Follow them every time.

### Naming and terminology

- Always refer to the system as **the AI PM OS**.
- Always refer to the launcher as the `start-day` command.
- Never write the full script path when public-facing copy is talking about the launcher.

### Static site sync is required

- Any change to `thoughts/*.md` must be mirrored manually to the matching HTML page in `docs/thoughts/` in the same edit.
- New thought posts must also update `docs/thoughts/index.html` and the thoughts section on `docs/index.html`.
- New public skills must update `docs/skills/index.html` and the skills section on `docs/index.html`.
- If a markdown or README change affects public landing-page copy, update the relevant `docs/` page in the same pass.

### Thought post structure

- Use this structure for blog posts:
  1. `#` H1 title
  2. a one-paragraph `## TL;DR`
  3. `## Context`
  4. the rest of the article
- Keep the markdown and HTML versions aligned section-for-section.

### Terminal command styling

- Command callouts should use the `.terminal-callout` component.
- The callout label must be `Typed into Amp`.
- The dollar sign must use `<span class="prompt-sign">$</span>`.
- Prefer showing `start-day` inside these callouts instead of a raw shell path.

### Images, diagrams, and SVGs

- Prefer SVG illustrations for AI PM OS posts and landing pages.
- In markdown, use standard image syntax like `![alt](./images/example.svg)` followed by an italicized caption on the next line.
- In HTML, wrap illustrations in `<figure>`, `<img>`, and `<figcaption>`.
- When SVG text runs long, manually split it across multiple `<text>` elements so it fits article widths cleanly.
- Preserve mobile-friendly layouts. Stack diagrams vertically when side-by-side layouts get cramped.

### AI PM OS landing page pattern

- Preserve the clickable CMUX mockup in `docs/ai-pm-os/index.html`.
- Keep the tab/panel interaction model for workspace previews.
- Keep the installation sequence vertical and Amp-first, with command steps styled as terminal callouts.

## Content Types

| Type | Directory | When to use |
|------|-----------|-------------|
| **Thought** | `/thoughts/` | Observations, experiments, write-ups, lessons learned |
| **Process** | `/processes/` | Repeatable workflows, automation playbooks, how-tos |
| **Skill** | `/skills/` | New public skill showcases (copy from ~/.agents/skills/) |

## Workflow

### 1. Determine Content Type

Based on the user's request, determine which type of content to create:
- "post a thought about..." → Thought
- "document a process for..." → Process
- "add skill X to synthetic-mind" → Skill showcase
- "update synthetic-mind" → Could be any — ask or infer

### 2. Create the Content

#### For Thoughts:
1. Read the template at `/Users/abhiroop/Development/synthetic-mind/thoughts/_template.md`
2. Create a new file: `/Users/abhiroop/Development/synthetic-mind/thoughts/YYYY-MM-DD-slug.md`
   - Use today's date and a URL-friendly slug derived from the title
3. Fill in the frontmatter (title, date, author, tags)
4. Write the content based on the user's input — keep it authentic and concise
5. Mirror the post to `/Users/abhiroop/Development/synthetic-mind/docs/thoughts/YYYY-MM-DD-slug.html`
   - Use the existing article-page structure from current posts
   - Keep the H1, TL;DR, Context, figures, terminal callouts, and related links aligned with the markdown version
6. Update `/Users/abhiroop/Development/synthetic-mind/thoughts/README.md` — add a row to the Posts table
7. Update `/Users/abhiroop/Development/synthetic-mind/docs/thoughts/index.html`
8. Update the thoughts section on `/Users/abhiroop/Development/synthetic-mind/docs/index.html`

#### For Processes:
1. Read the template at `/Users/abhiroop/Development/synthetic-mind/processes/_template.md`
2. Create a new file: `/Users/abhiroop/Development/synthetic-mind/processes/YYYY-MM-DD-slug.md`
3. Fill in the frontmatter (title, date, author, category)
4. Write the content based on the user's input
5. Update `/Users/abhiroop/Development/synthetic-mind/processes/README.md` — add a row to the Catalog table

#### For Skills:
1. Copy the skill folder from `~/.agents/skills/<skill-name>/` to `/Users/abhiroop/Development/synthetic-mind/skills/<skill-name>/`
2. Sanitize: remove any internal URLs, credentials, or company-specific references
3. Update `/Users/abhiroop/Development/synthetic-mind/skills/README.md` — add to the Quick Index table and the appropriate category section
4. Update `/Users/abhiroop/Development/synthetic-mind/docs/skills/index.html` with a matching public card
5. Update the skills section on `/Users/abhiroop/Development/synthetic-mind/docs/index.html`
6. Update the skill count in `/Users/abhiroop/Development/synthetic-mind/README.md`

#### For AI PM OS landing-page updates:
1. Treat `docs/ai-pm-os/index.html` as a crafted marketing page, not a generated dump
2. Preserve the existing structure unless the request explicitly changes it:
   - hero and positioning copy
   - vertical install sequence
   - terminal callouts labeled `Typed into Amp`
   - clickable CMUX mockup with tabs and panels
   - linked related-thought cards
3. When AI PM OS copy changes in thoughts or README content, check whether the landing page also needs matching updates

### 3. Update the Main README

After creating any content, update the "Latest Updates" section in `/Users/abhiroop/Development/synthetic-mind/README.md`:

Replace the content under `## Latest Updates` with a list of the 5 most recent items across all content types, formatted as:

```
## Latest Updates

- **YYYY-MM-DD** — [Title](./path/to/file.md) *(type)*
- **YYYY-MM-DD** — [Title](./path/to/file.md) *(type)*
```

To build this list, scan:
- `/thoughts/*.md` (exclude _template.md and README.md)
- `/processes/*.md` (exclude _template.md and README.md)
- Recent git commits for skill additions

Sort by date descending, show the 5 most recent.

### 4. Git Operations

After all content is created and indexes are updated:

1. Work in `/Users/abhiroop/Development/synthetic-mind`
2. `git add` only the specific files you created or modified
3. Commit and push to `main` automatically with a descriptive message (for example `add thought: <title>`, `update ai pm os landing page`, `update skill: synthetic-mind`)
4. Do not stop after editing. Pushing is part of the workflow.

### 5. Auto-Publish Skills

When a new skill is installed to `~/.agents/skills/`, automatically:

1. Upload the skill to synthetic-mind (follow the Skills workflow in step 2)
2. Create a companion blog post (thought) with:
   - **What it does** — one-paragraph summary of the skill's purpose
   - **How to use it** — invocation patterns and key parameters
   - **Examples** — 2-3 concrete usage examples
   - **Why it was created** — the problem it solves or workflow it improves
3. Update the main README "Latest Updates" section
4. Commit and push everything in one commit

## Writing Guidelines

- **Voice:** First-person, casual but insightful. Write like you're sharing with a peer.
- **Length:** Thoughts should be 200-500 words. Processes can be longer.
- **Format:** Use headers, bullet points, and code blocks liberally.
- **Tags:** Use lowercase, hyphenated tags (e.g., `ai-agents`, `memory-system`, `workflow`)
- **Public AI PM OS copy:** Use "the AI PM OS" consistently in prose.
- **Sanitization:** Never include internal company URLs, secrets, or proprietary details in public content.

## Anti-patterns

- Don't change `thoughts/*.md` without updating the matching `docs/thoughts/*.html`
- Don't use the script path when `start-day` is the right public term
- Don't skip the `Typed into Amp` terminal styling for command showcases
- Don't include internal/company-specific details in public posts
- Don't overwrite existing posts when a new one is warranted
- Don't skip updating the markdown indexes and public `docs/` surfaces
