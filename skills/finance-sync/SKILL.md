---
name: finance-sync
description: "Sync account balances from the Finances spreadsheet to the Tiller Foundation Template Balance History. Use when asked to update finances, sync balances, update Tiller, or refresh account data."
---

# Finance Sync

Syncs account balance data between two Google Sheets:
- **Source:** [Finances spreadsheet](https://docs.google.com/spreadsheets/d/1dNaTZ3igHWdxOlH2fTnLM5jxRxFCIlkifHyWz0wSFt0) — TOPLINE tab, column K (Total Amount in USD)
- **Destination:** [Tiller Foundation Template](https://docs.google.com/spreadsheets/d/1-vZF7pME9SAYlqiXuzd57Hvlmq9haEWhN6WvtIqPa-8) — Balance History tab (sheetId: `1531277441`)

## Prerequisites

Load the `gdrive` skill first. All commands run from the gdrive skill directory.

## Spreadsheet IDs

- Finances: `1dNaTZ3igHWdxOlH2fTnLM5jxRxFCIlkifHyWz0wSFt0`
- Tiller: `1-vZF7pME9SAYlqiXuzd57Hvlmq9haEWhN6WvtIqPa-8`

## Account Mapping (Fixed — these accounts won't change)

| # | Tiller Account Name | Account # | Account ID | Institution | Type | Class | Finances Row (TOPLINE) |
|---|---|---|---|---|---|---|---|
| 1 | Apostrophe Collective | | manual:c84feaba-1562-4847-aee1-68c697cc0350 | Private Company | Investment | Asset | "Private company" row (col K) |
| 2 | HSBC Holdings Plc | C0804209824 | manual:d726c5a3-090d-4821-8161-a3bae9e82eb3 | Computershare | Investment | Asset | "Computershare" row (col K) |
| 3 | CPF - Medisave Account - AB | | manual:c490a26c-76a7-4902-a40b-695bd571e4f3 | CPF | Savings | Asset | CPF / S8860492Z / Medisave Account (col K) |
| 4 | CPF - Medisave Account - ZI | | manual:57e4e202-b2eb-46fc-bec2-8b71cc4e15cc | CPF | Savings | Asset | CPF / S8636333Z / Medisave Account (col K) |
| 5 | CPF - Ordinary Account - AB | | manual:652d17c9-2768-49e1-ae16-5fc7eda54c3f | CPF | Savings | Asset | CPF / S8860492Z / Ordinary Account (col K) |
| 6 | CPF - Ordinary Account - ZI | | manual:35aca677-8497-4a96-840f-43c9cec9d30b | CPF | Savings | Asset | CPF / S8636333Z / Ordinary Account (col K) |
| 7 | CPF - Special Account - AB | | manual:50b47fb5-2ebc-4b0a-8921-02175a8329ab | CPF | Savings | Asset | CPF / S8860492Z / Special Account (col K) |
| 8 | CPF - Special Account - ZI | | manual:c13ce178-3982-439c-badb-20bd9893189f | CPF | Savings | Asset | CPF / S8636333Z / Special Account (col K) |
| 9 | DBS - Fixed Deposit (0019) | 281611010019 | manual:956373c5-6a21-4523-b94f-11c3de9ce5fe | DBS Treasures | Savings | Asset | DBS Treasures / 281611010019 / FD (col K) |
| 10 | DBS - Fixed Deposit (0028) | 281611010028 | manual:abff4ad1-6bfc-4a86-bc4c-a582f5289937 | DBS Treasures | Savings | Asset | DBS Treasures / 281611010028 / FD (col K) |
| 11 | DBS - Fixed Deposit (0037) | 281611010037 | manual:f591ddb7-01bd-47f0-bb15-c7e3fbed24c0 | DBS Treasures | Savings | Asset | DBS Treasures / 281611010037 / FD (col K) |
| 12 | DBS - Fixed Deposit (0046) | 281611010046 | manual:057995a2-62e1-464b-8af7-f5a04f0d2299 | DBS Treasures | Savings | Asset | DBS Treasures / 281611010046 / FD (col K) |
| 13 | DBS - NRE (9466) | 828020099466 | manual:9121d6f7-6f5a-476d-8fb1-8a87aac1819d | DBS Treasures | Savings | Asset | DBS Treasures / 828020099466 / NRE (col K) |
| 14 | DBS - NRO (9475) | 828010099475 | manual:4af6d29a-f648-486e-974f-6a8337be9b0b | DBS Treasures | Savings | Asset | DBS Treasures / 828010099475 / NRO (col K) |
| 15 | POSB eSavings - ZI (3037) | xxxx3037 | manual:0bc2c455-db15-4003-a970-1a5fdfc36f5a | DBS | Savings | Asset | POSB eSavings / 137-54794-5 (col K) — Note: this is Zareen's POSB |
| 16 | POSB Savings - AB (7945) | xxxx7945 | manual:b7df416c-b0f9-456b-bcbf-a4c46e9231c7 | DBS | Savings | Asset | POSB Savings / 017-31303-7 (col K) — Note: this is Abhi's POSB |
| 17 | Mazda CX-5 | 8CVW950 | manual:5bd19a8b-184d-4c64-812d-c6da20b87cd8 | Car | Other | Asset | "Mazda CX-5" row (col K) |
| 18 | 2424 Tulare Ave | | manual:04feacf4-7d42-4e52-9505-cc02bcb6a471 | Home | Other | Asset | "2424 Tulare Ave" row (col K) |

## Workflow

1. **Data Collection & Finances Input:**
   - **Statement Pre-Processing:**
     - Scan the `Dropbox/Money` folder for the latest PDF statements for specific accounts: POSB Savings (Abhi & Zareen), DBS Treasures (NRE, NRO, FD), and CPF (Abhi & Zareen).
     - Extract the closing balances from these PDFs and write them to Finances `TOPLINE` tab (INR to **Column I**, SGD to **Column J**). *Always use the Python `googleapiclient` method described in Technical Notes for writing.*
   - **Asset Valuation:**
     - **Mazda CX-5 (Car):** Fetch Kelly Blue Book (KBB) Fair Purchase Price for VIN: `JM3KFBDMXJ0335582` (2018 Grand Touring) and write to `TOPLINE!H57`.
     - **2424 Tulare Ave (House):** Fetch Zillow Zestimate and write to `TOPLINE!H53`.
     - **Payments Update:** Update [Payments spreadsheet](https://docs.google.com/spreadsheets/d/1hu0tTq4xCq_O6HrHaDV8dWLi9gGUBQoEbg2xHC3jlvU) → `Mortgage (Refi)` tab → Column K ("Est. Home Value") at the row for the current month with the Zestimate.
2. **Forward Sync: Finances → Tiller**
   - **Read TOPLINE tab** from Finances spreadsheet (`TOPLINE!A1:K80`) to get current balances in column K.
   - **Match accounts** using the mapping table above (including the assets) — match by account name (col A) + account number (col B).
   - **Insert new rows** at the top of Balance History (after header) using `sheets batch-update` with `insertDimension` on sheetId `1531277441`.
   - **Write rows** with current date/time, account metadata, and the balance from the Finances sheet. *Always use the Python `googleapiclient` method described in Technical Notes for writing.*
   - **Show summary table** to the user with: Account, Old Balance (from last Balance History entry), New Balance, Change.

## Balance History Column Format

| Col | Field | Example |
|-----|-------|---------|
| B | Date | 4/4/26 |
| C | Time | 11:00 PM |
| D | Account | HSBC Holdings Plc |
| E | Account # | C0804209824 |
| F | Account ID | manual:d726c5a3-... |
| G | Balance ID | (leave blank for manual) |
| H | Institution | Computershare |
| I | Balance | $216,833.38 |
| J | Month | 4/1/26 (first of current month) |
| K | Week | 3/29/26 (most recent Saturday) |
| L | Type | Investment / Savings |
| M | Class | Asset |
| N | Account Status | ACTIVE |
| O | Date Added | 4/4/2026 |

## Reverse Sync: Tiller Balances → Finances TOPLINE (Column H)

Pull the latest balances from Tiller's **Balances** tab and write them into column H of the Finances TOPLINE tab. 
**IMPORTANT**: Do not attempt to update the entire column `H4:H35` as a single block array, as this will shift empty values into incorrect cells. Always target the specific mapped cells explicitly.

| Tiller Account | Acct # | Finances Cell |
|---|---|---|
| Chase Checking | 0638 | H4 |
| Chase Savings | 9860 | H5 |
| Schwab Checking | 2413 | H6 |
| Schwab Emergency | 8231 | H7 |
| TreasuryDirect AB | 9305 | H14 |
| TreasuryDirect Trust | 1268 | H15 |
| TreasuryDirect ZI | 4883 | H16 |
| Chase Brokerage | 0053 | H24 |
| Schwab Personal | 5922 | H25 |
| Schwab Brokerage | 1756 | H26 |
| Vanguard | 1836 | H27 |
| E-Trade SQ RSU | 2334 | H28 |
| Fidelity 401K | 0207 | H31 |
| Fidelity HSA | 9907 | H32 |
| Schwab Rollover IRA ZI | 2468 | H33 |
| Schwab Roth IRA AB | 4123 | H34 |
| Schwab Roth IRA ZI | 4481 | H35 |
| Mortgage | 1199 | H54 |


## Sync Completion

After all updates are finished:
1. Write today's date into `TOPLINE!T9` to mark the sync completion.
2. **Execute the Mortgage Statement Skill:** Immediately trigger the `mortgage-statement` skill to process any recent mortgage payments and ensure the home tracking is fully up to date.

## Technical Notes

- Balance values from Finances are in **USD** (column K = "Total Amount in USD")
- Format balances as `$X,XXX.XX`
- The Month column should be the 1st of the current month
- The Week column should be the most recent Saturday
- Always insert rows at the TOP of Balance History (after header row). You can use `sheets batch-update` to insert the blank rows.
- **CRITICAL:** Do NOT use `batch-update` with `userEnteredValue` to write the actual row data containing dates/times, as it will bypass Google's date parsing and insert them as plain strings. Instead, after inserting the empty rows, use the Sheets API `values().batchUpdate()` to fill the row data.
- Column A is always blank (matches existing pattern)
- **Updating Google Sheets safely**: To completely avoid PowerShell JSON mangling and bash variable expansion issues (where `$19,432.80` gets truncated to `$432.80` because of the comma), **do not use the gdrive-cli via subprocess**. Instead, write a temporary Python script that directly uses `googleapiclient.discovery` utilizing the existing credentials at `~/.config/gdrive-skill/credentials.json`.

  Example Safe Python script:
  ```python
  import json, os
  from google.oauth2.credentials import Credentials
  from googleapiclient.discovery import build

  TOKEN_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gdrive-skill', 'credentials.json')
  with open(TOKEN_PATH) as f:
      token_data = json.load(f)

  creds = Credentials(**token_data)
  service = build('sheets', 'v4', credentials=creds)

  data = [
      {'range': 'TOPLINE!H24', 'values': [['$667,208.27']]},
      {'range': 'TOPLINE!H25', 'values': [['$319,406.00']]}
  ]

  service.spreadsheets().values().batchUpdate(
      spreadsheetId='1dNaTZ3igHWdxOlH2fTnLM5jxRxFCIlkifHyWz0wSFt0',
      body={'valueInputOption': 'USER_ENTERED', 'data': data}
  ).execute()
  ```
