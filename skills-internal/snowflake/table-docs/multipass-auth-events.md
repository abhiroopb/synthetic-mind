# Multipass Auth Events

Query and analyze Multipass authentication, session, and security events from Snowflake.

## Tables

### YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT

Multipass Events in EventStream — a catalog used to log activities related to the Multipass service,
which is involved in account and session management. This table is crucial for tracking authentication
and session-related events.

## Common Fields Reference

### Custom Multipass Fields

- `multipass_event_access_token_hash` - Base64 hash of OAuth access token
- `multipass_event_actor_id` - Unique identifier of the actor
- `multipass_event_event_name` - Type of event (e.g., 'EndpointCall', 'Operation')
- `multipass_event_event_value` - Specific action performed
- `multipass_event_two_factor_state` - 2FA state (NONE or REQUIRED)
- `multipass_event_two_factor_method` - 2FA method type (SMS, GOOGLEAUTH, WEBAUTHN)
- `multipass_event_error_code` - Error code if operation failed
- `multipass_event_success` - Success indicator
- `multipass_event_client_o_u` - Client organizational unit
- `multipass_event_impersonator` - Impersonator identifier for support actions

### Inherited Fields

- `connection_ip_address` - Request originating IP
- `connection_user_agent` - User agent string
- `connection_network_type` - Network type (wifi/cellular)
- `u_recorded_at` - Event timestamp
- `subject_person_token` - Person identifier
- `subject_customer_id` - Merchant identifier
- `subject_anonymous_token` - Anonymous visitor token

## Query Templates

### 1. Two-Factor Authentication Events

#### Monitor 2FA Requirement Changes (Merchant Level)

```sql
-- Track when merchants change their 2FA requirements
SELECT
  u_recorded_at,
  subject_customer_id,
  multipass_event_two_factor_state,
  connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
  AND multipass_event_event_name = 'EndpointCall'
  AND multipass_event_event_value = 'UpdateMerchantTwoFactorState'
ORDER BY u_recorded_at DESC
LIMIT 1000;
```

#### Monitor 2FA Requirement Changes (Person Level)

```sql
-- Track individual user 2FA requirement changes
SELECT
  u_recorded_at,
  subject_person_token,
  multipass_event_two_factor_reason,
  multipass_event_two_factor_state,
  connection_ip_address,
  connection_user_agent
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
  AND multipass_event_event_name = 'EndpointCall'
  AND multipass_event_event_value = 'UpdateTwoFactorRequirement'
ORDER BY u_recorded_at DESC
LIMIT 1000;
```

#### Track 2FA Method Enrollment

```sql
-- Monitor 2FA method additions
SELECT
  u_recorded_at,
  subject_person_token,
  multipass_event_two_factor_method,
  multipass_event_complete,
  connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name = 'EndpointCall'
  AND multipass_event_event_value = 'InternalEnrollTwoFactor'
ORDER BY u_recorded_at DESC;
```

#### Track 2FA Method Removal

```sql
-- Monitor 2FA method removals
SELECT
  u_recorded_at,
  subject_person_token,
  multipass_event_two_factor_method,
  multipass_event_impersonator,
  connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name = 'EndpointCall'
  AND multipass_event_event_value IN ('InternalRemoveTwoFactor', 'DeleteTwoFactorDetails')
ORDER BY u_recorded_at DESC;
```

### 2. Password Management

#### Password Reset Flow - Complete Journey

```sql
-- Track complete password reset journey for a person
WITH reset_events AS (
  SELECT
    subject_person_token,
    multipass_event_event_value as step,
    multipass_event_success,
    multipass_event_error_code,
    connection_ip_address,
    u_recorded_at
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
  WHERE 1=1
    AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
    AND multipass_event_event_name = 'EndpointCall'
    AND multipass_event_event_value IN (
      'GetPasswordResetLink',
      'InternalResetPasswordVerifyCode',
      'InternalResetPasswordChangePassword'
    )
)
SELECT
  subject_person_token,
  step,
  multipass_event_success,
  multipass_event_error_code,
  u_recorded_at,
  LAG(u_recorded_at) OVER (PARTITION BY subject_person_token ORDER BY u_recorded_at) as prev_step_time,
  DATEDIFF('minute',
    LAG(u_recorded_at) OVER (PARTITION BY subject_person_token ORDER BY u_recorded_at),
    u_recorded_at
  ) as minutes_between_steps
FROM reset_events
ORDER BY subject_person_token, u_recorded_at;
```

