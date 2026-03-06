# Query Limit Decision Events

Query and analyze limit decision data for P2P payments from Snowflake.

## Table

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Records from the cash-eligibility service documenting each limit validation decision for a payment. Typically one row
per customer per payment, but can have multiple rows when limits are re-evaluated (e.g., funding instrument change
triggers releasing old limits and reserving new ones). ~41 billion rows total.

**Not a payment-level table.** Each row is a limit check for one customer on one payment. A single P2P payment
usually has ~2 rows (one for sender, one for recipient). Use `SPLIT_PART(payment_token, ':', 1)` to extract the
payment ID for joining to payment tables.

**Not limited to P2P.** This table also records limit decisions for cash-ins, cash-outs, bank transfers, BTC
transactions, etc. Filter with `payment_token LIKE 'P2PE_%'` to restrict to P2P payments.

**Clustering key:** `LINEAR(event_received_at::date)`. Always filter on `EVENT_OCCURRED_AT` (or `EVENT_RECEIVED_AT`)
to leverage clustering. Default to `WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())` unless the user
specifies a different range.

**Source code:** The event is published by `LimitDecisionEventPublisher` in `cash-eligibility`. The proto is defined
at `cash-limits/protos/src/main/proto/example/app/cashlimits/events/limit_decision_event.proto`. The core decision
logic is in `LimitChecker.buildValidationDecision()` in `cash-limits`.

## Column Reference

- **Nullable**: Y = null values observed in practice, N = always populated
- **FK**: indicates column joins to another table

