# Event Resource Reference

Load when working with event JSON structure, datetime API formats, reminders, or visibility settings.

## Event Resource

Key fields returned by the Calendar API:

```json
{
  "id": "event123",
  "status": "confirmed",
  "htmlLink": "https://www.google.com/calendar/event?eid=...",
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "location": "Conference Room A",
  "creator": { "email": "user@example.com", "self": true },
  "organizer": { "email": "user@example.com", "self": true },
  "start": { "dateTime": "2026-03-01T10:00:00-05:00", "timeZone": "America/New_York" },
  "end": { "dateTime": "2026-03-01T11:00:00-05:00", "timeZone": "America/New_York" },
  "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=10"],
  "attendees": [
    { "email": "alice@example.com", "responseStatus": "accepted", "organizer": true },
    { "email": "bob@example.com", "responseStatus": "needsAction" }
  ],
  "conferenceData": {
    "entryPoints": [
      { "entryPointType": "video", "uri": "https://meet.google.com/abc-defg-hij" }
    ]
  },
  "reminders": { "useDefault": false, "overrides": [{ "method": "popup", "minutes": 10 }] },
  "visibility": "default",
  "colorId": "5",
  "created": "2026-02-15T12:00:00.000Z",
  "updated": "2026-02-15T12:00:00.000Z"
}
```

## Datetime Formats

The API uses two mutually exclusive fields for start/end:

- **All-day**: `{"date": "2026-03-15"}` — end date is exclusive
- **Timed**: `{"dateTime": "2026-03-15T10:00:00-05:00", "timeZone": "America/New_York"}` — `timeZone` optional if offset included

## Reminders

```json
// Default reminders
{ "reminders": { "useDefault": true } }

// Custom reminders (methods: "email", "popup")
{ "reminders": { "useDefault": false, "overrides": [{ "method": "popup", "minutes": 10 }, { "method": "email", "minutes": 1440 }] } }
```

## Event Visibility

| Value | Meaning |
|-------|---------|
| `default` | Uses calendar default |
| `public` | Visible to all |
| `private` | Only attendees see details |
| `confidential` | Same as private (legacy) |
