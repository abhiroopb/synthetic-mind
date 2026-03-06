#!/usr/bin/env python3
"""CLI wrapper for Looker Python SDK dashboard operations.

Usage:
    python looker_cli.py <command> [options]

Authentication (in priority order):
    1. LOOKERSDK_CLIENT_ID + LOOKERSDK_CLIENT_SECRET env vars
    2. OAuth token from macOS Keychain (with auto-refresh via PKCE)
    3. Run 'login' command to authenticate via browser
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import webbrowser

import looker_sdk
from looker_sdk import models40, methods40, requests_transport
from looker_sdk.rtl import api_settings, auth_session, serialize as sdk_serialize
from looker_sdk.rtl import auth_token as auth_token_lib

LOOKER_BASE_URL = "https://square.cloud.looker.com"
LOOKER_API_URL = f"{LOOKER_BASE_URL}:443/api/4.0"
KEYCHAIN_SERVICE = "looker_sdk"
KEYCHAIN_ACCOUNT = "looker_oauth_tokens"
OAUTH_CLIENT_ID = "mcp_client_prod"
OAUTH_REDIRECT_URI = "http://127.0.0.1:3007/callback"
CALLBACK_PORT = 3007


def _read_keychain_token():
    """Read OAuth token from macOS Keychain."""
    try:
        result = subprocess.run(
            [
                "security", "find-generic-password",
                "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT, "-w",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout.strip())
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def _save_keychain_token(token_data):
    """Save OAuth token to macOS Keychain (macOS only)."""
    token_json = json.dumps(token_data)
    result = subprocess.run(
        [
            "security", "add-generic-password",
            "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT,
            "-w", token_json, "-U",
        ],
        capture_output=True,
    )
    if result.returncode != 0:
        print("Warning: Could not save token to Keychain.", file=sys.stderr)


class OAuthApiSettings(api_settings.ApiSettings):
    """API settings for OAuth PKCE flow (no client_secret needed)."""

    def __init__(self):
        super().__init__()

    def read_config(self):
        return {
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": "",
            "looker_url": LOOKER_BASE_URL,
            "redirect_uri": OAUTH_REDIRECT_URI,
            "base_url": f"{LOOKER_BASE_URL}:443",
        }


def _create_oauth_session():
    """Create an OAuthSession and load existing keychain token if available."""
    settings = OAuthApiSettings()
    tp = requests_transport.RequestsTransport.configure(settings)
    session = auth_session.OAuthSession(
        settings=settings,
        transport=tp,
        serialize=sdk_serialize.serialize40,
        deserialize=sdk_serialize.deserialize40,
        version="4.0",
        crypto=auth_session.CryptoHash(),
    )
    token_data = _read_keychain_token()
    if token_data:
        expires_at = float(token_data.get("expires_at", 0))
        remaining = max(0, int(expires_at - time.time()))
        token = auth_token_lib.AccessToken(
            token_type="Bearer",
            access_token=token_data.get("access_token", ""),
            refresh_token=token_data.get("refresh_token", ""),
            expires_in=remaining,
        )
        session.token = auth_token_lib.AuthToken(token)
    return session


def _save_session_token(session):
    """Persist the OAuthSession's current token to keychain."""
    if session and session.token:
        expires_at = time.time() + (session.token.expires_in or 0)
        _save_keychain_token({
            "access_token": session.token.access_token,
            "refresh_token": session.token.refresh_token,
            "expires_in": session.token.expires_in,
            "expires_at": expires_at,
        })


def get_sdk():
    if os.environ.get("LOOKERSDK_CLIENT_ID") and os.environ.get(
        "LOOKERSDK_CLIENT_SECRET"
    ):
        if not os.environ.get("LOOKERSDK_BASE_URL"):
            os.environ["LOOKERSDK_BASE_URL"] = LOOKER_BASE_URL
        return looker_sdk.init40()

    session = _create_oauth_session()

    if not session.token or not (session.token.access_token or session.token.refresh_token):
        print(
            "Error: No valid auth available. Either:\n"
            "  - Set LOOKERSDK_CLIENT_ID and LOOKERSDK_CLIENT_SECRET env vars\n"
            "  - Run: python looker_cli.py login",
            file=sys.stderr,
        )
        sys.exit(1)

    sdk = methods40.Looker40SDK(
        auth=session,
        deserialize=session.deserialize,
        serialize=session.serialize,
        transport=session.transport,
        api_version="4.0",
    )

    try:
        sdk.me()
    except Exception as e:
        print(f"Auth failed ({e}). Run: python looker_cli.py login", file=sys.stderr)
        sys.exit(1)

    _save_session_token(session)
    return sdk


def to_json(obj):
    """Convert SDK model objects to JSON-serializable dicts."""
    if obj is None:
        return None
    if isinstance(obj, list):
        return [to_json(item) for item in obj]
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return {
            k: to_json(v)
            for k, v in obj.__dict__.items()
            if v is not None and not k.startswith("_")
        }
    return obj