| # | Field | Type | Nullable | FK | Description | Example / Enum Values |
|---|-------|------|----------|----|-------------|----------------------|
| 1 | EVENT_OCCURRED_AT | TIMESTAMP | N | | When the limit decision occurred | `2026-02-01T20:47:54.259` |
| 2 | EVENT_RECEIVED_AT | TIMESTAMP | N | | When the event was received by the pipeline | `2026-02-01T20:47:54.262` |
| 3 | OFFSET | NUMBER | N | | Kafka offset | `2635552830` |
| 4 | EVENTLY_ID | TEXT | N | | Unique event identifier (UUID) | `f218bc3e-ff4b-42e5-a139-2c671cc75073` |
| 5 | EVENTLY_TOPIC | TEXT | Y | | Always null for P2P events | |
| 6 | EVENTLY_SOURCE | TEXT | N | | System that produced the event | `cash-eligibility` |
| 7 | EVENTLY_TYPE | TEXT | N | | Proto type of the event | `type.googleapis.com/example.app.cashlimits.events.LimitDecisionEvent` |
| 8 | **CUSTOMER_TOKEN** | TEXT | N | `P2PENGINE_PAYMENT_STATE_LATEST_EVENT` (as `SENDER_TOKEN` or `RECIPIENT_CUSTOMER_TOKEN`) | Customer whose limits were checked | `C_sscgx1y5b` |
| 9 | INSTRUMENT_TOKEN | TEXT | Y | | Instrument token checked (null for balance-only checks) | `B$_C_sscgx1y5b`, `55318d6a...` |
| 10 | TRANSFER_TOKEN | TEXT | Y | | Transfer token (rarely populated for P2P) | |
| 11 | **PAYMENT_TOKEN** | TEXT | N | `P2PENGINE_PAYMENT_STATE_LATEST_EVENT` (as `PAYMENT_ID`, via `SPLIT_PART(payment_token, ':', 1)`) | Payment identifier. See "Payment Token Format" section. | `P2PE_FIAT_7E6F8BAA...` |
| 12 | MOVEMENT_TOKEN | TEXT | N | | Usually same as payment_token (without suffix) | `P2PE_FIAT_7E6F8BAA...` |
| 13 | BILL_TOKEN | TEXT | Y | | Bill token (null for CASH-orientation payments) | |
| 14 | AMOUNT | NUMBER | N | | Transaction amount in cents | `1000` ($10) |
| 15 | CURRENCY_CODE | TEXT | N | | Currency | `USD` |
| 16 | **VALIDATION_RESULT** | TEXT | N | | **Important.** Outcome of the limit check. See "Decision Logic" section. | **Enum:** `VALID` (99.7%), `BLOCKED` (0.17%), `VALID_WITH_CUSTOMER_ACTION` (0.14%) |
| 17 | BYPASSED_LIMITS | BOOLEAN | N | | Whether limits were bypassed (rare, ~0.07%) | `false`, `true` |
| 18 | IDV_STATUS | TEXT | Y | | Customer's IDV verification status. `VERIFIED` if eIDV or document IDV passed; `NOT_VERIFIED` otherwise; null if no IDV data exists. | **Enum:** `VERIFIED` (89%), `NOT_VERIFIED` (4.5%), null (6.4%) |
| 19 | LIMIT_CALCULATION_METHOD | TEXT | N | | How limits were calculated. `TIERED_LIMITS` = standard IDV-based tiers (most customers). `STATUS_LIMITS` = legacy status-level-based limits (sponsored/teen accounts). | **Enum:** `TIERED_LIMITS` (90%), `STATUS_LIMITS` (10%), `OTHER` (<0.1%) |
| 20 | RATE_PLAN | TEXT | Y | | Customer's rate plan | **Enum:** `UNDECIDED_DEFERRED` (90%), `PERSONAL`, `BUSINESS_2_60`, `BUSINESS_2_75`, `BUSINESS_0`, `BUSINESS_1_9` |
| 21 | REGION | TEXT | N | | Customer's region | `USA` |
| 22 | **SPONSORSHIP_STATUS** | TEXT | N | | Whether the customer is sponsored (teen/family account). Derived from AEGIS `SponsorshipState.ACTIVE` → `SPONSORED`; all other states → `NOT_SPONSORED`. | **Enum:** `NOT_SPONSORED` (90%), `SPONSORED` (10%) |
| 23 | STATUS_LEVEL | TEXT | Y | | Customer's status level within the limits system | **Enum (by frequency):** `GOLD_7_5K`, `GOLD`, `GOLD_10K`, `GREEN`, null. Also rare: `SQUARE_50M`, `SQUARE_1M`, `SQUARE_500K`, `GIVER_150K`, etc. |
| 24 | TIER | TEXT | N | | Customer's limits tier. `TIER_0` = sponsored, `TIER_1` = unverified, `TIER_2` = rare, `TIER_3` = eIDV verified, `TIER_3_PLUS` = eIDV verified (higher limits), `TIER_4` = document IDV verified (highest limits). | **Enum:** `TIER_3_PLUS` (51%), `TIER_4` (29%), `TIER_0` (10%), `TIER_3` (9%), `TIER_1` (1%), `TIER_2` (<0.01%) |
| 25 | USING_LINKED_CUSTOMERS | BOOLEAN | N | | Whether limits are shared across linked customers | `false` (88%), `true` (12%) |
| 26 | LINKED_CUSTOMER_TOKEN | ARRAY | N | | Array of customer tokens sharing limits | `["C_nmcgx0mqj"]` |
| 27 | **USAGES** | ARRAY | N | | **Important.** Current and projected limit usages across all categories and time windows. See "Querying Usages" section. | |
| 28 | **CUSTOMER_ACTIONS** | ARRAY | N | | **Important.** Actions required from customer to proceed. Empty when `VALID`. See "Decision Logic" section. | **Values:** `IDV`, `SPONSORSHIP`, `REQUEST_LIMITS_INCREASE_FROM_SPONSOR`, `DOCUMENT_IDV`, `SELECT_NON_BALANCE_INSTRUMENT` |
| 29 | **LIMITS_EXCEEDED** | ARRAY | N | | **Important.** Which limits were exceeded. Empty when `VALID`. See "Limits Exceeded Values" section. | |
| 30 | AMOUNT_OBJECT | OBJECT | Y | | Deprecated; use AMOUNT and CURRENCY_CODE instead (always null in recent data) | |
| 31 | CUSTOMER_ATTRIBUTES | OBJECT | Y | | Deprecated; use CUSTOMER_ATTRIBUTES_VARIANT instead (always null in recent data) | |
| 32 | LOAD_TIMESTAMP | TIMESTAMP | N | | When the row was loaded | |
| 33 | ETL_PRIMARY_KEY | TEXT | N | | Composite key: `customer_token__instrument_token__payment_token__amount_json__validation_result` | |
| 34 | ETL_UPSTREAM_TS | TIMESTAMP | N | | ETL upstream timestamp | |
| 35 | ETL_CHUNK_TS | TIMESTAMP | Y | | ETL chunk timestamp (usually null) | |
| 36 | ETL_ROW_HASH | TEXT | N | | Hash for ETL deduplication | |
| 37 | ETL_UPDATE_TS | TIMESTAMP | N | | When the row was last updated by ETL | |
| 38 | ETL_INSERT_TS | TIMESTAMP | N | | When the row was first inserted by ETL | |
| 39 | LIMIT_CONFIGURATION | ARRAY | Y | | The customer's full limit configuration at decision time. Array of objects with `amount`, `duration_in_days`, `limit_category`, `type`. See "Querying Limit Configuration" section. | |
| 40 | AMOUNT_VARIANT | VARIANT | Y | | Amount as a variant object | `{"amount": 1000, "currency_code": "USD"}` |
| 41 | CUSTOMER_ATTRIBUTES_VARIANT | VARIANT | Y | | All customer attributes as a variant object. Keys: `bypassed_limits`, `idv_status`, `limit_calculation_method`, `limit_decision_source`, `rate_plan`, `region`, `sponsorship_status`, `sponsorship_tier`, `status_level`, `tenant_token`, `tier`, `using_linked_customers`. | |

