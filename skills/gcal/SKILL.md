---
Skill name: gcal
Skill description: Use when scheduling, booking, creating, updating, deleting, cancelling, RSVPing to, checking, looking up, querying, finding, or managing calendar events. Also use for checking availability, free/busy lookups, adding Google Meet links, or working with recurring events.
roles: [frontend]
allowed-tools:
  - Bash(cd {{SKILL_DIR}} && uv run gcal-cli.py:*)
  - Read
---

# Google Calendar Skill

Manage Google Calendar events via a local Python CLI. Create, read, update, delete events, RSVP, check free/busy, and more.

**STOP** — Before proceeding, verify authentication. Run `cd {{SKILL_DIR}} && uv run gcal-cli.py auth status`. If `"authenticated": false`, **stop and ask the user** to run `cd {{SKILL_DIR}} && uv run gcal-cli.py auth login`. See [SETUP.md](SETUP.md) for full setup instructions.

## Quick Reference

All commands output JSON. Run from `{{SKILL_DIR}}`:

```bash
uv run gcal-cli.py <command> [options]
```

---

## Safety Rules

- ALWAYS confirm with the user before running destructive or notification-triggering operations: `events delete`, `events move`, `events update --attendees`, or `events create --attendees`.
- When deleting, show the event summary and date before proceeding.
- Prefer read-only commands (`events list`, `events get`, `calendars list`, `freebusy`) by default.

## Calendars

```bash
# List all calendars
uv run gcal-cli.py calendars list

# Include hidden calendars
uv run gcal-cli.py calendars list --show-hidden

# Get details for a specific calendar
uv run gcal-cli.py calendars get <calendar-id>
```

---

## Events

### List Events

```bash
# List upcoming events from primary calendar
uv run gcal-cli.py events list

# List today's events
uv run gcal-cli.py events list --time-min 2026-02-20T00:00:00Z --time-max 2026-02-21T00:00:00Z

# Search events
uv run gcal-cli.py events list --query "standup"

# List events from a specific calendar
uv run gcal-cli.py events list --calendar <calendar-id> --limit 50

# List without expanding recurring events
uv run gcal-cli.py events list --no-single-events --order-by updated
```

### Get Event Details

```bash
uv run gcal-cli.py events get <event-id>
uv run gcal-cli.py events get <event-id> --calendar <calendar-id>
```

### Create Events

```bash
# Simple timed event
uv run gcal-cli.py events create \
  --summary "Team standup" \
  --start 2026-02-20T10:00:00-05:00 \
  --end 2026-02-20T10:30:00-05:00

# All-day event (use YYYY-MM-DD format)
uv run gcal-cli.py events create \
  --summary "Company holiday" \
  --start 2026-12-25 \
  --end 2026-12-26

# Event with all options
uv run gcal-cli.py events create \
  --summary "Project review" \
  --start 2026-03-01T14:00:00Z \
  --end 2026-03-01T15:00:00Z \
  --description "Quarterly project review meeting" \
  --location "Conference Room A" \
  --attendees "alice@example.com,bob@example.com" \
  --timezone "America/New_York" \
  --conference \
  --visibility private \
  --color-id 5 \
  --reminders '[{"method":"popup","minutes":10},{"method":"email","minutes":30}]'

# Weekly recurring event
uv run gcal-cli.py events create \
  --summary "Weekly 1:1" \
  --start 2026-03-02T11:00:00Z \
  --end 2026-03-02T11:30:00Z \
  --recurrence "RRULE:FREQ=WEEKLY;COUNT=10"

# Event with Google Meet
uv run gcal-cli.py events create \
  --summary "Remote sync" \
  --start 2026-03-01T09:00:00Z \
  --end 2026-03-01T09:30:00Z \
  --conference
```

### Quick Add (Natural Language)

```bash
uv run gcal-cli.py events quick-add "Lunch tomorrow at noon"
uv run gcal-cli.py events quick-add "Meeting with Bob at 3pm on Friday"
uv run gcal-cli.py events quick-add "Dentist appointment March 15 10am-11am"
```

### Update Events

```bash
# Change event title
uv run gcal-cli.py events update <event-id> --summary "New title"

# Reschedule
uv run gcal-cli.py events update <event-id> \
  --start 2026-03-01T15:00:00Z \
  --end 2026-03-01T16:00:00Z

# Add attendees (replaces existing list)
uv run gcal-cli.py events update <event-id> \
  --attendees "alice@example.com,bob@example.com,carol@example.com"

# Update description and location
uv run gcal-cli.py events update <event-id> \
  --description "Updated agenda" \
  --location "Room B"
```

### Delete Events

```bash
# Delete without notifying attendees
uv run gcal-cli.py events delete <event-id>

# Delete and notify attendees
uv run gcal-cli.py events delete <event-id> --notify
```

### Move Events Between Calendars

```bash
uv run gcal-cli.py events move <event-id> --to <destination-calendar-id>
```

### Recurring Event Instances

```bash
# List instances of a recurring event
uv run gcal-cli.py events instances <recurring-event-id>

# List instances in a time range
uv run gcal-cli.py events instances <recurring-event-id> \
  --time-min 2026-03-01T00:00:00Z \
  --time-max 2026-04-01T00:00:00Z
```

---

## RSVP

```bash
# Accept an event
uv run gcal-cli.py rsvp <event-id> --status accept

# Decline with a comment
uv run gcal-cli.py rsvp <event-id> --status decline --comment "Out of office"

# Mark as tentative
uv run gcal-cli.py rsvp <event-id> --status tentative
```

---

## Free/Busy

```bash
# Check your availability
uv run gcal-cli.py freebusy \
  --time-min 2026-02-20T08:00:00Z \
  --time-max 2026-02-20T18:00:00Z

# Check multiple calendars
uv run gcal-cli.py freebusy \
  --time-min 2026-02-20T08:00:00Z \
  --time-max 2026-02-20T18:00:00Z \
  --calendars "primary,alice@example.com,bob@example.com"

# With timezone
uv run gcal-cli.py freebusy \
  --time-min 2026-02-20T08:00:00Z \
  --time-max 2026-02-20T18:00:00Z \
  --timezone "America/Los_Angeles"
```

---

## Datetime Formats

- **All-day events**: Use `YYYY-MM-DD` (e.g., `2026-03-15`). End date is exclusive.
- **Timed events**: Use ISO 8601 with offset (e.g., `2026-03-15T10:00:00-05:00`) or UTC (e.g., `2026-03-15T15:00:00Z`).
- Use `--timezone` flag to set IANA timezone for events without an offset.

---

## Reference Files

Load when needed:

| File | When to load |
|------|--------------|
| [SETUP.md](SETUP.md) | First-time setup, authentication, troubleshooting |
| [references/event-resource.md](references/event-resource.md) | Inspecting event JSON structure, datetime API formats, reminders, visibility |
| [references/attendees-and-conference.md](references/attendees-and-conference.md) | Managing attendees, checking RSVP statuses, adding Google Meet links |
| [references/freebusy-and-calendars.md](references/freebusy-and-calendars.md) | Querying availability, calendar metadata, access roles, API limits |
| [references/recurrence-and-colors.md](references/recurrence-and-colors.md) | Writing RRULE strings, choosing event color IDs |

## Related Skills

- **gdrive** — When working with Google Drive, Docs, Sheets, or Slides (shares OAuth infrastructure)
