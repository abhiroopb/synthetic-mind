---
Skill name: web-research
Skill description: Search the web and synthesize external information on a topic. Use when researching competitors, market context, industry trends, best practices, technical concepts, or any external information needed to inform PRDs, specs, strategy docs, or decision-making.
---

# Web Research

Search the web, pull in relevant content, and synthesize findings into a structured research brief. Designed to complement PRD-writing and spec-creation workflows by providing external context — competitor analysis, market trends, industry benchmarks, best practices, and technical reference material.

## When to Use

- Researching competitors or comparable products before writing a PRD
- Gathering market context, industry trends, or benchmarks for a feature area
- Finding best practices or design patterns for a UX/product decision
- Looking up technical concepts, API docs, or platform capabilities
- Answering "how do others solve this?" or "what's the state of the art?"
- Augmenting internal research (Slack, Snowflake, Glean) with external perspective

## Workflow

### 1. Clarify the Research Goal

Identify from the user's request:
- **Topic**: What are we researching?
- **Purpose**: Why? (e.g., PRD background, competitive analysis, technical feasibility)
- **Scope**: Broad landscape scan or deep dive on a specific question?
- **Output format**: Research brief, comparison table, bullet summary, or raw findings?

If the purpose is unclear, ask one focused question. Default to a structured research brief.

### 2. Generate Search Queries

From the topic, generate 3–7 diverse search queries that cover:
- **Direct queries**: The topic itself (e.g., "Square competitors checkout flow")
- **Comparative queries**: "best [category] solutions 2025", "[competitor] vs [competitor]"
- **Technical queries**: Implementation details, API docs, platform specifics
- **Trend queries**: "state of [industry] 2025", "[topic] market trends"

Use `web_search` with each query. Set `max_results` to 5–8 per query.

### 3. Read and Extract

For the most promising results (top 5–10 across all queries):
- Use `read_web_page` with a focused `objective` to extract only relevant content
- Skip paywalled, login-gated, or low-quality sources
- Prioritize: official docs, reputable publications, industry reports, product pages

### 4. Synthesize Findings

Compile findings into a structured research brief:

```markdown
# Web Research: <Topic>

**Research goal**: <one-line purpose>
**Date**: <today's date>
**Queries used**: <list of search queries>

## Key Findings

### <Finding Category 1> (e.g., Competitor Landscape)
- **[Source Name](URL)**: <key insight or data point>
- **[Source Name](URL)**: <key insight or data point>

### <Finding Category 2> (e.g., Best Practices)
- **[Source Name](URL)**: <key insight or data point>

### <Finding Category 3> (e.g., Market Data)
- **[Source Name](URL)**: <key insight or data point>

## Summary

<3–5 sentence synthesis of the most important takeaways>

## Relevance to <Purpose>

<How these findings inform the PRD/spec/decision — specific recommendations>

## Sources

| # | Source | URL | Relevance |
|---|--------|-----|-----------|
| 1 | [Name] | [URL] | [Why it matters] |
```

### 5. Present and Offer Next Steps

After presenting the brief, offer:
- "Want me to deep-dive on any of these findings?"
- "Want me to use these findings to start a PRD?" (→ load `writing-requirements-docs`)
- "Want me to save this research to a file?"

If the user wants to save, write to `research/<topic-kebab-case>/WEB-RESEARCH.md` in the current working directory.

## Integration with Other Skills

This skill is designed to chain with:
- **writing-requirements-docs**: Provide external context for Problem Statement (§1), competitive landscape for Non-Goals (§3), and market data for Goals (§2)
- **spec-creator**: Supply technical research and best practices
- **feedback-searcher**: Complement internal seller feedback with external market perspective
- **prototype-builder**: Research UI patterns and competitor implementations before building

When called as part of a PRD workflow, skip the standalone brief format and return findings as inline-ready content (quoted with source links) that the calling skill can weave directly into the document.

## Quality Standards

- **Every claim must have a source link.** No unsourced assertions.
- **Prefer recent sources.** Prioritize content from the last 12 months.
- **Distinguish facts from opinions.** Label analyst opinions, projections, and estimates clearly.
- **Be concise.** Summarize; don't dump raw page content.
- **Note gaps.** If a question couldn't be answered from web sources, say so explicitly.

## Anti-patterns

- Don't return raw search results without reading and synthesizing
- Don't include sources that are paywalled or inaccessible
- Don't present speculation as fact
- Don't over-research — aim for 5–10 high-quality sources, not 50 mediocre ones
- Don't skip source attribution — every finding needs a clickable URL
