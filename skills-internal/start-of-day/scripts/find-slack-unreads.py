#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.27.0"]
# ///
"""
Find unread Slack conversations using a hybrid search + check strategy.

Sources:
1. DMs/mentions: search.messages to find recently active conversations
2. Group DMs: conversations.list(types=mpim)
3. Channel unreads (hybrid): priority channels always shown + all member
   channels filtered to last 12 hours of activity
4. Thread unreads: threads the user participated in with newer replies
"""

import asyncio
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

SLACK_API_BASE = "https://slack.com/api/"
DEFAULT_WORKSPACES = {
    "workspace_1": "WORKSPACE_ID_1",
    "workspace_2": "WORKSPACE_ID_2",
    "workspace_3": "WORKSPACE_ID_3",
}
MY_USER_ID = "YOUR_USER_ID"

# Channels that always show unreads regardless of recency
PRIORITY_CHANNELS = {
    "block": {
        "your-team-channel", "eng-mobile", "pos-engineering",
        "pos-team", "checkout", "payments",
        "feature-channel-1", "feature-channel-2",
        "product", "product-managers",
    },
}

# Only show non-priority channel unreads if latest message is within this window
CHANNEL_RECENCY_HOURS = 12


def get_token() -> str:
    import os
    env_token = os.environ.get("SLACK_TOKEN")
    if env_token:
        return env_token
    config_file = Path.home() / ".config" / "slack-skill" / "credentials.json"
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f).get("token", "")
    raise RuntimeError("No Slack token found")


async def search_active_channels(client: httpx.AsyncClient, team_id: str, days_back: int = 3) -> set[str]:
    """Use search.messages to find channels with recent activity."""
    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    channel_ids = set()
    queries = [
        f"to:me after:{cutoff}",
        f"from:me after:{cutoff}",
        f"has:mention after:{cutoff}",
    ]
    for q in queries:
        for page in range(1, 6):
            try:
                resp = await client.get("/search.messages", params={
                    "query": q, "count": 100, "sort": "timestamp", "sort_dir": "desc",
                    "team_id": team_id, "page": page,
                })
                data = resp.json()
                if not data.get("ok"):
                    break
                matches = data.get("messages", {}).get("matches", [])
                if not matches:
                    break
                for m in matches:
                    ch_id = m.get("channel", {}).get("id", "")
                    if ch_id:
                        channel_ids.add(ch_id)
            except Exception:
                break
            await asyncio.sleep(0.3)
    return channel_ids


async def list_recent_mpim(client: httpx.AsyncClient, team_id: str, limit: int = 200) -> list[str]:
    """List recent group DMs."""
    try:
        resp = await client.get("/conversations.list", params={
            "types": "mpim", "limit": limit, "team_id": team_id, "exclude_archived": "true",
        })
        data = resp.json()
        if data.get("ok"):
            return [ch["id"] for ch in data.get("channels", [])]
    except Exception:
        pass
    return []


async def get_member_channels(client: httpx.AsyncClient, team_id: str) -> list[dict]:
    """Get all public/private channels the user is a member of."""
    channels = []
    cursor = ""
    for _ in range(10):
        params = {"types": "public_channel,private_channel", "limit": 200,
                  "exclude_archived": "true", "team_id": team_id}
        if cursor:
            params["cursor"] = cursor
        resp = await client.get("/users.conversations", params=params)
        data = resp.json()
        if not data.get("ok"):
            break
        channels.extend(data.get("channels", []))
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break
    return channels


