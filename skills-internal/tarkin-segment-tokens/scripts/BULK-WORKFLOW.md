# Bulk Add from CSV/List Grouped by Product Type

When the user provides a list of serial numbers with product types (e.g., from a Jira ticket CSV), follow this workflow:

1. **Parse the data** and group serial numbers by product type (e.g., T2B, T3A, X2, etc.)
2. **Search for matching segments** using `get-segment.sh --name "<PRODUCT_TYPE> EFFA - DO NOT UPDATE"` for each product type
3. **Report any product types with no matching segment** — do not create segments unless asked
4. **MANDATORY: Present a summary and ask user to confirm before proceeding.** The summary must include:
   - **Environment** (staging or production)
   - For each product type group:
     - Number of serial numbers
     - Target segment name and ID
   - Any product types that will be **skipped** (no matching segment found)
5. **Only proceed after explicit user confirmation**

```
User: Add these serial numbers from TARKIN-3044 to their EFFA segments on staging

Agent: [parses CSV, groups by PRODUCT_TYPE, searches for segments]

Here's the plan — please confirm:

Environment: staging

| Product Type | Count | Target Segment                  | Segment ID |
|-------------|-------|---------------------------------|------------|
| T3A         | 47    | T3a EFFA - DO NOT UPDATE        | 55         |
| T2B         | 1     | ⚠️ No matching segment found    | —          |

T2B serial numbers will be skipped. Proceed?

User: yes

[runs update-segment-tokens.sh for each group with a matching segment]
```

## Segment Naming Conventions

- **EFFA segments** follow the pattern: `<PRODUCT_TYPE> EFFA - DO NOT UPDATE`
  - Examples: `T3a EFFA - DO NOT UPDATE`, `T2B EFFA - DO NOT UPDATE`, `X2 EFFA - DO NOT UPDATE`
- When a user references an EFFA segment by product/device type (e.g., "T1B EFFA segment"), infer the full name as `T1B EFFA - DO NOT UPDATE` and use `get-segment.sh --name` to look it up
