# Google Slides API Reference

This reference covers advanced presentation manipulation using the `slides batch-update` command.

## Understanding Presentation Structure

Before editing, get the presentation structure to find slide and element IDs:

```bash
uv run gdrive-cli.py slides get <presentation-id>
```

The response includes:
- `slides[]` - Array of slide pages
- Each slide has `objectId` and `pageElements[]`
- `pageElements[]` contains shapes, images, tables with their `objectId` values
- `slideProperties.notesPage` contains speaker notes

## Batch Update Basics

Send requests via stdin as JSON:

```bash
echo '{"requests": [...]}' | uv run gdrive-cli.py slides batch-update <presentation-id>
```

Multiple requests execute atomically. If one fails, none are applied.

---

## Slide Operations

### Create New Slide

```json
{
  "requests": [{
    "createSlide": {
      "insertionIndex": 1,
      "slideLayoutReference": {
        "predefinedLayout": "TITLE_AND_BODY"
      }
    }
  }]
}
```

Predefined layouts:
- `BLANK`
- `CAPTION_ONLY`
- `TITLE`
- `TITLE_AND_BODY`
- `TITLE_AND_TWO_COLUMNS`
- `TITLE_ONLY`
- `SECTION_HEADER`
- `SECTION_TITLE_AND_DESCRIPTION`
- `ONE_COLUMN_TEXT`
- `MAIN_POINT`
- `BIG_NUMBER`

### Create Slide with Custom ID

```json
{
  "requests": [{
    "createSlide": {
      "objectId": "myCustomSlideId",
      "insertionIndex": 0,
      "slideLayoutReference": {
        "predefinedLayout": "BLANK"
      }
    }
  }]
}
```

### Delete Slide

```json
{
  "requests": [{
    "deleteObject": {
      "objectId": "slideObjectId"
    }
  }]
}
```

### Duplicate Slide

```json
{
  "requests": [{
    "duplicateObject": {
      "objectId": "sourceSlideId",
      "objectIds": {
        "sourceSlideId": "newSlideId"
      }
    }
  }]
}
```

### Reorder Slides

```json
{
  "requests": [{
    "updateSlidesPosition": {
      "slideObjectIds": ["slide1", "slide2"],
      "insertionIndex": 0
    }
  }]
}
```

---

## Shape Operations

### Create Text Box

```json
{
  "requests": [{
    "createShape": {
      "objectId": "myTextBox",
      "shapeType": "TEXT_BOX",
      "elementProperties": {
        "pageObjectId": "slideObjectId",
        "size": {
          "height": {"magnitude": 100, "unit": "PT"},
          "width": {"magnitude": 300, "unit": "PT"}
        },
        "transform": {
          "scaleX": 1,
          "scaleY": 1,
          "translateX": 100,
          "translateY": 100,
          "unit": "PT"
        }
      }
    }
  }]
}
```

### Create Rectangle Shape

```json
{
  "requests": [{
    "createShape": {
      "objectId": "myRectangle",
      "shapeType": "RECTANGLE",
      "elementProperties": {
        "pageObjectId": "slideObjectId",
        "size": {
          "height": {"magnitude": 50, "unit": "PT"},
          "width": {"magnitude": 200, "unit": "PT"}
        },
        "transform": {
          "scaleX": 1,
          "scaleY": 1,
          "translateX": 50,
          "translateY": 200,
          "unit": "PT"
        }
      }
    }
  }]
}
```

Common shape types: `TEXT_BOX`, `RECTANGLE`, `ROUND_RECTANGLE`, `ELLIPSE`, `TRIANGLE`, `ARROW`, `CLOUD`

### Delete Shape

```json
{
  "requests": [{
    "deleteObject": {
      "objectId": "shapeObjectId"
    }
  }]
}
```

---

## Text Operations

### Insert Text into Shape

```json
{
  "requests": [{
    "insertText": {
      "objectId": "shapeOrTextBoxId",
      "insertionIndex": 0,
      "text": "Hello, World!"
    }
  }]
}
```

### Delete Text from Shape

```json
{
  "requests": [{
    "deleteText": {
      "objectId": "shapeObjectId",
      "textRange": {
        "type": "ALL"
      }
    }
  }]
}
```

