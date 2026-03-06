#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx~=0.28.1",
#     "click~=8.3.1",
# ]
# ///
"""Slack CLI for agent skills - wraps the Slack Web API directly."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import httpx

# Config paths
CONFIG_DIR = Path.home() / ".config" / "slack-skill"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"

# Slack API base URL
SLACK_API_BASE = "https://slack.com/api"

# OAuth URL for token generation
OAUTH_URL = (
    "https://sq-block.slack.com/oauth/v2/authorize?"
    "client_id=5596012676549.8524078629858&"
    "scope=channels:read&"
    "user_scope=bookmarks:read,bookmarks:write,canvases:read,canvases:write,"
    "channels:history,channels:read,channels:write,channels:write.invites,"
    "channels:write.topic,chat:write,dnd:read,dnd:write,emoji:read,"
    "groups:history,groups:read,groups:write,groups:write.invites,"
    "groups:write.topic,identify,im:history,im:read,im:write,im:write.topic,"
    "links:read,mpim:history,mpim:read,mpim:write,mpim:write.topic,"
    "pins:read,pins:write,reactions:read,reactions:write,reminders:read,"
    "reminders:write,search:read,stars:read,stars:write,usergroups:read,"
    "usergroups:write,users.profile:read,users.profile:write,users:read,"
    "users:read.email,users:write,workflows.templates:read,"
    "workflows.templates:write,files:read,files:write"
)

# Known workspace IDs
DEFAULT_WORKSPACES = {
    "block": "T05HJ0CKWG5",
    "square": "T024FALR8",
    "cashapp": "T01H5TZGHUJ",
    "tidal": "T0414TYF4",
}


# =============================================================================
# Slack API Client
# =============================================================================

class SlackClient:
    """Simple Slack Web API client using httpx."""

    def __init__(self, token: str, workspace_id: str = ""):
        self.token = token
        self.workspace_id = workspace_id
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=SLACK_API_BASE,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _call(self, method: str, params: Optional[dict] = None, json_body: Optional[dict] = None) -> dict:
        """Call a Slack API method."""
        client = await self._get_client()

        if json_body:
            resp = await client.post(f"/{method}", json=json_body)
        elif params:
            resp = await client.get(f"/{method}", params=params)
        else:
            resp = await client.get(f"/{method}")

        data = resp.json()
        if not data.get("ok"):
            error = data.get("error", "unknown_error")
            raise SlackAPIError(error, data)
        return data

    # Auth methods
    async def auth_test(self) -> dict:
        """Test authentication and get current user info."""
        return await self._call("auth.test")

    # User methods
    async def users_info(self, user_id: str) -> dict:
        """Get info about a user."""
        return await self._call("users.info", {"user": user_id})

    async def users_lookup_by_email(self, email: str) -> dict:
        """Look up user by email."""
        return await self._call("users.lookupByEmail", {"email": email})

    async def users_profile_get(self, user_id: Optional[str] = None) -> dict:
        """Get user profile."""
        params = {}
        if user_id:
            params["user"] = user_id
        return await self._call("users.profile.get", params)

    async def users_profile_set(self, profile: dict) -> dict:
        """Set user profile (status, etc)."""
        return await self._call("users.profile.set", json_body={"profile": profile})

    async def users_set_presence(self, presence: str) -> dict:
        """Set presence (auto or away)."""
        return await self._call("users.setPresence", json_body={"presence": presence})

    async def users_get_presence(self, user_id: str) -> dict:
        """Get user presence."""
        return await self._call("users.getPresence", {"user": user_id})

    async def users_list(self, limit: int = 200, cursor: str = "") -> dict:
        """List users in a workspace."""
        params = {"limit": min(limit, 1000)}
        if cursor:
            params["cursor"] = cursor
        if self.workspace_id:
            params["team_id"] = self.workspace_id
        return await self._call("users.list", params)

    async def resolve_username_to_user_id(self, username: str) -> Optional[str]:
        """Resolve a username to user ID.

        First tries email guesses with common company domains (fast, O(k) API calls).
        Falls back to paginating users.list if email guesses fail (slow, O(n) API calls).

        Returns user_id if found, None otherwise.
        """
        # Common Block/Square email domains - try these first
        # Based on sampling 14k users: squareup.com (68%), block.xyz (17%), tidal.com (2%), tbd.email (0.2%)
        email_domains = [
            "squareup.com",
            "block.xyz",
            "tidal.com",
            "tbd.email",
        ]

        # Try email guesses first (much faster than pagination)
        for domain in email_domains:
            try:
                email = f"{username}@{domain}"
                result = await self.users_lookup_by_email(email)
                if result.get("ok") and result.get("user"):
                    return result["user"]["id"]
            except SlackAPIError as e:
                # users_not_found is expected, continue to next domain
                if e.error != "users_not_found":
                    raise

        # Fall back to pagination (slow, but handles edge cases)
        cursor = ""
        while True:
            result = await self.users_list(limit=200, cursor=cursor)
            for user in result.get("members", []):
                # Check both name (login) and display_name
                if user.get("name") == username:
                    return user.get("id")
                profile = user.get("profile", {})
                if profile.get("display_name") == username:
                    return user.get("id")
            cursor = result.get("response_metadata", {}).get("next_cursor", "")
            if not cursor:
                break
        return None

    # Conversations methods
    async def conversations_list(self, types: str = "public_channel,private_channel",
                                  limit: int = 200, cursor: str = "",
                                  exclude_archived: bool = True) -> dict:
        """List conversations the user is in."""
        params = {
            "types": types,
            "limit": min(limit, 1000),
            "exclude_archived": "true" if exclude_archived else "false"
        }
        if cursor:
            params["cursor"] = cursor
        if self.workspace_id:
            params["team_id"] = self.workspace_id
        return await self._call("conversations.list", params)

    async def conversations_info(self, channel_id: str) -> dict:
        """Get info about a conversation."""
        return await self._call("conversations.info", {"channel": channel_id})

    async def conversations_history(self, channel_id: str, limit: int = 30,
                                     cursor: str = "", oldest: str = "",
                                     latest: str = "", inclusive: bool = False) -> dict:
        """Get messages from a conversation."""
        params = {"channel": channel_id, "limit": min(limit, 100)}
        if cursor:
            params["cursor"] = cursor
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        if inclusive:
            params["inclusive"] = "true"
        return await self._call("conversations.history", params)

    async def conversations_replies(self, channel_id: str, ts: str,
                                     limit: int = 100, cursor: str = "") -> dict:
        """Get thread replies."""
        params = {
            "channel": channel_id,
            "ts": ts,
            "limit": min(limit, 100),
        }
        if cursor:
            params["cursor"] = cursor
        return await self._call("conversations.replies", params)

    async def conversations_open(self, users: str = "", channel: str = "") -> dict:
        """Open or resume a DM."""
        params = {}
        if users:
            params["users"] = users
        if channel:
            params["channel"] = channel
        return await self._call("conversations.open", json_body=params)

    async def conversations_create(self, name: str, is_private: bool = False) -> dict:
        """Create a channel."""
        params = {"name": name, "is_private": is_private}
        if self.workspace_id:
            params["team_id"] = self.workspace_id
        return await self._call("conversations.create", json_body=params)

    async def conversations_archive(self, channel_id: str) -> dict:
        """Archive a channel."""
        return await self._call("conversations.archive", json_body={"channel": channel_id})

    async def conversations_unarchive(self, channel_id: str) -> dict:
        """Unarchive a channel."""
        return await self._call("conversations.unarchive", json_body={"channel": channel_id})

    async def conversations_rename(self, channel_id: str, name: str) -> dict:
        """Rename a channel."""
        return await self._call("conversations.rename", json_body={
            "channel": channel_id,
            "name": name,
        })

    async def conversations_join(self, channel_id: str) -> dict:
        """Join a channel."""
        return await self._call("conversations.join", json_body={"channel": channel_id})

    async def conversations_leave(self, channel_id: str) -> dict:
        """Leave a channel."""
        return await self._call("conversations.leave", json_body={"channel": channel_id})

    async def conversations_invite(self, channel_id: str, user_ids: list[str]) -> dict:
        """Invite users to a channel."""
        return await self._call("conversations.invite", json_body={
            "channel": channel_id,
            "users": ",".join(user_ids),
        })

    async def conversations_kick(self, channel_id: str, user_id: str) -> dict:
        """Remove a user from a channel."""
        return await self._call("conversations.kick", json_body={
            "channel": channel_id,
            "user": user_id,
        })

    async def conversations_set_topic(self, channel_id: str, topic: str) -> dict:
        """Set channel topic."""
        return await self._call("conversations.setTopic", json_body={
            "channel": channel_id,
            "topic": topic,
        })

    async def conversations_set_purpose(self, channel_id: str, purpose: str) -> dict:
        """Set channel purpose/description."""
        return await self._call("conversations.setPurpose", json_body={
            "channel": channel_id,
            "purpose": purpose,
        })

    async def conversations_mark(self, channel_id: str, ts: str) -> dict:
        """Mark a channel as read up to a timestamp."""
        return await self._call("conversations.mark", json_body={
            "channel": channel_id,
            "ts": ts,
        })

    async def conversations_close(self, channel_id: str) -> dict:
        """Close a DM or MPIM."""
        return await self._call("conversations.close", json_body={"channel": channel_id})

    async def conversations_members(self, channel_id: str, limit: int = 100,
                                      cursor: str = "") -> dict:
        """Get channel members."""
        params = {
            "channel": channel_id,
            "limit": min(limit, 1000),
        }
        if cursor:
            params["cursor"] = cursor
        return await self._call("conversations.members", params)

    # Chat methods
    async def chat_post_message(self, channel: str, text: str = "",
                                 thread_ts: str = "", blocks: Optional[list] = None) -> dict:
        """Post a message."""
        payload = {"channel": channel}
        if text:
            payload["text"] = text
        if thread_ts:
            payload["thread_ts"] = thread_ts
        if blocks:
            payload["blocks"] = blocks
        return await self._call("chat.postMessage", json_body=payload)

    async def chat_update(self, channel: str, ts: str, text: str) -> dict:
        """Update a message."""
        return await self._call("chat.update", json_body={
            "channel": channel,
            "ts": ts,
            "text": text,
        })

    async def chat_delete(self, channel: str, ts: str) -> dict:
        """Delete a message."""
        return await self._call("chat.delete", json_body={"channel": channel, "ts": ts})

    # Reactions methods
    async def reactions_add(self, channel: str, timestamp: str, name: str) -> dict:
        """Add a reaction."""
        return await self._call("reactions.add", json_body={
            "channel": channel,
            "timestamp": timestamp,
            "name": name,
        })

    async def reactions_remove(self, channel: str, timestamp: str, name: str) -> dict:
        """Remove a reaction."""
        return await self._call("reactions.remove", json_body={
            "channel": channel,
            "timestamp": timestamp,
            "name": name,
        })

    async def reactions_get(self, channel: str, timestamp: str) -> dict:
        """Get reactions for a message."""
        return await self._call("reactions.get", {
            "channel": channel,
            "timestamp": timestamp,
            "full": "true",
        })

    # Search methods
    async def search_messages(self, query: str, count: int = 20,
                               sort: str = "score", sort_dir: str = "desc",
                               page: int = 1) -> dict:
        """Search messages."""
        params = {
            "query": query,
            "count": min(count, 100),
            "sort": sort,
            "sort_dir": sort_dir,
            "page": page,
        }
        if self.workspace_id:
            params["team_id"] = self.workspace_id
        return await self._call("search.messages", params)

    # DND methods
    async def dnd_set_snooze(self, num_minutes: int) -> dict:
        """Enable DND."""
        return await self._call("dnd.setSnooze", {"num_minutes": num_minutes})

    async def dnd_end_snooze(self) -> dict:
        """End DND."""
        return await self._call("dnd.endSnooze")

    async def dnd_info(self, user_id: Optional[str] = None) -> dict:
        """Get DND info."""
        params = {}
        if user_id:
            params["user"] = user_id
        return await self._call("dnd.info", params if params else None)


class SlackAPIError(Exception):
    """Slack API error."""
    def __init__(self, error: str, response: dict):
        self.error = error
        self.response = response
        super().__init__(error)


# =============================================================================
# Helpers
# =============================================================================

def output_json(data: dict | list) -> None:
    """Print data as JSON to stdout."""
    click.echo(json.dumps(data, indent=2, default=str))


def handle_error(e: Exception) -> None:
    """Handle errors with JSON output."""
    if isinstance(e, SlackAPIError):
        output_json({"error": e.error, "type": "SlackAPIError", "response": e.response})
    else:
        output_json({"error": str(e), "type": type(e).__name__})
    sys.exit(1)


def load_config() -> dict:
    """Load configuration from credentials file."""
    if not CREDENTIALS_FILE.exists():
        return {}
    try:
        return json.loads(CREDENTIALS_FILE.read_text())
    except Exception:
        return {}


def save_config(config: dict) -> None:
    """Save configuration to credentials file with secure permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_FILE.write_text(json.dumps(config, indent=2))
    CREDENTIALS_FILE.chmod(0o600)


