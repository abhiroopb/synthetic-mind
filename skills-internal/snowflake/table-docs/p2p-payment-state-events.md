# Query P2P Payment Summary Events

Query and analyze P2P payment state data from Snowflake.

## Tables

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

Full event history for P2P payments. One row per state transition event, so a single payment has multiple rows.
Use this table when you need to analyze specific events or transitions (e.g., finding payments that hit a particular
hurdle, or examining the sequence of states a payment went through).

### YOUR_DB.YOUR_SCHEMA.YOUR_TABLE

One row per payment reflecting the latest/current state. Use this table when you need the final outcome of a payment
(e.g., checking whether a payment ended in `PAID_OUT` or `FAILED`).

**Clustering key:** `LINEAR(TO_DATE(CREATED_AT))`. Always include a `CREATED_AT` date filter to leverage clustering
and avoid full table scans. Default to `WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())` unless the user
specifies a different range.

## Column Reference: P2PENGINE_PAYMENT_STATE_LATEST_EVENT

- **Nullable**: Y = null values observed in practice, N = always populated
- **FK**: indicates column joins to another table

| # | Field | Type | Nullable | FK | Description | Example / Enum Values |
|---|-------|------|----------|----|-------------|----------------------|
| 1 | EVENT_RECEIVED_AT | TIMESTAMP | N | | When the event was received by the pipeline | `2025-07-15T15:19:00.756` |
| 2 | EVENT_OCCURRED_AT | TIMESTAMP | N | | When the event actually occurred | `2025-07-15T15:19:00.753` |
| 3 | EVENT_ID | TEXT | N | | Unique event identifier (PAYMENT_ID \| sequence) | `P2PE_FIAT_E34BC69A81394DB6B030454458C13628\|50` |
| 4 | EVENT_SOURCE | TEXT | N | | System that produced the event | `p2p-engine` |
| 5 | PAYMENT_ID | TEXT | N | events table, `LIMIT_DECISION_EVENTS` (as `SPLIT_PART(payment_token, ':', 1)`), `STAGING_PLASMA_FLOW_EVENTS` (as `ALTERNATE_FLOW_ID`), `APP.PAYMENT_SUMMARY` (as `payment_token`) | Unique payment identifier | `P2PE_FIAT_E34BC69A81394DB6B030454458C13628` |
| 6 | CREATED_AT | TIMESTAMP | N | | When the payment was created. **Clustering key -- always filter on this.** | `2025-07-15T15:18:54.559` |
| 7 | CLIENT_ID | TEXT | N | | Originating client system | **Enum:** `fiatly`, `p2p-encore`, `payroll` |
| 8 | PAYMENT_TYPE | TEXT | N | | Type of payment (top 5 by volume) | **Enum:** `P2P_FIAT` (99.7%), `ALLOWANCE`, `CASH_CARD_PURCHASE`, `MARKETING`, `REFERRAL`, `INTERNAL_P2P_FIAT`, `BRAND_A_PAYROLL`, `MONEY_POOL_CONTRIBUTION`, `OON_MONEY_POOL_CONTRIBUTION`, `BRAND_D_ARTIST_CONTRIBUTION`, `REIMBURSEMENT`, `SPONSOR_DEPOSIT_TO_MANAGED_ACCOUNT`, `SPONSOR_WITHDRAWAL_FROM_MANAGED_ACCOUNT`, `OON_P2P_FIAT` |
| 9 | SENDER_TOKEN | TEXT | N | | Sender customer token | `C_g9ed1qm67` |
| 10 | RECIPIENT_CUSTOMER_TOKEN | TEXT | N | | Recipient customer token | `C_s92tw0yy3` |
| 11 | RECIPIENT_PROSPECT_TOKEN | TEXT | Y | | Token for recipients not yet on Brand B | |
| 12 | PAYMENT_VALUE_AMOUNT_CENTS | NUMBER | N | | Payment amount in cents | `47000` ($470), `1500` ($15) |
| 13 | PAYMENT_VALUE_CURRENCY_CODE | TEXT | N | | Currency | `USD` |
| 14 | PAYMENT_TAGS | ARRAY | N | | Tags; usually empty. Non-empty for recurring/payroll/referral. | `[{"tag": "recurring-payment-cadence", "data": "weekly"}]`, `[{"tag": "referrer_token", "data": "C_nt2z2hyvb"}]`, `[{"tag": "employer-display-name", "data": "Acme Corp"}]` |
| 15 | HAS_INITIATOR_NOTE | BOOLEAN | N | | Whether the sender included a note | `true`, `false` |
| 16 | EXTERNAL_ID | TEXT | N | | External-facing payment identifier (UUID portion) | `E34BC69A81394DB6B030454458C13628` |
| 17 | CREATED_AT_EPOCH_MS | NUMBER | N | | Payment creation time as epoch ms | `1752592734559` |
| 18 | CREATION_MECHANISM | TEXT | N | | How the payment was initiated (top 5 by volume) | **Enum:** `APP` (97%), `QR_CODE`, `CASHBOARD`, `PAY_LINK`, `RECURRING_PAYMENTS`, `WEB`, `REFERRAL_BOUNTY`, `REIMBURSEMENT`, `PURCHASE`, `SQPAYROLL_TO_EMPLOYEE`, `MARKETING`, `REFERRAL_REWARD`, `NEARBY` |
| 19 | PASSCODE_CONFIRMED_AT | TIMESTAMP | Y | | When the sender confirmed their passcode | `2025-07-15T15:18:55.439` |
| 20 | **PAYMENT_STATE_CODE** | TEXT | N | | **Important.** Current/final payment state. | **Enum (by frequency):** `PAID_OUT`, `FAILED`, `WAITING_ON_SENDER`, `WAITING_ON_RECIPIENT`, `WAITING_ON_SPONSOR`, `WAITING_ON_COMPLIANCE_REVIEW`, `WAITING_ON_RISK`, `CAPTURING`, `PAYING_OUT`, `WAITING_ON_INTERNAL`, `SCHEDULED`, `CAPTURED`, `VALIDATING`, `VALIDATED`, `CREATED`, `REFUNDING`, `PULLING_REFUND`, `WAITING_TO_REFUND`, `FREEZING` |
| 21 | **HURDLES** | ARRAY | N | | **Important.** Hurdles presented during the payment flow. Usually empty (`[]`). See "Querying Hurdles" section. | |
| 22 | **PAYMENT_EXPERIMENT_COHORTS** | OBJECT | Y | | **Important.** Experiment cohort assignments. See "Querying Experiment Cohorts" section. | `{"dag_v2_experiment_cohort": "BASIC_EXPERIMENT_COHORT_TREATMENT", ...}` |
| 23 | PULL_AMOUNT_CENTS | NUMBER | Y | | Amount pulled from sender in cents | `47000` |
| 24 | PULL_AMOUNT_CURRENCY_CODE | TEXT | Y | | Currency of pull amount | `USD` |
| 25 | PUSH_AMOUNT_CENTS | NUMBER | Y | | Amount pushed to recipient in cents | `47000` |
| 26 | PUSH_AMOUNT_CURRENCY_CODE | TEXT | Y | | Currency of push amount | `USD` |
| 27 | EXCHANGE_DETAILS | OBJECT | Y | | FX details for cross-border payments | |
| 28 | CAPTURED_AT | TIMESTAMP | Y | | When funds were captured from sender | `2025-07-15T15:18:58.831` |
| 29 | PAID_OUT_AT | TIMESTAMP | Y | | When funds were paid out to recipient | `2025-07-15T15:18:59.180` |
| 30 | PAYMENT_FUNDING_SOURCE | OBJECT | Y | | Funding source chosen by sender | |
| 30a | .payment_instrument_token | TEXT | | | `B$_` prefix = Cash balance, otherwise card hash | `B$_C_5eceaaywc`, `55318d6aad82938f169b6db09bf58ab474f845de` |
| 30b | .use_balance_first | BOOLEAN | | | Whether to use Cash balance before the card | `false` |
| 30c | .apple_pay_payment_token | TEXT | | | Apple Pay token if used | |
| 30d | .google_pay_payment_token | TEXT | | | Google Pay token if used | |
| 30e | .card_info | OBJECT | | | Card info if available | |
| 31 | PAYMENT_STATE_TRANSITIONS | ARRAY | N | | Ordered state transitions. States use `PAYMENT_STATE_CODE_` prefix. | `[{"payment_state_code": "PAYMENT_STATE_CODE_CREATED", "transitioned_at": "..."}]` |
| 32 | FAILED_AT | TIMESTAMP | Y | | When the payment failed | |
| 33 | FAILURE_REASON_CODE | TEXT | Y | | Reason for failure. Stored without the `PAYMENT_FAILURE_REASON_CODE_` prefix. **Top 10 by freq:** `INSUFFICIENT_FUNDS`, `RISK_FAILURE`, `MANUAL_CANCELLED`, `PULL_MONEY_CARD_DECLINED`, `SENDER_BLOCKED_FROM_RECIPIENT`, `RECIPIENT_BLOCKED_FROM_SENDER`, `SENDER_ACCOUNT_CLOSED`, `SENDER_FAILED_MONTHLY_LIMITS`, `PASSCODE_CHECK_FAILED`, `SENT_TO_SELF`. **Limits:** `SENDER_AMOUNT_EXCEEDED_SINGLE_TRANSACTION_LIMIT`, `SENDER_AMOUNT_BELOW_MINIMUM_TRANSACTION_LIMIT`, `SENDER_FAILED_WEEKLY_LIMITS`, `SENDER_OTHER_LIMITS_ERROR`, `RECIPIENT_AMOUNT_EXCEEDED_SINGLE_TRANSACTION_LIMIT`, `RECIPIENT_AMOUNT_BELOW_MINIMUM_TRANSACTION_LIMIT`, `RECIPIENT_FAILED_WEEKLY_LIMITS`, `RECIPIENT_FAILED_MONTHLY_LIMITS`, `RECIPIENT_OTHER_LIMITS_ERROR`, `SENDER_FAILED_MONTHLY_COMBINED_LIMIT`, `RECIPIENT_FAILED_MONTHLY_COMBINED_LIMIT`, `AMOUNT_EXCEEDED_BUSINESS_LIMIT`, `AMOUNT_EXCEEDED_P2P_SEND_WEEKLY_LIMIT`, `AMOUNT_EXCEEDED_P2P_SEND_MONTHLY_LIMIT`, `AMOUNT_EXCEEDED_SPONSOR_SET_P2P_SEND_MONTHLY_LIMIT`. **IDV:** `SENDER_DOCUMENT_IDV_SKIPPED`, `SENDER_ELECTRONIC_IDV_SKIPPED`, `RECIPIENT_DOCUMENT_IDV_SKIPPED`, `RECIPIENT_ELECTRONIC_IDV_SKIPPED`, `SENDER_IDV_ATTEMPTS_EXCEEDED`, `RECIPIENT_IDV_ATTEMPTS_EXCEEDED`. **Eligibility:** `SENDER_SUSPENDED`, `SENDER_DENYLISTED`, `RECIPIENT_SUSPENDED`, `RECIPIENT_DENYLISTED`, `SENDER_MONEY_MOVEMENT_BLOCK`, `RECIPIENT_MONEY_MOVEMENT_BLOCK`, `SENDER_OTHER_ELIGIBILITY_VIOLATION`, `RECIPIENT_OTHER_ELIGIBILITY_VIOLATION`. **Sponsorship:** `SENDER_SPONSORSHIP_AGE_GAP_RESTRICTION`, `RECIPIENT_SPONSORSHIP_AGE_GAP_RESTRICTION`, `SENDER_SPONSORSHIP_SUSPENDED`, `RECIPIENT_SPONSORSHIP_SUSPENDED`, `SENDER_SPONSORSHIP_PENDING`, `RECIPIENT_SPONSORSHIP_PENDING`, `SENDER_SPONSORSHIP_CANCELLED`, `RECIPIENT_SPONSORSHIP_CANCELLED`, `SENDER_RESTRICTED_SPONSORSHIP`, `RECIPIENT_RESTRICTED_SPONSORSHIP`, `DECLINED_BY_SENDER_SPONSOR`, `DECLINED_BY_RECIPIENT_SPONSOR`, `SENDER_NOT_IN_KID_ALLOWLIST`. **Risk/Scam:** `SCAM_WARNING_CHECK_CANCELED`, `SCAM_WARNING_CHECK_SKIPPED`, `POSSIBLE_UNKNOWN_PEER`, `NEW_POSSIBLE_UNKNOWN_PEER_OVER_LIMIT`, `POSSIBLE_UNKNOWN_PEER_W_UNVERIFIED`, `NEW_POSSIBLE_UNKNOWN_PEER_W_UNVERIFIED_OVER_LIMIT`, `RISKY_INVOLVING_MINOR`, `REFUNDED_BY_COMPLIANCE_CASE_REVIEW`, `FROZEN_BY_COMPLIANCE_CASE_REVIEW`. **MDP:** `SENDER_CANCELLED_ON_CONFIRM_RECIPIENT`, `SENDER_CONFIRM_RECIPIENT_PHONE_ATTEMPTS_EXCEEDED`. **Card/Instrument:** `PULL_MONEY_INVALID_INSTRUMENT`, `SENDER_CARD_DENYLISTED`, `RECIPIENT_CARD_DENYLISTED`, `SENDER_CARD_EXPIRED`, `DECLINED_INSTRUMENT_INCURS_ADDITIONAL_FEES`, `DECLINED_INVALID_USE_OF_CASH_CARD`, `PULL_MONEY_INSUFFICIENT_FUNDS`, `SENDER_EXCEEDED_CAPTURE_ATTEMPTS`. **Bill/Request:** `BILL_INITIATOR_RETRACT`, `BILL_GETTER_REFUSED`, `EXCEEDED_BILL_OUTSTANDING_LIMIT`, `REJECTED_BY_INCOMING_REQUEST_POLICY`, `DENIED_BY_SPAM_CHECK`, `DENIED_BY_HARASSMENT_CHECK`, `BILL_INITIATOR_ACCOUNT_CLOSED`, `BILL_GETTER_INVALID`. **Other:** `DUPLICATE_PAYMENT_CANCELLED`, `EXCEEDED_RETRY_EXPIRATION`, `RECIPIENT_P2P_TOGGLE_DISABLED`, `SENDER_P2P_TOGGLE_DISABLED`, `RECIPIENT_INVALID`, `CAPTURE_TRANSFER_FAILED`, `PAYOUT_TRANSFER_FAILED`, `PUSH_MONEY_FAILED`, `SENDER_CHARGEBACK`, `CLAWBACK`, `CROSS_BORDER_NOT_ALLOWED`, `SENDER_C4B_ONBOARDING_SUBFLOW`, `RECIPIENT_C4B_ONBOARDING_SUBFLOW`. 118 values in proto. | |
| 34 | RISK_ACTIONS | ARRAY | Y | | Risk actions taken. Elements: `{"type": "<action>", "causes": ["<cause>"]}`. Common types: `BLOCK`, `CREATE_COMPLIANCE_CASE_GAMBLING`, `CREATE_SCAM_ADVERSITY_RECIPIENT`, `SUSPEND_RECIPIENT_FOR_ENHANCED_VERIFICATION`. Common causes: `BY_RISK_SCAM_RULE`, `BY_RISK_RULE`, `BY_COMPLIANCE_RULE`, `BY_PRODUCT_POLICY_RULE`. | |
| 35 | ELIGIBILITY_VIOLATIONS | ARRAY | Y | | Eligibility violations. Elements: `{"violation_name": "<name>", "metadata": [...]}`. Common names: `CUSTOMER_DENYLISTED`, `GUARDRAILS_ADVERSITY_BLOCKED_ACTION_REQUIREMENT` (metadata: `DENYLIST`, `INAUTHENTIC_ACCOUNT_SUSPENSION`, `SCAM_SUSPENSION`), `GRADUATION_JOURNEY_ERROR_NOTIFICATIONS`, `ACCOUNT_CLOSED`, `MONEY_MOVEMENT_BLOCK`, `P2P_CONTROLS_BLOCKER`. | |
| 36 | ELIGIBILITY_VIOLATION_SOURCE | TEXT | Y | | Which side caused the violation | **Enum:** `SENDER`, `RECIPIENT` |
| 37 | REFUND_REQUESTED_AT | TIMESTAMP | Y | | When a refund was requested | |
| 38 | REFUND_REASON | TEXT | Y | | Reason for refund. Stored without the `REFUND_REASON_` prefix. | **Enum:** `SCAM_REPORT`, `SENDER_NOT_AUTHORIZED`, `WRONG_RECIPIENT`, `PURCHASE_CANCELLED`, `PURCHASE_RETURNED`, `DID_NOT_RECEIVE`, `NOT_AS_DESCRIBED`, `WRONG_AMOUNT`, `PURCHASE_RETURNED_OR_CANCELLED`, `SOMETHING_ELSE`, `RECIPIENT_INITIATED`, `MANUAL_REFUND_FROM_RECIPIENT`, `MANUAL_REFUND_FROM_SQUARE`, `SENDER_CHARGEBACK` |
| 39 | REFUNDED_AT | TIMESTAMP | Y | | When the refund completed | |
| 40 | REFUND_DEPOSITED_AT | TIMESTAMP | Y | | When refund funds were deposited back | |
| 41 | REFUNDED_TO_BALANCE | BOOLEAN | Y | | Whether refund went to Cash balance | `true`, `false` |
| 42 | REFUND_FAILURE_REASON_CODE | TEXT | Y | | Why a refund failed. Uses `PaymentReversalFailureReasonCode` proto values. | **Enum:** `REVERSE_CAPTURE_OTHER_FAILURE`, `REVERSE_PAYOUT_INSUFFICIENT_FUNDS`, `REVERSE_PAYOUT_OTHER_FAILURE`, `REFUNDER_DENYLISTED`, `REFUNDEE_DENYLISTED`, `REFUNDEE_SUSPENDED`, `REFUNDER_SUSPENDED`, `REFUNDER_MONEY_MOVEMENT_BLOCK`, `REFUNDEE_MONEY_MOVEMENT_BLOCK`, `REFUNDEE_OTHER_ELIGIBILITY_VIOLATION`, `REFUNDER_OTHER_ELIGIBILITY_VIOLATION` |
| 43 | REFUND_INSTRUMENT | OBJECT | Y | | Instrument used for refund | |
| 43a | .token | TEXT | | | Instrument token | `B$_C_seddb0ydz` |
| 43b | .type | TEXT | | | Instrument type | `PAYMENT_INSTRUMENT_TYPE_STORED_VALUE` |
| 43c | .cardInfo | OBJECT | | | Card BIN/suffix if refunded to card | |
| 43d | .fidelius_token | TEXT | | | Fidelius token | |
| 43e | .payment_account_reference | TEXT | | | Payment account reference | |
| 43f | .apple_pay_payment_token | TEXT | | | Apple Pay token | |
| 43g | .google_pay_payment_token | TEXT | | | Google Pay token | |
| 44 | REFUND_REQUEST_REASON | TEXT | Y | | Reason given when requesting a refund (same `RefundReason` proto as REFUND_REASON). In practice, only customer-facing reasons: | **Enum:** `WRONG_RECIPIENT`, `WRONG_AMOUNT`, `NOT_AS_DESCRIBED`, `DID_NOT_RECEIVE`, `PURCHASE_RETURNED_OR_CANCELLED`, `SOMETHING_ELSE` |
| 45 | REFUND_REQUEST_DECLINED_AT | TIMESTAMP | Y | | When a refund request was declined | |
| 46 | REFUND_REQUEST_EXPIRES_AT | TIMESTAMP | Y | | When the refund request expires | |
| 47 | REFUND_REQUEST_APPROVED_AT | TIMESTAMP | Y | | When the refund request was approved | |
| 48 | CANCELLATION_REQUESTED_AT | TIMESTAMP | Y | | When cancellation was requested | |
| 49 | CANCELLATION_REASON | TEXT | Y | | Reason for cancellation. Stored without the `CANCELLATION_REASON_` prefix. | **Enum:** `SENDER_CANCELED`, `RECIPIENT_DECLINED`, `MANUAL_CANCELED`, `ABUSE_REPORTED_ON_SENDER`, `ABUSE_REPORTED_ON_RECIPIENT`, `MANUAL_REIMBURSED`, `EXPIRED_WAITING_ON_SENDER`, `EXPIRED_WAITING_ON_RECIPIENT`, `EXPIRED_WAITING_ON_SPONSOR`, `EXPIRED_WAITING_ON_INTERNAL`, `EXPIRED_RETRY_INTENT`, `SENDER_CHARGEBACK_REPORTED`, `BILL_GETTER_REFUSED`, `BILL_INITIATOR_RETRACTED`, `SENDER_SPONSORSHIP_CANCELLED`, `SENDER_SPONSORSHIP_SUSPENDED`, `RECIPIENT_SPONSORSHIP_CANCELLED`, `RECIPIENT_SPONSORSHIP_SUSPENDED`, `RECIPIENT_BLOCKED_FROM_SENDER_BY_SPONSOR`, `SENDER_BLOCKED_FROM_RECIPIENT_BY_SPONSOR`, `RECIPIENT_P2P_TOGGLE_DISABLED`, `SENDER_P2P_TOGGLE_DISABLED`, `POOL_CLOSED`, `SENDER_DENYLISTED`, `RECIPIENT_DENYLISTED` |
| 50 | CANCELLED_AT | TIMESTAMP | Y | | When the payment was cancelled | |
| 51 | CANCEL_FAILURE_REASON_CODE | TEXT | Y | | Why a cancellation failed (no values observed) | |
| 52 | IS_SUSPECTED_SCAM | BOOLEAN | N | | Whether flagged as potential scam | `true`, `false` |
| 53 | IS_SUSPECTED_MISDIRECTED | BOOLEAN | N | | Whether flagged as possibly sent to wrong person | `true`, `false` |
| 54 | SOURCE_INSTRUMENT | OBJECT | Y | | Sender's instrument. Sub-fields: `token`, `type`, `cardInfo` (`bin`/`suffix`), `fidelius_token`, `payment_account_reference`, `apple_pay_payment_token`, `google_pay_payment_token`. | `{"type": "PAYMENT_INSTRUMENT_TYPE_DEBIT_CARD", "token": "55318d...", "cardInfo": {"bin": "434769", "suffix": "6166"}}` |
| 55 | RECIPIENT_INSTRUMENT | OBJECT | Y | | Recipient's instrument. Same sub-fields as SOURCE_INSTRUMENT. | `{"type": "PAYMENT_INSTRUMENT_TYPE_STORED_VALUE", "token": "B$_C_s92tw0yy3"}` |
| 56 | REQUEST_REFUND_AVAILABLE_UNTIL | TIMESTAMP | Y | | Deadline for requesting a refund (30 days after payout) | `2025-08-14T15:18:59.180` |
| 57 | DEPOSIT_PREFERENCE | TEXT | Y | | **Deprecated in proto.** Recipient's deposit preference. Always null for new payments. | `RETAIN_FUNDS_IN_CASH_BALANCE` |
| 58 | ORIENTATION | TEXT | N | | `CASH` = initiated by sender ("send"). `BILL` = initiated by recipient ("request"). | **Enum:** `CASH`, `BILL` |
| 59 | PULL_TRANSFER_ID | TEXT | Y | `MONEY_MOVER_TRANSACTIONS` (as `FLOW_TOKEN`) | Transfer ID for pulling funds from sender | `ST$_PE_yh338b3bae7xh677te3px0-0000` |
| 60 | PUSH_TRANSFER_ID | TEXT | Y | `MONEY_MOVER_TRANSACTIONS` (as `FLOW_TOKEN`) | Transfer ID for pushing funds to recipient | `ST$_PE_3mty25yng6e3tapwkz7f43-0001` |
| 61 | DISPLAY_ID | TEXT | N | | Human-readable display ID | `D-ZM5PVZV5` |
| 62 | REIMBURSEMENT_INFO | OBJECT | Y | | Reimbursement info (always null in recent data) | |
| 63 | SENDER_REGION | TEXT | Y | | Sender's region | `USA` |
| 64 | SENDER_RATE_PLAN | TEXT | Y | | Sender's rate plan | **Enum:** `UNDECIDED_DEFERRED`, `PERSONAL` |
| 65 | IS_CROSS_BORDER | BOOLEAN | N | | Whether the payment is cross-border | `true`, `false` |
| 66 | RECIPIENT_REGION | TEXT | Y | | Recipient's region (always null in recent data) | |
| 67 | EXPLICIT_SCAM_CONFIRMATION | BOOLEAN | N | | Whether sender confirmed "not a scam" | `true`, `false` |
| 68 | EXPLICIT_MISDIRECTED_PAYMENT_CONFIRMATION | BOOLEAN | N | | Whether sender confirmed correct recipient | `true`, `false` |
| 69 | EXPLICIT_SCAM_CONFIRMATION_AT | TIMESTAMP | Y | | When scam confirmation was made | |
| 70 | EXPLICIT_MISDIRECTED_PAYMENT_CONFIRMATION_AT | TIMESTAMP | Y | | When MDP confirmation was made | |
| 71 | BROWSER_INTERACTION_TOKEN | TEXT | Y | | Token for fraud detection | `urn:bi-token:v1:ac49ba7017463514...` |
| 72 | CHARGEBACK_REPORTED_AT | TIMESTAMP | Y | | When a chargeback was reported | |
| 73 | CHARGEBACK_REASON_CODE | TEXT | Y | | Card network chargeback reason code (46 values) | **Top 10:** `4837`, `4853`, `4863`, `4871`, `4834`, `A1`, `A3`, `A5`, `S01`, `13.1` |
| 74 | CHARGEBACK_FRAUD | BOOLEAN | Y | | Whether chargeback is fraud-related | `false` |
| 75 | CHARGEBACK_DECISION | TEXT | Y | | How the chargeback was handled | **Enum:** `ACCEPT`, `CHALLENGE`, `IGNORE` |
| 76 | CHARGEBACK_RESOLUTION | TEXT | Y | | Final chargeback outcome | **Enum:** `WON`, `LOST`, `LOST_NO_RECOURSE` |
| 77 | CLAWBACK_AMOUNT_CENTS | NUMBER | Y | | Amount clawed back in cents | |
| 78 | CLAWBACK_AMOUNT_CURRENCY_CODE | TEXT | Y | | Clawback currency | `USD` |
| 79 | CLAWBACK_SOURCE | TEXT | Y | | Where clawback funds came from. Note: proto's `UNSPECIFIED` maps to `RECIPIENT_UNSPECIFIED`. | **Enum:** `RECIPIENT_INSTRUMENT`, `RECIPIENT_BALANCE`, `SENDER_BALANCE` |
| 80 | CLAWBACK_RECLAIM_PULL_DATA | OBJECT | Y | | Clawback pull transaction details | |
| 81 | CLAWED_BACK_AT | TIMESTAMP | Y | | When the clawback occurred | |
| 82 | PAYMENT_INITIATOR_APP_TOKEN | TEXT | Y | | Token of the app that initiated the payment | `cc9c0be9c7a30a39d74af12f45c7b31df689ae16` |
| 83 | RECIPIENT_RATE_PLAN | TEXT | Y | | Recipient's rate plan | **Enum:** `UNDECIDED_DEFERRED`, `PERSONAL` |
| 84 | PULL_ADJUSTMENTS | ARRAY | N | | Fee adjustments on the pull (sender-side). Usually empty. | `[{"amount": {"amount": 150, "currency_code": "USD"}, "fee_type": "FEE_TYPE_CREDIT_CARD"}]` |
| 85 | PUSH_ADJUSTMENTS | ARRAY | N | | Fee adjustments on the push (recipient-side). Usually empty. | `[{"amount": {"amount": 36, "currency_code": "USD"}, "fee_type": "FEE_TYPE_BUSINESS"}]` |
| 86 | SENDER_FIRST_SELECTED_FUNDING_INSTRUMENT_AT | TIMESTAMP | Y | | When sender first selected their funding instrument | `2025-07-15T15:18:54.659` |
| 87 | DESIGNATED_PVT_PUBLISHER | TEXT | Y | | Designated PVT publisher | `P2P_ENGINE` |
| 88 | SENDER_SPONSOR_APPROVAL | TEXT | Y | | Sender's sponsor approval status (teen/family accounts) | **Enum:** `NOT_REQUIRED`, `APPROVED`, `DECLINED`, `EXPIRED`, `VOIDED` |
| 89 | RECIPIENT_SPONSOR_APPROVAL | TEXT | Y | | Recipient's sponsor approval status | **Enum:** `NOT_REQUIRED`, `APPROVED`, `DECLINED`, `EXPIRED`, `VOIDED` |
| 90 | PAYMENT_WORKFLOW_STATE_CODE | TEXT | N | | High-level workflow state (not same as PAYMENT_STATE_CODE) | **Enum:** `CREATED`, `COMPLETED`, `HURDLE_ENCOUNTERED`, `IN_PROGRESS`, `CANCELED`, `FAILED`, `RETRYABLE_ERROR`, `RUNNING` |
| 91 | PAYMENT_VERSION | NUMBER | N | | Version counter for the payment entity | `50` |
| 92 | CURRENT_WORKFLOW_TYPE | TEXT | N | | Current workflow type | **Enum:** `SEND`, `REQUEST`, `REFUND`, `CANCEL`, `CLAWBACK`, `REIMBURSE`, `FREEZE` |
| 93 | SEQUENCE | NUMBER | N | | Event sequence number | `50` |
| 94 | CLIENT_REQUEST_CONTEXT | OBJECT | N | | Originating client request context. Sub-fields: `triggered_by_customer_token`, `request_source` (`REQUEST_SOURCE_BRAND_B`, `REQUEST_SOURCE_INTERNAL_API`, `REQUEST_SOURCE_BACKGROUND_JOB`, `REQUEST_SOURCE_BACKFILL`), `retry_context` (sub-fields: `created_at` epoch ms, `retry_attempt` starting at 1, `is_foreground` bool for user-initiated vs app-scheduled retry). | `{"request_source": "REQUEST_SOURCE_BRAND_B", "triggered_by_customer_token": "C_g9ed1qm67"}` |
| 95 | LIMITS_RESERVATION_SEQUENCE | NUMBER | Y | | Incremented each time something materially relevant to limits changes (e.g., changing funding instrument triggers releasing old limits and reserving new ones) | `1` |
| 96 | INITIAL_RISK_EVALUATION_FLAGS | ARRAY | N | | Risk flags from initial risk check (TD_112). Complete enum from proto: | **All flags:** `PAYMENT_RISK_FLAG_AUTHENTICATE_VIA_PASSCODE`, `PAYMENT_RISK_FLAG_BLOCK`, `PAYMENT_RISK_FLAG_BLOCK_NEW_POSSIBLE_UNKNOWN_PEER_OVER_LIMIT`, `PAYMENT_RISK_FLAG_BLOCK_NEW_POSSIBLE_UNKNOWN_PEER_OVER_LIMIT_W_UNVERIFIED`, `PAYMENT_RISK_FLAG_BLOCK_POSSIBLE_UNKNOWN_PEER`, `PAYMENT_RISK_FLAG_BLOCK_POSSIBLE_UNKNOWN_PEER_W_UNVERIFIED`, `PAYMENT_RISK_FLAG_BLOCK_RISKY_INVOLVING_MINOR`, `PAYMENT_RISK_FLAG_ISSUE_MISDIRECTED_WARNING`, `PAYMENT_RISK_FLAG_ISSUE_SCAM_WARNING`, `PAYMENT_RISK_FLAG_ISSUE_SENDER_2FA_WARNING`, `PAYMENT_RISK_FLAG_ISSUE_SENDER_MISDIRECTED_WARNING`, `PAYMENT_RISK_FLAG_MARK_RECIPIENT_EXCEEDED_VELOCITY_LIMIT`, `PAYMENT_RISK_FLAG_MARK_SENDER_EXCEEDED_VELOCITY_LIMIT`, `PAYMENT_RISK_FLAG_REFUND_TO_ORIGINAL_INSTRUMENT`, `PAYMENT_RISK_FLAG_REQUIRE_RECIPIENT_IDV`, `PAYMENT_RISK_FLAG_REQUIRE_SENDER_IDV`, `PAYMENT_RISK_FLAG_REQUIRE_SPONSOR_APPROVAL`, `PAYMENT_RISK_FLAG_WAIT_FOR_COMPLIANCE_CASE_REVIEW` |
| 97 | ETL_ROW_HASH | TEXT | N | | Hash for ETL deduplication | |
| 98 | ETL_CREATED_AT | TIMESTAMP | N | | When the row was first loaded by ETL | |
| 99 | ETL_UPDATED_AT | TIMESTAMP | N | | When the row was last updated by ETL | |
| 100 | SENDER_CONFIRMED_RECIPIENT_AT | TIMESTAMP | Y | | When sender confirmed recipient identity | |
| 101 | REGISTRAR_EVENT_PUBLISHER | TEXT | Y | | Publisher for registrar events | `P2P_ENGINE_FLINK_APP` |
| 102 | LIMITS_EVENT_PUBLISHER | TEXT | Y | | Publisher for limits events | `P2P_ENGINE` |
| 103 | MONEY_MOVEMENT_EVENT_PUBLISHER | TEXT | Y | | Publisher for money movement events | **Enum:** `P2P_ENGINE`, `P2P_ENGINE_FLINK_APP` |
| 104 | DISABLE_RECIPIENT_MDP_BLOCKER_EXPERIMENT_COHORT | TEXT | Y | | Denormalized experiment cohort (prefer PAYMENT_EXPERIMENT_COHORTS) | **Enum:** `TREATMENT`, `CONTROL` |
| 105 | CONSOLIDATED_SENDER_SIDE_MDP_EXPERIMENT_COHORT | TEXT | Y | | Denormalized experiment cohort (prefer PAYMENT_EXPERIMENT_COHORTS) | **Enum:** `TREATMENT`, `CONTROL`, `UNASSIGNED` |
| 106 | MULTIPLE_CAPTURES_EXPERIMENT_COHORT | TEXT | Y | | Denormalized experiment cohort (prefer PAYMENT_EXPERIMENT_COHORTS) | `UNASSIGNED` |
| 107 | DESIGNATED_EVENT_PUBLISHERS | OBJECT | Y | | Map of designated publishers. Keys: `registrar_event_publisher`, `limits_event_publisher`, `money_movement_event_publisher`, `snowflake_event_publisher`, `encrypted_snowflake_event_publisher`. Values: `DESIGNATED_EVENT_PUBLISHER_P2P_ENGINE` or `DESIGNATED_EVENT_PUBLISHER_P2P_ENGINE_FLINK_APP`. | |

