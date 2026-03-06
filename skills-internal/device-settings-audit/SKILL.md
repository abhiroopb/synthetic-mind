---
name: device-settings-audit
description: Query device profile change history from Team Audit Log. Use when investigating who created/updated/linked device profiles and when changes occurred. Includes access to device profile JSON configuration.
roles:
  - device-platform
---

# Device Settings Audit

Query device profile changes (create, update, link) from the Team Audit Log service via device-settings.

## Quick Start

Query device profile changes for a merchant:
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"types\":[\"CREATED\",\"UPDATED\",\"LINKED\"],\"limit\":200}"}'
```

## Request Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `merchant_id` | string | **Yes** | Merchant token | `"MLFQVZ8YWP1A6"` |
| `location_ids` | string[] | No | Filter by location tokens | `["LOC1", "LOC2"]` |
| `employee_ids` | string[] | No | Filter by employee tokens | `["EMP1"]` |
| `types` | string[] | No | Event types to filter (see below) | `["CREATED", "UPDATED"]` |
| `start_at` | string | No | Start timestamp (RFC 3339, use UTC) | `"2025-01-01T00:00:00Z"` |
| `end_at` | string | No | End timestamp (RFC 3339, use UTC) | `"2025-01-31T23:59:59Z"` |
| `limit` | uint32 | No | Results per page, 1-200 (default 200) | `50` |
| `cursor` | string | No | Pagination cursor from previous response | |

## Event Types

Use these values in the `types` request filter:

| Value | Description |
|-------|-------------|
| `CREATED` | New device profile created |
| `UPDATED` | Device profile settings modified (includes before/after profile) |
| `LINKED` | Device profile linked to a device |

Note: `DELETED` and `UNLINKED` exist in the proto enum but are not supported by the audit log query.

When the user asks "what changed" (or equivalent wording), default to `types: ["UPDATED"]` and do not include `LINKED` events unless the user explicitly asks for linking activity.

## Response Format

```json
{
  "events": [ ... ],
  "cursor": "pagination-cursor-string"
}
```

Each `DeviceProfileAuditEvent` contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique event ID |
| `event_type` | string | `CREATED`, `UPDATED`, or `LINKED` |
| `merchant_id` | string | Merchant token |
| `location_ids` | string[] | Associated locations |
| `employee_id` | string | Who made the change (or "SYSTEM") |
| `recorded_at` | string | Timestamp (RFC 3339) |
| `timezone` | string | Timezone of the event |
| `device_profile_id` | string | Device profile ID |
| `device_profile_name` | string | Profile name |
| `linked_device_id` | string | Device ID (LINKED events only) |
| `unlinked_device_id` | string | Device ID (UNLINKED events only) |
| `current_profile` | DeviceProfile | Full profile at event time (UPDATED events) |
| `previous_profile` | DeviceProfile | Profile before the change (UPDATED events) |

### DeviceProfile Object

The `current_profile` and `previous_profile` fields are parsed `DeviceProfile` proto objects (not raw JSON strings). They contain:

| Field | Description |
|-------|-------------|
| `id` | Profile ID |
| `name` | Profile name |
| `version` | Version number (incremented on each update) |
| `shared` | Whether profile is shared across devices |
| `type` | Profile type (see below) |
| `created_at` | Creation timestamp |
| `updated_at` | Last modified timestamp |
| `spos_settings` | SPOS app settings (type=SPOS) |
| `rtl_settings` | Retail app settings (type=RETAIL) |
| `kds_settings` | KDS app settings (type=KDS) |
| `rst_settings` | Restaurant app settings (type=RESTAURANT) |
| `rst_mobile_settings` | Restaurant mobile settings (type=RESTAURANT_MOBILE) |
| `terminal_api_settings` | Terminal API settings (type=TERMINAL_API) |
| `square_hardware_settings` | Hardware settings (type=SQUARE_HARDWARE) |
| `apos_settings` | APOS app settings (type=APOS) |
| `kds_expo_settings` | KDS Expo settings (type=KDS_EXPO) |
| `release_manager_settings` | Release Manager settings (type=RELEASE_MANAGER) |
| `fnb_kiosk_settings` | FNB Kiosk settings (type=FNBKIOSK) |
| `ipos_settings` | Invoices settings (type=INVOICES) |
| `kiosk_settings` | 1P Kiosk settings (type=KIOSK) |
| `squid_kiosk_settings` | SQUID Kiosk settings (type=SQUID_KIOSK) |

## Examples

### Query all profile changes for a merchant
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"types\":[\"CREATED\",\"UPDATED\",\"LINKED\"],\"limit\":200}"}'
```

