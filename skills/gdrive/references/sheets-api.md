# Google Sheets API Reference

This reference covers advanced spreadsheet manipulation using the `sheets batch-update` command.

## Understanding Spreadsheet Structure

Before editing, get the spreadsheet structure to find sheet IDs:

```bash
uv run gdrive-cli.py sheets get <spreadsheet-id>
```

The response includes:
- `sheets[]` - Array of sheets in the spreadsheet
- Each sheet has `properties.sheetId` (numeric ID for batch operations)
- `properties.title` - Sheet name
- `properties.gridProperties` - Row/column counts

## Batch Update Basics

Send requests via stdin as JSON:

```bash
echo '{"requests": [...]}' | uv run gdrive-cli.py sheets batch-update <spreadsheet-id>
```

**Important**: Sheet ranges use 0-based indices, and `endRowIndex`/`endColumnIndex` are exclusive.

Example: Range `A1:C3` = `{"sheetId": 0, "startRowIndex": 0, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 3}`

---

## Cell Formatting

### Bold Header Row

```json
{
  "requests": [{
    "repeatCell": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 1
      },
      "cell": {
        "userEnteredFormat": {
          "textFormat": {"bold": true}
        }
      },
      "fields": "userEnteredFormat.textFormat.bold"
    }
  }]
}
```

### Background Color

```json
{
  "requests": [{
    "repeatCell": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 1
      },
      "cell": {
        "userEnteredFormat": {
          "backgroundColor": {
            "red": 0.2,
            "green": 0.5,
            "blue": 0.8
          }
        }
      },
      "fields": "userEnteredFormat.backgroundColor"
    }
  }]
}
```

### Text Color and Font

```json
{
  "requests": [{
    "repeatCell": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 10,
        "startColumnIndex": 0,
        "endColumnIndex": 1
      },
      "cell": {
        "userEnteredFormat": {
          "textFormat": {
            "foregroundColor": {"red": 0.8, "green": 0.2, "blue": 0.2},
            "fontSize": 12,
            "fontFamily": "Arial",
            "bold": true,
            "italic": false
          }
        }
      },
      "fields": "userEnteredFormat.textFormat"
    }
  }]
}
```

### Number Format (Currency, Percentage, Date)

```json
{
  "requests": [{
    "repeatCell": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 2,
        "endColumnIndex": 3
      },
      "cell": {
        "userEnteredFormat": {
          "numberFormat": {
            "type": "CURRENCY",
            "pattern": "$#,##0.00"
          }
        }
      },
      "fields": "userEnteredFormat.numberFormat"
    }
  }]
}
```

Number format types: `TEXT`, `NUMBER`, `PERCENT`, `CURRENCY`, `DATE`, `TIME`, `DATE_TIME`, `SCIENTIFIC`

### Borders

```json
{
  "requests": [{
    "updateBorders": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 10,
        "startColumnIndex": 0,
        "endColumnIndex": 5
      },
      "top": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
      "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
      "left": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
      "right": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
      "innerHorizontal": {"style": "DOTTED", "width": 1, "color": {"red": 0.5, "green": 0.5, "blue": 0.5}},
      "innerVertical": {"style": "DOTTED", "width": 1, "color": {"red": 0.5, "green": 0.5, "blue": 0.5}}
    }
  }]
}
```

Border styles: `NONE`, `DOTTED`, `DASHED`, `SOLID`, `SOLID_MEDIUM`, `SOLID_THICK`, `DOUBLE`

---

## Alternating Row Colors (Banding)

```json
{
  "requests": [{
    "addBanding": {
      "bandedRange": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0,
          "endRowIndex": 100,
          "startColumnIndex": 0,
          "endColumnIndex": 5
        },
        "rowProperties": {
          "headerColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
          "firstBandColor": {"red": 1, "green": 1, "blue": 1},
          "secondBandColor": {"red": 0.95, "green": 0.95, "blue": 0.95}
        }
      }
    }
  }]
}
```

---

## Data Validation

### Dropdown List

