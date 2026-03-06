# Invalid Request Errors (422 Unprocessable Entity)

## Common Causes

### Invalid Field Names

Field names in Airtable are case-sensitive and must match exactly.

```bash
curl "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.tables[].fields[].name'
```

**Wrong:**
```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"name": "Test"}}'
```

**Correct:**
```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Name": "Test"}}'
```

### Wrong Data Types

Ensure values match the expected field type.

#### Single Line Text
```bash
{"fields": {"Name": "John Doe"}}
```

#### Number
```bash
{"fields": {"Age": 25}}
{"fields": {"Price": 19.99}}
```

#### Checkbox (Boolean)
```bash
{"fields": {"Active": true}}
{"fields": {"Completed": false}}
```

#### Single Select
```bash
{"fields": {"Status": "Active"}}
```

#### Multiple Select
```bash
{"fields": {"Tags": ["Tag1", "Tag2", "Tag3"]}}
```

#### Date
```bash
{"fields": {"Created": "2024-01-26"}}
```

#### Date/Time
```bash
{"fields": {"Timestamp": "2024-01-26T10:30:00.000Z"}}
```

#### Linked Records
```bash
{"fields": {"Related": ["recXXXXXXXXXXXXXX", "recYYYYYYYYYYYYYY"]}}
```

#### Attachments
```bash
{
  "fields": {
    "Attachments": [
      {"url": "https://example.com/image.png"},
      {"url": "https://example.com/document.pdf"}
    ]
  }
}
```

### Missing Required Fields

Check base schema to identify required fields:

```bash
curl "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.tables[] | {name: .name, required_fields: [.fields[] | select(.required == true) | .name]}'
```

Ensure all required fields are included when creating records:

```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Name": "Test",
      "Status": "Active",
      "Required Field": "Value"
    }
  }'
```

### Invalid Record IDs

Record IDs must:
- Start with "rec"
- Be followed by exactly 14 alphanumeric characters
- Total length: 17 characters

**Valid:** `recXXXXXXXXXXXXXX`

**Invalid:**
- `XXXXXXXXXXXXXXXXX` (missing "rec" prefix)
- `rec123` (too short)
- `rec_XXXXXXXXXXXX` (contains underscore)

### Invalid Table Names

Table names or IDs must be either:
- URL-encoded table name: `My%20Table`
- Table ID: `tblXXXXXXXXXXXXXX`

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/My%20Table" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

or

```bash
curl "https://api.airtable.com/v0/${BASE_ID}/tblXXXXXXXXXXXXXX" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

## Debugging Steps

### 1. Verify Field Names and Types

```bash
curl "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.tables[] | select(.name == "Your Table") | .fields[] | {name: .name, type: .type, required: .required}'
```

### 2. Test with Minimal Payload

Start with a minimal request and gradually add fields:

```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Name": "Test"}}' \
  -w "\nStatus: %{http_code}\n"
```

### 3. Check Error Response

```bash
response=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Name": "Test"}}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "422" ]; then
  echo "Error Details:"
  echo "$body" | jq '.error'
fi
```

### 4. Validate JSON Syntax

```bash
echo '{"fields": {"Name": "Test"}}' | jq '.'
```

If jq returns an error, your JSON is malformed.

## Common Scenarios

### Creating Record with Invalid Choice

If you have a Single Select field with choices ["Active", "Pending", "Completed"]:

**Wrong:**
```bash
{"fields": {"Status": "active"}}
```

**Correct:**
```bash
{"fields": {"Status": "Active"}}
```

### Updating Non-Existent Record

```bash
curl -X PATCH "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"id": "recINVALIDIDHERE", "fields": {"Status": "Updated"}}
    ]
  }'
```

This will return 422 if the record ID doesn't exist or is malformed.

### Linked Record Not Found

```bash
curl -X POST "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Name": "Test",
      "Related": ["recDOESNOTEXIST"]
    }
  }'
```

Ensure linked record IDs exist in the target table.

## Reference

See the [Field Model Documentation](https://airtable.com/developers/web/api/field-model) for complete field type specifications.
