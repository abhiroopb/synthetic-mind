---
name: eng-ai-chat
description: Searches internal company knowledge grounded in application context. Use when the you need company-specific information about apps, services, infrastructure, integrations, or platform guidance for Cash Cloud (CAKE) or SKI (Square). Retrieves and synthesizes information from multiple sources including AI-generated summaries, dev guides, code search results, Google Docs, and internal knowledge bases to provide comprehensive answers.
roles: [backend, frontend, mobile, data]
allowed-tools: [Bash(sq:*)]
---

# Company Knowledge Search

Search internal company knowledge grounded in application context using `sq ai-app-context`.

## Workflow

1. **Identify app slugs**:

   If the user mentions specific app names, use those as `--app` values.
   Otherwise, discover potential apps from the current repo:

   ```bash
   sq ai-app-context discover-apps --path .
   ```

   Use the output to identify the most relevant app slug(s) for the query.

2. **Search with app context**: Run the search with one or more `--app` flags:

   ```bash
   sq ai-app-context company-search "<natural language question>" --app <app-slug>
   ```

   For queries spanning multiple apps:

   ```bash
   sq ai-app-context company-search "<question>" --app <app1> --app <app2>
   ```

3. **Synthesize results**: Read the output carefully. Present a clear answer
   grounded in the returned sources. If results are insufficient, refine the
   query and/or adjust app context; state uncertainty rather than guessing.

## Examples

```bash
# Single app query
sq ai-app-context company-search "How can I add a second deployment to paragon? I'm trying to ship a new paragon-jobs deployment for running background jobs." --app paragon

# Multi-app integration question
sq ai-app-context company-search "How can I integrate with multipass for paragon? I'm trying to have paragon query multipass for session validation." --app paragon --app multipass

# Discover apps first, then search
sq ai-app-context discover-apps --path .
sq ai-app-context company-search "How do I <question> <discovered-app>? <include-goal>" --app "<discovered-app>"
```

## Tips

- Formulate queries as natural language with high level of detail for best results.
- If results seem incomplete, try rephrasing the query with more details.
- Use subagents to ask multiple questions at the same time. The search can take 5 minutes.
