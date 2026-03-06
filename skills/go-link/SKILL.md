---
name: go-link
description: Translate internal go/ links (like go/benefits, go/oncall) to full URLs at https://go.sqprod.co/. Use when user mentions go/ links, go links, internal shortlinks, or asks to navigate/fetch URLs starting with "go/".
roles: [frontend]
---

# Go Link Navigation

Navigate to or fetch internal go/ links by translating them to their full URL. The browser may not have the go/ link extension installed, so this skill handles the translation.

## URL Translation Rule

- Base URL: `https://go.sqprod.co/`
- `go/path` or just `path` becomes `https://go.sqprod.co/path`

## Instructions

1. **Parse the go/ link**:
   - If the link starts with "go/", strip that prefix
   - Extract the path (e.g., "benefits" from "go/benefits")

2. **Construct the full URL**:
   - Full URL: `https://go.sqprod.co/{path}`

3. **Navigate or fetch** based on context:
   - If the user wants to view the page interactively, use browser navigation to open it
   - If the user wants information from the page, fetch the content

4. **Report the translation** to the user so they know what URL was accessed.

## Examples

| Input | Translated URL |
|-------|---------------|
| `go/benefits` | `https://go.sqprod.co/benefits` |
| `go/oncall/schedule` | `https://go.sqprod.co/oncall/schedule` |
| `go/wiki/engineering` | `https://go.sqprod.co/wiki/engineering` |
