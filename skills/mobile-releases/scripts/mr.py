#!/usr/bin/env python3
"""CLI for releases.example.com.

Provides structured JSON output for listing projects, versions, builds,
and downloading artifacts. Uses only Python stdlib (no pip dependencies).

API endpoints:
  /api/applications.json                                   — all projects
  /api/<app-id>/<platform>.json                            — versions + latest builds
  /api/builds/<app-id>/<version>/<platform>.json?page=&perPage= — all builds for a version
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse

BASE_URL = "https://releases.example.com"
ALLOWED_HOSTS = {"releases.example.com"}
VALID_APP_ID = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$')
VALID_PLATFORM = {"android", "ios", "ios_zip", "android_zip"}
VALID_VERSION = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$')


def validate_app_id(app_id):
    if not VALID_APP_ID.match(app_id):
        print(f"Invalid app ID: '{app_id}'. Must be alphanumeric with hyphens/underscores.", file=sys.stderr)
        sys.exit(1)


def validate_platform(platform):
    if platform not in VALID_PLATFORM:
        print(f"Invalid platform: '{platform}'. Must be one of: {', '.join(sorted(VALID_PLATFORM))}", file=sys.stderr)
        sys.exit(1)


def validate_version(version):
    if not VALID_VERSION.match(version):
        print(f"Invalid version: '{version}'. Must be alphanumeric with dots/hyphens.", file=sys.stderr)
        sys.exit(1)


def fetch_json(url, timeout=30):
    """Fetch a URL and parse as JSON."""
    req = urllib.request.Request(url, headers={"User-Agent": "mr.py/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason} for {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason} for {url}", file=sys.stderr)
        sys.exit(1)


def ipa_url_from_plist(itms_url):
    """Derive an .ipa download URL from an itms-services plist URL.

    Input:  itms-services://?action=download-manifest&amp;url=https://.../<sha>.plist
    Output: https://.../<sha>.ipa
    """
    # Extract the plist URL from the itms-services scheme
    match = re.search(r'url=(.+\.plist)', itms_url)
    if match:
        plist_url = match.group(1)
        return plist_url.rsplit('.plist', 1)[0] + '.ipa'
    return None


def cmd_list_projects(_args):
    data = fetch_json(f"{BASE_URL}/api/applications.json")
    projects = [
        {
            "id": app["urlFriendlyName"],
            "name": app["name"],
            "platforms": app["platforms"],
        }
        for app in data.get("applications", [])
    ]
    print(json.dumps(projects, indent=2))


def cmd_list_versions(args):
    validate_app_id(args.app_id)
    validate_platform(args.platform)

    data = fetch_json(f"{BASE_URL}/api/{args.app_id}/{args.platform}.json")

    versions = []
    for v in data.get("versions", []):
        version_info = {"version": v["human_name"]}
        variant_names = [var["name"] for var in v.get("variants", [])]
        if variant_names:
            version_info["variants"] = variant_names
        versions.append(version_info)

    result = {
        "app_id": args.app_id,
        "platform": args.platform,
        "versions": versions,
    }
    print(json.dumps(result, indent=2))


def cmd_list_builds(args):
    validate_app_id(args.app_id)
    validate_platform(args.platform)
    validate_version(args.version)

    data = fetch_json(
        f"{BASE_URL}/api/builds/{args.app_id}/{args.version}/{args.platform}.json"
        f"?page=1&perPage=50"
    )

    is_ios = args.platform.startswith("ios")

    builds = []
    for entry in data:
        for var in entry.get("variants", []):
            build = {
                "variant": var["name"],
                "build_number": entry.get("build_number"),
                "sha": entry.get("sha"),
                "timestamp": var.get("unix_timestamp"),
                "size_mb": round(var.get("size", 0) / (1024 * 1024), 2) if var.get("size") else None,
                "download_url": var.get("url"),
            }
            # For iOS, derive the direct .ipa URL from the plist link
            if is_ios and build["download_url"]:
                ipa = ipa_url_from_plist(build["download_url"])
                if ipa:
                    build["ipa_url"] = ipa
            if var.get("notes"):
                build["notes"] = var["notes"]
            # Remove None values
            build = {k: v for k, v in build.items() if v is not None}
            builds.append(build)

    result = {
        "app_id": args.app_id,
        "platform": args.platform,
        "version": args.version,
        "builds": builds,
    }
    print(json.dumps(result, indent=2))


def cmd_download(args):
    url = args.url
    if not url.startswith("http"):
        url = BASE_URL + url

    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        print(f"Blocked: host '{parsed.hostname}' not in allowed list: {ALLOWED_HOSTS}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        filename = url.split("/")[-1]
        output_path = f"/tmp/mobile-releases/{filename}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Downloading to {output_path}...", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "mr.py/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            total = resp.headers.get("Content-Length")
            total = int(total) if total else None
            downloaded = 0
            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded * 100 // total
                        print(f"\r  {downloaded // (1024*1024)} / {total // (1024*1024)} MB ({pct}%)", end="", file=sys.stderr)
            print(file=sys.stderr)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason} for {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason} for {url}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    result = {"path": output_path, "size_mb": round(size_mb, 2)}
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Mobile Releases CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-projects", help="List all available projects")

    vp = sub.add_parser("list-versions", help="List versions for a project")
    vp.add_argument("app_id", help="Project ID (e.g. cash, register, dashboard)")
    vp.add_argument("platform", help="Platform (e.g. android, ios, ios_zip)")

    bp = sub.add_parser("list-builds", help="List builds for a specific version")
    bp.add_argument("app_id", help="Project ID")
    bp.add_argument("platform", help="Platform")
    bp.add_argument("version", help="Version (e.g. 5.40.0, master)")

    dp = sub.add_parser("download", help="Download an artifact")
    dp.add_argument("url", help="Download URL from list-builds output")
    dp.add_argument("--output", "-o", help="Output file path (default: /tmp/mobile-releases/<filename>)")

    args = parser.parse_args()

    commands = {
        "list-projects": cmd_list_projects,
        "list-versions": cmd_list_versions,
        "list-builds": cmd_list_builds,
        "download": cmd_download,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
