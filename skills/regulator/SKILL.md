---
name: regulator
description: "Search and query Square's Regulator (go/regulator) for merchant accounts, cases, payments, and actions. Use when looking up sellers, merchant tokens, unit tokens, cases, or querying Regulator data."
---

# Regulator

Search and query Square's internal Regulator tool — the primary operational dashboard for viewing and managing seller accounts.

## URLs

| Environment | URL |
|---|---|
| **Production** | `https://regulator.sqprod.co` |
| **Production (new FE)** | `https://regulator-fe.sqprod.co` |
| **Staging** | `https://regulator.stage.sqprod.co` |

## Lookup by Merchant Token (Legacy JSON API)

Use `sq curl` to query the legacy Regulator API. This is the fastest way to look up a merchant by token.

```bash
sq curl -s 'https://regulator.sqprod.co/api/js/v2/merchants/{MERCHANT_TOKEN}' | python3 -m json.tool
```

This returns merchant details including name, status, units/locations, and metadata.

## GraphQL Queries (Block GraphQL Gateway)

For richer queries, use the Block GraphQL Gateway. **Always include the client name header.**

```bash
sq curl -s -X POST 'https://graphql-gateway.sqprod.co/graphql' \
  -H 'Content-Type: application/json' \
  -H 'apollographql-client-name: amp-regulator-skill' \
  -H 'apollographql-client-version: 1.0.0' \
  -d '{"query": "<GRAPHQL_QUERY>", "variables": {}}'
```

### Look up merchant by ID

```graphql
query MerchantLookup($ids: [ID!]) {
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

### Get action details

```graphql
query ActionDetails($actionIds: [ID!]!) {
  actionMetadatas(actionIds: $actionIds) {
    id
    name
    description
    entityType
  }
}
```

## Generating Regulator Links

When looking up entities, always provide clickable links to the Regulator UI:

| Entity | URL Pattern |
|---|---|
| Merchant | `https://regulator.sqprod.co/n/merchants/{merchant_token}` |
| Unit/Location | `https://regulator.sqprod.co/n/users/{unit_token}` |
| Case | `https://regulator.sqprod.co/n/cases/{case_id}` |
| Payment (new FE) | `https://regulator-fe.sqprod.co/n/locations/{location_token}/payments/{payment_id}` |
| Advanced Search | `https://regulator.sqprod.co/o/advanced-search` |

## Workflow

1. **Identify the entity type** — merchant token, unit token, case ID, email, etc.
2. **Choose the right API**:
   - For merchant token lookups → use the legacy JSON API (`/api/js/v2/merchants/{token}`)
   - For ID-based lookups or richer queries → use GraphQL Gateway
   - For browsing/searching that requires the UI → provide the appropriate Regulator URL
3. **Execute the query** using `sq curl`.
4. **Format the response** clearly, highlighting key fields (status, name, created date, etc.).
5. **Include Regulator UI links** so the user can view the full entity in the browser.

## Tips

- Merchant tokens look like `MLXXXXXXXX` (uppercase alphanumeric, ~12 chars).
- Unit tokens are similar format but represent individual locations.
- Case IDs/tokens are used to look up risk, compliance, and support cases.
- If a query returns 403, the user may not have the required Registry group permissions.
- Use `go/regulator` for production, `go/regulator-staging` for staging.
- For help, check **#regulator-help** on Slack.
