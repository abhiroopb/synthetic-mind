---
Skill name: free-disk-space
Skill description: Survey and clean up disk space on macOS developer machines. Targets known locations where storage accumulates (Gradle, Xcode, npm, etc.), categorizes by safety level, and executes cleanup only with explicit approval. Use when disk is full, running low on space, or wanting to reclaim storage.
roles: []
allowed-tools:
  - Bash(du:*)
  - Bash(rm:*)
  - Bash(gradle:*)
  - Bash(./gradlew:*)
  - Bash(xcrun:*)
  - Bash(brew:*)
  - Bash(git gc:*)
  - Bash(git worktree:*)
  - Bash(echo:*)
  - Bash(ls:*)
  - Bash(sort:*)
  - Bash(grep:*)
  - Read
  - Glob
  - AskUserQuestion
---

# Free Disk Space

Help macOS developers reclaim disk space by targeting **known locations** where storage accumulates.

## Principles

1. **Targeted, not exhaustive**: Only scan known problem areas. Fast execution over comprehensive scanning.
2. **Safe by default**: Always show commands before running. Always ask for permission. Never delete without approval.
3. **Educational**: Explain what each location contains and why it's safe (or not) to delete.
4. **No permission changes**: If files require `chmod` to delete, flag them but don't change permissions.

## Workflow

### Step 1: Survey

Run this to get a quick overview of known large directories:

```bash
echo "=== Quick Disk Survey ==="
du -sh ~/.android 2>/dev/null || echo "~/.android: not found"
du -sh ~/.gradle 2>/dev/null || echo "~/.gradle: not found"
du -sh ~/.m2 2>/dev/null || echo "~/.m2: not found"
du -sh ~/.cache 2>/dev/null || echo "~/.cache: not found"
du -sh ~/Library/Caches 2>/dev/null || echo "~/Library/Caches: not found"
du -sh ~/Library/Developer 2>/dev/null || echo "~/Library/Developer: not found"
du -sh ~/Library/Android/sdk 2>/dev/null || echo "~/Library/Android/sdk: not found"
```

### Step 2: Categorize

Group results by safety level and present a summary table:

- **Safe to delete** — caches that rebuild automatically
- **Use caution** — may contain active work or in-use resources; ask before deleting
- **Keep** — should not be deleted

### Step 3: Present Options

Show the user what you found, grouped by category. For each item show:
- Location and size
- What it contains
- Safety classification
- The exact command(s) that would be run

### Step 4: Execute with Approval

**Never delete without explicit user confirmation.** Ask which categories or specific items they want to clean up, then execute only what was approved.

---

## Known Storage Locations

### Android Development

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/.android/avd/` | Android emulators (AVDs) | ⚠️ Ask which emulators are in use |
| `~/Library/Android/sdk/system-images/` | System images for emulators | ⚠️ Check which are in use by AVDs |
| `~/.gradle/daemon/` | Gradle daemon logs | ✅ Yes |
| `~/.gradle/.tmp/` | Gradle temp files | ✅ Yes |
| `~/.gradle/build-scan-data/` | Build analytics | ✅ Yes |
| `~/.gradle/wrapper/` | Gradle versions | ❌ Keep - stores Gradle distributions |
| `~/Library/Caches/Google/AndroidStudio*/` | Android Studio caches | ⚠️ Keep current version, delete old |
| `~/Library/Application Support/Google/AndroidStudio*/` | AS settings | ⚠️ Usually small, keep |

**Cleanup commands:**
```bash
# Stop Gradle daemons before cleaning
gradle --stop

# Clean Gradle temp/logs (safe)
rm -rf ~/.gradle/daemon
rm -rf ~/.gradle/.tmp
rm -rf ~/.gradle/build-scan-data

