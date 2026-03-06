---
name: gdrive
description: Interact with Google Drive, Docs, Sheets, and Slides. Search files, read/write documents, manage sharing, work with spreadsheets, and create presentations.
roles: [frontend]
metadata:
  author: calebm
  version: "0.3.0"
  status: "beta"
---

# Google Drive Skill

Interact with Google Drive, Docs, Sheets, and Slides using a local Python CLI.

## Prerequisites

### Install uv (if needed)

```bash
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Authenticate

```bash
cd {{SKILL_DIR}} && uv run gdrive-cli.py auth login
```

Credentials are stored at `~/.config/gdrive-skill/credentials.json`.

Check status: `uv run gdrive-cli.py auth status`

---

## Quick Reference

All commands output JSON. Run from `{{SKILL_DIR}}`:

```bash
uv run gdrive-cli.py <command> [options]
```

---

## Search & List

```bash
# Search files
uv run gdrive-cli.py search "quarterly report" --limit 10
uv run gdrive-cli.py search "budget" --mime-type "application/vnd.google-apps.spreadsheet"
uv run gdrive-cli.py search "name contains 'OKR'" --raw-query

# List folder contents
uv run gdrive-cli.py list                    # Root of My Drive
uv run gdrive-cli.py list <folder-id>        # Specific folder
```

Search options: `--limit`, `--mime-type`, `--drive-id`, `--parent`, `--raw-query`

---

## File Operations

```bash
# Create new Doc, Sheet, or Slides presentation
uv run gdrive-cli.py create doc "My Document"
uv run gdrive-cli.py create sheet "My Spreadsheet" --parent <folder-id>
uv run gdrive-cli.py create slides "My Presentation"

# Read file content (Docs → text, Sheets → values matrix)
uv run gdrive-cli.py read <file-id>

# Download file
uv run gdrive-cli.py download <file-id> --dest ./downloads/

# Upload a local file
uv run gdrive-cli.py upload ./report.pdf --parent <folder-id>
uv run gdrive-cli.py upload ./data.csv --convert-to sheet  # Convert to Google Sheet

# Export Google Workspace files to other formats
uv run gdrive-cli.py export <doc-id> --format pdf --dest ./output/
uv run gdrive-cli.py export <sheet-id> --format csv --dest ./data.csv
uv run gdrive-cli.py export <sheet-id> --format xlsx --dest ./report.xlsx

# Create folder
uv run gdrive-cli.py mkdir "New Folder" --parent <folder-id>

# Move, rename, copy, trash
uv run gdrive-cli.py move <file-id> --to <folder-id>
uv run gdrive-cli.py rename <file-id> "New Name"
uv run gdrive-cli.py copy <file-id> --name "Copy Name" --parent <folder-id>
uv run gdrive-cli.py trash <file-id>
```

Export formats: `pdf`, `docx`, `txt`, `html`, `xlsx`, `csv`, `pptx`, `odt`, `ods`

---

## Google Docs

### List Tabs

```bash
# List all tabs in a document
uv run gdrive-cli.py docs tabs <doc-id>
```

### Read Document

**When a URL includes `?tab=`, always use `--tab` to fetch that specific tab.** See [references/url-parsing.md](references/url-parsing.md) for URL extraction details.

```bash
# Plain text content (first tab only)
uv run gdrive-cli.py read <doc-id>

# Read a specific tab by ID - USE THIS when URL has ?tab= parameter
uv run gdrive-cli.py read <doc-id> --tab <tab-id>

# Read ALL tabs at once
uv run gdrive-cli.py read <doc-id> --all-tabs

# Full structure with element indices (for batch-update)
uv run gdrive-cli.py docs get <doc-id>
```

**⚠️ Large document detection:** The `read` command truncates documents over ~69KB and prints `⚠️ Output truncated (document too large). Use 'docs get' for full content.` If you see this warning, switch to the structured `docs get` approach described in [references/searching-large-gdocs.md](references/searching-large-gdocs.md).

To list all available tabs: `uv run gdrive-cli.py docs tabs <doc-id>`

### Write Markdown with Formatting

The easiest way to add formatted content is with `docs insert-markdown`, which converts markdown to Google Docs formatting:

```bash
# Append formatted content to end of document (default)
echo "# Summary