## Payment Token Format

The `PAYMENT_TOKEN` column has two formats:

- **CASH (send) payments:** `P2PE_FIAT_<id>` — no suffix, the payment_token equals the payment ID.
- **BILL (request) payments:** `P2PE_FIAT_<id>:sender:C_<token>` or `P2PE_FIAT_<id>:recipient:C_<token>` — suffixed
  with the role and customer token.

~94% of rows have no suffix, ~4% have `:sender:`, ~3% have `:recipient:`.

**Why the suffix exists:** For BILL payments, the sender and recipient have their limits reserved independently with
separate transaction tokens. The suffix is constructed in the p2p-engine code
(`UsageUpdate.toTransactionTokenForBillGetterLimits` / `toTransactionTokenForBillInitiatorLimits`):
- `:sender:C_<token>` — the bill getter's (sender's) limits reservation
- `:recipient:C_<token>` — the bill initiator's (recipient's) limits reservation

**Always use `SPLIT_PART(payment_token, ':', 1)` to extract the payment ID** for joining to other tables:

```sql
SPLIT_PART(payment_token, ':', 1) AS payment_id
```

## Decision Logic

The `VALIDATION_RESULT` is determined by `LimitChecker.buildValidationDecision()` in cash-limits. The logic:

1. **Compute exceeded limits** for the customer's current limit configuration.
2. If the exceeded limits are all "soft" limits (e.g., prefund bank transfer limits) → `VALID`.
3. If the only exceeded limit is `CUSTOMER_BALANCE` → `VALID_WITH_CUSTOMER_ACTION` with
   `SELECT_NON_BALANCE_INSTRUMENT` (customer can switch to a card).
4. Otherwise, check if any `customerActionLimits` (IDV, sponsorship, etc.) would make the transaction pass:
   - If yes → `VALID_WITH_CUSTOMER_ACTION` with the applicable actions (e.g., `IDV`, `SPONSORSHIP`).
   - If no → `BLOCKED`.

The `CUSTOMER_ACTIONS` values and their meanings:

| Action | Description |
|--------|-------------|
| `IDV` | Customer can complete electronic identity verification (eIDV) to raise limits (Tier 1 → Tier 3/3+) |
| `DOCUMENT_IDV` | Customer has completed eIDV but hit Tier 3/3+ limits; can do document IDV (→ Tier 4) for higher limits |
| `SPONSORSHIP` | Sponsored (teen/family) customer can get limits raised through sponsorship relationship |
| `REQUEST_LIMITS_INCREASE_FROM_SPONSOR` | Sponsored customer can ask their sponsor to raise custom threshold limits |
| `SELECT_NON_BALANCE_INSTRUMENT` | Only the `CUSTOMER_BALANCE` limit was exceeded; customer can select a card instead |

