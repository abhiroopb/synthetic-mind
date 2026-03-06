# Authentication Issues

## 401 Unauthorized

### Verify Token

```bash
echo $AIRTABLE_TOKEN

curl -v "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN"
```

### Common Causes

- **Expired Token**: Personal Access Token has expired
- **Invalid Token**: Token was revoked or is malformed
- **Missing Scopes**: Token doesn't have required scopes (data.records:read, data.records:write, etc.)
- **Wrong Authorization Format**: Must use `Bearer` prefix in the Authorization header
- **Token Not Set**: Environment variable is not properly set or sourced

### Solutions

1. **Verify token is set correctly**
   ```bash
   source ~/.claude/skills/airtable/.env
   echo $AIRTABLE_TOKEN
   ```

2. **Check token format**
   ```bash
   curl -v "https://api.airtable.com/v0/meta/bases" \
     -H "Authorization: Bearer $AIRTABLE_TOKEN"
   ```
   Ensure the header format is: `Authorization: Bearer YOUR_TOKEN`

3. **Verify token scopes**
   - Go to [https://airtable.com/create/tokens](https://airtable.com/create/tokens)
   - Check that your token has the necessary scopes:
     - `data.records:read` - Read records
     - `data.records:write` - Create/update records
     - `schema.bases:read` - Read base schema
     - `webhook:manage` - Manage webhooks

4. **Create a new token if needed**
   - Navigate to [https://airtable.com/create/tokens](https://airtable.com/create/tokens)
   - Create a new Personal Access Token with appropriate scopes
   - Update your `.env` file with the new token

### Test Authentication

```bash
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  -w "\nHTTP Status: %{http_code}\n"
```

A successful response should return HTTP 200 with a list of bases.

## 403 Forbidden

### Common Causes

- **Insufficient Permissions**: Token has valid scopes but lacks permission to access specific base
- **Base Not Shared**: Base is not shared with the account that created the token
- **Workspace Restrictions**: Workspace has restrictions on API access

### Solutions

1. **Verify base access**
   - Ensure the base is shared with your Airtable account
   - Check base permissions (read vs. write access)

2. **Check workspace settings**
   - Some workspaces restrict API access
   - Contact workspace administrator if needed

3. **List accessible bases**
   ```bash
   curl "https://api.airtable.com/v0/meta/bases" \
     -H "Authorization: Bearer $AIRTABLE_TOKEN" | jq '.bases[].id'
   ```

## Reference

See the [API Authentication Documentation](https://airtable.com/developers/web/api/authentication) for more details.
