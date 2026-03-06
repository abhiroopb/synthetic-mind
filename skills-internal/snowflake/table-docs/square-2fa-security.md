# 2FA & Security

Query and analyze Two-Factor Authentication settings, credentials, and security configurations from data warehouse static tables.

## Tables

### YOUR_AUTH_SCHEMA.CREDENTIALS

User authentication settings.

**Key Fields:**
- `person_token`: User identifier
- `two_factor_state`: Can be 'NONE' or 'REQUIRED'
- `created_at`: Credential creation timestamp
- `updated_at`: Last update timestamp

### YOUR_AUTH_SCHEMA.TWO_FACTOR_REQUIREMENTS

Represents any 2FA requirement that may signify that 2FA is enabled on an account. Tracks per-user
(person_token) 2FA enrollment and current state.

**Key Fields:**
- `person_token`: User identifier
- `two_factor_state`: State of 2FA (e.g., 'REQUIRED')
- `two_factor_reason_id`: Reason for 2FA requirement (0=PERSONAL, 1=EMPLOYEE, 2=CUSTOMER, 3=ADMIN, 4=MERCHANT)

### YOUR_AUTH_SCHEMA.TWO_FACTOR_DETAILS

Represents any enrolled 2FA methods a user may have. Used to correlate with TWO_FACTOR_REQUIREMENTS
to see which specific 2FA methods a user has set up.

**Key Fields:**
- `person_token`: User identifier
- `method`: 2FA method type (SMS, GOOGLEAUTH, WEBAUTHN)
- `method_contact_details`: Contact details for the method (e.g., phone number for SMS)
- `hashed_method_contact_details`: Hashed version of contact details

### YOUR_AUTH_SCHEMA.TWO_FACTOR_PROMO_COHORT_DETAILS

Represents any 2FA promotional flow records for a specific customer_id.

**Key Fields:**
- `customer_id`: Customer identifier
- `mandatory_2fa_exception_reason`: Reason for 2FA exception if applicable

### YOUR_AUTH_SCHEMA.DEVICE_IDENTIFIERS

Device identification records.

## Table Relationships

### Authentication Flow

Tables commonly used together for authentication flow analysis:
- `YOUR_EVENT_SCHEMA.AUTH_EVENT` (see `auth-events.md`)
- `YOUR_AUTH_SCHEMA.TWO_FACTOR_REQUIREMENTS`
- `YOUR_AUTH_SCHEMA.TWO_FACTOR_DETAILS`

**Common join:** TWO_FACTOR_REQUIREMENTS and TWO_FACTOR_DETAILS join on `person_token`.

## Query Templates

### Person Alias and 2FA Cross-Analysis

These queries join CREDENTIALS with `YOUR_PERSON_SCHEMA.ALIASES`.

#### Get User 2FA Status and Aliases for Specific Person

```sql
SELECT
  c.person_token,
  c.two_factor_state,
  c.created_at as credential_created,
  c.updated_at as credential_updated,
  a.type as alias_type,
  a.value as alias_value,
  a.scope,
  a.created_at as alias_created
FROM YOUR_AUTH_SCHEMA.CREDENTIALS c
LEFT JOIN YOUR_PERSON_SCHEMA.ALIASES a
  ON a.customer_token = c.person_token
WHERE c.person_token = 'PERSON_TOKEN_HERE'
  AND (a.scope IS NULL OR a.scope = '')
ORDER BY a.type, a.created_at;
```

#### Find Users with Phone Only (No Email) and No 2FA

```sql
SELECT COUNT(DISTINCT c.person_token) as vulnerable_users
FROM YOUR_AUTH_SCHEMA.CREDENTIALS c
JOIN YOUR_PERSON_SCHEMA.ALIASES a
  ON a.customer_token = c.person_token
WHERE c.two_factor_state = 'NONE'
  AND a.type = 'PHONE'
  AND (a.scope IS NULL OR a.scope = '')
  AND NOT EXISTS (
    SELECT 1
    FROM YOUR_PERSON_SCHEMA.ALIASES a2
    WHERE a2.customer_token = c.person_token
      AND a2.type = 'EMAIL'
      AND (a2.scope IS NULL OR a2.scope = '')
  );
```

#### 2FA Adoption by Alias Type

```sql
SELECT
  CASE
    WHEN has_email = 1 AND has_phone = 1 THEN 'Email + Phone'
    WHEN has_email = 1 AND has_phone = 0 THEN 'Email Only'
    WHEN has_email = 0 AND has_phone = 1 THEN 'Phone Only'
    ELSE 'No Alias'
  END as user_type,
  COUNT(*) as total_users,
  SUM(CASE WHEN two_factor_state = 'REQUIRED' THEN 1 ELSE 0 END) as with_2fa,
  ROUND(
    SUM(CASE WHEN two_factor_state = 'REQUIRED' THEN 1 ELSE 0 END) * 100.0 /
    NULLIF(COUNT(*), 0),
    2
  ) as adoption_rate_pct
FROM (
  SELECT
    c.person_token,
    c.two_factor_state,
    MAX(CASE WHEN a.type = 'EMAIL' THEN 1 ELSE 0 END) as has_email,
    MAX(CASE WHEN a.type = 'PHONE' THEN 1 ELSE 0 END) as has_phone
  FROM YOUR_AUTH_SCHEMA.CREDENTIALS c
  LEFT JOIN YOUR_PERSON_SCHEMA.ALIASES a
    ON a.customer_token = c.person_token
    AND (a.scope IS NULL OR a.scope = '')
  GROUP BY c.person_token, c.two_factor_state
)
GROUP BY 1
ORDER BY 4 DESC;
```

#### Count SMS 2FA Methods

```sql
SELECT COUNT(*) as sms_2fa_count
FROM YOUR_AUTH_SCHEMA.TWO_FACTOR_DETAILS
WHERE METHOD = 'SMS';
```

#### 2FA Method Type Distribution

```sql
SELECT
  method,
  COUNT(*) as enrollment_count,
  COUNT(DISTINCT person_token) as unique_users,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM YOUR_AUTH_SCHEMA.TWO_FACTOR_DETAILS
GROUP BY method
ORDER BY enrollment_count DESC;
```
