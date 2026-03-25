---
name: synthetic-mind
description: Post thoughts, processes, and updates to the synthetic-mind repo. Use when asked to "post a thought", "document a process", "update synthetic-mind", or "showcase" something.
---

# synthetic-mind Publisher

You help publish content to the [synthetic-mind](https://github.com/abhiroopb/synthetic-mind) repository — a public showcase of AI-augmented work.

**Repo location:** `/Users/abhiroop/Development/synthetic-mind`

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
5. Update `/Users/abhiroop/Development/synthetic-mind/thoughts/README.md` — add a row to the Posts table

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
4. Update the skill count in `/Users/abhiroop/Development/synthetic-mind/README.md`

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

1. `cd /Users/abhiroop/Development/synthetic-mind`
2. `git add` only the specific files you created/modified
3. **Commit and push automatically** — use a descriptive commit message (e.g., `add thought: <title>`, `add skill: <name>`, `add process: <title>`)
4. Do NOT ask before committing — always auto-commit and auto-push

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
- **Sanitization:** Never include internal company URLs, secrets, or proprietary details in public content.

## Anti-patterns

- Don't skip committing and pushing — always auto-commit after changes
- Don't include internal/company-specific details in public posts
- Don't overwrite existing posts — create new ones
- Don't skip updating the index READMEs