## Querying Hurdles

The `HURDLES` column is an ARRAY of objects. Each object contains one key per possible hurdle type. The active hurdle
has a non-null value (an object like `{"_exists_": true}` or with additional data); all other keys are set to JSON
`null`.

### Extracting hurdle type with LATERAL FLATTEN

Use a double `LATERAL FLATTEN` to dynamically extract the active hurdle key and its payload. This avoids brittle CASE
blocks and automatically picks up new hurdle types without code changes:

```sql
SELECT payment_id, k.key AS hurdle_type, k.value AS hurdle_payload
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE,
LATERAL FLATTEN(input => HURDLES) f,
LATERAL FLATTEN(input => f.value) k
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND ARRAY_SIZE(HURDLES) > 0
  AND NOT IS_NULL_VALUE(k.value)
```

- `f` flattens the HURDLES array (one row per hurdle object)
- `k` flattens each hurdle object's keys (one row per key)
- `NOT IS_NULL_VALUE(k.value)` filters to only the active hurdle key

**Important:** Use `NOT IS_NULL_VALUE(k.value)` — not `IS NOT NULL` — because the inactive keys are present but set
to JSON `null`.

### Enriching specific hurdle types

When you need sub-field detail for certain hurdle types, use a small CASE on `k.key` to enrich the label. Always
break down eligibility violations by `violation_name` and passcode hurdles by `force_require`:

