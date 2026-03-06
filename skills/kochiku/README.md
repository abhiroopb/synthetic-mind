# Kochiku

> Fetch raw CI build data, logs, and artifacts from a CI system's JSON API.

## What it does

Kochiku provides direct access to CI build information via a JSON API. It can retrieve build status, list build parts, download artifact logs (stdout/stderr), and resolve commit SHAs to builds. This is the raw data layer — for analyzed build failures with root causes, use the `check-ci` skill instead.

## Usage

Use this skill when you need to manually inspect CI build data, download log files, or debug build issues at the raw artifact level.

**Trigger phrases:**
- "Fetch the logs for build 12345"
- "Show me the failed parts of this CI build"
- "Download the stdout log for this build attempt"
- "What's the build status for this commit?"

## Examples

- `"Show me the failed parts of build 12345 in the java repo"` — Queries the build API and filters for failed parts, showing their IDs and kinds.
- `"Download the stdout log for part 67890"` — Fetches the latest attempt's artifacts and downloads the compressed log.
- `"What build does commit abc123 belong to?"` — Resolves the commit SHA to a build ID via the redirect endpoint.

## Why it was created

When CI builds fail, you often need to dig into the raw logs beyond what automated analysis provides. This skill gives direct API access to build data, artifacts, and logs without needing to navigate a web UI.