When the p2p-engine receives these results, `BLOCKED` causes the payment to fail with
`SENDER_FAILED_MONTHLY_LIMITS` (or similar). `VALID_WITH_CUSTOMER_ACTION` triggers a hurdle in the payment flow
(e.g., `sender_idv_electronic_hurdle` for IDV, `response_to_senders_sponsorship_request_hurdle` for sponsorship).

## Limits Exceeded Values

The `LIMITS_EXCEEDED` array contains the specific limits that were exceeded. Empty (`[]`) when `VALIDATION_RESULT = 'VALID'`.

### When BLOCKED

| Limit | Description | Frequency |
|-------|-------------|-----------|
| `CUSTOMER_MONTHLY_SENDING_P2P` | Monthly P2P sending limit | Most common |
| `CUSTOMER_WEEKLY_SENDING_P2P` | Weekly P2P sending limit | |
| `INSTRUMENT_MONTHLY_SENDING_P2P` | Monthly sending limit on the specific instrument | |
| `CUSTOMER_MONTHLY_RECEIVING` | Monthly receiving limit | |
| `CUSTOMER_LIFETIME_SENDING_P2P` | Lifetime P2P sending limit (unverified customers) | |
| `CUSTOMER_OUTSTANDING_BILLS` | Outstanding bills limit | |
| `INSTRUMENT_WEEKLY_SENDING_P2P` | Weekly sending limit on the specific instrument | |
| `CUSTOMER_WEEKLY_CASH_IN` | Weekly cash-in limit | |
| `INSTRUMENT_WEEKLY_CASH_IN` | Weekly cash-in limit on instrument | |
| `CUSTOMER_MONTHLY_CASH_IN` | Monthly cash-in limit | |
| `MIN_TRANSACTION_AMOUNT` | Below minimum transaction amount | |
| `INSTRUMENT_MONTHLY_CASH_IN` | Monthly cash-in limit on instrument | |
| `CUSTOMER_LIFETIME_RECEIVING` | Lifetime receiving limit | |
| `CUSTOMER_BALANCE` | Balance limit exceeded | |
| `CUSTOMER_ACTIVE_LINKED_ACCOUNTS_COUNT` | Too many linked accounts | |
| `CUSTOMER_RECEIVE_COUNT` | Receiving count limit | |

### When VALID_WITH_CUSTOMER_ACTION

Same limit names appear, but the customer can take an action (IDV, sponsorship) to raise their limits. Most common:
`CUSTOMER_UNVERIFIED_ACTIVE_LINKED_ACCOUNTS_COUNT`, `CUSTOMER_LIFETIME_SENDING_P2P`,
`CUSTOMER_LIFETIME_LINKED_ACCOUNTS_COUNT`, `CUSTOMER_MONTHLY_SENDING_P2P`.

### Classifying blocks by monthly vs non-monthly

```sql
CASE
  WHEN (
    ARRAY_CONTAINS('CUSTOMER_MONTHLY_RECEIVING'::VARIANT, limits_exceeded)
    OR ARRAY_CONTAINS('CUSTOMER_MONTHLY_SENDING_P2P'::VARIANT, limits_exceeded)
    OR ARRAY_CONTAINS('INSTRUMENT_MONTHLY_SENDING_P2P'::VARIANT, limits_exceeded)
  ) THEN 'MONTHLY'
  ELSE 'NON_MONTHLY'
END AS block_reason_type
```

## Querying Usages

The `USAGES` array contains the customer's current and projected limit usage across all categories and time windows.
Each element is an object with:

- `category` — usage category (e.g., `SENDING_P2P`, `RECEIVING`, `SENDING_AND_RECEIVING`, `BANK_TRANSFER`,
  `CASH_IN`, `DEBIT_CASH_IN`, `PREFUND_BANK_TRANSFER`, `POTENTIAL_BALANCE`, `RECEIVING_COUNT`, `PAPER_MONEY_DEPOSIT`)
- `duration_in_days` — time window: `1` (daily), `7` (weekly), `30` (monthly), `-1` (lifetime)
- `current_usage_in_cents` — usage before this transaction
- `projected_usage_in_cents` — usage if this transaction is approved
- `amount_in_cents` — same as `projected_usage_in_cents`
- `is_customer` — `true` for customer-level usage, `false` for instrument-level usage
- `token` — customer or instrument token
- `updated_at` — epoch ms when usage was last updated

