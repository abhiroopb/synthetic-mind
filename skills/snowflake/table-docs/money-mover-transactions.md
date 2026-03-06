# Query Money Mover Transactions

Query and analyze money movement transaction data from Snowflake.

## Table

### APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS

One row per transaction reflecting the latest state. Each "flow" (e.g., a P2P payment) produces multiple transactions:
typically a PULL (debit sender) and a PUSH (credit recipient). A single payment may have additional rows for reversals,
re-captures, or fee adjustments.

**No clustering key.** This table has ~40 billion rows and ~3.7 TB. Always filter on `TX_CREATED_AT` to avoid
prohibitively slow scans. Default to `WHERE TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())` unless the user
specifies a different range.

**Flow ownership:** The table covers all Cash App money movement, not just P2P. Filter with
`FLOW_TOKEN LIKE 'P2PE%'` to isolate P2P Engine transactions, or use `FLOW_OWNER = 'P2P_ENGINE'`.

## Column Reference

- **Nullable**: Y = null values observed in practice, N = always populated
- **FK**: indicates column joins to another table

| # | Field | Type | Nullable | FK | Description | Example / Enum Values |
|---|-------|------|----------|----|-------------|----------------------|
| 1 | FLOW_NAME | TEXT | N | | The money-mover flow that created this transaction. See "Flow Names" section. | `P2P_ENGINE_TRANSFER`, `MONETA_CASH_IN_TRANSFER` |
| 2 | FLOW_TOKEN | TEXT | N | `P2PENGINE_PAYMENT_STATE_LATEST_EVENT` (as `PAYMENT_ID`) | Token identifying the parent flow. For P2P payments, this is the `PAYMENT_ID`. For multiple captures, a `_capture_N` suffix is appended. | `P2PE_FIAT_A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6`, `P2PE_FIAT_A1B2C3D4_capture_2` |
| 3 | FLOW_OWNER | TEXT | N | | System that owns the flow | **Top values:** `P2P_ENGINE` (44%), `MONETA` (30%), `BALANCE_MOVER` (16%), `CASH_OUT`, `INVEST_CRYPTO`, `CROW`, `LYNX`, `FIATLY`, `SALVAGER` |
| 4 | TX_NUMBER | NUMBER | Y* | | Transaction number within the flow. `0` = PULL, `1` = PUSH for standard P2P. Higher numbers appear for multi-capture or multi-leg flows. | `0`, `1`, `2` |
| 5 | LATEST_EVENT_SEQ_NUM | NUMBER | Y* | | Sequence number of the latest event for this transaction | `0`, `1`, `2`, `3` |
| 6 | LATEST_EVENT_EXPORT_VERSION | NUMBER | Y* | | Export version of the latest event | `1`, `2`, `3` |
| 7 | **TX_TYPE** | TEXT | Y* | | **Important.** Direction of the transaction. See `TransactionType.proto`. | **Enum:** `PULL` (pull money from customer's instrument to Square), `PUSH` (push money from Square to customer's instrument), `PULL_REVERSAL` (reversal of pull: pushes money back, usually to a different instrument), `PUSH_REVERSAL` (reversal of push: pulls money back, usually from same instrument as original push) |
| 8 | TX_MECHANISM | TEXT | Y* | | Payment rail used. See `TransactionMechanism.kt` and `MoneyMovingMechanism.proto`. | **Enum:** `BANKLIN_LEDGER` (77% -- ledger-based, for STORED_VALUE), `PANAMA` (21% -- card processing, for CARD/DEBIT_CARD/CREDIT_CARD), `TELLER_ACH` (<1% -- ACH via Teller/Wells Fargo, for BANK_ACCOUNT), `BANKLIN_LEDGER_AUTH` (<1% -- ledger with auth/capture workflow) |
| 9 | **TX_STATE** | TEXT | Y* | | **Important.** Current transaction state. See `TransactionState.proto`. | **Enum:** `SUCCEEDED` (94% -- money settled; **not truly terminal** for ACH/debit/credit -- chargebacks can occur later), `PERMANENTLY_FAILED` (4% -- failed by processing service, e.g. insufficient funds), `SCHEDULED` (planned for future execution), `CANCELED` (canceled in processing service), `RETURNED` (full amount returned to customer), `WAITING_TO_SETTLE` (ACH: sent, awaiting settlement), `WAITING_TO_SEND` (ACH: waiting to be sent, still cancellable), `AUTHED` (card: authorized but not yet captured) |
| 10 | TX_OCTOPUS_RESULT | TEXT | Y | | Result from the payment processor. Null for successful ledger transactions. | **Top values:** `SUCCESS`, `INSUFFICIENT_FUNDS`, `GENERIC_FAILURE`, `TRANSACTION_NOT_PERMITTED`, `INVALID_INSTRUMENT`, `SUSPECTED_FRAUD`, `CARD_TERMINATED`, `DECLINED`, `CARD_LOST_OR_STOLEN`, `DO_NOT_HONOR` |
| 11 | TX_AMOUNT_CENTS | NUMBER | Y* | | Transaction amount in cents | `47000` ($470), `1500` ($15) |
| 12 | TX_AMOUNT_CURRENCY_CODE | TEXT | Y* | | Currency | `USD` |
| 13 | TX_CODING_CATEGORY | TEXT | Y* | | Accounting category for the transaction | **P2P values:** `CASH_PAYMENT`, `CASH_BUSINESS_PAYMENT`. **Other:** `INTERNAL_TRANSFER`, `CASH_IN`, `CASH_OUT`, `DEBT_REPAYMENT_CASH_IN`, `CRYPTO_EXCHANGE` |
| 14 | TX_EXTERNAL_TRANSACTION_ID | TEXT | Y* | | External transaction ID. For `P2P_ENGINE_TRANSFER`/`P2P_ENGINE_INTERNAL_BALANCE_XFER`: `ST$_PE_<hash>-<seq>`. For `MONETA_CASH_IN_TRANSFER` PULL (card): opaque Panama token. For `MONETA_CASH_IN_TRANSFER` PUSH: `ST$_MO_<hash>-<seq>`. | `ST$_PE_abc123def456ghi789-0000`, `ST$_MO_abc123def456ghi789-0002` |
| 15 | TX_INSTRUMENT_OWNER_ID | TEXT | Y* | | Customer token of the instrument owner | `C_abc123xyz` |
| 16 | TX_INSTRUMENT_TOKEN | TEXT | Y* | | Token of the financial instrument used. `B$_` prefix = Cash balance (stored value). | `B$_C_abc123xyz`, `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8c9d0` |
| 17 | TX_INSTRUMENT_TYPE | TEXT | Y* | | Type of instrument | **Enum:** `STORED_VALUE` (77%), `CARD` (21%), `BANK_ACCOUNT` (<1%), `APPLE_PAY` (<1%), `GOOGLE_PAY` (<1%) |
| 18 | TX_MERCHANT_CATEGORY_CODE | NUMBER | Y | | MCC code. Populated only for card transactions via Panama. | |
| 19 | TX_CREATED_AT | TIMESTAMP | Y* | | **Date filter column.** When the transaction was created. Always filter on this. | `2026-02-08T04:08:35.672` |
| 20 | TX_CAPTURED_AT | TIMESTAMP | Y | | When the transaction was captured (card auth → capture). Null for ledger (BANKLIN_LEDGER) transactions. | `2026-02-08T04:08:36.500` |
| 21 | LATEST_EVENT_CREATED_AT | TIMESTAMP | Y* | | When the latest event for this transaction was created | `2026-02-08T04:47:20.185` |
| 22 | LATEST_EVENT_UPDATED_AT | TIMESTAMP | Y* | | When the latest event was last updated | `2026-02-08T04:47:20.259` |
| 23 | LATEST_EVENT_LOAD_TIMESTAMP | TIMESTAMP | Y* | | When the latest event was loaded into the pipeline | `2026-02-08T04:47:21.318` |
| 24 | ETL_UPSTREAM_TS | TIMESTAMP | N | | ETL upstream timestamp | |
| 25 | ETL_CREATED_AT | TIMESTAMP | N | | When the row was first loaded by ETL | |
| 26 | ETL_UPDATED_AT | TIMESTAMP | N | | When the row was last updated by ETL | |
| 27 | TX_COUNTERPARTY_TOKEN | TEXT | Y | | Counterparty token. Populated only for card PULL transactions (PANAMA mechanism). | `C_xyz789abc` |
| 28 | TX_ADJUSTMENTS_JSON | TEXT | Y | | JSON array of fee adjustments. Usually `[]`. See "Querying Adjustments" section. | `["{\"adj\":\"FEE\",\"amt\":{\"amount\":535,\"currency_code\":\"USD\"},\"type\":\"BUSINESS_FEE\"}"]` |

