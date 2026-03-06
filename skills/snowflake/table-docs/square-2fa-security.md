# Square 2FA & Security

Query and analyze Two-Factor Authentication settings, credentials, and security configurations from Snowflake static tables.

## Tables

### MULTIPASS.RAW_OLTP.CREDENTIALS

User authentication settings.

**Key Fields:**
- `person_token`: User identifier
- `two_factor_state`: Can be 'NONE' or 'REQUIRED'
- `created_at`: Credential creation timestamp
- `updated_at`: Last update timestamp

### MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS

Represents any 2FA requirement that may signify that 2FA is enabled on an account. Tracks per-user
(person_token) 2FA enrollment and current state.

**Key Fields:**
- `person_token`: User identifier
- `two_factor_state`: State of 2FA (e.g., 'REQUIRED')
- `two_factor_reason_id`: Reason for 2FA requirement (0=PERSONAL, 1=EMPLOYEE, 2=CUSTOMER, 3=ADMIN, 4=MERCHANT)

### MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS

Represents any enrolled 2FA methods a user may have. Used to correlate with TWO_FACTOR_REQUIREMENTS
to see which specific 2FA methods a user has set up.

**Key Fields:**
- `person_token`: User identifier
- `method`: 2FA method type (SMS, GOOGLEAUTH, WEBAUTHN)
- `method_contact_details`: Contact details for the method (e.g., phone number for SMS)
- `hashed_method_contact_details`: Hashed version of contact details

### MULTIPASS.RAW_OLTP.TWO_FACTOR_PROMO_COHORT_DETAILS

Represents any 2FA promotional flow records for a specific merchant_token.

**Key Fields:**
- `merchant_token`: Merchant identifier
- `mandatory_2fa_exception_reason`: Reason for 2FA exception if applicable

### MULTIPASS.RAW_OLTP.DEVICE_IDENTIFIERS

Device identification records.

## Table Relationships

### Authentication Flow

Tables commonly used together for authentication flow analysis:
- `EVENTSTREAM2.CATALOGS.MULTIPASS_EVENT` (see `multipass-auth-events.md`)
- `MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS`
- `MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS`

**Common join:** TWO_FACTOR_REQUIREMENTS and TWO_FACTOR_DETAILS join on `person_token`.

## Query Templates

### Person Alias and 2FA Cross-Analysis

These queries join CREDENTIALS with `PERSON.RAW_OLTP.ALIASES` (documented in `square-person-oauth-devices.md`).

#### Get User 2FA Status and Aliases for Specific Person

```sql
-- Get comprehensive user profile including 2FA status and contact methods
SELECT
  c.person_token,
  c.two_factor_state,
  c.created_at as credential_created,
  c.updated_at as credential_updated,
  a.type as alias_type,
  a.value as alias_value,
  a.scope,
  a.created_at as alias_created
FROM MULTIPASS.RAW_OLTP.CREDENTIALS c
LEFT JOIN PERSON.RAW_OLTP.ALIASES a
  ON a.customer_token = c.person_token
WHERE c.person_token = 'PERSON_TOKEN_HERE'  -- Replace with actual person token
  AND (a.scope IS NULL OR a.scope = '')  -- Default scope only
ORDER BY a.type, a.created_at;
```

#### Find Users with Phone Only (No Email) and No 2FA

```sql
-- Identify vulnerable users: phone-only accounts without 2FA
SELECT COUNT(DISTINCT c.person_token) as vulnerable_users
FROM MULTIPASS.RAW_OLTP.CREDENTIALS c
JOIN PERSON.RAW_OLTP.ALIASES a
  ON a.customer_token = c.person_token
WHERE c.two_factor_state = 'NONE'
  AND a.type = 'PHONE'
  AND (a.scope IS NULL OR a.scope = '')
  AND NOT EXISTS (
    SELECT 1
    FROM PERSON.RAW_OLTP.ALIASES a2
    WHERE a2.customer_token = c.person_token
      AND a2.type = 'EMAIL'
      AND (a2.scope IS NULL OR a2.scope = '')
  );
```

#### Detailed Analysis of Phone-Only Users Without 2FA

