# Google Docs API Quick Reference

## Tab Operations (via batch-update)

| Operation | Request Type | Key Detail |
|-----------|-------------|------------|
| Rename tab | `updateDocumentTabProperties` | `tabId` goes INSIDE `tabProperties` |
| Create tab | `addDocumentTab` | NOT `createTab` |
| Delete tab | `deleteDocumentTab` | |
| Clear content | `deleteContentRange` | Use `endIndex - 1` with `tabId` |

## Writing Content

```bash
cat << 'MDEOF' | uv run gdrive-cli.py docs insert-markdown <doc-id> --tab <tab-id>
<markdown content>
MDEOF
```

## Getting Content End Index

```bash
uv run gdrive-cli.py docs get <doc-id> | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tab in data.get('tabs', []):
    props = tab.get('tabProperties', {})
    body = tab.get('documentTab', {}).get('body', {})
    content = body.get('content', [])
    end_idx = content[-1]['endIndex'] if content else 1
    print(f'Tab: {props.get(\"title\")} (id={props.get(\"tabId\")}) endIndex={end_idx}')
"
```

## Extracting Rich Links

Google Docs stores embedded document links as `richLink` objects, not in `textRun` hyperlinks:

```bash
uv run gdrive-cli.py docs get <doc-id> | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tab in data.get('tabs', []):
    body = tab.get('documentTab', {}).get('body', {})
    for elem in body.get('content', []):
        for el in elem.get('paragraph', {}).get('elements', []):
            if 'richLink' in el:
                rl = el['richLink'].get('richLinkProperties', {})
                print(f'{rl.get(\"title\", \"\")} -> {rl.get(\"uri\", \"\")}')
"
```
