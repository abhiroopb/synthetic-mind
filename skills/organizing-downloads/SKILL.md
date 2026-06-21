---
name: organizing-downloads
description: "Organizes files in the local Downloads folder into proper folders. Use when asked to organize, sort, or file downloaded documents."
---

# Organizing Downloads

Scans the local filesystem at `C:\Users\basua\Dropbox\Downloads`, identifies each file's content, and moves/renames it according to the rules below.

## Filesystem Strategy

- **Use the local filesystem** (`run_shell_command` with PowerShell) for all scanning, moving, and renaming.
- **Path Handling:** Always use absolute Windows paths with backslashes.
- **Do NOT use the Dropbox MCP API** for file operations.

## Execution Workflow

1.  **Inventory:** List all files (top-level only) in `C:\Users\basua\Dropbox\Downloads`.
2.  **Deep Inspection & Contextual Discovery:**
    - **Step A: Text Extraction.** Use `Select-String` or `Get-Content -Raw` to search for entity names (e.g., "Sutter", "Block", "Fidelity", "EBMUD"), subjects ("Health", "Salary", "Dividend"), and confirmation codes.
    - **Step B: Date Extraction.** Locate the **statement date**, **service date**, or **invoice date** in the content. Do NOT use the file modification date unless no other date exists.
    - **Step C: Contextual Search.** If the file's origin is unclear, search `C:\Users\basua\Dropbox` for subfolders matching extracted keywords to find the established home for such documents.
    - **Step D: Precedent Check.** Once a destination is found, list the last 3-5 files in that folder. Use their naming convention as the absolute template for the new file.
3.  **Deduplication & Supplemental Check:**
    - **Identical:** If hashes match, delete the download.
    - **Supplemental/Update:** If the filename matches an existing file but the content differs (e.g., a seat upgrade in a flight confirmation, a revised invoice), **replace** the old file with the new one.
    - **Signed vs Unsigned:** If an unsigned version exists at the destination and the download is signed, replace it.
4.  **Summary & Approval:**
    - **MANDATORY:** Present a numbered table with columns: `#`, `Original Filename`, `New Name`, `Destination Folder`, and `Rationale` (why you chose this name/folder).
    - **MANDATORY:** If replacing an existing file or creating a new folder, highlight this in the summary.
    - **MANDATORY:** Wait for explicit user confirmation before proceeding.
5.  **Action:** Upon user approval, `move`, `replace`, or `delete` files.

## General Guidelines

- **Naming:** Date format is always `YYYY-MM-DD`.
- **Ignore Folders:** ALWAYS ignore folders within the Downloads directory. Only process files.
- **Ignore Subfolders:** Only process files at the top level of the Downloads folder.
- **Folder Creation:** Follow established patterns. Do NOT create year folders for Utilities or Zareen's medical bills.
- **Description:** For medical/health bills, always include a brief description of the service (e.g., "Sutter Bill for Injured Elbow").

## Rules

