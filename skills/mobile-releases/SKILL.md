---
name: mobile-releases
description: Browse, download, and install mobile app builds from an internal mobile releases portal. Use when the user wants to find app versions, list available builds, download APKs or IPAs, or install builds to Android devices or iOS simulators.
roles: [android, ios]
allowed-tools:
  - Bash(python3 scripts/mr.py:*)
  - Bash(adb install:*)
  - Bash(adb devices:*)
  - Bash(xcrun simctl:*)
  - AskUserQuestion
metadata:
  version: "1.0"
  status: experimental
---

# Mobile Releases

Browse, download, and install builds from the internal mobile releases portal.

The `mr.py` script queries the mobile releases portal via its JSON API and returns structured output. All commands print JSON to stdout and errors to stderr. Input validation (app IDs, platforms, versions) is enforced in the script.

## Querying Data

The script is at `scripts/mr.py` relative to this skill directory. Always use `python3` to run it.

### List all projects

```bash
python3 scripts/mr.py list-projects
```

Returns an array of `{"id", "name", "platforms"}` for every project on the portal. Use this when the user asks what apps are available or you need to look up an app's ID.

### List versions for a project

```bash
python3 scripts/mr.py list-versions <app-id> <platform>
```

Example: `python3 scripts/mr.py list-versions myapp android`

Returns the project's variants (build types) and all available versions, newest first.

### List builds for a specific version

```bash
python3 scripts/mr.py list-builds <app-id> <platform> <version>
```

Returns per-build details: variant name, build number, download URL, git SHA, timestamp, size in MB, download count, CI link, and notes. For iOS builds, an `ipa_url` field provides the direct IPA download link.

### Download an artifact

```bash
python3 scripts/mr.py download <url> --output <path>
```

Downloads the artifact. If `--output` is omitted, saves to `/tmp/mobile-releases/<filename>`. Use the `download_url` from `list-builds` output for Android APKs/AABs, and `ipa_url` for iOS IPAs.

## Installing Builds

### Android (adb)

1. Verify a device is connected:
   ```bash
   adb devices
   ```

2. Download the APK (use `download_url` from `list-builds` — must be a `.apk`, not `.aab`):
   ```bash
   python3 scripts/mr.py download <apk-url> --output /tmp/mobile-releases/app.apk
   ```

3. Install:
   ```bash
   adb install -r /tmp/mobile-releases/app.apk
   ```
   Use `-r` to replace an existing installation. Use `-d` to allow version downgrade if needed.

**Note:** `.aab` (Android App Bundle) files cannot be installed directly via `adb`. Only `.apk` variants (typically Debug, Beta, Release) can be installed. If the user wants a bundle variant, inform them it needs to be processed through `bundletool` first.

### iOS Simulator (xcrun simctl)

1. List available simulators:
   ```bash
   xcrun simctl list devices available
   ```

2. Boot a simulator if needed:
   ```bash
   xcrun simctl boot <UDID>
   ```

3. Download the IPA (use `ipa_url` from `list-builds`):
   ```bash
   python3 scripts/mr.py download <ipa-url> --output /tmp/mobile-releases/app.ipa
   ```

4. Install:
   ```bash
   xcrun simctl install <UDID> /tmp/mobile-releases/app.ipa
   ```

5. Launch (optional):
   ```bash
   xcrun simctl launch <UDID> <bundle-id>
   ```

## Typical Workflow

1. **User asks for a build** — identify the app ID and platform
2. **List versions** — show the user recent versions and variants
3. **List builds** — show builds for the chosen version
4. **Ask the user** which variant they want (e.g., Internal Debug vs Production for Android, Dogfood vs Experimental vs AppStore for iOS)
5. **Download** the artifact
6. **Install** if the user wants it on a device/simulator

## Archived Builds

Older builds may be archived to cloud storage. These have `"archived": true` in the `list-builds` output. Archived builds cannot be downloaded directly — they require a restoration request that takes ~12 hours. If a user requests an archived build, inform them and suggest using a newer version.
