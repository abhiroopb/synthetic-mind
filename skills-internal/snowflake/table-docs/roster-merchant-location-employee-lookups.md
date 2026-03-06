# ROSTER Merchant, Location & Employee Lookups

Shared patterns for looking up merchants, locations (units), and employees from the ROSTER database.

## Tables

### ROSTER.RAW_OLTP.MERCHANTS

Master merchant table. Contains the canonical merchant record.

**Important:** The `MERCHANT_TOKEN` column is **BINARY**. When comparing to string merchant_token values from other databases (ONBOARD, LEGALENTITIES, etc.), cast it:

```sql
TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')
```

**Key Fields:**
- `MERCHANT_TOKEN` (BINARY) — Merchant token (use `TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')` for string comparison)
- `PRIMARY_NAME` (TEXT) — Primary merchant name

### ROSTER.MERCHANTS.MERCHANTS

Merchant information. `ID` is the same underlying value as `ROSTER.RAW_OLTP.MERCHANTS.MERCHANT_TOKEN` but stored as VARCHAR.

**Key Fields:**
- `ID` (VARCHAR) — Merchant token
- `MAIN_LOCATION_ID` (VARCHAR) — FK → LOCATIONS.ID (primary location for this merchant)
- `BUSINESS_UNIT` (VARCHAR) — e.g., 'SQUARE'
- `STATUS` (BOOLEAN) — Active status
- `COUNTRY` (VARCHAR) — Country code (e.g., 'US', 'CA', 'JP')
- `CURRENCY` (VARCHAR) — e.g., 'USD', 'CAD'
- `IS_TEST` (BOOLEAN)
- `CREATED_AT`, `UPDATED_AT` (TIMESTAMP_NTZ)

### ROSTER.MERCHANTS.LOCATIONS

Locations (units) belonging to a merchant. One merchant can have many locations.

**Key Fields:**
- `ID` (VARCHAR) — Location/unit token
- `MERCHANT_ID` (VARCHAR) — FK → MERCHANTS.ID
- `BUSINESS_UNIT` (VARCHAR)
- `TIMEZONE` (VARCHAR)
- `IS_ACTIVE` (BOOLEAN)
- `IS_TEST` (BOOLEAN)
- `LANGUAGE_CODE` (VARCHAR)
- `CURRENCY` (VARCHAR)
- `IS_MOBILE` (BOOLEAN)
- `BUSINESS_TYPE` (VARCHAR) — e.g., 'food_stores_convenience_stores_and_specialty_markets'
- `CREATED_AT`, `UPDATED_AT` (TIMESTAMP_NTZ)

### ROSTER.MERCHANTS.EMPLOYEES

Employee records linked to merchants.

**Key Fields:**
- `ID` (VARCHAR) — Employee token
- `MERCHANT_ID` (VARCHAR) — FK → MERCHANTS.ID (merchant token)
- `PERSON_ID` (VARCHAR) — Person token (used by Accounts team and multipass/person services)

### ROSTER.MERCHANTS.EMPLOYEE_LOCATIONS

Maps employees to specific locations within a merchant.

**Key Fields:**
- `EMPLOYEE_ID` (VARCHAR) — FK → EMPLOYEES.ID
- `LOCATION_ID` (VARCHAR) — FK → LOCATIONS.ID

### ROSTER.MERCHANTS.EMPLOYEE_ROLE_ASSIGNMENTS

Role assignments for employees.

**Key Fields:**
- `EMPLOYEE_ID` (VARCHAR) — FK → EMPLOYEES.ID
- `EMPLOYEE_ROLE_ID` (VARCHAR) — FK → EMPLOYEE_ROLES.ID

### ROSTER.MERCHANTS.EMPLOYEE_ROLES

Role definitions.

**Key Fields:**
- `ID` (VARCHAR) — Role ID
- `ROLE_TYPE` (VARCHAR) — Role type (e.g., 'ACCOUNT_OWNER')

## Table Relationships

```
MERCHANTS (ID = merchant_token)
├── LOCATIONS (MERCHANT_ID → MERCHANTS.ID)  [one-to-many]
│   └── MERCHANTS.MAIN_LOCATION_ID → LOCATIONS.ID  [primary location]
├── EMPLOYEES (MERCHANT_ID → MERCHANTS.ID)
│   ├── EMPLOYEE_LOCATIONS (EMPLOYEE_ID → EMPLOYEES.ID, LOCATION_ID → LOCATIONS.ID)
│   └── EMPLOYEE_ROLE_ASSIGNMENTS (EMPLOYEE_ID → EMPLOYEES.ID)
│       └── EMPLOYEE_ROLES (ID ← EMPLOYEE_ROLE_ASSIGNMENTS.EMPLOYEE_ROLE_ID)
└── RAW_OLTP.MERCHANTS: TO_VARCHAR(MERCHANT_TOKEN, 'UTF-8') = MERCHANTS.ID
```