#### Password Change Notifications

```sql
-- Track password change notification emails
SELECT
  subject_person_token,
  u_recorded_at,
  COUNT(*) OVER (PARTITION BY subject_person_token) as total_notifications
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND multipass_event_event_name = 'Operation'
  AND multipass_event_event_value = 'PasswordChangerNotification'
ORDER BY u_recorded_at DESC;
```

### 3. Session Management

#### Login Activity Analysis

```sql
-- Analyze login patterns and failures
SELECT
  DATE_TRUNC('hour', u_recorded_at) as login_hour,
  multipass_event_event_value as login_type,
  CASE
    WHEN multipass_event_error_code IS NOT NULL THEN 'Failed'
    ELSE 'Success'
  END as status,
  COUNT(*) as login_count,
  COUNT(DISTINCT subject_person_token) as unique_users,
  COUNT(DISTINCT connection_ip_address) as unique_ips
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name = 'Operation'
  AND multipass_event_event_value IN ('SessionCreation', 'DeviceSessionCreation')
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 2, 3;
```

#### Device Login Monitoring

```sql
-- Monitor SPOS device logins
SELECT
  u_recorded_at,
  subject_device_credential_token,
  multipass_event_error_code,
  connection_ip_address,
  multipass_event_device_identifier
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -1, CURRENT_DATE())
  AND multipass_event_event_name = 'Operation'
  AND multipass_event_event_value = 'DeviceSessionCreation'
  AND subject_device_credential_token != ''
ORDER BY u_recorded_at DESC;
```

#### One Time Key (OTK) Creation

```sql
-- Track OTK creation patterns
SELECT
  DATE_TRUNC('hour', u_recorded_at) as otk_hour,
  COUNT(*) as otk_created,
  COUNT(DISTINCT subject_person_token) as unique_users,
  COUNT(DISTINCT multipass_event_client_o_u) as unique_clients
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name = 'EndpointCall'
  AND multipass_event_event_value = 'CreateOtk'
GROUP BY 1
ORDER BY 1 DESC;
```

### 4. Security and Account Management

#### Dashboard False 401 Errors

```sql
-- Track false 401 errors in Dashboard
SELECT
  DATE_TRUNC('hour', u_recorded_at) as error_hour,
  COUNT(*) as false_401_count,
  COUNT(DISTINCT subject_person_token) as affected_users
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name = 'Operation'
  AND multipass_event_event_value = 'DashboardFalse401'
GROUP BY 1
ORDER BY 1 DESC;
```

#### Email Change Requests

```sql
-- Track email change verification flow
SELECT
  u_recorded_at,
  subject_person_token,
  multipass_event_event_details,
  multipass_event_error_code,
  CASE
    WHEN multipass_event_error_code IS NULL THEN 'Success'
    ELSE 'Failed'
  END as status
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('month', -1, CURRENT_DATE())
  AND multipass_event_event_value = 'InternalChangeEmailWithVerification'
ORDER BY u_recorded_at DESC;
```

#### 2FA Disable Counts by Day and Source