### Example: find projected monthly P2P sending usage for blocked payments

```sql
SELECT
  customer_token,
  SPLIT_PART(payment_token, ':', 1) AS payment_id,
  u.value:current_usage_in_cents::NUMBER AS current_monthly_sending,
  u.value:projected_usage_in_cents::NUMBER AS projected_monthly_sending
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE,
  LATERAL FLATTEN(INPUT => usages) u
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
  AND validation_result = 'BLOCKED'
  AND u.value:category = 'SENDING_P2P'
  AND u.value:duration_in_days = 30
  AND u.value:is_customer = true
LIMIT 10
```

## Querying Limit Configuration

The `LIMIT_CONFIGURATION` array contains the customer's full limit schedule at decision time. Each element has:

- `limit_category` — the category (e.g., `SENDING_P2P`, `RECEIVING`, `CASH_IN`, `MAX_AMOUNT`, `MIN_AMOUNT`)
- `duration_in_days` — time window: `0` (per-transaction), `1`, `7`, `30`, `-1` (lifetime)
- `amount` — the limit amount in cents (null when unlimited)
- `type` — `FINITE`, `UNLIMITED`, or `MIN_THRESHOLD`
- `source` — (if present) `SYSTEM` for default limits, `SPONSOR` for sponsor-customized limits

### Example: find the weekly P2P sending limit for a customer

```sql
SELECT
  customer_token,
  lc.value:amount::NUMBER / 100.0 AS weekly_p2p_sending_limit_dollars
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE,
  LATERAL FLATTEN(INPUT => limit_configuration) lc
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
  AND lc.value:limit_category = 'SENDING_P2P'
  AND lc.value:duration_in_days = 7
  AND lc.value:type = 'FINITE'
LIMIT 10
```

## Customer Verification Status

The combination of `LIMIT_CALCULATION_METHOD`, `TIER`, `SPONSORSHIP_STATUS`, `IDV_STATUS`, and `STATUS_LEVEL` tells
you about the customer's verification status and which limits apply:

```sql
CASE
  WHEN sponsorship_status = 'SPONSORED' THEN 'SPONSORED'
  WHEN limit_calculation_method = 'STATUS_LIMITS' THEN status_level
  WHEN limit_calculation_method = 'TIERED_LIMITS' AND tier = 'TIER_1' THEN 'NOT_VERIFIED'
  WHEN limit_calculation_method = 'TIERED_LIMITS' AND tier IN ('TIER_2', 'TIER_3', 'TIER_3_PLUS', 'TIER_4') THEN 'VERIFIED'
  WHEN idv_status = 'VERIFIED' THEN 'VERIFIED'
  WHEN idv_status = 'NOT_VERIFIED' THEN 'NOT_VERIFIED'
  ELSE 'UNKNOWN'
END AS account_type
```

## Common Query Patterns

### Deduplicating multiple limit checks per payment

A single payment can have multiple limit check events (e.g., when the customer changes funding instrument). Use
`QUALIFY ROW_NUMBER()` to get the last decision per payment+customer:

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY SPLIT_PART(payment_token, ':', 1), customer_token
  ORDER BY event_occurred_at DESC
) = 1
```

### Counting blocked P2P payments

```sql
SELECT COUNT(DISTINCT SPLIT_PART(payment_token, ':', 1)) AS blocked_payments
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
  AND validation_result = 'BLOCKED'
```

### Finding which limits cause blocks (using LATERAL FLATTEN)

```sql
SELECT f.value::STRING AS limit_exceeded, COUNT(*) AS c
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE,
  LATERAL FLATTEN(INPUT => limits_exceeded) f
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
  AND validation_result = 'BLOCKED'
