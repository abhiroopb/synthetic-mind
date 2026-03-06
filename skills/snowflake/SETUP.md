# Snowflake Skill Setup

Full installation instructions for all platforms are available at
https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation.

The steps below are for macOS. Run these commands directly — prompt the user only for:
- **Email** (their Square email, e.g. `alice@squareup.com`)
- **LDAP** (default: the part of their email before `@`, uppercased)
- **Account** (default: `SQUAREINC-SQUARE` for production, `SQUAREINC-SQUARESTAGING` for staging)

## 1. Install the Snowflake CLI

```bash
brew tap snowflakedb/snowflake-cli
brew update
brew install snowflake-cli
```

Verify the installation:

```bash
snow --version
```

## 2. Configure connections

Create `~/.snowflake/config.toml` using the user's email, LDAP, and account values:

```toml
default_connection_name = "default"

[connections.default]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__MEDIUM"

[connections.small]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__SMALL"

[connections.large]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__LARGE"

[connections.xlarge]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__XLARGE"

# Staging connections (account: SQUAREINC-SQUARESTAGING)
[connections.staging-medium]
account = "SQUAREINC-SQUARESTAGING"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__MEDIUM"

[connections.staging-small]
account = "SQUAREINC-SQUARESTAGING"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__SMALL"

[connections.staging-large]
account = "SQUAREINC-SQUARESTAGING"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__LARGE"

[connections.staging-xlarge]
account = "SQUAREINC-SQUARESTAGING"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{LDAP}"
warehouse = "ADHOC__XLARGE"
```

## 3. Verify connectivity

Run a test query (requires VPN). A browser window will open for Okta SSO login on first use:

```bash
snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
```

Tokens are cached locally. If they expire, the browser opens automatically to re-authenticate.
