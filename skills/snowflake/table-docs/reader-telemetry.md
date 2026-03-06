# Query Reader Telemetry

Query card reader state machine telemetry uploaded by the Android CDX `StateLogger`.

## Table

### YOUR_EVENT_SCHEMA.CATALOGS.READER_TELEMETRY

One row per telemetry event emitted from the Hardware Register Android app for a card reader interaction.
Includes state transitions and state timeouts from CDX workflow state machines logged via `StateLogger`,
plus payment timing, connection info, and device context.

**Clustering key:** `U_RECORDED_DATE`. Always filter on this to avoid full table scans.

---

## Key Columns for CDX Oncall

### Identity / Filtering

| Column | Description | Example |
|--------|-------------|---------|
| `SUBJECT_LOCATION_ID` | Unit token (merchant/device) — **preferred filter for oncall investigations** | `'ABC12DEFG3H4J'` |
| `SUBJECT_CUSTOMER_ID` | Merchant token — broader than unit token | `'XY98ABCD2EF1G'` |
| `SUBJECT_USER_TOKEN` | User token (individual user) | `'ABC12DEFG3H4J'` |
| `HW_SERIAL_NUMBER` | Card reader serial number — use when investigating a specific reader | `'SN1234567890'` |
| `HW_LOCATION_ID` | Unit token scoped to the HW event context | same as `SUBJECT_LOCATION_ID` in practice |

### Event

| Column | Description | Example |
|--------|-------------|---------|
| `HW_EVENT_NAME` | Human-readable event name. StateLogger writes `'Workflow: State Transition'` and `'Workflow: State Timeout'`. | `'Workflow: State Timeout'` |
| `HW_EVENT_TYPE` | Programmatic event type key | |
| `HW_EVENT_PARAMETERS` | Structured parameters for the event (may overlap with `READER_TELEMETRY_DATA_RAWDATA`) | |
| `READER_TELEMETRY_DATA_RAWDATA` | Raw JSON payload from `StateLogger` — the primary field for state machine analysis. Contains `workflow`, `oldState`, `newState`, `connectionType`, `readerIdentifier`, `connectionId`. | See below |

### Reader Hardware

| Column | Description | Example |
|--------|-------------|---------|
| `HW_READER_TYPE_KEY` | Type identifier for the reader | `'magstripe'`, `'contactless_and_chip'` |
| `HW_FIRMWARE_VERSION` | Reader firmware version | `'1.2.3'` |
| `HW_FIRMWARE_BUILD_NUMBER` | Firmware build number | |
| `HW_CONNECTION_TYPE` | Connection type | `'ble'`, `'usb'` |
| `HW_CONNECTION_ID` | Connection session ID — groups events belonging to the same connection attempt | `1`, `2` |
| `HW_STAND_MLB_SERIAL_NUMBER` | Stand serial number (if reader is docked) | |
| `HW_STAND_MODEL_NUMBER` | Stand model | |

### Diagnostics

| Column | Description | Example |
|--------|-------------|---------|
| `READER_TELEMETRY_ERROR_DESCRIPTION` | Error description when present | |
| `READER_TELEMETRY_ERROR_BEFORE_CONNECTION` | Whether the error occurred before connection established | `true`, `false` |
| `READER_TELEMETRY_SECONDS_SINCE_LAST_LCR_COMMUNICATION` | Seconds since last successful LCR communication — useful for LCR initialization issues | `30`, `120` |
| `READER_TELEMETRY_CHARGE_PERCENT` | Reader battery level | `85` |
| `READER_TELEMETRY_IS_CHARGING` | Whether reader is charging | `true`, `false` |
| `READER_TELEMETRY_APP_IN_BACKGROUND` | Whether the app was backgrounded when the event occurred | `true`, `false` |

### Payment Timing (non-StateLogger events)

| Column | Description |
|--------|-------------|
| `READER_TELEMETRY_PAYMENT_TIMING_APPSEL` | App selection timing (EMV) |
| `READER_TELEMETRY_PAYMENT_TIMING_ARPC` | ARPC timing |
| `READER_TELEMETRY_PAYMENT_TIMING_ARQC` | ARQC timing |
| `READER_TELEMETRY_PAYMENT_TIMING_CARD_PRESENT` | Card present detection timing |
| `READER_TELEMETRY_PAYMENT_TIMING_COMPLETE` | Full payment completion timing |
| `READER_TELEMETRY_PAYMENT_TIMING_RAWDATA` | Raw timing data |
| `READER_TELEMETRY_CARD_ENTRY_METHOD` | How the card was entered |
| `READER_TELEMETRY_PAYMENT_SERVER_ID` | Payment server ID |
| `READER_TELEMETRY_SERVER_TENDER_ID` | Tender ID |

### Android Device (the POS tablet/phone, not the reader)

