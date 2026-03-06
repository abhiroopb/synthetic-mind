# Seller Snapshot

Generate a comprehensive seller snapshot and timeline for a Square merchant, providing a 360° view of the seller's relationship with Square.

## Instructions

**First, ask the user for the merchant token to lookup.** Do not proceed until you have a valid merchant token (e.g., `9NZZKMGK37Y3S`).

Once you have the merchant token, use the Snowflake extension to run the queries below and compile a comprehensive seller snapshot report.

### Prerequisites

Install the required CLI skill if not already installed:

```bash
sq agents skills add snowflake
```

**IMPORTANT: You must be connected to Cloudflare WARP VPN.**

### Required Extensions
- **Snowflake**: For running SQL queries against the data warehouse

---

## Data Collection Queries

Replace `{{MERCHANT_TOKEN}}` with the provided merchant token in all queries below.

### 1. Last 25 CS Interactions (All Channels) - WITH FULL DETAILS

```sql
SELECT
    c.CASE_CREATED_AT_UTC,
    c.CASE_STATUS,
    c.CASE_CHANNEL,
    c.CASE_ORIGIN,
    c.CASE_SUBJECT,
    c.CASE_GROUP_NAME,
    c.PRODUCT_TAGS,
    c.BEHAVIORAL_TAGS,
    c.AGENT_NAME,
    c.CASE_FIRST_RESOLVED_AT_UTC,
    c.CASE_LAST_RESOLVED_AT_UTC,
    c.CONTACT_DRIVER_CATEGORY,
    c.CONTACT_DRIVER_DETAILS,
    c.CASE_PRIORITY,
    p.ATTR_VA_SUMMARY AS CALL_SUMMARY,
    p.CALLER_INTENT_UTTERANCE,
    p.CALLER_INTENT,
    p.TALK_TIME AS CALL_TALK_TIME_SECONDS,
    p.HOLD_TIME AS CALL_HOLD_TIME_SECONDS,
    p.CSAT_ADVOCATE_RATING,
    p.CSAT_ISSUE_RESOLUTION
FROM APP_SUPPORT.APP_SUPPORT.CASES c
LEFT JOIN APP_SUPPORT.APP_SUPPORT.PHONES_RESEARCH p
    ON c.CALL_SEGMENT_ID = p.SEGMENT_ID
WHERE c.SQUARE_MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
ORDER BY c.CASE_CREATED_AT_UTC DESC
LIMIT 25
```

### 2. Last 10 AM Interactions (All Types)

```sql
SELECT 
    a.ACTIVITY_DATE,
    a.CREATED_DATE,
    a.ACTIVITY_TYPE,
    a.ACTIVITY_TYPE_GROUPED,
    a.SUBJECT,
    a.CALL_DISPOSITION,
    a.CALL_OUTCOME,
    a.CALL_DURATION_SECONDS,
    a.TALKTIME_CUSTOMER_SECONDS,
    a.TALKTIME_REP_SECONDS,
    a.IS_DM AS IS_DECISION_MAKER,
    a.IS_INBOUND,
    a.OWNER_NAME AS AM_NAME,
    a.AM_TEAM,
    a.STATUS,
    t.TRANSCRIPT_FULL,
    t.TRANSCRIPT_CUSTOMER,
    t.TRANSCRIPT_REP
FROM APP_MERCH_GROWTH.APP_MERCH_GROWTH_ETL.AM_FACT_ACTIVITIES a
LEFT JOIN APP_MERCH_GROWTH.APP_MERCH_GROWTH_ETL.AM_TRANSCRIPTIONS t 
    ON a.SFDC_TASK_ID = t.SFDC_TASK_ID
WHERE a.MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
ORDER BY a.ACTIVITY_DATE DESC, a.CREATED_DATE DESC
LIMIT 10
```

### 3. CS Contact Frequency

