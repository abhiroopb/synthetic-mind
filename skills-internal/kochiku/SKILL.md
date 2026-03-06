---
name: kochiku
description: "Fetch raw CI build data, logs, and artifacts via a CI system JSON API. Use when fetching, downloading, inspecting, or viewing CI build parts, build attempts, artifact logs, or stdout/stderr output. Not for failure analysis — use check-ci for that."
roles: [frontend]
allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
  - Bash(gunzip:*)
  - Bash(zcat:*)
metadata:
  status: stable
---

# CI Build Data Fetcher

Interact with CI builds via the CI system's JSON API.

For **analyzed build failures** with root causes and test results, use the `check-ci` skill instead. Use this skill when you need raw build data, log content, or manual inspection.

## API Endpoints

### Get Build Info

```bash
curl -s 'https://ci.example.com/org/{repository}/builds/{buildId}?format=json'
```

Key response fields:
- `build.state` — `running`, `succeeded`, `failed`, `doomed`, `errored`, `aborted`
- `build.ref` — git commit SHA
- `build.branch_record.name` — branch name
- `build.build_parts[]` — array with `id`, `status`, `kind`, `paths`

### Get Build Part (with attempts and artifacts)

```bash
curl -s 'https://ci.example.com/org/{repository}/builds/{buildId}/parts/{partId}?format=json'
```

Returns `build_part.build_attempts[]`, each containing:
- `state` — `passed`, `failed`, `errored`, etc.
- `files[]` — artifacts with `build_artifact.log_file.url` and `build_artifact.log_file.name`

### Fetch Artifact Content

Artifact `log_file.url` values are paths like `/build_artifacts/{id}`. Prepend the base URL and follow redirects (`-L`) since they redirect to cloud storage:

```bash
curl -s -L 'https://ci.example.com/build_artifacts/{artifactId}' | gunzip -c
```

Common artifact names: `stdout.log.gz` (main output), `stderr.log.gz` (error output).

## Workflow: Fetching Logs for a Failed Build

1. **Find failed parts:**
   ```bash
   curl -s 'https://ci.example.com/org/{repository}/builds/{buildId}?format=json' \
     | jq '.build.build_parts[] | select(.status == "failed") | {id, kind, status}'
   ```

2. **Get the latest attempt's artifacts:**
   ```bash
   curl -s 'https://ci.example.com/org/{repository}/builds/{buildId}/parts/{partId}?format=json' \
     | jq '.build_part.build_attempts[-1].files[] | .build_artifact.log_file | {name, url}'
   ```

3. **Download the stdout log:**
   ```bash
   curl -s -L 'https://ci.example.com{url_from_step_2}' | gunzip -c
   ```

## Resolving a Commit SHA to a Build

```bash
curl -sI 'https://ci.example.com/builds/{commitSHA}'
```

Parse the `Location` header to extract the repository and build ID from the redirect URL.

## Extracting Build IDs from URLs

| URL Pattern | Extract |
|---|---|
| `ci.example.com/org/java/builds/12345` | repository=`java`, buildId=`12345` |
| `ci.example.com/org/java/builds/12345/parts/67890` | partId=`67890` |
| `console.example.com/ci-results/12345` | buildId=`12345` (need repository separately) |

## Related Skills

- `check-ci` — analyzed build failures via CI results API (start here for failure triage)
- `buildkite` — Buildkite CI via the `bk` CLI
