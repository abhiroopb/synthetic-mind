# Common Issues and Debugging

## URL Encoding Issues

### Spaces in Table Names

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/My Table"

curl "https://api.airtable.com/v0/${BASE_ID}/My%20Table"

curl -G "https://api.airtable.com/v0/${BASE_ID}/My Table" \
  -d "fields[]=Name"
```

### Special Characters

Characters that need URL encoding:
- Space: ` ` → `%20`
- Forward slash: `/` → `%2F`
- Question mark: `?` → `%3F`
- Ampersand: `&` → `%26`
- Hash: `#` → `%23`
- Plus: `+` → `%2B`

### Automatic Encoding with curl

Use `-G` flag with `-d` or `--data-urlencode` for automatic encoding:

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/My Table Name" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "fields[]=Field Name" \
  -d "fields[]=Another Field"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=AND({Status}='Active', {Name}='Test')"
```

### Using Table IDs Instead

To avoid encoding issues, use table IDs:

```bash
curl "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.tables[] | {name: .name, id: .id}'

curl "https://api.airtable.com/v0/${BASE_ID}/tblXXXXXXXXXXXXXX" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Filter Formula Errors

### Debug Formula Syntax

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Status}='Active'" \
  -w "\nHTTP Status: %{http_code}\n"
```

### Common Formula Mistakes

#### String Literals

**Wrong:**
```bash
--data-urlencode "filterByFormula={Status}=Active"
```

**Correct:**
```bash
--data-urlencode "filterByFormula={Status}='Active'"
```

#### Field Names

**Wrong:**
```bash
--data-urlencode "filterByFormula=Status='Active'"
```

**Correct:**
```bash
--data-urlencode "filterByFormula={Status}='Active'"
```

#### Comparison Operators

**Wrong:**
```bash
--data-urlencode "filterByFormula={Count}=='10'"
```

**Correct:**
```bash
--data-urlencode "filterByFormula={Count}=10"
```

### Formula Testing Tips

1. **Test in Airtable UI first**: Create a formula field in Airtable to verify syntax
2. **Use simple formulas initially**: Start with basic conditions, then add complexity
3. **Check field names**: Formula field names are case-sensitive
4. **Use --data-urlencode**: Always use this flag to properly encode formulas

### Complex Formula Examples

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=AND({Status}='Active',IS_AFTER({Date},'2024-01-01'))"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=OR(SEARCH('keyword',{Description}),SEARCH('keyword',{Notes}))"
```

## Empty or Missing Records

### Check Pagination

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.offset'

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "offset=itrXXXXXXXXXXXXXX"
```

### Verify Filters

If no records are returned, check your filter:

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Status}='Active'"
```

### Check Views

By default, API returns records from the first view. Specify a view if needed:

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "view=Grid%20view"
```

### Pagination Loop

```bash
#!/bin/bash

offset=""
while : ; do
  if [ -z "$offset" ]; then
    response=$(curl -s "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
      -H "Authorization: Bearer $AIRTABLE_TOKEN")
  else
    response=$(curl -s -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
      -H "Authorization: Bearer $AIRTABLE_TOKEN" \
      -d "offset=$offset")
  fi
  
  echo "$response" | jq '.records[]'
  
  offset=$(echo "$response" | jq -r '.offset // empty')
  
  [ -z "$offset" ] && break
  
  sleep 0.2
done
```

## Debugging Tips

### Verbose Output

```bash
curl -v "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### Pretty Print JSON

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.'

curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.records[] | {id: .id, fields: .fields}'
```

### Save Response to File

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -o response.json

cat response.json | jq '.'
```

### Test with Minimal Payload

```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Name":"Test"}}' \
  -w "\nStatus: %{http_code}\n"
```

### Check HTTP Status Code

```bash
curl -s -w "\nHTTP Status: %{http_code}\n" \
  "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### View Request/Response Headers

```bash
curl -i "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### Validate JSON

```bash
echo '{"fields":{"Name":"Test"}}' | jq '.'

cat payload.json | jq '.'
```

### Debug Script with set -x

```bash
#!/bin/bash
set -x

curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"

set +x
```

## Common HTTP Status Codes

- **200 OK**: Successful GET/DELETE request
- **201 Created**: Successful POST request
- **400 Bad Request**: Malformed JSON or invalid syntax
- **401 Unauthorized**: Authentication failed
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Base or table doesn't exist
- **422 Unprocessable Entity**: Invalid field names, types, or values
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Airtable service issue
- **503 Service Unavailable**: Airtable service temporarily unavailable

## Troubleshooting Checklist

1. ✓ Token is set and valid
2. ✓ Base ID is correct
3. ✓ Table name is properly URL-encoded or using table ID
4. ✓ Field names match exactly (case-sensitive)
5. ✓ Data types match field configurations
6. ✓ Required fields are included
7. ✓ JSON syntax is valid
8. ✓ Rate limits are respected
9. ✓ Formulas are properly encoded
10. ✓ Record IDs are valid format

## Reference

See the [API Error Reference](https://airtable.com/developers/web/api/errors) for complete error code documentation.
