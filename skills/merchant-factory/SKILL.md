---
name: merchant-factory
description: Creates staging test accounts using a test data factory API. Use when asked to create test accounts, generate catalogs, add subscriptions, or set up staging data.
---

# Test Data Factory

Create and configure staging test accounts using curl.

## Create Account

Creates a new staging test account. Default password is `password`.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreateAccount' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "<username>+<timestamp>@example.com",
    "business_name": "Test Business",
    "country_code": "US",
    "preferred_language": "en",
    "activate_payments": true,
    "link_bank_account": false
  }'
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `email` | Yes | Format: `<username>+<unix_timestamp>@example.com` |
| `business_name` | Yes | Business name |
| `country_code` | Yes | `US`, `CA`, `GB`, `AU`, `JP` |
| `preferred_language` | No | Default: `en` |
| `activate_payments` | No | Default: `false` |
| `configuration_id` | No | Account configuration ID |
| `link_bank_account` | No | Default: `false` |
| `owner_metadata` | No | Object with `phone_number` |

### Response

```json
{
  "status": "SUCCESS",
  "account_token": "XXXXXXXXXX",
  "unit_tokens": ["YYYYYYYYYY"]
}
```

## Create Subscriptions

Add subscriptions to an existing account.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreateSubscriptions' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN",
    "plan_tokens": ["restaurants-plus", "marketing"]
  }'
```

### Available Plan Tokens

- `additional-restaurants-pos`
- `appointments`
- `appointments-free`
- `appointments-plus`
- `appointments-premium`
- `employee-management-per-location`
- `fnb-kiosk`
- `fnb-kiosk-open-beta`
- `invoices-plus`
- `kds`
- `marketing`
- `marketing-sms`
- `restaurants`
- `restaurants-free`
- `restaurants-plus`
- `restaurants-premium`
- `restaurants-pro`
- `retail-pos-per-location`
- `retail-pos-per-location-2023`
- `shifts-plus`
- `team-management`

## Create Premium Subscription

Add a premium subscription to an existing account.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreatePremiumSubscription' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN",
    "plan_token": "premium-plus-v2"
  }'
```

### Available Premium Plan Tokens

- `premium-free-v1`
- `premium-free-v2`
- `premium-plus-v1`
- `premium-plus-v2`
- `premium-pro-v1`
- `premium-pro-v2`

## Generate Catalog

Generate catalog items for an account.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/GenerateCatalog' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN",
    "product": "POS",
    "pos_options": {
      "grid_complexity": "SIMPLE",
      "business_type": "restaurant",
      "num_items_per_page": 10,
      "num_pages": 2
    }
  }'
```

### Catalog Products

- `POS` - Point of Sale
- `INVOICES`
- `ECOM`

### Grid Complexity

- `SIMPLE`
- `MEDIUM`
- `COMPLEX`

## Generate Customers

Generate test customers for an account.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/GenerateCustomers' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN"
  }'
```

## Create Locations

Create additional locations for an account.

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreateLocations' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN"
  }'
```

## Link Bank Account

```bash
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/LinkBankAccount' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "ACCOUNT_TOKEN",
    "persona_key": "DEFAULT"
  }'
```

## Full Example: Create Account with Subscriptions

```bash
# 1. Create account
RESPONSE=$(curl -s -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreateAccount' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "youruser+'$(date +%s)'@example.com",
    "business_name": "Test Restaurant",
    "country_code": "US",
    "activate_payments": true
  }')

echo "$RESPONSE"
ACCOUNT_TOKEN=$(echo "$RESPONSE" | jq -r '.account_token')

# 2. Add subscriptions
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/CreateSubscriptions' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "'"$ACCOUNT_TOKEN"'",
    "plan_tokens": ["restaurants-plus"]
  }'

# 3. Generate catalog
curl -X POST \
  'https://api.staging.example.com/services/testdata.AccountFactoryService/GenerateCatalog' \
  -H 'Content-Type: application/json' \
  -d '{
    "account_token": "'"$ACCOUNT_TOKEN"'",
    "product": "POS",
    "pos_options": {
      "grid_complexity": "SIMPLE"
    }
  }'
```

## Generate Magic Link (One-Time Login)

Generate a one-time login link for a test account. This is a two-step process:

### Step 1: Authenticate and Get Session Token

```bash
curl -X POST \
  'https://api.staging.example.com/services/auth.AuthService/AppLogin' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "your-email@example.com",
    "password": "password"
  }'
```

### Step 2: Create One-Time Key

```bash
curl -X POST \
  'https://api.staging.example.com/1.0/auth/create-otk' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Session SESSION_TOKEN_HERE' \
  -d '{
    "client_credentials": {
      "device_details": {
        "type": "WEB"
      }
    }
  }'
```

### Step 3: Build Magic Link URL

```
https://staging.example.com/session/otk?one_time_key=ONE_TIME_KEY_HERE
```

## Login

After creating an account, you can login using either:

### Standard Login
- **URL**: `https://staging.example.com/login`
- **Email**: The email used during creation
- **Password**: `password`

### Magic Link (One-Time Login)
- Generate a magic link using the steps above
- Click the link to login automatically without entering credentials
