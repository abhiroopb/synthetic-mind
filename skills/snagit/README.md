# Snagit

> Capture screenshots and recordings using TechSmith Snagit on macOS with AppleScript automation.

## What it does

Snagit automates screen capture and recording workflows on macOS using TechSmith Snagit 2024. It can trigger various capture modes (fullscreen, window, region, video) via keyboard shortcuts through AppleScript, open captured images in the Snagit editor for annotation, and access the Snagit library. It also supports macOS's built-in `screencapture` CLI for scripted captures that can optionally be opened in Snagit for editing.

## Usage

Invoke when you need to take a screenshot, capture a specific window, record the screen, open Snagit's editor, or automate a capture-and-annotate workflow.

**Trigger phrases:**
- "Take a screenshot"
- "Capture this window"
- "Record the screen"
- "Open Snagit"
- "Take a fullscreen capture"

## Examples

- `"Take a screenshot of the current window"`
- `"Capture the full screen and open it in Snagit for annotation"`
- `"Record a video of my screen"`

## Why it was created

Screen captures are essential for documentation, bug reports, and demos, but triggering them programmatically on macOS requires navigating AppleScript and keyboard shortcuts. This skill packages those patterns so you can capture, annotate, and save screenshots without leaving your workflow.
