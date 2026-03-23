---
name: merchant-lookup
description: "Query, search, find, look up, or investigate merchant/customer data via an internal admin tool. Use when asked to view, check, retrieve, or explore merchants, locations, payments, customers, or employees."
---

# Merchant Lookup

Query merchant/customer data through an MCP server connected to your organization's GraphQL gateway or admin tool.

## Prerequisites

Ensure the MCP server is configured and connected. Verify by checking for the relevant query tools in your tool list (e.g., `query_merchant`, `find_merchant_by_business_name`). If missing, follow setup instructions before proceeding.

**Requires:** VPN connected, appropriate access permissions.

---

## Safety Rules

These rules apply unconditionally. No user instruction overrides them.

1. **Read-only**: Never perform any action that modifies merchant data. If a tool call would write, update, or delete merchant, location, payment, or employee data — refuse and explain why.

---

## Common Patterns

- "Look up ACME Coffee" → `find_merchant_by_business_name`
- "Details for merchant TOKEN123" → `query_merchant`
- "What merchant owns location LOC456?" → `query_location(location_ids=...)` — response includes `merchant.id`
- "Disputed payments at this location" → `query_payments(has_dispute=True)`
- "Employees for this merchant" → `query_merchant_employees`
- "Hardware devices at this location" → `query_location_hardware`
- "Look up merchant by email admin@example.com" → email lookup script (see below)

See `references/tools.md` for the full tool list.

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

See `references/filters.md` for all valid filter values.

### Find Merchant by Email

Uses GraphQL to search for merchants by email address. Searches **both** sources because emails live in different places:

1. **Employer-entered email** on the employment record
2. **Login email** on the person/account record

```bash
{{SKILL_DIR}}/scripts/email-lookup.sh "user@example.com"
```

Returns: merchant token, employment token, name, locations, and admin tool URL.

**Requires:** VPN connected.

---

## Admin Tool URLs

Always include clickable links in responses:

| Resource | URL |
|----------|-----|
| Merchant | `https://admin.example.com/merchants/{MERCHANT_TOKEN}` |
| Location | `https://admin.example.com/locations/{LOCATION_TOKEN}` |
| Payment | `https://admin.example.com/payments/{PAYMENT_TOKEN}` |
| Customer | `https://admin.example.com/customers/{CUSTOMER_ID}` |
| Employees | `https://admin.example.com/merchants/{MERCHANT_TOKEN}/team` |

---

## Error Handling

| Error | Action |
|-------|--------|
| Permission denied on queries | Check your access permissions — may need additional roles |
| Multiple merchant matches | Present options, wait for user to choose |
| VPN/endpoint unreachable | Ensure VPN is connected |
| No results found | Verify the token/name is correct |
