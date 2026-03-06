---
name: mobile-cli
description: |
  Use the mobile CLI for common iOS & Android developer tasks. Use when building,
  testing, linting, running, or managing modules in mobile app repositories.
  Auto-detects platform and shows relevant commands.
roles: [mobile, android, ios]
argument-hint: <command> [args...] (e.g., build, test, lint, run, module, login)
allowed-tools: Bash(mobile:*), Bash(mobile), AskUserQuestion
metadata:
  author: anonymous
  status: experimental
  version: "0.4.0"
---

# Mobile CLI

The mobile CLI is the unified command-line interface for iOS & Android developer tasks.

## Direct Command Execution

When the user invokes `/mobile <command> [args...]`, execute the command directly if it matches a known command pattern.

### Known Commands (execute directly)

These commands can be run immediately when invoked with `/mobile`:

| Command Pattern | Action |
|-----------------|--------|
| `build [targets...] [flags]` | Run `mobile build [targets...] [flags]` |
| `test [targets...] [flags]` | Run `mobile test [targets...] [flags]` |
| `lint [flags]` | Run `mobile lint [flags]` |
| `run [target] [flags]` | Run `mobile run [target] [flags]` |
| `module <subcommand> [args]` | Run `mobile module <subcommand> [args]` |
| `proto update` | Run `mobile proto update` |
| `login [flags]` | Run `mobile login [flags]` (see special handling below) |
| `--help` or `-h` | Run `mobile --help` |
| `<command> --help` | Run `mobile <command> --help` |
| `update` | Run `mobile update` |

### Special Argument Handling

**Login command**: Map bare arguments to flags:
- `/mobile login user@example.com` → `mobile login --email=user@example.com`
- `/mobile login +15551234567` → `mobile login --phone-number=+15551234567`
- `/mobile login --email=...` → pass through as-is

### Execution Flow

1. **Parse the command**: Extract the command and arguments from `/mobile <input>`
2. **Match known pattern**: If the command matches a known pattern above, execute it directly
3. **Unknown command**: If not recognized, do NOT execute directly. Instead, follow the "Handling Unknown Command Formats" section below
4. **Report results**: Show the command output to the user

### Examples

```
/mobile build UIKit                    → mobile build UIKit
/mobile test --dirty                    → mobile test --dirty
/mobile lint --tidy                     → mobile lint --tidy
/mobile run --device="iPhone 15 Pro"    → mobile run --device="iPhone 15 Pro"
/mobile module create MyModule          → mobile module create MyModule
/mobile login test@example.com          → mobile login --email=test@example.com
/mobile --help                          → mobile --help
/mobile sim --help                      → mobile sim --help
```

---

## Platform Detection

Detect which repository you're in:

!`if [[ -f "Tools/MobileCLI/BUILD.bazel" ]]; then echo "ios"; elif [[ -f "mobile-android-cli/build.gradle.kts" ]]; then echo "android"; else echo "unknown"; fi`

- **iOS** (`app-ios`): Uses Bazel, CLI at `Tools/MobileCLI/`
- **Android** (`app-android`): Uses Gradle, CLI at `mobile-android-cli/`
- **Unknown**: Not in a mobile app repository. Install the CLI first (see Prerequisites).

## Prerequisites

Install the mobile CLI:

```bash
curl -fsSL "https://<artifact-server>/mobile-cli/install.sh" | bash
```

## Command Discovery

When the user asks about a command not documented below, run the help command to discover it:

```bash
# List ALL available commands for this platform
mobile --help

# Get detailed help for a specific command
mobile <command> --help
```

Always run `mobile --help` first if you're unsure what commands are available.

## Handling Unknown Command Formats

When a user provides a command in an unfamiliar or incorrect format:

1. **Discover the correct syntax**: Run `mobile <command> --help` to see available flags and arguments
2. **Map user intent to correct flags**: If the user provides a positional argument, find the appropriate flag
3. **Ask for clarification**: If multiple interpretations are possible, ask the user what they meant
4. **Execute the corrected command**: Run the command with proper syntax

**Example transformation:**
```
User input:    /mobile login user@example.com
Discovered:    mobile login --help shows --email flag
Corrected:     mobile login --email user@example.com
```

---

## Core Commands (Cross-Platform)

These commands are available on **both** iOS and Android with similar interfaces.

### build

Build targets using the repository's build system.

```bash
mobile build [targets...]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--config=<config>` | Yes | - | Build configuration (debug, release) |
| `--variant=<variant>` | Yes | - | Build flavor (alpha, dogfood) |
| `--apk` | - | Yes | Build APK output |
| `--additional-targets` | Yes | - | Include related targets |

**Examples:**
```bash
mobile build UIKit                    # Build a specific module
mobile build UIKit --config=debug     # iOS: Build with debug config
mobile build --apk                   # Android: Build APK
```

### test

Run tests in the project.

```bash
mobile test [targets...]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--dirty` | Yes | Yes | Only run tests for changed files |
| `--flavor=<flavor>` | - | Yes | Test flavor to use |

**Target formats:** Module name, build label (`//Foo/...`), or file path.

**Examples:**
```bash
mobile test MyFeatureTests    # Run tests for a module
mobile test --dirty           # Run only changed tests
```

### lint

Run linters on the codebase.