def get_token() -> str:
    """Get Slack token from config or environment."""
    env_token = os.environ.get("SLACK_TOKEN")
    if env_token:
        return env_token

    config = load_config()
    token = config.get("token", "")
    if not token:
        output_json({
            "ok": False,
            "error": "No Slack token configured",
            "error_type": "auth_required",
            "action_required": "Run: uv run slack-cli.py auth login",
            "message": "Authentication required. Run 'uv run slack-cli.py auth login' to open the OAuth flow."
        })
        sys.exit(1)
    return token


def get_workspace_id(workspace: str = "", workspace_id: str = "") -> str:
    """Resolve workspace alias or ID to actual workspace ID."""
    if workspace_id:
        return workspace_id

    config = load_config()
    workspaces = config.get("workspaces", DEFAULT_WORKSPACES)

    if workspace:
        ws_lower = workspace.lower()
        if ws_lower in workspaces:
            return workspaces[ws_lower]
        if workspace.startswith("T"):
            return workspace
        raise click.ClickException(f"Unknown workspace: {workspace}. Known: {', '.join(workspaces.keys())}")

    default_ws = config.get("default_workspace") or os.environ.get("SLACK_DEFAULT_WORKSPACE_ID")
    if default_ws:
        return default_ws

    return DEFAULT_WORKSPACES["block"]