\* Columns 4–23 are null together for ~1.6% of rows. These appear to be "skeleton" rows with only FLOW_NAME,
FLOW_TOKEN, FLOW_OWNER, and ETL columns populated. Filter them out with `TX_TYPE IS NOT NULL` if needed.

## Flow Names (P2P-Relevant)

Defined in `ClientFlowName.proto`. A single P2P payment typically generates transactions under multiple flow names.
The P2P-relevant flows are:

| Flow Name | Proto Policy | Description | TX_MECHANISM | TX_INSTRUMENT_TYPE |
|-----------|-------------|-------------|--------------|-------------------|
| `P2P_ENGINE_TRANSFER` | `P2PEngineTransferPolicy` | Direct balance-to-balance transfer (pull from sender, push to recipient) | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_INTERNAL_BALANCE_XFER` | `P2PEngineBalanceTransferPolicy` | Internal balance transfer used for balance-funded payments (when card cash-in occurs first via Moneta) | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `MONETA_CASH_IN_TRANSFER` | `MonetaCashInPolicy` | Card-funded cash-in to cover the payment. PULL = card charge via Panama, PUSH = balance credit via ledger. | PULL: `PANAMA`, PUSH: `BANKLIN_LEDGER` | PULL: `CARD`, PUSH: `STORED_VALUE` |
| `MONETA_INSTANT_CASH_IN_TRANSFER` | `MonetaCashInPolicy` | Instant card cash-in variant | `PANAMA` / `BANKLIN_LEDGER` | `CARD` / `STORED_VALUE` |
| `P2P_ENGINE_REVERSE_CAPTURE_XFER` | `P2PEngineReverseCaptureTransferPolicy` | Reversal of a capture (refund/cancel) | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_REIMBURSE_CUSTOMER` | `P2PEngineReimburseCustomerPolicy` | Reimbursement to customer | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_REIMBURSE_PUSH` | `P2PEngineReimbursePushPolicy` | Reimbursement push leg | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_SENDER_CLAWBACK` | `P2PEngineClawbackPolicy` | Clawback from sender | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_RECIPIENT_CLAWBACK` | `P2PEngineClawbackPolicy` | Clawback from recipient | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_INTERDICTION_FREEZE` | `P2PEngineSanctionInterdictionFreezePolicy` | Sanctions interdiction freeze | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_BYPASS_ADVERSITY_XFER` | `P2PEngineBypassAdversityTransferPolicy` | Bypass adversity transfer | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `P2P_ENGINE_BYPASS_ADVERSITY_PAY` | `P2PEngineBypassAdversityPayoutPolicy` | Bypass adversity payout | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `SALVAGER_SENDER_CLAWBACK` | `SalvagerSenderClawbackPolicy` | Salvager-initiated sender clawback | `BANKLIN_LEDGER` | `STORED_VALUE` |
| `SALVAGER_RECIPIENT_CLAWBACK` | `SalvagerRecipientClawbackPolicy` | Salvager-initiated recipient clawback | `BANKLIN_LEDGER` | `STORED_VALUE` |

Non-P2P flow names commonly seen in the table: `BALANCE_MOVER_TRANSFER`, `CASH_OUT_TRANSFER`,
`INVEST_CRYPTO_CASH_CARD_ROUND_UP`, `CROW_CRYPTO_UNRESTRICTED_BUY`, `CROW_CRYPTO_UNRESTRICTED_SELL`,
`LYNX_MICRO_AUTH_VERIFICATION`, `POOL_OWNER_CONTRIBUTION`, `POOL_WITHDRAWAL`.

## Joining to Payment State Tables

The primary join key is `FLOW_TOKEN` → `PAYMENT_ID`:

```sql
SELECT le.*, mmt.*
FROM APP_CASH.CASH_DATA_BOT.P2PENGINE_PAYMENT_STATE_LATEST_EVENT le
JOIN APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS mmt
  ON mmt.FLOW_TOKEN = le.PAYMENT_ID