def _run_query_by_id(sdk, query_id, result_format="json", auth_headers=None):
    """Run a query by ID using requests directly.

    The Looker Python SDK's run_query() has a deserialization bug
    (StructureHandlerNotFoundError for str | bytes) so we bypass it
    and call the REST endpoint directly with the SDK's auth headers.

    If *auth_headers* is provided they are used as-is (useful for
    pre-authenticated, thread-safe calls).  Otherwise headers are
    obtained from ``sdk.auth.authenticate()``.
    """
    import requests as req

    if auth_headers is None:
        try:
            auth_headers = sdk.auth.authenticate()
        except TypeError:
            auth_headers = sdk.auth.authenticate(transport_options={})
    resp = req.get(
        f"{LOOKER_API_URL}/queries/{query_id}/run/{result_format}",
        headers=auth_headers,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.text


def cmd_query_by_slug(args):
    sdk = get_sdk()
    query = sdk.query_for_slug(slug=args.slug)
    output = {
        "id": query.id,
        "model": query.model,
        "view": query.view,
        "fields": query.fields,
        "filters": query.filters,
        "filter_expression": query.filter_expression,
        "sorts": query.sorts,
        "limit": query.limit,
        "dynamic_fields": query.dynamic_fields,
    }
    print(json.dumps(output, indent=2))


def cmd_run_query(args):
    sdk = get_sdk()
    query = sdk.query_for_slug(slug=args.slug)
    result_format = args.format or "json"
    raw = _run_query_by_id(sdk, query.id, result_format)
    if result_format == "json":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
        if args.limit:
            data = data[: args.limit]
        print(json.dumps(data, indent=2))
    else:
        print(raw)


def cmd_run_explore(args):
    sdk = get_sdk()
    fields = [f.strip() for f in args.fields.split(",")]
    filters = {}
    if args.filters:
        for filt in args.filters:
            if "=" not in filt:
                print(f"Error: invalid filter '{filt}' (expected key=value)", file=sys.stderr)
                sys.exit(1)
            key, value = filt.split("=", 1)
            filters[key] = value
    sorts = [s.strip() for s in args.sorts.split(",")] if args.sorts else None
    pivots = [p.strip() for p in args.pivots.split(",")] if args.pivots else None

    body = models40.WriteQuery(
        model=args.model,
        view=args.view,
        fields=fields,
        filters=filters if filters else None,
        sorts=sorts,
        pivots=pivots,
        limit=str(args.limit) if args.limit else None,
        dynamic_fields=args.dynamic_fields,
    )
    new_query = sdk.create_query(body=body)
    result_format = args.format or "json"
    raw = _run_query_by_id(sdk, new_query.id, result_format)
    if result_format == "json":
        data = json.loads(raw)
        print(json.dumps(data, indent=2))
    else:
        print(raw)


def cmd_describe_explore(args):
    sdk = get_sdk()

    api_fields = "fields"
    if args.full or args.include_joins:
        api_fields = "fields,joins"

    explore = sdk.lookml_model_explore(
        lookml_model_name=args.model,
        explore_name=args.view,
        fields=api_fields,
    )

    if args.names_only:
        names = []
        for _kind, field_list in [
            ("dimension", explore.fields.dimensions or []),
            ("measure", explore.fields.measures or []),
        ]:
            for f in field_list:
                name = f.name or ""
                if args.filter and args.filter.lower() not in name.lower():
                    continue
                names.append(name)
        print(json.dumps(names, indent=2))
        return

    results = []
    dim_count = 0
    measure_count = 0

    for kind, field_list in [
        ("dimension", explore.fields.dimensions or []),
        ("measure", explore.fields.measures or []),
    ]:
        for f in field_list:
            name = f.name or ""
            if args.filter and args.filter.lower() not in name.lower():
                continue
            if kind == "dimension":
                dim_count += 1
            else:
                measure_count += 1

            if args.full:
                entry = {
                    "name": name,
                    "kind": kind,
                    "type": f.type or "",
                    "label": getattr(f, "label", None) or "",
                    "tags": getattr(f, "tags", None) or [],
                    "description": f.description or "",
                    "sql": getattr(f, "sql", None) or "",
                    "hidden": getattr(f, "hidden", None),
                }
            else:
                entry = {
                    "name": name,
                    "kind": kind,
                    "type": f.type or "",
                    "label": getattr(f, "label", None) or "",
                    "tags": getattr(f, "tags", None) or [],
                }
                if f.description:
                    entry["description"] = f.description
            results.append(entry)

    total = dim_count + measure_count
    if not args.filter and not args.full and total > 100:
        summary = {
            "dimensions": dim_count,
            "measures": measure_count,
            "hint": "Use --filter <keyword> or --names-only to narrow results",
        }
        print(json.dumps(summary, indent=2))
        return

    output = {"fields": results}

    if args.full or args.include_joins:
        joins = []
        for j in explore.joins or []:
            joins.append({
                "name": j.name or "",
                "relationship": j.relationship or "",
                "type": j.type or "",
                "sql_on": getattr(j, "sql_on", None) or "",
            })
        output["joins"] = joins

    print(json.dumps(output, indent=2))


def cmd_search(args):
    sdk = get_sdk()
    results = sdk.search_dashboards(
        title=args.title,
        folder_id=args.folder_id,
        limit=args.limit,
        fields="id,title,description,folder,user_id,slug,view_count,created_at,updated_at",
    )
    print(json.dumps(to_json(results), indent=2))


def cmd_get(args):
    sdk = get_sdk()
    if args.full:
        dashboard = sdk.dashboard(dashboard_id=args.id)
    else:
        dashboard = sdk.dashboard(
            dashboard_id=args.id,
            fields="id,title,description,folder,slug,view_count,created_at,updated_at,dashboard_elements,dashboard_filters",
        )
    print(json.dumps(to_json(dashboard), indent=2))


def cmd_update(args):
    sdk = get_sdk()
    body_kwargs = {}
    if args.title is not None:
        body_kwargs["title"] = args.title
    if args.description is not None:
        body_kwargs["description"] = args.description
    if args.folder_id is not None:
        body_kwargs["folder_id"] = args.folder_id
    if args.show_title is not None:
        body_kwargs["show_title"] = args.show_title.lower() == "true"
    if args.refresh_interval is not None:
        body_kwargs["refresh_interval"] = args.refresh_interval

    if not body_kwargs:
        print("Error: no update fields provided", file=sys.stderr)
        sys.exit(1)

    body = models40.WriteDashboard(**body_kwargs)
    result = sdk.update_dashboard(dashboard_id=args.id, body=body)
    print(json.dumps({
        "id": result.id,
        "updated": True,
        "changed_fields": list(body_kwargs.keys()),
        "updated_at": result.updated_at.isoformat() if result.updated_at else None,
    }, indent=2))


def cmd_list_elements(args):
    sdk = get_sdk()
    elements = sdk.dashboard_dashboard_elements(dashboard_id=args.dashboard_id)
    if not args.full:
        import urllib.parse
        summaries = []
        for el in elements:
            entry = {
                "id": el.id,
                "title": el.title,
                "type": el.type,
            }
            q = el.query
            if q:
                entry["model"] = q.model
                entry["view"] = q.view
                entry["fields"] = q.fields
                entry["pivots"] = q.pivots
                entry["filters"] = q.filters
                entry["filter_expression"] = q.filter_expression
                df = q.dynamic_fields
                if df:
                    if isinstance(df, str):
                        try:
                            df = json.loads(urllib.parse.unquote(df))
                        except (json.JSONDecodeError, TypeError):
                            df = None
                    if isinstance(df, list):
                        entry["dynamic_fields"] = [
                            {
                                k: d.get(k)
                                for k in ("label", "dimension", "table_calculation", "expression", "calculation_type")
                                if d.get(k)
                            }
                            for d in df
                        ]
            summaries.append(entry)
        print(json.dumps(summaries, indent=2))
    else:
        print(json.dumps(to_json(elements), indent=2))


def cmd_get_element(args):
    sdk = get_sdk()
    element = sdk.dashboard_element(dashboard_element_id=args.id)
    print(json.dumps(to_json(element), indent=2))


def cmd_update_element(args):
    sdk = get_sdk()
    body_kwargs = {}
    if args.title is not None:
        body_kwargs["title"] = args.title
    if args.title_hidden is not None:
        body_kwargs["title_hidden"] = args.title_hidden.lower() == "true"
    if args.body_text is not None:
        body_kwargs["body_text"] = args.body_text
    if args.note_text is not None:
        body_kwargs["note_text"] = args.note_text
    if args.subtitle_text is not None:
        body_kwargs["subtitle_text"] = args.subtitle_text

    if not body_kwargs:
        print("Error: no update fields provided", file=sys.stderr)
        sys.exit(1)

    body = models40.WriteDashboardElement(**body_kwargs)
    result = sdk.update_dashboard_element(dashboard_element_id=args.id, body=body)
    print(json.dumps({
        "id": result.id,
        "updated": True,
        "changed_fields": list(body_kwargs.keys()),
    }, indent=2))


def cmd_delete_element(args):
    sdk = get_sdk()
    sdk.delete_dashboard_element(dashboard_element_id=args.id)
    print(json.dumps({"deleted": args.id}))


def cmd_list_filters(args):
    sdk = get_sdk()
    filters = sdk.dashboard_dashboard_filters(dashboard_id=args.dashboard_id)
    if getattr(args, "full", False):
        print(json.dumps(to_json(filters), indent=2))
    else:
        summary = [{
            "id": f.id,
            "name": f.name,
            "title": f.title,
            "type": f.type,
            "default_value": f.default_value,
        } for f in filters]
        print(json.dumps(summary, indent=2))


def cmd_update_filter(args):
    sdk = get_sdk()
    body_kwargs = {}
    if args.title is not None:
        body_kwargs["title"] = args.title
    if args.default_value is not None:
        body_kwargs["default_value"] = args.default_value
    if args.name is not None:
        body_kwargs["name"] = args.name

    if not body_kwargs:
        print("Error: no update fields provided", file=sys.stderr)
        sys.exit(1)

    body = models40.WriteDashboardFilter(**body_kwargs)
    result = sdk.update_dashboard_filter(dashboard_filter_id=args.id, body=body)
    print(json.dumps({
        "id": result.id,
        "updated": True,
        "changed_fields": list(body_kwargs.keys()),
    }, indent=2))


def cmd_list_layouts(args):
    sdk = get_sdk()
    layouts = sdk.dashboard_dashboard_layouts(dashboard_id=args.dashboard_id)
    if getattr(args, "full", False):
        print(json.dumps(to_json(layouts), indent=2))
    else:
        summary = [{
            "id": layout.id,
            "dashboard_id": layout.dashboard_id,
            "type": layout.type,
            "layout_components_count": len(layout.dashboard_layout_components or []),
        } for layout in layouts]
        print(json.dumps(summary, indent=2))


def cmd_get_query(args):
    sdk = get_sdk()
    element = sdk.dashboard_element(dashboard_element_id=args.element_id)
    query = element.result_maker.query if element.result_maker else None
    if not query:
        print("Error: element has no query", file=sys.stderr)
        sys.exit(1)
    output = {
        "query_id": query.id,
        "model": query.model,
        "view": query.view,
        "fields": query.fields,
        "filters": query.filters,
        "filter_expression": query.filter_expression,
        "sorts": query.sorts,
        "limit": query.limit,
        "dynamic_fields": query.dynamic_fields,
    }
    print(json.dumps(output, indent=2))


def cmd_clone_element(args):
    sdk = get_sdk()
    source = sdk.dashboard_element(dashboard_element_id=args.source_id)
    query = source.result_maker.query if source.result_maker else None
    if not query:
        print("Error: source element has no query", file=sys.stderr)
        sys.exit(1)

    filter_expr = query.filter_expression
    if args.filter_replace:
        old, new = args.filter_replace.split("|||", 1)
        if old not in filter_expr:
            print(f"Warning: '{old}' not found in filter_expression", file=sys.stderr)
        filter_expr = filter_expr.replace(old, new)

    new_query = sdk.create_query(body=models40.WriteQuery(
        model=query.model,
        view=query.view,
        fields=query.fields,
        filters=query.filters,
        filter_expression=filter_expr,
        sorts=query.sorts,
        limit=str(query.limit) if query.limit else None,
        column_limit=str(query.column_limit) if query.column_limit else None,
        vis_config=query.vis_config,
        dynamic_fields=query.dynamic_fields,
    ))

    dashboard_id = args.dashboard_id or source.dashboard_id
    title = args.title or f"{source.title} (copy)"

    new_element = sdk.create_dashboard_element(body=models40.WriteDashboardElement(
        dashboard_id=str(dashboard_id),
        query_id=new_query.id,
        title=title,
        type=source.type,
    ))

    print(json.dumps({
        "element_id": new_element.id,
        "title": new_element.title,
        "query_id": new_query.id,
        "dashboard_id": dashboard_id,
    }, indent=2))


def cmd_create_element(args):
    sdk = get_sdk()
    body_kwargs = {
        "dashboard_id": args.dashboard_id,
        "type": args.type,
    }
    if args.title is not None:
        body_kwargs["title"] = args.title
    if args.query_id is not None:
        body_kwargs["query_id"] = args.query_id
    if args.body_text is not None:
        body_kwargs["body_text"] = args.body_text

    element = sdk.create_dashboard_element(
        body=models40.WriteDashboardElement(**body_kwargs)
    )
    print(json.dumps(to_json(element), indent=2))


def cmd_create_query(args):
    if args.file:
        with open(args.file) as f:
            spec = json.load(f)
    else:
        spec = json.loads(sys.stdin.read())

    if "model" not in spec or "view" not in spec:
        print("Error: JSON spec must include 'model' and 'view'", file=sys.stderr)
        sys.exit(1)

    query_kwargs = {
        "model": spec["model"],
        "view": spec["view"],
    }
    if "fields" in spec:
        query_kwargs["fields"] = spec["fields"]
    if "filters" in spec:
        query_kwargs["filters"] = spec["filters"]
    if "filter_expression" in spec:
        query_kwargs["filter_expression"] = spec["filter_expression"]
    if "sorts" in spec:
        query_kwargs["sorts"] = spec["sorts"]
    if "limit" in spec:
        query_kwargs["limit"] = str(spec["limit"]) if spec["limit"] is not None else None
    if "column_limit" in spec:
        query_kwargs["column_limit"] = str(spec["column_limit"]) if spec["column_limit"] is not None else None
    if "pivots" in spec:
        query_kwargs["pivots"] = spec["pivots"]
    if "dynamic_fields" in spec:
        query_kwargs["dynamic_fields"] = json.dumps(spec["dynamic_fields"]) if spec["dynamic_fields"] is not None else None
    if "vis_config" in spec:
        query_kwargs["vis_config"] = spec["vis_config"]

    sdk = get_sdk()
    new_query = sdk.create_query(body=models40.WriteQuery(**query_kwargs))

    if args.run:
        raw = _run_query_by_id(sdk, new_query.id, "json")
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
        print(json.dumps({"query_id": new_query.id, "row_count": len(data), "data": data}, indent=2))
    else:
        output = {
            "query_id": new_query.id,
            "model": new_query.model,
            "view": new_query.view,
            "fields": new_query.fields,
        }
        print(json.dumps(output, indent=2))


def cmd_get_look(args):
    sdk = get_sdk()
    look = sdk.look(look_id=args.look_id)
    output = {
        "id": look.id,
        "title": look.title,
        "description": look.description,
        "model": look.model.id if look.model else None,
        "query_id": look.query_id,
        "folder": to_json(look.folder),
    }
    if look.query:
        q = look.query
        output["query"] = {
            "model": q.model,
            "view": q.view,
            "fields": q.fields,
            "filters": q.filters,
            "filter_expression": q.filter_expression,
            "sorts": q.sorts,
            "limit": q.limit,
            "pivots": q.pivots,
            "dynamic_fields": q.dynamic_fields,
        }
    print(json.dumps(output, indent=2))


def cmd_run_look(args):
    sdk = get_sdk()
    import requests as req

    try:
        auth_headers = sdk.auth.authenticate()
    except TypeError:
        auth_headers = sdk.auth.authenticate(transport_options={})
    resp = req.get(
        f"{LOOKER_API_URL}/looks/{args.look_id}/run/json",
        headers=auth_headers,
        params={"limit": args.limit},
    )
    resp.raise_for_status()
    data = resp.json()
    print(json.dumps(data, indent=2))


def cmd_run_query_id(args):
    sdk = get_sdk()
    result_format = args.format or "json"
    raw = _run_query_by_id(sdk, args.query_id, result_format)
    if result_format == "json":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
        if args.limit:
            data = data[: args.limit]
        print(json.dumps(data, indent=2))
    else:
        print(raw)


_callback_event = threading.Event()
_callback_result = {}


class _OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures the OAuth callback code."""

    def do_GET(self):
        if self.path.startswith("/callback"):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            _callback_result["params"] = params
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this tab.")
        else:
            self.send_response(204)
            self.end_headers()
        _callback_event.set()
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, fmt, *log_args):
        pass


def cmd_login(args):
    """Authenticate with Looker via browser-based OAuth PKCE flow."""
    _callback_event.clear()
    _callback_result.clear()
    session = _create_oauth_session()
    state = str(uuid.uuid4())

    auth_url = session.create_auth_code_request_url("cors_api", state)

    try:
        server = HTTPServer(("127.0.0.1", CALLBACK_PORT), _OAuthCallbackHandler)
    except OSError as e:
        print(f"Error: Could not start callback server on port {CALLBACK_PORT}: {e}", file=sys.stderr)
        sys.exit(1)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    print("Opening browser for Looker authentication...")
    print(f"  URL: {auth_url}")
    webbrowser.open(auth_url)

    if not _callback_event.wait(timeout=300):
        server.shutdown()
        print("Error: Authentication timed out (5 minutes).", file=sys.stderr)
        sys.exit(1)

    server.shutdown()
    thread.join(timeout=5)

    params = _callback_result.get("params", {})

    if "error" in params:
        error = params["error"][0]
        desc = params.get("error_description", [""])[0]
        print(f"Error: OAuth failed: {error} - {desc}", file=sys.stderr)
        sys.exit(1)

    callback_state = params.get("state", [""])[0]
    if callback_state != state:
        print("Error: OAuth state mismatch (possible CSRF). Try again.", file=sys.stderr)
        sys.exit(1)

    code = params.get("code", [""])[0]
    if not code:
        print("Error: No authorization code received.", file=sys.stderr)
        sys.exit(1)

    session.redeem_auth_code(code)
    _save_session_token(session)

    sdk = methods40.Looker40SDK(
        auth=session,
        deserialize=session.deserialize,
        serialize=session.serialize,
        transport=session.transport,
        api_version="4.0",
    )
    user = sdk.me()
    print(f"Authenticated as: {user.display_name} ({user.email})")
    print("Token saved to macOS Keychain.")


def cmd_me(args):
    sdk = get_sdk()
    user = sdk.me()
    print(json.dumps(to_json(user), indent=2))


def cmd_list_models(args):
    sdk = get_sdk()
    models = sdk.all_lookml_models(
        fields="name,project_name,allowed_db_connection_names,explores",
    )
    results = []
    for m in models:
        entry = {
            "name": m.name,
            "project_name": m.project_name,
            "explore_count": len(m.explores) if m.explores else 0,
        }
        if args.full:
            entry["allowed_db_connection_names"] = m.allowed_db_connection_names or []
            entry["explores"] = [e.name for e in (m.explores or [])]
        results.append(entry)
    print(json.dumps(results, indent=2))


def cmd_search_content(args):
    sdk = get_sdk()
    content_results = sdk.search_content(terms=args.terms, limit=args.limit)
    folder_results = sdk.search_folders(name=args.terms, limit=args.limit)

    content = []
    for item in content_results:
        entry = {
            "content_id": item.content_id,
            "title": item.title,
            "type": item.type,
            "description": item.description,
            "folder_name": item.folder_name,
        }
        content.append(entry)

    folders = []
    for f in folder_results:
        folders.append({
            "id": f.id,
            "name": f.name,
            "parent_id": f.parent_id,
        })

    output = {
        "content": content,
        "folders": folders,
        "content_count": len(content),
        "folder_count": len(folders),
    }
    print(json.dumps(output, indent=2))


def cmd_search_looks(args):
    sdk = get_sdk()
    results = sdk.search_looks(
        title=args.title,
        folder_id=args.folder_id,
        limit=args.limit,
        fields="id,title,description,folder,user_id,view_count,created_at,updated_at",
    )
    print(json.dumps(to_json(results), indent=2))


def cmd_get_folder(args):
    sdk = get_sdk()

    folder_id = args.folder_id
    if "/folders/" in folder_id:
        folder_id = folder_id.split("/folders/")[1].split("?")[0].split("#")[0]

    metadata = sdk.folder(folder_id=folder_id, fields="id,name,parent_id")
    dashboards = sdk.folder_dashboards(folder_id=folder_id, fields="id,title")
    looks = sdk.folder_looks(folder_id=folder_id, fields="id,title")
    children = sdk.folder_children(folder_id=folder_id, fields="id,name")

    output = {
        "metadata": {
            "id": metadata.id,
            "name": metadata.name,
            "parent_id": metadata.parent_id,
        },
        "dashboards": [{"id": d.id, "title": d.title} for d in dashboards],
        "looks": [{"id": lk.id, "title": lk.title} for lk in looks],
        "child_folders": [{"id": c.id, "name": c.name} for c in children],
    }
    print(json.dumps(output, indent=2))


def _resolve_query_id(sdk, element):
    """Resolve the query ID for a dashboard element, or None for text-only tiles."""
    if element.query_id:
        return element.query_id
    if element.result_maker and element.result_maker.query and element.result_maker.query.id:
        return element.result_maker.query.id
    if element.look_id:
        look = sdk.look(look_id=element.look_id)
        if look.query_id:
            return look.query_id
    return None


def _run_tile(sdk, element, query_id, limit, auth_headers=None):
    """Run a single tile's query and return structured result."""
    try:
        raw = _run_query_by_id(sdk, query_id, "json", auth_headers=auth_headers)
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
        row_count = len(data)
        truncated = row_count > limit
        if truncated:
            data = data[:limit]
        columns = list(data[0].keys()) if data else []
        return {
            "element_id": element.id,
            "title": element.title,
            "query_id": query_id,
            "row_count": row_count,
            "columns": columns,
            "data": data,
            "truncated": truncated,
            "error": None,
        }
    except Exception as e:
        return {
            "element_id": element.id,
            "title": element.title,
            "query_id": query_id,
            "row_count": 0,
            "columns": [],
            "data": [],
            "truncated": False,
            "error": str(e),
        }


def cmd_run_dashboard(args):
    sdk = get_sdk()
    dashboard = sdk.dashboard(dashboard_id=args.id)
    limit = args.limit
    tile_filter = args.tile

    elements = dashboard.dashboard_elements or []

    runnable = []
    for el in elements:
        query_id = _resolve_query_id(sdk, el)
        if query_id is None:
            continue
        if tile_filter:
            id_match = str(el.id) == tile_filter
            title_match = el.title and tile_filter.lower() in el.title.lower()
            if not id_match and not title_match:
                continue
        runnable.append((el, query_id))

    try:
        auth_headers = sdk.auth.authenticate()
    except TypeError:
        auth_headers = sdk.auth.authenticate(transport_options={})

    tiles = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_element = {
            executor.submit(_run_tile, sdk, el, qid, limit, auth_headers=auth_headers): el
            for el, qid in runnable
        }
        for future in as_completed(future_to_element):
            tiles.append(future.result())

    tiles.sort(key=lambda t: str(t["element_id"]))

    tiles_with_data = sum(1 for t in tiles if t["error"] is None and t["row_count"] > 0)
    tiles_with_errors = sum(1 for t in tiles if t["error"] is not None)

    output = {
        "dashboard_id": args.id,
        "dashboard_title": dashboard.title,
        "tiles": tiles,
        "tile_count": len(tiles),
        "tiles_with_data": tiles_with_data,
        "tiles_with_errors": tiles_with_errors,
    }
    print(json.dumps(output, indent=2))


def cmd_create_look(args):
    sdk = get_sdk()
    body_kwargs = {
        "title": args.title,
        "query_id": args.query_id,
    }
    if args.description is not None:
        body_kwargs["description"] = args.description
    if args.folder_id is not None:
        body_kwargs["folder_id"] = args.folder_id
    else:
        user = sdk.me(fields="personal_folder_id")
        body_kwargs["folder_id"] = user.personal_folder_id

    look = sdk.create_look(body=models40.WriteLookWithQuery(**body_kwargs))
    print(json.dumps({
        "id": look.id,
        "title": look.title,
        "query_id": look.query_id,
        "folder_id": look.folder_id,
        "short_url": look.short_url,
    }, indent=2))


def cmd_update_look(args):
    sdk = get_sdk()
    body_kwargs = {}
    if args.title is not None:
        body_kwargs["title"] = args.title
    if args.description is not None:
        body_kwargs["description"] = args.description
    if args.folder_id is not None:
        body_kwargs["folder_id"] = args.folder_id
    if args.query_id is not None:
        body_kwargs["query_id"] = args.query_id

    if not body_kwargs:
        print("Error: no update fields provided", file=sys.stderr)
        sys.exit(1)

    result = sdk.update_look(look_id=args.id, body=models40.WriteLookWithQuery(**body_kwargs))
    print(json.dumps({
        "id": result.id,
        "updated": True,
        "changed_fields": list(body_kwargs.keys()),
        "updated_at": result.updated_at.isoformat() if result.updated_at else None,
    }, indent=2))


def cmd_delete_look(args):
    sdk = get_sdk()
    sdk.delete_look(look_id=args.id)
    print(json.dumps({"deleted": args.id}))


def cmd_security_lookup(args):
    import requests as req

    sdk = get_sdk()
    me = sdk.me(fields="email")
    email = me.email
    if not email:
        print("Error: could not determine user email from Looker", file=sys.stderr)
        sys.exit(1)
    ldap = email.split("@")[0]

    url = args.url
    if not url.startswith("http"):
        url = f"{LOOKER_BASE_URL}/{url.lstrip('/')}"

    try:
        resp = req.get(
            "https://looker-bellhop.sqprod.co/api/security/lookup/single",
            params={"ldap": ldap, "url": url},
            timeout=30,
        )
    except req.ConnectionError as e:
        print(f"Error: could not connect to Bellhop: {e}", file=sys.stderr)
        sys.exit(1)
    except req.Timeout:
        print("Error: Bellhop request timed out", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"Error: Bellhop returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(resp.json(), indent=2))


def main():
    parser = argparse.ArgumentParser(description="Looker Dashboard CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p = sub.add_parser("search", help="Search dashboards by title")
    p.add_argument("--title", help="Title substring to search")
    p.add_argument("--folder-id", help="Filter by folder ID")
    p.add_argument("--limit", type=int, default=20, help="Max results")

    # get
    p = sub.add_parser("get", help="Get full dashboard details")
    p.add_argument("id", help="Dashboard ID")
    p.add_argument("--full", action="store_true", help="Show all fields (default: compact subset)")

    # update
    p = sub.add_parser("update", help="Update dashboard properties")
    p.add_argument("id", help="Dashboard ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--description", help="New description")
    p.add_argument("--folder-id", help="Move to folder")
    p.add_argument("--show-title", help="Show title (true/false)")
    p.add_argument("--refresh-interval", help="Auto-refresh interval")

    # list-elements
    p = sub.add_parser("list-elements", help="List dashboard tiles/elements")
    p.add_argument("dashboard_id", help="Dashboard ID")
    p.add_argument("--full", action="store_true", help="Show full element details (default: compact summary)")

    # get-element
    p = sub.add_parser("get-element", help="Get a dashboard element")
    p.add_argument("id", help="Element ID")

    # update-element
    p = sub.add_parser("update-element", help="Update a dashboard element")
    p.add_argument("id", help="Element ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--title-hidden", help="Hide title (true/false)")
    p.add_argument("--body-text", help="Body text (for text tiles)")
    p.add_argument("--note-text", help="Note text")
    p.add_argument("--subtitle-text", help="Subtitle text")

    # delete-element
    p = sub.add_parser("delete-element", help="Delete a dashboard element")
    p.add_argument("id", help="Element ID")

    # list-filters
    p = sub.add_parser("list-filters", help="List dashboard filters")
    p.add_argument("dashboard_id", help="Dashboard ID")
    p.add_argument("--full", action="store_true", help="Show full filter details")

    # update-filter
    p = sub.add_parser("update-filter", help="Update a dashboard filter")
    p.add_argument("id", help="Filter ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--default-value", help="New default value")
    p.add_argument("--name", help="New filter name")

    # list-layouts
    p = sub.add_parser("list-layouts", help="List dashboard layouts")
    p.add_argument("dashboard_id", help="Dashboard ID")
    p.add_argument("--full", action="store_true", help="Show full layout details")

    # get-query
    p = sub.add_parser("get-query", help="Get the query behind a dashboard element")
    p.add_argument("element_id", help="Element ID")

    # query-by-slug
    p = sub.add_parser("query-by-slug", help="Get query definition by slug (qid from Explore URLs)")
    p.add_argument("slug", help="Query slug (the qid parameter from Explore URLs)")

    # run-query
    p = sub.add_parser("run-query", help="Run a saved query by its slug (qid)")
    p.add_argument("slug", help="Query slug (the qid parameter from Explore URLs)")
    p.add_argument("--limit", type=int, help="Max rows to return")
    p.add_argument("--format", choices=["json", "csv", "txt"], default="json", help="Output format")

    # run-explore
    p = sub.add_parser("run-explore", help="Run an ad-hoc inline query against a Looker Explore")
    p.add_argument("--model", required=True, help="LookML model name (e.g., Square)")
    p.add_argument("--view", required=True, help="Explore/view name (e.g., fact_pull_requests)")
    p.add_argument("--fields", required=True, help="Comma-separated list of fields")
    p.add_argument("--pivots", help="Comma-separated list of pivot fields")
    p.add_argument("--filters", nargs="*", help="Filters as key=value pairs (e.g., dim.name=value)")
    p.add_argument("--sorts", help="Comma-separated sort fields (e.g., 'measure desc')")
    p.add_argument("--limit", type=int, default=50, help="Row limit (default: 50)")
    p.add_argument("--dynamic-fields", dest="dynamic_fields", help="JSON string of dynamic field definitions")
    p.add_argument("--format", choices=["json", "csv", "txt"], default="json", help="Output format")

    # clone-element
    p = sub.add_parser("clone-element", help="Clone a tile, optionally modifying its query")
    p.add_argument("source_id", help="Source element ID to clone")
    p.add_argument("--title", help="Title for the new element")
    p.add_argument("--dashboard-id", help="Target dashboard ID (defaults to same dashboard)")
    p.add_argument(
        "--filter-replace",
        help="Replace text in filter_expression: 'old|||new' (triple-pipe delimiter)",
    )

    # create-element
    p = sub.add_parser("create-element", help="Create a new dashboard element")
    p.add_argument("dashboard_id", help="Dashboard ID")
    p.add_argument("--type", default="vis", help="Element type (vis, text, etc.)")
    p.add_argument("--title", help="Element title")
    p.add_argument("--query-id", help="Query ID to attach")
    p.add_argument("--body-text", help="Body text (for text tiles)")

    # create-query
    p = sub.add_parser("create-query", help="Create a query from JSON spec (file or stdin)")
    p.add_argument("--file", "-f", help="Path to JSON file (reads stdin if omitted)")
    p.add_argument("--run", action="store_true", help="Also run the query and print results")

    # get-look
    p = sub.add_parser("get-look", help="Get look metadata (title, query, folder)")
    p.add_argument("look_id", help="Look ID")

    # run-look
    p = sub.add_parser("run-look", help="Run a look and return JSON results")
    p.add_argument("look_id", help="Look ID")
    p.add_argument("--limit", type=int, default=50, help="Max rows (default: 50)")

    # run-query-id
    p = sub.add_parser("run-query-id", help="Run a query by its numeric ID")
    p.add_argument("query_id", help="Query ID")
    p.add_argument("--limit", type=int, help="Max rows to return")
    p.add_argument("--format", choices=["json", "csv", "txt"], default="json", help="Output format")

    # describe-explore
    p = sub.add_parser("describe-explore", help="List dimensions and measures for a Looker Explore")
    p.add_argument("--model", required=True, help="LookML model name (e.g., Square)")
    p.add_argument("--view", required=True, help="Explore/view name (e.g., fact_pull_requests)")
    p.add_argument("--filter", help="Substring filter on field names (e.g., 'author')")
    p.add_argument("--names-only", action="store_true", help="Return just field names")
    p.add_argument("--include-joins", action="store_true", help="Include join information")
    p.add_argument("--full", action="store_true", help="Full metadata including joins, sql, hidden")

    # list-models
    p = sub.add_parser("list-models", help="List all LookML models")
    p.add_argument("--full", action="store_true", help="Include explores and connections")

    # search-content
    p = sub.add_parser("search-content", help="Search across dashboards, looks, and folders")
    p.add_argument("terms", help="Search terms")
    p.add_argument("--limit", type=int, default=10, help="Max results per type")

    # search-looks
    p = sub.add_parser("search-looks", help="Search looks by title")
    p.add_argument("--title", help="Title substring to search")
    p.add_argument("--folder-id", help="Filter by folder ID")
    p.add_argument("--limit", type=int, default=20, help="Max results")

    # get-folder
    p = sub.add_parser("get-folder", help="Get folder contents (dashboards, looks, subfolders)")
    p.add_argument("folder_id", help="Folder ID or full Looker folder URL")

    # run-dashboard
    p = sub.add_parser("run-dashboard", help="Run all tiles in a dashboard and return results")
    p.add_argument("id", help="Dashboard ID")
    p.add_argument("--limit", type=int, default=50, help="Max rows per tile (default: 50)")
    p.add_argument("--tile", help="Run only a specific tile (element ID or title substring)")

    # create-look
    p = sub.add_parser("create-look", help="Create a new Look")
    p.add_argument("--title", required=True, help="Look title")
    p.add_argument("--query-id", required=True, help="Query ID to attach")
    p.add_argument("--description", help="Look description")
    p.add_argument("--folder-id", help="Folder ID to save in")

    # update-look
    p = sub.add_parser("update-look", help="Update an existing Look")
    p.add_argument("id", help="Look ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--description", help="New description")
    p.add_argument("--folder-id", help="Move to folder")
    p.add_argument("--query-id", help="New query ID")

    # delete-look
    p = sub.add_parser("delete-look", help="Delete a Look")
    p.add_argument("id", help="Look ID")

    # security-lookup
    p = sub.add_parser("security-lookup", help="Check permissions for a Looker URL via Bellhop")
    p.add_argument("url", help="Looker URL (dashboard, look, folder, or explore)")

    # login
    sub.add_parser("login", help="Authenticate with Looker via browser (OAuth PKCE)")

    # me
    sub.add_parser("me", help="Get current authenticated user")

    args = parser.parse_args()

    commands = {
        "login": cmd_login,
        "search": cmd_search,
        "get": cmd_get,
        "update": cmd_update,
        "list-elements": cmd_list_elements,
        "get-element": cmd_get_element,
        "update-element": cmd_update_element,
        "delete-element": cmd_delete_element,
        "list-filters": cmd_list_filters,
        "update-filter": cmd_update_filter,
        "list-layouts": cmd_list_layouts,
        "get-query": cmd_get_query,
        "query-by-slug": cmd_query_by_slug,
        "run-query": cmd_run_query,
        "run-explore": cmd_run_explore,
        "clone-element": cmd_clone_element,
        "describe-explore": cmd_describe_explore,
        "create-element": cmd_create_element,
        "create-query": cmd_create_query,
        "get-look": cmd_get_look,
        "run-look": cmd_run_look,
        "run-query-id": cmd_run_query_id,
        "me": cmd_me,
        "list-models": cmd_list_models,
        "search-content": cmd_search_content,
        "search-looks": cmd_search_looks,
        "get-folder": cmd_get_folder,
        "run-dashboard": cmd_run_dashboard,
        "create-look": cmd_create_look,
        "update-look": cmd_update_look,
        "delete-look": cmd_delete_look,
        "security-lookup": cmd_security_lookup,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