Or delete specific range:
```json
{
  "requests": [{
    "deleteText": {
      "objectId": "shapeObjectId",
      "textRange": {
        "type": "FIXED_RANGE",
        "startIndex": 0,
        "endIndex": 10
      }
    }
  }]
}
```

### Replace All Text

```json
{
  "requests": [{
    "replaceAllText": {
      "containsText": {
        "text": "{{placeholder}}",
        "matchCase": true
      },
      "replaceText": "Actual content"
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
      "objectId": "shapeObjectId",
      "textRange": {
        "type": "FIXED_RANGE",
        "startIndex": 0,
        "endIndex": 5
      },
      "style": {
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
      "objectId": "shapeObjectId",
      "textRange": {"type": "ALL"},
      "style": {
        "fontSize": {"magnitude": 18, "unit": "PT"},
        "foregroundColor": {
          "opaqueColor": {
            "rgbColor": {"red": 0.2, "green": 0.4, "blue": 0.8}
          }
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
      "objectId": "shapeObjectId",
      "textRange": {"type": "ALL"},
      "style": {
        "link": {"url": "https://example.com"}
      },
      "fields": "link"
    }
  }]
}
```

---

## Paragraph Formatting

### Bullet Points

```json
{
  "requests": [{
    "createParagraphBullets": {
      "objectId": "shapeObjectId",
      "textRange": {"type": "ALL"},
      "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
    }
  }]
}
```

Bullet presets:
- `BULLET_DISC_CIRCLE_SQUARE`
- `BULLET_DIAMONDX_ARROW3D_SQUARE`
- `BULLET_CHECKBOX`
- `BULLET_ARROW_DIAMOND_DISC`
- `BULLET_STAR_CIRCLE_SQUARE`
- `BULLET_ARROW3D_CIRCLE_SQUARE`
- `BULLET_LEFTTRIANGLE_DIAMOND_DISC`
- `NUMBERED_DIGIT_ALPHA_ROMAN`
- `NUMBERED_DIGIT_ALPHA_ROMAN_PARENS`
- `NUMBERED_DIGIT_NESTED`
- `NUMBERED_UPPERALPHA_ALPHA_ROMAN`
- `NUMBERED_UPPERROMAN_UPPERALPHA_DIGIT`
- `NUMBERED_ZERODIGIT_ALPHA_ROMAN`

### Remove Bullets

```json
{
  "requests": [{
    "deleteParagraphBullets": {
      "objectId": "shapeObjectId",
      "textRange": {"type": "ALL"}
    }
  }]
}
```

### Alignment

```json
{
  "requests": [{
    "updateParagraphStyle": {
      "objectId": "shapeObjectId",
      "textRange": {"type": "ALL"},
      "style": {
        "alignment": "CENTER"
      },
      "fields": "alignment"
    }
  }]
}
```

Alignments: `START`, `CENTER`, `END`, `JUSTIFIED`

---

## Images

### Insert Image from URL

```json
{
  "requests": [{
    "createImage": {
      "objectId": "myImage",
      "url": "https://example.com/image.png",
      "elementProperties": {
        "pageObjectId": "slideObjectId",
        "size": {
          "height": {"magnitude": 200, "unit": "PT"},
          "width": {"magnitude": 300, "unit": "PT"}
        },
        "transform": {
          "scaleX": 1,
          "scaleY": 1,
          "translateX": 100,
          "translateY": 100,
          "unit": "PT"
        }
      }
    }
  }]
}
```

### Replace All Shapes with Image

```json
{
  "requests": [{
    "replaceAllShapesWithImage": {
      "imageUrl": "https://example.com/logo.png",
      "imageReplaceMethod": "CENTER_INSIDE",
      "containsText": {
        "text": "{{logo}}",
        "matchCase": true
      }
    }
  }]
}
```

---

## Tables

### Create Table

```json
{
  "requests": [{
    "createTable": {
      "objectId": "myTable",
      "elementProperties": {
        "pageObjectId": "slideObjectId",
        "size": {
          "height": {"magnitude": 200, "unit": "PT"},
          "width": {"magnitude": 400, "unit": "PT"}
        },
        "transform": {
          "scaleX": 1,
          "scaleY": 1,
          "translateX": 50,
          "translateY": 150,
          "unit": "PT"
        }
      },
      "rows": 3,
      "columns": 4
    }
  }]
}
```

### Insert Text into Table Cell

