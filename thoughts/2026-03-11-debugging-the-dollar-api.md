# When Your Plugin Works but Nothing Happens

## TL;DR

The amp-mem plugin's registered tools (`amp_mem_search`, `amp_mem_save`, `amp_mem_stats`) were responding without errors but returning empty results. The root cause: Amp's experimental `$` tagged template API single-quotes arguments (preventing `$HOME` expansion) and treats interpolated strings as single tokens instead of command + args. Fix: replace `$` with `child_process.execFile` + `promisify` and swap shell backup commands for `node:fs`.

## Context

I'd just finished building [amp-mem](./2026-03-05-building-amp-mem.md) — a persistent memory system for Amp. The CLI worked great. The plugin hooked into all the right lifecycle events. Tools were registered and the agent could call them. Everything looked correct.

Except nothing worked. Every search returned empty. Every save silently did nothing. Stats came back blank. No errors anywhere.

This is the worst kind of bug. The one where everything succeeds.

## The Hunt

First thing I checked: is the database healthy?

```bash
amp-mem stats
# 105 observations, 12 sessions, last save 2 hours ago
```

Database is fine. CLI works perfectly standalone.

Next: are the tools actually registered?

Yes. The agent could see them, call them, and get responses. The responses were just... empty strings. No errors, no stack traces, no warnings.

So I narrowed it down to the `ampMem` helper function — the bridge between the plugin and the CLI. Here's what it looked like:

### Before (broken)

```typescript
async function ampMem($: PluginAPI['$'], args: string[]): Promise<string> {
  const cmd = `${process.env.HOME}/bin/amp-mem ${args.join(' ')}`
  const result = await $`${cmd}`
  return result.stdout?.trim() || ''
}
```

And for backup operations in `session.start`:

```typescript
// Backup with shell commands
await $`cp ${dbPath} ${backupPath}`
await $`ls -1t ${backupDir}/amp-mem-*.db 2>/dev/null | tail -n +8 | xargs rm -f`
```

Looks fine, right? I thought so too. But the `$` tagged template literal API has two behaviors that make this silently fail:

**Problem 1: `$HOME` doesn't expand.** The `$` API single-quotes all interpolated values for safety. So `${process.env.HOME}/bin/amp-mem` becomes `'/Users/abhiroop/bin/amp-mem search some query'` — the entire string is treated as a single executable path. There's no file at that path, so it just... returns empty.

**Problem 2: Arguments aren't split.** Even if the path resolved, `${args.join(' ')}` gets interpolated as one token. So instead of `amp-mem search "my query"` with separate arguments, you get the whole thing mashed into a single argument.

Both failures are silent. No error. No crash. Just empty stdout.

### After (fixed)

```typescript
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'
import { copyFile, readdir, unlink } from 'node:fs/promises'

const execFileAsync = promisify(execFile)
const AMP_MEM_BIN = `${process.env.HOME}/bin/amp-mem`

async function ampMem(args: string[]): Promise<string> {
  try {
    const { stdout } = await execFileAsync(AMP_MEM_BIN, args, {
      env: { ...process.env, HOME: process.env.HOME || '' },
      timeout: 15_000,
    })
    return stdout?.trim() || ''
  } catch {
    return ''
  }
}
```

And backups:

```typescript
// Backup with node:fs
await copyFile(dbPath, backupPath)

const files = await readdir(backupDir)
const backups = files
  .filter(f => f.startsWith('amp-mem-') && f.endsWith('.db'))
  .sort()
  .reverse()

for (const old of backups.slice(7)) {
  await unlink(join(backupDir, old))
}
```

Key changes:
- **`execFile` instead of `$`** — takes the binary path and args as separate parameters, no shell involved
- **`node:fs` instead of shell commands** — `copyFile`, `readdir`, `unlink` don't need a shell
- **Explicit `HOME` in env** — no reliance on shell variable expansion
- **15s timeout** — prevents hanging if the CLI gets stuck
- **No more `$` dependency** — the helper function doesn't even need the plugin context anymore

## What I Learned

1. **Experimental APIs fail silently.** The `$` tagged template API is marked experimental for a reason. It has implicit behaviors (single-quoting, token merging) that aren't obvious until they break you. The fix isn't "read the docs harder" — it's to verify with a known-good path when something goes wrong.

2. **Always test the seam.** The CLI worked. The plugin called the CLI. But the seam between them — the `ampMem` helper — was where things broke. When debugging integrations, start at the boundary.

3. **"No errors" doesn't mean "working."** This bug would've been caught instantly if `execFile` threw on a missing binary. The `$` API swallowed the failure and returned empty stdout. Silent failures are the hardest to debug. When you can, prefer APIs that fail loudly.

4. **Use the simplest API that works.** Tagged template literals are elegant. `execFile` is boring. Boring won. It takes a path, takes args as an array, and does exactly what you'd expect. No quoting rules, no token merging, no surprises.

5. **Node builtins beat shell commands in plugins.** `copyFile` is more reliable than `cp` when you don't control the shell environment. Same for `readdir` vs `ls`. If you're in a TypeScript plugin, use TypeScript tools.

---

*Debugging time: ~45 minutes. Time lost to the bug before noticing: ~3 days of sessions with no memory capture.*
