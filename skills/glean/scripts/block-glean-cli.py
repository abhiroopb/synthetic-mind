#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "authlib~=1.6.8",
#     "httpx~=0.28.1",
#     "click~=8.3.1",
#     "requests~=2.32.5",
# ]
# ///
"""Glean CLI for agent skills - search, chat, and read from your company's Glean."""

import asyncio
import json
import secrets
import sys
import time
import uuid
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from threading import Thread
from typing import Optional
from urllib.parse import parse_qs, urlparse

import click
import httpx
import requests
from authlib.oauth2.rfc7636 import create_s256_code_challenge

# =============================================================================
# Configuration
# =============================================================================

CONFIG_DIR = Path.home() / ".config" / "block-glean"
TOKEN_FILE = CONFIG_DIR / "tokens.json"

# OAuth endpoints (update these for your organization)
CLIENT_ID_URL = "https://internal.example.com/api/glean/client_id"
AUTHORIZE_URL = "https://sso.example.com/oauth2/v1/authorize"
TOKEN_URL = "https://sso.example.com/oauth2/v1/token"

# Glean API (update for your Glean instance)
API_BASE = "https://your-org-be.glean.com/rest/api/v1"

# OAuth callback
CALLBACK_PORT = 8030
REDIRECT_URI = f"http://localhost:{CALLBACK_PORT}/callback"

# Datasource name mapping
DATASOURCE_MAP = {
    "google drive": "gdrive",
    "the hub": "thehub",
    "slack": "slackentgrid",
    "videos": "kaltura",
}


# =============================================================================
# Output helpers
# =============================================================================

def output_json(data: dict) -> None:
    """Print JSON output."""
    print(json.dumps(data, indent=2, default=str))


def output_error(message: str, error_type: str = "error") -> None:
    """Print error as JSON."""
    output_json({"ok": False, "error": message, "error_type": error_type})


def run_async(coro):
    """Run async coroutine."""
    return asyncio.run(coro)


# =============================================================================
# OAuth Authentication
# =============================================================================

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler to capture OAuth callback."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            self.server.auth_code = query["code"][0]

        self.wfile.write(b"<html><body><h1>Authorization successful!</h1>"
                        b"<p>You can close this window.</p></body></html>")

    def log_message(self, fmt, *args):
        pass  # Suppress logging


