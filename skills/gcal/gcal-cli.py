#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client>=2.174.0,<3",
#     "google-auth-httplib2>=0.2.0,<1",
#     "google-auth-oauthlib>=1.2.1,<2",
#     "click>=8.0.0,<9",
# ]
# ///
"""Google Calendar CLI for agent skills."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import click

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts import auth
from scripts.services import get_calendar_service


def output_json(data: dict | list) -> None:
    """Print data as JSON to stdout."""
    click.echo(json.dumps(data, indent=2, default=str))


def handle_error(e: Exception) -> None:
    """Handle errors with JSON output."""
    output_json({"error": str(e), "type": type(e).__name__})
    sys.exit(1)


def parse_datetime(value: str) -> dict:
    """Parse a datetime string into a Google Calendar API date or dateTime dict.

    - YYYY-MM-DD → {"date": "..."}  (all-day event)
    - Anything else → {"dateTime": "..."}  (timed event)
    """
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return {"date": value}
    return {"dateTime": value}


def parse_datetime_with_tz(value: str, timezone: str | None) -> dict:
    """Parse datetime and optionally attach a timeZone."""
    result = parse_datetime(value)
    if timezone and "dateTime" in result:
        result["timeZone"] = timezone
    return result


@click.group()
def cli():
    """Google Calendar CLI for agent skills."""
    pass


# =============================================================================
# Auth commands
# =============================================================================

@cli.group()
def auth_cmd():
    """Authentication commands."""
    pass


@auth_cmd.command("login")
@click.option("--force", is_flag=True, help="Force re-authentication")
def auth_login(force: bool):
    """Authenticate with Google OAuth."""
    try:
        result = auth.login(force=force)
        output_json(result)
    except Exception as e:
        handle_error(e)


@auth_cmd.command("status")
def auth_status():
    """Check authentication status."""
    output_json(auth.get_auth_status())


@auth_cmd.command("logout")
def auth_logout():
    """Remove stored credentials."""
    output_json(auth.logout())


# Alias 'auth' group
cli.add_command(auth_cmd, name="auth")


# =============================================================================
# Calendars commands
# =============================================================================

@cli.group()
def calendars():
    """Calendar management commands."""
    pass


@calendars.command("list")
@click.option("--limit", default=100, help="Maximum calendars to return")
@click.option("--show-hidden", is_flag=True, help="Include hidden calendars")
def calendars_list(limit: int, show_hidden: bool):
    """List available calendars."""
    try:
        service = get_calendar_service()

        params = {
            "maxResults": min(limit, 250),
            "showHidden": show_hidden,
        }

        result = service.calendarList().list(**params).execute()
        items = result.get("items", [])

        calendars_data = []
        for cal in items:
            calendars_data.append({
                "id": cal.get("id"),
                "summary": cal.get("summary"),
                "description": cal.get("description"),
                "primary": cal.get("primary", False),
                "accessRole": cal.get("accessRole"),
                "backgroundColor": cal.get("backgroundColor"),
                "timeZone": cal.get("timeZone"),
                "hidden": cal.get("hidden", False),
            })

        output_json({
            "count": len(calendars_data),
            "calendars": calendars_data,
        })
    except Exception as e:
        handle_error(e)


@calendars.command("get")
@click.argument("calendar_id")
def calendars_get(calendar_id: str):
    """Get details for a specific calendar."""
    try:
        service = get_calendar_service()
        result = service.calendarList().get(calendarId=calendar_id).execute()
        output_json(result)
    except Exception as e:
        handle_error(e)


# =============================================================================
# Events commands
# =============================================================================

@cli.group()
def events():
    """Event management commands."""
    pass


@events.command("list")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--time-min", default=None, help="Start of time range (ISO 8601)")
@click.option("--time-max", default=None, help="End of time range (ISO 8601)")
@click.option("--query", "q", default=None, help="Free text search query")
@click.option("--limit", default=25, help="Maximum events to return")
@click.option("--single-events", is_flag=True, default=True, help="Expand recurring events (default: true)")
@click.option("--no-single-events", is_flag=True, help="Don't expand recurring events")
@click.option("--order-by", default="startTime", type=click.Choice(["startTime", "updated"]),
              help="Sort order (default: startTime, requires single-events)")
def events_list(calendar_id: str, time_min: str | None, time_max: str | None,
                q: str | None, limit: int, single_events: bool,
                no_single_events: bool, order_by: str):
    """List events from a calendar."""
    try:
        service = get_calendar_service()

        use_single_events = single_events and not no_single_events

        params = {
            "calendarId": calendar_id,
            "maxResults": min(limit, 2500),
            "singleEvents": use_single_events,
        }

        if use_single_events:
            params["orderBy"] = order_by

        if time_min:
            params["timeMin"] = time_min
        if time_max:
            params["timeMax"] = time_max
        if q:
            params["q"] = q

        result = service.events().list(**params).execute()
        items = result.get("items", [])

        output_json({
            "count": len(items),
            "calendar": calendar_id,
            "timeZone": result.get("timeZone"),
            "events": items,
        })
    except Exception as e:
        handle_error(e)


@events.command("get")
@click.argument("event_id")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
def events_get(event_id: str, calendar_id: str):
    """Get details for a specific event."""
    try:
        service = get_calendar_service()
        result = service.events().get(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()
        output_json(result)
    except Exception as e:
        handle_error(e)


@events.command("create")
@click.option("--summary", required=True, help="Event title")
@click.option("--start", required=True, help="Start time (ISO 8601 or YYYY-MM-DD for all-day)")
@click.option("--end", required=True, help="End time (ISO 8601 or YYYY-MM-DD for all-day)")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--description", default=None, help="Event description")
@click.option("--location", default=None, help="Event location")
@click.option("--attendees", default=None, help="Comma-separated email addresses")
@click.option("--timezone", default=None, help="IANA timezone (e.g., America/New_York)")
@click.option("--recurrence", default=None, help="RRULE string (e.g., RRULE:FREQ=WEEKLY;COUNT=10)")
@click.option("--conference", is_flag=True, help="Add Google Meet link")
@click.option("--visibility", default=None, type=click.Choice(["default", "public", "private", "confidential"]),
              help="Event visibility")
@click.option("--reminders", default=None, help="JSON reminder overrides (e.g., [{\"method\":\"popup\",\"minutes\":10}])")
@click.option("--color-id", default=None, help="Event color ID (1-11)")
def events_create(summary: str, start: str, end: str, calendar_id: str,
                  description: str | None, location: str | None,
                  attendees: str | None, timezone: str | None,
                  recurrence: str | None, conference: bool,
                  visibility: str | None, reminders: str | None,
                  color_id: str | None):
    """Create a new calendar event."""
    try:
        service = get_calendar_service()

        event_body: dict = {
            "summary": summary,
            "start": parse_datetime_with_tz(start, timezone),
            "end": parse_datetime_with_tz(end, timezone),
        }

        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location
        if visibility:
            event_body["visibility"] = visibility
        if color_id:
            event_body["colorId"] = color_id

        if attendees:
            event_body["attendees"] = [
                {"email": email.strip()} for email in attendees.split(",")
            ]

        if recurrence:
            event_body["recurrence"] = [recurrence]

        if conference:
            event_body["conferenceData"] = {
                "createRequest": {
                    "requestId": f"gcal-skill-{hash(summary) % 10**8}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            }

        if reminders:
            event_body["reminders"] = {
                "useDefault": False,
                "overrides": json.loads(reminders),
            }

        params = {
            "calendarId": calendar_id,
            "body": event_body,
        }
        if conference:
            params["conferenceDataVersion"] = 1

        result = service.events().insert(**params).execute()
        output_json(result)
    except Exception as e:
        handle_error(e)


@events.command("update")
@click.argument("event_id")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--summary", default=None, help="New event title")
@click.option("--start", default=None, help="New start time (ISO 8601 or YYYY-MM-DD)")
@click.option("--end", default=None, help="New end time (ISO 8601 or YYYY-MM-DD)")
@click.option("--description", default=None, help="New event description")
@click.option("--location", default=None, help="New event location")
@click.option("--attendees", default=None, help="Comma-separated email addresses (replaces existing)")
@click.option("--timezone", default=None, help="IANA timezone (e.g., America/New_York)")
@click.option("--recurrence", default=None, help="RRULE string")
@click.option("--visibility", default=None, type=click.Choice(["default", "public", "private", "confidential"]))
@click.option("--color-id", default=None, help="Event color ID (1-11)")
@click.option("--reminders", default=None, help="JSON reminder overrides")
def events_update(event_id: str, calendar_id: str, summary: str | None,
                  start: str | None, end: str | None, description: str | None,
                  location: str | None, attendees: str | None,
                  timezone: str | None, recurrence: str | None,
                  visibility: str | None, color_id: str | None,
                  reminders: str | None):
    """Update an existing calendar event."""
    try:
        service = get_calendar_service()

        # Fetch existing event to merge changes
        existing = service.events().get(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()

        if summary is not None:
            existing["summary"] = summary
        if description is not None:
            existing["description"] = description
        if location is not None:
            existing["location"] = location
        if visibility is not None:
            existing["visibility"] = visibility
        if color_id is not None:
            existing["colorId"] = color_id

        if start is not None:
            existing["start"] = parse_datetime_with_tz(start, timezone)
        if end is not None:
            existing["end"] = parse_datetime_with_tz(end, timezone)

        if attendees is not None:
            existing["attendees"] = [
                {"email": email.strip()} for email in attendees.split(",")
            ]

        if recurrence is not None:
            existing["recurrence"] = [recurrence]

        if reminders is not None:
            existing["reminders"] = {
                "useDefault": False,
                "overrides": json.loads(reminders),
            }

        result = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=existing,
        ).execute()

        output_json(result)
    except Exception as e:
        handle_error(e)


@events.command("delete")
@click.argument("event_id")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--notify", is_flag=True, help="Send cancellation notifications to attendees")
def events_delete(event_id: str, calendar_id: str, notify: bool):
    """Delete a calendar event."""
    try:
        service = get_calendar_service()

        params = {
            "calendarId": calendar_id,
            "eventId": event_id,
        }
        if notify:
            params["sendUpdates"] = "all"

        service.events().delete(**params).execute()

        output_json({
            "status": "ok",
            "message": f"Deleted event {event_id}",
            "calendar": calendar_id,
        })
    except Exception as e:
        handle_error(e)


@events.command("quick-add")
@click.argument("text")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
def events_quick_add(text: str, calendar_id: str):
    """Create an event using natural language text.

    Examples:
        "Lunch tomorrow at noon"
        "Meeting with Bob at 3pm on Friday"
        "Dentist appointment March 15 10am-11am"
    """
    try:
        service = get_calendar_service()

        result = service.events().quickAdd(
            calendarId=calendar_id,
            text=text,
        ).execute()

        output_json(result)
    except Exception as e:
        handle_error(e)


@events.command("move")
@click.argument("event_id")
@click.option("--to", "dest_calendar", required=True, help="Destination calendar ID")
@click.option("--calendar", "calendar_id", default="primary", help="Source calendar ID (default: primary)")
def events_move(event_id: str, dest_calendar: str, calendar_id: str):
    """Move an event to a different calendar."""
    try:
        service = get_calendar_service()

        result = service.events().move(
            calendarId=calendar_id,
            eventId=event_id,
            destination=dest_calendar,
        ).execute()

        output_json(result)
    except Exception as e:
        handle_error(e)


@events.command("instances")
@click.argument("event_id")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--time-min", default=None, help="Start of time range (ISO 8601)")
@click.option("--time-max", default=None, help="End of time range (ISO 8601)")
@click.option("--limit", default=25, help="Maximum instances to return")
def events_instances(event_id: str, calendar_id: str, time_min: str | None,
                     time_max: str | None, limit: int):
    """List instances of a recurring event."""
    try:
        service = get_calendar_service()

        params = {
            "calendarId": calendar_id,
            "eventId": event_id,
            "maxResults": min(limit, 2500),
        }

        if time_min:
            params["timeMin"] = time_min
        if time_max:
            params["timeMax"] = time_max

        result = service.events().instances(**params).execute()
        items = result.get("items", [])

        output_json({
            "count": len(items),
            "recurringEventId": event_id,
            "instances": items,
        })
    except Exception as e:
        handle_error(e)


# =============================================================================
# RSVP command
# =============================================================================

@cli.command()
@click.argument("event_id")
@click.option("--status", "response_status", required=True,
              type=click.Choice(["accept", "decline", "tentative"]),
              help="RSVP response")
@click.option("--calendar", "calendar_id", default="primary", help="Calendar ID (default: primary)")
@click.option("--comment", default=None, help="Optional comment with RSVP")
def rsvp(event_id: str, response_status: str, calendar_id: str, comment: str | None):
    """RSVP to a calendar event (accept, decline, or tentative)."""
    try:
        service = get_calendar_service()

        # Map friendly names to API values
        status_map = {
            "accept": "accepted",
            "decline": "declined",
            "tentative": "tentative",
        }
        api_status = status_map[response_status]

        # Get the user's email from the primary calendar
        cal_meta = service.calendarList().get(calendarId="primary").execute()
        user_email = cal_meta.get("id", "")

        # Get the event
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()

        # Find and update the attendee entry
        attendees = event.get("attendees", [])
        found = False
        for attendee in attendees:
            if attendee.get("email", "").lower() == user_email.lower() or attendee.get("self", False):
                attendee["responseStatus"] = api_status
                if comment:
                    attendee["comment"] = comment
                found = True
                break

        if not found:
            output_json({
                "error": "You are not listed as an attendee of this event",
                "userEmail": user_email,
                "eventId": event_id,
            })
            sys.exit(1)

        event["attendees"] = attendees

        result = service.events().patch(
            calendarId=calendar_id,
            eventId=event_id,
            body={"attendees": attendees},
            sendUpdates="all",
        ).execute()

        output_json({
            "status": "ok",
            "responseStatus": api_status,
            "eventId": event_id,
            "summary": result.get("summary"),
        })
    except Exception as e:
        handle_error(e)


# =============================================================================
# Free/Busy command
# =============================================================================

@cli.command()
@click.option("--time-min", required=True, help="Start of time range (ISO 8601)")
@click.option("--time-max", required=True, help="End of time range (ISO 8601)")
@click.option("--calendars", default=None, help="Comma-separated calendar IDs (default: primary)")
@click.option("--timezone", default=None, help="IANA timezone (e.g., America/New_York)")
def freebusy(time_min: str, time_max: str, calendars: str | None, timezone: str | None):
    """Query free/busy information for calendars."""
    try:
        service = get_calendar_service()

        calendar_ids = [c.strip() for c in calendars.split(",")] if calendars else ["primary"]

        body: dict = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": cid} for cid in calendar_ids],
        }

        if timezone:
            body["timeZone"] = timezone

        result = service.freebusy().query(body=body).execute()

        # Simplify the output
        busy_data = {}
        for cal_id, cal_info in result.get("calendars", {}).items():
            busy_data[cal_id] = {
                "busy": cal_info.get("busy", []),
                "errors": cal_info.get("errors", []),
            }

        output_json({
            "timeMin": result.get("timeMin"),
            "timeMax": result.get("timeMax"),
            "calendars": busy_data,
        })
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    cli()