### Query with time range
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"types\":[\"UPDATED\"],\"start_at\":\"2025-01-01T00:00:00Z\",\"end_at\":\"2025-01-31T23:59:59Z\",\"limit\":50}"}'
```

### Query specific location
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"location_ids\":[\"LOCATION_TOKEN\"],\"types\":[\"CREATED\",\"UPDATED\"],\"limit\":100}"}'
```

### Query by employee
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"employee_ids\":[\"EMPLOYEE_TOKEN\"],\"types\":[\"UPDATED\"],\"limit\":50}"}'
```

### Extract profile changes with jq
```bash
sq curl -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"MERCHANT_TOKEN\",\"types\":[\"UPDATED\"],\"limit\":10}"}' \
  | jq '.events[] | {recorded_at, event_type, device_profile_name, employee_id}'
```

## Environments

| Environment | URL |
|-------------|-----|
| **Staging** | `https://device-settings.stage.sqprod.co/_admin/rpc/call` |
| **Production** | `https://device-settings.sqprod.co/_admin/rpc/call` |

Always test in staging first before querying production data.

## Playpen Support

Test with device-settings playpen:
```bash
sq curl --playpen device-settings -L --post302 \
  'https://device-settings.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "squareup.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"TEST_MERCHANT\",\"types\":[\"CREATED\"],\"limit\":10}"}'
```

## Prerequisites

You need capabilities for the `device-settings` app in Registry.
Request access at: https://registry.sqprod.co/applications/device-settings

## Troubleshooting

**Error: "Permission denied"**
- Request device-settings capabilities in Registry

**Error: "merchant_id is required"**
- Ensure `merchant_id` is provided in `json_body`

**Empty results:**
- Verify merchant has device profiles
- Ensure `start_at`/`end_at` use UTC — all audit events are stored in UTC
- Try without location filter first
- Audit events are only recorded after the feature was deployed

**Timeout errors (10s RPC timeout):**
- Reduce the time range
- Reduce the limit parameter
- Add more specific filters (location_ids, employee_ids, types)

## Presenting Results

When displaying results, **group events by `device_profile_id`** and include the `device_profile_name` as the group heading. Within each group, list events in reverse chronological order. Example format:

### Profile: "Standard mode" (ID: 0vPztG39DC7VZw4IlkN12BCHyIB)

| Time | Event | Employee | Details |
|------|-------|----------|---------|
| Feb 12 18:48:33 | UPDATED | TMudo1Wa54EWi2iG | |
| Feb 12 18:21:14 | UPDATED | TMudo1Wa54EWi2iG | |
| Feb 11 22:28:50 | LINKED | TMudo1Wa54EWi2iG | → Device B90B2428... |

### Profile: "Retail mod" (ID: Hd6x6k7HcMo0YvTsXqQowBCHyIB)

| Time | Event | Employee | Details |
|------|-------|----------|---------|
| Feb 11 18:37:50 | LINKED | TMudo1Wa54EWi2iG | → Device BE2CF776... |

For `UPDATED` events, diff the `previous_profile` and `current_profile` objects field by field. Show each changed field using its **dot-notation nested path** and display the before → after values. This is required: do not report only "field changed" without showing both values. Example:

| Field | Previous | Current |
|-------|----------|---------|
| `rst_settings.checkout.tipping.enabled` | `false` | `true` |
| `rst_settings.checkout.tipping.default_percent` | `15` | `20` |
| `rst_settings.coursing.auto_fire_enabled` | `true` | `false` |

Omit unchanged fields. If the profiles are large, focus on the fields that actually differ.

When summarizing an `UPDATED` event in the top-level event table, include at least one concrete value change in `Details` (for example: ``passcodes_enabled: null -> true``). If multiple fields changed, either list each change inline or add a short per-event diff table directly below the event row.

## Tips

- Use `UPDATED` events to compare `current_profile` vs `previous_profile` to see exactly what changed
- For "what changed" requests, query only `UPDATED` events unless the user explicitly requests other event types
- Set `limit` to 200 (maximum) for comprehensive history
- Use pagination with `cursor` for large result sets
- Filter by `employee_ids` to see changes by a specific person
- Pipe results through `jq` for easier JSON parsing