```sql
CASE
  WHEN k.key IN ('sender_eligibility_violation_hurdle', 'recipient_eligibility_violation_hurdle')
    THEN k.key || ':' || COALESCE(k.value:violation_name::STRING, 'UNKNOWN')
  WHEN k.key = 'passcode_required_hurdle'
    THEN k.key || ':force_require=' || COALESCE(k.value:force_require::STRING, 'null')
  ELSE k.key
END AS hurdle_type
```

### Counting hurdle types

```sql
SELECT k.key AS hurdle_type, COUNT(*) AS cnt
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE,
LATERAL FLATTEN(input => HURDLES) f,
LATERAL FLATTEN(input => f.value) k
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND ARRAY_SIZE(HURDLES) > 0
  AND NOT IS_NULL_VALUE(k.value)
GROUP BY hurdle_type
ORDER BY cnt DESC
```

### Finding payments with a specific hurdle

When you need to filter for a specific known hurdle type, use `IS_NULL_VALUE` directly on the key:

```sql
SELECT payment_id
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND ARRAY_SIZE(hurdles) > 0
  AND NOT IS_NULL_VALUE(hurdles[0]:sender_insufficient_funds_hurdle)
```

Bracket syntax also works: `hurdles[0]['sender_suspected_misdirected_payment_hurdle']`.