```sql
-- Track 2FA disables by day, distinguishing between user-initiated and CS-initiated
WITH otk_events AS (
  SELECT DISTINCT
    subject_anonymous_token,
    MAX(CASE WHEN multipass_event_impersonator IS NOT NULL THEN 1 ELSE 0 END) as was_impersonated
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
  WHERE 1=1
    AND u_recorded_at >= CURRENT_DATE - INTERVAL '30 days'
    AND multipass_event_event_name = 'EndpointCall'
    AND multipass_event_event_value = 'CreateOtk'
  GROUP BY subject_anonymous_token
),
daily_stats AS (
  SELECT
    DATE_TRUNC('day', m.u_recorded_at) as event_date,
    CASE
      WHEN o.was_impersonated = 1 THEN 'CS_DISABLED'
      ELSE 'USER_DISABLED'
    END as disable_source,
    COUNT(DISTINCT m.subject_person_token) as unique_persons
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT m
  LEFT JOIN otk_events o ON m.subject_anonymous_token = o.subject_anonymous_token
  WHERE 1=1
    AND m.u_recorded_at >= CURRENT_DATE - INTERVAL '30 days'
    AND m.multipass_event_event_name = 'EndpointCall'
    AND m.multipass_event_event_value = 'UpdateTwoFactorRequirement'
    AND m.multipass_event_two_factor_state = 'none'
  GROUP BY event_date, disable_source
)
SELECT
  event_date,
  SUM(CASE WHEN disable_source = 'CS_DISABLED' THEN unique_persons ELSE 0 END) as cs_disabled_unique_persons,
  SUM(CASE WHEN disable_source = 'USER_DISABLED' THEN unique_persons ELSE 0 END) as user_disabled_unique_persons,
  SUM(unique_persons) as total_disabled_count
FROM daily_stats
GROUP BY event_date
ORDER BY event_date DESC;
```

### 5. Step-Up Authentication (SUA)

#### SUA Upgrade Events by Method

```sql
-- Analyze Step-Up Authentication upgrades by 2FA method
SELECT
  multipass_event_two_factor_method,
  COUNT(multipass_event_two_factor_method) as method_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalUpgradeSessionTwoFactor'
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND me.multipass_event_two_factor_verification_source = 'step_up_authentication'
GROUP BY multipass_event_two_factor_method
ORDER BY method_count DESC;
```

#### 2FA Upgrades by Verification Source

```sql
-- Analyze 2FA upgrades by verification source
SELECT
  multipass_event_two_factor_verification_source,
  COUNT(multipass_event_two_factor_verification_source) as source_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalUpgradeSessionTwoFactor'
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
GROUP BY multipass_event_two_factor_verification_source
ORDER BY source_count DESC;
```

### 6. Error Analysis

#### 2FA Enrollment Errors

```sql
-- Analyze error types from 2FA enrollment attempts
SELECT
  multipass_event_error_code,
  COUNT(multipass_event_error_code) as error_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalEnrollTwoFactor'
  AND me.u_recorded_at >= DATEADD('month', -6, CURRENT_DATE())
  AND me.multipass_event_error_code IS NOT NULL
  AND me.multipass_event_error_code != ''
GROUP BY multipass_event_error_code
ORDER BY error_count DESC;
```

#### Password Reset Errors for Specific User

```sql
-- Analyze password reset errors for a specific user
SELECT
  multipass_event_error_code,
  COUNT(multipass_event_error_code) as error_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalResetPasswordChangePassword'
  AND me.subject_person_token = 'person:PERSON_TOKEN_HERE'  -- Replace with actual person token
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND me.multipass_event_error_code IS NOT NULL
  AND me.multipass_event_error_code != ''
GROUP BY multipass_event_error_code
ORDER BY error_count DESC;
```

### 7. Session Validation and Termination

#### Session Termination by Application

```sql
-- Analyze session terminations by application ID
SELECT
  multipass_event_application_id,
  COUNT(multipass_event_application_id) as termination_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionValidator'
  AND me.u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND me.multipass_event_error_code = 'SESSION_ID_TERMINATED'
GROUP BY multipass_event_application_id
ORDER BY termination_count DESC;
```

#### Correlated Session Terminations

