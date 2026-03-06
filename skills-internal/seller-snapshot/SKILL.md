# Customer Snapshot

Generate a comprehensive customer snapshot and timeline for an account, providing a 360° view of the customer's relationship with your platform.

## Instructions

**First, ask the user for the account token to lookup.** Do not proceed until you have a valid account token.

Once you have the account token, use Snowflake (or your data warehouse) to run the queries below and compile a comprehensive customer snapshot report.

### Prerequisites

**IMPORTANT: You must be connected to VPN.**

### Required Extensions
- **Snowflake** (or equivalent data warehouse): For running SQL queries

---

## Data Collection Queries

Replace `{{ACCOUNT_TOKEN}}` with the provided account token in all queries below.

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
    p.CALL_SUMMARY,
    p.CALLER_INTENT,
    p.TALK_TIME AS CALL_TALK_TIME_SECONDS,
    p.HOLD_TIME AS CALL_HOLD_TIME_SECONDS,
    p.CSAT_ADVOCATE_RATING,
    p.CSAT_ISSUE_RESOLUTION
FROM SUPPORT.CASES c
LEFT JOIN SUPPORT.PHONES_RESEARCH p
    ON c.CALL_SEGMENT_ID = p.SEGMENT_ID
WHERE c.ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
ORDER BY c.CASE_CREATED_AT_UTC DESC
LIMIT 25
```

### 2. Last 10 Account Manager Interactions

```sql
SELECT 
    a.ACTIVITY_DATE,
    a.CREATED_DATE,
    a.ACTIVITY_TYPE,
    a.SUBJECT,
    a.CALL_DISPOSITION,
    a.CALL_OUTCOME,
    a.CALL_DURATION_SECONDS,
    a.IS_INBOUND,
    a.OWNER_NAME AS AM_NAME,
    a.AM_TEAM,
    a.STATUS,
    t.TRANSCRIPT_FULL
FROM GROWTH.AM_ACTIVITIES a
LEFT JOIN GROWTH.AM_TRANSCRIPTIONS t 
    ON a.TASK_ID = t.TASK_ID
WHERE a.ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
ORDER BY a.ACTIVITY_DATE DESC
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
FROM SUPPORT.CASES
WHERE ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
    AND CASE_CREATED_AT_UTC >= DATEADD('day', -365, CURRENT_DATE())
```

### 4. Account Profile & Revenue

```sql
SELECT 
    m.ACCOUNT_TOKEN,
    m.BUSINESS_NAME,
    m.BUSINESS_TYPE,
    m.BUSINESS_CATEGORY,
    m.CITY,
    m.STATE,
    m.COUNTRY_CODE,
    m.CREATED_AT,
    m.FIRST_PAYMENT_DATE,
    m.LATEST_PAYMENT_DATE,
    m.NUM_LOCATIONS,
    m.ACTIVE_LOCATIONS,
    m.EMPLOYEE_COUNT,
    m.ACTIVE_STATUS,
    m.REVENUE_TOTAL / 100.0 AS REVENUE_TOTAL_USD,
    m.REVENUE_PAYMENTS / 100.0 AS REVENUE_PAYMENTS_USD,
    m.REVENUE_SAAS / 100.0 AS REVENUE_SAAS_USD,
    m.IS_CURRENTLY_FROZEN,
    m.HAS_BEEN_FROZEN,
    m.TOTAL_TIMES_FROZEN
FROM BI.DIM_MERCHANT m
WHERE m.ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
```

### 5. GPV Last 365 Days

```sql
SELECT 
    ACCOUNT_TOKEN,
    T365D_GPV_USD AS GPV_L365_USD,
    T91D_GPV_USD AS GPV_L91_USD
FROM ANALYTICS.TRAILING_GPV
WHERE ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
```

### 6. Device Summary by Type

```sql
SELECT 
    lk.READER_TYPE,
    COUNT(DISTINCT ua.SERIAL) AS DEVICE_COUNT,
    COUNT(DISTINCT CASE WHEN ua.END_TS IS NULL THEN ua.SERIAL END) AS ACTIVE_DEVICES,
    MIN(ua.START_TS) AS FIRST_ACTIVATION,
    MAX(ua.START_TS) AS LATEST_ACTIVATION
FROM HARDWARE.UNIT_ACTIVATIONS ua
LEFT JOIN HARDWARE.READER_MODEL_LOOKUP lk
    ON SUBSTRING(ua.SERIAL, 5, 4) = lk.MODEL_SUBSTRING
JOIN BI.DIM_USER u 
    ON ua.UNIT_TOKEN = u.USER_TOKEN
WHERE u.ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
GROUP BY lk.READER_TYPE
ORDER BY ACTIVE_DEVICES DESC
```

### 7. SaaS Products Used

```sql
SELECT 
    ACCOUNT_TOKEN,
    ACTIVE_SAAS_PRODUCTS,
    SUBSCRIPTION_DOMAIN
FROM ANALYTICS.SAAS_SUBSCRIPTIONS
WHERE ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
```

### 8. Risk Events

```sql
SELECT 
    UNIT_TOKEN,
    VERIFICATION_CREATED_AT,
    VERIFICATION_TYPE,
    CASE_ID,
    REVIEWED_STATUS,
    DEACTIVATED_AT
FROM RISK.VERIFICATION_EVENTS
WHERE UNIT_TOKEN IN (
    SELECT USER_TOKEN 
    FROM BI.DIM_USER 
    WHERE ACCOUNT_TOKEN = '{{ACCOUNT_TOKEN}}'
)
ORDER BY VERIFICATION_CREATED_AT DESC
```

---

## Output Format

Present the Customer Snapshot in this organized format:

### **Account Overview**
| Field | Value |
|-------|-------|
| Business Name | {BUSINESS_NAME} |
| Account Token | {ACCOUNT_TOKEN} |
| Location | {CITY, STATE, COUNTRY} |
| Business Type | {BUSINESS_TYPE} |
| Account Created | {DATE} |
| Active Status | {ACTIVE/FROZEN/DEACTIVATED} |

### **Financial Metrics**
| Metric | Value |
|--------|-------|
| GPV L365 | ${GPV_L365_USD} |
| GPV L91 | ${GPV_L91_USD} |
| Revenue Total | ${REVENUE_TOTAL_USD} |

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
Summarize any freeze history, verification events, or issues.

### **Recent CS Interactions (Last 25)**
Summarize the key themes, issues, and resolutions from recent support cases.

### **Recent AM Calls**
Summarize AM engagement, call outcomes, and key discussion points.

### **Timeline of Key Events**
Create a chronological timeline of significant events (account creation, first payment, freezes, major support issues, AM calls, etc.)

---

## Important Notes

1. **ALWAYS display the full snapshot report directly in chat.** Do not save to a file or skip the output.
2. **Revenue Values**: Values in the dimension table are in cents — divide by 100 for dollars.
3. **Account vs Unit Token**: Some tables use `USER_TOKEN`/`UNIT_TOKEN` — join via the user dimension to get `ACCOUNT_TOKEN`.
4. **Freeze Status**: `0` = Not frozen, `1` = Currently frozen.