GROUP BY limit_exceeded
ORDER BY c DESC
```

### Counting sponsored blocks by daily/monthly classification

```sql
WITH sponsored_blocks AS (
  SELECT
    DATE(event_occurred_at) AS event_date,
    payment_token,
    limits_exceeded
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    AND payment_token LIKE 'P2PE_%'
    AND validation_result = 'BLOCKED'
    AND sponsorship_status = 'SPONSORED'
),
classified_blocks AS (
  SELECT
    event_date,
    payment_token,
    CASE
      WHEN (
        ARRAY_CONTAINS('CUSTOMER_MONTHLY_RECEIVING'::VARIANT, limits_exceeded)
        OR ARRAY_CONTAINS('CUSTOMER_MONTHLY_SENDING_P2P'::VARIANT, limits_exceeded)
        OR ARRAY_CONTAINS('INSTRUMENT_MONTHLY_SENDING_P2P'::VARIANT, limits_exceeded)
      ) THEN 'MONTHLY'
      ELSE 'NON_MONTHLY'
    END AS block_reason_type
  FROM sponsored_blocks
)
SELECT
  event_date,
  block_reason_type,
  COUNT(DISTINCT payment_token) AS blocked_payment_count
FROM classified_blocks
GROUP BY event_date, block_reason_type
ORDER BY event_date DESC, block_reason_type
```

### Finding payments that required IDV and sponsorship actions

```sql
SELECT
  customer_token,
  SPLIT_PART(payment_token, ':', 1) AS payment_id
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_token LIKE 'P2PE_%'
  AND validation_result = 'VALID_WITH_CUSTOMER_ACTION'
  AND ARRAY_CONTAINS('IDV'::VARIANT, customer_actions)
  AND ARRAY_CONTAINS('SPONSORSHIP'::VARIANT, customer_actions)
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY SPLIT_PART(payment_token, ':', 1), customer_token
  ORDER BY event_occurred_at DESC
) = 1
```

### Joining limit decisions to payment outcomes

Join on the payment ID extracted via `SPLIT_PART`. **Always mirror the date filter on both tables** to leverage
clustering:

```sql
WITH blocked_payments AS (
  SELECT DISTINCT SPLIT_PART(payment_token, ':', 1) AS payment_id
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    AND payment_token LIKE 'P2PE_%'
    AND validation_result = 'BLOCKED'
)
SELECT le.payment_state_code, COUNT(*) AS c
FROM blocked_payments bp
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE le
  ON le.payment_id = bp.payment_id
WHERE le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY le.payment_state_code
ORDER BY c DESC
```

### Joining limit decisions to payment events (checking hurdles)

When limits require customer action, the p2p-engine presents hurdles. Join limit decisions to payment events to see
which hurdle was shown and how the customer resolved it:

```sql
WITH payments_with_limit_actions AS (
  SELECT
    customer_token,
    SPLIT_PART(payment_token, ':', 1) AS payment_id
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    AND payment_token LIKE 'P2PE_%'
    AND validation_result = 'VALID_WITH_CUSTOMER_ACTION'
    AND ARRAY_CONTAINS('IDV'::VARIANT, customer_actions)
    AND ARRAY_CONTAINS('SPONSORSHIP'::VARIANT, customer_actions)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY SPLIT_PART(payment_token, ':', 1), customer_token
    ORDER BY event_occurred_at DESC
  ) = 1
)
SELECT pses.payment_id, pses.payment_state_code
FROM payments_with_limit_actions pwla
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE pses
  ON pses.payment_id = pwla.payment_id
WHERE pses.created_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND ARRAY_SIZE(pses.hurdles) > 0
  AND (
    (pwla.customer_token = pses.sender_token
     AND NOT IS_NULL_VALUE(pses.hurdles[0]:response_to_senders_sponsorship_request_hurdle))
    OR
    (pwla.customer_token = pses.recipient_customer_token
     AND NOT IS_NULL_VALUE(pses.hurdles[0]:response_to_recipients_sponsorship_request_hurdle))
  )
QUALIFY ROW_NUMBER() OVER (PARTITION BY pses.payment_id ORDER BY pses.sequence DESC) = 1
```

### Looking up a specific payment's limit decisions

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE event_occurred_at >= '2026-02-01'
  AND event_occurred_at < '2026-02-02'
  AND payment_token LIKE 'P2PE_FIAT_<id>%'
```

Use `LIKE 'P2PE_FIAT_<id>%'` (with `%` wildcard) to match both the bare payment token and any suffixed variants.