```sql
-- Find ValidateSession errors correlated with TerminateAuthorization events
WITH recently_terminated_authorization_ids AS (
  SELECT
    multipass_event_authorization_id
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
  WHERE 1=1
    AND me.multipass_event_event_name = 'EndpointCall'
    AND me.multipass_event_event_value = 'TerminateAuthorization'
    AND me.u_recorded_at >= DATEADD('day', -1, CURRENT_DATE())
)
SELECT
  COUNT(*) as correlated_termination_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionValidator'
  AND me.u_recorded_at >= DATEADD('day', -1, CURRENT_DATE())
  AND me.multipass_event_error_code = 'SESSION_ID_TERMINATED'
  AND me.multipass_event_authorization_id IN (
    SELECT multipass_event_authorization_id
    FROM recently_terminated_authorization_ids
  );
```

#### Hourly Session Termination Pattern

```sql
-- Analyze session termination patterns by hour
SELECT
  me.u_recorded_date,
  HOUR(me.u_recorded_at) as hour_of_day,
  COUNT(*) as termination_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_date >= CURRENT_DATE() - 1
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionValidator'
  AND me.multipass_event_error_code = 'SESSION_ID_TERMINATED'
GROUP BY me.u_recorded_date, HOUR(me.u_recorded_at)
ORDER BY me.u_recorded_date, hour_of_day;
```

### 8. User Activity Tracking

#### 2FA Activity for Specific User

```sql
-- Track 2FA enrollments, disables, and requirement changes for a user
SELECT
  me.u_recorded_at,
  me.subject_person_token,
  me.multipass_event_event_value as action,
  me.multipass_event_two_factor_method,
  me.multipass_event_two_factor_state,
  me.multipass_event_two_factor_reason,
  me.multipass_event_two_factor_enrollment_source
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('year', -1, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value IN ('InternalEnrollTwoFactor', 'UpdateTwoFactorRequirement')
  AND me.subject_person_token = 'person:PERSON_TOKEN_HERE'  -- Replace with actual person token
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

#### Successful Login Pattern Analysis

```sql
-- Analyze successful login patterns grouped by day
SELECT
  DATE(me.u_recorded_at) AS login_date,
  COUNT(*) as successful_login_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('month', -1, CURRENT_DATE())
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionCreation'
  AND me.subject_person_token = 'person:PERSON_TOKEN_HERE'  -- Replace with actual person token
  AND (me.multipass_event_error_code IS NULL OR me.multipass_event_error_code = '')
GROUP BY DATE(me.u_recorded_at)
ORDER BY login_date DESC;
```

### 9. Account Security Events

#### Dormant Account Detection

```sql
-- Find dormant account login attempts
SELECT
  me.subject_person_token,
  me.u_recorded_at,
  me.multipass_event_error_code,
  me.connection_ip_address,
  me.connection_user_agent
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionCreation'
  AND me.multipass_event_error_code = 'DORMANT_ACCOUNT'
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

#### Account Lock Events

```sql
-- Find when accounts were locked
SELECT
  me.subject_person_token,
  me.u_recorded_at,
  me.multipass_event_lockout_reason,
  me.multipass_event_event_value,
  me.connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'LockAccount'
  AND me.u_recorded_at >= DATEADD('month', -1, CURRENT_DATE())
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

#### Dormant Account Recovery Attempts

```sql
-- Track all dormant account recovery attempts
SELECT
  me.subject_person_token,
  me.multipass_event_account_recovery_method,
  me.multipass_event_error_code,
  me.multipass_event_success,
  me.u_recorded_at
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'VerifyRecoveryDetail'
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

### 10. Bot Detection and Security

#### Kasada Bot Classification

```sql
-- Analyze Kasada bot detection classifications
SELECT
  me.multipass_event_kasada_classification,
  COUNT(*) as classification_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND me.multipass_event_kasada_classification != ''
  AND me.multipass_event_kasada_classification IS NOT NULL
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'SessionCreation'
GROUP BY me.multipass_event_kasada_classification
ORDER BY classification_count DESC;
```

#### Kasada Request Analysis