### Extracting sub-fields from a hurdle

```sql
hurdles[0]:sender_eligibility_violation_hurdle:violation_name::STRING
hurdles[0]:sender_suspected_misdirected_payment_hurdle:risk_flags
```

Or via the flatten approach: `k.value:violation_name::STRING`, `k.value:risk_flags`.

### Known hurdle types

Complete list from `PaymentHurdle` proto oneof (proto source:
`p2p-engine/proto/src/main/proto/example/app/p2p/engine/api/v1/payment_hurdle.proto`):

`sender_idv_document_hurdle`, `sender_idv_electronic_hurdle`, `passcode_required_hurdle` (sub-field:
`force_require` bool), `scam_warning_hurdle`, `recipient_idv_document_hurdle`, `recipient_idv_electronic_hurdle`,
`recipient_misdirected_payment_hurdle`, `sender_insufficient_funds_hurdle` (sub-fields: `idempotence_token`,
`credit_card_fee_amount`), `duplicate_payment_hurdle` (sub-field: `duplicate_payment_display_ids` array),
`sender_eligibility_violation_hurdle` (sub-fields: `violation_name`, `metadata` array),
`recipient_eligibility_violation_hurdle` (sub-fields: `violation_name`, `metadata` array),
`sender_payment_request_select_funding_instrument_hurdle`,
`internal_review_of_sender_idv_documents_hurdle` (sub-field: `token`),
`internal_review_of_recipient_idv_documents_hurdle` (sub-field: `token`),
`sender_sponsor_approval_required_hurdle`, `recipient_sponsor_approval_required_hurdle`,
`response_to_senders_sponsorship_request_hurdle` (sub-field: `token`),
`response_to_recipients_sponsorship_request_hurdle` (sub-field: `token`),
`bill_getter_confirmation_hurdle` (sub-field: `contact_relation_unavailable` bool),
`additional_authentication_required_hurdle` (3DS subflow for debit cash-in via Moneta),
`instrument_access_verification_required_hurdle` (sub-fields: `instrument_token`, `idempotence_token`),
`sender_card_expired_hurdle` (sub-field: `idempotence_token`),
`sender_suspected_misdirected_payment_hurdle` (sub-field: `risk_flags` array -- specifically
`PAYMENT_RISK_FLAG_ISSUE_SENDER_2FA_WARNING` or `PAYMENT_RISK_FLAG_ISSUE_SENDER_MISDIRECTED_WARNING`),
`recipient_claim_payment_hurdle`.

