---
name: cash
description: |
  Use the Cash CLI for common Cash App iOS & Android developer tasks. Use when building,
  testing, linting, running, or managing modules in cash-ios or cash-android repositories.
  Auto-detects platform and shows relevant commands.
roles: [mobile, cash-android, cash-ios]
argument-hint: <command> [args...] (e.g., build, test, lint, run, module, login)
allowed-tools: Bash(cash:*), Bash(cash), AskUserQuestion
metadata:
  author: jamesalee
  status: experimental
  version: "0.4.0"
---

# Cash CLI

The Cash CLI is the unified command-line interface for Cash App iOS & Android developer tasks.

## Direct Command Execution

When the user invokes `/cash <command> [args...]`, execute the command directly if it matches a known command pattern.

### Known Commands (execute directly)

These commands can be run immediately when invoked with `/cash`:

| Command Pattern | Action |
|-----------------|--------|
| `build [targets...] [flags]` | Run `cash build [targets...] [flags]` |
| `test [targets...] [flags]` | Run `cash test [targets...] [flags]` |
| `lint [flags]` | Run `cash lint [flags]` |
| `run [target] [flags]` | Run `cash run [target] [flags]` |
| `module <subcommand> [args]` | Run `cash module <subcommand> [args]` |
| `proto update` | Run `cash proto update` |
| `login [flags]` | Run `cash login [flags]` (see special handling below) |
| `--help` or `-h` | Run `cash --help` |
| `<command> --help` | Run `cash <command> --help` |
| `update` | Run `cash update` |

### Special Argument Handling

**Login command**: Map bare arguments to flags:
- `/cash login user@example.com` → `cash login --email=user@example.com`
- `/cash login +15551234567` → `cash login --phone-number=+15551234567`
- `/cash login --email=...` → pass through as-is

### Execution Flow

1. **Parse the command**: Extract the command and arguments from `/cash <input>`
2. **Match known pattern**: If the command matches a known pattern above, execute it directly
3. **Unknown command**: If not recognized, do NOT execute directly. Instead, follow the "Handling Unknown Command Formats" section below
4. **Report results**: Show the command output to the user

### Examples

```
/cash build Arcade                    → cash build Arcade
/cash test --dirty                    → cash test --dirty
/cash lint --tidy                     → cash lint --tidy
/cash run --device="iPhone 15 Pro"    → cash run --device="iPhone 15 Pro"
/cash module create MyModule          → cash module create MyModule
/cash login test@example.com          → cash login --email=test@example.com
/cash --help                          → cash --help
/cash sim --help                      → cash sim --help
```

---

## Platform Detection

Detect which repository you're in:

!`if [[ -f "Tools/CashCLI/BUILD.bazel" ]]; then echo "ios"; elif [[ -f "cash-android-cli/build.gradle.kts" ]]; then echo "android"; else echo "unknown"; fi`

- **iOS** (`cash-ios`): Uses Bazel, CLI at `Tools/CashCLI/`
- **Android** (`cash-android`): Uses Gradle, CLI at `cash-android-cli/`
- **Unknown**: Not in a Cash repository. Install the CLI first (see Prerequisites).

## Prerequisites

Install the Cash CLI:

```bash
curl -fsSL "https://global.block-artifacts.com/artifactory/cash-cli/install.sh" | bash
```

## Command Discovery

When the user asks about a command not documented below, run the help command to discover it:

```bash
# List ALL available commands for this platform
cash --help

# Get detailed help for a specific command
cash <command> --help
```

Always run `cash --help` first if you're unsure what commands are available.

## Handling Unknown Command Formats

When a user provides a command in an unfamiliar or incorrect format:

1. **Discover the correct syntax**: Run `cash <command> --help` to see available flags and arguments
2. **Map user intent to correct flags**: If the user provides a positional argument, find the appropriate flag
3. **Ask for clarification**: If multiple interpretations are possible, ask the user what they meant
4. **Execute the corrected command**: Run the command with proper syntax

**Example transformation:**
```
User input:    /cash login user@example.com
Discovered:    cash login --help shows --email flag
Corrected:     cash login --email user@example.com
```

---

## Core Commands (Cross-Platform)

These commands are available on **both** iOS and Android with similar interfaces.

### build

Build targets using the repository's build system.

```bash
cash build [targets...]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--config=<config>` | Yes | - | Build configuration (debug, release) |
| `--variant=<variant>` | Yes | - | Build flavor (alpha, dogfood) |
| `--apk` | - | Yes | Build APK output |
| `--additional-targets` | Yes | - | Include related targets |

**Examples:**
```bash
cash build Arcade                    # Build a specific module
cash build Arcade --config=debug     # iOS: Build with debug config
cash build --apk                   # Android: Build APK
```

### test

Run tests in the project.

```bash
cash test [targets...]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--dirty` | Yes | Yes | Only run tests for changed files |
| `--flavor=<flavor>` | - | Yes | Test flavor to use |

**Target formats:** Module name, build label (`//Foo/...`), or file path.

**Examples:**
```bash
cash test MyFeatureTests    # Run tests for a module
cash test --dirty           # Run only changed tests
```

### lint

Run linters on the codebase.