# List AVDs with sizes
du -sh ~/.android/avd/*.avd | sort -hr

# Check which system images are in use
grep -h "image.sysdir" ~/.android/avd/*.avd/config.ini
```

### iOS Development

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/Library/Developer/Xcode/DerivedData/` | Xcode build artifacts | ✅ Yes - rebuilds as needed |
| `~/Library/Developer/CoreSimulator/` | iOS Simulators | ⚠️ Ask which are in use |
| `~/Library/Developer/Xcode/Archives/` | App archives | ⚠️ May want to keep recent |
| `~/Library/Caches/CocoaPods/` | CocoaPods cache | ✅ Yes |

**Cleanup commands:**
```bash
# Clean Xcode derived data
rm -rf ~/Library/Developer/Xcode/DerivedData/*

# List simulators (requires Xcode)
xcrun simctl list devices

# Clean CocoaPods cache
rm -rf ~/Library/Caches/CocoaPods
```

### JetBrains IDEs

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/Library/Caches/JetBrains/` | IDE caches (IntelliJ, Fleet, etc.) | ⚠️ Keep current version |

**Cleanup commands:**
```bash
# List JetBrains caches by size
du -d 1 -h ~/Library/Caches/JetBrains | sort -hr

# Delete old versions (example - adjust versions)
rm -rf ~/Library/Caches/JetBrains/IntelliJIdea2024.*
rm -rf ~/Library/Caches/JetBrains/Fleet
```

### Python

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/.cache/uv/` | uv package manager cache | ✅ Yes |
| `~/.cache/pip/` | pip cache | ✅ Yes |
| `~/.pyenv/versions/` | Python versions | ⚠️ Ask which are in use |

**Cleanup commands:**
```bash
rm -rf ~/.cache/uv
rm -rf ~/.cache/pip
```

### Rust

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/.cargo/registry/` | Cargo package cache | ✅ Yes |
| `~/.rustup/toolchains/` | Rust toolchains | ⚠️ Ask which are in use |

### Node.js

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/.npm/` | npm cache | ✅ Yes |
| `~/Library/Caches/Yarn/` | Yarn cache | ✅ Yes |

**Cleanup commands:**
```bash
rm -rf ~/.npm
rm -rf ~/Library/Caches/Yarn
```

### Homebrew

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/Library/Caches/Homebrew/` | Downloaded packages | ✅ Yes |

**Cleanup commands:**
```bash
rm -rf ~/Library/Caches/Homebrew
# Or use: brew cleanup --prune=all
```

### Bazel

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/Library/Caches/bazel*/` | Bazel build cache | ✅ Yes |
| `~/.cache/bazel*/` | Bazel cache (alternate location) | ✅ Yes |

**Cleanup commands:**
```bash
rm -rf ~/Library/Caches/bazel*
rm -rf ~/.cache/bazel*
```

### Git Repositories

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `<repo>/build/` | Build outputs in repos | ✅ Yes |
| `<repo>/.gradle/` | Project Gradle cache | ✅ Yes |
| `*-worktrees/` directories | Git worktrees | ⚠️ Check for uncommitted work |

**Cleanup commands:**
```bash
# List all worktrees for a repo
git worktree list

# Clean build outputs (from repo root)
./gradlew clean

# Compact git history (fast - usually sufficient)
git gc --prune=now

# Compact git history (slow - maximum compression)
# Only use --aggressive after major cleanups (deleted branches, force pushes)
# Can take 30+ minutes on large repos
git gc --aggressive --prune=now
```

**git gc explained:**
- `git gc` — Packs loose objects, removes unreachable objects, compresses repo
- `--prune=now` — Immediately remove unreachable objects (default waits 2 weeks)
- `--aggressive` — Recomputes all deltas with max compression. Much slower but smaller result. Only worth it after significant history changes.

### System Caches

| Location | Description | Safe to Delete? |
|----------|-------------|-----------------|
| `~/Library/Caches/Spotify/` | Music cache | ✅ Yes |
| `~/Library/Caches/Firefox/` | Browser cache | ✅ Yes (may slow browsing briefly) |
| `~/.Trash/` | Trash | ✅ Yes |

**Cleanup commands:**
```bash
# Empty trash
rm -rf ~/.Trash/*

# Clear app caches (check sizes first)
du -sh ~/Library/Caches/Spotify 2>/dev/null
du -sh ~/Library/Caches/Firefox 2>/dev/null
```

## du Cheat Sheet

```bash
du [options] [path]

# Key options:
-h    # Human readable (KB, MB, GB)
-s    # Summary (total only)
-d N  # Depth: how many levels deep to report

# Common patterns:
du -sh /path          # Total size of one directory
du -sh /path/*        # Size of each item in directory
du -d 1 -h /path      # One level deep with sizes
du -sh * | sort -hr   # Current dir, sorted largest first
```
