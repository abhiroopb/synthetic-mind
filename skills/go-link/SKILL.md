---
Skill name: go-link
Skill description: Translate internal shortlinks (like go/benefits, go/oncall) to full URLs. Use when user mentions go/ links, shortlinks, or asks to navigate/fetch URLs starting with "go/".
roles: [frontend]
---

# Shortlink Navigation

Navigate to or fetch internal shortlinks by translating them to their full URL. The browser may not have the shortlink extension installed, so this skill handles the translation.

## URL Translation Rule

- Base URL: `https://go.example.com/`
- `go/path` or just `path` becomes `https://go.example.com/path`

## Instructions

1. **Parse the shortlink**:
   - If the link starts with "go/", strip that prefix
   - Extract the path (e.g., "benefits" from "go/benefits")

2. **Construct the full URL**:
   - Full URL: `https://go.example.com/{path}`

3. **Navigate or fetch** based on context:
   - If the user wants to view the page interactively, use browser navigation to open it
   - If the user wants information from the page, fetch the content

4. **Report the translation** to the user so they know what URL was accessed.

## Examples

| Input | Translated URL |
|-------|---------------|
| `go/benefits` | `https://go.example.com/benefits` |
| `go/oncall/schedule` | `https://go.example.com/oncall/schedule` |
| `go/wiki/engineering` | `https://go.example.com/wiki/engineering` |
