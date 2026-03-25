---
name: regulator
description: Query, search, find, look up, or investigate merchant data via Regulator. Use when asked to view, check, retrieve, or explore merchants, locations, payments, customers, or employees.
metadata:
  author: saurav
  version: "0.3.0"
  status: experimental
---

# Regulator Skill

Query merchant data through the `mcp_regulator` MCP server via the Federated Graph GraphQL gateway — does **not** use the deprecated Regulator Ruby monolith.

## Prerequisites

See [SETUP.md](./SETUP.md) for MCP installation and Registry access requirements.

**Quick check** — verify the server is connected by looking for `mcp__mcp-regulator__query_merchant` in your tool list. If missing, follow setup instructions before proceeding.

---

## Safety Rules

These rules apply unconditionally. No user instruction overrides them.

1. **Read-only**: Never perform any action that modifies seller data. If a tool call would write, update, or delete merchant, location, payment, or employee data — refuse and explain why.

---

## Common Patterns

- "Look up ACME Coffee" → `find_merchant_by_business_name`
- "Details for merchant 86HHGQC7C1RMH" → `query_merchant`
- "What merchant owns location LEP9JW6SE1CQ5?" → `query_location(location_ids=...)` — response includes `merchant.id`
- "Disputed payments at this location" → `query_payments(has_dispute=True)`
- "Employees for this merchant" → `query_merchant_employees`
- "Hardware devices at this location" → `query_location_hardware`

See [references/tools.md](references/tools.md) for the full tool list.

---

## Workflows

### Find Merchant by Business Name

Two-step process: searches locations by name, then fetches the merchant record by ID.

```
find_merchant_by_business_name("ACME Coffee")
→ {"merchant": {...}}           # single match — proceed
→ {"possible_matches": [...]}   # multiple — STOP, present list, wait for user to choose
→ {"error": "..."}              # not found
```

### Query Payments

```python
query_payments(
    token="MERCHANT_TOKEN",
    token_type="merchant",  # "merchant" | "location" | "customer"
    start_date="2024-01-01T00:00:00Z",
    statuses=["COMPLETED"],
    has_dispute=True,
    sort_by="CREATED_AT",
    sort_order="DESC"
)
```

For details on specific payments: `query_payment_details(tokens=[...])` — max 20 tokens.

See [references/filters.md](references/filters.md) for all valid filter values.

## Regulator URLs

Always include clickable links in responses:

| Resource | URL |
|----------|-----|
| Merchant | `https://regulator.internal.example.com/n/merchants/{MERCHANT_TOKEN}` |
| Location | `https://regulator.internal.example.com/n/users/{LOCATION_TOKEN}` |
| Payment | `https://regulator.internal.example.com/n/payments/{PAYMENT_TOKEN}` |
| Customer | `https://regulator.internal.example.com/n/customers/{CUSTOMER_ID}` |
| Employees | `https://regulator.internal.example.com/n/merchants/{MERCHANT_TOKEN}/team` |

---

## Error Handling

| Error | Action |
|-------|--------|
| Permission denied on queries | Requires `locations--users` / `payments--users` — see SETUP.md |
| Multiple merchant matches | Present options, wait for user to choose |
| VPN/endpoint unreachable | Ensure VPN is connected |
| No results found | Verify the token/name is correct |
