// @i-know-the-amp-plugin-api-is-wip-and-very-experimental-right-now
//
// amp-mem plugin — Passive memory capture for Amp
// Inspired by claude-mem: automatically captures observations from sessions,
// classifies them by type, and injects context into future sessions.
// Wraps ~/bin/amp-mem CLI (SQLite + FTS5 backed).
//
import type {
  PluginAPI,
  PluginEventContext,
  AgentEndEvent,
  ToolResultEvent,
  ThreadMessage,
} from '@ampcode/plugin'

// ── Configuration ────────────────────────────────────────────────────────

// Pure read-only tools — zero signal, never capture
const IGNORED_TOOLS = new Set([
  'Read', 'glob', 'Grep', 'finder',
  'read_web_page', 'web_search', 'look_at',
  'mermaid', 'read_thread', 'find_thread',
  'undo_edit', 'oracle', 'librarian', 'get_diagnostics',
])

// File edit tools — batched per turn, saved at agent.end
const FILE_TOOLS = new Set(['edit_file', 'create_file'])

// Paths that indicate noisy/insignificant file edits
const NOISY_PATHS = [
  'node_modules', '.cache', '.tmp', '.DS_Store',
  'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
]

// Auto-consolidation threshold
const COMPACT_THRESHOLD = 100

// Batch file edits — accumulate within a turn, save once at agent.end
let pendingFileEdits: { tool: string; path: string }[] = []

// Track the current session ID
let currentSessionId: string | null = null

// Track observation count for auto-consolidation
let sessionObservationCount = 0

// ── Helpers ──────────────────────────────────────────────────────────────

/** Run amp-mem CLI and return stdout. */
async function ampMem($: PluginAPI['$'] | PluginEventContext['$'], args: string[]): Promise<string> {
  const cmd = ['$HOME/bin/amp-mem', ...args].map(a => `'${a.replace(/'/g, "'\\''")}'`).join(' ')
  try {
    const result = await $`${cmd}`
    return result.stdout.trim()
  } catch {
    return ''
  }
}

/** Extract text blocks from assistant messages */
function extractAssistantText(messages: ThreadMessage[]): string[] {
  const blocks: string[] = []
  for (const msg of messages) {
    if (msg.role === 'assistant') {
      for (const block of msg.content) {
        if (block.type === 'text' && block.text.length > 20) {
          blocks.push(block.text.slice(0, 500))
        }
      }
    }
  }
  return blocks
}

/** Extract a human-readable tool name from MCP tool names */
function friendlyToolName(tool: string): string {
  // mcp__gmail__draft_tool → Gmail: draft
  // mcp__linear__linear_createIssue → Linear: createIssue
  const match = tool.match(/^mcp__(\w+)__(?:\w+_)?(.+)$/)
  if (match) return `${match[1]}: ${match[2]}`
  return tool
}

// ── Structured extractors for known tools ────────────────────────────────

interface Extraction { type: string; topic: string; summary: string }

