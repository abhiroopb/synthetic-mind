# Query AEGIS Sponsorship Data

Query and analyze sponsored account (teen/family) data from the AEGIS Snowflake tables.

## Tables

All three tables live in the `AEGIS.AEGIS_PRODUCTION_001_1__AEGIS` schema. They are CDC-replicated from the AEGIS
production database and contain full history back to 2021-05.

### SPONSORED_ACCOUNT_STATE_TRANSITIONS

One row per state transition event for a sponsored account. Use this table when you need the history of sponsorship
state changes (e.g., when an account moved from PENDING to ACTIVE, or was SUSPENDED). ~93M rows total; ~420K rows
per week.

**No clustering key.** Filter on `CREATED_AT` (or `EVENT_SENT_AT`) to limit scan scope.

### SPONSORED_ACCOUNTS

One row per sponsored account reflecting the current/latest state. Use this table when you need the current
sponsorship status of an account, or to join to other tables via `DEPENDENT_CUSTOMER_ID` or `SPONSOR_CUSTOMER_ID`.
~28M rows total.

### CUSTOMERS

One row per AEGIS customer. Maps customer IDs (used in `SPONSORED_ACCOUNTS`) to customer tokens (used in P2P payment
tables). ~39M rows total.

**Key column:** `TOKEN` — this is the customer token (e.g., `C_gmcf2aya1`) that matches `SENDER_TOKEN` or
`RECIPIENT_CUSTOMER_TOKEN` in P2P payment tables.

## Domain Concepts

These concepts come from the AEGIS service's domain model.

### "Activeish" (sponsored) vs inactive

An account is considered **sponsored** ("activeish") if its state is `ACTIVE` or `SUSPENDED`. Both states grant the
dependent a valid sponsorship relationship. An account in `PENDING` or `CANCELED` is **inactive** — it does not have
a valid sponsorship.

When checking "is this customer sponsored?" for P2P payment analysis, check `state IN ('ACTIVE', 'SUSPENDED')`.

### Sponsorship tiers

- **TEEN** — ages 13+. The most common tier.
- **MANAGED_ACCOUNT** — ages 6-12 ("kids"). Less common; may not appear in short sample windows.

### State machine

Valid transitions follow a formal state machine:

```
PENDING  → ACTIVE, PENDING (reason update), CANCELED
ACTIVE   → SUSPENDED, CANCELED
SUSPENDED → ACTIVE, CANCELED
CANCELED → PENDING (re-request)
```

A PENDING account with a suspended sponsor becomes CANCELED, not SUSPENDED.

## Column Reference: SPONSORED_ACCOUNT_STATE_TRANSITIONS

| # | Field | Type | Description | Example / Enum Values |
|---|-------|------|-------------|----------------------|
| 1 | ID | NUMBER | Unique transition ID (monotonically increasing) | `93026569` |
| 2 | CREATED_AT | TIMESTAMP | When the transition occurred. **Always filter on this.** | `2026-02-03T14:22:16.828` |
| 3 | UPDATED_AT | TIMESTAMP | Usually equals CREATED_AT | |
| 4 | SPONSORED_ACCOUNT_ID | NUMBER | FK to `SPONSORED_ACCOUNTS.ID` | `27501870` |
| 5 | **STATE** | TEXT | State transitioned TO | **Enum:** `PENDING`, `ACTIVE`, `SUSPENDED`, `CANCELED` |
| 6 | PREVIOUS_STATE | TEXT | State transitioned FROM (null for first transition) | **Enum:** `PENDING`, `ACTIVE`, `SUSPENDED`, `CANCELED`, null |
| 7 | **STATE_REASON** | TEXT | Why the transition happened | See State Reasons section |
| 8 | FLOW_TOKEN | TEXT | Flow token associated with the transition (nullable) | `88rbve1v9sygkh552ycvpv33c` |
| 9 | TOKEN | TEXT | Unique transition token (`SAST_` prefix) | `SAST_8c8qu36dyksc751sj9ljvuv0x` |
| 10 | REQUEST_SOURCE | TEXT | Where the sponsorship request originated (nullable) | See Request Sources section |
| 11 | EVENT_SENT_AT | TIMESTAMP | When the event was published | `2026-02-03T14:22:16.851` |
| 12 | SIDE_EFFECTS_COMPLETED | NUMBER | Whether side effects completed (0 or 1) | `0`, `1` |
| 13 | SEND_EVENT | NUMBER | Whether event was sent (0 or 1) | `0`, `1` |
| — | __CDC_* / __TS_MS / __SOURCE_TS_MS / __SNAPSHOT / __DB_NAME / __ENTITY_SCHEMA_NAME / __DELETED_UPSTREAM | — | CDC metadata columns; generally not needed for analysis | |