WHERE le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND mmt.TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
```

**Important:** Always mirror the date filter on both tables.

For multiple-capture payments, `FLOW_TOKEN` has a `_capture_N` suffix. This is generated by
`TransferIdempotenceKeyGenerator` in p2p-engine: attempt 1 uses the raw payment ID, attempt 2+ appends
`_capture_<attemptNumber>` (e.g., `P2PE_FIAT_xxx_capture_2`). There is a 128-character limit on these tokens;
overflow cases use a truncated format with the display ID.

To join these back to the payment, split on `_capture_`:

```sql
SPLIT(FLOW_TOKEN, '_capture_')[0] AS PAYMENT_ID
```

The payment state table also has `PULL_TRANSFER_ID` and `PUSH_TRANSFER_ID` columns. For `P2P_ENGINE_TRANSFER` PUSH
transactions, `TX_EXTERNAL_TRANSACTION_ID` matches `PUSH_TRANSFER_ID`. However, for PULL transactions and
`MONETA_CASH_IN_TRANSFER`, the IDs do not reliably match. **Use `FLOW_TOKEN = PAYMENT_ID` as the primary join.**

## Querying Adjustments

`TX_ADJUSTMENTS_JSON` is a TEXT column containing a JSON array of stringified objects. Parse with:

```sql
SELECT
  mmt.FLOW_TOKEN,
  adj.value:adj::STRING AS adjustment,
  adj.value:type::STRING AS fee_type,
  adj.value:amt:amount::NUMBER AS fee_amount_cents,
  adj.value:amt:currency_code::STRING AS fee_currency
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS mmt,
LATERAL FLATTEN(input => PARSE_JSON(mmt.TX_ADJUSTMENTS_JSON)) raw,
LATERAL FLATTEN(input => ARRAY_CONSTRUCT(PARSE_JSON(raw.value))) adj
WHERE mmt.TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND mmt.TX_ADJUSTMENTS_JSON != '[]'
```

Known fee types for P2P: `BUSINESS_FEE`, `CREDIT_CARD_FEE`. Other flows: `INSTANT_DEPOSIT_FEE`.

## Common Query Patterns

### Analyzing captures for a P2P payment

Find all PULL transactions (captures) for a specific payment or set of payments. This includes re-capture attempts
(rows with `_capture_N` suffix on `FLOW_TOKEN`):

```sql
SELECT
  SPLIT(FLOW_TOKEN, '_capture_')[0] AS PAYMENT_ID,
  COUNT(*) AS CAPTURE_ATTEMPT_COUNT,
  SUM(TX_AMOUNT_CENTS) AS TOTAL_AMOUNT_CENTS,
  MIN(TX_CREATED_AT) AS FIRST_CAPTURE_AT,
  MAX(TX_CREATED_AT) AS LAST_CAPTURE_AT,
  LISTAGG(DISTINCT FLOW_NAME, ', ') AS FLOW_NAMES,
  LISTAGG(DISTINCT TX_MECHANISM, ', ') AS MECHANISMS
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS
WHERE FLOW_TOKEN LIKE 'P2PE%'
  AND TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND TX_TYPE = 'PULL'
  AND TX_STATE = 'SUCCEEDED'
  AND FLOW_NAME IN ('P2P_ENGINE_INTERNAL_BALANCE_XFER', 'MONETA_CASH_IN_TRANSFER')