```sql
-- Get details about phone-only users without 2FA
WITH phone_only_users AS (
  SELECT
    c.person_token,
    c.two_factor_state,
    c.created_at as account_created,
    c.updated_at as last_updated
  FROM MULTIPASS.RAW_OLTP.CREDENTIALS c
  WHERE c.two_factor_state = 'NONE'
    AND EXISTS (
      SELECT 1
      FROM PERSON.RAW_OLTP.ALIASES a
      WHERE a.customer_token = c.person_token
        AND a.type = 'PHONE'
        AND (a.scope IS NULL OR a.scope = '')
    )
    AND NOT EXISTS (
      SELECT 1
      FROM PERSON.RAW_OLTP.ALIASES a2
      WHERE a2.customer_token = c.person_token
        AND a2.type = 'EMAIL'
        AND (a2.scope IS NULL OR a2.scope = '')
    )
)
SELECT
  DATE_TRUNC('month', account_created) as creation_month,
  COUNT(*) as users_count,
  MIN(account_created) as earliest_account,
  MAX(account_created) as latest_account
FROM phone_only_users
GROUP BY 1
ORDER BY 1 DESC;
```

#### User Alias Distribution Analysis

```sql
-- Analyze distribution of alias types across users
WITH user_aliases AS (
  SELECT
    customer_token,
    SUM(CASE WHEN type = 'EMAIL' THEN 1 ELSE 0 END) as email_count,
    SUM(CASE WHEN type = 'PHONE' THEN 1 ELSE 0 END) as phone_count,
    SUM(CASE WHEN type = 'PAN_FIDELIUS' THEN 1 ELSE 0 END) as pan_count
  FROM PERSON.RAW_OLTP.ALIASES
  WHERE scope IS NULL OR scope = ''
  GROUP BY customer_token
)
SELECT
  CASE
    WHEN email_count > 0 AND phone_count > 0 THEN 'Email + Phone'
    WHEN email_count > 0 AND phone_count = 0 THEN 'Email Only'
    WHEN email_count = 0 AND phone_count > 0 THEN 'Phone Only'
    ELSE 'Other'
  END as alias_combination,
  COUNT(*) as user_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM user_aliases
GROUP BY 1
ORDER BY 2 DESC;
```

#### 2FA Adoption by Alias Type

```sql
-- Compare 2FA adoption rates between email vs phone users
WITH user_profile AS (
  SELECT
    c.person_token,
    c.two_factor_state,
    MAX(CASE WHEN a.type = 'EMAIL' THEN 1 ELSE 0 END) as has_email,
    MAX(CASE WHEN a.type = 'PHONE' THEN 1 ELSE 0 END) as has_phone
  FROM MULTIPASS.RAW_OLTP.CREDENTIALS c
  LEFT JOIN PERSON.RAW_OLTP.ALIASES a
    ON a.customer_token = c.person_token
    AND (a.scope IS NULL OR a.scope = '')
  GROUP BY c.person_token, c.two_factor_state
)
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
FROM user_profile
GROUP BY 1
ORDER BY 4 DESC;
```

#### Recent 2FA Changes for Users

```sql
-- Track recent 2FA state changes from credentials table
SELECT
  c.person_token,
  c.two_factor_state,
  c.updated_at,
  a.type as primary_alias_type,
  COUNT(DISTINCT a.type) as alias_type_count
FROM MULTIPASS.RAW_OLTP.CREDENTIALS c
LEFT JOIN PERSON.RAW_OLTP.ALIASES a
  ON a.customer_token = c.person_token
  AND (a.scope IS NULL OR a.scope = '')
WHERE c.updated_at >= DATEADD('day', -7, CURRENT_DATE())
GROUP BY c.person_token, c.two_factor_state, c.updated_at, a.type
ORDER BY c.updated_at DESC
LIMIT 1000;
```

### TWO_FACTOR_* Table Analysis

#### Count SMS 2FA Methods

```sql
-- Count total SMS 2FA methods enrolled
SELECT COUNT(*) as sms_2fa_count
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS
WHERE METHOD = 'SMS';
```

#### 2FA Mandatory Exception Reasons

```sql
-- Explore mandatory 2FA exception reasons
SELECT
  MANDATORY_2FA_EXCEPTION_REASON,
  COUNT(*) as occurrence_count
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_PROMO_COHORT_DETAILS
WHERE MANDATORY_2FA_EXCEPTION_REASON IS NOT NULL
GROUP BY MANDATORY_2FA_EXCEPTION_REASON
ORDER BY occurrence_count DESC
LIMIT 1000;
```