```json
{
  "requests": [{
    "setDataValidation": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 3,
        "endColumnIndex": 4
      },
      "rule": {
        "condition": {
          "type": "ONE_OF_LIST",
          "values": [
            {"userEnteredValue": "Open"},
            {"userEnteredValue": "In Progress"},
            {"userEnteredValue": "Closed"}
          ]
        },
        "showCustomUi": true,
        "strict": true
      }
    }
  }]
}
```

### Checkbox

```json
{
  "requests": [{
    "setDataValidation": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 0,
        "endColumnIndex": 1
      },
      "rule": {
        "condition": {
          "type": "BOOLEAN"
        },
        "showCustomUi": true
      }
    }
  }]
}
```

### Number Range

```json
{
  "requests": [{
    "setDataValidation": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 2,
        "endColumnIndex": 3
      },
      "rule": {
        "condition": {
          "type": "NUMBER_BETWEEN",
          "values": [
            {"userEnteredValue": "1"},
            {"userEnteredValue": "100"}
          ]
        },
        "strict": true,
        "inputMessage": "Enter a number between 1 and 100"
      }
    }
  }]
}
```

Validation types: `ONE_OF_LIST`, `ONE_OF_RANGE`, `BOOLEAN`, `NUMBER_GREATER`, `NUMBER_LESS`, `NUMBER_BETWEEN`, `DATE_BEFORE`, `DATE_AFTER`, `TEXT_CONTAINS`, `CUSTOM_FORMULA`

---

## Conditional Formatting

### Highlight Cells Based on Value

```json
{
  "requests": [{
    "addConditionalFormatRule": {
      "rule": {
        "ranges": [{
          "sheetId": 0,
          "startRowIndex": 1,
          "endRowIndex": 100,
          "startColumnIndex": 4,
          "endColumnIndex": 5
        }],
        "booleanRule": {
          "condition": {
            "type": "NUMBER_GREATER",
            "values": [{"userEnteredValue": "1000"}]
          },
          "format": {
            "backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8}
          }
        }
      },
      "index": 0
    }
  }]
}
```

### Color Scale (Gradient)

```json
{
  "requests": [{
    "addConditionalFormatRule": {
      "rule": {
        "ranges": [{
          "sheetId": 0,
          "startRowIndex": 1,
          "endRowIndex": 100,
          "startColumnIndex": 2,
          "endColumnIndex": 3
        }],
        "gradientRule": {
          "minpoint": {
            "color": {"red": 1, "green": 0.8, "blue": 0.8},
            "type": "MIN"
          },
          "midpoint": {
            "color": {"red": 1, "green": 1, "blue": 0.8},
            "type": "PERCENTILE",
            "value": "50"
          },
          "maxpoint": {
            "color": {"red": 0.8, "green": 1, "blue": 0.8},
            "type": "MAX"
          }
        }
      },
      "index": 0
    }
  }]
}
```

---

## Sheet Management

### Add New Sheet

```json
{
  "requests": [{
    "addSheet": {
      "properties": {
        "title": "New Sheet",
        "gridProperties": {
          "rowCount": 1000,
          "columnCount": 26
        }
      }
    }
  }]
}
```

### Rename Sheet

```json
{
  "requests": [{
    "updateSheetProperties": {
      "properties": {
        "sheetId": 0,
        "title": "Renamed Sheet"
      },
      "fields": "title"
    }
  }]
}
```

### Delete Sheet

```json
{
  "requests": [{
    "deleteSheet": {
      "sheetId": 123456789
    }
  }]
}
```

### Freeze Rows/Columns

```json
{
  "requests": [{
    "updateSheetProperties": {
      "properties": {
        "sheetId": 0,
        "gridProperties": {
          "frozenRowCount": 1,
          "frozenColumnCount": 2
        }
      },
      "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
    }
  }]
}
```

### Hide/Show Sheet

```json
{
  "requests": [{
    "updateSheetProperties": {
      "properties": {
        "sheetId": 0,
        "hidden": true
      },
      "fields": "hidden"
    }
  }]
}
```