GROUP BY SPLIT(FLOW_TOKEN, '_capture_')[0]
HAVING COUNT(*) > 1
ORDER BY CAPTURE_ATTEMPT_COUNT DESC
LIMIT 50
```

### Breakdown of funding sources for P2P payments

Analyze which instrument types and mechanisms are used for P2P captures:

```sql
SELECT
  TX_INSTRUMENT_TYPE,
  TX_MECHANISM,
  FLOW_NAME,
  COUNT(*) AS cnt,
  SUM(TX_AMOUNT_CENTS) AS total_cents
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS
WHERE TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND FLOW_TOKEN LIKE 'P2PE%'
  AND TX_TYPE = 'PULL'
  AND TX_STATE = 'SUCCEEDED'
GROUP BY TX_INSTRUMENT_TYPE, TX_MECHANISM, FLOW_NAME
ORDER BY cnt DESC
```

### Analyzing card decline reasons

Find why card-funded P2P captures are failing:

```sql
SELECT
  TX_OCTOPUS_RESULT,
  COUNT(*) AS cnt
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS
WHERE TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND FLOW_TOKEN LIKE 'P2PE%'
  AND TX_TYPE = 'PULL'
  AND TX_STATE = 'PERMANENTLY_FAILED'
  AND FLOW_NAME = 'MONETA_CASH_IN_TRANSFER'
