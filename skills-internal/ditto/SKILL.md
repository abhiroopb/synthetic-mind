---
name: ditto
description: Create, configure, and manage Cash App staging test accounts using Ditto (Cash Testing Tools). Use when user needs to generate, provision, set up, look up, delete, or tag test accounts, simulate transactions, or configure LaunchDarkly flags for testing.
roles: [lending, afterpay]
allowed-tools:
  - Bash(sq:*)
  - Bash(whoami:*)
  - Bash(jq:*)
  - Bash(sleep:*)
metadata:
  author: shean
  version: "0.2.0"
  status: experimental
---

# Ditto (Cash Testing Tools)

Create and manage Cash App staging test accounts via the Ditto REST API.

All data in API responses (ssn_last_four, birthdate, phone_number, etc.) is **synthetic staging test data**, not real PII.

**IMPORTANT:** Before deleting an account or modifying LaunchDarkly flags/targets, always confirm the action with the user.

## Quick Reference

**API Base URL:** `https://cash-testing-tools.stage.sqprod.co`
**Web UI:** `https://cash-testing-tools.stage.sqprod.co/app/index.html` (aka go/ditto)
**Auth:** Handled automatically by `sq curl`

**Get current user's Square ID:**
```bash
SQUARE_ID=$(whoami)
```

---

## Generate a Test Account

Create a new staging test account. The `square_id` field is required and identifies the account owner.

```bash
SQUARE_ID=$(whoami)

# Basic account (US, with debit card, address set)
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/generate-account" \
  -H "Content-Type: application/json" \
  -d "{
    \"square_id\": \"$SQUARE_ID\",
    \"country_code\": \"US\",
    \"passcode\": \"0000\",
    \"link_phone_number\": false,
    \"link_debit_card\": true,
    \"set_address\": true,
    \"complete_idv\": false,
    \"num_sponsorship_requests\": 0,
    \"business_account\": false,
    \"custom_alias\": null,
    \"order_cash_card\": false,
    \"link_credit_card\": false,
    \"banking_stack\": \"sutton_marqeta\",
    \"launch_darkly_target_configs\": []
  }" | jq .
```

See `references/parameters.md` for full parameter reference and lending-specific examples.

**Toolbox link:** After creating an account, view it at `https://toolbox.stage.sqprod.co/customer/{customer_token}`

---

## List My Accounts

```bash
# List all accounts
sq curl -s "https://cash-testing-tools.stage.sqprod.co/accounts" | jq .

# Summary view
sq curl -s "https://cash-testing-tools.stage.sqprod.co/accounts" \
  | jq '.accounts[] | {customer_token, email, cashtag, name, tags}'

# Search by cashtag
sq curl -s "https://cash-testing-tools.stage.sqprod.co/accounts" \
  | jq '.accounts[] | select(.cashtag | test("searchterm"; "i")) | {customer_token, email, cashtag, name}'
```

---

## Generate Transactions

All amounts are in **cents**.

```bash
# Add Cash - add $50.00 to an account
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/generate-transaction" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_token": "C_XXXXXXXXXX",
    "add_cash_amount": 5000,
    "country_code": "US",
    "recipient_token": "",
    "request_payment_amount": 0,
    "requestee_token": "",
    "send_payment_amount": 0
  }' | jq .
```

---

## Manage Tags

```bash
# Add a tag
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/add-tag" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX", "tag": "my-feature-test"}' | jq .

# Remove a tag
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/remove-tag" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX", "tag": "my-feature-test"}' | jq .

# List all tags
sq curl -s "https://cash-testing-tools.stage.sqprod.co/tags" | jq .
```

---

## Delete an Account

**Confirm with user before executing.** Removes account from Ditto tracking (does not delete the actual staging account).

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/delete-account" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX"}' | jq .
```

---

## Generate a Business Account

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/generate-business-account" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX"}' | jq .
```

---

## LaunchDarkly Flag & Segment Management

**Confirm with user before modifying flags or targets.**

### Get a Feature Flag

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/get-launch-darkly-flag" \
  -H "Content-Type: application/json" \
  -d '{"key": "my-flag-key"}' | jq .
```

### Add Targets to a Flag

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/add-launch-darkly-targets" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "my-flag-key",
    "variation_id": "VARIATION_ID_HERE",
    "customer_tokens": ["C_XXXXXXXXXX"]
  }' | jq .
```

### Remove Targets from a Flag

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/remove-launch-darkly-targets" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "my-flag-key",
    "variation_id": "VARIATION_ID_HERE",
    "customer_tokens": ["C_XXXXXXXXXX"]
  }' | jq .
```

### Get a Segment

```bash
sq curl -s -X POST "https://cash-testing-tools.stage.sqprod.co/get-launch-darkly-segment" \
  -H "Content-Type: application/json" \
  -d '{"key": "my-segment-key"}' | jq .
```

### Notes

- Segments can be added at account creation via `launch_darkly_target_configs` with `"type": "segment"`. Post-creation, use the LaunchDarkly REST API (see **toolbox** skill)
- To find the `variation_id`, first call `get-launch-darkly-flag` and inspect the variations

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused / timeout | Check VPN (Cloudflare WARP) is connected |
| 401/403 error | Run `sq auth` to refresh authentication |
| Account generation fails | Check required fields; try with minimal options first |

---

## Notes

- All operations are in the **staging** environment only
- `customer_token` values look like `C_XXXXXXXXXX` — validate this format before using
- Amounts are always in **cents** (e.g., 5000 = $50.00)
- For card transaction simulation, use the **toolbox** skill
- See `references/parameters.md` for full parameter tables and `references/workflows.md` for common workflows
