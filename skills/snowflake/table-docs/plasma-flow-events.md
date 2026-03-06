# Query Plasma Flow Events

Query and analyze Plasma flow event data from Snowflake. Plasma is the client-side flow orchestration framework that
drives every user-facing step in Brand B — passcode entry, instrument selection, confirm-recipient screens, IDV,
scam warnings, and more. This table records every event emitted by Plasma flows across the entire app, not just P2P.

## Tables

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE (preferred)

**Use this table when you need to join plasma flows to payments.** It is a superset of the public table with the same
schema plus extra columns: `ALTERNATE_FLOW_ID` (contains the payment ID for SEND and REQUEST flows), `APP_PLATFORM`,
`APP_VERSION`, `BLOCKER_IDS`, and `OBSERVABILITY_METADATA`.

~291 billion rows total. ~2.5 billion rows per day.

**Clustering key:** `LINEAR(TO_DATE(EVENT_OCCURRED_AT))`. Always include an `EVENT_OCCURRED_AT` date filter.
Default to `WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())` unless the user specifies a different range.

**Column naming:** This table uses `EVENT_OCCURRED_AT` (not `_OCCURRED_AT`) and `EVENTLY_ENTITY_IDENTIFIER`
(not `_ENTITY_IDENTIFIER`). The public table uses underscore-prefixed Evently envelope names.

### CASH_DATA_BOT.PUBLIC.PLASMA_FLOW_EVENTS

The original public table. Same event data but **missing** `ALTERNATE_FLOW_ID`, `APP_PLATFORM`, `APP_VERSION`,
`BLOCKER_IDS`, and `OBSERVABILITY_METADATA`. Use this table only when you don't need the payment linkage or
app metadata. Uses `_OCCURRED_AT` as the clustering key.

**Clustering key:** `LINEAR(_OCCURRED_AT)`.

## How Events Are Produced

Events are published by `RealFlowEventPublisher` in the Plasma service. Each event is a `FlowStateEvent` proto
(defined in `plasma/plasma-events/src/main/proto/example/app/plasma/flows/events.proto`). The publisher sets
`subject = flowSnapshot.flowToken`, which becomes the Evently `entity_identifier`. The `alternate_flow_id` field
is populated from `flowSnapshot.alternateFlowId`, which is set at flow creation time.

For P2P SEND and REQUEST flows, fiatly's `PlasmaFlowFactory` (at
`fiatly/service/src/main/kotlin/.../PlasmaFlowFactory.kt`) calls `.alternate_flow_id(paymentId)` when creating the
flow, so `ALTERNATE_FLOW_ID` = the `P2PE_FIAT_...` payment ID. **This is the recommended way to join plasma flows to
payments** — it works for ~97% of SEND events and ~96% of REQUEST events.

The ~3% of events within SEND/REQUEST flows that are missing `ALTERNATE_FLOW_ID` are **subflow events**. Subflows
(e.g., IDV, link card, insufficient funds) run inside the parent flow and share the same `FLOW_TOKEN`, but they do
not inherit `ALTERNATE_FLOW_ID` because they are created by the client-side Plasma framework rather than the
server-side factory. For most use cases this doesn't matter — the parent flow's top-level events (`INITIATED`,
`SEND_PAYMENT_REQUIREMENT`, `JANUS_VERIFY_PASSCODE`, `RESUME_PAYMENT_REQUIREMENT`, `ENDED`) all have the ID populated.

`ALTERNATE_FLOW_ID` is populated for these flow types:

| Flow Type | % Populated | Missing Events |
|-----------|------------|----------------|
| `SEND_P2P_FIAT_PAYMENT` | ~97% | Subflow events (IDV, LINK_CARD_V2, instrument selection, etc.) |
| `REQUEST_P2P_FIAT_PAYMENT` | ~96% | Subflow events |

`ALTERNATE_FLOW_ID` is **always null** for: `RESUME_P2P_FIAT_PAYMENT`, `CANCEL_P2P_FIAT_PAYMENT`,
`P2P_CREATE_PAYMENT_LINK`, `REFUND_P2P_FIAT_PAYMENT`, `REVIEW_P2P_REFUND_REQUEST`, and
`PLASMA_REQUIREMENT_WRAPPER_FOR_FRANKLIN`.

