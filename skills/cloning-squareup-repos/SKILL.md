---
name: cloning-repos
description: Clone organization repositories using the correct SSH remote. Use when cloning, downloading, fetching, pulling, checking out, or setting up any organization GitHub repository.
---

# Cloning Organization Repos

When cloning a repository from your organization, always use the correct SSH remote format configured for your org.

## SSH Remote Format

Use the organization-specific SSH remote:

```
<org-ssh-alias>@github.com:<org-name>/<repo-name>.git
```

Example:

```bash
git clone <org-ssh-alias>@github.com:<org-name>/web.git
```

**Why?** Many organizations configure custom SSH aliases for GitHub access (e.g., for SSO, deploy keys, or multi-account setups). Using the standard `git@github.com` remote may fail authentication. Check your `~/.ssh/config` or organization docs for the correct alias.

## Customization

Replace the placeholder values with your organization's setup:
- `<org-ssh-alias>` — your org's SSH alias (e.g., `org-12345`)
- `<org-name>` — your GitHub organization name
