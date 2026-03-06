# People API

> Query employee data from an internal directory — search by name, username, Slack ID, function, or org.

## What it does

The People API skill provides access to an organization's internal people directory. You can search for employees by name or username, look up full profiles, resolve Slack IDs to employee records, browse org charts, list direct reports with sub-team assignments, filter by function or org hierarchy, and find new hires since a given date. It supports pagination, photo URLs, and manager chain lookups.

## Usage

Use this skill when you need to find information about people in the organization. Works with VPN access; an API token is recommended for reliability.

**Trigger phrases:**
- "Who is johndoe?"
- "Find engineers in Web Engineering"
- "Who is the manager of jane?"
- "Look up this Slack user"
- "Who joined the team in the last month?"
- "Show me the org chart for this team"

## Examples

- `"Who is johndoe?"` — Fetches the full profile for the given username, including title, team, location, manager, and contact info.
- `"Find all engineers in Web Engineering with their managers"` — Searches by function hierarchy and includes lead details.
- `"Who joined since January 2026?"` — Uses the `since` parameter to find employees created or updated after the given date.

## Why it was created

Looking up people information — who's on what team, who manages whom, what's someone's Slack handle — is a frequent task that normally requires navigating a web directory. This skill brings the full people directory to the agent, enabling instant lookups and org exploration.