For P2P RESUME flows, the **client app** creates the flow directly with Plasma (the server sends a client route
containing `ResumeP2pFiatPaymentFlowParameters` with `payment_id` and `external_id`, but these are flow parameters
not exposed in the event schema). The client does not set `alternate_flow_id`, so it is always null for RESUME flows.

## Column Reference (STAGING_PLASMA_FLOW_EVENTS)

Column names shown are for the staging table. The public table equivalents are noted where they differ.

| # | Column | Public Name | Type | Nullable | Description |
|---|--------|-------------|------|----------|-------------|
| 1 | EVENT_RECEIVED_AT | _RECEIVED_AT | TIMESTAMP | Y | When the event was received by the pipeline |
| 2 | EVENTLY_TOPIC | _TOPIC | TEXT | Y | Always `plasma_flow_events` |
| 3 | EVENTLY_ID | _ID | TEXT | Y | Unique event identifier |
| 4 | EVENTLY_ENTITY_IDENTIFIER | _ENTITY_IDENTIFIER | TEXT | Y | Usually equals `flow_token`. For confirm-recipient-phone subflows, contains `<payment_id>:P2P_SENDER_CONFIRM_RECIPIENT_PHONE`. |
| 5 | EVENTLY_PARTITION_KEY | _PARTITION_KEY | TEXT | Y | Always equals entity identifier |
| 6 | EVENTLY_TYPE | _TYPE | TEXT | Y | Always `PLASMA_FLOW_EVENT` |
| 7 | **EVENT_OCCURRED_AT** | **_OCCURRED_AT** | TIMESTAMP | Y | **Clustering key — always filter on this.** |
| 8 | EVENTLY_VERSION | _VERSION | TEXT | Y | Always null |
| 9 | **CUSTOMER_TOKEN** | same | TEXT | Y | Customer who triggered the flow |
| 10 | **FLOW_EVENT_TYPE** | same | TEXT | Y | Type of flow event. See "Flow Event Types". |
| 11 | **FLOW_RESULT** | same | TEXT | Y | Terminal result. Only on `ENDED` events. **Enum:** `SUCCESS`, `FAILED`, `CANCELED` |
| 12 | **FLOW_TOKEN** | same | TEXT | Y | Unique token for this flow instance. All events in the same flow share this. |
| 13 | **FLOW_TYPE** | same | TEXT | Y | The type of Plasma flow. See "P2P Flow Types". |
| 14 | MESSAGE_ID | same | TEXT | Y | Composite key: `<flow_token>:<event_type>:<scope_key>:<req_type>:<resolution>` |
| 15 | **REQUIREMENT_RESOLUTION** | same | TEXT | Y | How a requirement resolved. **Enum:** `RESOLVED`, `FAILED`, `SKIPPED_RESOLUTION`, `CANCELED_RESOLUTION` |
| 16 | **REQUIREMENT_TYPE** | same | TEXT | Y | The requirement presented to the user. See "P2P Requirement Types". |
| 17 | SCOPE_KEY | same | TEXT | Y | Scoping key. Usually `flow_token`. For NSF retries: `FundPaymentCompositeStep\|runloop\|N:insufficient_funds_subflow` |
| 18 | SUBFLOW_TOKEN | same | TEXT | Y | Token of a child subflow (on `REQUIREMENT_SUBFLOW` events) |
| 19 | SUBFLOW_TYPE | same | TEXT | Y | Type of child subflow. See "P2P Subflow Types". |
| 20 | **ALTERNATE_FLOW_ID** | _(not in public)_ | TEXT | Y | **Payment ID for SEND and REQUEST flows.** Set by fiatly to `P2PE_FIAT_...`. ~97% populated for SEND, ~96% for REQUEST. Always null for RESUME and other flow types. |
| 21 | APP_PLATFORM | _(not in public)_ | TEXT | Y | Client platform. `IOS`, `ANDROID`, `WEB`. |
| 22 | APP_VERSION | _(not in public)_ | TEXT | Y | Client app version. `5.36.0`, `5.37.0`, etc. |
| 23 | BLOCKER_IDS | _(not in public)_ | TEXT | Y | Comma-separated blocker IDs sent to the client during this event. |
| 24 | OBSERVABILITY_METADATA | _(not in public)_ | TEXT | Y | Optional metadata from the flow/requirement owner. Usually empty. |

