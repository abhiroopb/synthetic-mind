---
name: graphql-schema-discovery
description: "Discover and navigate your organization's GraphQL schema using AI tools. Use when exploring, searching, browsing, introspecting, or understanding the GraphQL schema, finding available types and fields, discovering operations, or setting up an MCP server for schema navigation."
---

# GraphQL Schema Discovery

Two approaches for discovering what's available in your organization's GraphQL schema: an MCP server for AI-native exploration, and direct introspection queries.

## MCP Server Approach

Use an MCP server (e.g., `mcp_graphql`) that provides AI agents with tools for schema navigation and query execution.

### Quick Start

```bash
npx -y @your-org/mcp_graphql
```

Options:
- `--client CLIENT` — Client configuration (e.g., `default`, `dashboard`, `admin`)
- `--env staging|production` — Target environment (default: staging)

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `get_operations` | List pre-built operations for the configured client |
| `execute_graphql` | Execute a GraphQL operation against the gateway |
| `validate_graphql_operation` | Validate a query against the schema without executing |
| `introspect_graphql_schema` | Explore types, fields, and directives in the schema |

### Adding Operations

Create `.graphql` files in `src/operations/<client>/` within your MCP GraphQL repo:

```graphql
# Description: Fetch merchant details by ID
# This operation retrieves core merchant information
query GetMerchant($id: ID!) {
  merchant(id: $id) {
    id
    name
    country
  }
}
```

Comments before the operation become the tool description. The operation name becomes the tool identifier.

### Adding a New Client

Add a client entry to `src/config.yaml`:

```yaml
clients:
  my-client:
    name: my-client
    variant: internal
    capabilities:
      introspect: true
    auth:
      type: bearer
      token_env: MY_AUTH_TOKEN  # Optional: env var for auth token
```

## Direct Introspection

When the MCP server isn't available, query the schema directly:

```graphql
# List all root query fields
{ __schema { queryType { fields { name description } } } }

# Explore a specific type
{ __type(name: "Merchant") { fields { name type { name kind } } } }

# Discover filter inputs
{ __type(name: "MerchantFilterInput") { inputFields { name type { name kind } } } }

# List all types in the schema
{ __schema { types { name kind } } }
```

Run these via Apollo Explorer or cURL:

```bash
curl -X POST https://your-graphql-gateway.example.com/graphql \
  -H 'Content-Type: application/json' \
  -H 'apollographql-client-name: schema-explorer' \
  -d '{"query": "{ __schema { queryType { fields { name } } } }"}'
```

## Reference Files

- `references/mcp-graphql-setup.md` — Load when setting up the MCP server for a new agent or troubleshooting
- `references/introspection-queries.md` — Load when running introspection directly against the gateway

## Related Skills

- `graphql-client` — Use when consuming GraphQL from web, mobile, or server-side applications
- `graphql-connectors` — Use when authoring REST Connector subgraphs
- `graphql-subgraphs` — Use when building standalone GraphQL subgraph services
