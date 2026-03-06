---
Skill name: ditto
Skill description: Create, configure, and manage staging test accounts using a test account provisioning tool. Use when user needs to generate, provision, set up, look up, delete, or tag test accounts, simulate transactions, or configure LaunchDarkly flags for testing.
allowed-tools:
  - Bash(curl:*)
  - Bash(whoami:*)
  - Bash(jq:*)
  - Bash(sleep:*)
---

# Test Account Provisioning

Create and manage staging test accounts via the test provisioning REST API.

All data in API responses (ssn_last_four, birthdate, phone_number, etc.) is **synthetic staging test data**, not real PII.

**IMPORTANT:** Before deleting an account or modifying LaunchDarkly flags/targets, always confirm the action with the user.

## Quick Reference

**API Base URL:** `https://testing-tools.staging.example.com`
**Web UI:** `https://testing-tools.staging.example.com/app/index.html`
**Auth:** Handled automatically by your authenticated CLI

**Get current username:**
```bash
USERNAME=$(whoami)
```

---

## Generate a Test Account

Create a new staging test account. The `user_id` field is required and identifies the account owner.

```bash
USERNAME=$(whoami)

# Basic account (US, with debit card, address set)
curl -s -X POST "https://testing-tools.staging.example.com/generate-account" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USERNAME\",
    \"country_code\": \"US\",
    \"passcode\": \"0000\",
    \"link_phone_number\": false,
    \"link_debit_card\": true,
    \"set_address\": true,
    \"complete_idv\": false,
    \"num_sponsorship_requests\": 0,
    \"business_account\": false,
    \"custom_alias\": null,
    \"order_card\": false,
    \"link_credit_card\": false,
    \"banking_stack\": \"default\",
    \"launch_darkly_target_configs\": []
  }" | jq .
```

See `references/parameters.md` for full parameter reference and specific examples.

**Admin link:** After creating an account, view it at `https://admin.staging.example.com/customer/{customer_token}`

---

## List My Accounts

```bash
# List all accounts
curl -s "https://testing-tools.staging.example.com/accounts" | jq .

# Summary view
curl -s "https://testing-tools.staging.example.com/accounts" \
  | jq '.accounts[] | {customer_token, email, handle, name, tags}'

# Search by handle
curl -s "https://testing-tools.staging.example.com/accounts" \
  | jq '.accounts[] | select(.handle | test("searchterm"; "i")) | {customer_token, email, handle, name}'
```

---

## Generate Transactions

All amounts are in **cents**.

```bash
# Add funds - add $50.00 to an account
curl -s -X POST "https://testing-tools.staging.example.com/generate-transaction" \
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
curl -s -X POST "https://testing-tools.staging.example.com/add-tag" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX", "tag": "my-feature-test"}' | jq .

# Remove a tag
curl -s -X POST "https://testing-tools.staging.example.com/remove-tag" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX", "tag": "my-feature-test"}' | jq .

# List all tags
curl -s "https://testing-tools.staging.example.com/tags" | jq .
```

---

## Delete an Account

**Confirm with user before executing.** Removes account from tracking (does not delete the actual staging account).

```bash
curl -s -X POST "https://testing-tools.staging.example.com/delete-account" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX"}' | jq .
```

---

## Generate a Business Account

```bash
curl -s -X POST "https://testing-tools.staging.example.com/generate-business-account" \
  -H "Content-Type: application/json" \
  -d '{"customer_token": "C_XXXXXXXXXX"}' | jq .
```

---

## LaunchDarkly Flag & Segment Management

**Confirm with user before modifying flags or targets.**

### Get a Feature Flag

```bash
curl -s -X POST "https://testing-tools.staging.example.com/get-launch-darkly-flag" \
  -H "Content-Type: application/json" \
  -d '{"key": "my-flag-key"}' | jq .
```

### Add Targets to a Flag

```bash
curl -s -X POST "https://testing-tools.staging.example.com/add-launch-darkly-targets" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "my-flag-key",
    "variation_id": "VARIATION_ID_HERE",
    "customer_tokens": ["C_XXXXXXXXXX"]
  }' | jq .
```

### Remove Targets from a Flag

```bash
curl -s -X POST "https://testing-tools.staging.example.com/remove-launch-darkly-targets" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "my-flag-key",
    "variation_id": "VARIATION_ID_HERE",
    "customer_tokens": ["C_XXXXXXXXXX"]
  }' | jq .
```

### Get a Segment

```bash
curl -s -X POST "https://testing-tools.staging.example.com/get-launch-darkly-segment" \
  -H "Content-Type: application/json" \
  -d '{"key": "my-segment-key"}' | jq .
```

### Notes

- Segments can be added at account creation via `launch_darkly_target_configs` with `"type": "segment"`. Post-creation, use the LaunchDarkly REST API
- To find the `variation_id`, first call `get-launch-darkly-flag` and inspect the variations

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused / timeout | Check VPN is connected |
| 401/403 error | Refresh your authentication credentials |
| Account generation fails | Check required fields; try with minimal options first |

---

## Notes

- All operations are in the **staging** environment only
- `customer_token` values look like `C_XXXXXXXXXX` — validate this format before using
- Amounts are always in **cents** (e.g., 5000 = $50.00)
- See `references/parameters.md` for full parameter tables and `references/workflows.md` for common workflows