```sql
SELECT 
    COUNT(*) AS TOTAL_CASES_L365,
    COUNT(CASE WHEN CASE_CREATED_AT_UTC >= DATEADD('day', -90, CURRENT_DATE()) THEN 1 END) AS CASES_L90,
    COUNT(CASE WHEN CASE_CREATED_AT_UTC >= DATEADD('day', -30, CURRENT_DATE()) THEN 1 END) AS CASES_L30,
    ROUND(COUNT(*) / 12.0, 1) AS AVG_CASES_PER_MONTH,
    MIN(CASE_CREATED_AT_UTC) AS FIRST_CASE_DATE,
    MAX(CASE_CREATED_AT_UTC) AS LAST_CASE_DATE
FROM APP_SUPPORT.APP_SUPPORT.CASES
WHERE SQUARE_MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
    AND CASE_CREATED_AT_UTC >= DATEADD('day', -365, CURRENT_DATE())
```

### 4. Merchant Profile & GPV

```sql
SELECT 
    m.MERCHANT_TOKEN,
    m.BUSINESS_NAME,
    m.MERCHANT_BUSINESS_TYPE,
    m.MERCHANT_BUSINESS_CATEGORY,
    m.MERCHANT_RECEIPT_CITY,
    m.MERCHANT_RECEIPT_STATE,
    m.MERCHANT_RECEIPT_COUNTRY_CODE,
    m.MERCHANT_CREATED_AT,
    m.MERCHANT_FIRST_PAYMENT_DATE,
    m.MERCHANT_LATEST_PAYMENT_DATE,
    m.NUM_UNITS AS NUM_LOCATIONS,
    m.NUM_CURRENTLY_ACTIVE_UNITS AS ACTIVE_LOCATIONS,
    m.EMPLOYEE_COUNT,
    m.MERCHANT_ACTIVE_STATUS,
    m.MERCHANT_NPA_TOTAL / 100.0 AS NPA_TOTAL_USD,
    m.MERCHANT_NPA_PAYMENTS / 100.0 AS NPA_PAYMENTS_USD,
    m.MERCHANT_NPA_SAAS / 100.0 AS NPA_SAAS_USD,
    m.MERCHANT_NPA_CAPITAL / 100.0 AS NPA_CAPITAL_USD,
    m.MERCHANT_NPA_BANKING / 100.0 AS NPA_BANKING_USD,
    m.MERCHANT_NVA / 100.0 AS NVA_USD,
    m.IS_CURRENTLY_FROZEN,
    m.HAS_BEEN_FROZEN,
    m.TOTAL_TIMES_FROZEN
FROM APP_BI.HEXAGON.VDIM_MERCHANT m
WHERE m.MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
```

### 5. GPV Last 365 Days

```sql
SELECT 
    MERCHANT_TOKEN,
    T365D_GPV_USD AS GPV_L365_USD,
    T91D_GPV_USD AS GPV_L91_USD
FROM APP_HARDWARE.ADHOC.BETA_MERCHANT_TRAILING_GPV
WHERE MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
```

### 6. Device Summary by Type

```sql
SELECT 
    lk.READER_TYPE,
    COUNT(DISTINCT ua.FATP_SERIAL) AS DEVICE_COUNT,
    COUNT(DISTINCT CASE WHEN ua.END_TS IS NULL THEN ua.FATP_SERIAL END) AS ACTIVE_DEVICES,
    MIN(ua.START_TS) AS FIRST_ACTIVATION,
    MAX(ua.START_TS) AS LATEST_ACTIVATION
FROM APP_HARDWARE.HDM.FACT_UNIT_ACTIVATIONS ua
LEFT JOIN FIVETRAN.APP_HARDWARE_STAGING.LOOKUP_READER_MODEL_FROM_FATP_SERIAL lk
    ON SUBSTRING(ua.FATP_SERIAL, 5, 4) = lk.MODEL_FROM_FATP_SUBSTRING
JOIN APP_BI.HEXAGON.VDIM_USER u 
    ON ua.UNIT_TOKEN = u.USER_TOKEN
WHERE u.MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
GROUP BY lk.READER_TYPE
ORDER BY ACTIVE_DEVICES DESC
```

