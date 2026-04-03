---
name: go-link
description: Use when translating, navigating, fetching, opening, resolving, looking up, or browsing internal go/ links (like go/benefits, go/oncall) to full URLs via a URL shortener service.
---

# Go Link Navigation

Navigate to or fetch internal go/ links by translating them to their full URL. The browser may not have the go/ link extension installed, so this skill handles the translation.

## URL Translation Rule

- Base URL: `https://go.your-company.com/`
- `go/path` or just `path` becomes `https://go.your-company.com/path`

## Instructions

1. **Parse the go/ link**:
   - If the link starts with "go/", strip that prefix
   - Extract the path (e.g., "benefits" from "go/benefits")

2. **Construct the full URL**:
   - Full URL: `https://go.your-company.com/{path}`

3. **Navigate or fetch** based on context:
   - If the user wants to view the page interactively, use browser navigation to open it
   - If the user wants information from the page, fetch the content

4. **Report the translation** to the user so they know what URL was accessed.

## Examples

| Input | Translated URL |
|-------|---------------|
| `go/benefits` | `https://go.your-company.com/benefits` |
| `go/oncall/schedule` | `https://go.your-company.com/oncall/schedule` |
| `go/wiki/engineering` | `https://go.your-company.com/wiki/engineering` |

## Customization

Replace `https://go.your-company.com/` with your organization's URL shortener base URL (e.g., GoLinks, go/ service, or similar).
