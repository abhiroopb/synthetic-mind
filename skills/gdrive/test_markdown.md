# Markdown Converter Test Document

A comprehensive test of all markdown formatting features.

## Text Formatting

### Basic Styles

The formatter supports **bold**, *italic*, and ***bold italic*** text. You can also use `inline code` for technical terms.

### Links

Links work in two ways:

- Explicit markdown links: [Google Docs API](https://developers.google.com/docs/api)
- Bare URLs are auto-detected: https://github.com/anthropics/claude-code

---

## Code

### Inline Code

Use backticks for `variable_names`, `function_calls()`, and `CommandLineArgs`.

### Code Blocks

For longer code samples, use fenced code blocks:

```python
def convert_markdown(content: str, doc_id: str) -> dict:
    """Convert markdown and append to a Google Doc."""
    requests = parse_markdown(content)
    return docs_service.batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()
```

---

## Lists

### Bullet Lists

Key features of this tool:

- Simple and intuitive syntax
- Supports nested formatting like **bold** and `code`
- Links work too: [Documentation](https://docs.example.com)
- Multiple paragraphs supported

### Numbered Lists

Steps to use the converter:

1. Parse the markdown into an AST
2. Walk the tree and collect formatting ranges
3. Generate Google Docs API requests
4. Apply all changes in a single batch update

---

## Tables

### Feature Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| Headings | Yes | H1 through H6 |
| Bold | Yes | Double asterisks |
| Italic | Yes | Single asterisks |
| Links | Yes | Explicit and auto-detect |
| Code | Yes | Inline and blocks |

### Status Table

| Component | Status | Owner |
|-----------|--------|-------|
| Parser | Complete | Team A |
| Formatter | Complete | Team B |
| Tables | Complete | Team C |
| Testing | In Progress | Team D |

### Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Latency | 120ms | <200ms |
| Success Rate | 99.9% | >99% |
| Coverage | 85% | >80% |

---

## Block Quotes

> Block quotes are rendered in italics, making them useful for callouts or citations.

---

## Mixed Content

This section tests **bold with [links](https://example.com)** and *italic with `code`* together.

Here's a table followed immediately by text:

| A | B |
|---|---|
| 1 | 2 |

And here's more text with a [link](https://google.com) after the table.

---

## Resources

For more information:

- API Reference: https://developers.google.com/docs/api/reference/rest
- Source Code: https://github.com/anthropics/claude-code
- Issue Tracker: https://github.com/anthropics/claude-code/issues

---

*Document generated using the gdrive skill markdown formatter.*
