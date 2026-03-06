# Search by partial name

```bash
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://my.sqprod.co/people/api/all.json?query=Charl+C" | python3 -m json.tool
```
