# Brand A Person, OAuth & Devices

Query and analyze Brand A person identity, OAuth authorizations, device registry, and merchant/employee data from Snowflake.

## Tables

### YOUR_PERSON_SCHEMA.RAW_OLTP.PROFILES

Primary source of all person_token values that exist at Brand A. Each row represents a unique person.
This table is fundamental for user identity management.

### YOUR_PERSON_SCHEMA.RAW_OLTP.ALIASES

Stores all known aliases (email addresses, phone numbers, etc.) for each person, linked by
customer_token (person_token). Essential for user contact information and identity verification.

**Key Fields:**
- `customer_token`: Maps to credentials.person_token
- `type`: Can be 'EMAIL', 'PHONE', 'PAN_FIDELIUS', or 'UNKNOWN'
- `scope`: Default scope is NULL or empty string
- `value`: The actual email or phone number (encrypted)
- `created_at`: Alias creation timestamp

### OAUTH.OAUTH_PRODUCTION_AURORA_001__COURIC_PRODUCTION.OAUTH_AUTHORIZATIONS

OAuth authorization records, including revocation data.

### DEVICEREGISTRY.RAW_OLTP.DEVICES

Repository of registered devices associated with users, primarily supporting device-push notifications
and authentication workflows.

### DEVICEREGISTRY.RAW_OLTP.DEVICE_USAGES

Represents the observed association of a device with either a person or a unit. Important for
tracking device usage patterns and user-device relationships.

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Merchant information. For ROSTER merchant/unit token lookups, see `roster-merchant-location-employee-lookups.md`.

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Employee records.

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Role assignments.

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Role definitions.

## Table Relationships

### User Identity

- PROFILES and ALIASES join on `person_token` (`ALIASES.customer_token = PROFILES.person_token`)

### Device Management

- DEVICES and DEVICE_USAGES join on `device_id`

### Merchant/Employee

- MERCHANTS → EMPLOYEES on `merchant_id`
- EMPLOYEES → EMPLOYEE_ROLE_ASSIGNMENTS on `employee_id`
- EMPLOYEE_ROLE_ASSIGNMENTS → EMPLOYEE_ROLES on `employee_role_id`

## Query Templates

### OAuth Authorization Revocations

```sql
-- Find total number of authorizations revoked per day (last 90 days)
-- This queries the OAuth database directly for revocation data
SELECT
  DATE(REVOKED_AT) as revoke_date,
  COUNT(*) as total_revocations
FROM OAUTH.OAUTH_PRODUCTION_AURORA_001__COURIC_PRODUCTION.OAUTH_AUTHORIZATIONS
WHERE REVOKED_AT >= DATEADD('day', -90, CURRENT_DATE())
  AND REVOKED_AT IS NOT NULL
GROUP BY DATE(REVOKED_AT)
ORDER BY revoke_date DESC;
```

### Merchant and Employee Analysis

#### Get Account Owners for Specific Merchants

```sql
-- Find all account owners for given merchant IDs
SELECT
  m.id as merchant_id,
  m.name as merchant_name,
  e.id as employee_id,
  e.person_id,
  er.role_type
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE m
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE e
  ON e.merchant_id = m.id
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE era
  ON era.employee_id = e.id
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE er
  ON er.id = era.employee_role_id
WHERE 1=1
  AND er.role_type = 'ACCOUNT_OWNER'
  AND m.id IN ('MERCHANT_ID_1', 'MERCHANT_ID_2')  -- Replace with actual merchant IDs
ORDER BY m.id, e.person_id;
```

#### Get All Employees for Specific Merchants

```sql
-- Find all employees and their roles for given merchants
SELECT
  m.id as merchant_id,
  m.name as merchant_name,
  e.id as employee_id,
  e.person_id,
  er.role_type,
  COUNT(*) OVER (PARTITION BY m.id) as total_employees_per_merchant,
  COUNT(*) OVER (PARTITION BY m.id, er.role_type) as employees_per_role
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE m
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE e
  ON e.merchant_id = m.id
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE era
  ON era.employee_id = e.id
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE er
  ON er.id = era.employee_role_id
WHERE 1=1
  AND m.id IN ('MERCHANT_ID_1', 'MERCHANT_ID_2')  -- Replace with actual merchant IDs
ORDER BY m.id, er.role_type, e.person_id;
```

## Snowflake Context

| Database | Schema | Table | Description |
|----------|--------|-------|-------------|
| PERSON | RAW_OLTP | PROFILES | Primary source of all person_token values at Brand A. Each row represents a unique person. |
| PERSON | RAW_OLTP | ALIASES | Stores all known aliases (email, phone, etc.) for each person, linked by customer_token (person_token). |
| ROSTER | MERCHANTS | MERCHANTS | Merchant information. |
| ROSTER | MERCHANTS | EMPLOYEES | Tracks the relationship between merchants and their employees. |
| DEVICEREGISTRY | RAW_OLTP | DEVICES | Repository of registered devices associated with users, primarily supporting device-push notifications and authentication workflows. |
| DEVICEREGISTRY | RAW_OLTP | DEVICE_USAGES | Represents the observed association of a device with either a person or a unit. |
| OAUTH | OAUTH_PRODUCTION_AURORA_001__COURIC_PRODUCTION | OAUTH_AUTHORIZATIONS | OAuth authorization records, including revocation data. |
