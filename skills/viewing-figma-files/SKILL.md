---
Skill name: viewing-figma-files
Skill description: View Figma files, inspect page/frame structure, export node images, and read comments via the Figma REST API. Use when asked to view, inspect, open, read, export, or describe a Figma file, frame, component, or design.
---

# Viewing Figma Files

View and inspect Figma files via the REST API. Supports file metadata, page/frame structure, node rendering, and comments.

## Authentication

The skill uses a **Figma Personal Access Token** stored at `~/.config/figma/token`.

If the token file doesn't exist, prompt the user:

> To use this skill you need a Figma personal access token.
> 1. Go to **Figma → Settings → Security → Personal access tokens**
> 2. Generate a token with the `file_content:read` scope
> 3. Save it:
> ```
> mkdir -p ~/.config/figma && echo "YOUR_TOKEN" > ~/.config/figma/token
> ```

The current token was created on 2026-02-28 and expires ~2026-05-29. If a request returns `403`, remind the user to regenerate.

Read the token:
```bash
FIGMA_TOKEN="$(cat ~/.config/figma/token 2>/dev/null)"
```

## Parsing Figma URLs

Users will typically paste a Figma URL. Extract the **file key** and optional **node ID**:

| URL pattern | File key | Node ID |
|---|---|---|
| `https://www.figma.com/design/<KEY>/...` | `<KEY>` | from `?node-id=X-Y` |
| `https://www.figma.com/file/<KEY>/...` | `<KEY>` | from `?node-id=X-Y` |
| `https://www.figma.com/proto/<KEY>/...` | `<KEY>` | from `?node-id=X-Y` |
| `https://www.figma.com/board/<KEY>/...` | `<KEY>` | — |

Node IDs in URLs use `-` as separator (e.g., `1-2`) but the API expects `:` (e.g., `1:2`). Always convert `-` → `:` in node IDs.

## Core API Calls

Base URL: `https://api.figma.com`

All requests use:
```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" "https://api.figma.com/v1/..."
```

### 1. File Metadata (lightweight)

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/meta"
```

Returns: name, folder, last touched, creator, thumbnail URL, editor type, role.

### 2. File Structure (pages + top-level frames)

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY?depth=2"
```

Use `depth=2` to get pages and their immediate children (frames/groups) without downloading the full tree. Present as a structured list:

```
📄 File: "My Design"
  📑 Page 1: "Home"
    🖼 Frame 1:2 — "Header"
    🖼 Frame 1:3 — "Hero Section"
    🖼 Frame 1:4 — "Footer"
  📑 Page 2: "Settings"
    🖼 Frame 2:1 — "Account Settings"
```

### 3. Specific Nodes

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE_IDS"
```

`NODE_IDS` is comma-separated (e.g., `1:2,1:3`). Returns detailed node JSON.

### 4. Render Node as Image

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images/$FILE_KEY?ids=$NODE_IDS&format=png&scale=2"
```

Returns a map of node IDs → image URLs (expire after 30 days). Download and display them:

```bash
curl -sL "$IMAGE_URL" -o /tmp/figma-node.png
```

Then use the `look_at` tool to view/describe the rendered image.

Supported formats: `png`, `jpg`, `svg`, `pdf`. Scale: `0.01`–`4` (default `1`, use `2` for retina).

### 5. File Comments

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/comments"
```

Returns all comments with author, message, timestamp, and associated node.

### 6. File Components

Components are included in the `GET /v1/files/:key` response under the `components` key. Use `depth=1` and parse the components map for a quick listing.

### 7. File Versions

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/versions"
```

Returns version history with labels, timestamps, and user info.

## Workflow

1. **Parse** the Figma URL or file key from the user's input.
2. **Check** for `~/.config/figma/token`. If missing, guide user to create one.
3. **Fetch metadata** first (lightweight, confirms access).
4. **Fetch structure** at `depth=2` to show pages and frames.
5. If the user wants to **see a specific frame/node**, render it as an image and display via `look_at`.
6. If the user asks about **comments**, fetch and present them.
7. If the user pastes a URL with a `node-id`, go directly to rendering that node.

## Tips

- Always use `depth=2` for initial file overview to avoid downloading massive file trees.
- Use `| python3 -m json.tool` to pretty-print JSON responses when debugging.
- Image URLs from the render endpoint expire after 30 days — don't store them long-term.
- For very large files, use the `ids` parameter to fetch only the nodes you need.
- Node IDs in Figma URLs use `-` (e.g., `1-2`), but the API expects `:` (e.g., `1:2`). Always convert.