def run_async(coro):
    """Run an async coroutine."""
    return asyncio.run(coro)


def format_timestamp(ts: str) -> str:
    """Convert Slack timestamp to readable format."""
    try:
        unix_ts = float(ts.split(".")[0])
        dt = datetime.fromtimestamp(unix_ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts


def format_message(msg: dict, full_text: bool = False) -> dict:
    """Format a message for output."""
    text = msg.get("text", "")
    if not full_text and len(text) > 500:
        text = text[:500] + "... [truncated]"
    result = {
        "ts": msg.get("ts"),
        "time": format_timestamp(msg.get("ts", "")),
        "user": msg.get("user"),
        "text": text,
        "type": msg.get("type"),
        "subtype": msg.get("subtype"),
        "thread_ts": msg.get("thread_ts"),
        "reply_count": msg.get("reply_count", 0),
    }
    raw_files = msg.get("files")
    if raw_files:
        result["files"] = [{"id": f.get("id"), "name": f.get("name")} for f in raw_files]
    return result


# =============================================================================
# CLI Commands
# =============================================================================

@click.group()
def cli():
    """Slack CLI for agent skills."""
    pass


# =============================================================================
# Auth commands
# =============================================================================

@cli.group()
def auth():
    """Authentication commands."""
    pass


@auth.command("login")
@click.option("--token", default="", help="Slack token (xoxp-...) - if not provided, will prompt")
@click.option("--no-browser", is_flag=True, help="Don't open the browser automatically")
@click.option("--no-prompt", is_flag=True, help="Don't prompt for token - just open browser and exit")
def auth_login(token: str, no_browser: bool, no_prompt: bool):
    """Authenticate with Slack."""
    try:
        if not token:
            click.echo("=" * 60)
            click.echo("SLACK AUTHENTICATION")
            click.echo("=" * 60)
            click.echo()
            click.echo("Prerequisites:")
            click.echo("  • You MUST be connected to WARP VPN")
            click.echo()

            if not no_browser:
                click.echo("Opening Slack OAuth page in your browser...")
                click.echo()
                webbrowser.open(OAUTH_URL)
            else:
                click.echo("Open this URL in your browser:")
                click.echo()
                click.echo(f"  {OAUTH_URL}")
                click.echo()

            click.echo("After clicking 'Allow':")
            click.echo("  1. Copy the SLACK_TOKEN value (starts with xoxp-)")
            click.echo("  2. Copy the SLACK_DEFAULT_WORKSPACE_ID value")
            click.echo()

            if no_prompt:
                output_json({
                    "ok": True,
                    "status": "browser_opened",
                    "message": "Browser opened for OAuth. User should complete auth and then run: auth set-token --token <token>",
                    "oauth_url": OAUTH_URL,
                    "next_step": "After user clicks Allow and copies token, run: uv run slack-cli.py auth set-token --token <TOKEN> --workspace block"
                })
                return

            token = click.prompt("Paste your SLACK_TOKEN (xoxp-...)")

        if not token.startswith("xoxp-"):
            raise click.ClickException("Invalid token format. Token should start with 'xoxp-'")

        click.echo()
        click.echo("Which workspace should be the default?")
        click.echo("  1. Block (T05HJ0CKWG5)")
        click.echo("  2. Square (T024FALR8)")
        click.echo("  3. Cash App (T01H5TZGHUJ)")
        click.echo("  4. Tidal (T0414TYF4)")
        click.echo()

        choice = click.prompt("Enter number or workspace ID", default="1")

        workspace_map = {"1": "T05HJ0CKWG5", "2": "T024FALR8", "3": "T01H5TZGHUJ", "4": "T0414TYF4"}

        if choice in workspace_map:
            default_workspace = workspace_map[choice]
        elif choice.startswith("T"):
            default_workspace = choice
        else:
            default_workspace = "T05HJ0CKWG5"

        click.echo()
        click.echo("Validating token...")

        async def validate():
            client = SlackClient(token, default_workspace)
            try:
                result = await client.auth_test()
                return result
            finally:
                await client.close()

        auth_info = run_async(validate())

        config = {
            "token": token,
            "default_workspace": default_workspace,
            "workspaces": DEFAULT_WORKSPACES,
        }
        save_config(config)

        output_json({
            "ok": True,
            "message": "Authentication successful!",
            "user": {
                "id": auth_info.get("user_id"),
                "name": auth_info.get("user"),
                "team": auth_info.get("team"),
            },
            "default_workspace": default_workspace,
            "config_file": str(CREDENTIALS_FILE),
        })

    except Exception as e:
        handle_error(e)


@auth.command("status")
def auth_status():
    """Check authentication status."""
    config = load_config()

    if not config.get("token"):
        output_json({
            "authenticated": False,
            "message": "No token configured. Run: uv run slack-cli.py auth login",
        })
        return

    token = config.get("token", "")
    masked_token = f"{token[:10]}...{token[-4:]}" if len(token) > 14 else "****"

    output_json({
        "authenticated": True,
        "token": masked_token,
        "default_workspace": config.get("default_workspace"),
        "workspaces": config.get("workspaces", DEFAULT_WORKSPACES),
        "config_file": str(CREDENTIALS_FILE),
    })


@auth.command("set-token")
@click.option("--token", default="", help="Slack token (xoxp-...)")
@click.option("--workspace", default="block", help="Default workspace alias")
def auth_set_token(token: str, workspace: str):
    """Set the Slack token."""
    try:
        if not token:
            click.echo("Paste your Slack token (xoxp-...) and press Enter:")
            token = click.prompt("Token", hide_input=False)

        if not token.startswith("xoxp-"):
            raise click.ClickException("Invalid token format. Token should start with 'xoxp-'")

        workspace_id = DEFAULT_WORKSPACES.get(workspace.lower())
        if not workspace_id:
            if workspace.startswith("T"):
                workspace_id = workspace
            else:
                raise click.ClickException(f"Unknown workspace: {workspace}")

        async def validate():
            client = SlackClient(token, workspace_id)
            try:
                return await client.auth_test()
            finally:
                await client.close()

        auth_info = run_async(validate())

        config = {
            "token": token,
            "default_workspace": workspace_id,
            "workspaces": DEFAULT_WORKSPACES,
        }
        save_config(config)

        output_json({
            "ok": True,
            "message": "Authentication successful!",
            "user": {
                "id": auth_info.get("user_id"),
                "name": auth_info.get("user"),
            },
            "default_workspace": workspace_id,
            "config_file": str(CREDENTIALS_FILE),
        })

    except Exception as e:
        handle_error(e)


@auth.command("logout")
def auth_logout():
    """Remove stored credentials."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        output_json({"ok": True, "message": "Credentials removed"})
    else:
        output_json({"ok": True, "message": "No credentials to remove"})


@auth.command("callback")
@click.option("--port", default=9876, help="Port for local callback server")
@click.option("--workspace", default="block", help="Default workspace alias")
def auth_callback(port: int, workspace: str):
    """Start a local server to receive the token via web UI."""
    import http.server
    import socketserver
    import threading
    import mimetypes

    workspace_id = DEFAULT_WORKSPACES.get(workspace.lower())
    if not workspace_id:
        if workspace.startswith("T"):
            workspace_id = workspace
        else:
            raise click.ClickException(f"Unknown workspace: {workspace}")

    result = {"ok": False, "error": "No token received"}
    server_should_stop = threading.Event()

    script_dir = Path(__file__).parent
    assets_dir = script_dir.parent / "assets"

    def load_asset(filename: str) -> str:
        content = (assets_dir / filename).read_text()
        return content.replace("{{OAUTH_URL}}", OAUTH_URL)

    class TokenHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):  # noqa: A002 - matches BaseHTTPRequestHandler signature
            pass

        def do_GET(self):
            path = self.path

            if path.startswith("/assets/"):
                filename = path[8:]
                # Only allow specific known asset files - no path traversal possible
                allowed_files = {"auth.html", "auth.css", "auth.js"}
                if filename not in allowed_files:
                    self.send_response(404)
                    self.end_headers()
                    return
                asset_path = assets_dir / filename
                if not asset_path.is_file():
                    self.send_response(404)
                    self.end_headers()
                    return
                content_type, _ = mimetypes.guess_type(str(asset_path))
                if asset_path.suffix == ".html":
                    content = load_asset(filename).encode()
                else:
                    content = asset_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-type", content_type or "application/octet-stream")
                self.end_headers()
                self.wfile.write(content)
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(load_asset("auth.html").encode())

        def do_POST(self):
            nonlocal result

            if self.path != "/submit":
                self.send_response(404)
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()

            try:
                data = json.loads(body)
                token = data.get("token", "")

                if not token.startswith("xoxp-"):
                    self.send_json({"ok": False, "error": "Invalid token format"})
                    return

                async def validate():
                    client = SlackClient(token, workspace_id)
                    try:
                        return await client.auth_test()
                    finally:
                        await client.close()

                auth_info = run_async(validate())

                config = {
                    "token": token,
                    "default_workspace": workspace_id,
                    "workspaces": DEFAULT_WORKSPACES,
                }
                save_config(config)

                result = {
                    "ok": True,
                    "message": "Authentication successful!",
                    "user": {
                        "id": auth_info.get("user_id"),
                        "name": auth_info.get("user"),
                    },
                    "default_workspace": workspace_id,
                }

                self.send_json(result)
                threading.Thread(target=lambda: (threading.Event().wait(0.5), server_should_stop.set())).start()

            except Exception as e:
                self.send_json({"ok": False, "error": str(e)})

        def send_json(self, data):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

    for attempt_port in range(port, port + 10):
        try:
            with socketserver.TCPServer(("127.0.0.1", attempt_port), TokenHandler) as httpd:
                url = f"http://127.0.0.1:{attempt_port}"
                webbrowser.open(url)

                httpd.timeout = 1
                while not server_should_stop.is_set():
                    httpd.handle_request()

                output_json(result)
                return
        except OSError:
            continue

    output_json({"ok": False, "error": f"Could not find available port in range {port}-{port+9}"})


# =============================================================================
# Workspace commands
# =============================================================================

@cli.group()
def workspace():
    """Workspace management commands."""
    pass


@workspace.command("list")
def workspace_list():
    """List all configured workspaces."""
    config = load_config()
    workspaces = config.get("workspaces", DEFAULT_WORKSPACES)
    default_ws = config.get("default_workspace", DEFAULT_WORKSPACES["block"])

    output_json({"workspaces": workspaces, "default": default_ws})


@workspace.command("set-default")
@click.argument("workspace_alias")
def workspace_set_default(workspace_alias: str):
    """Set the default workspace."""
    config = load_config()
    workspaces = config.get("workspaces", DEFAULT_WORKSPACES)

    ws_lower = workspace_alias.lower()
    if ws_lower not in workspaces:
        raise click.ClickException(f"Unknown workspace: {workspace_alias}")

    config["default_workspace"] = workspaces[ws_lower]
    save_config(config)

    output_json({"ok": True, "default_workspace": workspaces[ws_lower], "alias": ws_lower})


@workspace.command("add")
@click.argument("alias")
@click.argument("workspace_id")
def workspace_add(alias: str, workspace_id: str):
    """Add a workspace alias."""
    config = load_config()
    workspaces = config.get("workspaces", DEFAULT_WORKSPACES.copy())

    workspaces[alias.lower()] = workspace_id
    config["workspaces"] = workspaces
    save_config(config)

    output_json({"ok": True, "alias": alias.lower(), "workspace_id": workspace_id})


# =============================================================================
# Channel commands
# =============================================================================

@cli.command("list-channels")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--types", default="public_channel,private_channel", help="Channel types")
@click.option("--limit", default=200, help="Maximum channels to return per page")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--include-archived/--exclude-archived", default=False, help="Include archived channels")
@click.option("--name-filter", default="", help="Filter by name substring")
def list_channels(workspace: str, types: str, limit: int, cursor: str,
                  include_archived: bool, name_filter: str):
    """List channels you're a member of."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                result = await client.conversations_list(
                    types=types,
                    limit=limit,
                    cursor=cursor,
                    exclude_archived=not include_archived
                )
                channels = result.get("channels", [])
                next_cursor = result.get("response_metadata", {}).get("next_cursor", "")

                if name_filter:
                    channels = [c for c in channels if name_filter.lower() in c.get("name", "").lower()]

                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "count": len(channels),
                    "next_cursor": next_cursor,
                    "channels": [{"id": c.get("id"), "name": c.get("name"), "is_private": c.get("is_private")} for c in channels],
                }
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


