# Issue Template

Use this template when formatting issues. Each issue should be self-contained enough for a future agent to execute without the original planning context.

```markdown
## Context

[1-2 paragraphs explaining the background. Include enough context that someone unfamiliar with the plan can understand why this work matters.]

## Objective

[Single clear sentence: "Implement X that does Y so that Z"]

## Acceptance Criteria

- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

## Relevant Code

| File | Purpose |
|------|---------|
| `src/path/file.ts` | [What's there, what needs to change] |

## Technical Notes

[Any implementation hints, gotchas, or decisions from the plan]

## Dependencies

- **Blocked by**: None / ISSUE-XXX
- **Blocks**: None / ISSUE-YYY

---
*Created from plan via plan-to-linear skill*
*Source: [thread URL or doc link]*
```

## Tips for Good Issues

1. **Be specific**: "Update `validateToken()` in `auth.ts` to check expiry" not "fix auth"
2. **Include file paths**: Future agents need to know where to look
3. **Define done**: Acceptance criteria should be checkable
4. **Explain why**: Context prevents wrong solutions
5. **Note dependencies**: Order matters for execution

## Thread URLs and Visibility

**Important**: Thread URLs (e.g. from Amp) may only be accessible to the original user. Always include the actual context in the issue description. Use thread URLs for traceability, not as the primary source of information.
