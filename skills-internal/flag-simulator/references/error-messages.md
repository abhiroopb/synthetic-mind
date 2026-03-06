# Error Messages

When the status is not SUCCESS, display user-friendly messages:

| Status | Message |
|--------|---------|
| `SDK_ERROR` | SDK encountered an error while evaluating the flag. |
| `INVALID_REQUEST` | Invalid Merchant or Unit Token. |
| `NOT_FOUND` | Flag not found in project {project}. |
| `WRONG_TYPE` | Flag type mismatch. Load the `launchdarkly` skill to look up the correct flag type, then retry with the correct `--flag-type`. |
| `SERVICE_NOT_READY` | LaunchDarkly SDK is not ready. |
| `MISSING_USER_TOKEN` | User authentication token is missing. |