class GleanAuth:
    """OAuth handler with lazy server creation (fixes port-binding bug)."""

    def __init__(self):
        self._server: Optional[HTTPServer] = None
        self._client_id: Optional[str] = None
        self.code_verifier = secrets.token_urlsafe(64)

    @property
    def client_id(self) -> str:
        """Lazily fetch client ID only when needed."""
        if self._client_id is None:
            try:
                response = requests.get(CLIENT_ID_URL, timeout=10)
                if response.status_code == 200 and len(response.text) < 100:
                    self._client_id = response.text
                else:
                    raise RuntimeError(
                        "Unable to retrieve Glean client_id. "
                        "Check VPN and The Hub access."
                    )
            except requests.RequestException as e:
                raise RuntimeError(
                    f"Failed to fetch client_id: {e}. Check VPN connection."
                ) from e
        return self._client_id

    def _create_server(self) -> HTTPServer:
        """Create HTTP server only when OAuth flow is needed."""
        if self._server is None:
            self._server = HTTPServer(
                ("localhost", CALLBACK_PORT), OAuthCallbackHandler
            )
        return self._server

    def _load_cached_token(self) -> Optional[str]:
        """Load token from cache if valid."""
        if not TOKEN_FILE.exists():
            return None

        try:
            with open(TOKEN_FILE) as f:
                data = json.load(f)

            access_token = data.get("access_token")
            expiry = data.get("expiry", 0)

            if access_token and time.time() < expiry:
                return access_token
        except (json.JSONDecodeError, IOError):
            pass

        return None

    def _save_token(self, token_data: dict) -> None:
        """Save token to cache."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        expires_in = token_data.get("expires_in", 3600)
        expiry = int(time.time() + expires_in)

        with open(TOKEN_FILE, "w") as f:
            json.dump({
                "access_token": token_data.get("access_token"),
                "expiry": expiry,
            }, f)

        # Secure permissions
        TOKEN_FILE.chmod(0o600)

    def _run_oauth_flow(self) -> str:
        """Run the OAuth PKCE flow."""
        # Create server only now (lazy binding)
        server = self._create_server()
        server.auth_code = None

        # Start callback server
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        try:
            # Generate PKCE challenge
            code_challenge = create_s256_code_challenge(self.code_verifier)
            state = f"state-{uuid.uuid4()}"

            # Build authorization URL
            params = {
                "client_id": self.client_id,
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "scope": "openid",
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
            auth_url = f"{AUTHORIZE_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            # Open browser
            print("Opening browser for authorization...", file=sys.stderr)
            webbrowser.open(auth_url)

            # Wait for callback
            while server.auth_code is None:
                time.sleep(0.5)

            # Exchange code for token
            token_response = requests.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "code_verifier": self.code_verifier,
                    "code": server.auth_code,
                    "redirect_uri": REDIRECT_URI,
                },
                timeout=30,
            )

            if token_response.status_code != 200:
                raise RuntimeError(
                    f"Token exchange failed: {token_response.text}"
                )

            token_data = token_response.json()
            self._save_token(token_data)

            return token_data.get("access_token")

        finally:
            server.shutdown()
            server.server_close()
            self._server = None

    def get_token(self, force_reauth: bool = False) -> str:
        """Get valid access token, triggering OAuth only if needed."""
        if not force_reauth:
            token = self._load_cached_token()
            if token:
                return token

        return self._run_oauth_flow()

    def get_token_status(self) -> dict:
        """Get current token status."""
        if not TOKEN_FILE.exists():
            return {"authenticated": False, "reason": "No token file"}

        try:
            with open(TOKEN_FILE) as f:
                data = json.load(f)

            expiry = data.get("expiry", 0)
            now = time.time()

            if now >= expiry:
                return {
                    "authenticated": False,
                    "reason": "Token expired",
                    "expired_at": expiry,
                }

            return {
                "authenticated": True,
                "expires_at": expiry,
                "expires_in_seconds": int(expiry - now),
            }
        except (json.JSONDecodeError, IOError) as e:
            return {"authenticated": False, "reason": str(e)}

    def logout(self) -> bool:
        """Remove stored tokens."""
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            return True
        return False


# =============================================================================
# Glean API Client
# =============================================================================

class GleanClient:
    """Async Glean API client."""

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Glean-Auth-Type": "OAUTH",
        }

    async def _request(self, endpoint: str, data: dict) -> dict:
        """Make API request."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{API_BASE}/{endpoint}",
                headers=self.headers,
                json=data,
            )

            if response.status_code == 401:
                raise RuntimeError("Token expired or invalid")

            response.raise_for_status()
            return response.json()

    async def search(
        self,
        query: str,
        datasources: Optional[list[str]] = None,
        page_size: int = 15,
        cursor: str = "",
    ) -> dict:
        """Search documents."""
        # Map datasource names
        if datasources:
            datasources = [
                DATASOURCE_MAP.get(ds.lower(), ds.lower())
                for ds in datasources
            ]

        data = {
            "query": query,
            "pageSize": page_size,
            "cursor": cursor,
            "requestOptions": {
                "datasourcesFilter": datasources or [],
            },
        }

        result = await self._request("search", data)
        return self._clean_search_results(result)

    def _clean_search_results(self, result: dict) -> dict:
        """Clean search results for readability."""
        cleaned = []
        for item in result.get("results", []):
            doc = item.get("document", {})
            cleaned.append({
                "document_id": doc.get("id"),
                "title": item.get("title") or doc.get("title"),
                "url": doc.get("url"),
                "datasource": doc.get("datasource"),
                "snippets": [
                    s.get("text") for s in item.get("snippets", [])
                    if s.get("text")
                ][:2],  # Limit snippets
            })

        return {
            "ok": True,
            "results": cleaned,
            "has_more": result.get("hasMoreResults", False),
            "cursor": result.get("cursor", ""),
        }

    async def chat(self, query: str, agent_id: Optional[str] = None) -> dict:
        """Chat with Glean AI."""
        data = {
            "stream": False,
            "messages": [
                {"author": "USER", "fragments": [{"text": query}]}
            ],
        }

        if agent_id:
            data["agentId"] = agent_id

        result = await self._request("chat", data)
        return self._clean_chat_response(result)

    def _clean_chat_response(self, result: dict) -> dict:
        """Clean chat response."""
        messages = []
        for msg in result.get("messages", []):
            if msg.get("messageType") == "CONTENT":
                for fragment in msg.get("fragments", []):
                    if text := fragment.get("text"):
                        messages.append(text)

        return {
            "ok": True,
            "response": "\n".join(messages),
        }

    async def read_document(
        self,
        doc_id: str,
        start_line: int = 1,
        end_line: int = 100,
    ) -> dict:
        """Read document content."""
        data = {
            "documentSpecs": [{"id": doc_id}],
            "includeFields": ["DOCUMENT_CONTENT"],
        }

        result = await self._request("getdocuments", data)

        documents = result.get("documents", {})
        if doc_id not in documents:
            return {"ok": False, "error": f"Document {doc_id} not found"}

        doc_data = documents[doc_id]
        if error := doc_data.get("error"):
            return {"ok": False, "error": error}

        content_list = doc_data.get("content", {}).get("fullTextList", [])
        if not content_list:
            return {"ok": False, "error": "Document has no content"}

        # Extract line range
        total_lines = len(content_list)
        start_idx = max(0, min(start_line - 1, total_lines - 1))
        end_idx = max(1, min(end_line, total_lines))

        return {
            "ok": True,
            "document_id": doc_id,
            "title": doc_data.get("title", ""),
            "url": doc_data.get("url", ""),
            "total_lines": total_lines,
            "line_range": [start_idx + 1, end_idx],
            "content": "\n".join(content_list[start_idx:end_idx]),
        }

    async def mentions(self) -> dict:
        """Get recent @mentions of the current user from the Glean feed."""
        result = await self._request("feed", {"categories": ["MENTION"]})

        window_hours = result.get("mentionsTimeWindowInHours", 0)
        mentions = []
        for item in result.get("results", []):
            if item.get("category") != "MENTION":
                continue
            entry = item.get("primaryEntry", {})
            entry_id = entry.get("entryId", "")
            title = entry.get("title", "")

            # Parse source and doc ID from entryId
            # Format: MENTION:<DATASOURCE>_<ID>:<timestamp>
            source = ""
            doc_id = ""
            parts = entry_id.split(":", 2)
            if len(parts) >= 2:
                source_part = parts[1]
                underscore_idx = source_part.find("_")
                if underscore_idx > 0:
                    source = source_part[:underscore_idx].lower()
                    doc_id = source_part[underscore_idx + 1:]

            source_label = {
                "gdrive": "Google Drive",
                "jira": "Jira",
                "slackentgrid": "Slack",
                "linear": "Linear",
            }.get(source, source)

            mentions.append({
                "title": title,
                "source": source_label,
                "doc_id": doc_id,
                "entry_id": entry_id,
            })

        return {
            "ok": True,
            "count": len(mentions),
            "window_hours": window_hours,
            "mentions": mentions,
        }

    async def list_agents(self, name: Optional[str] = None) -> dict:
        """List/search Glean agents."""
        data = {}
        if name:
            data["name"] = name

        result = await self._request("agents/search", data)

        agents = []
        for agent in result.get("agents", []):
            agents.append({
                "agent_id": agent.get("agent_id"),
                "name": agent.get("name"),
                "description": agent.get("description"),
            })

        return {"ok": True, "agents": agents}


