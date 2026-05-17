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
- **Ignore Subfolders:** Only process files at the top level of the Downloads folder.
- **Folder Creation:** Follow established patterns. Do NOT create year folders for Utilities or Zareen's medical bills.
- **Description:** For medical/health bills, always include a brief description of the service (e.g., "Sutter Bill for Injured Elbow").

## Rules

### Rule 1: Purchase Receipts (Non-Home)
- **Destination:** `C:\Users\basua\Dropbox\Money\Receipts\{YEAR}\`
- **Naming:** `YYYY-MM-DD - Item Name (Business Name).pdf`

### Rule 2: Home Contractor Documents (2424 Tulare Ave)
- **Destination:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Contractors\{Contractor Name}\`
- **Naming:** `YYYY-MM-DD - Description.pdf`

### Rule 3: Bank & Brokerage Statements
- **Destination:** `C:\Users\basua\Dropbox\Money\Banks\{Bank Name}\{Account Folder}\Statements\`
- **Naming:** `YYYY-MM-DD.pdf` (statement end date).

### Rule 4: Utilities (2424 Tulare Ave)
- **Destination:** `C:\Users\basua\Dropbox\Documents\2424 Tulare Ave\Utilities\{Utility Name}\`
- **Naming:** `YYYY-MM-DD.pdf`
- **EBSAN:** `EBSAN\Statement\`.
- **EBMUD:** `EBMUD/`.
- **PG&E:** `PG&E/`.
- **Sonic:** `Sonic/`.

### Rule 5: Pay Stubs & Employment
- **Destination:** `C:\Users\basua\Dropbox\Money\Payslips\Abhi\{YEAR}\`
- **Naming:** `YYYY-MM-DD.pdf`.

### Rule 6: Car & Transport
- **FasTrak:** `C:\Users\basua\Dropbox\Documents\Car\FasTrak\YYYY-MM-DD.pdf`.

### Rule 7: Insurance & Health
- **Dental EOBs (Abhi):** `C:\Users\basua\Dropbox\Documents\Health\Abhi\Dental\YYYY-MM-DD - Delta Dental.pdf` (No "EOB" in name).
- **Aetna EOBs (Zareen):** `C:\Users\basua\Dropbox\Documents\Health\Zareen\Bill Payments\YYYY-MM-DD - Aetna EOB.pdf`.
- **Health Visits (Abhi):** `C:\Users\basua\Dropbox\Documents\Health\Abhi\Visits\YYYY-MM-DD - Description.pdf`.
- **Bill Payments (Zareen):** `C:\Users\basua\Dropbox\Documents\Health\Zareen\Bill Payments\YYYY-MM-DD - Description.pdf`. (No "Health" prefix, no year folders).

### Rule 8: Taxes
- **Destination:** `C:\Users\basua\Dropbox\Money\Tax\Abhi\YA{YEAR}\Documents\`
- **Naming:** Follow precedent: `{Owner} - {Entity} - {Form/Type}.pdf` (e.g., `Abhi - Fidelity (HSA) - 5498-SA.pdf`).

### Rule 9: Travel
- **Destination:** `C:\Users\basua\Dropbox\Travel\{YYYY-MM - Destination}\`
- **Naming:** `YYYY-MM-DD - Description (Details).pdf`.
- **Deduplication:** Always check if a flight confirmation is an update to an existing booking.