```sql
-- Sample Kasada request IDs for investigation
SELECT
  me.subject_person_token,
  me.multipass_event_kasada_request_id,
  me.u_recorded_at
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_kasada_request_id != ''
  AND me.multipass_event_kasada_request_id IS NOT NULL
  AND me.u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

### 11. Attack Detection

#### High-Volume 2FA Attempts by IP

```sql
-- Detect potential 2FA brute force attempts by IP
SELECT
  connection_ip_address,
  COUNT(connection_ip_address) as attempt_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalUpgradeSessionTwoFactor'
  AND me.u_recorded_at >= DATEADD('hour', -1, CURRENT_DATE())
  AND me.multipass_event_error_code = 'INVALID_CREDENTIALS'
GROUP BY connection_ip_address
HAVING COUNT(connection_ip_address) > 10
ORDER BY attempt_count DESC;
```

#### High-Volume 2FA Attempts by User

```sql
-- Detect users with excessive failed 2FA attempts
SELECT
  subject_person_token,
  COUNT(subject_person_token) as failed_attempt_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalUpgradeSessionTwoFactor'
  AND me.u_recorded_at >= DATEADD('hour', -1, CURRENT_DATE())
  AND me.multipass_event_error_code = 'INVALID_CREDENTIALS'
GROUP BY subject_person_token
HAVING COUNT(subject_person_token) > 5
ORDER BY failed_attempt_count DESC;
```

#### Successful SMS 2FA Upgrades Analysis

```sql
-- Analyze successful SMS 2FA upgrades in a time window
SELECT
  subject_person_token,
  COUNT(subject_person_token) as success_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'InternalUpgradeSessionTwoFactor'
  AND me.u_recorded_at >= DATEADD('hour', -1, CURRENT_DATE())
  AND me.multipass_event_success = true
  AND me.multipass_event_two_factor_method = 'SMS'
GROUP BY subject_person_token
ORDER BY success_count DESC;
```

### 12. OAuth Session Events

#### OAuth Session Terminations

```sql
-- Track OAuth session terminations with access tokens
SELECT
  me.u_recorded_at,
  me.multipass_event_access_token_hash,
  me.multipass_event_session_type,
  me.subject_person_token
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'TerminateSession'
  AND me.multipass_event_session_type = 'OAUTH'
  AND me.multipass_event_access_token_hash != ''
  AND me.multipass_event_access_token_hash IS NOT NULL
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

#### OAuth Session Terminations Daily Trend

```sql
-- Track OAuth session terminations per day (last 90 days)
-- Same pattern works for authorization terminations: change event_value to 'TerminateAuthorization'
-- and remove the session_type/access_token_hash filters
SELECT
  DATE(me.u_recorded_at) as termination_date,
  COUNT(*) as termination_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -90, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'TerminateSession'
  AND me.multipass_event_session_type = 'OAUTH'
  AND me.multipass_event_access_token_hash != ''
  AND me.multipass_event_access_token_hash IS NOT NULL
GROUP BY DATE(me.u_recorded_at)
ORDER BY termination_date DESC;
```

#### OAuth Authorization Terminations Daily Trend

```sql
-- Track OAuth authorization terminations per day (last 90 days)
SELECT
  DATE(me.u_recorded_at) as termination_date,
  COUNT(*) as authorization_termination_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -90, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'TerminateAuthorization'
GROUP BY DATE(me.u_recorded_at)
ORDER BY termination_date DESC;
```

#### OAuth Access Token Creation Events

```sql
-- Track OAuth access token creation from refresh tokens
SELECT
  me.u_recorded_at,
  me.subject_person_token,
  me.multipass_event_access_token_hash,
  me.multipass_event_client_o_u,
  me.connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -90, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'NewAccessTokenFromRefreshToken'
  AND me.multipass_event_access_token_hash != ''
  AND me.multipass_event_access_token_hash IS NOT NULL
  AND (me.multipass_event_error_code = '' OR me.multipass_event_error_code IS NULL)
ORDER BY me.u_recorded_at DESC
LIMIT 1000;
```

#### OAuth Access Token Creation Daily Trend