```bash
mobile lint
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--tidy` | Yes | Yes | Auto-fix lint issues |
| `--tasks=<tasks>` | Yes | Yes | Run specific lint tasks only |
| `--all` | Yes | Yes | Run all linters on all files |
| `--fix` | Yes | - | Alias for --tidy on iOS |

**Examples:**
```bash
mobile lint --tidy              # Run linters with auto-fix
mobile lint --tasks=swiftlint   # Run specific lint task
```

### run

Run the app in simulator/emulator.

```bash
mobile run [target]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--device=<device>` | Yes | Yes | Device/simulator to run on |
| `--os=<version>` | Yes | - | iOS version for simulator |
| `--version=<version>` | - | Yes | App version to run |
| `--sha=<sha>` | - | Yes | Specific commit SHA to run |

**Examples:**
```bash
mobile run                           # Run on default simulator
mobile run --device="iPhone 15 Pro"  # iOS: Run on specific device
mobile run --version=4.50          # Android: Run specific version
```

### module

Scaffold, edit, and manage modules.

```bash
mobile module <subcommand>
```

| Subcommand | iOS | Android | Description |
|------------|-----|---------|-------------|
| `create <path>` | Yes | Yes | Create a new module |
| `edit <module>` | Yes | - | Edit module (add tests, etc.) |
| `move <src> <dest>` | Yes | - | Move/rename a module |
| `find <query>` | Yes | - | Find modules matching query |
| `presenter` | - | Yes | Create a presenter |

### proto

Update protobuf definitions.

```bash
mobile proto update
```

### login

Start the app and log in with credentials.

```bash
mobile login [options]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--email=<email>` | Yes | Yes | Email address to log in with |
| `--phone-number=<phone>` | Yes | Yes | Phone number to log in with |

**Argument handling:** If user provides a bare email or phone number, map it to the correct flag:
- `/mobile login user@example.com` → `mobile login --email=user@example.com`
- `/mobile login +15551234567` → `mobile login --phone-number=+15551234567`

**Examples:**
```bash
mobile login --email=user@example.com
mobile login --phone-number="+1234567890"
```

---

## iOS-Specific Commands

These commands are **only available in app-ios**.

| Command | Description | Example |
|---------|-------------|---------|
| `mobile analyze` | Codebase analysis (14 subcommands) | `mobile analyze --upload` |
| `mobile ci` | CI tasks | `mobile ci --build-event-directory=<path>` |
| `mobile cursor` | Cursor IDE setup | `mobile cursor setup` |
| `mobile docs` | Build DocC documentation | `mobile docs --open` |
| `mobile github` | GitHub interactions | `mobile github auth`, `mobile github pr` |
| `mobile jira` | JIRA ticket management | `mobile jira create`, `mobile jira list` |
| `mobile knit` | Dependency injection | `mobile knit test`, `mobile knit validate` |
| `mobile linear` | Linear issue tracking | `mobile linear create`, `mobile linear list` |
| `mobile localization` | i18n/l10n tasks | `mobile localization extract-all` |
| `mobile project` | Xcode project generation | `mobile project edit`, `mobile project focus` |
| `mobile sim` | Simulator management | `mobile sim open-url <url>`, `mobile sim show-touches` |
| `mobile slices` | App slice management | `mobile slices list`, `mobile slices enable` |
| `mobile snaps` | Snapshot testing | `mobile snaps record`, `mobile snaps download` |
| `mobile spm` | Swift Package Manager | `mobile spm resolve`, `mobile spm update` |
| `mobile tools` | Misc tools | `mobile tools buildozer`, `mobile tools swiftlint` |
| `mobile vscode` | VS Code setup | `mobile vscode setup` |
| `mobile zed` | Zed IDE setup | `mobile zed setup` |
| `mobile cdf` | Event testing | `mobile cdf local` |
| `mobile feature-flags` | Feature flag CLI | `mobile feature-flags <args>` |

For detailed usage, run: `mobile <command> --help`

---

## Android-Specific Commands

These commands are **only available in app-android**.

| Command | Description | Example |
|---------|-------------|---------|
| `mobile navigation` | Screen/presenter lookup | `mobile navigation --device=<id>` |
| `mobile bugsnag` | Crash analysis by module | `mobile bugsnag --module=<name>` |
| `mobile pr` | Create pull requests | `mobile pr --title="Title" --draft` |
| `mobile lib update` | Update libraries | `mobile lib update androidProtos` |
| `mobile feature-flag` | Feature flag CLI | `mobile feature-flag --update` |
| `mobile ide run` | Bootstrap dev environment | `mobile ide run` |
| `mobile ide channel setup` | IDE channel subscription | `mobile ide channel setup stable` |
| `mobile ide profile setup` | IDE profile subscription | `mobile ide profile setup` |
| `mobile release` | Find release branch | `mobile release --commit-hash=<sha>` |

For detailed usage, run: `mobile <command> --help`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `mobile: command not found` | Run the install script (see Prerequisites) |
| Command not found | Run `mobile --help` to see available commands |
| CLI is outdated | Run `mobile update` or reinstall |
| Build fails | Check `mobile <command> --help` for correct syntax |

## Resources

- [Mobile CLI Documentation](https://<internal-docs-url>/mobile/docs/cli)
- [iOS CLI Source](https://github.com/<org>/app-ios/tree/main/Tools/MobileCLI)
- [Android CLI Source](https://github.com/<org>/app-android/tree/master/mobile-android-cli)
- Slack: `#mobile-cli-support`