| Column | Description | Example |
|--------|-------------|---------|
| `DEVICE_MODEL` | Android device model | `'Pixel 7'` |
| `DEVICE_MANUFACTURER` | Manufacturer | `'Google'` |
| `DEVICE_BRAND` | Brand | `'google'` |
| `DEVICE_FORM_FACTOR` | Form factor | `'phone'`, `'tablet'` |
| `MOBILE_APP_VERSION_NAME` | Register app version | `'6.45.0'` |
| `MOBILE_APP_VERSION_CODE` | Version code | `645000` |
| `MOBILE_APP_PACKAGE_NAME` | Package name | `'com.example'` |
| `ANDROID_DEVICE_ID` | Android device ID | |
| `OS_VERSION` | Android OS version | `'14'` |

### Brand A Hardware (SQUID/BRAN — only populated on Brand A-manufactured hardware, not COTS)

| Column | Description |
|--------|-------------|
| `SQ_HARDWARE_HODOR_SQUID_VERSION` | Hodor firmware version (Brand A hardware only) |
| `SQ_HARDWARE_HODOR_SERIAL` | Hodor serial |
| `SQ_HARDWARE_BRAN_SQUID_VERSION` | Bran firmware version |
| `SQ_HARDWARE_BRAN_SERIAL` | Bran serial |
| `SQ_HARDWARE_SPE_SERIAL` | SPE serial |
| `SQ_HARDWARE_K21_FIRMWARE_VERSION` | K21 firmware version |

> These columns are **NULL on COTS (Commercial Off-The-Shelf) devices**. Do not use them as filters
> unless you are explicitly targeting Brand A hardware.

### Timestamps

| Column | Description |
|--------|-------------|
| `U_RECORDED_DATE` | **Clustering key.** Date portion of when the event was recorded. Always filter on this. |
| `U_RECORDED_AT` | Full timestamp of the event. **UTC.** |
| `U_RECORDED_AT_USEC` | Microsecond-precision UTC timestamp |
| `U_INGESTED_AT` | When the event was ingested into Snowflake |
| `SESSION_START_TIME_MSEC` | Session start time in milliseconds |

---

## READER_TELEMETRY_DATA_RAWDATA — StateLogger Payload

For `HW_EVENT_NAME IN ('Workflow: State Transition', 'Workflow: State Timeout')`, the rawdata
contains a JSON-serialized `ReaderWorkflowStateTransitionAnalytics` object:

```json
{
  "workflow":        "LcrInitializationWorkflow",
  "oldState":        "ConnectLcrClient",
  "newState":        "LcrClientConnected",
  "connectionType":  "ble",
  "readerIdentifier":"AA:BB:CC:DD:EE:FF",
  "connectionId":    1
}
```

For timeouts, `oldState` is the state that timed out; `newState` may be absent or a timeout sentinel.

**Filtering:** Use `LIKE '%WorkflowName%'` if the column is TEXT, or JSON path if it's VARIANT:
```sql
-- TEXT
AND READER_TELEMETRY_DATA_RAWDATA LIKE '%LcrInitializationWorkflow%'

-- VARIANT
AND READER_TELEMETRY_DATA_RAWDATA:workflow::STRING = 'LcrInitializationWorkflow'
```

Source:
- `android-register/cdx/cardreaders/public/src/main/java/com/example/cardreaders/StateLogger.kt`
- `android-register/cdx/analytics/public/src/main/java/com/example/cdx/analytics/reader/CardreaderAnalytics.kt`

---

## Common Queries

### Fetch all StateLogger events for a unit + time window

```sql
SELECT
    U_RECORDED_AT,
    HW_EVENT_NAME,
    HW_SERIAL_NUMBER,
    HW_READER_TYPE_KEY,
    HW_CONNECTION_TYPE,
    HW_CONNECTION_ID,
    MOBILE_APP_VERSION_NAME,
    READER_TELEMETRY_DATA_RAWDATA,
    READER_TELEMETRY_ERROR_DESCRIPTION,
    READER_TELEMETRY_SECONDS_SINCE_LAST_LCR_COMMUNICATION
FROM YOUR_EVENT_SCHEMA.CATALOGS.READER_TELEMETRY
WHERE U_RECORDED_DATE BETWEEN
        DATEADD(DAY, -1, TO_DATE('<incident_timestamp>'))
        AND DATEADD(DAY, 1, TO_DATE('<incident_timestamp>'))
    AND U_RECORDED_AT BETWEEN
        DATEADD(HOUR, -2, '<incident_timestamp>'::TIMESTAMP)
        AND DATEADD(HOUR, 2, '<incident_timestamp>'::TIMESTAMP)
    AND SUBJECT_LOCATION_ID = '<location_id>'
    AND HW_EVENT_NAME IN ('Workflow: State Transition', 'Workflow: State Timeout')
ORDER BY U_RECORDED_AT ASC
```

**By merchant instead:** swap `SUBJECT_LOCATION_ID = '...'` for `SUBJECT_CUSTOMER_ID = '<customer_id>'`.
**By serial instead:** swap `SUBJECT_LOCATION_ID = '...'` for `HW_SERIAL_NUMBER = '<serial>'`.