@cli.command("get-channel-info")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", default="", help="Channel ID")
@click.option("--channel-name", default="", help="Channel name")
def get_channel_info(workspace: str, channel_id: str, channel_name: str):
    """Get information about a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                cid = channel_id
                if channel_name and not channel_id:
                    result = await client.conversations_list()
                    for ch in result.get("channels", []):
                        if ch.get("name") == channel_name:
                            cid = ch.get("id")
                            break
                    if not cid:
                        return {"ok": False, "error": f"Channel '{channel_name}' not found"}

                result = await client.conversations_info(cid)
                return {"ok": True, "workspace_id": ws_id, "channel": result.get("channel")}
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


@cli.command("get-channel-messages")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", default="", help="Channel ID")
@click.option("--channel-name", default="", help="Channel name")
@click.option("--dm-username", default="", help="DM with this username")
@click.option("--thread-ts", default="", help="Thread timestamp for replies")
@click.option("--limit", default=30, help="Number of messages (max 100)")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--oldest", default="", help="Only messages after this timestamp")
@click.option("--latest", default="", help="Only messages before this timestamp")
@click.option("--inclusive/--exclusive", default=False, help="Include oldest/latest boundary messages")
@click.option("--full-text", is_flag=True, default=False, help="Return full message text without truncation")
def get_channel_messages(workspace: str, channel_id: str, channel_name: str,
                         dm_username: str, thread_ts: str, limit: int,
                         cursor: str, oldest: str, latest: str, inclusive: bool,
                         full_text: bool):
    """Get messages from a channel, DM, or thread."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                cid = channel_id

                # Resolve channel name to ID
                if channel_name and not channel_id:
                    result = await client.conversations_list()
                    for ch in result.get("channels", []):
                        if ch.get("name") == channel_name:
                            cid = ch.get("id")
                            break
                    if not cid:
                        return {"ok": False, "error": f"Channel '{channel_name}' not found"}

                # Resolve DM username to channel ID
                if dm_username and not cid:
                    uid = await client.resolve_username_to_user_id(dm_username)
                    if not uid:
                        return {"ok": False, "error": f"User '{dm_username}' not found"}
                    dm_result = await client.conversations_open(users=uid)
                    if not dm_result.get("ok") or "channel" not in dm_result:
                        return {"ok": False, "error": f"Failed to open DM with user '{dm_username}': {dm_result.get('error', 'unknown error')}"}
                    cid = dm_result["channel"]["id"]

                if not cid:
                    return {"ok": False, "error": "Must provide channel-id, channel-name, or dm-username"}

                if thread_ts:
                    result = await client.conversations_replies(cid, thread_ts, limit, cursor)
                    messages = result.get("messages", [])
                else:
                    result = await client.conversations_history(
                        cid, limit, cursor, oldest, latest, inclusive
                    )
                    messages = result.get("messages", [])

                next_cursor = result.get("response_metadata", {}).get("next_cursor", "")
                formatted = [format_message(m, full_text=full_text) for m in messages]

                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "channel_id": cid,
                    "count": len(formatted),
                    "next_cursor": next_cursor,
                    "messages": formatted,
                }
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


