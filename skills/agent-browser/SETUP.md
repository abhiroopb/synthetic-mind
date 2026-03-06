# Setup

## CLI Installation (once per session)

```bash
npm install -g agent-browser@latest
agent-browser install
```

Installs the CLI globally and downloads Chromium. Subsequent commands run instantly via the Rust CLI + daemon architecture (no `npx` overhead).

If commands fail with "command not found", re-run the install above.

## iOS Simulator Setup (one-time)

Requires macOS with Xcode installed.

```bash
npm install -g appium
appium driver install xcuitest
```

List available simulators: `agent-browser device list`

**Real devices:** Use `--device "<UDID>"` where UDID is from `xcrun xctrace list devices`.
