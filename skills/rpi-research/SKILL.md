---
Skill name: rpi-research
Skill description: Research codebase for complex tasks using RPI methodology. Use when starting a new feature, investigating unfamiliar code, or needing comprehensive understanding before planning. Creates documented research artifacts.
---

# RPI Research

Research phase of the RPI (Research, Plan, Implement) methodology. Creates comprehensive, documented understanding of relevant code before planning or implementation.

## One Goal Per Session

Each RPI phase (research, plan, implement, iterate) should run in its own fresh session/context. This keeps the agent focused and prevents context window degradation. Artifacts (research docs, plan files) are the bridge between phases.

## CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY

- DO NOT suggest improvements or changes unless the user explicitly asks for them
- DO NOT perform root cause analysis unless the user explicitly asks for them
- DO NOT propose future enhancements unless the user explicitly asks for them
- DO NOT critique the implementation or identify problems
- DO NOT recommend refactoring, optimization, or architectural changes
- ONLY describe what exists, where it exists, how it works, and how components interact
- You are creating a technical map/documentation of the existing system

## Initial Setup

When this skill is invoked without a specific research question, respond with:

```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (tickets, docs, JSON), read them FULLY first
   - **IMPORTANT**: Read entire files without truncation or partial reads
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research

2. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas
   - Think deeply about the underlying patterns, connections, and architectural implications the user might be seeking
   - Identify specific components, patterns, or concepts to investigate
   - Create a checklist to track all subtasks and their completion
   - Consider which directories, files, or architectural patterns are relevant

3. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Create multiple parallel sub-agents to research different aspects concurrently

   **For finding WHERE code lives:**
   ```
   "Find all files related to [component]. Return categorized list with paths:
   - Implementation files
   - Test files
   - Configuration
   - Type definitions
   Document what exists without suggesting improvements."
   ```

   **For understanding HOW code works:**
   ```
   "Analyze [specific file/component]. Trace data flow, identify key functions.
   Return analysis with file:line references.
   Document implementation without critique."
   ```

   **For finding similar patterns:**
   ```
   "Find examples of [pattern] in the codebase.
   Return code snippets with file:line references.
   Show patterns without evaluating quality."
   ```

   **IMPORTANT**: All sub-agents are documentarians, not critics. They describe what exists without suggesting improvements or identifying issues.

   The key is to use sub-agents intelligently:
   - Start with locator tasks to find what exists
   - Then use analyzer tasks on the most promising findings to document how they work
   - Run multiple tasks in parallel when they're searching for different things
   - Remind sub-agents they are documenting, not evaluating or improving

4. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results
   - Prioritize live codebase findings as primary source of truth
   - Connect findings across different components
   - Include specific file paths and line numbers for reference
   - Highlight patterns, connections, and architectural decisions
   - Answer the user's specific questions with concrete evidence

5. **Gather metadata for the research document:**
   - Run Bash commands to collect: git user name, current commit hash, branch name, repo name, current date
   - Filename: `thoughts/shared/research/YYYY-MM-DD-TICKET-description.md`
     - Format: `YYYY-MM-DD-TICKET-description.md` where:
       - YYYY-MM-DD is today's date
       - TICKET is the ticket number (omit if no ticket)
       - description is a brief kebab-case description of the research topic
     - Examples:
       - With ticket: `2025-01-08-ENG-1478-parent-child-tracking.md`
       - Without ticket: `2025-01-08-authentication-flow.md`

6. **Generate research document:**
   - Use the metadata gathered in step 5
   - Structure the document with YAML frontmatter followed by content:

   ```markdown
   ---
   date: [ISO timestamp with timezone]
   researcher: [name from git config]
   git_commit: [current commit hash]
   branch: [current branch]
   repository: [repo name]
   topic: "[Research Question]"
   tags: [research, codebase, component-names]
   status: complete
   last_updated: [YYYY-MM-DD]
   last_updated_by: [researcher name]
   ---

   # Research: [Topic]

   **Date**: [timestamp]
   **Researcher**: [name]
   **Git Commit**: [hash]
   **Branch**: [branch]
   **Repository**: [repo name]

   ## Research Question
   [Original query]

   ## Summary
   [High-level documentation of what was found, answering the user's question by describing what exists]

   ## Detailed Findings

   ### [Component/Area 1]
   - Description of what exists ([file.ext:line](link))
   - How it connects to other components
   - Current implementation details (without evaluation)

   ### [Component/Area 2]
   ...

   ## Code References
   - `path/to/file.py:123` - Description of what's there
   - `another/file.ts:45-67` - Description of the code block

   ## Architecture Documentation
   [Current patterns, conventions, and design implementations found in the codebase]

   ## Related Research
   [Links to other research documents in thoughts/shared/research/]

   ## Open Questions
   [Areas needing further investigation]
   ```

7. **Add GitHub permalinks (if applicable):**
   - Check if on main branch or if commit is pushed: `git branch --show-current` and `git status`
   - If on main/master or pushed, generate GitHub permalinks:
     - Get repo info: `gh repo view --json owner,name`
     - Create permalinks: `https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`
   - Replace local file references with permalinks in the document

8. **Present findings:**
   - Provide concise summary of findings to the user
   - Include key file references for easy navigation
   - Ask if they have follow-up questions or need clarification

9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter
   - Add a new section: `## Follow-up Research [timestamp]`
   - Spawn new sub-agents as needed for additional investigation

## Related Skills

- `rpi-plan` — Planning phase (run after research)
- `rpi-implement` — Execute an approved plan
- `rpi-iterate` — Update an existing plan based on feedback