@cli.command("list-channel-members")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--limit", default=100, help="Maximum members to return per page")
@click.option("--cursor", default="", help="Pagination cursor")
def list_channel_members(workspace: str, channel_id: str, limit: int, cursor: str):
    """List members of a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                result = await client.conversations_members(channel_id, limit, cursor)
                next_cursor = result.get("response_metadata", {}).get("next_cursor", "")
                members = result.get("members", [])

                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "channel_id": channel_id,
                    "count": len(members),
                    "next_cursor": next_cursor,
                    "members": members,
                }
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


@cli.command("create-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--name", "-n", required=True, help="Channel name")
@click.option("--private/--public", default=False, help="Create private channel")
def create_channel(workspace: str, name: str, private: bool):
    """Create a new channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                result = await client.conversations_create(name, is_private=private)
                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "channel": result.get("channel"),
                }
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("archive-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
def archive_channel(workspace: str, channel_id: str):
    """Archive a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                await client.conversations_archive(channel_id)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "result": "archived"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("unarchive-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
def unarchive_channel(workspace: str, channel_id: str):
    """Unarchive a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                await client.conversations_unarchive(channel_id)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "result": "unarchived"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("rename-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--new-name", required=True, help="New channel name")
def rename_channel(workspace: str, channel_id: str, new_name: str):
    """Rename a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                result = await client.conversations_rename(channel_id, new_name)
                return {"ok": True, "workspace_id": ws_id, "channel": result.get("channel")}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("invite-to-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--user-ids", required=True, help="Comma-separated user IDs")
def invite_to_channel(workspace: str, channel_id: str, user_ids: str):
    """Invite users to a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                ids = [uid.strip() for uid in user_ids.split(",")]
                result = await client.conversations_invite(channel_id, ids)
                return {"ok": True, "workspace_id": ws_id, "channel": result.get("channel")}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("remove-from-channel")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--user-id", required=True, help="User ID to remove")
def remove_from_channel(workspace: str, channel_id: str, user_id: str):
    """Remove a user from a channel."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                await client.conversations_kick(channel_id, user_id)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "user_id": user_id, "result": "removed"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("set-channel-purpose")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--purpose", required=True, help="Channel purpose/description")
def set_channel_purpose(workspace: str, channel_id: str, purpose: str):
    """Set the channel purpose/description."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                result = await client.conversations_set_purpose(channel_id, purpose)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "purpose": result.get("purpose")}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("mark-channel-read")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--ts", required=True, help="Timestamp to mark as read up to")
