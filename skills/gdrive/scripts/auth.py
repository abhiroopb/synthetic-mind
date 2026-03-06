"""OAuth2 authentication for Google Drive API with file-based credential storage."""

import json
import os
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Default paths - same structure as gconf uses
CONFIG_DIR = Path.home() / ".config" / "gdrive-skill"
OAUTH_KEYS_PATH = CONFIG_DIR / "gcp-oauth.keys.json"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"

# Full Drive scope for read/write access
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.activity.readonly",
    "https://www.googleapis.com/auth/directory.readonly",
]

# Bundled OAuth client config (same as gconf's gcp-oauth.keys.json)
# This is a public OAuth client for the skill
BUNDLED_OAUTH_CONFIG = {
    "installed": {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "project_id": "YOUR_PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
        "redirect_uris": ["http://localhost"],
    }
}


def get_oauth_config() -> dict[str, Any]:
    """Get OAuth client configuration.
    
    Checks for user-provided config file first, falls back to bundled config.
    """
    if OAUTH_KEYS_PATH.exists():
        with open(OAUTH_KEYS_PATH) as f:
            return json.load(f)
    return BUNDLED_OAUTH_CONFIG


def get_credentials(force_refresh: bool = False) -> Credentials | None:
    """Load credentials from file, refreshing if needed.
    
    Args:
        force_refresh: If True, ignore existing credentials and re-authenticate.
        
    Returns:
        Valid Credentials object, or None if not authenticated.
    """
    creds = None
    
    if not force_refresh and CREDENTIALS_PATH.exists():
        try:
            with open(CREDENTIALS_PATH) as f:
                creds_data = json.load(f)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        except (json.JSONDecodeError, ValueError):
            creds = None
    
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
        except Exception:
            creds = None
    
    return creds if (creds and creds.valid) else None


def login(force: bool = False) -> dict[str, Any]:
    """Run OAuth2 browser flow and save credentials.
    
    Args:
        force: If True, re-authenticate even if valid credentials exist.
        
    Returns:
        Dict with status information.
    """
    if not force:
        existing = get_credentials()
        if existing:
            return {
                "status": "already_authenticated",
                "message": "Already authenticated. Use --force to re-authenticate.",
                "credentials_path": str(CREDENTIALS_PATH),
            }
    
    oauth_config = get_oauth_config()
    flow = InstalledAppFlow.from_client_config(oauth_config, SCOPES)
    
    # Run local server for OAuth callback
    creds = flow.run_local_server(
        port=0,  # Use any available port
        prompt="consent",
        authorization_prompt_message="Opening browser for Google authentication...",
        success_message="Authentication successful! You can close this tab.",
    )
    
    _save_credentials(creds)
    
    return {
        "status": "ok",
        "message": "Successfully authenticated",
        "credentials_path": str(CREDENTIALS_PATH),
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
    }


def get_auth_status() -> dict[str, Any]:
    """Check current authentication status.
    
    Returns:
        Dict with authentication status information.
    """
    creds = get_credentials()
    
    if not creds:
        return {
            "authenticated": False,
            "credentials_path": str(CREDENTIALS_PATH),
            "credentials_exist": CREDENTIALS_PATH.exists(),
        }
    
    return {
        "authenticated": True,
        "credentials_path": str(CREDENTIALS_PATH),
        "scopes": list(creds.scopes) if creds.scopes else [],
        "expired": creds.expired,
        "valid": creds.valid,
    }


def logout() -> dict[str, Any]:
    """Remove stored credentials.
    
    Returns:
        Dict with status information.
    """
    if CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.unlink()
        return {"status": "ok", "message": "Credentials removed"}
    return {"status": "ok", "message": "No credentials to remove"}


def require_auth() -> Credentials:
    """Get credentials or raise an error if not authenticated.
    
    Returns:
        Valid Credentials object.
        
    Raises:
        RuntimeError: If not authenticated.
    """
    creds = get_credentials()
    if not creds:
        raise RuntimeError(
            "Not authenticated. Run 'python gdrive-cli.py auth login' first."
        )
    return creds


def _save_credentials(creds: Credentials) -> None:
    """Save credentials to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    creds_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
    }
    
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump(creds_data, f, indent=2)
    
    # Secure the file
    os.chmod(CREDENTIALS_PATH, 0o600)
