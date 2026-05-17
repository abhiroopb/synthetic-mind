---
name: mortgage-statement
description: "Process incoming Rocket Mortgage billing statements. Copies PDF from Dropbox Downloads to the Payments folder, extracts payment data, updates the Google Sheet tracker, adds Dropbox shareable link, and deletes the original. Use when a mortgage statement arrives or is mentioned in Downloads."
---

# Mortgage Statement Processing

Process a Rocket Mortgage billing statement PDF and update the mortgage tracker spreadsheet.

## Source & Destination

- **Source**: `Dropbox/Downloads/` — the statement PDF (e.g., "Client Mortgage Statement.pdf")
- **Destination**: `Dropbox/Documents/2424 Tulare Ave/Mortgage/Payments/YYYY-MM-DD.pdf`
  - Name using the **Statement Date** from the PDF (not the due date)
  - Local Dropbox root: `C:\Users\basua\Dropbox`

## Google Sheet

- **Spreadsheet ID**: `1hu0tTq4xCq_O6HrHaDV8dWLi9gGUBQoEbg2xHC3jlvU`
- **Tab**: `Mortgage (Refi)` (sheetId: `37179790`)
- **gdrive CLI**: `c:\Users\basua\.agents\skills\gdrive\gdrive-cli.py` (run via `uv run gdrive-cli.py` from that directory)
- **Auth credentials**: `~/.config/gdrive-skill/credentials.json`

### Column Layout (Row 1 headers)

| Col | Header | Type | Notes |
|-----|--------|------|-------|
| A | No. | Static | Payment number |
| B | Date | Static | Payment date (1-Mon-YYYY) |
| C | Paid to | Static | "Rocket Mortgage" |
| D | Principal | **Enter** | From "Next Payment Breakdown" |
| E | Interest | **Enter** | From "Next Payment Breakdown" |
| F | Taxes and Insurance | **Enter** | Usually $0.00 |
| G | Insurance | **Enter** | Usually $0.00 |
| H | Total | Formula | `=sum(D:G)` — do NOT overwrite |
| I | Link | **Enter** | Rich text hyperlink to Dropbox (see below) |
| J | Cumulative Principal | Formula | `=J_prev+D` — do NOT overwrite |
| K | Est. Home Value | **Enter** | Zillow Zestimate for 2424 Tulare Ave, El Cerrito CA |
| L | Home Equity | Formula | `=K-$Q$6+J` — do NOT overwrite |

### Finding the Correct Row

The statement's **Due Date** determines which row to update:
- Due Date "04/01/2026" → row with Date "1-Apr-2026"
- Read `A60:B70` to find the matching row
- The "Next Payment Breakdown" in the statement gives the values for that row

### Data Extraction from PDF

Extract from the Dropbox MCP `get_file_content` response or read the local PDF:
- **Principal**: "Next Payment Breakdown" → Principal line
- **Interest**: "Next Payment Breakdown" → Interest line  
- **Taxes**: "Next Payment Breakdown" → Taxes line (under Escrow)
- **Insurance**: "Next Payment Breakdown" → Insurance line (under Escrow)

### Zillow Zestimate

Look up the current Zestimate for **2424 Tulare Ave, El Cerrito, CA 94530** on Zillow.
Use `web_search` or `read_web_page` on `https://www.zillow.com/homes/2424-Tulare-Ave-El-Cerrito-CA-94530_rb/`.

## Workflow

### Step 1: Identify the Statement PDF
Search Dropbox Downloads for the mortgage statement PDF.

### Step 2: Extract Statement Data
Use Dropbox MCP `get_file_content` to read the PDF and extract:
- Statement Date (for filename)
- Due Date (to find the correct spreadsheet row)
- Next Payment Breakdown values (Principal, Interest, Taxes, Insurance)