```bash
cash lint
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--tidy` | Yes | Yes | Auto-fix lint issues |
| `--tasks=<tasks>` | Yes | Yes | Run specific lint tasks only |
| `--all` | Yes | Yes | Run all linters on all files |
| `--fix` | Yes | - | Alias for --tidy on iOS |

**Examples:**
```bash
cash lint --tidy              # Run linters with auto-fix
cash lint --tasks=swiftlint   # Run specific lint task
```

### run

Run the app in simulator/emulator.

```bash
cash run [target]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--device=<device>` | Yes | Yes | Device/simulator to run on |
| `--os=<version>` | Yes | - | iOS version for simulator |
| `--version=<version>` | - | Yes | App version to run |
| `--sha=<sha>` | - | Yes | Specific commit SHA to run |

**Examples:**
```bash
cash run                           # Run on default simulator
cash run --device="iPhone 15 Pro"  # iOS: Run on specific device
cash run --version=4.50          # Android: Run specific version
```

### module

Scaffold, edit, and manage modules.

```bash
cash module <subcommand>
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
cash proto update
```

### login

Start the app and log in with credentials.

```bash
cash login [options]
```

| Flag | iOS | Android | Description |
|------|-----|---------|-------------|
| `--email=<email>` | Yes | Yes | Email address to log in with |
| `--phone-number=<phone>` | Yes | Yes | Phone number to log in with |

**Argument handling:** If user provides a bare email or phone number, map it to the correct flag:
- `/cash login user@example.com` → `cash login --email=user@example.com`
- `/cash login +15551234567` → `cash login --phone-number=+15551234567`

**Examples:**
```bash
cash login --email=user@example.com
cash login --phone-number="+1234567890"
```

---

## iOS-Specific Commands

These commands are **only available in cash-ios**.

| Command | Description | Example |
|---------|-------------|---------|
| `cash analyze` | Codebase analysis (14 subcommands) | `cash analyze --upload` |
| `cash ci` | CI tasks | `cash ci --build-event-directory=<path>` |
| `cash cursor` | Cursor IDE setup | `cash cursor setup` |
| `cash docs` | Build DocC documentation | `cash docs --open` |
| `cash github` | GitHub interactions | `cash github auth`, `cash github pr` |
| `cash jira` | JIRA ticket management | `cash jira create`, `cash jira list` |
| `cash knit` | Dependency injection | `cash knit test`, `cash knit validate` |
| `cash linear` | Linear issue tracking | `cash linear create`, `cash linear list` |
| `cash localization` | i18n/l10n tasks | `cash localization extract-all` |
| `cash project` | Xcode project generation | `cash project edit`, `cash project focus` |
| `cash sim` | Simulator management | `cash sim open-url <url>`, `cash sim show-touches` |
| `cash slices` | App slice management | `cash slices list`, `cash slices enable` |
| `cash snaps` | Snapshot testing | `cash snaps record`, `cash snaps download` |
| `cash spm` | Swift Package Manager | `cash spm resolve`, `cash spm update` |
| `cash tools` | Misc tools | `cash tools buildozer`, `cash tools swiftlint` |
| `cash vscode` | VS Code setup | `cash vscode setup` |
| `cash zed` | Zed IDE setup | `cash zed setup` |
| `cash cdf` | CDF event testing | `cash cdf local` |
| `cash ccb` | CCB dashboard | Opens browser |
| `cash compony` | Compony CLI passthrough | `cash compony <args>` |
| `cash feature-flags` | Feature flag CLI | `cash feature-flags <args>` |

For detailed usage, run: `cash <command> --help`

---

## Android-Specific Commands

These commands are **only available in cash-android**.

| Command | Description | Example |
|---------|-------------|---------|
| `cash navigation` | Screen/presenter lookup | `cash navigation --device=<id>` |
| `cash bugsnag` | Crash analysis by module | `cash bugsnag --module=<name>` |
| `cash pr` | Create pull requests | `cash pr --title="Title" --draft` |
| `cash lib update` | Update libraries | `cash lib update cashAndroidProtos` |
| `cash feature-flag` | Feature flag CLI | `cash feature-flag --update` |
| `cash compony` | Compony CLI | `cash compony --update` |
| `cash ccb` | Trigger CCB process | `cash ccb` |
| `cash ide run` | Bootstrap dev environment | `cash ide run` |
| `cash ide channel setup` | IDE channel subscription | `cash ide channel setup stable` |
| `cash ide profile setup` | IDE profile subscription | `cash ide profile setup` |
| `cash release` | Find release branch | `cash release --commit-hash=<sha>` |

For detailed usage, run: `cash <command> --help`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `cash: command not found` | Run the install script (see Prerequisites) |
| Command not found | Run `cash --help` to see available commands |
| CLI is outdated | Run `cash update` or reinstall |
| Build fails | Check `cash <command> --help` for correct syntax |

## Resources

- [Cash CLI Documentation](https://dev-guides.sqprod.co/cash/docs/mobile/cli)
- [iOS CLI Source](https://github.com/squareup/cash-ios/tree/main/Tools/CashCLI)
- [Android CLI Source](https://github.com/squareup/cash-android/tree/master/cash-android-cli)
- Slack: [#cash-cli-group](https://square.enterprise.slack.com/archives/C04HHDP1T0T)