```json
{
  "requests": [{
    "insertText": {
      "objectId": "myTable",
      "cellLocation": {
        "rowIndex": 0,
        "columnIndex": 0
      },
      "text": "Header 1",
      "insertionIndex": 0
    }
  }]
}
```

### Insert/Delete Table Rows

```json
{
  "requests": [{
    "insertTableRows": {
      "tableObjectId": "myTable",
      "cellLocation": {"rowIndex": 1, "columnIndex": 0},
      "insertBelow": true,
      "number": 2
    }
  }]
}
```

```json
{
  "requests": [{
    "deleteTableRow": {
      "tableObjectId": "myTable",
      "cellLocation": {"rowIndex": 2, "columnIndex": 0}
    }
  }]
}
```

---

## Shape Properties

### Background Color

```json
{
  "requests": [{
    "updateShapeProperties": {
      "objectId": "shapeObjectId",
      "shapeProperties": {
        "shapeBackgroundFill": {
          "solidFill": {
            "color": {
              "rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
            }
          }
        }
      },
      "fields": "shapeBackgroundFill.solidFill.color"
    }
  }]
}
```

### Border/Outline

```json
{
  "requests": [{
    "updateShapeProperties": {
      "objectId": "shapeObjectId",
      "shapeProperties": {
        "outline": {
          "outlineFill": {
            "solidFill": {
              "color": {
                "rgbColor": {"red": 0, "green": 0, "blue": 0}
              }
            }
          },
          "weight": {"magnitude": 2, "unit": "PT"}
        }
      },
      "fields": "outline"
    }
  }]
}
```

---

## Speaker Notes

### Add/Update Speaker Notes

The speaker notes object ID is in `slide.slideProperties.notesPage.notesProperties.speakerNotesObjectId`.

```json
{
  "requests": [
    {
      "deleteText": {
        "objectId": "speakerNotesObjectId",
        "textRange": {"type": "ALL"}
      }
    },
    {
      "insertText": {
        "objectId": "speakerNotesObjectId",
        "insertionIndex": 0,
        "text": "These are the speaker notes for this slide."
      }
    }
  ]
}
```

---

## Complete Example: Create Slide with Content

```bash
cat << 'EOF' | uv run gdrive-cli.py slides batch-update <presentation-id>
{
  "requests": [
    {
      "createSlide": {
        "objectId": "newSlide1",
        "insertionIndex": 1,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}
      }
    },
    {
      "createShape": {
        "objectId": "titleBox",
        "shapeType": "TEXT_BOX",
        "elementProperties": {
          "pageObjectId": "newSlide1",
          "size": {"height": {"magnitude": 50, "unit": "PT"}, "width": {"magnitude": 600, "unit": "PT"}},
          "transform": {"scaleX": 1, "scaleY": 1, "translateX": 50, "translateY": 30, "unit": "PT"}
        }
      }
    },
    {
      "insertText": {
        "objectId": "titleBox",
        "insertionIndex": 0,
        "text": "Presentation Title"
      }
    },
    {
      "updateTextStyle": {
        "objectId": "titleBox",
        "textRange": {"type": "ALL"},
        "style": {"fontSize": {"magnitude": 32, "unit": "PT"}, "bold": true},
        "fields": "fontSize,bold"
      }
    },
    {
      "createShape": {
        "objectId": "contentBox",
        "shapeType": "TEXT_BOX",
        "elementProperties": {
          "pageObjectId": "newSlide1",
          "size": {"height": {"magnitude": 300, "unit": "PT"}, "width": {"magnitude": 600, "unit": "PT"}},
          "transform": {"scaleX": 1, "scaleY": 1, "translateX": 50, "translateY": 100, "unit": "PT"}
        }
      }
    },
    {
      "insertText": {
        "objectId": "contentBox",
        "insertionIndex": 0,
        "text": "First bullet point\nSecond bullet point\nThird bullet point"
      }
    },
    {
      "createParagraphBullets": {
        "objectId": "contentBox",
        "textRange": {"type": "ALL"},
        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
      }
    }
  ]
}
EOF
```

---

## Official Documentation

For the complete API reference, see:
- [Google Slides API batchUpdate](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations/batchUpdate)
- [Request types](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations/request)
- [Page elements](https://developers.google.com/workspace/slides/api/concepts/page-elements)
- [Add shapes and text](https://developers.google.com/workspace/slides/api/guides/add-shape)
