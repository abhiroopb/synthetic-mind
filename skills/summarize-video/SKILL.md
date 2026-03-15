---
Skill name: summarize-video
Skill description: Summarize a video — extract transcript via Kaltura API, generate AI summary with key takeaways and timestamped quotes, and build styled HTML page. Requires Chrome DevTools MCP.
argument-hint: <video_url>
allowed-tools:
  - mcp__chrome-devtools__new_page
  - mcp__chrome-devtools__navigate_page
  - mcp__chrome-devtools__evaluate_script
  - mcp__chrome-devtools__take_snapshot
  - mcp__chrome-devtools__wait_for
  - mcp__chrome-devtools__click
  - mcp__chrome-devtools__list_pages
  - mcp__chrome-devtools__select_page
  - Bash(python3 {{SKILL_DIR}}/scripts/format_transcript.py:*)
  - Bash(python3 {{SKILL_DIR}}/scripts/build.py:*)
  - Bash(python3 -c:*)
  - Bash(pip3 install markdown:*)
  - Bash(mkdir:*)
  - Bash(whoami:*)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Summarize a Video

## Prerequisites

This skill requires Chrome DevTools MCP and the `markdown` Python package. See [SETUP.md](./SETUP.md) for installation instructions.

## Workflow

Given a video URL from a Kaltura-based video platform, perform the following steps.

## Step 1: Set up output directory

Create an output directory based on the video title slug (lowercase, hyphens):

```bash
mkdir -p <output_dir>
```

## Step 2: Extract the SRT caption file

1. Open the video URL in Chrome using chrome-devtools MCP (`new_page` with a 30s timeout — it may need SSO auth).
2. Once the page loads, extract the Kaltura session token and caption download URL by running this script in the browser via `evaluate_script`. **Important:** The `ks` token is a session credential — do not log it, persist it, or include it in any output.

```javascript
async () => {
  const player = window.KalturaPlayer.getPlayers()['kplayer'];
  const ks = player.config.provider.ks;
  const entryId = player.config.sources.id;

  // List caption assets
  const listResp = await fetch('https://www.kaltura.com/api_v3/service/caption_captionasset/action/list', {
    method: 'POST',
    body: new URLSearchParams({ ks, format: '1', 'filter[entryIdEqual]': entryId })
  });
  const listData = await listResp.json();
  if (!listData.objects?.length) return JSON.stringify({ error: 'No captions found' });

  const captionId = listData.objects[0].id;

  // Get download URL
  const urlResp = await fetch('https://www.kaltura.com/api_v3/service/caption_captionasset/action/getUrl', {
    method: 'POST',
    body: new URLSearchParams({ ks, format: '1', id: captionId })
  });
  const downloadUrl = await urlResp.json();

  // Fetch the actual SRT content
  const srtResp = await fetch(downloadUrl);
  const srt = await srtResp.text();
  return srt;
}
```

3. The SRT content may be too large for the response — it gets saved to a tool-results file. Extract it and save as a `.srt` file:

```python
import json
with open('<tool-results-file>') as f:
    data = json.load(f)
raw = data[0]['text']
# Content is inside a ```json "..." ``` block
import re
match = re.search(r'```json\n(.*?)\n```', raw, re.DOTALL)
if not match:
    raise ValueError("Could not find JSON block in tool-results file")
srt = json.loads(match.group(1))
with open('<output_dir>/video.srt', 'w') as f:
    f.write(srt)
```

## Step 3: Generate transcript.md

Run the format script. Use the video title from the page and the original URL:

```bash
python3 {{SKILL_DIR}}/scripts/format_transcript.py \
  <output_dir>/video.srt \
  "<video_url>" \
  --title "<Video Title>" \
  --interval 30 \
  -o <output_dir>/transcript.md
```

## Step 4: Write summary.md (use a subagent)

**Spawn a subagent** (Task tool, subagent_type="general-purpose") to read transcript.md and write summary.md. This keeps the main context clean, especially for long videos.

The subagent prompt should include:
- The path to transcript.md to read
- The output path for summary.md to write
- The video URL and title
- The full structure and rules below
- An explicit instruction that the subagent should **only** read the transcript file and write the summary file — no other file operations or tool use

The subagent should write `<output_dir>/summary.md` with this exact structure:

```markdown
# <Video Title>

> <Date> | [Watch Video](<video_url>)

*The takeaways and summary below are AI-generated from the transcript. Direct quotes are marked in italics with linked timestamps but have not been verified for accuracy. The [full verbatim transcript](#full-transcript) from the video's caption file is included below.*

## Key Takeaways

- **Takeaway 1.** 1-2 sentences with *"direct quotes"* and linked timestamps ([MM:SS](<video_url>?st=SECONDS)).
- **Takeaway 2.** 1-2 sentences with *"direct quotes"* and linked timestamps.
- **Takeaway 3.** 1-2 sentences with *"direct quotes"* and linked timestamps.

## Summary

### Section Title 1
[MM:SS](<video_url>?st=SECONDS) – [MM:SS](<video_url>?st=SECONDS)

Summary paragraph with *"direct quotes"* and linked timestamps like ([MM:SS](<video_url>?st=SECONDS)).

### Section Title 2
...
```

Rules:
- Max 3 takeaways — each should include direct quotes with linked timestamps, same style as the summary sections
- Use as many thematic sections as needed (3-5 for presentations, more for Q&As — e.g. one per question)
- Use direct quotes in italics with timestamp links
- Timestamp link format: `[MM:SS](<video_url>?st=TOTAL_SECONDS)`
- Do NOT modify any transcript content — summary.md is only AI-generated content
- The transcript is verbatim from the video's caption file and must never be edited

## Step 5: Build HTML and publish

```bash
pip3 install markdown==3.7 --break-system-packages -q
python3 {{SKILL_DIR}}/scripts/build.py <output_dir>/
```

The built HTML page will be in `<output_dir>/index.html`. Tell the user the output path so they can open it in a browser or publish it to their preferred hosting.
