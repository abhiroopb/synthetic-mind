---
name: snagit
description: "Capture screenshots and recordings using TechSmith Snagit on macOS. Use when asked to take a screenshot, capture a window, record the screen, open Snagit, access Snagit library, or automate screen capture workflows."
---

# Snagit — Screen Capture & Recording Automation

Automate TechSmith Snagit 2024 on macOS for screenshots, recordings, and library access.

## Default Save Location

All screenshots should be saved to `~/Documents/screenshots/` (not Desktop).
Use filename format: `capture_YYYYMMDD_HHMMSS.png`

## Prerequisites

- Snagit 2024 installed at `/Applications/Snagit 2024.app`
- Bundle ID: `com.TechSmith.Snagit2024`
- Screen Recording permission granted in System Settings → Privacy & Security
- Accessibility permission may be needed for System Events automation

## Capabilities

### 1. Launch & Control Snagit

```bash
# Open Snagit (launches or activates)
open -a "Snagit 2024"

# Open Snagit Editor
osascript -e 'tell application "Snagit 2024" to activate'
```

### 2. Take Screenshots via Keyboard Shortcuts

Use AppleScript + System Events to trigger Snagit's capture hotkeys:

```bash
# Trigger global capture (Control+Shift+C) — opens Snagit crosshair
osascript -e '
tell application "Snagit 2024" to activate
delay 0.5
tell application "System Events"
    keystroke "c" using {control down, shift down}
end tell'

# Image capture (Control+Shift+S)
osascript -e '
tell application "Snagit 2024" to activate
delay 0.5
tell application "System Events"
    keystroke "s" using {control down, shift down}
end tell'

# Window capture (Control+Shift+W)
osascript -e '
tell application "Snagit 2024" to activate
delay 0.5
tell application "System Events"
    keystroke "w" using {control down, shift down}
end tell'

# Video capture (Control+Shift+V)
osascript -e '
tell application "Snagit 2024" to activate
delay 0.5
tell application "System Events"
    keystroke "v" using {control down, shift down}
end tell'

# Fullscreen capture — trigger capture then press F
osascript -e '
tell application "Snagit 2024" to activate
delay 0.5
tell application "System Events"
    keystroke "c" using {control down, shift down}
    delay 0.3
    keystroke "f"
end tell'
```

### 3. macOS Built-in Screenshot (Complement)

When Snagit's interactive mode isn't needed, use macOS `screencapture` for scripted captures:

```bash
# Capture fullscreen to file
screencapture ~/Desktop/screenshot.png

# Capture fullscreen to clipboard
screencapture -c

# Capture with mouse selection (interactive)
screencapture -i ~/Desktop/screenshot.png

# Capture specific window (interactive click)
screencapture -iw ~/Desktop/window.png

# Capture without shadow
screencapture -o ~/Desktop/screenshot.png

# Capture after delay (seconds)
screencapture -T 3 ~/Desktop/screenshot.png

# Open result in Snagit for editing
screencapture ~/Desktop/screenshot.png && open -a "Snagit 2024" ~/Desktop/screenshot.png
```

### 4. Open Snagit Editor & Library

```bash
# Open Editor
osascript -e '
tell application "Snagit 2024" to activate
delay 0.3
tell application "System Events"
    keystroke "e" using {command down, shift down}
end tell'

# Switch to Library view
osascript -e '
tell application "Snagit 2024" to activate
delay 0.3
tell application "System Events"
    keystroke "1" using {command down}
end tell'
```

### 5. Open a File in Snagit Editor

```bash
# Open an existing image in Snagit for annotation
open -a "Snagit 2024" /path/to/image.png
```

### 6. Capture & Save Workflow

For automated capture-and-save workflows, use `screencapture` then open in Snagit:

```bash
# 1. Capture to temp file
CAPTURE_FILE="$HOME/Desktop/capture_$(date +%Y%m%d_%H%M%S).png"
screencapture -i "$CAPTURE_FILE"

# 2. Open in Snagit for editing/annotation
open -a "Snagit 2024" "$CAPTURE_FILE"
```

### 7. Access Snagit Data Locations

| Location | Path |
|---|---|
| App Data | `~/Library/Group Containers/7TQL462TU8.com.techsmith.snagit/Snagit 2024/` |
| Preferences | `defaults read com.TechSmith.Snagit2024` |
| Stamps | `~/Library/Group Containers/7TQL462TU8.com.techsmith.snagit/Snagit 2024/Stamps/` |
| Share History | `~/Library/Group Containers/7TQL462TU8.com.techsmith.snagit/Snagit 2024/ShareHistoryArchivedItems/` |

## Keyboard Shortcuts Reference

### Capture
| Action | Shortcut |
|---|---|
| Global Capture | Control+Shift+C |
| Image Capture | Control+Shift+S |
| Window Capture | Control+Shift+W |
| Video Capture | Control+Shift+V |
| Fullscreen (during capture) | F |
| Scroll Horizontally | R |
| Scroll Vertically | D |
| Cancel Capture | Esc |
| Start/Pause Recording | Control+Shift+Space |
| Stop Recording | Control+Shift+V |

### Editor
| Action | Shortcut |
|---|---|
| Open Editor | Command+Shift+E |
| Library View | Command+1 |
| Save | Command+S |
| Save As | Shift+Command+S |
| Copy All | Option+Command+C |
| Grab Text (OCR) | Shift+Command+O |
| Trim | Shift+Command+X |
| Resize Image | Shift+Command+R |

### Tools
| Tool | Shortcut |
|---|---|
| Arrow/Line | Control+A |
| Text | Control+T |
| Callout | Control+D |
| Shape | Control+U |
| Blur | Control+B |
| Step Numbers | Control+S |
| Highlighter | Control+H |
| Crop | Control+C |
| Pen | Control+P |

## Workflow Patterns

### Pattern A: Quick Screenshot for Documentation
1. Run `screencapture -i ~/Desktop/screenshot.png`
2. Open in Snagit: `open -a "Snagit 2024" ~/Desktop/screenshot.png`
3. User annotates in Snagit Editor
4. Save/share from Snagit

### Pattern B: Trigger Snagit's Native Capture
1. Activate Snagit and trigger capture hotkey via AppleScript
2. User interacts with Snagit's capture UI (select region, scroll capture, etc.)
3. Snagit opens result in Editor automatically

### Pattern C: Batch Capture Multiple Windows
```bash
# Capture multiple windows to Desktop
for i in 1 2 3; do
    screencapture -iw "$HOME/Desktop/window_$i.png"
done
# Open all in Snagit
open -a "Snagit 2024" ~/Desktop/window_*.png
```

## Notes

- Snagit does NOT have a native AppleScript scripting dictionary (.sdef) — automation is via System Events keyboard shortcuts and macOS `screencapture` CLI
- System Events automation requires Accessibility permission for the terminal/Amp process
- URL schemes available: `techsmithsnagit://`, `en-techsmith-snagit://`, `com.techsmith.snagit2024://`
- Snagit's scrolling capture, OCR, and annotation features are only available through its native UI
