# Google Docs URL Parsing

This document explains how to extract document IDs and tab IDs from Google Docs URLs.

## URL Formats

Google Docs URLs can be in edit or view mode, with optional tab and heading parameters:

```
https://docs.google.com/document/d/<doc-id>/edit
https://docs.google.com/document/d/<doc-id>/edit?tab=<tab-id>
https://docs.google.com/document/d/<doc-id>/edit?tab=<tab-id>#heading=h.xxx
https://docs.google.com/document/d/<doc-id>/view?tab=<tab-id>
```

**When a URL includes `?tab=`, always use `--tab` to fetch that specific tab.**

## Extraction

- **doc-id**: The string between `/d/` and `/edit` or `/view`
- **tab-id**: The value after `?tab=` (before `#` if present) - optional
- **heading**: Ignore the `#heading=` fragment - not needed for fetching

## Examples

Edit mode:
```
https://docs.google.com/document/d/1T-EnEF3PEippZa6qFO40OqQuaMd9QYJlzw36oMXVAMo/edit?tab=t.ralstp66hflk#heading=h.k4qjxc2yt4zk
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       ^^^^^^^^^^^^^^^
                                  doc-id                                              tab-id
```

View mode:
```
https://docs.google.com/document/d/1T-EnEF3PEippZa6qFO40OqQuaMd9QYJlzw36oMXVAMo/view?tab=t.ralstp66hflk
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^
                                  doc-id                                             tab-id
```

## Commands

```bash
# Read specific tab (use when URL has ?tab= parameter)
uv run gdrive-cli.py read 1T-EnEF3PEippZa6qFO40OqQuaMd9QYJlzw36oMXVAMo --tab t.ralstp66hflk

# List all tabs in a document
uv run gdrive-cli.py docs tabs 1T-EnEF3PEippZa6qFO40OqQuaMd9QYJlzw36oMXVAMo
```