### State Reasons (grouped by which state they produce)

**→ PENDING:** `DEPENDENT_REQUESTED`, `DEPENDENT_ORDERED_CARD`, `SPONSOR_REQUESTED`, `MANUAL_REVIEW_REQUIRED`,
`SPONSOR_DIDV_REQUIRED`, `ISSUER_ACCOUNT_LINKS_REQUIRED`, `ISSUER_ACCOUNT_LINKS_ESTABLISHED`.

**→ ACTIVE:** `SPONSOR_APPROVED`, `SPONSORSHIP_REINSTATED`, `SUPPORT_APPROVED`, `DEPENDENT_APPROVED`,
`SPONSOR_ONBOARDED_KID`.

**→ SUSPENDED:** `SPONSOR_IDV_REVOKED`, `SPONSOR_SUSPENDED`, `SPONSOR_DENYLISTED`, `SPONSOR_ISSUER_SUSPENDED`,
`ELIGIBILITY_VIOLATED`.

**→ CANCELED:** `SPONSOR_DECLINED`, `SPONSOR_DECLINED_DONT_KNOW_PERSON`,
`SPONSOR_DECLINED_KNOW_PERSON_DONT_WANT_TO_APPROVE`, `SPONSOR_DECLINED_KNOW_PERSON_NOT_BEST_SPONSOR`,
`SPONSOR_DECLINED_DONT_WANT_PRODUCT`, `SPONSOR_DECLINED_NONE_OF_THE_ABOVE`, `DEPENDENT_DECLINED`,
`SPONSOR_CANCELED_REQUEST`, `SPONSOR_ABANDONED_REQUEST`, `SPONSOR_ACCOUNT_CLOSED`, `DEPENDENT_ACCOUNT_CLOSED`,
`SUPPORT_CANCELED`, `SPONSOR_INELIGIBLE`, `SPONSORED_ELSEWHERE`, `ISSUER_ACCOUNT_LINKS_FAILED`,
`DEPENDENT_CANCELED_REQUEST`, `REQUEST_EXPIRED`, `GRADUATED`, `DEPENDENT_INELIGIBLE`, `RISK`,
`GRADUATION_JOURNEY_TERMINATED`, `MANUAL_REVIEW_DENIED`, `ATTESTATION_INVALID_NEW_REQUIREMENTS`.

### Request Sources

`CARD_ONBOARDING`, `P2P`, `PAPERMONEY_DEPOSIT`, `DEBIT_CASH_IN`, `FAMILY_ACCOUNT_NULL_STATE`, `INVITE_LINK`,
`INVESTING`, `CRYPTO`, `GIFT_CARD`, `IDENTITY_HUB`, `LIMITS_PAGE`, `RMA_CAMPAIGN_NUDGE`, `DECLINED_SPONSORSHIP`,
`ACTIVITY_ITEM`, `ONBOARDING`, `DISPUTES_STEP_UP`, `UNVERIFIED_P2P_RISK_AUTOFAIL`, `CANCELED_SPONSORSHIP`,
`ABANDONED_SPONSORSHIP_INVITATION`, `FAMILY_APPLET_NULL_STATE`, `CHECK_DEPOSIT`, `ENABLE_CARD`, `CASH_APP_PAY`,
`RMA_PERSISTENT_BANNER`.

## Column Reference: SPONSORED_ACCOUNTS