---

## Row/Column Operations

### Auto-Resize Columns

```json
{
  "requests": [{
    "autoResizeDimensions": {
      "dimensions": {
        "sheetId": 0,
        "dimension": "COLUMNS",
        "startIndex": 0,
        "endIndex": 5
      }
    }
  }]
}
```

### Set Column Width

```json
{
  "requests": [{
    "updateDimensionProperties": {
      "range": {
        "sheetId": 0,
        "dimension": "COLUMNS",
        "startIndex": 0,
        "endIndex": 1
      },
      "properties": {
        "pixelSize": 200
      },
      "fields": "pixelSize"
    }
  }]
}
```

### Hide Rows/Columns

```json
{
  "requests": [{
    "updateDimensionProperties": {
      "range": {
        "sheetId": 0,
        "dimension": "ROWS",
        "startIndex": 5,
        "endIndex": 10
      },
      "properties": {
        "hiddenByUser": true
      },
      "fields": "hiddenByUser"
    }
  }]
}
```

### Insert Rows/Columns

```json
{
  "requests": [{
    "insertDimension": {
      "range": {
        "sheetId": 0,
        "dimension": "ROWS",
        "startIndex": 5,
        "endIndex": 8
      },
      "inheritFromBefore": true
    }
  }]
}
```

### Delete Rows/Columns

```json
{
  "requests": [{
    "deleteDimension": {
      "range": {
        "sheetId": 0,
        "dimension": "COLUMNS",
        "startIndex": 3,
        "endIndex": 5
      }
    }
  }]
}
```

---

## Cell Merging

### Merge Cells

```json
{
  "requests": [{
    "mergeCells": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 1,
        "startColumnIndex": 0,
        "endColumnIndex": 3
      },
      "mergeType": "MERGE_ALL"
    }
  }]
}
```

Merge types: `MERGE_ALL`, `MERGE_COLUMNS`, `MERGE_ROWS`

### Unmerge Cells

```json
{
  "requests": [{
    "unmergeCells": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 1,
        "startColumnIndex": 0,
        "endColumnIndex": 3
      }
    }
  }]
}
```

---

## Sorting and Filtering

### Sort Range

```json
{
  "requests": [{
    "sortRange": {
      "range": {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 0,
        "endColumnIndex": 5
      },
      "sortSpecs": [{
        "dimensionIndex": 2,
        "sortOrder": "DESCENDING"
      }]
    }
  }]
}
```

### Add Filter View

```json
{
  "requests": [{
    "setBasicFilter": {
      "filter": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0,
          "endRowIndex": 100,
          "startColumnIndex": 0,
          "endColumnIndex": 5
        }
      }
    }
  }]
}
```

---

## Complete Example: Format a Data Table

```bash
cat << 'EOF' | uv run gdrive-cli.py sheets batch-update <spreadsheet-id>
{
  "requests": [
    {
      "repeatCell": {
        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
        "cell": {
          "userEnteredFormat": {
            "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
            "textFormat": {"bold": true, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
          }
        },
        "fields": "userEnteredFormat(backgroundColor,textFormat)"
      }
    },
    {
      "updateSheetProperties": {
        "properties": {"sheetId": 0, "gridProperties": {"frozenRowCount": 1}},
        "fields": "gridProperties.frozenRowCount"
      }
    },
    {
      "autoResizeDimensions": {
        "dimensions": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 10}
      }
    },
    {
      "setDataValidation": {
        "range": {"sheetId": 0, "startRowIndex": 1, "startColumnIndex": 4, "endColumnIndex": 5},
        "rule": {
          "condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": "Active"}, {"userEnteredValue": "Inactive"}]},
          "showCustomUi": true
        }
      }
    }
  ]
}
EOF
```

---

## Official Documentation

For the complete API reference, see:
- [Google Sheets API batchUpdate](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
- [Request types](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request)
- [Cell formatting](https://developers.google.com/sheets/api/guides/formats)
- [Data validation](https://developers.google.com/sheets/api/guides/validation)