### 7. SaaS Products Used

```sql
SELECT 
    MERCHANT_TOKEN,
    ACTIVE_SAAS_PRODUCTS,
    SO_DOMAIN
FROM APP_MKTG_INTL.INTL_PROD.MERCHANT_SAAS_SUBSCRIPTIONS
WHERE MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
```

### 8. Risk Events - SSP/Verification

```sql
SELECT 
    UNIT_TOKEN,
    VERIFF_REQUEST_CREATED_AT,
    VERIFF_TYPE,
    CASE_ID,
    SSP_TOKEN,
    SSP_SENT_AT,
    SSP_FIRST_RESPONSE_AT,
    SSP_REVIEWED_STATUS,
    VERIFF_TO_CASE_MINS,
    DEACTIVATED_AT,
    MIN_UNFREEZE_AT
FROM APP_RISK.APP_RISK.SHEALTH_VERIFF_SSP
WHERE UNIT_TOKEN IN (
    SELECT USER_TOKEN 
    FROM APP_BI.HEXAGON.VDIM_USER 
    WHERE MERCHANT_TOKEN = '{{MERCHANT_TOKEN}}'
)
ORDER BY VERIFF_REQUEST_CREATED_AT DESC
```

---

## Output Format

Present the Seller Snapshot in this organized format:

### **Merchant Overview**
| Field | Value |
|-------|-------|
| Business Name | {BUSINESS_NAME} |
| Merchant Token | {MERCHANT_TOKEN} |
| Location | {CITY, STATE, COUNTRY} |
| Business Type | {BUSINESS_TYPE} |
| Account Created | {DATE} |
| Active Status | {ACTIVE/FROZEN/DEACTIVATED} |

### **Financial Metrics**
| Metric | Value |
|--------|-------|
| GPV L365 | ${GPV_L365_USD} |
| GPV L91 | ${GPV_L91_USD} |
| NPA Total | ${NPA_TOTAL_USD} |

### **Account Structure**
| Metric | Value |
|--------|-------|
| # Locations | {NUM_LOCATIONS} |
| Active Locations | {ACTIVE_LOCATIONS} |
| Employee Count | {EMPLOYEE_COUNT} |
| Active Devices | {DEVICE_COUNT} by type |
| SaaS Products | {PRODUCT_LIST} |

### **Support Contact Frequency**
| Period | Cases |
|--------|-------|
| L30 Days | {CS_CASES_L30} |
| L90 Days | {CS_CASES_L90} |
| L365 Days | {CS_CASES_L365} |
| Avg/Month | {AVG_CASES_PER_MONTH} |

### **Risk Events**
Summarize any freeze history, SSP events, or verification issues.

### **Recent CS Interactions (Last 25)**
Summarize the key themes, issues, and resolutions from recent support cases.

### **Recent AM Calls**
Summarize AM engagement, call outcomes, and key discussion points.

### **Timeline of Key Events**
Create a chronological timeline of significant events (account creation, first payment, freezes, major support issues, AM calls, etc.)

---

## Important Notes

1. **ALWAYS display the full snapshot report directly in chat.** Do not save to a file or skip the output. The user must see the complete formatted report in the same response where the queries are run. If queries fail and need retrying, still present the final compiled snapshot clearly — do not bury it between error outputs.
2. **GPV Values**: Values from `BETA_MERCHANT_TRAILING_GPV` are in USD dollars
3. **NPA/NVA Values**: Values in `VDIM_MERCHANT` are in cents - divide by 100 for dollars
4. **Merchant vs Unit Token**: Some tables use `USER_TOKEN`/`UNIT_TOKEN` - join via `VDIM_USER` to get `MERCHANT_TOKEN`
5. **Freeze Status**: `-1` at merchant level = N/A (check at unit level), `0` = Not frozen, `1` = Currently frozen
