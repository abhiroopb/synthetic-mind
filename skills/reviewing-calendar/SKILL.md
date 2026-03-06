---
Skill name: reviewing-calendar
Skill description: Review Google Calendar events in a visual weekly view mirroring Google Calendar's format. Generates an HTML calendar showing events with conflict detection, color coding, and tooltips. Use when asked to review calendar, check calendar invites, view schedule, or show calendar events.
---

# Reviewing Calendar

Present calendar events inline in chat, one at a time, with surrounding context and conflict detection.

## Workflow

1. **Load gcal skill** for authentication and data fetching
2. **Fetch ALL events** (not just pending) for the date range
3. **Identify target events** based on user request (e.g., pending invites = `responseStatus: needsAction`)
4. **Present each event one at a time** using the inline format below
5. **Wait for user action** before showing the next event
6. **Execute RSVP** if requested, then show next event

## Fetching Events

```bash
cd ~/.agents/skills/gcal && uv run gcal-cli.py events list \
  --limit 300 \
  --time-min "YYYY-MM-DDTHH:MM:SS-07:00" \
  --time-max "YYYY-MM-DDTHH:MM:SS-07:00" 2>/dev/null
```

Parse the JSON to extract ALL events with each attendee's self status, AND identify the target events (e.g., pending invites where `"self": true` and `"responseStatus": "needsAction"`).

## Inline Presentation Format

Show **one event at a time**. For each event, show a 3-hour window before and after on the same day so the user can see context and conflicts.

### Format Template

```
### 📩 {Event Title}
**{Optional/Required}** · {Day of week} {Month} {Day} · {start} – {end} ({duration}) · from **{organizer}**

**Your calendar around this time:**

\```
  {time}  {status_icon} {Event name}
  {time}  {status_icon} {Event name}
          ·····························
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
 ┃  {time}  ⏳ {EVENT TITLE IN CAPS}                        ┃
 ┃           {duration} · {optional/required} · from {org}  ┃
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  {time}  🔶 {Conflicting event name}       ← CONFLICT (overlaps Xm)
          ·····························
  {time}  {status_icon} {Event name}
\```

⚠️ **{N} conflict(s)** with {event names}

**Accept, Decline, Tentative, or Skip?**
```

### Rules

- **The target event** is always inside the `┏━━━┓` box to make it visually prominent
- **Surrounding events** use status emoji but NO box — they must be visually subordinate
- **Conflicts** (events overlapping the target) get the 🔶 icon AND a `← CONFLICT (overlaps Xm)` annotation
- **Free gaps** shown as `·····························` separator
- **Status icons** for surrounding events:
  - ✅ accepted
  - ❌ declined
  - ❓ tentative
  - ⏳ needs action
  - 👤 you organize
  - 🔶 conflicts with this invite
- **Cancelled/Outdated** events get a ⛔ tag in the header
- **Only show 3 hours before and 3 hours after** the target event on the same day
- **One event per message** — wait for user input before showing the next

## After Each Event

Wait for the user to say one of:
- **Accept** → RSVP accept, confirm, show next
- **Decline** → Ask for optional comment, RSVP decline, confirm, show next
- **Tentative** → RSVP tentative, confirm, show next
- **Skip** → Show next without action

Also support batch commands like "accept this and the next 3" or "decline all office hours".

## RSVP Commands

```bash
# Accept
cd ~/.agents/skills/gcal && uv run gcal-cli.py rsvp <event-id> --status accept

# Decline
cd ~/.agents/skills/gcal && uv run gcal-cli.py rsvp <event-id> --status decline --comment "reason"

# Tentative
cd ~/.agents/skills/gcal && uv run gcal-cli.py rsvp <event-id> --status tentative
```
