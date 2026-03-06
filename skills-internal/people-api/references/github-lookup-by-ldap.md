# Look up GitHub username by LDAP

```bash
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://internal-api.example.com" | python3 -c "
import sys, json; d = json.load(sys.stdin)
print(f\"{d['preferred_first_name']} {d['last_name']}: github={d.get('github')}\")
"
```