def mark_channel_read(workspace: str, channel_id: str, ts: str):
    """Mark a channel as read up to a specific message."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                await client.conversations_mark(channel_id, ts)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "marked_to": ts}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("close-dm")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="DM/MPIM channel ID")
def close_dm(workspace: str, channel_id: str):
    """Close a DM or multi-person DM."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                await client.conversations_close(channel_id)
                return {"ok": True, "workspace_id": ws_id, "channel_id": channel_id, "result": "closed"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


# =============================================================================
# Search commands
# =============================================================================

@cli.command("search-messages")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--query", "-q", required=True, help="Search query")
@click.option("--limit", default=20, help="Maximum results (max 100)")
@click.option("--sort", default="score", type=click.Choice(["score", "timestamp"]), help="Sort by")
@click.option("--sort-dir", default="desc", type=click.Choice(["asc", "desc"]), help="Sort direction")
@click.option("--in-channel", default="", help="Limit to channel name(s)")
@click.option("--from-user", default="", help="Filter by username")
@click.option("--page", default=1, help="Page number for pagination (1-indexed)")
@click.option("--full-text", is_flag=True, default=False, help="Return full message text without truncation")
def search_messages(workspace: str, query: str, limit: int, sort: str, sort_dir: str,
                    in_channel: str, from_user: str, page: int, full_text: bool):
    """Search messages across Slack."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                # Build query with filters
                full_query = query
                if in_channel:
                    full_query += f" in:{in_channel}"
                if from_user:
                    full_query += f" from:{from_user}"

                result = await client.search_messages(
                    full_query,
                    count=limit,
                    sort=sort,
                    sort_dir=sort_dir,
                    page=page
                )

                matches = result.get("messages", {}).get("matches", [])

                formatted = []
                for m in matches:
                    text = m.get("text", "")
                    if not full_text and len(text) > 500:
                        text = text[:500] + "... [truncated]"
                    formatted.append({
                        "ts": m.get("ts"),
                        "time": format_timestamp(m.get("ts", "")),
                        "channel": m.get("channel", {}).get("name"),
                        "channel_id": m.get("channel", {}).get("id"),
                        "user": m.get("user"),
                        "username": m.get("username"),
                        "text": text,
                        "permalink": m.get("permalink"),
                    })

                paging = result.get("messages", {}).get("paging", {})
                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "query": full_query,
                    "count": len(formatted),
                    "total": result.get("messages", {}).get("total", 0),
                    "page": paging.get("page", 1),
                    "pages": paging.get("pages", 1),
                    "messages": formatted,
                }
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


# =============================================================================
# User commands
# =============================================================================

@cli.command("get-user-info")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--user-id", default="", help="User ID")
@click.option("--email", default="", help="User email")
@click.option("--username", default="", help="Username (display name)")
def get_user_info(workspace: str, user_id: str, email: str, username: str):
    """Get information about a user."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                if user_id:
                    result = await client.users_info(user_id)
                    return {"ok": True, "workspace_id": ws_id, "user": result.get("user")}
                elif email:
                    result = await client.users_lookup_by_email(email)
                    return {"ok": True, "workspace_id": ws_id, "user": result.get("user")}
                elif username:
                    uid = await client.resolve_username_to_user_id(username)
                    if not uid:
                        return {"ok": False, "error": f"User '{username}' not found"}
                    result = await client.users_info(uid)
                    return {"ok": True, "workspace_id": ws_id, "user": result.get("user")}
                else:
                    # Get current user
                    auth = await client.auth_test()
                    uid = auth.get("user_id")
                    result = await client.users_info(uid)
                    return {"ok": True, "workspace_id": ws_id, "user": result.get("user")}
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


# =============================================================================
# Message commands
# =============================================================================

@cli.command("post-message")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", default="", help="Channel ID")
@click.option("--channel-name", default="", help="Channel name")
@click.option("--dm-username", default="", help="DM a user by username")
@click.option("--dm-myself", is_flag=True, help="DM yourself")
@click.option("--thread-ts", default="", help="Reply to thread")
@click.option("--format", "fmt", default="markdown",
              type=click.Choice(["markdown", "mrkdwn", "json"]),
              help="Input format: markdown (default, native Slack markdown blocks), "
                   "mrkdwn (already Slack-formatted), "
                   "json (Block Kit blocks JSON array)")
@click.argument("content")
def post_message(workspace: str, channel_id: str, channel_name: str, dm_username: str,
                 dm_myself: bool, thread_ts: str, fmt: str, content: str):
    """Post a message to a channel or DM a user.

    CONTENT is the message text (or Block Kit JSON when --format json).

    \b
    Formats:
      markdown  Send as native Slack markdown block (default)
      mrkdwn    Content is already in Slack mrkdwn format
      json      Block Kit blocks JSON array
    """
    if dm_myself and dm_username:
        raise click.UsageError("--dm-myself and --dm-username are mutually exclusive")

    blocks = None
    text = ""
    if fmt == "markdown":
        blocks = [{"type": "markdown", "text": content}]
    elif fmt == "json":
        try:
            blocks = json.loads(content)
        except json.JSONDecodeError as e:
            raise click.UsageError(f"Invalid JSON for --format json: {e}") from e
        if not isinstance(blocks, list):
            raise click.UsageError("--format json expects a JSON array of Block Kit blocks")
    elif fmt == "mrkdwn":
        text = content

    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def send():
            client = SlackClient(token, ws_id)
            try:
                cid = channel_id

                # DM myself
                if dm_myself:
                    auth = await client.auth_test()
                    uid = auth.get("user_id")
                    dm_result = await client.conversations_open(users=uid)
                    if not dm_result.get("ok") or "channel" not in dm_result:
                        return {"ok": False, "error": f"Failed to open DM with self: {dm_result.get('error', 'unknown error')}"}
                    cid = dm_result["channel"]["id"]
                # DM via username
                elif dm_username:
                    uid = await client.resolve_username_to_user_id(dm_username)
                    if not uid:
                        return {"ok": False, "error": f"User '{dm_username}' not found"}
                    dm_result = await client.conversations_open(users=uid)
                    if not dm_result.get("ok") or "channel" not in dm_result:
                        return {"ok": False, "error": f"Failed to open DM with user '{dm_username}': {dm_result.get('error', 'unknown error')}"}
                    cid = dm_result["channel"]["id"]
                elif channel_name and not channel_id:
                    result = await client.conversations_list()
                    for ch in result.get("channels", []):
                        if ch.get("name") == channel_name:
                            cid = ch.get("id")
                            break
                    if not cid:
                        return {"ok": False, "error": f"Channel '{channel_name}' not found"}

                if not cid:
                    return {"ok": False, "error": "Must provide --channel-id, --channel-name, --dm-username, or --dm-myself"}

                result = await client.chat_post_message(cid, text, thread_ts, blocks)
                return {
                    "ok": True,
                    "workspace_id": ws_id,
                    "channel": result.get("channel"),
                    "ts": result.get("ts"),
                    "message": result.get("message"),
                }
            finally:
                await client.close()

        output_json(run_async(send()))

    except Exception as e:
        handle_error(e)


@cli.command("message")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--channel-id", required=True, help="Channel ID")
@click.option("--message-ts", required=True, help="Message timestamp")
@click.option("--operation", "-o", required=True,
              type=click.Choice(["get_message_reactions", "add_reaction", "remove_reaction",
                                "update_message", "delete_message"]),
              help="Operation to perform")
@click.option("--emoji", default="", help="Emoji for reactions (without colons)")
@click.option("--text", default="", help="New text for update_message")
def message_tool(workspace: str, channel_id: str, message_ts: str, operation: str,
                 emoji: str, text: str):
    """Perform operations on a specific message."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                if operation == "get_message_reactions":
                    result = await client.reactions_get(channel_id, message_ts)
                    return {"ok": True, "workspace_id": ws_id, "message": result.get("message")}
                elif operation == "add_reaction":
                    if not emoji:
                        return {"ok": False, "error": "emoji required for add_reaction"}
                    result = await client.reactions_add(channel_id, message_ts, emoji)
                    return {"ok": True, "workspace_id": ws_id, "result": "reaction added"}
                elif operation == "remove_reaction":
                    if not emoji:
                        return {"ok": False, "error": "emoji required for remove_reaction"}
                    result = await client.reactions_remove(channel_id, message_ts, emoji)
                    return {"ok": True, "workspace_id": ws_id, "result": "reaction removed"}
                elif operation == "update_message":
                    if not text:
                        return {"ok": False, "error": "text required for update_message"}
                    result = await client.chat_update(channel_id, message_ts, text)
                    return {"ok": True, "workspace_id": ws_id, "result": result}
                elif operation == "delete_message":
                    result = await client.chat_delete(channel_id, message_ts)
                    return {"ok": True, "workspace_id": ws_id, "result": "message deleted"}
                else:
                    return {"ok": False, "error": f"Unknown operation: {operation}"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


# =============================================================================
# Misc commands
# =============================================================================

@cli.command("misc-read")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--operation", "-o", required=True,
              type=click.Choice(["get_user_profile", "get_presence", "get_dnd_info", "get_channel_members"]),
              help="Read operation")
@click.option("--user-id", default="", help="User ID for user-specific operations")
@click.option("--channel-id", default="", help="Channel ID for channel-specific operations")
def misc_read(workspace: str, operation: str, user_id: str, channel_id: str):
    """Perform misc read operations."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                if operation == "get_user_profile":
                    result = await client.users_profile_get(user_id if user_id else None)
                    return {"ok": True, "workspace_id": ws_id, "profile": result.get("profile")}
                elif operation == "get_presence":
                    target_user_id = user_id
                    if not target_user_id:
                        auth = await client.auth_test()
                        target_user_id = auth.get("user_id")
                    result = await client.users_get_presence(target_user_id)
                    return {"ok": True, "workspace_id": ws_id, "presence": result.get("presence")}
                elif operation == "get_dnd_info":
                    result = await client.dnd_info(user_id if user_id else None)
                    return {"ok": True, "workspace_id": ws_id, "dnd": result}
                elif operation == "get_channel_members":
                    if not channel_id:
                        return {"ok": False, "error": "channel_id required"}
                    result = await client.conversations_members(channel_id)
                    return {"ok": True, "workspace_id": ws_id, "members": result.get("members")}
                else:
                    return {"ok": False, "error": f"Unknown operation: {operation}"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("misc-write")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--operation", "-o", required=True,
              type=click.Choice(["set_status", "clear_status", "set_presence", "set_dnd",
                                "end_dnd", "set_channel_topic", "join_channel", "leave_channel"]),
              help="Write operation")
@click.option("--channel-id", default="", help="Channel ID")
@click.option("--status-text", default="", help="Status text")
@click.option("--status-emoji", default="", help="Status emoji")
@click.option("--presence", default="", type=click.Choice(["auto", "away", ""]), help="Presence setting")
@click.option("--num-minutes", default=0, help="DND duration in minutes")
@click.option("--topic", default="", help="Channel topic")
def misc_write(workspace: str, operation: str, channel_id: str, status_text: str,
               status_emoji: str, presence: str, num_minutes: int, topic: str):
    """Perform misc write operations."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def execute():
            client = SlackClient(token, ws_id)
            try:
                if operation == "set_status":
                    profile = {"status_text": status_text, "status_emoji": status_emoji}
                    result = await client.users_profile_set(profile)
                    return {"ok": True, "workspace_id": ws_id, "profile": result.get("profile")}
                elif operation == "clear_status":
                    profile = {"status_text": "", "status_emoji": ""}
                    result = await client.users_profile_set(profile)
                    return {"ok": True, "workspace_id": ws_id, "result": "status cleared"}
                elif operation == "set_presence":
                    if not presence:
                        return {"ok": False, "error": "presence required (auto or away)"}
                    result = await client.users_set_presence(presence)
                    return {"ok": True, "workspace_id": ws_id, "result": f"presence set to {presence}"}
                elif operation == "set_dnd":
                    if not num_minutes:
                        return {"ok": False, "error": "num_minutes required"}
                    result = await client.dnd_set_snooze(num_minutes)
                    return {"ok": True, "workspace_id": ws_id, "dnd": result}
                elif operation == "end_dnd":
                    result = await client.dnd_end_snooze()
                    return {"ok": True, "workspace_id": ws_id, "result": "DND ended"}
                elif operation == "set_channel_topic":
                    if not channel_id or not topic:
                        return {"ok": False, "error": "channel_id and topic required"}
                    result = await client.conversations_set_topic(channel_id, topic)
                    return {"ok": True, "workspace_id": ws_id, "result": result}
                elif operation == "join_channel":
                    if not channel_id:
                        return {"ok": False, "error": "channel_id required"}
                    result = await client.conversations_join(channel_id)
                    return {"ok": True, "workspace_id": ws_id, "channel": result.get("channel")}
                elif operation == "leave_channel":
                    if not channel_id:
                        return {"ok": False, "error": "channel_id required"}
                    result = await client.conversations_leave(channel_id)
                    return {"ok": True, "workspace_id": ws_id, "result": "left channel"}
                else:
                    return {"ok": False, "error": f"Unknown operation: {operation}"}
            finally:
                await client.close()

        output_json(run_async(execute()))

    except Exception as e:
        handle_error(e)


@cli.command("download-file")
@click.option("--workspace", "-w", default="", help="Workspace alias")
@click.option("--file-id", required=True, help="Slack file ID (e.g. F0AE4JL1SDS)")
@click.option("--output", "-o", required=True, help="Local path to save the file")
def download_file(workspace: str, file_id: str, output: str):
    """Download a file from Slack by its file ID."""
    try:
        token = get_token()
        ws_id = get_workspace_id(workspace)

        async def fetch():
            client = SlackClient(token, ws_id)
            try:
                result = await client._call("files.info", {"file": file_id})
                file_info = result.get("file", {})
                url = file_info.get("url_private_download") or file_info.get("url_private")
                if not url:
                    return {"ok": False, "error": "No download URL found for file"}

                http_client = await client._get_client()
                resp = await http_client.get(url, follow_redirects=True)
                resp.raise_for_status()

                import os
                os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
                with open(output, "wb") as f:
                    f.write(resp.content)

                return {
                    "ok": True,
                    "file_id": file_id,
                    "name": file_info.get("name"),
                    "size": len(resp.content),
                    "saved_to": os.path.abspath(output),
                }
            finally:
                await client.close()

        output_json(run_async(fetch()))

    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    cli()