### Step 3: Copy & Rename
```
cmd /c copy "C:\Users\basua\Dropbox\Downloads\<original filename>.pdf" "C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Mortgage\Payments\YYYY-MM-DD.pdf"
```

### Step 4: Wait for Dropbox Sync
The file must sync to Dropbox cloud before getting a shareable link.
- Poll with `get_file_metadata` using path `/Documents/2424 Tulare Ave/Mortgage/Payments/YYYY-MM-DD.pdf`
- Files are in namespace `ns:8206295520`
- Sync can take 5-30+ minutes; poll every 60 seconds
- If the user says to wait, use `python -c "import time; time.sleep(N)"` (max ~240s per call to avoid timeout)

### Step 5: Get Dropbox Shareable Link
Use Dropbox MCP `get_file_content` on the synced file. The response includes a `content_link` field.

### Step 6: Get Zillow Zestimate
Look up the current Zestimate value.

### Step 7: Update the Google Sheet

**For D, E, F, G, K columns** — use the gdrive CLI via a Python script to avoid PowerShell escaping:

```python
import subprocess, json, os
os.chdir(r"c:\Users\basua\.agents\skills\gdrive")

SPREADSHEET_ID = "1hu0tTq4xCq_O6HrHaDV8dWLi9gGUBQoEbg2xHC3jlvU"
ROW = 64  # adjust to correct row

# Write payment values
result = subprocess.run(
    ["uv", "run", "gdrive-cli.py", "sheets", "write",
     SPREADSHEET_ID,
     "--range", f"'Mortgage (Refi)'!D{ROW}:G{ROW}",
     "--values", json.dumps([[1306.08, 1289.33, 0, 0]])],
    capture_output=True, text=True
)

# Write Zestimate
result2 = subprocess.run(
    ["uv", "run", "gdrive-cli.py", "sheets", "write",
     SPREADSHEET_ID,
     "--range", f"'Mortgage (Refi)'!K{ROW}",
     "--values", json.dumps([[1108100]])],
    capture_output=True, text=True
)
```

**For I column (hyperlink)** — the Link column uses **rich text hyperlinks** (NOT `=HYPERLINK()` formulas). Use the Google Sheets `batchUpdate` API directly:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".config", "gdrive-skill", "credentials.json")
with open(TOKEN_PATH) as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data.get("token"),
    refresh_token=token_data.get("refresh_token"),
    token_uri=token_data.get("token_uri"),
    client_id=token_data.get("client_id"),
    client_secret=token_data.get("client_secret"),
    scopes=token_data.get("scopes"),
)

service = build("sheets", "v4", credentials=creds)

request_body = {
    "requests": [{
        "updateCells": {
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "Link"},
                    "textFormatRuns": [{
                        "startIndex": 0,
                        "format": {"link": {"uri": DROPBOX_LINK}}
                    }]
                }]
            }],
            "range": {
                "sheetId": 37179790,
                "startRowIndex": ROW - 1,  # 0-based
                "endRowIndex": ROW,
                "startColumnIndex": 8,     # Column I
                "endColumnIndex": 9,
            },
            "fields": "userEnteredValue,textFormatRuns"
        }
    }]
}

service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=request_body
).execute()
```

### Step 8: Verify
Read back the updated row to confirm all values are correct:
```
uv run gdrive-cli.py sheets read <SPREADSHEET_ID> --range "'Mortgage (Refi)'!A<ROW>:L<ROW>"
```

### Step 9: Delete Original
```
cmd /c del "C:\Users\basua\Dropbox\Downloads\<original filename>.pdf"
```

## Important Notes

- **Never overwrite formula columns** (H, J, L). Only write to D, E, F, G, I, K.
- **Always use a Python script file** for gdrive CLI calls. PowerShell and cmd have escaping issues with JSON `--values` arguments.
- The statement's "Next Payment Breakdown" is for the **upcoming** payment (matching the Due Date row), not the statement date row.
- Combine all operations into a single Python script when possible for efficiency.
