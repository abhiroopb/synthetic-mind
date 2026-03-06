# Mobile Releases

> Browse, download, and install mobile app builds from an internal releases portal.

## What it does

Mobile Releases queries an internal mobile releases portal to list available projects, versions, and builds. It can download APKs and IPAs, install builds to Android devices via `adb` or iOS simulators via `xcrun simctl`, and handle variant selection (Debug, Beta, Release, Dogfood, etc.). The skill walks you through the full workflow from finding a build to installing it on a device.

## Usage

Use this skill when you need to find, download, or install a specific mobile app build for testing or debugging.

**Trigger phrases:**
- "Find the latest build of the app"
- "Download the Android APK for version 6.45"
- "Install the iOS beta on the simulator"
- "What app versions are available?"
- "List all projects on the releases portal"

## Examples

- `"Show me the latest Android builds for the POS app"` — Lists available versions and variants (Debug, Beta, Release) with build numbers, download URLs, and git SHAs.
- `"Install the latest iOS beta on my simulator"` — Downloads the IPA, boots an available simulator, and installs the build.
- `"What projects are available on the releases portal?"` — Lists all projects with their supported platforms.

## Why it was created

Finding and installing specific mobile builds requires navigating a web portal, selecting the right variant, downloading manually, and running install commands. This skill streamlines the entire flow into a single conversational workflow.
