# Recurrence Rules & Event Colors

## Common Recurrence Rules (RRULE)

Pass RRULE strings via `--recurrence`. Uses RFC 5545 format.

| Rule | Meaning |
|------|---------|
| `RRULE:FREQ=DAILY;COUNT=5` | Daily for 5 days |
| `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR` | Every Mon, Wed, Fri |
| `RRULE:FREQ=WEEKLY;COUNT=10` | Weekly for 10 weeks |
| `RRULE:FREQ=MONTHLY;BYMONTHDAY=1` | 1st of every month |
| `RRULE:FREQ=YEARLY;BYMONTH=12;BYMONTHDAY=25` | Every Dec 25 |
| `RRULE:FREQ=WEEKLY;UNTIL=20261231T000000Z` | Weekly until end of 2026 |
| `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` | Every weekday |
| `RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=MO` | Every other Monday |
| `RRULE:FREQ=MONTHLY;BYDAY=MO;BYSETPOS=1` | First Monday of month |
| `RRULE:FREQ=MONTHLY;BYDAY=FR;BYSETPOS=-1` | Last Friday of month |
| `RRULE:FREQ=MONTHLY;INTERVAL=3;BYMONTHDAY=1` | Quarterly on the 1st |

### RRULE Components

| Component | Values | Example |
|-----------|--------|---------|
| `FREQ` | `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY` | `FREQ=WEEKLY` |
| `COUNT` | Number of occurrences | `COUNT=10` |
| `UNTIL` | End date (UTC) | `UNTIL=20261231T000000Z` |
| `INTERVAL` | Repeat interval | `INTERVAL=2` (every 2 weeks) |
| `BYDAY` | Day of week | `BYDAY=MO,WE,FR` |
| `BYMONTHDAY` | Day of month | `BYMONTHDAY=1,15` |
| `BYMONTH` | Month | `BYMONTH=1,6` (Jan, Jun) |
| `BYSETPOS` | Position in set | `BYSETPOS=-1` (last occurrence) |

## Event Color IDs

Use `--color-id` when creating or updating events.

| ID | Color |
|----|-------|
| 1 | Lavender |
| 2 | Sage |
| 3 | Grape |
| 4 | Flamingo |
| 5 | Banana |
| 6 | Tangerine |
| 7 | Peacock |
| 8 | Graphite |
| 9 | Blueberry |
| 10 | Basil |
| 11 | Tomato |
