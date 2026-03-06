# Google Docs API Reference

This reference covers advanced document manipulation using the `docs batch-update` command.

## Understanding Document Structure

Before editing, get the document structure to find element indices:

```bash
uv run gdrive-cli.py docs get <doc-id>
```

The response includes:
- `body.content[]` - Array of structural elements (paragraphs, tables, etc.)
- Each element has `startIndex` and `endIndex` properties
- Text is inserted at an index position (1 = start of document body)

## Batch Update Basics

Send requests via stdin as JSON:

```bash
echo '{"requests": [...]}' | uv run gdrive-cli.py docs batch-update <doc-id>
```

Multiple requests execute in order. Get indices from `docs get` first.

---

## Text Operations

### Insert Text

```json
{
  "requests": [{
    "insertText": {
      "location": {"index": 1},
      "text": "Hello World\n"
    }
  }]
}
```

Insert at specific location (indices shift after insertion):
```json
{
  "requests": [{
    "insertText": {
      "location": {"index": 25},
      "text": " inserted "
    }
  }]
}
```

### Delete Text

```json
{
  "requests": [{
    "deleteContentRange": {
      "range": {
        "startIndex": 1,
        "endIndex": 15
      }
    }
  }]
}
```

### Replace Text (Find and Replace)

```json
{
  "requests": [{
    "replaceAllText": {
      "containsText": {
        "text": "old text",
        "matchCase": false
      },
      "replaceText": "new text"
    }
  }]
}
```

---

## Text Formatting

### Bold, Italic, Underline

```json
{
  "requests": [{
    "updateTextStyle": {
      "range": {
        "startIndex": 1,
        "endIndex": 12
      },
      "textStyle": {
        "bold": true,
        "italic": true,
        "underline": true
      },
      "fields": "bold,italic,underline"
    }
  }]
}
```

### Font Size and Color

```json
{
  "requests": [{
    "updateTextStyle": {
      "range": {"startIndex": 1, "endIndex": 20},
      "textStyle": {
        "fontSize": {"magnitude": 14, "unit": "PT"},
        "foregroundColor": {
          "color": {"rgbColor": {"red": 0.2, "green": 0.4, "blue": 0.8}}
        }
      },
      "fields": "fontSize,foregroundColor"
    }
  }]
}
```

### Add Hyperlink

```json
{
  "requests": [{
    "updateTextStyle": {
      "range": {"startIndex": 1, "endIndex": 10},
      "textStyle": {
        "link": {"url": "https://example.com"}
      },
      "fields": "link"
    }
  }]
}
```

---

## Paragraph Formatting

### Headings

```json
{
  "requests": [{
    "updateParagraphStyle": {
      "range": {"startIndex": 1, "endIndex": 20},
      "paragraphStyle": {
        "namedStyleType": "HEADING_1"
      },
      "fields": "namedStyleType"
    }
  }]
}
```

Named styles: `NORMAL_TEXT`, `HEADING_1` through `HEADING_6`, `TITLE`, `SUBTITLE`

### Alignment

```json
{
  "requests": [{
    "updateParagraphStyle": {
      "range": {"startIndex": 1, "endIndex": 50},
      "paragraphStyle": {
        "alignment": "CENTER"
      },
      "fields": "alignment"
    }
  }]
}
```

Alignments: `START`, `CENTER`, `END`, `JUSTIFIED`

### Indentation and Spacing

```json
{
  "requests": [{
    "updateParagraphStyle": {
      "range": {"startIndex": 1, "endIndex": 100},
      "paragraphStyle": {
        "indentFirstLine": {"magnitude": 36, "unit": "PT"},
        "indentStart": {"magnitude": 18, "unit": "PT"},
        "spaceAbove": {"magnitude": 12, "unit": "PT"},
        "spaceBelow": {"magnitude": 12, "unit": "PT"},
        "lineSpacing": 150
      },
      "fields": "indentFirstLine,indentStart,spaceAbove,spaceBelow,lineSpacing"
    }
  }]
}
```

---

## Lists

### Create Bulleted List

```json
{
  "requests": [{
    "createParagraphBullets": {
      "range": {"startIndex": 1, "endIndex": 50},
      "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
    }
  }]
}
```

