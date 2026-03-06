# Query Cash Ins Latest Event

Query and analyze cash-in transfer data from Snowflake.

## Table

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

One row per cash-in transfer reflecting its latest/current state. A "cash-in" is any flow that pulls money from an
external source (debit card, credit card, bank account, Apple Pay, Google Pay) into a customer's Brand B balance. This
includes manual add-cash, the funding leg of P2P payments, loan payments, crypto/stock purchases, and savings
transfers.

~7.2 billion rows, ~2.1 TB. Extremely large -- always use tight date filters.

**ETL:** Runs twice daily from `CASH_DATA_BOT.PUBLIC.CASH_INS_SNOWFLAKE` (raw events). Joins instrument data from
other sources to enrich the rows. Expect up to ~12 hours of delay.

**Clustering key:** `LINEAR(DATE(EVENT_UPDATED_AT), DATE(EVENT_LOAD_TIMESTAMP))`. Always filter on `EVENT_UPDATED_AT`
to leverage clustering and avoid full table scans. Default to
`WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())` unless the user specifies a different range.

**Important:** This table tracks the pull side of money movement only. For P2P payments, it represents the sender's
card/bank charge. A single P2P payment can have **multiple cash-in rows** when the first capture attempt fails (e.g.,
insufficient funds) and the customer retries with a different funding instrument. The first attempt's `EXTERNAL_ID`
equals the payment ID directly (e.g., `P2PE_FIAT_...`), but retry attempts get a `_capture_N` suffix (e.g.,
`P2PE_FIAT_..._capture_2`). Use `EXTERNAL_REFERENCE_ID` (not `EXTERNAL_ID`) to join to
`P2PENGINE_PAYMENT_STATE_LATEST_EVENT`, as it always contains the clean payment ID for real transfers.

**Always filter out `PREEMPTIVELY_CANCELED`** cash-ins when analyzing P2P payments. These are placeholder transfers
created in an already-cancelled state to reserve an idempotency key — they do not represent real money movement. They
account for a large share of P2P cash-in rows but carry no meaningful data (null instrument, rail, etc.).

**Source code:** Proto definitions live in `moneta/client-protos/src/main/proto/example/app/moneta/`. The Snowflake
event schema is defined in `events/CashInSnowflakeEvent.proto`. The internal event with typed enums is in
`events/CashInEvent.proto`. Core enums (TransferEntityState, FundingReason, FailureReason, CaptureReason,
ProcessingMode, TransferRail) are in `core/models.proto` and `core/model/transfer_rail.proto`.

**Related Snowflake tables:**
- `CASH_DATA_BOT.PUBLIC.CASH_INS_SNOWFLAKE` -- raw event data, essentially real-time, very expensive to query
- `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` -- one row per event (multiple per transfer), ETL runs twice daily
- `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` -- aggregation layer between this table and TRANSFER_SUMMARY
- `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` -- combined cash-in and cash-out data (all products, not just Moneta)

## Column Reference

- **Nullable**: Y = null values common, R = rare nulls, N = always populated
- **FK**: indicates column joins to another table

