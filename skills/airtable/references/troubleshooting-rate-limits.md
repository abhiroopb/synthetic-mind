# Rate Limiting Issues

## 429 Too Many Requests

### Check Rate Limit Headers

```bash
curl -i "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### Important Headers

- `X-RateLimit-Limit: 5` - Maximum requests per second per base
- `X-RateLimit-Remaining: 3` - Requests remaining in current window
- `Retry-After: 30` - Seconds to wait before retrying (present when rate limited)

## Rate Limit Rules

- **5 requests per second** per base
- Rate limits are calculated on a per-base basis
- Multiple bases can be accessed concurrently without affecting each other's limits
- Rate limit window is a rolling 1-second period

## Solutions

### 1. Implement Basic Rate Limiting

```bash
for i in {1..10}; do
  curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN"
  sleep 0.2
done
```

### 2. Respect Retry-After Header

```bash
#!/bin/bash

make_request() {
  response=$(curl -i -s "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN")
  
  http_code=$(echo "$response" | grep HTTP | awk '{print $2}')
  retry_after=$(echo "$response" | grep -i "Retry-After:" | awk '{print $2}')
  
  if [ "$http_code" = "429" ]; then
    echo "Rate limited. Waiting ${retry_after}s..."
    sleep "$retry_after"
    make_request
  else
    echo "$response"
  fi
}
```

### 3. Implement Exponential Backoff

```bash
#!/bin/bash

make_request_with_backoff() {
  local max_retries=5
  local retry_count=0
  local wait_time=1
  
  while [ $retry_count -lt $max_retries ]; do
    response=$(curl -s -w "\n%{http_code}" "$1" \
      -H "Authorization: Bearer $AIRTABLE_TOKEN")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "429" ]; then
      echo "Rate limited. Waiting ${wait_time}s..." >&2
      sleep "$wait_time"
      wait_time=$((wait_time * 2))
      ((retry_count++))
    elif [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
      echo "$body"
      return 0
    else
      echo "Error: HTTP $http_code" >&2
      return 1
    fi
  done
  
  echo "Max retries reached" >&2
  return 1
}
```

### 4. Use Batch Operations

Instead of individual requests, batch up to 10 records per request:

```bash
curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"id": "rec1", "fields": {"Status": "Updated"}},
      {"id": "rec2", "fields": {"Status": "Updated"}},
      {"id": "rec3", "fields": {"Status": "Updated"}},
      {"id": "rec4", "fields": {"Status": "Updated"}},
      {"id": "rec5", "fields": {"Status": "Updated"}},
      {"id": "rec6", "fields": {"Status": "Updated"}},
      {"id": "rec7", "fields": {"Status": "Updated"}},
      {"id": "rec8", "fields": {"Status": "Updated"}},
      {"id": "rec9", "fields": {"Status": "Updated"}},
      {"id": "rec10", "fields": {"Status": "Updated"}}
    ]
  }'
```

### 5. Monitor Rate Limit Status

```bash
#!/bin/bash

check_rate_limit() {
  response=$(curl -i -s "https://api.airtable.com/v0/meta/bases" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN")
  
  limit=$(echo "$response" | grep -i "X-RateLimit-Limit:" | awk '{print $2}')
  remaining=$(echo "$response" | grep -i "X-RateLimit-Remaining:" | awk '{print $2}')
  
  echo "Rate Limit: $limit requests/second"
  echo "Remaining: $remaining requests"
}
```

## Best Practices

- **Add Delays**: Always add at least 200ms (0.2s) between requests
- **Batch Requests**: Group operations to minimize API calls
- **Implement Retries**: Always retry 429 responses with proper backoff
- **Monitor Headers**: Track `X-RateLimit-Remaining` to prevent hitting limits
- **Use Webhooks**: For real-time updates instead of polling
- **Cache Data**: Cache base schema and frequently accessed records

## Common Scenarios

### High-Frequency Updates

If you need to update many records:
1. Batch records into groups of 10
2. Add 200ms delay between batches
3. Implement exponential backoff for 429 responses

### Polling for Changes

Instead of frequent polling:
1. Use webhooks for real-time notifications
2. If polling is required, set minimum 5-second intervals
3. Use `filterByFormula` to query only changed records

### Multiple Base Access

Rate limits are per-base, so:
1. Parallel requests to different bases won't affect each other
2. Track rate limits separately for each base
3. Consider distributing operations across bases if possible

## Reference

See the [Rate Limits Documentation](https://airtable.com/developers/web/api/rate-limits) for complete details on rate limiting policies.
