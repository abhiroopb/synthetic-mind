# People API Setup

## Get an API Token

1. Go to https://my.sqprod.co/dev/tokens (requires WARP VPN)
2. Create a new token
3. Copy the hex API key (e.g., `b8eda553073136517b393d0a48374eb0`)

## Provide the Token

Set `PEOPLE_API_TOKEN` in your environment however you prefer. For example:

```bash
# In your shell profile (~/.zshrc, ~/.bashrc, etc.)
export PEOPLE_API_TOKEN=your_token_here

# Or in a secrets file you source
echo 'export PEOPLE_API_TOKEN=your_token_here' >> ~/.secrets-people-api
```

## Verify

```bash
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://my.sqprod.co/people/api/p/$(whoami).json" | python3 -m json.tool | head -5
```

You should see your own profile data.
