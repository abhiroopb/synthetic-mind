---
name: merchant-factory
description: Creates staging merchants for Square using MerchantFactory API. Use when asked to create test merchants, generate catalogs, add subscriptions, or set up staging data.
---

# Merchant Factory

Create and configure staging merchants for Square using curl.

## Create Merchant

Creates a new staging merchant. Default password is `password`.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateMerchant' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "<ldap>+<timestamp>@squareup.com",
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
| `email` | Yes | Format: `<ldap>+<unix_timestamp>@squareup.com` |
| `business_name` | Yes | Business name |
| `country_code` | Yes | `US`, `CA`, `GB`, `AU`, `JP` |
| `preferred_language` | No | Default: `en` |
| `activate_payments` | No | Default: `false` |
| `configuration_id` | No | Merchant configuration ID |
| `link_bank_account` | No | Default: `false` |
| `owner_metadata` | No | Object with `phone_number` |

### Response

```json
{
  "status": "SUCCESS",
  "merchant_token": "XXXXXXXXXX",
  "unit_tokens": ["YYYYYYYYYY"]
}
```

## Create Subscriptions

Add subscriptions to an existing merchant.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateSubscriptions' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN",
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

## Create Square One Subscription

Add a Square One subscription to an existing merchant.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateSquareOneSubscription' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN",
    "plan_token": "square-one-plus-v2"
  }'
```

### Available Square One Plan Tokens

- `square-one-free-v1`
- `square-one-free-v2`
- `square-one-plus-v1`
- `square-one-plus-v2`
- `square-one-premium-v1`
- `square-one-premium-v2`

## Generate Catalog

Generate catalog items for a merchant.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/GenerateCatalog' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN",
    "product": "SPOS",
    "spos_options": {
      "grid_complexity": "SIMPLE",
      "business_type": "restaurant",
      "num_items_per_page": 10,
      "num_pages": 2
    }
  }'
```

### Catalog Products

- `SPOS` - Square Point of Sale
- `INVOICES`
- `ECOM`

### SPOS Grid Complexity

- `SIMPLE`
- `MEDIUM`
- `COMPLEX`

## Generate Customers

Generate test customers for a merchant.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/GenerateCustomers' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN"
  }'
```

## Create Locations

Create additional locations for a merchant.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateLocations' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN"
  }'
```

## Link Bank Account

> **Note**: As of 2025-01-08, this endpoint is not working due to backend requiring a multipassuser. See [PR #405590](https://github.com/squareup/java/pull/405590) for updates.

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/LinkBankAccount' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "MERCHANT_TOKEN",
    "persona_key": "DEFAULT"
  }'
```

## Full Example: Create Merchant with Subscriptions

```bash
# 1. Create merchant
RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateMerchant' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "yourldap+'$(date +%s)'@squareup.com",
    "business_name": "Test Restaurant",
    "country_code": "US",
    "activate_payments": true
  }')

echo "$RESPONSE"
MERCHANT_TOKEN=$(echo "$RESPONSE" | jq -r '.merchant_token')

# 2. Add subscriptions
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateSubscriptions' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "'"$MERCHANT_TOKEN"'",
    "plan_tokens": ["restaurants-plus"]
  }'

# 3. Generate catalog
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/GenerateCatalog' \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_token": "'"$MERCHANT_TOKEN"'",
    "product": "SPOS",
    "spos_options": {
      "grid_complexity": "SIMPLE"
    }
  }'
```

## Generate Magic Link (One-Time Login)

Generate a one-time login link for a merchant account. This is a two-step process:

### Step 1: Authenticate and Get Session Token

```bash
curl -X POST \
  'https://api.squareupstaging.com/services/squareup.multipass.external.MultipassAppService/AppLogin' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "your-email@squareup.com",
    "password": "password"
  }'
```

**Response:**
```json
{
  "session_token": "SESSION_TOKEN_HERE",
  ...
}
```

### Step 2: Create One-Time Key

Using the `session_token` from Step 1, create a one-time key:

```bash
curl -X POST \
  'https://api.squareupstaging.com/1.0/multipass/create-otk' \
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

**Response:**
```json
{
  "one_time_key": {
    "value": "ONE_TIME_KEY_HERE"
  },
  ...
}
```

### Step 3: Build Magic Link URL

The final one-time login URL:
```
https://squareupstaging.com/session/otk?one_time_key=ONE_TIME_KEY_HERE
```

### Complete Example: Generate Magic Link

```bash
EMAIL="yourldap+$(date +%s)@squareup.com"
PASSWORD="password"

# Step 1: Authenticate and get session token
echo "Authenticating..."
LOGIN_RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/services/squareup.multipass.external.MultipassAppService/AppLogin' \
  -H 'Content-Type: application/json' \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

SESSION_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.session_token')

# Step 2: Create one-time key
echo "Generating one-time key..."
OTK_RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/1.0/multipass/create-otk' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Session $SESSION_TOKEN" \
  -d '{
    "client_credentials": {
      "device_details": {
        "type": "WEB"
      }
    }
  }')

ONE_TIME_KEY=$(echo "$OTK_RESPONSE" | jq -r '.one_time_key.value')

# Step 3: Build magic link URL
MAGIC_LINK="https://squareupstaging.com/session/otk?one_time_key=$ONE_TIME_KEY"
echo "Magic Link: $MAGIC_LINK"
```

## Full Example: Create Merchant and Generate Magic Link

```bash
# 1. Create merchant
TIMESTAMP=$(date +%s)
EMAIL="yourldap+${TIMESTAMP}@squareup.com"

RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/services/squareup.merchantfactory.MerchantFactoryService/CreateMerchant' \
  -H 'Content-Type: application/json' \
  -d "{
    \"email\": \"$EMAIL\",
    \"business_name\": \"Test Business\",
    \"country_code\": \"US\",
    \"activate_payments\": true
  }")

echo "$RESPONSE"
MERCHANT_TOKEN=$(echo "$RESPONSE" | jq -r '.merchant_token')

# 2. Generate magic link
LOGIN_RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/services/squareup.multipass.external.MultipassAppService/AppLogin' \
  -H 'Content-Type: application/json' \
  -d "{\"email\": \"$EMAIL\", \"password\": \"password\"}")

SESSION_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.session_token')

OTK_RESPONSE=$(curl -s -X POST \
  'https://api.squareupstaging.com/1.0/multipass/create-otk' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Session $SESSION_TOKEN" \
  -d '{
    "client_credentials": {
      "device_details": {
        "type": "WEB"
      }
    }
  }')

ONE_TIME_KEY=$(echo "$OTK_RESPONSE" | jq -r '.one_time_key.value')
MAGIC_LINK="https://squareupstaging.com/session/otk?one_time_key=$ONE_TIME_KEY"

echo -e "\n✓ Merchant Created"
echo "Email: $EMAIL"
echo "Merchant Token: $MERCHANT_TOKEN"
echo -e "\n✓ Magic Link Generated:"
echo "$MAGIC_LINK"
```

## Login

After creating a merchant, you can login using either:

### Standard Login
- **URL**: `https://squareupstaging.com/login`
- **Email**: The email used during creation
- **Password**: `password`

### Magic Link (One-Time Login)
- Generate a magic link using the steps above
- Click the link to login automatically without entering credentials