**Key findings:**
- First point with [link](https://example.com)
- Second point with \`inline code\`

## Details

1. Numbered item one
2. Numbered item two

\`\`\`
code block here
\`\`\`
" | uv run gdrive-cli.py docs insert-markdown <doc-id>

# Insert at beginning
echo "# Title" | uv run gdrive-cli.py docs insert-markdown <doc-id> --at-index 1

# Insert at a specific position (use 'docs get' to find indices)
echo "## New Section" | uv run gdrive-cli.py docs insert-markdown <doc-id> --at-index 342

# Insert into a specific tab in a multi-tab document
echo "# Tab Content" | uv run gdrive-cli.py docs insert-markdown <doc-id> --tab <tab-id>
```

Supported markdown:
| Markdown | Result |
|----------|--------|
| `# Heading` | HEADING_1 |
| `## Heading` | HEADING_2 |
| `### Heading` | HEADING_3 |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `[text](url)` | Clickable link |
| Bare URLs | Auto-linkified |
| `` `code` `` | Monospace + green text |
| ``` code block ``` | Monospace block |
| `- item` | Bullet list |
| `1. item` | Numbered list |
| `| table |` | Google Docs table |
| `> quote` | Italic block quote |
| `---` | Horizontal rule |

### Raw Batch Update

For advanced formatting, use `docs batch-update` with Google Docs API requests via stdin:

```bash
# Insert text at beginning
echo '{"requests": [{"insertText": {"location": {"index": 1}, "text": "Hello World\n"}}]}' \
  | uv run gdrive-cli.py docs batch-update <doc-id>

# Delete content
echo '{"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": 10}}}]}' \
  | uv run gdrive-cli.py docs batch-update <doc-id>

# Insert table at end
echo '{"requests": [{"insertTable": {"rows": 3, "columns": 2, "endOfSegmentLocation": {"segmentId": ""}}}]}' \
  | uv run gdrive-cli.py docs batch-update <doc-id>
```

Common operations: `insertText`, `deleteContentRange`, `insertTable`, `updateTextStyle`, `updateParagraphStyle`

**For detailed API reference:** See [references/docs-api.md](references/docs-api.md)

---

## Google Sheets

### List Tabs

```bash
# List all tabs/sheets in a spreadsheet
uv run gdrive-cli.py sheets tabs <spreadsheet-id>
```

### Read Values

> **⚠️ `gid=` in URLs:** The `gid` parameter is a random numeric ID, not a tab index. Run `sheets tabs <spreadsheet-id>` first to resolve it to the actual tab name.

```bash
# Read a specific range
uv run gdrive-cli.py sheets read <spreadsheet-id> --range "Sheet1!A1:D10"

# Read an entire tab by name
uv run gdrive-cli.py sheets read <spreadsheet-id> --sheet "Sheet1"

# Read ALL visible tabs at once
uv run gdrive-cli.py sheets read <spreadsheet-id> --all-sheets

# Read a named range
uv run gdrive-cli.py sheets read <spreadsheet-id> --named-range "MyNamedRange"
```

### Write Values

```bash
# Write to range
uv run gdrive-cli.py sheets write <spreadsheet-id> \
  --range "Sheet1!A1" \
  --values '[["Header1", "Header2"], ["val1", "val2"]]'

# Append rows
uv run gdrive-cli.py sheets append <spreadsheet-id> \
  --range "Sheet1" \
  --values '[["new", "row", "data"]]'

# Clear a range (keeps formatting, removes values)
uv run gdrive-cli.py sheets clear <spreadsheet-id> --range "Sheet1!A2:Z"
```

### Get Structure

```bash
# Spreadsheet metadata (sheet IDs, properties)
uv run gdrive-cli.py sheets get <spreadsheet-id>

# Include all cell data
uv run gdrive-cli.py sheets get <spreadsheet-id> --include-grid-data

# List named ranges
uv run gdrive-cli.py sheets named-ranges <spreadsheet-id>
```

### Formatting & Advanced Operations

Use `sheets batch-update` with Google Sheets API requests via stdin:

```bash
# Bold header row
cat << 'EOF' | uv run gdrive-cli.py sheets batch-update <spreadsheet-id>
{
  "requests": [{
    "repeatCell": {
      "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
      "cell": {"userEnteredFormat": {"textFormat": {"bold": true}}},
      "fields": "userEnteredFormat.textFormat.bold"
    }
  }]
}
EOF

# Add dropdown validation
cat << 'EOF' | uv run gdrive-cli.py sheets batch-update <spreadsheet-id>
{
  "requests": [{
    "setDataValidation": {
      "range": {"sheetId": 0, "startRowIndex": 1, "startColumnIndex": 3, "endColumnIndex": 4},
      "rule": {
        "condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": "Yes"}, {"userEnteredValue": "No"}]},
        "showCustomUi": true
      }
    }
  }]
}
EOF

# Alternating row colors
cat << 'EOF' | uv run gdrive-cli.py sheets batch-update <spreadsheet-id>
{
  "requests": [{
    "addBanding": {
      "bandedRange": {
        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 10, "startColumnIndex": 0, "endColumnIndex": 4},
        "rowProperties": {
          "headerColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
          "firstBandColor": {"red": 1, "green": 1, "blue": 1},
          "secondBandColor": {"red": 0.95, "green": 0.95, "blue": 0.95}
        }
      }
    }
  }]
}
EOF
```

Common operations: `repeatCell`, `addBanding`, `setDataValidation`, `mergeCells`, `updateSheetProperties`, `addSheet`, `autoResizeDimensions`

**For detailed API reference:** See [references/sheets-api.md](references/sheets-api.md)

---

## Google Slides

### List Slides

```bash
# List all slides in a presentation
uv run gdrive-cli.py slides list <presentation-id>
```

### Read Content

```bash
# Read text content from all slides
uv run gdrive-cli.py slides read <presentation-id>

# Read a specific slide
uv run gdrive-cli.py slides read <presentation-id> --slide <slide-id>

# Read speaker notes
uv run gdrive-cli.py slides notes <presentation-id>

# Get full presentation structure (for batch-update)
uv run gdrive-cli.py slides get <presentation-id>

# Get a specific page/slide by ID
uv run gdrive-cli.py slides page <presentation-id> <slide-id>
```

### Modify Presentations

```bash
# Add a new slide
uv run gdrive-cli.py slides add-slide <presentation-id> --layout TITLE_AND_BODY

# Add text box to a slide
uv run gdrive-cli.py slides add-text <presentation-id> <slide-id> "Hello World" --x 100 --y 100

# Find and replace text across presentation
uv run gdrive-cli.py slides replace <presentation-id> --find "old text" --replace "new text"

# Add image from URL
uv run gdrive-cli.py slides add-image <presentation-id> <slide-id> "https://example.com/image.png"

# Duplicate a slide
uv run gdrive-cli.py slides duplicate-slide <presentation-id> <slide-id>

# Delete a slide
uv run gdrive-cli.py slides delete-slide <presentation-id> <slide-id>
```

Layouts: `BLANK`, `TITLE`, `TITLE_AND_BODY`, `TITLE_AND_TWO_COLUMNS`, `TITLE_ONLY`, `SECTION_HEADER`, `CAPTION_ONLY`, `BIG_NUMBER`

### Export for Visual Analysis

```bash
# Export as PDF (useful for AI visual analysis of layouts)
uv run gdrive-cli.py slides export-pdf <presentation-id> --dest ./presentation.pdf
```

### Advanced Operations

Use `slides batch-update` with Google Slides API requests via stdin:

```bash
# Create slide with custom content
cat << 'EOF' | uv run gdrive-cli.py slides batch-update <presentation-id>
{
  "requests": [
    {"createSlide": {"insertionIndex": 1, "slideLayoutReference": {"predefinedLayout": "BLANK"}}},
    {"createShape": {
      "objectId": "myTextBox",
      "shapeType": "TEXT_BOX",
      "elementProperties": {
        "pageObjectId": "<slide-id>",
        "size": {"height": {"magnitude": 100, "unit": "PT"}, "width": {"magnitude": 400, "unit": "PT"}},
        "transform": {"scaleX": 1, "scaleY": 1, "translateX": 100, "translateY": 100, "unit": "PT"}
      }
    }},
    {"insertText": {"objectId": "myTextBox", "text": "Hello World"}}
  ]
}
EOF
```

**For detailed API reference:** See [references/slides-api.md](references/slides-api.md)

---

## Revisions

```bash
# List revisions for a file
uv run gdrive-cli.py revisions list <file-id>

# Get details for a specific revision
uv run gdrive-cli.py revisions get <file-id> <revision-id>
```

---

## Sharing

```bash
# List permissions
uv run gdrive-cli.py share list <file-id>

# Share with user
uv run gdrive-cli.py share add <file-id> --email user@example.com --role writer

# Share with anyone (link sharing)
uv run gdrive-cli.py share add <file-id> --type anyone --role reader

# Remove permission
uv run gdrive-cli.py share remove <file-id> <permission-id>
```

Roles: `owner`, `organizer`, `fileOrganizer`, `writer`, `commenter`, `reader`

---

## Comments

```bash
# List comments
uv run gdrive-cli.py comments list <file-id>

# Add comment
uv run gdrive-cli.py comments add <file-id> "This needs review"

# Reply to comment
uv run gdrive-cli.py comments reply <file-id> <comment-id> "Done!"
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Not authenticated" | Run `uv run gdrive-cli.py auth login` |
| "Insufficient permissions" | Run `uv run gdrive-cli.py auth login --force` |

Check auth: `uv run gdrive-cli.py auth status`