Bullet presets:
- `BULLET_DISC_CIRCLE_SQUARE`
- `BULLET_DIAMONDX_ARROW3D_SQUARE`
- `BULLET_CHECKBOX`
- `NUMBERED_DECIMAL_ALPHA_ROMAN`
- `NUMBERED_DECIMAL_NESTED`

### Remove Bullets

```json
{
  "requests": [{
    "deleteParagraphBullets": {
      "range": {"startIndex": 1, "endIndex": 50}
    }
  }]
}
```

---

## Tables

### Insert Table

```json
{
  "requests": [{
    "insertTable": {
      "rows": 3,
      "columns": 4,
      "location": {"index": 1}
    }
  }]
}
```

Or at end of document:
```json
{
  "requests": [{
    "insertTable": {
      "rows": 3,
      "columns": 4,
      "endOfSegmentLocation": {"segmentId": ""}
    }
  }]
}
```

### Insert Table Row

```json
{
  "requests": [{
    "insertTableRow": {
      "tableCellLocation": {
        "tableStartLocation": {"index": 5},
        "rowIndex": 1,
        "columnIndex": 0
      },
      "insertBelow": true
    }
  }]
}
```

### Insert Table Column

```json
{
  "requests": [{
    "insertTableColumn": {
      "tableCellLocation": {
        "tableStartLocation": {"index": 5},
        "rowIndex": 0,
        "columnIndex": 1
      },
      "insertRight": true
    }
  }]
}
```

### Delete Table Row/Column

```json
{
  "requests": [{
    "deleteTableRow": {
      "tableCellLocation": {
        "tableStartLocation": {"index": 5},
        "rowIndex": 2,
        "columnIndex": 0
      }
    }
  }]
}
```

### Merge Table Cells

```json
{
  "requests": [{
    "mergeTableCells": {
      "tableRange": {
        "tableCellLocation": {
          "tableStartLocation": {"index": 5},
          "rowIndex": 0,
          "columnIndex": 0
        },
        "rowSpan": 1,
        "columnSpan": 2
      }
    }
  }]
}
```

---

## Images

### Insert Inline Image

```json
{
  "requests": [{
    "insertInlineImage": {
      "location": {"index": 1},
      "uri": "https://example.com/image.png",
      "objectSize": {
        "height": {"magnitude": 100, "unit": "PT"},
        "width": {"magnitude": 100, "unit": "PT"}
      }
    }
  }]
}
```

---

## Headers and Footers

### Create Header

```json
{
  "requests": [{
    "createHeader": {
      "type": "DEFAULT",
      "sectionBreakLocation": {"index": 0}
    }
  }]
}
```

### Create Footer

```json
{
  "requests": [{
    "createFooter": {
      "type": "DEFAULT",
      "sectionBreakLocation": {"index": 0}
    }
  }]
}
```

---

## Page Breaks

```json
{
  "requests": [{
    "insertPageBreak": {
      "location": {"index": 50}
    }
  }]
}
```

---

## Complete Example: Create a Formatted Document

```bash
cat << 'EOF' | uv run gdrive-cli.py docs batch-update <doc-id>
{
  "requests": [
    {
      "insertText": {
        "location": {"index": 1},
        "text": "Project Report\n\nExecutive Summary\nThis document outlines the key findings.\n\nKey Points:\n• First point\n• Second point\n• Third point\n"
      }
    },
    {
      "updateParagraphStyle": {
        "range": {"startIndex": 1, "endIndex": 15},
        "paragraphStyle": {"namedStyleType": "TITLE"},
        "fields": "namedStyleType"
      }
    },
    {
      "updateParagraphStyle": {
        "range": {"startIndex": 17, "endIndex": 35},
        "paragraphStyle": {"namedStyleType": "HEADING_1"},
        "fields": "namedStyleType"
      }
    }
  ]
}
EOF
```

---

## Official Documentation

For the complete API reference, see:
- [Google Docs API batchUpdate](https://developers.google.com/docs/api/reference/rest/v1/documents/batchUpdate)
- [Request types](https://developers.google.com/docs/api/reference/rest/v1/documents/request)
- [Document structure](https://developers.google.com/docs/api/concepts/structure)
