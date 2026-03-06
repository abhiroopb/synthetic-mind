#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.27.0"]
# ///
"""Fetch Slack saved items (stars) and active reminders."""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

import httpx

SLACK_API_BASE = "https://slack.com/api/"
TEAM_ID = "T05HJ0CKWG5"


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


async def main():
    token = get_token()
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    async with httpx.AsyncClient(
        base_url=SLACK_API_BASE,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30.0,
    ) as client:
        # Fetch stars (saved items)
        stars_resp = await client.get("stars.list", params={"limit": limit, "team_id": TEAM_ID})
        stars_data = stars_resp.json()

        saved_items = []
        if stars_data.get("ok"):
            for item in stars_data.get("items", []):
                if item.get("type") == "message":
                    msg = item.get("message", {})
                    saved_items.append({
                        "type": "saved",
                        "channel_id": item.get("channel", ""),
                        "message_ts": msg.get("ts", ""),
                        "text": msg.get("text", "")[:200],
                        "user": msg.get("user", ""),
                        "user_name": msg.get("user_profile", {}).get("real_name", "") if msg.get("user_profile") else "",
                        "date_created": item.get("date_create", 0),
                    })

        # Fetch reminders
        rem_resp = await client.get("reminders.list", params={"team_id": TEAM_ID})
        rem_data = rem_resp.json()

        reminders = []
        now = datetime.now().timestamp()
        if rem_data.get("ok"):
            for r in rem_data.get("reminders", []):
                # Skip completed reminders
                if r.get("complete_ts", 0) > 0:
                    continue
                remind_time = r.get("time", 0)
                is_overdue = remind_time < now if remind_time > 0 else False
                reminders.append({
                    "type": "reminder",
                    "id": r.get("id", ""),
                    "text": r.get("text", "")[:200],
                    "time": remind_time,
                    "is_overdue": is_overdue,
                    "recurring": r.get("recurring", False),
                    "channel_id": r.get("item", {}).get("channel", "") if r.get("item") else "",
                    "message_ts": r.get("item", {}).get("message_ts", "") if r.get("item") else "",
                })

        output = {
            "ok": True,
            "saved_count": len(saved_items),
            "reminder_count": len(reminders),
            "saved_items": saved_items,
            "reminders": reminders,
        }
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
