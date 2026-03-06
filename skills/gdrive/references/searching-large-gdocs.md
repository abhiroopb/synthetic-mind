# Searching Large Google Docs

The `read` command truncates documents over ~69KB. When that happens, use the structured `docs get` API to extract headings and retrieve specific sections:

**Step 1: List all headings to find relevant sections:**

```bash
uv run gdrive-cli.py docs get <doc-id> | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tab in data.get('tabs', []):
    body = tab.get('documentTab', {}).get('body', {})
    for elem in body.get('content', []):
        para = elem.get('paragraph', {})
        style = para.get('paragraphStyle', {})
        if style.get('namedStyleType', '').startswith('HEADING'):
            text = ''
            for el in para.get('elements', []):
                text += el.get('textRun', {}).get('content', '')
            print(f'[{style[\"namedStyleType\"]}] {text.strip()}')
"
```

**Step 2: Extract the content of a matching section** (replace `HEADING_TEXT` with the heading found in step 1):

```bash
uv run gdrive-cli.py docs get <doc-id> | python3 -c "
import sys, json
data = json.load(sys.stdin)
capture = False
result = []
for tab in data.get('tabs', []):
    body = tab.get('documentTab', {}).get('body', {})
    for elem in body.get('content', []):
        para = elem.get('paragraph', {})
        style = para.get('paragraphStyle', {})
        text = ''
        for el in para.get('elements', []):
            text += el.get('textRun', {}).get('content', '')
        if 'HEADING_TEXT' in text.strip():
            capture = True
        elif capture and style.get('namedStyleType', '').startswith('HEADING'):
            break
        if capture:
            result.append(text.rstrip())
print('\n'.join(result))
"
```

Run these commands from the gdrive skill directory (`~/.agents/skills/gdrive`).
