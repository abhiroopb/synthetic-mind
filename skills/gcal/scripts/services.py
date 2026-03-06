"""Google Calendar API service initialization."""

from googleapiclient.discovery import build, Resource

from .auth import require_auth


def get_calendar_service() -> Resource:
    """Get Google Calendar API v3 service."""
    creds = require_auth()
    return build("calendar", "v3", credentials=creds, cache_discovery=False)