```sql
-- Track OAuth access token creations per day (last 90 days)
SELECT
  DATE(me.u_recorded_at) as creation_date,
  COUNT(*) as token_creation_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -90, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'NewAccessTokenFromRefreshToken'
  AND me.multipass_event_access_token_hash != ''
  AND me.multipass_event_access_token_hash IS NOT NULL
  AND (me.multipass_event_error_code = '' OR me.multipass_event_error_code IS NULL)
GROUP BY DATE(me.u_recorded_at)
ORDER BY creation_date DESC;
```

#### OAuth Token Lifecycle Analysis

```sql
-- Comprehensive OAuth token lifecycle metrics (last 30 days)
WITH token_creations AS (
  SELECT
    DATE(me.u_recorded_at) as activity_date,
    COUNT(*) as tokens_created
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
  WHERE 1=1
    AND me.u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
    AND me.multipass_event_event_name = 'EndpointCall'
    AND me.multipass_event_event_value = 'NewAccessTokenFromRefreshToken'
    AND me.multipass_event_access_token_hash != ''
    AND (me.multipass_event_error_code = '' OR me.multipass_event_error_code IS NULL)
  GROUP BY DATE(me.u_recorded_at)
),
token_terminations AS (
  SELECT
    DATE(me.u_recorded_at) as activity_date,
    COUNT(*) as tokens_terminated
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
  WHERE 1=1
    AND me.u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
    AND me.multipass_event_event_name = 'EndpointCall'
    AND me.multipass_event_event_value = 'TerminateSession'
    AND me.multipass_event_session_type = 'OAUTH'
    AND me.multipass_event_access_token_hash != ''
  GROUP BY DATE(me.u_recorded_at)
),
auth_terminations AS (
  SELECT
    DATE(me.u_recorded_at) as activity_date,
    COUNT(*) as auths_terminated
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
  WHERE 1=1
    AND me.u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
    AND me.multipass_event_event_name = 'EndpointCall'
    AND me.multipass_event_event_value = 'TerminateAuthorization'
  GROUP BY DATE(me.u_recorded_at)
)
SELECT
  COALESCE(c.activity_date, t.activity_date, a.activity_date) as date,
  COALESCE(c.tokens_created, 0) as tokens_created,
  COALESCE(t.tokens_terminated, 0) as tokens_terminated,
  COALESCE(a.auths_terminated, 0) as authorizations_terminated,
  COALESCE(c.tokens_created, 0) - COALESCE(t.tokens_terminated, 0) as net_token_change
FROM token_creations c
FULL OUTER JOIN token_terminations t ON c.activity_date = t.activity_date
FULL OUTER JOIN auth_terminations a ON c.activity_date = a.activity_date
ORDER BY date DESC;
```

#### OAuth Access Token Error Analysis

```sql
-- Analyze errors in OAuth token refresh attempts
SELECT
  me.multipass_event_error_code,
  COUNT(*) as error_count,
  COUNT(DISTINCT me.subject_person_token) as affected_users
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'NewAccessTokenFromRefreshToken'
  AND me.multipass_event_error_code != ''
  AND me.multipass_event_error_code IS NOT NULL
GROUP BY me.multipass_event_error_code
ORDER BY error_count DESC;
```

#### OAuth Client Analysis

```sql
-- Analyze OAuth activity by client/application
SELECT
  me.multipass_event_client_o_u as client,
  COUNT(CASE WHEN me.multipass_event_event_value = 'NewAccessTokenFromRefreshToken' THEN 1 END) as tokens_created,
  COUNT(CASE WHEN me.multipass_event_event_value = 'TerminateSession' THEN 1 END) as sessions_terminated,
  COUNT(DISTINCT me.subject_person_token) as unique_users
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value IN ('NewAccessTokenFromRefreshToken', 'TerminateSession')
  AND me.multipass_event_session_type = 'OAUTH'
GROUP BY me.multipass_event_client_o_u
ORDER BY tokens_created DESC;
```

#### TOTP Session Scope Analysis

