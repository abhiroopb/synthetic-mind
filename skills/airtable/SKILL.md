---
name: airtable
description: Integrate with Airtable's cloud database platform API for managing bases, tables, records, and automations with powerful filtering, sorting, and real-time collaboration features.
metadata:
  author: rbarnwell
  version: "1.0.0"
  status: experimental
---

# Airtable API Integration

This skill provides comprehensive guidance for integrating with Airtable's cloud database platform API.

## Prerequisites

Create a Personal Access Token: [https://airtable.com/create/tokens](https://airtable.com/create/tokens)

Create a `.env` file to store your credentials:

```bash
mkdir -p ~/.claude/skills/airtable
cat > ~/.claude/skills/airtable/.env << 'EOF'
AIRTABLE_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"
BASE_ID="your_base_id"
EOF
```

Load the environment variables before making API calls:

```bash
source ~/.claude/skills/airtable/.env
```

## Quick Start

### Authentication

```bash
# Test authentication by listing bases
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### List Records

```bash
# List all records in a table
curl "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"

# List records with specific fields only
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "fields[]=Name" \
  -d "fields[]=Status"

# List with pagination
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "pageSize=10" \
  -d "maxRecords=100"
```

### Filter Records

```bash
# Filter by formula
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Status}='Active'"

# Complex filter with AND/OR
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=AND({Status}='Active',{Priority}='High')"

# Sort results
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -d "sort[0][field]=Name" \
  -d "sort[0][direction]=asc"
```

### Create Records

```bash
# Create a single record
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Name": "New Record",
      "Status": "Active",
      "Priority": "High"
    }
  }'

# Create multiple records (up to 10 per request)
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "fields": {
          "Name": "Record 1",
          "Status": "Active"
        }
      },
      {
        "fields": {
          "Name": "Record 2",
          "Status": "Pending"
        }
      }
    ]
  }'
```

### Update Records

```bash
# Update a single record (PATCH - updates only specified fields)
curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "id": "recXXXXXXXXXXXXXX",
        "fields": {
          "Status": "Completed"
        }
      }
    ]
  }'

# Replace a record (PUT - replaces all fields)
curl -X PUT "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "id": "recXXXXXXXXXXXXXX",
        "fields": {
          "Name": "Updated Name",
          "Status": "Active"
        }
      }
    ]
  }'

# Update multiple records (up to 10 per request)
curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "id": "recXXXXXXXXXXXXXX",
        "fields": {"Status": "Completed"}
      },
      {
        "id": "recYYYYYYYYYYYYYY",
        "fields": {"Status": "Completed"}
      }
    ]
  }'
```

### Delete Records

```bash
# Delete a single record
curl -X DELETE "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}/recXXXXXXXXXXXXXX" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"

# Delete multiple records (up to 10 per request)
curl -X DELETE "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}?records[]=recXXXXXXXXXXXXXX&records[]=recYYYYYYYYYYYYYY" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Core Capabilities

### Base & Schema Management

```bash
# List all accessible bases
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"

# Get base schema (tables and fields)
curl "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### Record Operations
- **CRUD**: Full create, read, update, delete operations
- **Batch Processing**: Handle up to 10 records per API call
- **Advanced Filtering**: Complex queries using `filterByFormula`
- **Pagination**: Efficient data retrieval with `pageSize` and `offset`

### Real-time Features
- **Webhooks**: Subscribe to record changes with payload specifications
- **Rate Limiting**: 5 requests/second per base with proper backoff handling
- **Field Types**: Support for 20+ field types including attachments, linked records, formulas

## Advanced Features

For detailed examples and advanced usage, see the reference documentation:

- **[Complex Filtering](./references/filtering.md)** - Advanced query patterns using Airtable's formula syntax
- **[Webhook Integration](./references/webhooks.md)** - Real-time notifications for data changes
- **[Batch Operations](./references/batch-operations.md)** - Efficient bulk processing with rate limiting

## Best Practices

- **Rate Limits**: Airtable enforces 5 requests/second per base. Monitor `X-RateLimit-*` headers
- **Batch Operations**: Group operations (up to 10 records) to minimize API calls
- **Data Efficiency**: Use `fields[]` parameter to retrieve only needed fields
- **URL Encoding**: Always URL encode table names and filter formulas
- **Error Handling**: Check HTTP status codes and implement retry logic for 429 (rate limit) responses
- **Pagination**: Use `offset` parameter to handle large datasets
- **Field Validation**: Validate data types match field configurations before creating/updating

## Troubleshooting

For detailed troubleshooting guides, see the reference documentation:

- **[Authentication Issues](./references/troubleshooting-auth.md)** - Resolve 401/403 errors and token problems
- **[Rate Limiting](./references/troubleshooting-rate-limits.md)** - Handle 429 errors and implement proper rate limiting
- **[Invalid Requests](./references/troubleshooting-invalid-requests.md)** - Fix 422 errors, field validation, and data type issues
- **[Common Issues & Debugging](./references/troubleshooting-common-issues.md)** - URL encoding, formulas, pagination, and debugging tools

## Important Links

- **API Reference**: https://airtable.com/developers/web/api/introduction
- **Personal Access Tokens**: https://airtable.com/create/tokens
- **Webhook Documentation**: https://airtable.com/developers/web/api/webhooks-overview
- **Formula Field Reference**: https://support.airtable.com/docs/formula-field-reference
- **Field Types Guide**: https://airtable.com/developers/web/api/field-model
- **Rate Limits**: https://airtable.com/developers/web/api/rate-limits
- **OAuth Integration**: https://airtable.com/developers/web/api/oauth-reference
- **API Changelog**: https://airtable.com/developers/web/api/changelog
- **Status Page**: https://status.airtable.com/

