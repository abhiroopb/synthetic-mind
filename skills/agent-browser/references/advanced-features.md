# Advanced Features

## Local Files (PDFs, HTML)

```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

## Timeouts and Slow Pages

Default Playwright timeout is 60 seconds. For slow pages, use explicit waits:

```bash
agent-browser wait --load networkidle     # Wait for network to settle (best for slow pages)
agent-browser wait "#content"             # Wait for specific element
agent-browser wait --url "**/dashboard"   # Wait after redirects
agent-browser wait --fn "document.readyState === 'complete'"
```

Use `wait --load networkidle` after `open` for consistently slow websites.

## Debugging

```bash
agent-browser open example.com --headed  # Show browser window
agent-browser highlight @e1              # Highlight element
agent-browser record start demo.webm     # Record session
agent-browser profiler start             # Start Chrome DevTools profiling
agent-browser profiler stop trace.json   # Stop and save profile
agent-browser console                    # View console messages
agent-browser errors                     # View page errors
```

## Configuration File

Create `agent-browser.json` in the project root for persistent settings:

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

Priority (lowest to highest): `~/.agent-browser/config.json` < `./agent-browser.json` < env vars < CLI flags. Use `--config <path>` or `AGENT_BROWSER_CONFIG` env var for a custom config path. All CLI options map to camelCase keys (e.g., `--executable-path` becomes `"executablePath"`).
