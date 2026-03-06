# Advanced Interactions

## Semantic Locators (locate + act in one call)

When refs are unavailable or unreliable:

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

## Tabs & Frames

```bash
agent-browser tab                     # List tabs
agent-browser tab new [url]           # New tab
agent-browser tab <n>                 # Switch to tab n
agent-browser tab close [n]
agent-browser frame <sel>             # Switch to iframe
agent-browser frame main              # Back to main frame
```

## Check State

```bash
agent-browser is visible @e1
agent-browser is enabled @e1
agent-browser is checked @e1
```

## Dialogs

```bash
agent-browser dialog accept [text]
agent-browser dialog dismiss
```

## Network Mocking

```bash
agent-browser network route <url> --abort       # Block requests
agent-browser network route <url> --body <json>  # Mock response
agent-browser network unroute [url]
agent-browser network requests --filter api     # View tracked requests
```

## Browser Settings

```bash
agent-browser set viewport 1280 720
agent-browser set device "iPhone 14"
agent-browser set geo <lat> <lng>
agent-browser set offline on
agent-browser set media dark
```
