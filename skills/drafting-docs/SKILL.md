---
name: drafting-docs
description: "Draft and format Google Docs with consistent styling. Use when creating, drafting, writing, formatting, building, composing, or producing Google Docs, strategy docs, PRDs, reports, summaries, or any document output."
depends-on: [gdrive]
---

# Drafting Docs

Create Google Docs with consistent styling based on a template. All document output goes to Google Docs, never local files.

## Workflow

1. **Copy the template:** Use the Google Drive CLI to copy your template doc
2. **Clear template placeholder content** using batch updates (delete everything after the context box)
3. **Update the title** with the actual document title
4. **Leave the context box as-is** — the template has dropdown chips for Document Status, Author, Last Updated, and Related Docs. Do NOT replace these with plain text.
5. **Insert content** using the `insert-markdown` command after the context box
6. **Apply named styles** via batch updates to match the template's heading hierarchy
7. **Insert horizontal rules** between major sections (see Horizontal Rules below)
8. **Share the link** with the user

## Document Structure

Every doc follows this order:

```
Title (TITLE style)
[blank line]
Context Box (1×1 table)
Horizontal Rule
Section Heading (HEADING_1)
Body text...
Horizontal Rule
Section Heading (HEADING_1)
Body text with subsection headings (HEADING_2, HEADING_3)
...
```

## Context Box

A 1-row, 1-column table immediately after the title. **Never skip this.**

**Cell styling:**
- Background: `#F3F3F3` (RGB `0.953, 0.953, 0.953`)
- Padding: 18pt all sides
- Borders: invisible (white color, 0pt width)
- Content alignment: TOP

**Fields (each on its own line):**
- **Document Status:** (dropdown chip — do not replace)
- **Author:** (dropdown chip — do not replace)
- **Last Updated:** (dropdown chip — do not replace)
- **Related Docs:** (dropdown chip — do not replace)

Only the field labels (before the colon) are bold.

## Named Styles

| Level | Named Style | Font | Size | Color | Notes |
|-------|------------|------|------|-------|-------|
| Title | `TITLE` | Inter Tight (500 weight) | 28pt | `#1B2126` | lineSpacing 100, spaceBelow 5pt |
| H1 | `HEADING_1` | Inter (inherited) | 20pt | `#1B2126` | spaceAbove 24pt, spaceBelow 6pt |
| H2 | `HEADING_2` | Inter (inherited) | 16pt | `#0066FF` (blue) | spaceAbove 20pt, spaceBelow 15pt |
| H3 | `HEADING_3` | Inter (inherited) | 14pt | `#434343` (dark gray) | spaceAbove 16pt, spaceBelow 4pt |
| Body | `NORMAL_TEXT` | Inter (400 weight) | 11pt | black | lineSpacing 115 |

## Horizontal Rules

Use paragraph bottom borders for section dividers. **Never use `────────────────────` text characters.**

Insert an empty paragraph with border styling:

```json
{
  "updateParagraphStyle": {
    "range": {"startIndex": "START", "endIndex": "END"},
    "paragraphStyle": {
      "borderBottom": {
        "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
        "width": {"magnitude": 1, "unit": "PT"},
        "padding": {"magnitude": 12, "unit": "PT"},
        "dashStyle": "SOLID"
      },
      "spaceBelow": {"magnitude": 12, "unit": "PT"}
    },
    "fields": "borderBottom,spaceBelow"
  }
}
```

Place horizontal rules:
- After the context box (before the first H1)
- Between each major H1 section

## Table Styling

**Header row:** Black background, white bold text, left-aligned
**Body rows:** White background, black text, normal weight
**All cells:** 1pt solid black borders, TOP alignment, text wrap enabled

## Writing Voice

- Sentence case, casual and direct, properly capitalized
- Avoid emdashes (—) unless they fit organically; prefer colons, commas, or separate sentences
- Tables for comparisons, bullets for lists
- Concise: say it in fewer words when possible
- All links must be clickable (never raw URLs without hyperlinks)

## Batch Update Order

Process deletions and insertions from **end of document to beginning** to prevent index shifts. Always re-fetch indices if unsure.

## Quick Start Example

```bash
# 1. Copy template
gdrive-cli copy <template-doc-id> --name "My New Doc"

# 2. Read the copy to get its ID and current indices
gdrive-cli read <new-doc-id>

# 3. Clear placeholder content
# 4. Update title text
# 5. Leave context box dropdowns as-is
# 6. Insert markdown content
echo "## Section 1\n\nContent here\n\n## Section 2\n\nMore content" | \
  gdrive-cli docs insert-markdown <new-doc-id> --at-index <after-context-box>

# 7. Insert horizontal rules between sections
# 8. Share the link
```