```sql
-- Analyze TOTP session creation by scope
SELECT
  multipass_event_scope,
  COUNT(multipass_event_scope) as scope_count
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.multipass_event_event_name = 'Operation'
  AND me.multipass_event_event_value = 'TotpSessionCreation'
  AND me.u_recorded_at >= DATEADD('year', -1, CURRENT_DATE())
GROUP BY multipass_event_scope
ORDER BY scope_count DESC;
```

### 13. Trusted Device Analysis

#### Trusted Device Token Validation

```sql
-- Analyze trusted device token validation for a user
SELECT
  me.u_recorded_at,
  me.multipass_event_success,
  me.multipass_event_error_code,
  me.connection_ip_address,
  me.connection_user_agent
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('month', -1, CURRENT_DATE())
  AND me.multipass_event_event_name = 'EndpointCall'
  AND me.multipass_event_event_value = 'ValidateTrustedDeviceToken'
  AND me.subject_person_token = 'person:PERSON_TOKEN_HERE'  -- Replace with actual person token
ORDER BY me.u_recorded_at DESC
LIMIT 100;
```

### 14. Comprehensive User Activity

```sql
-- Get comprehensive activity for a specific user
SELECT
  me.u_recorded_at,
  me.multipass_event_event_name,
  me.multipass_event_event_value,
  me.multipass_event_event_details,
  me.multipass_event_scope,
  me.multipass_event_session_type,
  me.multipass_event_success,
  me.multipass_event_error_code,
  me.multipass_event_two_factor_method,
  me.connection_ip_address,
  me.connection_user_agent
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT AS me
WHERE 1=1
  AND me.u_recorded_at >= DATEADD('month', -3, CURRENT_DATE())
  AND (
    me.subject_person_token = 'person:PERSON_TOKEN_HERE'
    OR me.multipass_event_unverified_person_token = 'person:PERSON_TOKEN_HERE'
  )  -- Replace with actual person token
ORDER BY me.u_recorded_at DESC
LIMIT 200;
```

## Advanced Analysis

### Suspicious Activity Detection

```sql
-- Detect potential suspicious login patterns
WITH login_stats AS (
  SELECT
    subject_person_token,
    DATE_TRUNC('day', u_recorded_at) as login_day,
    COUNT(*) as daily_login_attempts,
    COUNT(DISTINCT connection_ip_address) as unique_ips,
    COUNT(DISTINCT connection_user_agent) as unique_user_agents,
    SUM(CASE WHEN multipass_event_error_code IS NOT NULL THEN 1 ELSE 0 END) as failed_attempts
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
  WHERE 1=1
    AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
    AND multipass_event_event_name = 'Operation'
    AND multipass_event_event_value = 'SessionCreation'
  GROUP BY 1, 2
)
SELECT
  subject_person_token,
  login_day,
  daily_login_attempts,
  unique_ips,
  unique_user_agents,
  failed_attempts,
  ROUND(failed_attempts::FLOAT / NULLIF(daily_login_attempts, 0) * 100, 2) as failure_rate_pct
FROM login_stats
WHERE daily_login_attempts > 10  -- Flag high volume
  OR unique_ips > 5  -- Flag multiple IPs
  OR (failed_attempts > 5 AND failed_attempts::FLOAT / daily_login_attempts > 0.5)  -- Flag high failure rate
ORDER BY daily_login_attempts DESC;
```

### 2FA Adoption Metrics

```sql
-- Calculate 2FA adoption rates by merchant
WITH merchant_2fa AS (
  SELECT
    subject_customer_id,
    MAX(CASE WHEN multipass_event_two_factor_state = 'REQUIRED' THEN 1 ELSE 0 END) as has_2fa_required,
    MAX(u_recorded_at) as last_update
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
  WHERE 1=1
    AND multipass_event_event_name = 'EndpointCall'
    AND multipass_event_event_value = 'UpdateMerchantTwoFactorState'
  GROUP BY 1
),
merchant_counts AS (
  SELECT
    COUNT(DISTINCT subject_customer_id) as total_merchants,
    SUM(has_2fa_required) as merchants_with_2fa
  FROM merchant_2fa
)
SELECT
  total_merchants,
  merchants_with_2fa,
  ROUND(merchants_with_2fa::FLOAT / NULLIF(total_merchants, 0) * 100, 2) as adoption_rate_pct
FROM merchant_counts;
```

