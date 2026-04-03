---
name: eng-ai-chat
description: Searches internal company knowledge grounded in application context. Use when searching, querying, looking up, finding, asking, investigating, or retrieving company-specific information about apps, services, infrastructure, integrations, or platform guidance. Retrieves and synthesizes information from multiple sources including AI-generated summaries, dev guides, code search results, docs, and internal knowledge bases.
---

# Company Knowledge Search

Search internal company knowledge grounded in application context using a company-search CLI.

## Prerequisites

Before running any commands, verify the CLI is available and authenticated:

```bash
company-search --help
```

If the command is not found or returns an authentication error, **STOP** and tell the user to install and authenticate.

## Workflow

1. **Identify app slugs**:

   If the user mentions specific app names, use those.
   Otherwise, discover potential apps from the current repo:

   ```bash
   company-search discover-apps --path .
   ```

   Use the output to identify the most relevant app slug(s) for the query.

2. **Search with app context**: Run the search with one or more `--app` flags:

   ```bash
   company-search "<natural language question>" --app <app-slug>
   ```

   For queries spanning multiple apps:

   ```bash
   company-search "<question>" --app <app1> --app <app2>
   ```

3. **Synthesize results**: Read the output carefully. Present a clear answer
   grounded in the returned sources. If results are insufficient, refine the
   query and/or adjust app context; state uncertainty rather than guessing.

## Examples

```bash
# Single app query
company-search "How can I add a second deployment to my-service? I'm trying to ship a new background jobs deployment." --app my-service

# Multi-app integration question
company-search "How can I integrate with auth-service for my-app? I'm trying to have my-app query auth-service for session validation." --app my-app --app auth-service

# Discover apps first, then search
company-search discover-apps --path .
company-search "How do I configure rate limiting for api-gateway?" --app api-gateway
```

## Tips

- Formulate queries as natural language with high level of detail for best results.
- If results seem incomplete, try rephrasing the query with more details.
- Use subagents to ask multiple questions at the same time. The search can take 5 minutes.
