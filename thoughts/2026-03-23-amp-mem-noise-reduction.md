# Cutting 80% of the Noise from My AI Memory System

## TL;DR

After distilling 2,718 observations, I found ~90% were noise. Made 7 changes to the amp-mem plugin that should cut observation volume by ~80% while preserving all meaningful signal. The key insight: tool-level captures are mostly redundant when you have an AI-gated turn evaluator. The real signal comes from what you *do* with search results, not the searches themselves.

## Context

I ran `kb-distill` for the first time in a while and found 2,718 pending observations. That's… a lot. So I actually looked at them.

Only ~42 were high-signal — real preferences, decisions, discoveries, workflow patterns. The rest? Raw command traces, search queries, email draft records, and meta-noise about the memory system itself. 42 out of 2,718. That's a 1.5% signal rate.

The passive capture system I [built and tuned](./2026-03-11-tuning-memory-noise.md) was doing its job — it just wasn't filtering hard enough. Every Gmail search, every Slack read, every `amp-mem search` call was generating an observation. The structured extractors were firing on read-only operations that produced zero actionable insight.

The distillation process (kb-distill) still surfaced the real patterns — that's the compression step that matters — but wading through 2,700 garbage entries to find 42 gems is not a system that scales.

## The Changes

Seven targeted changes to `~/.config/amp/plugins/amp-mem.ts`:

### 1. Added amp_mem tools to IGNORED_TOOLS

```typescript
const IGNORED_TOOLS = [
  // ... existing entries
  'amp_mem_search',
  'amp_mem_save',
  'amp_mem_stats',
]
```

The memory system was observing itself. Again. I [fixed this at the context injection layer](./2026-03-11-tuning-memory-noise.md) before, but the capture layer was still recording every `amp_mem_search` call as a structured observation. Pure meta-noise.

### 2. Skipped Gmail drafts from structured capture

```typescript
// Skip Gmail draft operations — "Drafted email to X" floods decisions
if (toolName === 'mcp__gmail__draft_tool') return
```

Every email draft was being captured as a "decision" observation. Drafting an email is not a decision — it's an action. The actual decision (what to say, who to reply to) is captured by the AI-gated turn evaluator at the end of the turn. The per-tool capture was just adding noise.

### 3. Skipped all search/read tools

```typescript
const READ_ONLY_TOOLS = [
  'mcp__gmail__search_tool',
  'mcp__gmail__read_message_tool',
  'mcp__slack__search_messages',
  'mcp__slack__read_channel',
  'mcp__linear__linear_searchIssues',
  'mcp__linear__linear_getIssueById',
  'mcp__notion__notion_search',
  'mcp__notion__notion_fetch',
  'mcp__gdrive__search',
  'mcp__gdrive__read',
]
```

This was the biggest single win. Every search across every tool was generating observations like "Searched Gmail for cash rounding emails" or "Read Slack message in #checkout-flow." None of that is signal. What matters is what the agent *does* after reading — reply, create a ticket, draft a doc. That's captured by the turn evaluator.

### 4. Bash: skip slack-cli, amp-mem, block-glean-cli

```typescript
const SKIP_BASH_PREFIXES = [
  'slack-cli',
  'amp-mem',
  'block-glean-cli',
  'warp-cli',
  'git status',
  'git fetch',
]
```

Bash commands were already partially filtered, but CLI wrappers for MCP tools were slipping through. A `slack-cli search` command is the same noise as a `mcp__slack__search_messages` call — just via a different path.

### 5. Generic extractor: only capture write/mutate operations

```typescript
const WRITE_OPS_PATTERN = /create|update|post|send|draft|edit|delete|transition|assign|move|add|remove/i

// In the generic MCP extractor:
if (!WRITE_OPS_PATTERN.test(toolName)) return
```

This is the philosophical shift. Instead of capturing everything and filtering later, only capture operations that *change state*. Reads are context-gathering. Writes are decisions. The memory system should remember decisions.

### 6. AI gating threshold: 0.65 → 0.75

```typescript
const AI_GATE_THRESHOLD = 0.75  // was 0.65
```

The `agent.end` handler runs an AI evaluation on the full turn to decide if anything worth remembering happened. Bumping the threshold from 0.65 to 0.75 makes it pickier. Combined with the other filters, this means fewer but higher-quality observations from the safety-net layer.

### 7. Deduplication via recentTopics

```typescript
const recentTopics = new Set<string>()

function isDuplicate(topic: string): boolean {
  const normalized = topic.toLowerCase().trim()
  if (recentTopics.has(normalized)) return true
  recentTopics.add(normalized)
  // Clean up after 50 entries
  if (recentTopics.size > 50) {
    const first = recentTopics.values().next().value
    recentTopics.delete(first)
  }
  return false
}
```

Same insight was getting saved 2-3x per session because multiple tools in the same turn would each trigger a capture. The dedup set catches these within-session repeats.

### Bonus: Short user prompts

```typescript
// Skip user messages under 30 chars — "ok", "yes", "do it" aren't worth saving
if (event.content.length < 30) return
```

"yes", "ok", "do that", "looks good" — none of these are observations worth persisting.

## The Key Insight

The safety net is the AI-gated `agent.end` handler. It evaluates the *entire turn* — all tool calls, all results, the user's message, the agent's response — and decides if anything meaningful happened. That's where the real signal extraction lives.

Tool-level structured captures were mostly *redundant* with that. They were pre-extracting observations that the turn evaluator would catch anyway, but at lower quality because they lacked the full-turn context.

The right architecture: aggressive filtering at the tool level (only capture writes/mutations), with the AI-gated turn evaluator as the quality layer that catches everything else worth remembering.

## What I Learned

1. **Passive capture without curation creates garbage.** The instinct to "capture everything, filter later" doesn't work for memory systems. The volume grows faster than your ability to filter. Better to be aggressive at capture time and trust your safety-net evaluator.

2. **The distillation step is what matters.** kb-distill takes raw observations and compresses them into structured knowledge notes. That's the actual intelligence — the pattern recognition, the synthesis, the "what does this mean?" step. Raw observations are just the input.

3. **Read operations are almost never signal.** What you searched for doesn't matter. What you did with what you found — that's the signal. This applies broadly: logs of "user viewed page" are noise; "user purchased item" is signal.

4. **Keep the AI gate as your quality layer.** Don't try to make every extractor smart. Make them fast and selective, then let one high-quality AI evaluation at the end decide what's worth keeping.

5. **1.5% signal rate means your filter is broken.** If you're keeping 98.5% garbage, you don't have a memory system — you have a logging system. Memory requires curation.

---

*This is the third post in the amp-mem series, after [Building a Persistent Memory System](./2026-03-05-building-amp-mem.md) and [The Signal-to-Noise Problem](./2026-03-11-tuning-memory-noise.md). The pattern: build → tune injection → tune capture. Next will probably be tuning retrieval.*

---

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
