---
name: controlling-computer
description: "Control this Mac via AppleScript and shell commands. Open/quit/switch apps, manage windows, adjust volume/brightness, toggle dark mode, lock screen, send notifications, read clipboard, query system info. Use when asked to control the computer, manage windows, change settings, or automate macOS actions."
---

# Controlling Computer

Control macOS via `osascript` (AppleScript/JXA) and shell commands. Always confirm before destructive actions (restart, shutdown, force-quit).

## Capabilities

### App Management
```bash
# Open an app
open -a "App Name"

# Quit an app gracefully
osascript -e 'tell application "App Name" to quit'

# Force-quit (confirm first)
osascript -e 'tell application "App Name" to quit saving no'

# Activate / bring to front
osascript -e 'tell application "App Name" to activate'

# List running apps
osascript -e 'tell application "System Events" to get name of every process whose background only is false'
```

### Window Management
```bash
# Get frontmost app and window info
osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'

# Resize window (app, x, y, width, height)
osascript -e 'tell application "System Events" to tell process "App Name" to set position of window 1 to {0, 25}' 
osascript -e 'tell application "System Events" to tell process "App Name" to set size of window 1 to {960, 1050}'

# Minimize window
osascript -e 'tell application "System Events" to tell process "App Name" to set value of attribute "AXMinimized" of window 1 to true'

# Fullscreen toggle
osascript -e 'tell application "System Events" to tell process "App Name" to set value of attribute "AXFullScreen" of window 1 to true'

# Tile two apps side-by-side (left half / right half on 1920-wide display)
# Left:
osascript -e 'tell application "System Events" to tell process "App1" to set position of window 1 to {0, 25}' -e 'tell application "System Events" to tell process "App1" to set size of window 1 to {960, 1050}'
# Right:
osascript -e 'tell application "System Events" to tell process "App2" to set position of window 1 to {960, 25}' -e 'tell application "System Events" to tell process "App2" to set size of window 1 to {960, 1050}'
```

To get screen dimensions for accurate tiling:
```bash
system_profiler SPDisplaysDataType | grep Resolution
```

### Volume & Audio
```bash
# Get current volume (0-100)
osascript -e 'output volume of (get volume settings)'

# Set volume (0-100)
osascript -e 'set volume output volume 50'

# Mute / unmute
osascript -e 'set volume output muted true'
osascript -e 'set volume output muted false'

# Toggle mute
osascript -e 'set volume output muted (not (output muted of (get volume settings)))'

# Get input volume
osascript -e 'input volume of (get volume settings)'
```

### Brightness
```bash
# Get brightness (requires brightness CLI: brew install brightness)
brightness -l

# Set brightness (0.0 to 1.0)
brightness 0.7
```

### Dark Mode
```bash
# Check current mode
osascript -e 'tell application "System Events" to tell appearance preferences to get dark mode'

# Toggle dark mode
osascript -e 'tell application "System Events" to tell appearance preferences to set dark mode to not dark mode'

# Set explicitly
osascript -e 'tell application "System Events" to tell appearance preferences to set dark mode to true'
```

### Do Not Disturb
```bash
# Check DND (macOS Sonoma+)
defaults read com.apple.controlcenter "NSStatusItem Visible FocusModes" 2>/dev/null

# Toggle Focus/DND via shortcuts (requires Shortcuts app setup)
shortcuts run "Toggle Do Not Disturb" 2>/dev/null || echo "Set up a Shortcut named 'Toggle Do Not Disturb' first"
```

### Notifications
```bash
# Send a notification
osascript -e 'display notification "Body text" with title "Title" subtitle "Subtitle" sound name "Glass"'
```

### Clipboard
```bash
# Read clipboard
pbpaste

# Write to clipboard
echo "text" | pbcopy

# Copy file path to clipboard
echo "/path/to/file" | pbcopy
```

### System Info
```bash
# Battery
pmset -g batt

# Uptime
uptime

# Disk space
df -h /

# Wi-Fi network name
networksetup -getairportnetwork en0 2>/dev/null || ipconfig getifaddr en0

# IP addresses
ifconfig | grep "inet " | grep -v 127.0.0.1

# macOS version
sw_vers

# CPU / memory
sysctl -n machdep.cpu.brand_string
sysctl -n hw.memsize | awk '{print $1/1073741824 " GB"}'

# Top processes by CPU
ps aux --sort=-%cpu | head -11

# Top processes by memory
ps aux --sort=-%mem | head -11
```

### Finder & Files
```bash
# Open folder in Finder
open /path/to/folder

# Reveal file in Finder
open -R /path/to/file

# Get selected Finder files
osascript -e 'tell application "Finder" to get POSIX path of (selection as alias list)'

# Eject a volume (confirm first)
diskutil eject /Volumes/DiskName

# Trash a file
osascript -e 'tell application "Finder" to delete POSIX file "/path/to/file"'
```

### Screenshots
```bash
# Full screen to file
screencapture ~/Desktop/screenshot.png

# Interactive region selection
screencapture -i ~/Desktop/screenshot.png

# Specific window (click to select)
screencapture -iW ~/Desktop/screenshot.png

# Clipboard only
screencapture -c
```

### System Actions (ALWAYS confirm before executing)
```bash
# Lock screen
osascript -e 'tell application "System Events" to keystroke "q" using {control down, command down}'
# or:
pmset displaysleepnow

# Sleep
osascript -e 'tell application "System Events" to sleep'

# Restart (CONFIRM FIRST)
osascript -e 'tell application "System Events" to restart'

# Shutdown (CONFIRM FIRST)
osascript -e 'tell application "System Events" to shut down'

# Log out (CONFIRM FIRST)
osascript -e 'tell application "System Events" to log out'
```

### Keyboard & Mouse Simulation
```bash
# Type text
osascript -e 'tell application "System Events" to keystroke "hello"'

# Press a key combo (e.g., Cmd+Space for Spotlight)
osascript -e 'tell application "System Events" to keystroke space using command down'

# Press Enter
osascript -e 'tell application "System Events" to key code 36'

# Press Escape
osascript -e 'tell application "System Events" to key code 53'
```

### Wi-Fi
```bash
# Turn Wi-Fi off/on
networksetup -setairportpower en0 off
networksetup -setairportpower en0 on

# Current Wi-Fi network
networksetup -getairportnetwork en0
```

### Bluetooth
```bash
# Toggle Bluetooth (requires blueutil: brew install blueutil)
blueutil --power 0  # off
blueutil --power 1  # on
blueutil --power    # status
```

## Safety Rules

1. **Always confirm** before: restart, shutdown, log out, force-quit, eject, trash/delete
2. **Never** execute `rm -rf` or destructive file operations without explicit approval
3. **Prefer graceful** quit over force-quit
4. **Show current state** before changing settings (e.g., show volume before changing it)

## Tips

- Chain multiple `osascript -e` statements for multi-step automation
- Use `open -a` for launching apps (handles .app bundles automatically)
- For complex AppleScript, use heredoc: `osascript <<'EOF' ... EOF`
- Check if a CLI tool exists before using it: `command -v brightness &>/dev/null`
- Get screen resolution first when doing window management: `system_profiler SPDisplaysDataType | grep Resolution`