## Flow Event Types

Events for a single flow occur in this order:

1. **`INITIATED`** — Flow started. `flow_result`, `requirement_type`, `requirement_resolution` are all null.
2. **`REQUIREMENT_UI_FORM`** — A UI screen was shown to the user (e.g., passcode entry, confirm recipient).
   `requirement_type` is set; `requirement_resolution` is null.
3. **`REQUIREMENT_ENDED`** — A requirement completed. Both `requirement_type` and `requirement_resolution` are set.
4. **`REQUIREMENT_SUBFLOW`** — A child subflow was launched. `subflow_type` and `subflow_token` are set.
5. **`FLOW_UI_FORM`** — A flow-level UI form was shown (less common than requirement-level forms).
6. **`IDLE`** / **`REQUIREMENT_IDLE`** — Flow or requirement entered an idle state (rare).
7. **`ENDED`** — Flow completed. `flow_result` is set (`SUCCESS`, `FAILED`, or `CANCELED`).

A typical successful P2P send flow produces this sequence:

```
INITIATED
REQUIREMENT_ENDED  (SEND_PAYMENT_REQUIREMENT → RESOLVED)
REQUIREMENT_UI_FORM (JANUS_VERIFY_PASSCODE)
REQUIREMENT_ENDED  (JANUS_VERIFY_PASSCODE → RESOLVED)
REQUIREMENT_ENDED  (RESUME_PAYMENT_REQUIREMENT → RESOLVED)
ENDED              (SUCCESS)
```

If a confirm-recipient screen is shown, additional events appear between passcode and resume:

```
REQUIREMENT_UI_FORM (FIATLY_CONFIRM_RECIPIENT_REQUIREMENT)
REQUIREMENT_ENDED  (FIATLY_CONFIRM_RECIPIENT_REQUIREMENT → RESOLVED)
REQUIREMENT_ENDED  (RESUME_PAYMENT_REQUIREMENT → RESOLVED)
```

## P2P Flow Types

| Flow Type | 7d Volume | Description |
|-----------|-----------|-------------|
| `SEND_P2P_FIAT_PAYMENT` | ~367M | Sending a P2P payment (covers the full flow including passcode, requirements, and submission) |
| `RESUME_P2P_FIAT_PAYMENT` | ~21M | Resuming a draft/pending payment (e.g., after sponsor approval or instrument change) |
| `REQUEST_P2P_FIAT_PAYMENT` | ~13M | Requesting money from another user |
| `CANCEL_P2P_FIAT_PAYMENT` | ~7M | Cancelling a pending payment |
| `P2P_CREATE_PAYMENT_LINK` | ~1.6M | Creating a payment link |
| `REFUND_P2P_FIAT_PAYMENT` | ~955K | Refunding a payment |
| `REVIEW_P2P_REFUND_REQUEST` | ~305K | Reviewing a refund request |
| `PLASMA_REQUIREMENT_WRAPPER_FOR_FRANKLIN` | (non-P2P-specific) | Wraps passcode reset flows. Useful for finding customers who reset their passcode before a payment. |

## P2P Requirement Types (for SEND_P2P_FIAT_PAYMENT)

Sorted by 7-day volume:

| Requirement Type | Volume | Description |
|------------------|--------|-------------|
| `JANUS_VERIFY_PASSCODE` | ~85M | User verified their passcode |
| `RESUME_PAYMENT_REQUIREMENT` | ~69M | Backend submitted the payment (always appears after all other requirements resolve) |
| `SEND_PAYMENT_REQUIREMENT` | ~67M | Initial payment creation step |
| `FIATLY_DUPLICATE_PAYMENT_REQUIREMENT` | ~6.4M | Duplicate payment warning shown |
| `FIATLY_SCAM_WARNING_REQUIREMENT` | ~1.2M | Scam warning interstitial |
| `LINK_CARD_V2` | ~806K | User prompted to link a card |
| `FIATLY_INSUFFICIENT_FUNDS_REQUIREMENT` | ~691K | Insufficient funds; user may switch instruments |
| `FIATLY_P2P_INSTRUMENT_SELECTION_REQUIREMENT` | ~262K | Instrument selection screen |
| `IDV` / `EIDV_INTRODUCTION` / `ELECTRONIC_IDV` | ~230K each | Identity verification steps |
| `FIATLY_CONFIRM_RECIPIENT_REQUIREMENT` | ~220K | Confirm recipient identity screen (MDP-related) |
| `IDV_OR_SPONSORSHIP` | ~211K | IDV or sponsorship required (teen/family accounts) |
| `FIATLY_SENDER_CONFIRM_RECIPIENT_PHONE` | ~79K | Confirm recipient phone number screen (MDP-related) |
| `GUARDRAILS_ADVERSITY_BLOCKED_ACTION_REQUIREMENT` | ~98K | Your Companyed by guardrails adversity |
| `GRADUATION_JOURNEY_ERROR_NOTIFICATIONS` | ~11K | Graduation journey (teen → adult) error |

### Passcode Reset Requirements (PLASMA_REQUIREMENT_WRAPPER_FOR_FRANKLIN)

| Requirement Type | Description |
|------------------|-------------|
| `VERIFY_ALIAS_FOR_PASSCODE_RESET` | Verify email/phone for passcode reset |
| `VERIFY_INSTRUMENT_FOR_PASSCODE_RESET` | Verify card for passcode reset |
| `VERIFY_SSN_FOR_PASSCODE_RESET` | Verify SSN for passcode reset |
| `SET_PASSCODE` | Set new passcode after verification |
| `PASSES_CUSTOMER_DENYLIST` | Denylist check during passcode reset |

## P2P Subflow Types

| Subflow Type | Description |
|--------------|-------------|
| `ELIGIBILITY_RESOLUTION` | Eligibility check subflow |
| `IDV_OR_SPONSORSHIP` | Identity verification or sponsorship subflow |
| `IDV_IDENTITY_VERIFICATION` | Identity verification subflow |
| `ELECTRONIC_IDENTITY_VERIFICATION` | Electronic IDV subflow |
| `P2P_INSUFFICIENT_FUNDS` | Insufficient funds resolution subflow |
| `LINK_CARD` | Card linking subflow |
| `VERIFY_PASSCODE` | Passcode verification subflow |
| `CASH_IN_INSTRUMENT_SELECTION_FLOW` | Cash-in instrument selection subflow |

## Joining to Payment Tables

A single payment can have **multiple** Plasma flows: one SEND flow (initial creation) and zero or more RESUME flows
(e.g., after sponsor approval, instrument change, or re-entering the payment from activity feed). The SEND and RESUME
flows have different flow_tokens and are separate rows. Use the strategies below depending on which flows you need.

### Strategy 1: ALTERNATE_FLOW_ID (best for SEND and REQUEST flows)

The staging table's `ALTERNATE_FLOW_ID` column contains the `P2PE_FIAT_...` payment ID, set by fiatly when creating
the flow. This is populated for ~97% of SEND and ~96% of REQUEST events. It is always null for RESUME and other flows.

```sql
SELECT alternate_flow_id AS payment_id, flow_token, flow_event_type, requirement_type
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND flow_type IN ('SEND_P2P_FIAT_PAYMENT', 'REQUEST_P2P_FIAT_PAYMENT')
  AND alternate_flow_id = 'P2PE_FIAT_...'
ORDER BY event_occurred_at ASC
```

Find all SEND/REQUEST flows for a payment:

```sql
SELECT DISTINCT flow_token, flow_type
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND alternate_flow_id = 'P2PE_FIAT_...'
```

### Strategy 2: customer_token + timestamp proximity (for RESUME flows or public table)

Join on `customer_token` and a narrow time window. For SEND flows, match the flow INITIATED time to the payment
`CREATED_AT`. For RESUME flows, match to the payment's `CREATED_AT` with a wider window since the resume happens
after the payment already exists.