async def check_unread(client: httpx.AsyncClient, channel_id: str, sem: asyncio.Semaphore) -> dict | None:
    """Check if a channel/DM has unreads using last_read vs latest_ts comparison."""
    async with sem:
        try:
            info_resp, hist_resp = await asyncio.gather(
                client.get("/conversations.info", params={"channel": channel_id}),
                client.get("/conversations.history", params={"channel": channel_id, "limit": 1}),
            )
            info_data = info_resp.json()
            hist_data = hist_resp.json()
            if not info_data.get("ok") or not hist_data.get("ok"):
                return None

            ch = info_data.get("channel", {})
            last_read = ch.get("last_read", "0")
            msgs = hist_data.get("messages", [])
            if not msgs:
                return None

            latest = msgs[0]
            latest_ts = latest.get("ts", "0")

            # Use unread_count_display if available, fall back to ts comparison
            unread_count = ch.get("unread_count_display")
            has_unread = False
            if unread_count and unread_count > 0:
                has_unread = True
            elif float(latest_ts) > float(last_read):
                has_unread = True
                unread_count = unread_count or 1

            if has_unread:
                return {
                    "channel_id": channel_id,
                    "name": ch.get("name") or "",
                    "is_im": ch.get("is_im", False),
                    "is_mpim": ch.get("is_mpim", False),
                    "is_channel": ch.get("is_channel", False) or ch.get("is_group", False),
                    "unread_count": unread_count or 1,
                    "user": ch.get("user", ""),
                    "latest_text": latest.get("text", "")[:200],
                    "latest_ts": latest_ts,
                    "latest_user": latest.get("user", ""),
                    "latest_user_name": "",
                }
        except Exception:
            pass
    return None


async def check_channel_unread_with_recency(
    client: httpx.AsyncClient, ch_id: str, ch_name: str,
    sem: asyncio.Semaphore, priority_names: set[str], recency_cutoff_ts: float,
) -> dict | None:
    """Check a member channel for unreads, applying recency filter for non-priority."""
    async with sem:
        try:
            info_resp, hist_resp = await asyncio.gather(
                client.get("/conversations.info", params={"channel": ch_id}),
                client.get("/conversations.history", params={"channel": ch_id, "limit": 1}),
            )
            info = info_resp.json()
            hist = hist_resp.json()
            if not info.get("ok") or not hist.get("ok"):
                return None

            last_read = info["channel"].get("last_read", "0")
            msgs = hist.get("messages", [])
            if not msgs:
                return None

            latest = msgs[0]
            latest_ts = float(latest["ts"])
            if latest_ts <= float(last_read):
                return None

            is_priority = ch_name.lower() in priority_names
            if not is_priority and latest_ts < recency_cutoff_ts:
                return None

            return {
                "channel_id": ch_id,
                "name": ch_name,
                "is_im": False,
                "is_mpim": False,
                "is_channel": True,
                "is_priority": is_priority,
                "unread_count": 1,
                "user": "",
                "latest_text": latest.get("text", "")[:200],
                "latest_ts": latest["ts"],
                "latest_user": latest.get("user", ""),
                "latest_user_name": "",
            }
        except Exception:
            pass
    return None