# =============================================================================
# CLI Commands
# =============================================================================

@click.group()
def cli():
    """Glean CLI - search your company's internal knowledge base."""
    pass


# -----------------------------------------------------------------------------
# Auth commands
# -----------------------------------------------------------------------------

@cli.group()
def auth():
    """Authentication commands."""
    pass


@auth.command("login")
@click.option("--reauth", is_flag=True, help="Force re-authentication")
def auth_login(reauth: bool):
    """Authenticate with Glean via SSO."""
    try:
        handler = GleanAuth()
        token = handler.get_token(force_reauth=reauth)
        if token:
            output_json({"ok": True, "message": "Authentication successful"})
        else:
            output_error("Authentication failed", "auth_failed")
    except Exception as e:
        output_error(str(e), "auth_error")


@auth.command("status")
def auth_status():
    """Check authentication status."""
    handler = GleanAuth()
    status = handler.get_token_status()
    status["ok"] = status.get("authenticated", False)
    output_json(status)


@auth.command("logout")
def auth_logout():
    """Remove stored authentication tokens."""
    handler = GleanAuth()
    if handler.logout():
        output_json({"ok": True, "message": "Logged out successfully"})
    else:
        output_json({"ok": True, "message": "No tokens to remove"})


# -----------------------------------------------------------------------------
# API commands
# -----------------------------------------------------------------------------

