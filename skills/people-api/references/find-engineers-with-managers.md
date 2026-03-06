# Find Web Engineers with their managers

```bash
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://internal-api.example.com" | python3 -c "
import sys, json
for r in json.load(sys.stdin)['results']:
    lead = r.get('lead', {})
    print(f\"{r['username']}: {r.get('preferred_full_name')}, lead={lead.get('username') if lead else 'N/A'}\")
"
```