| # | Field | Type | Description | Example / Enum Values |
|---|-------|------|-------------|----------------------|
| 1 | ID | NUMBER | Unique sponsored account ID. FK target for `SPONSORED_ACCOUNT_STATE_TRANSITIONS.SPONSORED_ACCOUNT_ID` | `27501870` |
| 2 | CREATED_AT | TIMESTAMP | When the sponsorship was first created | |
| 3 | UPDATED_AT | TIMESTAMP | When the sponsorship was last updated | |
| 4 | TOKEN | TEXT | Unique account token (`SA_` prefix) | `SA_34ooeboxho1dwjeipvc8c3kn4` |
| 5 | **STATE** | TEXT | Current sponsorship state | **Enum:** `PENDING`, `ACTIVE`, `SUSPENDED`, `CANCELED` |
| 6 | **DEPENDENT_CUSTOMER_ID** | NUMBER | FK to `CUSTOMERS.ID` — the sponsored (teen) customer | `32624949384` |
| 7 | **SPONSOR_CUSTOMER_ID** | NUMBER | FK to `CUSTOMERS.ID` — the sponsoring (parent) customer | `30962641390` |
| 8 | STATE_REASON | TEXT | Reason for the current state | Same enum as transitions |
| 9 | LAST_REQUESTED_AT | TIMESTAMP | When the sponsorship was last requested | |
| 10 | SPONSORSHIP_TIER | TEXT | Sponsorship tier | **Enum:** `TEEN` (ages 13+), `MANAGED_ACCOUNT` (ages 6-12) |
| — | __CDC_* / etc. | — | CDC metadata columns | |

## Column Reference: CUSTOMERS

| # | Field | Type | Description | Example / Enum Values |
|---|-------|------|-------------|----------------------|
| 1 | ID | NUMBER | Unique customer ID. FK target for `SPONSORED_ACCOUNTS.DEPENDENT_CUSTOMER_ID` and `SPONSOR_CUSTOMER_ID` | `32616759007` |
| 2 | CREATED_AT | TIMESTAMP | When the customer record was created in AEGIS | |
| 3 | UPDATED_AT | TIMESTAMP | When the customer record was last updated | |
| 4 | **TOKEN** | TEXT | Customer token. Matches `SENDER_TOKEN` / `RECIPIENT_CUSTOMER_TOKEN` in P2P payment tables. | `C_gmcf2aya1` |
| 5 | FULL_NAME | BINARY | Customer's full name (encrypted/masked) | |
| 6 | PHOTO_URL | TEXT | Profile photo URL (masked in Snowflake) | |
| 7 | CASHTAG | TEXT | Customer's $cashtag (without `$` prefix) | `janedoe123` |
| 8 | BIRTH_DATE | BINARY | Date of birth (encrypted/masked) | |
| 9 | FORGOTTEN_AT | TIMESTAMP | When the customer was "forgotten" (GDPR), null if not | |
| — | __CDC_* / etc. | — | CDC metadata columns | |

## Join Patterns

### Building the "relevant transitions" CTE

The standard pattern joins all three tables to produce a flat view of transitions with customer tokens:

```sql
SELECT
    trns.id,
    trns.state,
    trns.previous_state,
    trns.state_reason,
    trns.created_at AS transitioned_at,
    trns.sponsored_account_id,
    customers.token AS customer_token
FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions trns
JOIN aegis.aegis_production_001_1__aegis.sponsored_accounts
    ON sponsored_accounts.id = trns.sponsored_account_id
JOIN aegis.aegis_production_001_1__aegis.customers
    ON customers.id = sponsored_accounts.dependent_customer_id
```

### As-of join: sponsorship state at payment creation time

To find the most recent sponsorship state of a customer at or before a given timestamp (e.g., payment creation),
use `QUALIFY ROW_NUMBER()`:

```sql
WITH relevant_transitions AS (
    SELECT trns.id, trns.state, customers.token AS customer_token, trns.created_at AS transitioned_at
    FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions trns
    JOIN aegis.aegis_production_001_1__aegis.sponsored_accounts
        ON sponsored_accounts.id = trns.sponsored_account_id
    JOIN aegis.aegis_production_001_1__aegis.customers
        ON customers.id = sponsored_accounts.dependent_customer_id
)
SELECT
    p.payment_id,
    t.state AS sponsorship_state_at_payment_time
FROM payments p
LEFT JOIN relevant_transitions t
    ON t.customer_token = p.sender_token
   AND t.transitioned_at <= p.created_at
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY p.payment_id
    ORDER BY t.transitioned_at DESC, t.id DESC
) = 1
```