function extractFromTool(event: ToolResultEvent): Extraction | null {
  const input = event.input as Record<string, string>

  switch (event.tool) {
    // ── Linear ──
    case 'mcp__linear__linear_createIssue':
      return {
        type: 'decision',
        topic: `Created Linear issue: ${input.title || 'untitled'}`,
        summary: `Team: ${input.teamId || '?'}, Title: ${input.title || '?'}${input.description ? '\nDescription: ' + input.description.slice(0, 200) : ''}`,
      }
    case 'mcp__linear__linear_updateIssue':
      return {
        type: 'observation',
        topic: `Updated Linear issue: ${input.id || '?'}`,
        summary: `Updated fields: ${Object.keys(event.input).filter(k => k !== 'id').join(', ')}`,
      }
    case 'mcp__linear__linear_searchIssues':
      return {
        type: 'observation',
        topic: `Searched Linear: "${(input.query || '').slice(0, 60)}"`,
        summary: `Query: ${input.query || '?'}${input.states ? ', States: ' + input.states : ''}`,
      }

    // ── Gmail ──
    case 'mcp__gmail__draft_tool':
      return {
        type: 'decision',
        topic: `Drafted email: ${input.subject || '(reply/forward)'}`,
        summary: `To: ${input.to_recipient || '(reply)'}, Type: ${input.draft_type || 'common'}`,
      }
    case 'mcp__gmail__search_tool':
      return {
        type: 'observation',
        topic: `Searched Gmail: "${(input.subject || input.body_terms || input.from_sender || '').slice(0, 60)}"`,
        summary: `Subject: ${input.subject || '?'}, From: ${input.from_sender || '?'}`,
      }
    case 'mcp__gmail__read_message_tool':
      return {
        type: 'observation',
        topic: `Read email: ${(input.message_ids as unknown as string[])?.length || 1} message(s)`,
        summary: `Message IDs: ${JSON.stringify(input.message_ids).slice(0, 100)}`,
      }

    // ── Slack ──
    case 'mcp__slack__slack_post_message':
      return {
        type: 'decision',
        topic: `Posted to Slack: #${input.channel || '?'}`,
        summary: `Channel: ${input.channel || '?'}\nMessage: ${(input.text || '').slice(0, 200)}`,
      }
    case 'mcp__slack__slack_search_messages':
      return {
        type: 'observation',
        topic: `Searched Slack: "${(input.query || '').slice(0, 60)}"`,
        summary: `Query: ${input.query || '?'}`,
      }

    // ── Notion ──
    case 'mcp__notion__notion_fetch':
      return {
        type: 'observation',
        topic: `Fetched Notion page: ${(input.id || '').slice(0, 80)}`,
        summary: `Page/DB: ${input.id || '?'}`,
      }

    // ── Calendar ──
    case 'mcp__gcal__gcal_create_event':
      return {
        type: 'decision',
        topic: `Created calendar event: ${input.summary || input.title || '?'}`,
        summary: `Event: ${input.summary || input.title || '?'}, Start: ${input.start || '?'}`,
      }

    // ── Google Drive ──
    case 'mcp__gdrive__gdrive_create_doc':
      return {
        type: 'decision',
        topic: `Created Google Doc: ${input.title || '?'}`,
        summary: `Title: ${input.title || '?'}`,
      }
    case 'mcp__gdrive__gdrive_search':
      return {
        type: 'observation',
        topic: `Searched Google Drive: "${(input.query || '').slice(0, 60)}"`,
        summary: `Query: ${input.query || '?'}`,
      }

    // ── Bash ──
    case 'Bash':
      // Only capture non-trivial commands (skip simple ls, cat, etc.)
      if (input.cmd && input.cmd.length > 30) {
        return {
          type: 'observation',
          topic: `Ran command: ${(input.cmd || '').slice(0, 60)}`,
          summary: `Command: ${(input.cmd || '').slice(0, 200)}${input.cwd ? '\nDirectory: ' + input.cwd : ''}`,
        }
      }
      return null

    default:
      return null // handled by generic extractor
  }
}

// ── Plugin ───────────────────────────────────────────────────────────────