def require_auth() -> Optional[str]:
    """Get token, triggering OAuth flow if needed."""
    try:
        handler = GleanAuth()
        return handler.get_token()
    except Exception as e:
        output_error(str(e), "auth_error")
        return None


@cli.command("search")
@click.argument("query")
@click.option("--datasource", "-d", multiple=True, help="Filter by datasource")
@click.option("--limit", "-l", default=15, help="Number of results (default: 15)")
@click.option("--cursor", default="", help="Pagination cursor")
def cmd_search(query: str, datasource: tuple, limit: int, cursor: str):
    """Search documents in Glean."""
    token = require_auth()
    if not token:
        return

    try:
        client = GleanClient(token)
        result = run_async(client.search(
            query,
            datasources=list(datasource) if datasource else None,
            page_size=limit,
            cursor=cursor,
        ))
        output_json(result)
    except Exception as e:
        output_error(str(e), "api_error")


@cli.command("mentions")
def cmd_mentions():
    """Get recent @mentions of you across Google Docs, Sheets, Jira, etc."""
    token = require_auth()
    if not token:
        return

    try:
        client = GleanClient(token)
        result = run_async(client.mentions())
        output_json(result)
    except Exception as e:
        output_error(str(e), "api_error")


@cli.command("chat")
@click.argument("query")
@click.option("--agent-id", "-a", help="Specific agent ID to use")
def cmd_chat(query: str, agent_id: Optional[str]):
    """Chat with Glean AI."""
    token = require_auth()
    if not token:
        return

    try:
        client = GleanClient(token)
        result = run_async(client.chat(query, agent_id=agent_id))
        output_json(result)
    except Exception as e:
        output_error(str(e), "api_error")


@cli.command("read")
@click.argument("doc_id")
@click.option("--start", "-s", default=1, help="Start line (default: 1)")
@click.option("--end", "-e", default=100, help="End line (default: 100)")
def cmd_read(doc_id: str, start: int, end: int):
    """Read document content by ID."""
    token = require_auth()
    if not token:
        return

    try:
        client = GleanClient(token)
        result = run_async(client.read_document(doc_id, start, end))
        output_json(result)
    except Exception as e:
        output_error(str(e), "api_error")


@cli.command("agents")
@click.option("--name", "-n", help="Filter agents by name")
def cmd_agents(name: Optional[str]):
    """List available Glean agents."""
    token = require_auth()
    if not token:
        return

    try:
        client = GleanClient(token)
        result = run_async(client.list_agents(name=name))
        output_json(result)
    except Exception as e:
        output_error(str(e), "api_error")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    cli()