| # | Field | Type | Nullable | FK | Description | Example / Enum Values |
|---|-------|------|----------|----|-------------|----------------------|
| 1 | EVENTLY_ID | TEXT | N | | Unique event identifier. Format: `{TRANSFER_TOKEN}_{version}_{event_version}_{STATE}` | `MCI_2se6usrvnz6wxawjgs3d42tm5_13_1_COMPLETED` |
| 2 | EVENTLY_PARTITION_KEY | TEXT | N | | Partition key, same as OWNER_TOKEN | `C_fse3pgycg` |
| 3 | EVENT_ID | TEXT | N | | Same as EVENTLY_ID | |
| 4 | ENTITY_VERSION | TEXT | N | | Incremented for each state change the transfer entity undergoes | `13` |
| 5 | EVENT_VERSION | TEXT | N | | Incremented only if the same event needs re-processing (bug fix or schema change) | `1` |
| 6 | TRANSFER_TOKEN | TEXT | N | `MONEY_MOVER_TRANSACTIONS` (as `FLOW_TOKEN` when `FLOW_NAME = 'MONETA_CASH_IN_TRANSFER'`) | Unique transfer identifier. Always prefixed `MCI_`. | `MCI_2se6usrvnz6wxawjgs3d42tm5` |
| 7 | OWNER_TOKEN | TEXT | N | | Customer token of the account owner | `C_fse3pgycg` |
| 8 | CUSTOMER_ID | NUMBER | N | | Internal numeric customer ID | `32497008108` |
| 9 | CUSTOMER_CREATED_AT | TIMESTAMP | N | | When the customer account was created | `2025-11-13T09:59:37` |
| 10 | TRANSFER_TYPE | TEXT | Y | | **Deprecated** in favor of TRANSFER_RAIL. Always null in recent data. | |
| 11 | **TRANSFER_RAIL** | TEXT | N | | **Important.** Rail used for the transfer | **Enum:** `DEBIT` (94%), `None` (3.6%, preemptively canceled), `ACH` (1.7%), `CREDIT` (0.4%), `APPLE_PAY`, `GOOGLE_PAY` |
| 12 | PROCESSING_MODE | TEXT | N | | Whether funds are available in the target instrument immediately or after some time | **Enum:** `SYNCHRONOUS` (97%), `None` (3.5%, preemptively canceled), `ASYNCHRONOUS` (rare) |
| 13 | **STATE** | TEXT | N | | **Important.** Current/final transfer state. Maps to `TransferEntityState` proto enum. Terminal states: `COMPLETED`, `FAILED`, `CHARGED_BACK` (charged back and clawed back), `REVERSED`, `CLAWBACK_REIMBURSED` (chargeback reversed, clawback reimbursed). | **Enum (by frequency):** `COMPLETED` (78%), `FAILED` (22%), `WAITING_ON_MONEY_TRANSFER_TO_SETTLE`, `CHARGED_BACK`, `REVERSED`, `WAITING_ON_MONEY_TRANSFER_TO_PROCESS`, `AUTHORIZED_WAITING_CALLER_ACTION`, `WAITING_ON_MONEY_TRANSFER_AUTHORIZATION`, `WAITING_ON_INSTRUMENT_ACCESS_VERIFICATION`, `WAITING_ON_MONEY_TRANSFER_CAPTURE`, `WAITING_ON_RISK`, `CLAWBACK_REIMBURSED`, `WAITING_ON_ELIGIBILITY`, `PARTIALLY_AUTHORIZED_WAITING_CALLER_ACTION`, `WAITING_ON_LIMITS`, `INITIATING`, `WAITING_ON_INSTRUMENT_SELECTION`, `WAITING_ON_TRANSFER_RAIL_DECISION` |
| 14 | **AMOUNT** | NUMBER | N | | Transfer amount in cents | `8000` ($80), `1500` ($15) |
| 15 | CURRENCY | TEXT | N | | Currency code | `USD` |
| 16 | LAST_KNOWN_BALANCE_AMOUNT | NUMBER | Y | | Customer's balance in cents after this transfer | `8000` |
| 17 | LAST_KNOWN_BALANCE_CURRENCY | TEXT | Y | | Balance currency | `USD` |
| 18 | LAST_KNOWN_BALANCE_VERSION | NUMBER | Y | | Balance ledger version | `90` |
| 19 | CAPTURE_REASON | TEXT | Y | | How the capture was triggered. `IMMEDIATE_AUTO`: captured automatically right after auth approval. `DELAYED_MANUAL`: captured at the caller's (e.g., P2P engine's) request. `DELAYED_AUTO`: captured automatically before auth expiration per expiringAuthPolicy. | **Enum:** `IMMEDIATE_AUTO` (43%), `DELAYED_MANUAL` (33%), `None` (24%, failed before capture), `DELAYED_AUTO` (rare) |
| 20 | CREDIT_CARD_FEE_AMOUNT | NUMBER | Y | | Credit card fee in cents (only for CREDIT rail) | |
| 21 | CREDIT_CARD_FEE_CURRENCY | TEXT | Y | | Credit card fee currency | `USD` |
| 22 | OON_FEE_AMOUNT | NUMBER | Y | | Out-of-network fee in cents (rare) | |
| 23 | OON_FEE_CURRENCY | TEXT | Y | | Out-of-network fee currency | |
| 24 | INITIAL_AMOUNT | NUMBER | Y | | Requested amount before partial auth. Always null in recent data. | |
| 25 | PARTIAL_AMOUNT_ALLOWED | NUMBER | Y | | Whether partial authorization allowed. Always null in recent data. | |
| 26 | FINAL_AMOUNT | NUMBER | Y | | Final amount after partial auth. Always null in recent data. | |
| 27 | SOURCE_INSTRUMENT_LINK_ID | NUMBER | Y | | Internal instrument link ID | `3330193707` |
| 28 | SOURCE_INSTRUMENT_TOKEN | TEXT | Y | | Token of the source instrument (card/bank account) | `b1d768dfbc05baa293dd100f4497d42d38edd6db` |
| 29 | **SOURCE_INSTRUMENT_TYPE** | TEXT | Y | | **Important.** Type of external instrument | **Enum:** `DEBIT_CARD` (94%), `None` (3.9%, failed early), `BANK_ACCOUNT` (1.7%), `CREDIT_CARD` (0.4%) |
| 30 | SOURCE_INSTRUMENT_FIDELIUS_TOKEN | TEXT | Y | | Tokenized instrument reference | `fid-1-156864c4a2d9638a...` |
| 31 | SOURCE_INSTRUMENT_LINKED_AT | TIMESTAMP | Y | | When the instrument was linked to the account | |
| 32 | SOURCE_INSTRUMENT_BIN | TEXT | Y | | Card BIN (first 6 digits) | `456331` |
| 33 | SOURCE_INSTRUMENT_ZIP | TEXT | Y | | Billing ZIP code | `07631` |
| 34 | SOURCE_INSTRUMENT_PAR | TEXT | Y | | Payment Account Reference. Used as the identifier for digital wallet instrument types (Apple Pay, Google Pay) instead of SOURCE_INSTRUMENT_TOKEN, which may be a placeholder. | |
| 35 | TARGET_INSTRUMENT_LINK_ID | NUMBER | Y | | Target instrument link ID (null for P2P) | |
| 36 | TARGET_INSTRUMENT_TOKEN | TEXT | Y | | Target instrument token. For P2P: `B$_P2P_{customer_token}`. For manual cash-in: `B$_{customer_token}`. | `B$_P2P_C_fse3pgycg`, `B$_C_abc123` |
| 37 | TARGET_INSTRUMENT_TYPE | TEXT | Y | | Target instrument type. Null when failed or for P2P. | **Enum:** `CASH_BALANCE`, `SAVINGS` |
| 38 | TARGET_INSTRUMENT_FIDELIUS_TOKEN | TEXT | Y | | Target fidelius token (always null) | |
| 39 | TARGET_INSTRUMENT_LINKED_AT | TIMESTAMP | Y | | Target instrument linked at (always null) | |
| 40 | TARGET_INSTRUMENT_BIN | TEXT | Y | | Target instrument BIN (always null) | |
| 41 | TARGET_INSTRUMENT_ZIP | TEXT | Y | | Target instrument ZIP (always null) | |
| 42 | **FUNDING_REASON** | TEXT | N | | **Important.** Why the cash-in was initiated | **Enum (by frequency):** `MANUAL_CASH_IN` (45%), `P2P_PAYMENT` (39%), `LOAN_PAYMENT` (10%), `MANUAL_LOAN_PAYMENT` (4%), `CRYPTO_PURCHASE`, `MANUAL_SAVINGS_CASH_IN`, `STOCK_PURCHASE`, `AUTO_CASH_IN`, `MANUAL_OVERDRAFT_PAYMENT`, `AUTO_CRYPTO_PURCHASE`, `AUTO_STOCK_PURCHASE`, `BALANCE_BASED_ADD_CASH`, `POOL_OWNER_CONTRIBUTION`, `P2P_POOL_CONTRIBUTION`, `CRYPTO_PURCHASE_CUSTOM`, `P2P_OON_POOL_CONTRIBUTION`, `REMITTANCE`, `AUTO_SAVINGS_TRANSFER` |
| 43 | IS_SAVINGS | BOOLEAN | N | | Whether this funds a savings account | `true`, `false` |
| 44 | **EXTERNAL_ID** | TEXT | N | | External reference. For P2P first attempt: the payment ID (e.g., `P2PE_FIAT_...`). For P2P retry attempts: payment ID with `_capture_N` suffix. For manual cash-in: a UUID. **Do not use for joins to payment state tables; use `EXTERNAL_REFERENCE_ID` instead.** | `P2PE_FIAT_2D761F027A8E4D2A8CD9CACB43C365E8`, `P2PE_FIAT_..._capture_2`, `79048C7FA8E941168985267BBC56ACAC` |
| 45 | **FAILURE_REASON** | TEXT | Y | | Reason the transfer failed (null when successful) | **Top 10:** `INSUFFICIENT_FUNDS` (53%), `TRANSFER_DECLINED` (23%), `PREEMPTIVELY_CANCELED` (16%), `RISK_DECLINED`, `TRANSACTION_NOT_PERMITTED`, `RATE_LIMITED`, `INVALID_INSTRUMENT`, `TRANSACTION_AMOUNT_BELOW_MINIMUM`, `CANCELED_BY_CALLER`, `CUSTOMER_DECLINED_PARTIAL_AUTHORIZATION` |
| 46 | CASH_CLIENT_SCENARIO | TEXT | Y | | Client scenario identifier | **Enum:** `TRANSFER_FUNDS` (manual cash-in), `PLASMA`, `EXCHANGE_EQUITY`, `INITIATE_BITCOIN_WITHDRAWAL`, `INITIATE_TAX_UPGRADE` |
| 47 | CASH_FLOW_TOKEN | TEXT | Y | | Parent Plasma token that may encompass multiple cash-in transfer attempts (e.g., a failed debit followed by an ACH retry). Individual attempts get their own execution flow token, but share this parent token. | `4VovO9xjpYtdLf96Ia9r6mMBQ` |
| 48 | CLIENT_IP | TEXT | Y | | Client IP address (~54% null) | |
| 49 | DEVICE_ID | TEXT | Y | | Device identifier (~87% null) | |
| 50 | TIMEZONE | TEXT | Y | | Client timezone | |
| 51 | USER_AGENT | TEXT | Y | | Client user agent string | `Mozilla/5.0 (V54AP; CPU iPhone OS 26.2.1...)` |
| 52 | PLATFORM | TEXT | N | | Client platform | **Enum:** `iOS` (59%), `Android` (23%), `UNKNOWN` (18%), `Web` (<0.1%) |
| 53 | APP_VERSION | TEXT | Y | | App version string | `5.36.0` |
| 54 | MAJOR_VERSION | TEXT | Y | | Major version number | `5` |
| 55 | MINOR_VERSION | TEXT | Y | | Minor version number | `36` |
| 56 | INSTALLER_PACKAGE | TEXT | Y | | Installer package (rare) | |
| 57 | DRM_ID | TEXT | Y | | DRM identifier (rare) | |
| 58 | TRACKING_COOKIE | TEXT | Y | | Tracking cookie (rare) | |
| 59 | ACCEPT_LANGUAGE | TEXT | Y | | Accept-Language header (rare) | |
| 60 | BROWSER_FINGERPRINT | TEXT | Y | | Browser fingerprint (rare) | |
| 61 | NETWORK_OPERATOR | TEXT | Y | | Mobile network operator (rare) | |
| 62 | SIM_INFO | TEXT | Y | | SIM card info (rare) | |
| 63 | RETRY_CREATED_AT | TIMESTAMP | Y | | When the retry attempt was created (~99.9% null) | |
| 64 | RETRY_ATTEMPT | TEXT | Y | | Retry attempt number (~99.9% null) | |
| 65 | RETRY_IS_FOREGROUND | TEXT | Y | | Whether the retry was in foreground (~99.9% null) | |
| 66 | EVENT_RECEIVED_AT | TIMESTAMP | N | | When the event was received by the pipeline | `2026-02-07T00:46:37.711` |
| 67 | EVENT_OCCURRED_AT | TIMESTAMP | N | | When the event actually occurred | `2026-02-07T00:46:37.517` |
| 68 | EVENT_CREATED_AT | TIMESTAMP | N | | When the transfer was created | `2026-02-07T00:46:34.530` |
| 69 | **EVENT_UPDATED_AT** | TIMESTAMP | N | | When the transfer was last updated. **Clustering key -- always filter on this.** | `2026-02-07T00:46:37.517` |
| 70 | EVENT_LOAD_TIMESTAMP | TIMESTAMP | N | | When the event was loaded into Snowflake (also clustering key) | `2026-02-07T00:46:37.711` |
| 71 | TRANSFER_CHARGED_BACK_AT | TIMESTAMP | Y | | When the transfer was charged back. Mostly manual cash-in, loan payments. Never P2P. | |
| 72 | TRANSFER_REVERSED_AT | TIMESTAMP | Y | | When the transfer was reversed. Mostly P2P payments (refunds/clawbacks). | |
| 73 | TRANSFER_COMPLETED_AT | TIMESTAMP | Y | | When the transfer completed (null if not completed) | `2026-02-07T00:46:37.517` |
| 74 | TRANSFER_FAILED_AT | TIMESTAMP | Y | | When the transfer failed (null if not failed) | |
| 75 | ETL_CREATED_AT | TIMESTAMP | N | | When the row was first loaded by ETL | |
| 76 | ETL_UPDATED_AT | TIMESTAMP | N | | When the row was last updated by ETL | |
| 77 | ETL_HASH_PER_ROW | NUMBER | N | | Hash for ETL deduplication | |
| 78 | ORIGINATING_CALLING_PRINCIPLE | TEXT | Y | | Service that called Moneta to initiate the cash-in. Maps to `ClientService` proto enum. Null for P2P payments (P2P_ENGINE calls Moneta but this field isn't populated for that path). | **Enum:** `CASH_PROXY` (manual cash-in), `CRYPTO_INVEST_FLOW`, `INVEST_FLOW`, `PIGGYBANK`. Proto also defines: `BBAC`, `BTC_MOONGATE`, `FRANKLIN`, `LOANSTAR`, `P2P_ENGINE`, `REPEATEDLY`, `SHADOW`, `TOOLBOX`. |
| 79 | CUSTOMER_REGION | TEXT | R | | Customer's region (~3.5% null for preemptively canceled) | `USA` |
| 80 | PILLOW_TOKEN | TEXT | Y | | Browser interaction / fraud detection token (~36% null) | `urn:bi-token:v1:b24d9b418d32dec3...` |
| 81 | DEVICE_ADVERTISING_ID | TEXT | Y | | Advertising ID (rare) | |
| 82 | DEVICE_INSTALLATION_ID | TEXT | Y | | Installation ID (rare) | |
| 83 | DEVICE_VENDOR_ID | TEXT | Y | | Vendor ID (rare) | |
| 84 | SQUARE_DEVICE_ID | TEXT | Y | | Brand A device ID (rare) | |
| 85 | **EXTERNAL_REFERENCE_ID** | TEXT | N | `P2PENGINE_PAYMENT_STATE_LATEST_EVENT` (as `PAYMENT_ID` when `FUNDING_REASON = 'P2P_PAYMENT'`) | **Important.** The clean payment ID for P2P cash-ins, without the `_capture_N` suffix that `EXTERNAL_ID` may have. **Use this column (not `EXTERNAL_ID`) for joins to payment state tables.** For `PREEMPTIVELY_CANCELED` rows this falls back to `TRANSFER_TOKEN`, but those rows should always be filtered out. For non-P2P flows: same as `TRANSFER_TOKEN`. | `P2PE_FIAT_2D761F027A8E4D2A8CD9CACB43C365E8`, `MCI_90zf0k2790ewu0c6l7czetu8h` |

## Failure Reason Categories

The `FAILURE_REASON` column maps to the `FailureReason` proto enum in `core/models.proto`. The values fall into
these categories:

**Money transfer failures** (card/bank declines): `INSUFFICIENT_FUNDS`, `TRANSFER_DECLINED`, `INVALID_INSTRUMENT`,
`INSTRUMENT_EXPIRED`, `TRANSACTION_NOT_PERMITTED`, `RESTRICTED_CARD`, `CARD_TERMINATED`, `INVALID_USE_OF_CASH_CARD`,
`MONEY_TRANSFER_SUSPECTED_FRAUD`, `DO_NOT_HONOR`, `ACCOUNT_FROZEN`, `FAILED_TO_REACH_ISSUER`, `PICK_UP_CARD`,
`CARD_LOST_OR_STOLEN`, `UNSUPPORTED_INSTRUMENT`, `INVALID_CVV_OR_EXPIRATION_DATE`, `REVOCATION_OF_AUTH`,
`INVALID_AMOUNT`, `REENTER_TRANSACTION`, `BALANCE_REQUIRED`

**Limits failures**: `CUSTOMER_WEEKLY_SENDING_LIMIT_EXCEEDED`, `TRANSACTION_AMOUNT_BELOW_MINIMUM`,
`TRANSACTION_AMOUNT_EXCEEDS_MAXIMUM`, `CUSTOMER_MONTHLY_SENDING_LIMIT_EXCEEDED`, and many other
`CUSTOMER_*_EXCEEDED` / `INSTRUMENT_*_EXCEEDED` variants

**Risk failures**: `RISK_DECLINED`, `GENERAL_RISK_ERROR`, `RISK_EVALUATION_TIMEOUT`, `ACCOUNT_NAME_MISMATCH`,
`ACCOUNT_WOULD_NSF` (bank has less money than needed), `ACCOUNT_NAME_MISMATCH_AND_WOULD_NSF`

**Cancellation reasons**: `PREEMPTIVELY_CANCELED` (placeholder transfer created in an already-cancelled state to
reserve an idempotency key — **not a real transfer**, always filter these out for P2P analysis),
`CANCELED_BY_CALLER`, `MANUAL_CANCELLATION`, `AUTOMATICALLY_CANCELED`,
`CUSTOMER_DECLINED_PARTIAL_AUTHORIZATION`

**Instrument access verification failures**: `INSTRUMENT_ACCESS_VERIFICATION_DECLINED_BY_CUSTOMER`,
`INSTRUMENT_ACCESS_VERIFICATION_TIME_LIMIT_EXCEEDED`, `INSTRUMENT_ACCESS_VERIFICATION_CUSTOMER_INELIGIBLE`,
`INSTRUMENT_ACCESS_VERIFICATION_FAILED`, `INSTRUMENT_ACCESS_VERIFICATION_AUTH_DECLINED`,
`INSTRUMENT_ACCESS_VERIFICATION_INSUFFICIENT_FUNDS`

**Plaid/bank linking failures**: `PLAID_INVALID_ACCESS_TOKEN`, `PLAID_ITEM_LOGIN_REQUIRED`,
`PLAID_INVALID_ACCOUNT_ID`, `PLAID_NO_ACCOUNTS`, `PLAID_ITEM_NOT_FOUND`, `PLAID_INSUFFICIENT_CREDENTIALS`,
`PLAID_ITEM_NOT_SUPPORTED`, `PRESELECTED_BANK_ACCOUNT_NOT_ACTIVE_PLAID_LINK`

**Other**: `RATE_LIMITED`, `ELIGIBILITY_CHECK_FAILED`, `EXPIRED_WAITING_ON_IDV`, `ASYNC_CASH_IN_BLOCKED`,
`MISSING_FAILURE_REASON`, `ONCALL_MANUAL_FAILURE`, `AUTOMATIC_FAILURE`, `EXPIRED_PENDING_CALLER_ACTION`

## Relationship to P2P Payment Tables

For P2P payments (`FUNDING_REASON = 'P2P_PAYMENT'`), each cash-in represents the pull (sender's card charge) for a
payment. A single payment can produce **multiple cash-in rows**: if the first capture attempt fails (e.g.,
`INSUFFICIENT_FUNDS` or `TRANSFER_DECLINED`), the customer may update their funding instrument and retry. The first
attempt's `EXTERNAL_ID` equals the payment ID directly, but subsequent attempts get a `_capture_N` suffix
(e.g., `_capture_2`, `_capture_3`). This suffix is generated by `TransferIdempotenceKeyGenerator` in p2p-engine.

**Join on `EXTERNAL_REFERENCE_ID`** (not `EXTERNAL_ID`), and **always filter out `PREEMPTIVELY_CANCELED`**:

```sql
SELECT ci.*, le.PAYMENT_STATE_CODE, le.FAILURE_REASON_CODE
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE ci
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE le
  ON ci.EXTERNAL_REFERENCE_ID = le.PAYMENT_ID
WHERE ci.EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND ci.FUNDING_REASON = 'P2P_PAYMENT'
  AND ci.FAILURE_REASON IS DISTINCT FROM 'PREEMPTIVELY_CANCELED'
```

**Why not `EXTERNAL_ID`?** Retry attempts have a `_capture_N` suffix on `EXTERNAL_ID` that won't match
`PAYMENT_ID`. `EXTERNAL_REFERENCE_ID` always contains the clean payment ID for real transfers.

**Why filter `PREEMPTIVELY_CANCELED`?** These are placeholder rows pushed to Snowflake for debugging — they don't
represent real transfers. Their `EXTERNAL_REFERENCE_ID` falls back to `TRANSFER_TOKEN` (an `MCI_` value) instead
of the payment ID, so they would fail the join anyway.

The `PULL_TRANSFER_ID` column in `P2PENGINE_PAYMENT_STATE_LATEST_EVENT` does NOT reliably join to `TRANSFER_TOKEN`
here.

## Relationship to MONEY_MOVER_TRANSACTIONS

The `TRANSFER_TOKEN` (e.g., `MCI_...`) maps to `FLOW_TOKEN` in `MONEY_MOVER_TRANSACTIONS` where
`FLOW_NAME = 'MONETA_CASH_IN_TRANSFER'`:

```sql
SELECT ci.TRANSFER_TOKEN, mm.TX_STATE, mm.TX_MECHANISM, mm.TX_AMOUNT_CENTS
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE ci
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE mm
  ON ci.TRANSFER_TOKEN = mm.FLOW_TOKEN
WHERE ci.EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND mm.TX_CREATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND mm.FLOW_NAME = 'MONETA_CASH_IN_TRANSFER'
  AND ci.STATE = 'COMPLETED'
LIMIT 10
```

## Common Query Patterns

### Filtering P2P cash-ins only

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND FUNDING_REASON = 'P2P_PAYMENT'
  AND FAILURE_REASON IS DISTINCT FROM 'PREEMPTIVELY_CANCELED'
```

### Cash-in failure rate by instrument type

```sql
SELECT
  SOURCE_INSTRUMENT_TYPE,
  COUNT(*) AS total,
  SUM(CASE WHEN STATE = 'COMPLETED' THEN 1 ELSE 0 END) AS completed,
  SUM(CASE WHEN STATE = 'FAILED' THEN 1 ELSE 0 END) AS failed,
  ROUND(100.0 * SUM(CASE WHEN STATE = 'FAILED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_pct
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND SOURCE_INSTRUMENT_TYPE IS NOT NULL
GROUP BY SOURCE_INSTRUMENT_TYPE
ORDER BY total DESC
```

### Top failure reasons for P2P cash-ins

```sql
SELECT FAILURE_REASON, COUNT(*) AS c
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND FUNDING_REASON = 'P2P_PAYMENT'
  AND STATE = 'FAILED'
  AND FAILURE_REASON != 'PREEMPTIVELY_CANCELED'
GROUP BY FAILURE_REASON
ORDER BY c DESC
LIMIT 20
```

### P2P NSF analysis: join cash-in failure with payment outcome

Find P2P payments where the card charge failed with NSF, and check whether the payment ultimately succeeded (possibly
via retry with a different instrument):

```sql
WITH nsf_cash_ins AS (
  SELECT EXTERNAL_REFERENCE_ID AS payment_id, TRANSFER_TOKEN, SOURCE_INSTRUMENT_TYPE
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
    AND FUNDING_REASON = 'P2P_PAYMENT'
    AND STATE = 'FAILED'
    AND FAILURE_REASON = 'INSUFFICIENT_FUNDS'
)
SELECT
  le.PAYMENT_STATE_CODE,
  le.FAILURE_REASON_CODE,
  COUNT(*) AS c
FROM nsf_cash_ins ci
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE le
  ON ci.payment_id = le.PAYMENT_ID
WHERE le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY le.PAYMENT_STATE_CODE, le.FAILURE_REASON_CODE
ORDER BY c DESC
```

### Cash-in volume by funding reason and rail

```sql
SELECT
  FUNDING_REASON,
  TRANSFER_RAIL,
  COUNT(*) AS total,
  SUM(AMOUNT) / 100.0 AS total_dollars
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND STATE = 'COMPLETED'
GROUP BY FUNDING_REASON, TRANSFER_RAIL
ORDER BY total DESC
```

### Chargebacks and reversals

Chargebacks happen mostly on manual cash-ins. Reversals happen mostly on P2P (when the P2P payment is refunded
or clawed back):

```sql
SELECT FUNDING_REASON, STATE, COUNT(*) AS c
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND (TRANSFER_CHARGED_BACK_AT IS NOT NULL OR TRANSFER_REVERSED_AT IS NOT NULL)
GROUP BY FUNDING_REASON, STATE
ORDER BY c DESC
```

### Cash-in volume by platform

```sql
SELECT
  PLATFORM,
  COUNT(*) AS total,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EVENT_UPDATED_AT >= DATEADD(day, -7, CURRENT_DATE())
  AND STATE = 'COMPLETED'
GROUP BY PLATFORM
ORDER BY total DESC
```

### Looking up a specific P2P payment's cash-in(s)

Returns all capture attempts for a payment, including retries:

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE EXTERNAL_REFERENCE_ID = 'P2PE_FIAT_2D761F027A8E4D2A8CD9CACB43C365E8'
  AND EVENT_UPDATED_AT >= DATEADD(day, -30, CURRENT_DATE())
  AND FUNDING_REASON = 'P2P_PAYMENT'
  AND FAILURE_REASON IS DISTINCT FROM 'PREEMPTIVELY_CANCELED'
ORDER BY EVENT_CREATED_AT
```