async def find_thread_unreads(client: httpx.AsyncClient, team_id: str) -> list[dict]:
    """Find threads I participated in that have newer replies from others."""
    cutoff = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    threads_seen: dict[tuple[str, str], str] = {}  # (channel_id, thread_ts) -> my_latest_ts
    try:
        for page in range(1, 4):
            resp = await client.get("/search.messages", params={
                "query": f"from:me is:thread after:{cutoff}",
                "count": 50, "sort": "timestamp", "sort_dir": "desc",
                "team_id": team_id, "page": page,
            })
            data = resp.json()
            if not data.get("ok"):
                break
            matches = data.get("messages", {}).get("matches", [])
            if not matches:
                break
            for m in matches:
                ch_id = m.get("channel", {}).get("id", "")
                permalink = m.get("permalink", "")
                my_ts = m.get("ts", "")
                if not ch_id or not permalink:
                    continue
                # Extract thread_ts from permalink
                thread_ts = None
                ts_match = re.search(r'thread_ts=(\d+\.\d+)', permalink)
                if ts_match:
                    thread_ts = ts_match.group(1)
                else:
                    p_match = re.search(r'/p(\d{16})', permalink)
                    if p_match:
                        raw = p_match.group(1)
                        thread_ts = f"{raw[:10]}.{raw[10:]}"
                if not thread_ts:
                    continue
                key = (ch_id, thread_ts)
                if key not in threads_seen or float(my_ts) > float(threads_seen[key]):
                    threads_seen[key] = my_ts
            await asyncio.sleep(0.5)
    except Exception:
        pass

    if not threads_seen:
        return []

    print(f"  Checking {len(threads_seen)} threads for new replies...", file=sys.stderr)

    sem = asyncio.Semaphore(10)
    thread_unreads: list[dict] = []

    async def check_thread(ch_id: str, thread_ts: str, my_latest_ts: str):
        async with sem:
            try:
                resp = await client.get("/conversations.replies", params={
                    "channel": ch_id, "ts": thread_ts, "oldest": my_latest_ts, "limit": 10,
                })
                data = resp.json()
                if not data.get("ok"):
                    return
                new_replies = [
                    msg for msg in data.get("messages", [])
                    if msg.get("user") != MY_USER_ID and float(msg["ts"]) > float(my_latest_ts)
                ]
                if new_replies:
                    latest = new_replies[-1]
                    thread_unreads.append({
                        "channel_id": ch_id,
                        "thread_ts": thread_ts,
                        "new_reply_count": len(new_replies),
                        "latest_reply_text": latest.get("text", "")[:200],
                        "latest_reply_user": latest.get("user", ""),
                        "latest_reply_ts": latest.get("ts", ""),
                    })
            except Exception:
                pass

    tasks = [check_thread(ch_id, thread_ts, my_ts) for (ch_id, thread_ts), my_ts in threads_seen.items()]
    await asyncio.gather(*tasks)
    return thread_unreads


async def resolve_user(client: httpx.AsyncClient, user_id: str, cache: dict[str, str]) -> str:
    """Resolve a user ID to display name, with caching."""
    if user_id in cache:
        return cache[user_id]
    try:
        resp = await client.get("/users.info", params={"user": user_id})
        data = resp.json()
        if data.get("ok"):
            profile = data.get("user", {}).get("profile", {})
            name = profile.get("display_name") or profile.get("real_name") or user_id
            cache[user_id] = name
            return name
    except Exception:
        pass
    cache[user_id] = user_id
    return user_id


async def resolve_mpim_members(client: httpx.AsyncClient, channel_id: str, cache: dict[str, str]) -> str:
    """Get display names for group DM members (excluding self)."""
    try:
        resp = await client.get("/conversations.members", params={"channel": channel_id, "limit": 10})
        data = resp.json()
        if data.get("ok"):
            member_ids = [m for m in data.get("members", []) if m != MY_USER_ID][:4]
            names = [await resolve_user(client, mid, cache) for mid in member_ids]
            return ", ".join(names)
    except Exception:
        pass
    return ""


async def resolve_channel_name(client: httpx.AsyncClient, channel_id: str, cache: dict[str, str]) -> str:
    """Get channel name, with caching."""
    if channel_id in cache:
        return cache[channel_id]
    try:
        resp = await client.get("/conversations.info", params={"channel": channel_id})
        data = resp.json()
        if data.get("ok"):
            name = data["channel"].get("name", channel_id)
            cache[channel_id] = name
            return name
    except Exception:
        pass
    cache[channel_id] = channel_id
    return channel_id