The `ORDER BY t.transitioned_at DESC, t.id DESC` ensures that when multiple transitions share the same timestamp,
the latest one (by ID) wins.

### Joining to P2P payments via customer token

The bridge between AEGIS and P2P payment data is `CUSTOMERS.TOKEN`:

- For **sender** sponsorship: `customers.token = payment.sender_token`
- For **recipient** sponsorship: `customers.token = payment.recipient_customer_token`

### Full example: payment outcomes for customers with PENDING sponsorship

```sql
WITH payments AS (
    SELECT payment_id, cancellation_reason, failure_reason_code, payment_state_code,
           created_at, sender_token, orientation, recipient_customer_token
    FROM app_cash.cash_data_bot.p2pengine_payment_state_latest_event
    WHERE created_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
)
, relevant_transitions AS (
    SELECT trns.id, trns.state, customers.token AS customer_token, trns.created_at AS transitioned_at
    FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions trns
    JOIN aegis.aegis_production_001_1__aegis.sponsored_accounts
        ON sponsored_accounts.id = trns.sponsored_account_id
    JOIN aegis.aegis_production_001_1__aegis.customers
        ON customers.id = sponsored_accounts.dependent_customer_id
)
, sender_asof AS (
    SELECT p.payment_id, t.state AS sender_sponsorship_state
    FROM payments p
    LEFT JOIN relevant_transitions t
        ON t.customer_token = p.sender_token
       AND t.transitioned_at <= p.created_at
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY p.payment_id
        ORDER BY t.transitioned_at DESC, t.id DESC
    ) = 1
)
, recipient_asof AS (
    SELECT p.payment_id, t.state AS recipient_sponsorship_state
    FROM payments p
    LEFT JOIN relevant_transitions t
        ON t.customer_token = p.recipient_customer_token
       AND t.transitioned_at <= p.created_at
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY p.payment_id
        ORDER BY t.transitioned_at DESC, t.id DESC
    ) = 1
)
SELECT
    COALESCE(p.cancellation_reason, p.failure_reason_code, p.payment_state_code) AS outcome,
    COUNT(*) AS cnt
FROM payments p
LEFT JOIN sender_asof sa USING (payment_id)
LEFT JOIN recipient_asof ra USING (payment_id)
WHERE (
    (p.orientation = 'CASH' AND sa.sender_sponsorship_state = 'PENDING')
    OR
    (p.orientation = 'BILL' AND ra.recipient_sponsorship_state = 'PENDING')
)
GROUP BY outcome
ORDER BY cnt DESC
```

## Common Query Patterns

### Distinct sponsorship states

```sql
SELECT DISTINCT state
FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions
WHERE created_at >= DATEADD(day, -7, CURRENT_DATE())
```

### Count transitions by state and reason

```sql
SELECT state, state_reason, COUNT(*) AS cnt
FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions
WHERE created_at >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY state, state_reason
ORDER BY cnt DESC
```

### Find the current sponsorship state for a customer token

```sql
SELECT sa.state, sa.state_reason, sa.sponsorship_tier, sa.updated_at
FROM aegis.aegis_production_001_1__aegis.customers c
JOIN aegis.aegis_production_001_1__aegis.sponsored_accounts sa
    ON sa.dependent_customer_id = c.id
WHERE c.token = 'C_xxxxxxxxx'
```

### Check if a customer is sponsored (current state)

```sql
SELECT c.token, sa.state
FROM aegis.aegis_production_001_1__aegis.customers c
JOIN aegis.aegis_production_001_1__aegis.sponsored_accounts sa
    ON sa.dependent_customer_id = c.id
WHERE c.token IN ('C_token1', 'C_token2')
```

### Count sponsorship requests by source

```sql
SELECT request_source, COUNT(*) AS cnt
FROM aegis.aegis_production_001_1__aegis.sponsored_account_state_transitions
WHERE created_at >= DATEADD(day, -7, CURRENT_DATE())
  AND request_source IS NOT NULL
GROUP BY request_source
ORDER BY cnt DESC
```
