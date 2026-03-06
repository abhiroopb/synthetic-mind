# Free/Busy & Calendar List

Load when querying availability, inspecting calendar metadata, or checking access roles and API limits.

## Free/Busy Query

Request:
```json
{
  "timeMin": "2026-03-01T00:00:00Z",
  "timeMax": "2026-03-02T00:00:00Z",
  "timeZone": "America/New_York",
  "items": [{ "id": "primary" }, { "id": "alice@example.com" }]
}
```

Response:
```json
{
  "calendars": {
    "primary": { "busy": [{ "start": "2026-03-01T10:00:00Z", "end": "2026-03-01T11:00:00Z" }] },
    "alice@example.com": { "busy": [{ "start": "2026-03-01T09:00:00Z", "end": "2026-03-01T10:30:00Z" }] }
  }
}
```

## CalendarList Resource

```json
{
  "id": "user@example.com",
  "summary": "My Calendar",
  "description": "Personal calendar",
  "timeZone": "America/New_York",
  "backgroundColor": "#9a9cff",
  "foregroundColor": "#000000",
  "accessRole": "owner",
  "primary": true,
  "hidden": false
}
```

## Access Roles

| Role | Permissions |
|------|-------------|
| `owner` | Full control |
| `writer` | Create and modify events |
| `reader` | View events |
| `freeBusyReader` | Only see free/busy |

## API Limits

- Max results per page: 250 (events and calendarList)
- Max attendees per event: ~300
- Rate limits: ~1,000 queries per 100 seconds per user