async def process_workspace(client: httpx.AsyncClient, ws_name: str, ws_id: str) -> tuple[list, list]:
    """Find all unreads in a workspace: DMs/mentions, channels, and threads."""
    print(f"  Scanning {ws_name}...", file=sys.stderr)
    user_cache: dict[str, str] = {}
    channel_name_cache: dict[str, str] = {}

    # --- Source 1: DMs and mentions via search ---
    active_channels = await search_active_channels(client, ws_id)
    print(f"  Found {len(active_channels)} recently active channels via search", file=sys.stderr)

    # --- Source 2: Group DMs ---
    mpim_channels = await list_recent_mpim(client, ws_id, limit=200)
    print(f"  Found {len(mpim_channels)} group DMs to check", file=sys.stderr)

    search_channel_ids = active_channels | set(mpim_channels)

    # --- Source 3: Member channel unreads (hybrid: priority + recency) ---
    member_channels = await get_member_channels(client, ws_id)
    print(f"  Found {len(member_channels)} member channels", file=sys.stderr)

    member_only = [(ch["id"], ch.get("name", "")) for ch in member_channels
                   if ch["id"] not in search_channel_ids]

    priority_names = {n.lower() for n in PRIORITY_CHANNELS.get(ws_name, set())}
    recency_cutoff = datetime.now(timezone.utc) - timedelta(hours=CHANNEL_RECENCY_HOURS)
    recency_cutoff_ts = recency_cutoff.timestamp()

    # --- Run all checks concurrently ---
    sem = asyncio.Semaphore(15)
    search_tasks = [check_unread(client, cid, sem) for cid in search_channel_ids]
    channel_tasks = [
        check_channel_unread_with_recency(client, ch_id, ch_name, sem, priority_names, recency_cutoff_ts)
        for ch_id, ch_name in member_only
    ]

    search_results, channel_results, thread_unreads = await asyncio.gather(
        asyncio.gather(*search_tasks),
        asyncio.gather(*channel_tasks),
        find_thread_unreads(client, ws_id),
    )

    unreads = [r for r in search_results if r is not None]
    channel_unreads = [r for r in channel_results if r is not None]

    # Dedupe: skip channels already found by search
    existing_ids = {u["channel_id"] for u in unreads}
    for cu in channel_unreads:
        if cu["channel_id"] not in existing_ids:
            unreads.append(cu)
            existing_ids.add(cu["channel_id"])

    print(f"  Found {len(unreads)} conversations with unreads, "
          f"{len(thread_unreads)} threads with new replies in {ws_name}", file=sys.stderr)

    # --- Resolve display names ---
    for u in unreads:
        if u["is_im"] and u["user"]:
            u["display_name"] = await resolve_user(client, u["user"], user_cache)
        elif u["is_mpim"]:
            u["display_name"] = await resolve_mpim_members(client, u["channel_id"], user_cache)
        else:
            u["display_name"] = u["name"]
        if u.get("latest_user"):
            u["latest_user_name"] = await resolve_user(client, u["latest_user"], user_cache)
        u["workspace"] = ws_name

    for t in thread_unreads:
        if t.get("latest_reply_user"):
            t["latest_reply_user_name"] = await resolve_user(client, t["latest_reply_user"], user_cache)
        t["channel_name"] = await resolve_channel_name(client, t["channel_id"], channel_name_cache)
        t["workspace"] = ws_name

    return unreads, thread_unreads


async def main():
    token = get_token()
    workspaces = DEFAULT_WORKSPACES

    if len(sys.argv) > 1:
        requested = sys.argv[1:]
        workspaces = {k: v for k, v in workspaces.items() if k in requested}

    async with httpx.AsyncClient(
        base_url=SLACK_API_BASE,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30.0,
    ) as client:
        all_unreads = []
        all_thread_unreads = []
        for ws_name, ws_id in workspaces.items():
            unreads, thread_unreads = await process_workspace(client, ws_name, ws_id)
            all_unreads.extend(unreads)
            all_thread_unreads.extend(thread_unreads)

        # Sort: DMs first, then group DMs, then channels
        all_unreads.sort(key=lambda x: (
            2 if x.get("is_channel") else 0 if x.get("is_im") else 1,
            -x.get("unread_count", 0),
        ))

        # Sort thread unreads by latest reply time (newest first)
        all_thread_unreads.sort(key=lambda x: float(x.get("latest_reply_ts", "0")), reverse=True)

        output = {
            "ok": True,
            "total_unreads": sum(u.get("unread_count", 1) for u in all_unreads),
            "total_channels": len(all_unreads),
            "total_thread_unreads": len(all_thread_unreads),
            "unreads": all_unreads,
            "thread_unreads": all_thread_unreads,
        }
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