Deprecated (may appear in old data): `exchange_quote_acceptance_hurdle`, `sender_c4b_auto_downgraded_hurdle`,
`recipient_c4b_auto_downgraded_hurdle`.

## Querying Experiment Cohorts

`PAYMENT_EXPERIMENT_COHORTS` is an OBJECT with one key per experiment. Values come from the `BasicExperimentCohort`
proto enum: `BASIC_EXPERIMENT_COHORT_TREATMENT`, `BASIC_EXPERIMENT_COHORT_CONTROL`,
`BASIC_EXPERIMENT_COHORT_UNASSIGNED`, or null.

Known experiment keys (as of 2025-08): `consolidated_sender_side_mdp_experiment_cohort`,
`dag_v2_experiment_cohort`, `disable_recipient_mdp_blocker_experiment_cohort`,
`draft_payment_expiration_extension_experiment_cohort`, `multiple_captures_experiment_cohort`,
`resumable_payments_experiment_cohort`.

Filter by experiment cohort:

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND PAYMENT_EXPERIMENT_COHORTS:multiple_captures_experiment_cohort::STRING = 'BASIC_EXPERIMENT_COHORT_TREATMENT'
```

Compare treatment vs control:

```sql
SELECT
  PAYMENT_EXPERIMENT_COHORTS:multiple_captures_experiment_cohort::STRING AS cohort,
  COUNT(*) AS total,
  SUM(CASE WHEN PAYMENT_STATE_CODE = 'PAID_OUT' THEN 1 ELSE 0 END) AS paid_out,
  SUM(CASE WHEN PAYMENT_STATE_CODE = 'FAILED' THEN 1 ELSE 0 END) AS failed
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND PAYMENT_EXPERIMENT_COHORTS:multiple_captures_experiment_cohort IS NOT NULL
GROUP BY cohort
```

There are also top-level denormalized experiment cohort columns for older experiments (columns 104-106). For newer
experiments, use `PAYMENT_EXPERIMENT_COHORTS` instead.

## Common Query Patterns

### Getting the last event per payment (on the events table)

Use `QUALIFY ROW_NUMBER()` to get the most recent event for each payment:

```sql
SELECT *
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND payment_id = 'P2PE_FIAT_...'
QUALIFY ROW_NUMBER() OVER (PARTITION BY payment_id ORDER BY sequence DESC) = 1
```

### Joining events table with latest-event table

Use the events table to find payments that hit a specific hurdle or state, then join to the latest-event table for
the final outcome. **Always mirror the `CREATED_AT` filter on both tables** to leverage clustering:

```sql
WITH payments_with_hurdle AS (
  SELECT DISTINCT payment_id
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    AND ARRAY_SIZE(hurdles) > 0
    AND NOT IS_NULL_VALUE(hurdles[0]:sender_insufficient_funds_hurdle)
)
SELECT le.payment_state_code, COUNT(*) AS c
FROM payments_with_hurdle ph
JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE le
  ON le.payment_id = ph.payment_id
