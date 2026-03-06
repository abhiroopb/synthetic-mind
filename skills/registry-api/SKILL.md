---
Skill name: registry-api
Skill description: Query a service registry API using a Python client library. Use when you need to look up applications, users, groups, roles, infrastructure, dependencies, or ownership information from the service registry with full API access.
allowed-tools:
  - Bash(uv run --with registry python:*)
  - AskUserQuestion
---

# Service Registry API Skill

Query the service registry API using a Python client library. This provides direct access to all registry API v2 endpoints including applications, users, groups, roles, and infrastructure.

## Setup

Run all scripts using `uv run --with registry`, which automatically provides the `registry` package and all its dependencies in a cached environment. No manual install needed.

```bash
uv run --with registry python script.py
```

Use the `Client` class (no auth needed for most read endpoints):

```python
from registry import Client
client = Client(base_url="https://registry.example.com/api/v2")
```

## Available API Endpoints

Use the `sync()` function from each endpoint module. All return parsed model objects or `None`.

### Core lookups
- **Applications**: `from registry.api.applications import get_applications` — filter by `slug`, `q` (search), `id`, `infra_type`, `reliability_tier`, `team_id`, `git_repo`, `page`, `page_size`
- **Application by ID**: `from registry.api.applications import get_applications_id` — takes `id` (int)
- **Application groups**: `from registry.api.applications import get_applications_id_groups`
- **Application owners**: `from registry.api.applications import get_applications_id_owners_group`
- **Application infras**: `from registry.api.applications import get_applications_id_infras`
- **Application dependencies**: `from registry.api.applications import get_applications_id_dependencies`
- **Application dependent apps**: `from registry.api.applications import get_applications_id_dependent_apps`
- **Application integrations**: `from registry.api.applications import get_applications_id_integrations`

### Users
- **List/search users**: `from registry.api.users import get_users` — filter by `uid`, `username`, `email`, `employee_id`, `state`, `type_`, `page`, `page_size`
- **Search users**: `from registry.api.users import get_users_search` — takes `query` (str, required), `state`, `type_`
- **User by ID**: `from registry.api.users import get_users_id`
- **User groups**: `from registry.api.users import get_users_id_groups`
- **User roles**: `from registry.api.users import get_users_id_roles`
- **Current user**: `from registry.api.me import get_me`

### Groups
- **List groups**: `from registry.api.groups import get_groups` — filter by `groupname`, `type_`, `tag`, `view`, `page`, `page_size`
- **Group by ID**: `from registry.api.groups import get_groups_id`
- **Group users**: `from registry.api.groups import get_groups_id_users`
- **Group roles**: `from registry.api.groups import get_groups_id_roles`
- **Group grants**: `from registry.api.groups import get_groups_id_grants`

### Roles
- **List roles**: `from registry.api.roles import get_roles`
- **Role by ID**: `from registry.api.roles import get_roles_id`
- **Role users**: `from registry.api.roles import get_roles_id_users`
- **Role groups**: `from registry.api.roles import get_roles_id_groups`

### Infrastructure
- **AWS accounts**: `from registry.api.aws_accounts import get_aws_accounts`
- **AWS resources**: `from registry.api.aws_resources import get_aws_resources`
- **Cost centers**: `from registry.api.cost_centers import get_cost_centers`
- **Zones**: `from registry.api.zones import get_zones`
- **Ports**: `from registry.api.ports import get_ports`

### Health
- **API status**: `from registry.api.health import get_status`

## Example script pattern

```python
import json
from registry import Client
from registry.api.applications import get_applications

client = Client(base_url="https://registry.example.com/api/v2")
with client as c:
    results = get_applications.sync(client=c, q="my-app")
    if results:
        for app in results:
            print(f"{app.slug} (id={app.id}) - {app.tagline}")
            print(f"  repo: {app.git_repo}")
            print(f"  contact: {app.contact}")
    else:
        print("No results found")
```

## Instructions

1. Write a short Python script that answers the user's question using the appropriate endpoint(s).
2. **Show the script to the user** before executing it so they can review what will be queried.
3. Run it with: `uv run --with registry python <script>`
4. Present the results in a clear, readable format.
5. If the first query doesn't find what the user needs, try alternate search strategies.
6. Clean up any temporary scripts after use.
7. Models use `attrs` — access fields as attributes (e.g., `app.slug`, `user.username`). To inspect all fields, use `attrs.asdict(obj)`.
8. **Model ID fields vary by type**: Applications use `app.id`, Users use `user.uid`, Groups use `group.gid`.
9. **Sensitive data guardrail**: Before querying user PII (emails, employee IDs) or infrastructure endpoints, confirm with the user using `AskUserQuestion` that they need this data.

## Related Skills

- **registry-info**: Query the service registry using a simpler CLI (fewer endpoints)