SEND flow → payment linkage:

```sql
WITH p2p_flows AS (
  SELECT event_occurred_at, customer_token, flow_token
  FROM app_cash.cash_data_bot.staging_plasma_flow_events
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
    AND flow_type = 'SEND_P2P_FIAT_PAYMENT'
    AND flow_event_type = 'INITIATED'
)
SELECT f.flow_token, p.payment_id
FROM p2p_flows f
JOIN app_cash.cash_data_bot.p2pengine_payment_state_latest_event p
  ON p.sender_token = f.customer_token
  AND DATEDIFF('second', f.event_occurred_at, p.created_at) BETWEEN -1 AND 5
WHERE p.created_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
QUALIFY ROW_NUMBER() OVER (PARTITION BY f.flow_token ORDER BY p.created_at ASC) = 1
```

### Strategy 3: EVENTLY_ENTITY_IDENTIFIER for confirm-recipient-phone subflows

For `FIATLY_SENDER_CONFIRM_RECIPIENT_PHONE` events, `EVENTLY_ENTITY_IDENTIFIER` contains the payment ID in the
format `P2PE_FIAT_...:P2P_SENDER_CONFIRM_RECIPIENT_PHONE`:

```sql
SELECT SPLIT_PART(evently_entity_identifier, ':', 1) AS payment_id, flow_token
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND evently_entity_identifier LIKE 'P2PE_%'
```

### Strategy 4: Look up flow events by known payment_id + customer_token

If you already have a `payment_id` from the payment tables, look up the SEND flow directly via `ALTERNATE_FLOW_ID`,
or search by `customer_token` and time for RESUME flows:

```sql
-- SEND flow (direct lookup)
SELECT flow_event_type, flow_result, requirement_type, requirement_resolution
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND alternate_flow_id = 'P2PE_FIAT_...'
ORDER BY event_occurred_at ASC

-- RESUME flows (by customer_token + time)
SELECT flow_event_type, flow_result, requirement_type, requirement_resolution, flow_token
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= '2026-02-01'
  AND customer_token = 'C_xxxxxxxx'
  AND flow_type = 'RESUME_P2P_FIAT_PAYMENT'
ORDER BY event_occurred_at ASC
```

## Common Query Patterns

### Trace all events for a single flow

```sql
SELECT event_occurred_at, flow_event_type, flow_result, requirement_type, requirement_resolution, subflow_type,
  scope_key, alternate_flow_id
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND flow_token = '<flow_token>'
ORDER BY event_occurred_at ASC
```

### Trace all P2P events for a customer

```sql
SELECT event_occurred_at, flow_type, flow_event_type, flow_result, flow_token, requirement_type,
  requirement_resolution, alternate_flow_id
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND customer_token = 'C_xxxxxxxx'
  AND flow_type IN ('SEND_P2P_FIAT_PAYMENT', 'RESUME_P2P_FIAT_PAYMENT', 'REQUEST_P2P_FIAT_PAYMENT')
ORDER BY event_occurred_at ASC
```

### Count requirement types for P2P sends

```sql
SELECT requirement_type, COUNT(*) AS c
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND flow_type = 'SEND_P2P_FIAT_PAYMENT'
  AND flow_event_type = 'REQUIREMENT_ENDED'
  AND requirement_type IS NOT NULL
GROUP BY requirement_type
ORDER BY c DESC
```

### Check whether a specific requirement was shown for a payment

Use `ALTERNATE_FLOW_ID` to find all events for a known payment:

```sql
SELECT flow_event_type, requirement_type, requirement_resolution, app_platform, app_version
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND alternate_flow_id = 'P2PE_FIAT_...'
  AND requirement_type = 'FIATLY_CONFIRM_RECIPIENT_REQUIREMENT'
```

### Count confirm-recipient resolution outcomes

```sql
SELECT requirement_resolution, COUNT(*) AS c
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND requirement_type = 'GRADUATION_JOURNEY_ERROR_NOTIFICATIONS'
  AND requirement_resolution IS NOT NULL
GROUP BY requirement_resolution
```

### Find payments where sender saw confirm-recipient AND confirm-phone

