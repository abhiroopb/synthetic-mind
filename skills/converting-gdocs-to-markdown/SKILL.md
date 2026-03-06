---
name: converting-gdocs-to-markdown
description: Convert Google Docs to markdown files for the repository. Use when importing documentation from Google Drive or converting gdocs to local markdown.
---

# Converting Google Docs to Markdown

Convert Google Docs to markdown files using the gdrive skill.

## Prerequisites

The gdrive skill must be installed and authenticated. Install it if needed:

```bash
sq agents skills add gdrive
```

Then load it:

```
Load the gdrive skill
```

If not authenticated, run from the gdrive skill directory:

```bash
uv run gdrive-cli.py auth login
```

## Workflow

### 1. Get the Document ID

Extract the document ID from the Google Docs URL:
- URL: `https://docs.google.com/document/d/DOCUMENT_ID/edit`
- The document ID is the long string between `/d/` and `/edit`

### 2. Read the Document Content

From the gdrive skill directory ({{SKILL_DIR}} when gdrive is loaded):

```bash
uv run gdrive-cli.py read <document-id>
```

If the document has tabs (URL contains `?tab=`):

```bash
uv run gdrive-cli.py read <document-id> --tab <tab-id>
```

To read all tabs:

```bash
uv run gdrive-cli.py read <document-id> --all-tabs
```

### 3. Convert to Markdown

The gdrive skill returns plain text. Convert to proper markdown conforming to the templates in AGENTS.md §7:

1. Add appropriate headers (`#`, `##`, `###`)
2. Format lists with `-` or `1.`
3. Add bold (`**text**`) and italic (`*text*`) where appropriate
4. Convert tables to markdown table format
5. Add code blocks with triple backticks
6. **Ensure all required template sections are present** — refer to AGENTS.md §7.1 for PRDs, §7.4 for research, §7.3 for decisions

### 4. Save to Repository

Save to the appropriate directory following the `<scope>/<feature>` convention:
- PRDs → `requirements/<scope>/<feature>/PRD.md`
- Research → `requirements/<scope>/<feature>/RESEARCH.md`
- Decisions → `requirements/<scope>/<feature>/DECISIONS.md`

Use kebab-case for all path segments.

## Tips

- Use `--all-tabs` to get complete documents with multiple sections
- Check document structure with `uv run gdrive-cli.py docs get <doc-id>` for complex formatting
- For documents with images, download them separately and reference locally
- After conversion, run the validation checks from AGENTS.md §5
