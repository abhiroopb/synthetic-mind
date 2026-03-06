# Batch Operations with Rate Limiting

Efficiently process multiple records while respecting Airtable's rate limits.

## Basic Batch Update

```bash
#!/bin/bash

BASE_ID="your_base_id"
TABLE_NAME="{tableIdOrName}"

for batch in batch1 batch2 batch3; do
  curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "records": [
        {"id": "rec1", "fields": {"Status": "Updated"}},
        {"id": "rec2", "fields": {"Status": "Updated"}}
      ]
    }'
  
  sleep 0.2
done
```

## Batch Create Records

```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"fields": {"Name": "Record 1", "Status": "Active"}},
      {"fields": {"Name": "Record 2", "Status": "Active"}},
      {"fields": {"Name": "Record 3", "Status": "Active"}},
      {"fields": {"Name": "Record 4", "Status": "Active"}},
      {"fields": {"Name": "Record 5", "Status": "Active"}},
      {"fields": {"Name": "Record 6", "Status": "Active"}},
      {"fields": {"Name": "Record 7", "Status": "Active"}},
      {"fields": {"Name": "Record 8", "Status": "Active"}},
      {"fields": {"Name": "Record 9", "Status": "Active"}},
      {"fields": {"Name": "Record 10", "Status": "Active"}}
    ]
  }'
```

## Batch Update Records

```bash
curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"id": "recXXXXXXXXXXXXXX", "fields": {"Status": "Completed"}},
      {"id": "recYYYYYYYYYYYYYY", "fields": {"Status": "Completed"}},
      {"id": "recZZZZZZZZZZZZZZ", "fields": {"Status": "Completed"}}
    ]
  }'
```

## Batch Delete Records

```bash
curl -X DELETE "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}?records[]=recXXXXXXXXXXXXXX&records[]=recYYYYYYYYYYYYYY&records[]=recZZZZZZZZZZZZZZ" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Rate Limiting Strategy

```bash
#!/bin/bash

RATE_LIMIT=5
BATCH_SIZE=10
DELAY=$(echo "scale=2; 1 / $RATE_LIMIT" | bc)

process_batch() {
  local record_ids=("$@")
  
  curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"records\": $(printf '%s\n' "${record_ids[@]}" | jq -R . | jq -s .)}"
  
  sleep "$DELAY"
}
```

## Handling Rate Limit Errors

```bash
#!/bin/bash

make_request_with_retry() {
  local max_retries=3
  local retry_count=0
  
  while [ $retry_count -lt $max_retries ]; do
    response=$(curl -s -w "\n%{http_code}" -X PATCH \
      "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
      -H "Authorization: Bearer $AIRTABLE_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$1")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "429" ]; then
      retry_after=30
      echo "Rate limited. Waiting ${retry_after}s..." >&2
      sleep "$retry_after"
      ((retry_count++))
    elif [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
      echo "$body"
      return 0
    else
      echo "Error: HTTP $http_code - $body" >&2
      return 1
    fi
  done
  
  echo "Max retries reached" >&2
  return 1
}
```

## Best Practices

- **Batch Size**: Always process up to 10 records per request (Airtable's maximum)
- **Rate Limiting**: Respect the 5 requests/second per base limit
- **Sleep Duration**: Add at least 0.2 seconds (200ms) between requests
- **Error Handling**: Implement retry logic for 429 (rate limit) responses
- **Monitor Headers**: Check `X-RateLimit-Remaining` header to track your quota
- **Exponential Backoff**: Increase wait time exponentially on repeated rate limit errors

## Rate Limit Headers

```bash
curl -i "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

Response headers to monitor:
- `X-RateLimit-Limit: 5`
- `X-RateLimit-Remaining: 3`
- `Retry-After: 30` (present when rate limited)

## Reference

See the [Rate Limits Documentation](https://airtable.com/developers/web/api/rate-limits) for detailed information on rate limiting policies.