```sql
WITH flows_with_confirm AS (
  SELECT alternate_flow_id AS payment_id,
    MAX(CASE WHEN requirement_type = 'FIATLY_CONFIRM_RECIPIENT_REQUIREMENT' THEN 1 ELSE 0 END) AS saw_confirm,
    MAX(CASE WHEN requirement_type = 'FIATLY_SENDER_CONFIRM_RECIPIENT_PHONE' THEN 1 ELSE 0 END) AS saw_phone
  FROM app_cash.cash_data_bot.staging_plasma_flow_events
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
    AND flow_type = 'SEND_P2P_FIAT_PAYMENT'
    AND alternate_flow_id IS NOT NULL
    AND requirement_type IN ('FIATLY_CONFIRM_RECIPIENT_REQUIREMENT', 'FIATLY_SENDER_CONFIRM_RECIPIENT_PHONE')
  GROUP BY payment_id
)
SELECT saw_confirm, saw_phone, COUNT(*) AS c
FROM flows_with_confirm
GROUP BY 1, 2
```

### Find customers who reset their passcode before a payment

```sql
WITH passcode_resets AS (
  SELECT event_occurred_at, customer_token
  FROM app_cash.cash_data_bot.staging_plasma_flow_events
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
    AND flow_type = 'PLASMA_REQUIREMENT_WRAPPER_FOR_FRANKLIN'
    AND requirement_type IN ('VERIFY_ALIAS_FOR_PASSCODE_RESET', 'VERIFY_INSTRUMENT_FOR_PASSCODE_RESET')
    AND flow_event_type = 'REQUIREMENT_ENDED'
    AND requirement_resolution = 'RESOLVED'
)
SELECT le.payment_state_code, COUNT(*) AS c
FROM passcode_resets pr
JOIN app_cash.cash_data_bot.p2pengine_payment_state_latest_event le
  ON le.sender_token = pr.customer_token
  AND le.created_at BETWEEN pr.event_occurred_at AND DATEADD(hour, 1, pr.event_occurred_at)
WHERE le.created_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY le.payment_state_code
ORDER BY c DESC
```

### Insufficient funds retry loop analysis

The `scope_key` column tracks retry iterations for insufficient funds. The pattern
`FundPaymentCompositeStep|runloop|N:insufficient_funds_subflow` indicates the Nth attempt:

```sql
SELECT scope_key, COUNT(*) AS c
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND flow_type IN ('SEND_P2P_FIAT_PAYMENT', 'RESUME_P2P_FIAT_PAYMENT')
  AND scope_key LIKE 'FundPaymentCompositeStep%insufficient_funds%'
GROUP BY scope_key
ORDER BY c DESC
```

### Join plasma flows to payment outcomes (via ALTERNATE_FLOW_ID)

Use `ALTERNATE_FLOW_ID` to directly link SEND flows to payment outcomes without timestamp matching:

```sql
WITH flows_with_requirement AS (
  SELECT DISTINCT alternate_flow_id AS payment_id
  FROM app_cash.cash_data_bot.staging_plasma_flow_events
  WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
    AND flow_type = 'SEND_P2P_FIAT_PAYMENT'
    AND alternate_flow_id IS NOT NULL
    AND requirement_type = 'FIATLY_CONFIRM_RECIPIENT_REQUIREMENT'
)
SELECT le.payment_state_code, COUNT(*) AS c
FROM flows_with_requirement fr
JOIN app_cash.cash_data_bot.p2pengine_payment_state_latest_event le ON le.payment_id = fr.payment_id
WHERE le.created_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY le.payment_state_code
ORDER BY c DESC
```

### Analyze by app platform/version

```sql
SELECT app_platform, app_version, COUNT(DISTINCT flow_token) AS flows
FROM app_cash.cash_data_bot.staging_plasma_flow_events
WHERE event_occurred_at >= DATEADD(day, -7, CURRENT_DATE())
  AND flow_type = 'SEND_P2P_FIAT_PAYMENT'
  AND flow_event_type = 'INITIATED'
GROUP BY app_platform, app_version
ORDER BY flows DESC
LIMIT 20
```
