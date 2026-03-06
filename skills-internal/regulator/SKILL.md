---
name: regulator
description: "Search and query an internal account/merchant lookup tool for accounts, cases, payments, and actions. Use when looking up sellers, account tokens, unit tokens, cases, or querying account data."
---

# Account Lookup Tool

Search and query the internal account lookup tool — the primary operational dashboard for viewing and managing customer accounts.

## URLs

| Environment | URL |
|---|---|
| **Production** | `https://accounts.example.com` |
| **Staging** | `https://accounts.staging.example.com` |

## Lookup by Account Token (Legacy JSON API)

Use authenticated `curl` to query the legacy API. This is the fastest way to look up an account by token.

```bash
curl -s 'https://accounts.example.com/api/js/v2/merchants/{ACCOUNT_TOKEN}' | python3 -m json.tool
```

This returns account details including name, status, units/locations, and metadata.

## GraphQL Queries (GraphQL Gateway)

For richer queries, use the GraphQL Gateway. **Always include the client name header.**

```bash
curl -s -X POST 'https://graphql-gateway.example.com/graphql' \
  -H 'Content-Type: application/json' \
  -H 'apollographql-client-name: agent-account-skill' \
  -H 'apollographql-client-version: 1.0.0' \
  -d '{"query": "<GRAPHQL_QUERY>", "variables": {}}'
```

### Look up account by ID

```graphql
query AccountLookup($ids: [ID!]) {
  merchantsBulk(ids: $ids) {
    id
    businessName
    createdAt
    updatedAt
    status
    isTestMerchant
    country { code }
    currency { code }
    mainLocation { id name }
    locations { nodes { id name } }
  }
}
```

### Query cases

```graphql
query CaseLookup($tokens: [String!]) {
  cases(tokens: $tokens) {
    nodes {
      token
      status
      caseType
      createdAt
      updatedAt
    }
  }
}
```

### Search actions

```graphql
query SearchActions($filter: ActionMetadataFilterInput) {
  searchActionMetadata(filter: $filter) {
    nodes {
      id
      name
      description
      entityType
    }
  }
}
```

## Generating Account Lookup Links

When looking up entities, always provide clickable links to the UI:

| Entity | URL Pattern |
|---|---|
| Account | `https://accounts.example.com/n/merchants/{account_token}` |
| Unit/Location | `https://accounts.example.com/n/users/{unit_token}` |
| Case | `https://accounts.example.com/n/cases/{case_id}` |
| Advanced Search | `https://accounts.example.com/o/advanced-search` |

## Workflow

1. **Identify the entity type** — account token, unit token, case ID, email, etc.
2. **Choose the right API**:
   - For account token lookups → use the legacy JSON API
   - For ID-based lookups or richer queries → use GraphQL Gateway
   - For browsing/searching that requires the UI → provide the appropriate UI URL
3. **Execute the query** using authenticated `curl`.
4. **Format the response** clearly, highlighting key fields (status, name, created date, etc.).
5. **Include UI links** so the user can view the full entity in the browser.

## Tips

- Account tokens are uppercase alphanumeric identifiers (~12 chars).
- Unit tokens are similar format but represent individual locations.
- Case IDs/tokens are used to look up risk, compliance, and support cases.
- If a query returns 403, the user may not have the required permissions.
- For help, check the relevant Slack channel.
