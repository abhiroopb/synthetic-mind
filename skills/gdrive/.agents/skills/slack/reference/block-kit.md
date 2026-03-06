# Block Kit reference

Block Kit is Slack's JSON-based UI framework for rich message layouts.
Use it via `--format json`, passing a JSON array of blocks as `--text`.

Official docs: https://api.slack.com/reference/block-kit/blocks

Slack also publishes an LLM-optimized developer reference (covers more than
just Block Kit): https://docs.slack.dev/llms.txt

---

## Block types

| Block type | Purpose |
|------------|---------|
| `header` | Large bold heading (`plain_text` only, max 150 chars) |
| `section` | Text paragraph (supports `mrkdwn`); optional two-column `fields` and an accessory element |
| `rich_text` | Structured rich text with proper lists, quotes, code blocks |
| `divider` | Horizontal separator |
| `context` | Small footnote-style text (up to 10 elements) |
| `image` | Embedded image via `image_url`; requires `alt_text` |
| `table` | Tabular data (max 100 rows, 20 columns). Only one table per message; rendered as an attachment at the bottom |
| `actions` | Interactive elements (buttons, menus, pickers); requires interaction handling |
| `video` | Embedded video with thumbnail; requires `links.embed:write` scope |
| `file` | Remote file reference (read-only; appears when retrieving messages with files, not directly postable) |
| `markdown` | Native Markdown text (same as `--format markdown` uses under the hood) |

---

## `header`

Large bold heading. Only supports `plain_text` (no mrkdwn), max 150 characters.

```json
{"type": "header", "text": {"type": "plain_text", "text": "Status update"}}
```

## `section`

Versatile text block. Supports `mrkdwn` text, optional two-column `fields`
array, and an optional `accessory` element (button, image, etc.).

```json
{"type": "section", "text": {"type": "mrkdwn", "text": "*Environment:* production"}}
```

With fields (two-column layout):

```json
{"type": "section", "fields": [
  {"type": "mrkdwn", "text": "*Status:*\nHealthy"},
  {"type": "mrkdwn", "text": "*Region:*\nus-east-1"}
]}
```

## `rich_text`

Structured rich text — the native format Slack's composer produces. Contains
an `elements` array of sub-elements:

| Sub-element | Purpose |
|-------------|---------|
| `rich_text_section` | Inline text run (bold, italic, code, links) |
| `rich_text_list` | Bulleted or numbered list |
| `rich_text_quote` | Blockquote |
| `rich_text_preformatted` | Code block |

Inline elements within sections support a `style` object with `bold`,
`italic`, `strike`, and `code` booleans.
Links use `{"type": "link", "url": "...", "text": "..."}`.

### Bulleted list

```json
{"type": "rich_text", "elements": [
  {"type": "rich_text_list", "style": "bullet", "elements": [
    {"type": "rich_text_section", "elements": [{"type": "text", "text": "First item"}]},
    {"type": "rich_text_section", "elements": [{"type": "text", "text": "Second item"}]}
  ]}
]}
```

### Numbered list

```json
{"type": "rich_text", "elements": [
  {"type": "rich_text_list", "style": "ordered", "elements": [
    {"type": "rich_text_section", "elements": [{"type": "text", "text": "Step one"}]},
    {"type": "rich_text_section", "elements": [{"type": "text", "text": "Step two"}]}
  ]}
]}
```

### Inline formatting

```json
{"type": "rich_text", "elements": [
  {"type": "rich_text_section", "elements": [
    {"type": "text", "text": "This is "},
    {"type": "text", "text": "bold", "style": {"bold": true}},
    {"type": "text", "text": " and "},
    {"type": "link", "url": "https://example.com", "text": "a link"}
  ]}
]}
```

### Blockquote

```json
{"type": "rich_text", "elements": [
  {"type": "rich_text_quote", "elements": [
    {"type": "text", "text": "To be or not to be"}
  ]}
]}
```

### Code block

```json
{"type": "rich_text", "elements": [
  {"type": "rich_text_preformatted", "elements": [
    {"type": "text", "text": "def hello():\n    print('world')"}
  ]}
]}
```

## `divider`

Horizontal separator. No content.

```json
{"type": "divider"}
```

## `context`

Small supplementary text displayed in lighter style. Up to 10 elements
(mix of `plain_text`, `mrkdwn`, and `image`).

```json
{"type": "context", "elements": [
  {"type": "mrkdwn", "text": "Last updated: 2026-02-24 at 10:30 AEDT"}
]}
```

## `image`

Embedded image. Requires `image_url` and `alt_text`.

```json
{"type": "image", "image_url": "https://example.com/chart.png", "alt_text": "Traffic chart"}
```

## `table`

Tabular data. Constraints:

- Only **one table per message**
- Max 100 rows, 20 columns
- Rendered as an attachment at the bottom of the message, not inline
- Rows are arrays of cells; the first row is used as the header
- Cell types: `raw_text` (plain text) or `rich_text` (formatted text with links, bold, emoji, mentions)
- Optional `column_settings` array controls alignment (`left`/`center`/`right`) and wrapping (`is_wrapped`)

```json
{"type": "table", "rows": [
  [
    {"type": "raw_text", "text": "Topic"},
    {"type": "raw_text", "text": "Status"},
    {"type": "raw_text", "text": "Rows"}
  ],
  [
    {"type": "raw_text", "text": "payments"},
    {"type": "raw_text", "text": "Done"},
    {"type": "raw_text", "text": "1.2M"}
  ],
  [
    {"type": "raw_text", "text": "transfers"},
    {"type": "raw_text", "text": "In progress"},
    {"type": "raw_text", "text": "800K"}
  ]
]}
```

## `actions`

Container for interactive elements (buttons, select menus, date pickers).
Requires your app to handle interaction payloads.

```json
{"type": "actions", "elements": [
  {"type": "button", "text": {"type": "plain_text", "text": "Approve"}, "action_id": "approve", "style": "primary"},
  {"type": "button", "text": {"type": "plain_text", "text": "Reject"}, "action_id": "reject", "style": "danger"}
]}
```

## `markdown`

Native Markdown block — Slack renders it server-side into `rich_text` blocks.
This is the same mechanism `--format markdown` uses. Generally prefer
`--format markdown` over constructing these blocks manually.

---

## Combining blocks

A complete message typically combines several block types:

```json
[
  {"type": "header", "text": {"type": "plain_text", "text": "Deploy report"}},
  {"type": "section", "fields": [
    {"type": "mrkdwn", "text": "*Service:*\npayments-api"},
    {"type": "mrkdwn", "text": "*Environment:*\nproduction"}
  ]},
  {"type": "divider"},
  {"type": "rich_text", "elements": [
    {"type": "rich_text_list", "style": "bullet", "elements": [
      {"type": "rich_text_section", "elements": [{"type": "text", "text": "All health checks passing"}]},
      {"type": "rich_text_section", "elements": [{"type": "text", "text": "Latency within SLO"}]}
    ]}
  ]},
  {"type": "context", "elements": [
    {"type": "mrkdwn", "text": "Deployed by <@U123> at 2026-02-24 10:30 AEDT"}
  ]}
]
```
