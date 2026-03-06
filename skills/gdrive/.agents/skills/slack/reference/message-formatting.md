# Message formatting reference

The `post-message` command accepts a `--format` option to control how the
content argument is interpreted.

## `--format markdown` (default)

Just write standard Markdown. The text is sent as a native Slack
[`markdown` block](https://api.slack.com/reference/block-kit/blocks/markdown-block),
which Slack renders server-side into proper `rich_text` blocks. This gives you
semantic bulleted lists, numbered lists, blockquotes, code blocks, and inline
formatting - all from plain Markdown.

Supported features:

- **Bold**, *italic*, ~~strikethrough~~, inline `code`
- Links: `[text](url)`
- Headings: `#` through `######`
- Bulleted lists: `- item` or `* item` (rendered as proper `rich_text_list`)
- Numbered lists: `1. item` (rendered as proper `rich_text_list`)
- Code blocks: fenced with triple backticks
- Blockquotes: `> text`

Limitations:

- No table support (use `--format json` with Block Kit for tables)
- No task lists / checkboxes
- No horizontal rules
- No syntax highlighting in code blocks
- 12,000 character cumulative limit across all `markdown` blocks in a message

## `--format mrkdwn`

Text is sent directly to Slack with no conversion. Use this when you've already
composed text in
[Slack mrkdwn](https://api.slack.com/reference/surfaces/formatting) format.

Quick reference:

| Element | Slack mrkdwn syntax |
|---------|-------------------|
| Bold | `*text*` |
| Italic | `_text_` |
| Strikethrough | `~text~` |
| Inline code | `` `text` `` |
| Code block | ` ```text``` ` |
| Blockquote | `> text` |
| Link | `<https://url\|display text>` |
| User mention | `<@U1234567890>` |
| Channel link | `<#C1234567890>` |

Slack mrkdwn does NOT support: headings, tables, images, or nested/semantic
lists. For those, use `--format json` with Block Kit.

See: https://api.slack.com/reference/surfaces/formatting

## `--format json`

The content argument is parsed as a JSON array of
[Block Kit](https://api.slack.com/block-kit) blocks. This enables rich layouts
that mrkdwn cannot express: headers, tables, semantic bulleted/numbered lists,
two-column fields, interactive elements, and more.

**IMPORTANT: Before constructing Block Kit JSON, read
[block-kit.md](block-kit.md) for the correct schema.
Do not rely on memory — Block Kit schemas are easy to get wrong.**

Available block types:

| Block type | Use for |
|------------|---------|
| `header` | Large bold heading text |
| `section` | Text paragraphs, two-column `fields` |
| `rich_text` | Formatted text, semantic lists, quotes, code blocks |
| `table` | Native tabular data (one per message) |
| `divider` | Horizontal rule separator |
| `context` | Small grey metadata text |
| `image` | Inline images |
| `actions` | Buttons, selects (requires interaction handling) |

For detailed documentation and examples of each, see
[block-kit.md](block-kit.md).