### Session Duration Analysis

```sql
-- Analyze session durations and patterns
WITH session_events AS (
  SELECT
    subject_person_token,
    multipass_event_session_token,
    MIN(u_recorded_at) as session_start,
    MAX(u_recorded_at) as session_end,
    COUNT(*) as event_count
  FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
  WHERE 1=1
    AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
    AND multipass_event_session_token IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  DATE_TRUNC('hour', session_start) as hour,
  COUNT(*) as total_sessions,
  AVG(DATEDIFF('minute', session_start, session_end)) as avg_duration_minutes,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY DATEDIFF('minute', session_start, session_end)) as median_duration_minutes,
  MAX(DATEDIFF('minute', session_start, session_end)) as max_duration_minutes
FROM session_events
WHERE session_end > session_start  -- Filter out single-event sessions
GROUP BY 1
ORDER BY 1 DESC;
```

## Troubleshooting

### Investigating Login Failures

```sql
-- Deep dive into login failures for specific user
SELECT
  u_recorded_at,
  multipass_event_error_code,
  multipass_event_event_details,
  connection_ip_address,
  connection_user_agent,
  multipass_event_two_factor_state
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND subject_person_token = 'PERSON_TOKEN_HERE'  -- Replace with actual person token
  AND u_recorded_at >= DATEADD('day', -7, CURRENT_DATE())
  AND multipass_event_event_name IN ('Operation', 'EndpointCall')
  AND multipass_event_error_code IS NOT NULL
ORDER BY u_recorded_at DESC;
```

### Tracking Support Actions

```sql
-- Monitor support-initiated actions (impersonation)
SELECT
  u_recorded_at,
  multipass_event_event_value as action,
  subject_person_token as affected_user,
  multipass_event_impersonator as support_agent,
  multipass_event_client_o_u,
  connection_ip_address
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
  AND multipass_event_impersonator IS NOT NULL
ORDER BY u_recorded_at DESC;
```

## Daily Health Check

```sql
-- Overall system health metrics
SELECT
  DATE_TRUNC('day', u_recorded_at) as day,
  COUNT(*) as total_events,
  COUNT(DISTINCT subject_person_token) as unique_users,
  COUNT(DISTINCT subject_customer_id) as unique_merchants,
  SUM(CASE WHEN multipass_event_error_code IS NOT NULL THEN 1 ELSE 0 END) as error_count,
  ROUND(SUM(CASE WHEN multipass_event_error_code IS NOT NULL THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100, 2) as error_rate_pct
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE u_recorded_at >= DATEADD('day', -30, CURRENT_DATE())
GROUP BY 1
ORDER BY 1 DESC;
```

## Top Error Codes

```sql
-- Most common errors in the last 24 hours
SELECT
  multipass_event_error_code,
  multipass_event_event_value,
  COUNT(*) as error_count,
  COUNT(DISTINCT subject_person_token) as affected_users
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT
WHERE 1=1
  AND u_recorded_at >= DATEADD('day', -1, CURRENT_DATE())
  AND multipass_event_error_code IS NOT NULL
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 20;
```

## Data Freshness Check

```sql
-- Get the most recent multipass_event record to verify data freshness
SELECT
  me.u_recorded_at as latest_event_time
FROM YOUR_EVENT_SCHEMA.CATALOGS.MULTIPASS_EVENT me
ORDER BY me.u_recorded_at DESC
LIMIT 1;
```

## Best Practices

1. **Time Ranges**: Always include appropriate time filters to avoid scanning entire table
2. **Indexing**: Leverage u_recorded_at for efficient time-based queries
3. **Person Tokens**: Use person tokens for user-specific investigations
4. **Error Analysis**: Check multipass_event_error_code for failure investigations
