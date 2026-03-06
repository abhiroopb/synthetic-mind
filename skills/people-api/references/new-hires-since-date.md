# Get new hires since a date

```bash
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://my.sqprod.co/people/api/all.json?since=2026-01-01&sort=started_at&dir=desc" | python3 -c "
import sys, json
for p in json.load(sys.stdin):
    print(f\"{p['start_date']} {p['preferred_first_name']} {p['last_name']} ({p['username']})\")
"
```