## MERCHANT_TOKEN Binary Cast Pattern

`ROSTER.RAW_OLTP.MERCHANTS` stores `MERCHANT_TOKEN` as BINARY. Other databases (ONBOARD, LEGALENTITIES, MULTIPASS) store it as TEXT. Always cast when joining:

```sql
-- Join ROSTER RAW_OLTP to any table with a string merchant_token
SELECT ...
FROM ROSTER.RAW_OLTP.MERCHANTS M
JOIN <other_table> T
    ON T.MERCHANT_TOKEN = TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')
WHERE TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8') = '<merchant_token_string>'
```

**Tip:** `ROSTER.MERCHANTS.MERCHANTS.ID` stores the same value as VARCHAR — no casting needed when joining to that table instead.

## Merchant ↔ Location Mapping

### Merchant → All Locations

```sql
SELECT
    L.ID AS location_id,
    L.MERCHANT_ID,
    L.TIMEZONE,
    L.IS_ACTIVE,
    L.BUSINESS_TYPE
FROM ROSTER.MERCHANTS.LOCATIONS L
WHERE L.MERCHANT_ID = '<merchant_token>'
```

### Merchant → Main Location

```sql
SELECT
    M.ID AS merchant_id,
    M.MAIN_LOCATION_ID,
    L.TIMEZONE,
    L.IS_ACTIVE,
    L.BUSINESS_TYPE
FROM ROSTER.MERCHANTS.MERCHANTS M
JOIN ROSTER.MERCHANTS.LOCATIONS L
    ON L.ID = M.MAIN_LOCATION_ID
WHERE M.ID = '<merchant_token>'
```

### Location → Merchant

```sql
SELECT
    M.ID AS merchant_id,
    M.COUNTRY,
    M.CURRENCY,
    M.MAIN_LOCATION_ID
FROM ROSTER.MERCHANTS.LOCATIONS L
JOIN ROSTER.MERCHANTS.MERCHANTS M
    ON M.ID = L.MERCHANT_ID
WHERE L.ID = '<location_id>'
```

## Employee Queries

### Account Owners for a Merchant

```sql
SELECT
    M.ID AS merchant_id,
    E.ID AS employee_id,
    E.PERSON_ID,
    ER.ROLE_TYPE
FROM ROSTER.MERCHANTS.MERCHANTS M
JOIN ROSTER.MERCHANTS.EMPLOYEES E
    ON E.MERCHANT_ID = M.ID
JOIN ROSTER.MERCHANTS.EMPLOYEE_ROLE_ASSIGNMENTS ERA
    ON ERA.EMPLOYEE_ID = E.ID
JOIN ROSTER.MERCHANTS.EMPLOYEE_ROLES ER
    ON ER.ID = ERA.EMPLOYEE_ROLE_ID
WHERE ER.ROLE_TYPE = 'ACCOUNT_OWNER'
    AND M.ID = '<merchant_token>'
```

### Employees at a Specific Location

```sql
SELECT
    E.ID AS employee_id,
    E.PERSON_ID,
    EL.LOCATION_ID
FROM ROSTER.MERCHANTS.EMPLOYEE_LOCATIONS EL
JOIN ROSTER.MERCHANTS.EMPLOYEES E
    ON E.ID = EL.EMPLOYEE_ID
WHERE EL.LOCATION_ID = '<location_id>'
```

## Notes

- **One merchant, many locations:** ~2M merchants have multiple locations. `MERCHANTS.MAIN_LOCATION_ID` identifies the primary one.
- **RAW_OLTP vs MERCHANTS schema:** `ROSTER.RAW_OLTP.MERCHANTS.MERCHANT_TOKEN` (BINARY) = `ROSTER.MERCHANTS.MERCHANTS.ID` (VARCHAR). Use MERCHANTS schema for joins within ROSTER; use RAW_OLTP when you need `PRIMARY_NAME` or the binary token.
- **Cross-database joins:** Other databases (LEGALENTITIES, MULTIPASS, ONBOARD) store merchant_token as TEXT. Use `TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')` when joining RAW_OLTP to them.
- **LEGALENTITIES link:** `LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT` maps `STRUCTURE_TOKEN` → `MERCHANT_TOKEN` (TEXT).
