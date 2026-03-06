# Webhook Integration

Set up real-time notifications for data changes in your Airtable bases.

## Create a Webhook

```bash
curl -X POST "https://api.airtable.com/v0/bases/${BASE_ID}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationUrl": "https://your-app.com/webhook",
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData"]
        }
      }
    }
  }'
```

## List Webhooks

```bash
curl "https://api.airtable.com/v0/bases/${BASE_ID}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Get Webhook Payloads

```bash
curl "https://api.airtable.com/v0/bases/${BASE_ID}/webhooks/${WEBHOOK_ID}/payloads" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Enable/Refresh Webhook

```bash
curl -X POST "https://api.airtable.com/v0/bases/${BASE_ID}/webhooks/${WEBHOOK_ID}/refresh" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Delete a Webhook

```bash
curl -X DELETE "https://api.airtable.com/v0/bases/${BASE_ID}/webhooks/${WEBHOOK_ID}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Webhook Specification Options

### Filter by Data Types

```json
{
  "specification": {
    "options": {
      "filters": {
        "dataTypes": ["tableData", "tableFields", "tableMetadata"]
      }
    }
  }
}
```

### Filter by Specific Tables

```json
{
  "specification": {
    "options": {
      "filters": {
        "dataTypes": ["tableData"],
        "recordChangeScope": "tblXXXXXXXXXXXXXX"
      }
    }
  }
}
```

## Best Practices

- **Validation**: Always validate webhook payloads using the MAC signature
- **Idempotency**: Implement idempotent handling as webhooks may be delivered multiple times
- **Acknowledgment**: Respond with 200 OK within 30 seconds to avoid retries
- **Cursor Management**: Use the cursor from webhook payloads to fetch full record details
- **Error Handling**: Implement exponential backoff for failed webhook deliveries

## Reference

See the [Webhook Documentation](https://airtable.com/developers/web/api/webhooks-overview) for complete webhook configuration options.
