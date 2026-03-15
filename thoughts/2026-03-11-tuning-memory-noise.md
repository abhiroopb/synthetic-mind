# The Signal-to-Noise Problem in AI Memory

## TL;DR

After a week of running amp-mem, context injection got noisy. Routine bash commands, self-referential entries about the memory system itself, duplicate injections on every agent turn, and summaries cut mid-sentence. Five targeted fixes brought the signal-to-noise ratio back: sentence-boundary truncation, duplicate injection prevention, meta-noise filtering, silent context injection, and a budget increase from 40 to 60 lines. Here's what I changed and why.

## Context

I [built amp-mem](./2026-03-05-building-amp-mem.md) to give Amp persistent memory across sessions. It worked. Maybe too well. After a week of daily use — 142 observations, 74 ingested threads, 256K database — the context block injected at session start was getting cluttered.

The symptoms:

- **Hard-cut summaries** — "Configured the LaunchDarkly flag for the new feature with targeting rules for mercha" — mid-word. Useless.
- **Self-referential noise** — Half the injected context was about the memory system itself. "Saved observation about amp-mem configuration." Thanks, I know.
- **Duplicate injection** — The `agent.start` hook fires on every turn, so the same context block was being injected 15+ times per session. Same memories, every single turn.
- **Bash noise** — `git status`, `ls`, `warp-cli connect` — routine commands getting captured and injected as if they were meaningful.
- **Visual clutter** — The context block was rendered in the chat UI with `display: true`, pushing my actual conversation down.

The system was remembering everything. It just wasn't remembering the right things at the right time.

## The Fixes

### Fix 1: Sentence-boundary truncation

The `context` command's Python script was doing a hard cut at 150 characters for summaries. Mid-word. Mid-thought. The fix: cut at sentence boundaries instead, with a higher budget.

```python
def truncate_summary(text, max_len=400):
    """Truncate at sentence boundary instead of hard-cutting mid-word."""
    if len(text) <= max_len:
        return text
    # Find the last sentence boundary before max_len
    for sep in ['. ', '! ', '? ', '; ']:
        idx = text.rfind(sep, 0, max_len)
        if idx > max_len * 0.4:  # Don't cut too short
            return text[:idx + 1].strip()
    # Fallback: cut at last space
    idx = text.rfind(' ', 0, max_len)
    return (text[:idx] + '…') if idx > 0 else text[:max_len] + '…'
```

Going from 150 to ~400 chars with sentence boundaries means each observation actually carries enough context to be useful. "Configured the LaunchDarkly flag for the new feature with targeting rules for user segments in staging." — complete thought, complete value.

### Fix 2: Duplicate injection prevention

The `agent.start` hook fires on every turn. That's by design — Amp runs it before each message. But injecting the same 40-line context block on turn 1, turn 2, turn 3, and turn 15 is pure waste.

The fix is a single boolean:

```typescript
let contextInjected = false

amp.on('session.start', async (_event, ctx) => {
  contextInjected = false  // Reset per session
  // ... rest of session start
})

amp.on('agent.start', async (event, ctx) => {
  if (contextInjected) return  // Already injected this session
  
  const context = await ampMem(ctx.$, ['context', '--lines', '60'])
  if (context && context.length > 50) {
    contextInjected = true
    return {
      message: {
        content: `<amp-mem-context>\n${context}\n</amp-mem-context>`,
        display: false,
      },
    }
  }
})
```

Context injects once at session start. Done. The agent has the memory it needs without seeing it repeated 15 times.

### Fix 3: Meta-noise filtering

The memory system was remembering itself. Every time I worked on amp-mem — which was often that first week — it would capture observations about its own configuration. Then those observations would get injected as context. Then *that* would sometimes trigger new observations about the context injection. Recursive noise.

The fix: skip entries where the topic is about the memory system itself.

```python
META_NOISE_KEYWORDS = [
    'amp-mem', 'amp_mem', 'memory system', 'memory plugin',
    'context injection', 'observation capture', 'kb-distill',
    'knowledge distillation', 'memory budget'
]

def is_meta_noise(topic, summary):
    """Skip entries about the memory system itself."""
    combined = (topic + ' ' + summary).lower()
    return any(kw in combined for kw in META_NOISE_KEYWORDS)
```

This single filter cut about 15-20% of the injected context. All of it was noise.

### Fix 4: Silent context injection

Changed `display: true` to `display: false` in the `agent.start` return value. The agent still sees the context — it's injected into the message stream — but it doesn't render in the chat UI anymore.

Before: every session started with a 40-line block of memory context visible in the chat, pushing the actual conversation down. After: clean chat, memory working invisibly in the background.

One line change. Biggest UX improvement of the batch.

### Fix 5: Context budget increase

With the noise filtered out, I could afford more signal. Bumped the context budget from 40 to 60 lines. More decisions, more preferences, more actually-useful observations — without the noise floor rising.

The combination matters: filtering noise *then* increasing budget means 60 lines of high-signal context instead of 40 lines of mixed signal.

## The Numbers

After one week of daily use:

| Metric | Value |
|--------|-------|
| Total observations | 142 |
| Database size | 256K |
| Threads ingested | 74 |
| Context lines (before) | 40, noisy |
| Context lines (after) | 60, filtered |
| Summary truncation | 150 chars hard-cut → ~400 chars sentence-boundary |
| Meta-noise filtered | ~15-20% of entries |
| Duplicate injections eliminated | ~14 per session |

## What I Learned

1. **Build the system first, then tune it.** I deliberately shipped amp-mem without these filters. You can't optimize signal-to-noise until you have enough data to see what the noise looks like. A week of real usage was the right amount of time.

2. **Self-referential noise is the sneakiest problem.** A system that observes itself creates a feedback loop. You have to explicitly break that loop. This applies to any observability system, not just AI memory.

3. **One-line UX fixes matter.** `display: true` → `display: false` took 2 seconds to change and made the biggest experiential difference. The best context injection is invisible.

4. **Sentence boundaries are worth the complexity.** Hard-cutting text at character limits is a lazy default that makes every summary worse. The 15-line Python function to find sentence boundaries was the highest-ROI code I wrote that week.

5. **Filter noise, then increase budget.** The instinct is to reduce budget when things get noisy. The better move is to filter the noise source and *increase* budget so more signal fits.

---

*This is a sequel to [Building a Persistent Memory System for Amp](./2026-03-05-building-amp-mem.md). amp-mem is still evolving — I expect to write more of these tuning posts as patterns emerge.*

---

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