#### 2FA Requirements by Reason

```sql
-- Query 2FA requirements filtered by reason type
-- Reason IDs from TwoFactorReason proto:
-- 0 = PERSONAL, 1 = EMPLOYEE, 2 = CUSTOMER, 3 = ADMIN, 4 = MERCHANT
SELECT
  person_token,
  two_factor_state,
  two_factor_reason_id,
  created_at,
  updated_at
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS tfr
WHERE 1=1
  AND tfr.two_factor_reason_id = 4  -- Change to 0 for PERSONAL, 4 for MERCHANT, etc.
  AND tfr.two_factor_state = 'REQUIRED'
LIMIT 10000;
```

#### Distribution of Records per User

```sql
-- Analyze how many records each user has in a given table
-- Replace table and column references as needed:
--   TWO_FACTOR_DETAILS (method='SMS') → SMS phone numbers per user
--   TWO_FACTOR_REQUIREMENTS → 2FA requirements per user
--   TWO_FACTOR_DETAILS (no filter) → 2FA methods per user
SELECT
  cnt AS records_per_user,
  COUNT(*) as occurrences
FROM (
  SELECT
    person_token,
    COUNT(*) AS cnt
  FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS  -- Or TWO_FACTOR_REQUIREMENTS
  WHERE method = 'SMS'  -- Remove or change filter as needed
  GROUP BY person_token
)
GROUP BY cnt
ORDER BY cnt DESC
LIMIT 20;
```

#### Reused SMS Phone Numbers Analysis

```sql
-- Find SMS phone numbers used across multiple accounts
-- Note: Remove SHA2() to see actual phone numbers (PII)
SELECT
  SHA2(tfd.method_contact_details) as hashed_phone,
  COUNT(DISTINCT tfd.person_token) AS unique_users,
  COUNT(*) AS total_enrollments
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS tfd
WHERE method = 'SMS'
GROUP BY tfd.method_contact_details
HAVING COUNT(DISTINCT tfd.person_token) > 1
ORDER BY unique_users DESC
LIMIT 2000;
```

#### Users with Both Merchant and Personal 2FA Requirements

```sql
-- Find users who have both merchant-required and personal 2FA
WITH m_tfr AS (
  SELECT DISTINCT person_token
  FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS tfr
  WHERE tfr.two_factor_reason_id = 4
    AND tfr.two_factor_state = 'REQUIRED'
),
p_tfr AS (
  SELECT DISTINCT person_token
  FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS tfr
  WHERE tfr.two_factor_reason_id = 0
    AND tfr.two_factor_state = 'REQUIRED'
)
SELECT
  COUNT(*) as users_with_both_requirements
FROM m_tfr
WHERE m_tfr.person_token IN (SELECT person_token FROM p_tfr);
```

#### Device Identifiers Count

```sql
-- Get total count of device identifiers
SELECT COUNT(*) as total_device_identifiers
FROM MULTIPASS.RAW_OLTP.DEVICE_IDENTIFIERS;
```

#### 2FA Method Type Distribution

```sql
-- Analyze distribution of 2FA method types
SELECT
  method,
  COUNT(*) as enrollment_count,
  COUNT(DISTINCT person_token) as unique_users,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_DETAILS
GROUP BY method
ORDER BY enrollment_count DESC;
```

#### 2FA Requirements Summary by Reason

```sql
-- Analyze 2FA requirements by reason type
SELECT
  two_factor_reason_id,
  CASE two_factor_reason_id
    WHEN 0 THEN 'PERSONAL'
    WHEN 1 THEN 'EMPLOYEE'
    WHEN 2 THEN 'CUSTOMER'
    WHEN 3 THEN 'ADMIN'
    WHEN 4 THEN 'MERCHANT'
    ELSE 'OTHER'
  END as reason_name,
  two_factor_state,
  COUNT(*) as requirement_count,
  COUNT(DISTINCT person_token) as unique_users
FROM MULTIPASS.RAW_OLTP.TWO_FACTOR_REQUIREMENTS
GROUP BY two_factor_reason_id, two_factor_state
ORDER BY requirement_count DESC;
```