### Rule 1: Purchase Receipts (Non-Home)
- **Destination:** `C:\Users\basua\Dropbox\Money\Receipts\{YEAR}\`
- **Naming:** `YYYY-MM-DD - Item Name (Business Name).pdf`
- **Note:** Verify items carefully from content text extraction (e.g. distinguishing a "Paisley Cotton Bandana" from a "Cotton Shirt" for Boggi Milano; using NordVPN, REI, SP Connect, or Sony/Best Buy as business/brand names).

### Rule 2: Home Contractor Documents (2424 Tulare Ave)
- **Destination:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Contractors\{Contractor Name}\`
- **Naming:** `YYYY-MM-DD - Description.pdf`

### Rule 3: Bank & Brokerage Statements
- **Destination:** `C:\Users\basua\Dropbox\Money\Banks\{Bank Name}\{Account Folder}\Statements\`
- **Naming:** `YYYY-MM-DD.pdf` (statement end date).
- **Note:** For the active/current year, statements are stored directly in the account root folder, while past completed years are grouped in `{YEAR}\` subfolders.
- **Exceptions:** Do not use `\Statements` subfolders for:
  - Chase DoorDash Card: `C:\Users\basua\Dropbox\Money\Banks\Chase\DoorDash Card (8900)\`
  - Chase Amazon Card: `C:\Users\basua\Dropbox\Money\Banks\Chase\Amazon Card (9951)\`
  - Chase CPC Checking: `C:\Users\basua\Dropbox\Money\Banks\Chase\CPC Checking (822920638)\`
  - Chase CPC Savings: `C:\Users\basua\Dropbox\Money\Banks\Chase\CPC Savings (3760199860)\`
- **Specific Account Mapping:**
  - Charles Schwab: Check the suffix to map correctly (e.g. 123 -> `5003-4123 - AB Roth IRA\Statements`). Some folders use `\Statement` (singular) instead of `\Statements` (plural) based on precedent.

### Rule 4: Bill Payments
- **Destination:** `C:\Users\basua\Dropbox\Money\Banks\{Bank Name}\{Account Folder}\Bill Payment\` (or `\Bill Payments\`)
- **Naming:** `YYYY-MM-DD.pdf`
- **Exception:** Do not add "- payment" or any other suffix. Only use the date the file was paid on.

### Rule 5: E-Trade (RSU + ESPP)
- **Statements:** `C:\Users\basua\Dropbox\Money\Banks\E-Trade\Statements\`
- **Trade/Release/Payout Confirmations:** `C:\Users\basua\Dropbox\Money\Banks\E-Trade\RSU + ESPP\`
- **Naming:** Ensure all confirmations have a unique name (e.g., `YYYY-MM-DD - Release - 100 shares.pdf` or `YYYY-MM-DD - Trade - 50 shares (2).pdf`).

### Rule 6: Utilities (2424 Tulare Ave)
- **Destination:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Utilities\{Utility Name}\`
- **Naming:** `YYYY-MM-DD.pdf`
- **EBSAN:** `EBSAN\Statement\`.
- **EBMUD:** `EBMUD\`.
- **PG&E:** `PG&E\Electric and Gas Statements\`.
- **Sonic:** `Sonic\`.

### Rule 7: Home & Mortgage (2424 Tulare Ave)
- **Mortgage Payments:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Mortgage\Payments\`
- **Home Insurance:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Home Insurance\` (e.g., `YYYY-MM-DD - 2026 Policy Renewal.pdf`).

### Rule 8: Insurance & Health
- **Aetna EOBs (Zareen):** `C:\Users\basua\Dropbox\Documents\Health\Zareen\Bill Payments\YYYY-MM-DD - Aetna EOB.pdf`.
- **Aetna EOBs (Abhi):** `C:\Users\basua\Dropbox\Documents\Health\Abhi\Bills\YYYY-MM-DD - Aetna EOB.pdf`.
- **Dental EOBs (Abhi):** `C:\Users\basua\Dropbox\Documents\Health\Abhi\Dental\YYYY-MM-DD - Delta Dental.pdf` (No "EOB" in name).
- **Health Visits (Abhi):** `C:\Users\basua\Dropbox\Documents\Health\Abhi\Visits\YYYY-MM-DD - Description.pdf`.
- **Bill Payments (Zareen):** `C:\Users\basua\Dropbox\Documents\Health\Zareen\Bill Payments\YYYY-MM-DD - Description.pdf`. (No "Health" prefix, no year folders).

### Rule 9: Pay Stubs & Employment
- **Destination:** `C:\Users\basua\Dropbox\Money\Payslips\Abhi\{YEAR}\`
- **Naming:** `YYYY-MM-DD.pdf`.
- **Note:** For the active/current year, files are stored directly in the root of `Abhi\`, while completed past years are grouped in `{YEAR}\` subfolders.

### Rule 10: Car & Transport
- **FasTrak:** `C:\Users\basua\Dropbox\Documents\Car\FasTrak\YYYY-MM-DD.pdf`.
- **Tickets:** `C:\Users\basua\Dropbox\Documents\Car\Tickets\`
  - **Naming:** `YYYY-MM-DD - Description (Vendor).pdf` or `YYYY-MM-DD - Traffic Ticket (Comune di Pienza).pdf` for parking/traffic violations.
- **Travelers Auto Insurance:** `C:\Users\basua\Dropbox\Documents\Car\Travelers\`
  - **Naming:** `YYYY-MM-DD - Premium payment {YEAR}.pdf` or `YYYY-MM-DD - Billing Notice.pdf`.

### Rule 11: Taxes
- **Destination:** `C:\Users\basua\Dropbox\Money\Tax\Abhi\YA{YEAR}\Documents\`
- **Naming:** Follow precedent: `{Owner} - {Entity} - {Form/Type}.pdf` (e.g., `Abhi - Fidelity (HSA) - 5498-SA.pdf`).

### Rule 12: Travel
- **Destination:** `C:\Users\basua\Dropbox\Travel\{YYYY-MM - Destination}\`
- **Naming:** `YYYY-MM-DD - Description (Details).pdf`.
- **Deduplication:** Always check if a flight confirmation is an update to an existing booking.

### Rule 13: Software Installers
- **Destination:** `C:\Users\basua\Dropbox\Software\To Install\`
- **Naming:** Keep original installer name (e.g. `Antigravity-x64.exe`).

### Rule 14: Fog City Advisors
- **Destination:** `C:\Users\basua\Dropbox\Money\Fog City Advisors\`
- **Naming:** `YYYY-MM-DD - Invoice {Number}.pdf` or `YYYY-MM-DD - Payment receipt.pdf` for advisory fees.