GROUP BY TX_OCTOPUS_RESULT
ORDER BY cnt DESC
```

### Finding all transactions for a specific payment

Look up all money-mover transactions associated with a single P2P payment:

```sql
SELECT
  FLOW_TOKEN,
  TX_NUMBER,
  TX_TYPE,
  TX_STATE,
  TX_MECHANISM,
  TX_INSTRUMENT_TYPE,
  TX_AMOUNT_CENTS,
  TX_OCTOPUS_RESULT,
  FLOW_NAME,
  TX_CREATED_AT
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS
WHERE TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND (FLOW_TOKEN = 'P2PE_FIAT_<ID>'
       OR FLOW_TOKEN LIKE 'P2PE_FIAT_<ID>_capture_%')
ORDER BY TX_CREATED_AT
```

### Joining to payment state table with capture details

Get payment outcomes with funding source details from money-mover:

```sql
SELECT
  le.PAYMENT_ID,
  le.PAYMENT_STATE_CODE,
  le.PAYMENT_VALUE_AMOUNT_CENTS,
  mmt.FLOW_NAME,
  mmt.TX_TYPE,
  mmt.TX_STATE,
  mmt.TX_INSTRUMENT_TYPE,
  mmt.TX_MECHANISM,
  mmt.TX_AMOUNT_CENTS,
  mmt.TX_OCTOPUS_RESULT
FROM APP_CASH.CASH_DATA_BOT.P2PENGINE_PAYMENT_STATE_LATEST_EVENT le
JOIN APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS mmt
  ON mmt.FLOW_TOKEN = le.PAYMENT_ID
WHERE le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND mmt.TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND mmt.TX_TYPE = 'PULL'
  AND le.PAYMENT_STATE_CODE = 'FAILED'
  AND le.FAILURE_REASON_CODE = 'INSUFFICIENT_FUNDS'