export default function (amp: PluginAPI) {
  amp.logger.log('[amp-mem] Plugin loaded')

  // ── session.start ────────────────────────────────────────────────────
  // Auto-init, backup, start session, check distill status, auto-consolidate
  amp.on('session.start', async (_event, ctx) => {
    ctx.logger.log('[amp-mem] Session starting')

    // Ensure DB exists
    await ampMem(ctx.$, ['init'])

    // Backup (daily, not per-session)
    const today = new Date().toISOString().slice(0, 10)
    try {
      const check = await ctx.$`test -f ~/.amp/memory/amp-mem.db.backup-${today} && echo exists || echo missing`
      if (check.stdout.trim() === 'missing') {
        await ctx.$`cp ~/.amp/memory/amp-mem.db ~/.amp/memory/amp-mem.db.backup-${today}`
        await ctx.$`find ~/.amp/memory -name 'amp-mem.db.backup-*' -mtime +7 -delete`
        ctx.logger.log('[amp-mem] Daily backup created')
      }
    } catch {
      ctx.logger.log('[amp-mem] Backup skipped')
    }

    // Start a session with the thread URL
    const threadId = ctx.thread?.id || ''
    const threadUrl = threadId ? `https://ampcode.com/threads/${threadId}` : ''
    const sessionArgs = ['session-start']
    if (threadUrl) sessionArgs.push('--thread-url', threadUrl)
    const sessionResult = await ampMem(ctx.$, sessionArgs)
    currentSessionId = sessionResult.trim() || null
    ctx.logger.log(`[amp-mem] Session #${currentSessionId} started (thread: ${threadId || 'none'})`)

    // Check distill status and log
    const status = await ampMem(ctx.$, ['distill-status'])
    ctx.logger.log(`[amp-mem] ${status}`)

    // Auto-consolidation: compact if too many un-compacted observations
    try {
      const statsOutput = await ampMem(ctx.$, ['stats'])
      const obsMatch = statsOutput.match(/Observations:\s+(\d+)/)
      const compactMatch = statsOutput.match(/Compacted:\s+(\d+)/)
      const totalObs = obsMatch ? parseInt(obsMatch[1]) : 0
      const compacted = compactMatch ? parseInt(compactMatch[1]) : 0
      if (totalObs > COMPACT_THRESHOLD && compacted === 0) {
        ctx.logger.log(`[amp-mem] Auto-compacting: ${totalObs} observations exceed threshold`)
        await ampMem(ctx.$, ['compact'])
        await ampMem(ctx.$, ['decay'])
      }
    } catch {
      // Non-critical
    }

    // Reset accumulators
    pendingFileEdits = []
    sessionObservationCount = 0
  })

  // ── agent.start ──────────────────────────────────────────────────────
  // Save user prompt + inject memory context
  amp.on('agent.start', async (event, ctx) => {
    // Reset file edit accumulator for this turn
    pendingFileEdits = []

    // Save raw user prompt (like claude-mem's UserPromptSubmit)
    if (event.message && event.message.length > 20) {
      const isPrivate = event.message.includes('<private>')
      const promptTopic = event.message.slice(0, 100)
      const sessionArgs = currentSessionId ? ['--session', currentSessionId] : []
      const privacyArgs = isPrivate ? ['--private'] : []
      await ampMem(ctx.$, ['save', 'session', `User prompt: ${promptTopic}`, event.message.slice(0, 500), ...sessionArgs, ...privacyArgs])
      sessionObservationCount++
    }

    // Inject recent memory context
    const context = await ampMem(ctx.$, ['context', '--lines', '20'])
    if (context && context.length > 50) {
      return {
        message: {
          content: `<amp-mem-context>\n${context}\n</amp-mem-context>`,
          display: true,
        },
      }
    }
  })

  // ── agent.end ────────────────────────────────────────────────────────
  // AI-gated observation extraction from the completed turn.
  // Saves accumulated file edits. Auto-compacts if needed.
  amp.on('agent.end', async (event, ctx) => {
    if (event.status !== 'done') return

    const toolCalls = amp.helpers.toolCallsInMessages(event.messages)
    const textBlocks = extractAssistantText(event.messages)

    // Skip trivial turns
    if (textBlocks.length === 0 && toolCalls.length === 0) return

    const toolSummary = toolCalls
      .slice(0, 15)
      .map(tc => tc.call.tool)
      .join(', ')

    // ── Save accumulated file edits as a batch observation ──
    if (pendingFileEdits.length > 0) {
      const uniquePaths = [...new Set(pendingFileEdits.map(e => e.path))]
      const filesTopic = `Edited ${uniquePaths.length} file(s)`
      const filesSummary = uniquePaths.map(p => `- ${p}`).join('\n')

      if (uniquePaths.length > 1 || uniquePaths.some(p =>
        p.includes('plugin') || p.includes('AGENTS') || p.includes('SKILL') ||
        p.includes('config') || p.includes('schema'))) {
        const sessionArgs = currentSessionId ? ['--session', currentSessionId] : []
        await ampMem(ctx.$, ['save', 'observation', filesTopic, filesSummary, ...sessionArgs])
        sessionObservationCount++
        ctx.logger.log(`[amp-mem] Saved file edits: ${uniquePaths.length} files`)
      }
      pendingFileEdits = []
    }

    // ── AI-gated observation extraction from the turn ──
    const turnText = textBlocks.slice(0, 4).join('\n---\n')
    const turnSummary = `User prompt: ${event.message.slice(0, 200)}\n\nTools: [${toolSummary}]\n\nAssistant output:\n${turnText}`.slice(0, 2000)

    const assessment = await ctx.ai.ask(
      `Does this agent conversation turn contain a noteworthy insight worth preserving ` +
      `for future sessions? In your reasoning, classify it as one of: ` +
      `DECISION (chose/decided something), DISCOVERY (found/learned something new), ` +
      `PREFERENCE (user expressed a preference), BUGFIX (fixed a bug), ` +
      `CONFIG (changed configuration/settings), WORKFLOW (established a process/pattern), ` +
      `PEOPLE (context about a person/team), or OBSERVATION (general noteworthy fact).\n\n` +
      `NOT noteworthy: trivial reads, routine greetings, simple file lookups, ` +
      `pure informational responses with no new insight.\n\n` +
      `Turn summary:\n${turnSummary}`
    )

    ctx.logger.log(`[amp-mem] Turn assessment: ${assessment.result} (p=${assessment.probability.toFixed(2)}) — ${assessment.reason}`)

    if (assessment.result === 'yes' && assessment.probability > 0.65) {
      let type = 'observation'
      const reason = assessment.reason.toUpperCase()
      if (reason.includes('DECISION')) type = 'decision'
      else if (reason.includes('DISCOVERY')) type = 'discovery'
      else if (reason.includes('PREFERENCE')) type = 'preference'
      else if (reason.includes('BUGFIX')) type = 'bugfix'
      else if (reason.includes('CONFIG')) type = 'config'
      else if (reason.includes('WORKFLOW')) type = 'workflow'
      else if (reason.includes('PEOPLE')) type = 'people'

      const isPrivate = event.message.includes('<private>')
      const topic = event.message.slice(0, 100) || 'Agent turn'
      const summary = `${assessment.reason}\n\nTools used: ${toolSummary}`
      const sessionArgs = currentSessionId ? ['--session', currentSessionId] : []
      const privacyArgs = isPrivate ? ['--private'] : []

      await ampMem(ctx.$, ['save', type, topic, summary, ...sessionArgs, ...privacyArgs])
      sessionObservationCount++
      ctx.logger.log(`[amp-mem] Saved ${type}: ${topic}`)
    }

    // ── Session tracking: update ended_at each turn (last one sticks) ──
    if (currentSessionId) {
      const endSummary = event.message.slice(0, 200)
      await ampMem(ctx.$, ['session-end', '--session', currentSessionId, '--summary', endSummary])
    }

    // ── Auto-consolidation: compact after many observations in this session ──
    if (sessionObservationCount > 0 && sessionObservationCount % 20 === 0) {
      ctx.logger.log(`[amp-mem] Auto-compacting after ${sessionObservationCount} observations this session`)
      await ampMem(ctx.$, ['compact', '--older-than', '14'])
      await ampMem(ctx.$, ['decay'])
    }
  })

  // ── tool.result ──────────────────────────────────────────────────────
  // Capture ALL non-ignored tool results.
  // File edits are batched. Known tools get structured extraction.
  // Unknown tools get generic capture.
  amp.on('tool.result', async (event, ctx) => {
    if (event.status !== 'done') return
    if (IGNORED_TOOLS.has(event.tool)) return

    // ── File edits: accumulate, don't save individually ──
    if (FILE_TOOLS.has(event.tool)) {
      const input = event.input as Record<string, string>
      const path = input.path || ''
      if (path && !NOISY_PATHS.some(n => path.includes(n))) {
        pendingFileEdits.push({ tool: event.tool, path })
      }
      return
    }

    // ── Try structured extraction first ──
    const structured = extractFromTool(event)
    if (structured) {
      const sessionArgs = currentSessionId ? ['--session', currentSessionId] : []
      await ampMem(ctx.$, ['save', structured.type, structured.topic, structured.summary, ...sessionArgs])
      sessionObservationCount++
      ctx.logger.log(`[amp-mem] Captured ${structured.type}: ${structured.topic}`)
      return
    }

    // ── Generic extraction for all other tools ──
    // Skip orchestration tools and noisy read-like operations
    if (['Task', 'handoff', 'skill', 'format_file', 'task_list'].includes(event.tool)) return
    // Skip Gmail/Slack read-only operations (already have search extractors above)
    if (event.tool === 'mcp__gmail__read_message_tool') return
    if (event.tool === 'mcp__gmail__labels_tool') return
    if (event.tool === 'mcp__gmail__edit_message') return
    if (event.tool === 'mcp__slack__slack_list_channels') return

    const input = event.input as Record<string, string>
    const friendly = friendlyToolName(event.tool)

    // Build a meaningful topic from the input
    let topic = `${friendly}`
    const inputKeys = Object.keys(input)
    // Use the first string input value as context
    for (const key of ['query', 'title', 'name', 'subject', 'id', 'issueId', 'channel', 'label_name']) {
      if (input[key] && typeof input[key] === 'string') {
        topic += `: ${String(input[key]).slice(0, 60)}`
        break
      }
    }

    // Build summary from input params
    const summaryParts = inputKeys
      .filter(k => input[k] && typeof input[k] === 'string' && String(input[k]).length < 200)
      .slice(0, 5)
      .map(k => `${k}: ${String(input[k]).slice(0, 100)}`)
    const summary = summaryParts.join('\n') || `Tool: ${event.tool}`

    const sessionArgs = currentSessionId ? ['--session', currentSessionId] : []
    await ampMem(ctx.$, ['save', 'observation', topic.slice(0, 100), summary.slice(0, 500), ...sessionArgs])
    sessionObservationCount++
    ctx.logger.log(`[amp-mem] Captured observation: ${topic.slice(0, 80)}`)
  })

  // ── Custom tool: amp_mem_search ────────────────────────────────────────
  amp.registerTool({
    name: 'amp_mem_search',
    description: 'Search persistent cross-session memory. Use before answering questions that might relate to past work, decisions, or context from previous sessions.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'FTS5 search query (supports AND, OR, NOT, prefix*)' },
        type: { type: 'string', description: 'Filter by type: observation, decision, discovery, preference, bugfix, config, workflow, people, session, thread' },
        limit: { type: 'number', description: 'Max results (default 20)' },
      },
      required: ['query'],
    },
    async execute(input) {
      const args = ['search', input.query as string]
      if (input.type) args.push('--type', input.type as string)
      if (input.limit) args.push('--limit', String(input.limit))
      return (await ampMem(amp.$, args)) || 'No results found.'
    },
  })

  // ── Custom tool: amp_mem_save ──────────────────────────────────────────
  amp.registerTool({
    name: 'amp_mem_save',
    description: 'Save an observation to persistent memory. Use when you encounter a noteworthy decision, discovery, preference, bug fix, or important context that the passive system might miss.',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          description: 'Type: observation, decision, discovery, preference, bugfix, config, workflow, people',
          enum: ['observation', 'decision', 'discovery', 'preference', 'bugfix', 'config', 'workflow', 'people'],
        },
        topic: { type: 'string', description: 'Short topic/title (max 100 chars)' },
        summary: { type: 'string', description: 'Detailed summary of what was learned or decided' },
        private: { type: 'boolean', description: 'Mark as private — excluded from context injection' },
        project: { type: 'string', description: 'Optional project name' },
        tags: { type: 'string', description: 'Optional comma-separated tags' },
      },
      required: ['type', 'topic', 'summary'],
    },
    async execute(input) {
      const args = ['save', input.type as string, input.topic as string, input.summary as string]
      if (input.private) args.push('--private')
      if (input.project) args.push('--project', input.project as string)
      if (input.tags) args.push('--tags', input.tags as string)
      if (currentSessionId) args.push('--session', currentSessionId)
      return (await ampMem(amp.$, args)) || 'Saved.'
    },
  })

  // ── Custom tool: amp_mem_stats ─────────────────────────────────────────
  amp.registerTool({
    name: 'amp_mem_stats',
    description: 'Show memory statistics: total observations, sessions, compacted summaries, DB size, and breakdown by type/project.',
    inputSchema: { type: 'object', properties: {} },
    async execute() {
      return (await ampMem(amp.$, ['stats'])) || 'No stats available.'
    },
  })
}