WHERE le.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY le.payment_state_code
ORDER BY c DESC
```

### Detecting retry payments

Match retries by sender + recipient + amount with a time window:

```sql
SELECT original.PAYMENT_ID, retry.PAYMENT_ID AS retry_payment_id
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE original
LEFT JOIN YOUR_DB.YOUR_SCHEMA.YOUR_TABLE retry
  ON original.SENDER_TOKEN = retry.SENDER_TOKEN
  AND original.RECIPIENT_CUSTOMER_TOKEN = retry.RECIPIENT_CUSTOMER_TOKEN
  AND original.PAYMENT_VALUE_AMOUNT_CENTS = retry.PAYMENT_VALUE_AMOUNT_CENTS
  AND retry.CREATED_AT > original.CREATED_AT
  AND retry.CREATED_AT <= DATEADD(hour, 24, original.CREATED_AT)
  AND retry.PAYMENT_STATE_CODE = 'PAID_OUT'
WHERE original.CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND original.PAYMENT_STATE_CODE = 'FAILED'
```

To detect offline/queued retries via `client_request_context`:

```sql
NOT IS_NULL_VALUE(client_request_context:retry_context:retry_attempt)
```

### Classifying payment outcomes

Use `COALESCE` to produce a single outcome column that captures the most specific failure reason:

```sql
COALESCE(cancellation_reason, failure_reason_code, payment_state_code) AS outcome
```

### Counting P2P actives

Count distinct customers who participated in a successful P2P payment over a date range:

```sql
WITH senders AS (
  SELECT sender_token AS customer_token
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE CREATED_AT BETWEEN '2025-10-01' AND '2025-11-01'
    AND payment_state_code = 'PAID_OUT'
),
recipients AS (
  SELECT recipient_customer_token AS customer_token
  FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
  WHERE CREATED_AT BETWEEN '2025-10-01' AND '2025-11-01'
    AND payment_state_code = 'PAID_OUT'
)
SELECT COUNT(DISTINCT customer_token)
FROM (
  SELECT customer_token FROM senders
  UNION
  SELECT customer_token FROM recipients
)
```

### Filtering by instrument type

```sql
SOURCE_INSTRUMENT:type = 'PAYMENT_INSTRUMENT_TYPE_DEBIT_CARD'
SOURCE_INSTRUMENT:type IN ('PAYMENT_INSTRUMENT_TYPE_DEBIT_CARD', 'PAYMENT_INSTRUMENT_TYPE_CREDIT_CARD')
```

### Checking risk flags

```sql
ARRAY_CONTAINS('PAYMENT_RISK_FLAG_ISSUE_SCAM_WARNING'::variant, initial_risk_evaluation_flags)
```

### Detecting foreground vs background retries

```sql
SELECT
  payment_id,
  client_request_context:retry_context:retry_attempt::INT AS retry_attempt,
  client_request_context:retry_context:is_foreground::BOOLEAN AS is_foreground
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND NOT IS_NULL_VALUE(client_request_context:retry_context:retry_attempt)
```

## Data Pipeline

These tables are populated by `PaymentSummaryEvent` protos published from p2p-engine to Kafka, then ingested into
Snowflake via an ETL pipeline. Understanding the pipeline helps explain column naming, JSON structure, and which
fields come from the `Payment` proto vs the `PaymentSummaryEvent` wrapper.

### Event flow

1. p2p-engine persists a `PaymentStateTransitionEvent` (contains `from` and `to` `PaymentStateEvent`, each wrapping
   a full `Payment` proto plus workflow state, sequence, client request context, limits reservation sequence)
2. `PaymentStateTransitionToPaymentSummaryEventHandler` consumes these transitions, filters to payments where
   `designatedEventPublishers.snowflakeEventPublisher == P2P_ENGINE`, and publishes only when the payment is new or
   `paymentState` changed (not on every version bump)
3. The handler builds a `PaymentSummaryEvent` proto (~35 fields) from the `Payment` proto (~62 fields)
4. The ETL pipeline (Flink or direct ingestion) denormalizes the `PaymentSummaryEvent` + the full `Payment` proto
   into the flat 107-column Snowflake table

### Why hurdles use IS_NULL_VALUE

The `HURDLES` column is serialized from the proto's `PaymentHurdle` message, which uses a `oneof`. In the proto,
only one hurdle field is set at a time. When serialized to JSON for Snowflake, all oneof keys are present in the
object but inactive ones are set to JSON `null`. This is why `NOT IS_NULL_VALUE(k.value)` is required instead of
`IS NOT NULL` -- the keys exist, they just have null values.

### Key source files in cash-server

Proto definitions:
- `p2p-engine/proto/src/main/proto/example/app/p2p/engine/api/v1/common.proto` -- `Payment` message, all major
  enums (`PaymentStateCode`, `PaymentFailureReasonCode`, `CancellationReason`, `RefundReason`, `CreationMechanism`,
  `PaymentType`, `Orientation`, `ClawbackSource`, `FeeType`, `PaymentWorkflowStateCode`, `PaymentWorkflowType`,
  `EligibilityViolationSource`, `PaymentReversalFailureReasonCode`)
- `p2p-engine/proto/src/main/proto/example/app/p2p/engine/api/v1/payment_hurdle.proto` -- `PaymentHurdle` oneof
  and all individual hurdle messages with their sub-fields
- `p2p-engine/proto/src/main/proto/example/app/p2p/engine/api/v1/payment_risk_flag.proto` -- `PaymentRiskFlag`
  enum (18 values)
- `p2p-engine/proto/src/main/proto/example/app/p2p/engine/api/v1/payment_experiment_cohort.proto` --
  `PaymentExperimentCohorts` message and `BasicExperimentCohort` enum
- `p2p-engine/proto/src/main/proto/example/app/p2p/engine/event/v1/payment_summary_event.proto` -- the
  `PaymentSummaryEvent` proto that is published to Kafka for Snowflake ingestion

Event publishing:
- `p2p-engine/service/src/main/kotlin/com/example/app/p2p/engine/transport/event/kafka/handler/PaymentStateTransitionToPaymentSummaryEventHandler.kt`
  -- transforms `PaymentStateTransitionEvent` into `PaymentSummaryEvent`, controls when events are published
  (only on state code changes or new payments, only when designated publisher is `P2P_ENGINE`)
- `p2p-engine/service/src/main/kotlin/com/example/app/p2p/engine/transport/event/kafka/handler/FranklinFailureReasonExtensions.kt`
  -- maps `PaymentFailureReasonCode` to legacy Franklin failure reasons (populates `payment_summary_legacy` field)