```

### Counting reversals

```sql
SELECT
  TX_TYPE,
  TX_STATE,
  COUNT(*) AS cnt
FROM APP_CASH.CASH_DATA_BOT.MONEY_MOVER_TRANSACTIONS
WHERE TX_CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND FLOW_TOKEN LIKE 'P2PE%'
  AND TX_TYPE IN ('PUSH_REVERSAL', 'PULL_REVERSAL')
GROUP BY TX_TYPE, TX_STATE
ORDER BY cnt DESC
```

### Understanding the transaction lifecycle of a P2P payment

A typical successful balance-funded P2P payment generates these rows:

| TX_NUMBER | TX_TYPE | FLOW_NAME | TX_MECHANISM | TX_INSTRUMENT_TYPE | Description |
|-----------|---------|-----------|--------------|-------------------|-------------|
| 0 | PULL | P2P_ENGINE_TRANSFER | BANKLIN_LEDGER | STORED_VALUE | Debit sender's balance |
| 1 | PUSH | P2P_ENGINE_TRANSFER | BANKLIN_LEDGER | STORED_VALUE | Credit recipient's balance |

A card-funded payment adds Moneta rows:

| TX_NUMBER | TX_TYPE | FLOW_NAME | TX_MECHANISM | TX_INSTRUMENT_TYPE | Description |
|-----------|---------|-----------|--------------|-------------------|-------------|
| 0 | PULL | MONETA_CASH_IN_TRANSFER | PANAMA | CARD | Charge sender's card |
| 1 | PUSH | MONETA_CASH_IN_TRANSFER | BANKLIN_LEDGER | STORED_VALUE | Credit sender's Cash balance |
| 0 | PULL | P2P_ENGINE_INTERNAL_BALANCE_XFER | BANKLIN_LEDGER | STORED_VALUE | Debit sender's balance |
| 1 | PUSH | P2P_ENGINE_INTERNAL_BALANCE_XFER | BANKLIN_LEDGER | STORED_VALUE | Credit recipient's balance |

## Source Code References

Key source files in cash-server for understanding this table's data:

- Proto definitions (money-mover):
  - `money-mover/client-protos/src/main/proto/squareup/cash/moneymover/api/v3/transaction/TransactionType.proto`
  - `money-mover/client-protos/src/main/proto/squareup/cash/moneymover/api/v3/transaction/TransactionState.proto`
  - `money-mover/client-protos/src/main/proto/squareup/cash/moneymover/api/v3/transaction/MoneyMovingMechanism.proto`
  - `money-mover/client-protos/src/main/proto/squareup/cash/moneymover/api/v3/common/ClientFlowName.proto`
- Kotlin models (money-mover):
  - `money-mover/core/src/main/kotlin/com/squareup/cash/moneymover/models/TransactionType.kt`
  - `money-mover/core/src/main/kotlin/com/squareup/cash/moneymover/models/TransactionState.kt`
  - `money-mover/core/src/main/kotlin/com/squareup/cash/moneymover/models/TransactionMechanism.kt` -- maps mechanisms to instrument types and processing services
- P2P Engine capture logic:
  - `p2p-engine/service/src/main/kotlin/com/squareup/cash/p2p/engine/service/payments/lifecycle/workflow/dag/steps/context/TransferIdempotenceKeyGenerator.kt` -- generates `_capture_N` suffixed FLOW_TOKENs
  - `p2p-engine/service/src/main/kotlin/com/squareup/cash/p2p/engine/service/payments/lifecycle/workflow/dag/steps/CaptureFromExternalInstrumentStep.kt` -- orchestrates card capture
  - `p2p-engine/service/src/main/kotlin/com/squareup/cash/p2p/engine/service/payments/lifecycle/workflow/dag/steps/reverse/ReverseCaptureExternalTransferToBalanceStep.kt` -- handles capture reversals
