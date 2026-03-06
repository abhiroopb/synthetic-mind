# Attendees & Conference Data

Load when managing attendees, checking RSVP statuses, or adding Google Meet links.

## Attendee Object

```json
{
  "email": "user@example.com",
  "displayName": "User Name",
  "responseStatus": "accepted",
  "optional": false,
  "organizer": false,
  "self": false,
  "comment": "Looking forward to it"
}
```

## Response Status Values

| Status | Meaning |
|--------|---------|
| `needsAction` | Not yet responded |
| `declined` | Declined |
| `tentative` | Tentatively accepted |
| `accepted` | Accepted |

## Conference Data (Google Meet)

To create a Google Meet link, include `conferenceData` and set `conferenceDataVersion=1`:

```json
{
  "conferenceData": {
    "createRequest": {
      "requestId": "unique-string",
      "conferenceSolutionKey": { "type": "hangoutsMeet" }
    }
  }
}
```

Response includes entry points:

```json
{
  "conferenceData": {
    "conferenceId": "abc-defg-hij",
    "conferenceSolution": { "key": { "type": "hangoutsMeet" }, "name": "Google Meet" },
    "entryPoints": [
      { "entryPointType": "video", "uri": "https://meet.google.com/abc-defg-hij" },
      { "entryPointType": "phone", "uri": "tel:+1-234-567-8901", "pin": "123456789" }
    ]
  }
}
```
