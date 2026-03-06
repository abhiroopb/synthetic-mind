# Snowflake Skill Setup

Full installation instructions for all platforms are available at
https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation.

The steps below are for macOS. Run these commands directly — prompt the user only for:
- **Email** (their corporate email, e.g. `alice@yourcompany.com`)
- **Username** (default: the part of their email before `@`, uppercased)
- **Account** (default: your Snowflake account identifier, e.g. `YOUR_ORG-YOUR_ACCOUNT`)

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

Create `~/.snowflake/config.toml` using the user's email, username, and account values:

```toml
default_connection_name = "default"

[connections.default]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__MEDIUM"

[connections.small]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__SMALL"

[connections.large]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__LARGE"

[connections.xlarge]
account = "{ACCOUNT}"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__XLARGE"

# Staging connections (use your staging account identifier)
[connections.staging-medium]
account = "YOUR_STAGING_ACCOUNT"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__MEDIUM"

[connections.staging-small]
account = "YOUR_STAGING_ACCOUNT"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__SMALL"

[connections.staging-large]
account = "YOUR_STAGING_ACCOUNT"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__LARGE"

[connections.staging-xlarge]
account = "YOUR_STAGING_ACCOUNT"
user = "{EMAIL}"
authenticator = "externalbrowser"
role = "{USERNAME}"
warehouse = "ADHOC__XLARGE"
```

## 3. Verify connectivity

Run a test query (requires VPN). A browser window will open for SSO login on first use:

```bash
snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
```

Tokens are cached locally. If they expire, the browser opens automatically to re-authenticate.
