#!/usr/bin/env python3
"""Build styled HTML page from summary.md and transcript.md.

Usage: python3 build.py <directory> [--video-url URL]

The directory must contain summary.md and transcript.md.
Outputs index.html in the same directory.
"""

import argparse
import html
import markdown
import os
import re


def _js_escape(s):
    """Escape a string for safe embedding in a JS single-quoted string literal."""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("<", "\\u003c").replace("\n", "\\n")


def _build_chat_widget(video_url):
    """Generate the AI chat widget HTML/CSS/JS for embedding in video summary pages."""
    video_url = _js_escape(video_url)
    return f"""
<style>
  .chat-fab {{
    position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 1000;
    width: 52px; height: 52px; border-radius: 50%; border: none;
    background: var(--accent); color: #fff; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25); transition: transform 0.2s;
  }}
  .chat-fab:hover {{ transform: scale(1.08); }}
  .chat-fab.open .chat-fab-icon {{ display: none; }}
  .chat-fab.open::after {{ content: '\\00d7'; font-size: 1.6rem; line-height: 1; }}
  .chat-fab-icon {{ font-size: 1.5rem; line-height: 1; }}

  .chat-panel {{
    position: fixed; bottom: 5.5rem; right: 1.5rem; z-index: 999;
    width: 420px; max-width: calc(100vw - 2rem); height: 520px; max-height: calc(100vh - 7rem);
    background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2); display: none; flex-direction: column;
    overflow: hidden; transition: all 0.25s ease;
  }}
  .chat-panel.open {{ display: flex; }}
  .chat-panel.expanded {{
    width: 680px; height: calc(100vh - 7rem);
    max-width: calc(100vw - 2rem);
  }}

  .chat-header {{
    padding: 0.6rem 0.75rem; border-bottom: 1px solid var(--border);
    font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;
    background: var(--card-bg); flex-shrink: 0;
  }}
  .chat-header .title {{ flex: 1; }}
  .chat-header .header-btn {{
    background: none; border: none; color: var(--muted); cursor: pointer;
    padding: 0.2rem; border-radius: 4px; display: flex; align-items: center;
  }}
  .chat-header .header-btn:hover {{ color: var(--text); background: var(--border); }}
  .chat-header .header-btn svg {{ width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}

  .chat-messages {{
    flex: 1; overflow-y: auto; padding: 0.75rem; display: flex; flex-direction: column; gap: 0.6rem;
  }}

  .chat-msg {{ max-width: 92%; padding: 0.5rem 0.75rem; border-radius: 12px; font-size: 0.85rem; line-height: 1.55; word-wrap: break-word; }}
  .chat-msg.user {{ align-self: flex-end; background: var(--accent); color: #fff; border-bottom-right-radius: 4px; }}
  .chat-msg.ai {{ align-self: flex-start; background: var(--card-bg); border: 1px solid var(--border); border-bottom-left-radius: 4px; }}
  .chat-msg.ai p {{ margin: 0 0 0.4rem 0; }}
  .chat-msg.ai p:last-child {{ margin-bottom: 0; }}
  .chat-msg.ai strong {{ font-weight: 600; }}
  .chat-msg.ai em {{ background: var(--highlight); padding: 0.05em 0.2em; border-radius: 2px; }}
  .chat-msg.ai a {{ color: var(--accent); font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.82em; font-weight: 600; }}
  .chat-msg.ai ul {{ margin: 0.2rem 0 0.4rem 1rem; padding: 0; }}
  .chat-msg.ai li {{ margin-bottom: 0.3rem; }}
  .chat-msg.system {{ align-self: center; background: transparent; color: var(--muted); font-size: 0.78rem; font-style: italic; text-align: center; padding: 0.2rem; }}
  .chat-msg.error {{ align-self: center; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; font-size: 0.8rem; text-align: center; }}
  @media (prefers-color-scheme: dark) {{
    .chat-msg.error {{ background: #450a0a; color: #fca5a5; border-color: #7f1d1d; }}
  }}

  .chat-typing {{ display: inline-flex; gap: 4px; padding: 0.5rem 0.75rem; }}
  .chat-typing span {{ width: 5px; height: 5px; background: var(--muted); border-radius: 50%; animation: chatBounce 1.2s infinite; }}
  .chat-typing span:nth-child(2) {{ animation-delay: 0.2s; }}
  .chat-typing span:nth-child(3) {{ animation-delay: 0.4s; }}
  @keyframes chatBounce {{ 0%,60%,100% {{ transform: translateY(0); }} 30% {{ transform: translateY(-4px); }} }}

  .chat-input-row {{
    padding: 0.6rem; border-top: 1px solid var(--border); display: flex; gap: 0.4rem;
    background: var(--card-bg); flex-shrink: 0;
  }}
  .chat-input-row input {{
    flex: 1; padding: 0.45rem 0.65rem; border: 1px solid var(--border); border-radius: 8px;
    background: var(--bg); color: var(--text); font-size: 0.85rem; outline: none;
  }}
  .chat-input-row input:focus {{ border-color: var(--accent); }}
  .chat-input-row button {{
    padding: 0.45rem 0.85rem; border: none; border-radius: 8px;
    background: var(--accent); color: #fff; font-size: 0.85rem; font-weight: 600;
    cursor: pointer;
  }}
  .chat-input-row button:disabled {{ opacity: 0.5; cursor: not-allowed; }}

  .chat-selection-tooltip {{
    position: absolute; z-index: 1001; display: none;
    background: var(--accent); color: #fff; font-size: 0.75rem; font-weight: 500;
    padding: 0.4rem 0.7rem 0.4rem 0.55rem; border-radius: 8px; cursor: pointer;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25); white-space: nowrap;
    transform: translateX(-50%);
    animation: chatTooltipFadeIn 0.15s ease;
    display: none; align-items: center; gap: 0.35rem;
    letter-spacing: 0.01em;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }}
  .chat-selection-tooltip svg {{
    width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0;
  }}
  .chat-selection-tooltip::after {{
    content: ''; position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
    border: 5px solid transparent; border-top-color: var(--accent);
  }}
  .chat-selection-tooltip:hover {{ filter: brightness(1.1); }}
  .chat-selection-tooltip:active {{ transform: translateX(-50%) scale(0.97); }}
  @keyframes chatTooltipFadeIn {{ from {{ opacity: 0; transform: translateX(-50%) translateY(4px); }} to {{ opacity: 1; transform: translateX(-50%) translateY(0); }} }}
</style>

<button class="chat-fab" id="chatFab" title="Ask AI about this video">
  <span class="chat-fab-icon">💬</span>
</button>

<div class="chat-panel" id="chatPanel">
  <div class="chat-header">
    <span class="title">Ask AI about this video <span style="font-weight:400;color:var(--muted);font-size:0.78em">(gpt-5.2)</span></span>
    <button class="header-btn" id="chatClear" title="New chat">
      <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 1 3 6.7"/><path d="M3 22v-6h6"/></svg>
    </button>
    <button class="header-btn" id="chatExpand" title="Expand">
      <svg viewBox="0 0 24 24"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
    </button>
  </div>
  <div class="chat-messages" id="chatMessages">
    <div class="chat-msg system">Ask anything about this video. Answers are AI-generated from the transcript and may not be perfectly accurate.</div>
  </div>
  <div class="chat-input-row">
    <input type="text" id="chatInput" placeholder="Ask a question..." autocomplete="off" />
    <button id="chatSend">Send</button>
  </div>
</div>

<div class="chat-selection-tooltip" id="chatSelectionTooltip">
  <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  Chat about this
</div>

<script>
(function() {{
  var API_URL = 'https://qai.sqprod.co/openai/v1/chat/completions';
  var MODEL = 'gpt-5.2';
  var VIDEO_URL = '{video_url}';
  var fab = document.getElementById('chatFab');
  var panel = document.getElementById('chatPanel');
  var expandBtn = document.getElementById('chatExpand');
  var clearBtn = document.getElementById('chatClear');
  var messagesEl = document.getElementById('chatMessages');
  var inputEl = document.getElementById('chatInput');
  var sendBtn = document.getElementById('chatSend');
  var conversationHistory = [];
  var systemPrompt = null;
  var sending = false;
  var defaultMsg = '<div class="chat-msg system">Ask anything about this video. Answers are AI-generated from the transcript and may not be perfectly accurate.</div>';

  fab.addEventListener('click', function() {{
    var isOpen = panel.classList.toggle('open');
    fab.classList.toggle('open', isOpen);
    if (isOpen && !systemPrompt) systemPrompt = buildSystemPrompt();
    if (isOpen) inputEl.focus();
  }});

  expandBtn.addEventListener('click', function() {{
    panel.classList.toggle('expanded');
  }});

  clearBtn.addEventListener('click', function() {{
    conversationHistory = [];
    messagesEl.innerHTML = defaultMsg;
    inputEl.focus();
  }});

  function buildSystemPrompt() {{
    // Gather full page content: summary (TOC + body) and transcript
    var summaryDiv = document.querySelector('.summary');
    var summaryText = summaryDiv ? summaryDiv.innerText : '';

    var tocNav = document.querySelector('.toc');
    var tocText = tocNav ? tocNav.innerText : '';

    var transcriptDiv = document.querySelector('.transcript');
    var transcriptText = transcriptDiv ? transcriptDiv.innerText : '';

    return 'You are an AI assistant that answers questions about a video based on its full content below.\\n' +
      'Use ONLY the content below to answer. If the answer is not covered, say so.\\n' +
      'Heavily lean on direct quotes from the transcript. For every claim, include the speaker\\'s exact words.\\n' +
      'Wrap direct quotes in single asterisks for emphasis: *"exact words from the video"*\\n' +
      'Always include timestamps as markdown links: [MM:SS](' + VIDEO_URL + '?st=TOTAL_SECONDS) where TOTAL_SECONDS = minutes*60 + seconds.\\n' +
      'IMPORTANT: Only apply quote formatting and timestamp links for content from the video. For conversational questions (greetings, questions about previous messages, etc.), respond normally without quotes or timestamps.\\n' +
      'Keep answers concise (2-4 paragraphs). Use **bold** for key points, *"italics"* for direct quotes, and - for bullet lists.\\n\\n' +
      'TABLE OF CONTENTS:\\n' + tocText + '\\n\\n' +
      'SUMMARY:\\n' + summaryText + '\\n\\n' +
      'TRANSCRIPT:\\n' + transcriptText;
  }}

  function renderMarkdown(text) {{
    // Convert bare [MM:SS] timestamps to video links
    text = text.replace(/\\[(\\d{{1,2}}):(\\d{{2}})\\](?!\\()/g, function(_, m, s) {{
      var secs = parseInt(m)*60 + parseInt(s);
      return '[' + m + ':' + s + '](' + VIDEO_URL + '?st=' + secs + ')';
    }});
    // Convert (MM:SS) timestamps too
    text = text.replace(/\\((\\d{{1,2}}):(\\d{{2}})\\)(?!\\])/g, function(_, m, s) {{
      var secs = parseInt(m)*60 + parseInt(s);
      return '([' + m + ':' + s + '](' + VIDEO_URL + '?st=' + secs + '))';
    }});

    var blocks = text.split(/\\n\\n+/);
    var htmlBlocks = blocks.map(function(block) {{
      var lines = block.split('\\n');
      if (lines.every(function(l) {{ return /^\\s*[-*]\\s/.test(l) || l.trim() === ''; }})) {{
        var items = lines.filter(function(l) {{ return /^\\s*[-*]\\s/.test(l); }}).map(function(l) {{
          return '<li>' + inlineFmt(l.replace(/^\\s*[-*]\\s+/, '')) + '</li>';
        }});
        return '<ul>' + items.join('') + '</ul>';
      }}
      return '<p>' + inlineFmt(block.replace(/\\n/g, '<br>')) + '</p>';
    }});
    return htmlBlocks.join('');
  }}

  function escapeHtml(str) {{
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }}

  function inlineFmt(text) {{
    text = escapeHtml(text);
    return text
      .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
      .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
      .replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  }}

  function addMsg(role, html) {{
    var div = document.createElement('div');
    div.className = 'chat-msg ' + role;
    div.innerHTML = html;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return div;
  }}

  function sendMessage() {{
    var text = inputEl.value.trim();
    if (!text || sending) return;
    sending = true;
    sendBtn.disabled = true;
    inputEl.value = '';

    addMsg('user', escapeHtml(text));
    conversationHistory.push({{ role: 'user', content: text }});

    var typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg ai chat-typing';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    messagesEl.appendChild(typingDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    var body = {{
      model: MODEL,
      messages: [{{ role: 'system', content: systemPrompt }}].concat(conversationHistory),
      stream: true,
      max_completion_tokens: 2048,
      temperature: 0.3
    }};

    fetch(API_URL, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(body)
    }}).then(function(resp) {{
      if (!resp.ok) {{
        return resp.text().then(function(errBody) {{
          var errMsg = resp.statusText;
          try {{ errMsg = JSON.parse(errBody).error.message || errMsg; }} catch(e) {{}}
          throw new Error('API returned ' + resp.status + ': ' + errMsg);
        }});
      }}
      typingDiv.remove();
      var aiDiv = addMsg('ai', '');
      var fullText = '';
      var reader = resp.body.getReader();
      var decoder = new TextDecoder();
      var buffer = '';

      function pump() {{
        return reader.read().then(function(result) {{
          if (result.done) {{
            conversationHistory.push({{ role: 'assistant', content: fullText }});
            sending = false;
            sendBtn.disabled = false;
            inputEl.focus();
            return;
          }}
          buffer += decoder.decode(result.value, {{ stream: true }});
          var lines = buffer.split('\\n');
          buffer = lines.pop();
          for (var i = 0; i < lines.length; i++) {{
            if (lines[i].indexOf('data: ') !== 0) continue;
            var data = lines[i].slice(6);
            if (data === '[DONE]') continue;
            try {{
              var parsed = JSON.parse(data);
              var delta = parsed.choices && parsed.choices[0] && parsed.choices[0].delta && parsed.choices[0].delta.content;
              if (delta) {{
                fullText += delta;
                aiDiv.innerHTML = renderMarkdown(fullText);
                messagesEl.scrollTop = messagesEl.scrollHeight;
              }}
            }} catch(e) {{}}
          }}
          return pump();
        }});
      }}
      return pump();
    }}).catch(function(err) {{
      typingDiv.remove();
      addMsg('error', 'Error: ' + escapeHtml(String(err.message)));
      sending = false;
      sendBtn.disabled = false;
      inputEl.focus();
    }});
  }}

  sendBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('keydown', function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); sendMessage(); }}
  }});

  // Text selection tooltip
  var tooltip = document.getElementById('chatSelectionTooltip');
  var selectedText = '';

  document.addEventListener('mouseup', function(e) {{
    // Ignore selections inside the chat panel
    if (panel.contains(e.target) || fab.contains(e.target) || tooltip.contains(e.target)) return;

    var sel = window.getSelection();
    var text = sel.toString().trim();
    if (text.length < 5) {{
      tooltip.style.display = 'none';
      return;
    }}
    selectedText = text;

    var range = sel.getRangeAt(0);
    var rect = range.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2 + window.scrollX) + 'px';
    tooltip.style.top = (rect.top + window.scrollY - 40) + 'px';
    tooltip.style.display = 'flex';
  }});

  document.addEventListener('mousedown', function(e) {{
    if (!tooltip.contains(e.target)) {{
      tooltip.style.display = 'none';
    }}
  }});

  tooltip.addEventListener('click', function() {{
    tooltip.style.display = 'none';

    // Always start a fresh chat
    conversationHistory = [];
    messagesEl.innerHTML = defaultMsg;

    // Open chat if not open
    if (!panel.classList.contains('open')) {{
      panel.classList.add('open');
      fab.classList.add('open');
    }}
    if (!systemPrompt) systemPrompt = buildSystemPrompt();

    // Truncate selection for display
    var display = selectedText.length > 300 ? selectedText.slice(0, 300) + '...' : selectedText;

    // Show quoted excerpt in chat
    var quoteDiv = document.createElement('div');
    quoteDiv.className = 'chat-msg system';
    quoteDiv.style.cssText = 'background: var(--card-bg); border-left: 3px solid var(--accent); border-radius: 4px; font-style: normal; font-size: 0.8rem; max-width: 95%; align-self: stretch; padding: 0.5rem 0.75rem; text-align: left; color: var(--text);';
    quoteDiv.textContent = display;
    messagesEl.appendChild(quoteDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    // Pre-fill context into conversation
    conversationHistory.push({{ role: 'user', content: 'Regarding this excerpt from the video: "' + selectedText + '"\\n\\nPlease explain or elaborate on this.' }});

    inputEl.placeholder = 'Ask a follow-up or press Send...';
    inputEl.value = 'Explain this part of the video.';
    inputEl.focus();
    inputEl.select();

    window.getSelection().removeAllRanges();
  }});
}})();
</script>
"""


def build(directory, video_url=None):
    with open(os.path.join(directory, "summary.md")) as f:
        summary_md = f.read()

    with open(os.path.join(directory, "transcript.md")) as f:
        transcript_md = f.read()

    # Skip the transcript header (title, blank, quote, blank, ---)
    transcript_lines = transcript_md.split("\n")
    transcript_body = "\n".join(transcript_lines[5:])

    # Split summary into header (title + quote + disclaimer) and body
    summary_parts = summary_md.split("## Key Takeaways", 1)
    header_md = summary_parts[0]
    body_md = "## Key Takeaways" + summary_parts[1] if len(summary_parts) > 1 else ""

    # Extract page title from the first markdown heading
    title_match = re.match(r'#\s+(.+)', header_md.strip())
    page_title = title_match.group(1).strip() if title_match else "Video Summary"

    header_html = markdown.markdown(header_md, extensions=["extra"])

    md_toc = markdown.Markdown(extensions=["extra", "toc"])
    body_html = md_toc.convert(body_md)
    transcript_html = markdown.markdown(transcript_body, extensions=["extra"])

    # Build TOC dynamically from rendered heading IDs
    headings = re.findall(r'<(h[23])[^>]*id="([^"]+)"[^>]*>(.*?)</\1>', body_html)

    ai_label = '<span class="toc-label ai">AI-generated</span>'
    verbatim_label = '<span class="toc-label verbatim">Verbatim from video</span>'

    toc_lines = []
    in_sublist = False
    for tag, hid, text in headings:
        clean = re.sub(r'<[^>]+>', '', text)
        if tag == 'h2':
            if in_sublist:
                toc_lines.append('      </ol>')
                toc_lines.append('    </li>')
                in_sublist = False
            elif toc_lines:
                toc_lines.append('    </li>')
            toc_lines.append(f'    <li><a href="#{hid}">{clean}</a> {ai_label}')
        elif tag == 'h3':
            if not in_sublist:
                toc_lines.append('      <ol>')
                in_sublist = True
            toc_lines.append(f'        <li><a href="#{hid}">{clean}</a></li>')

    if in_sublist:
        toc_lines.append('      </ol>')
        toc_lines.append('    </li>')
    elif toc_lines:
        toc_lines.append('    </li>')

    toc_lines.append(f'    <li><a href="#full-transcript">Full Transcript</a> {verbatim_label}</li>')
    toc_html = '\n'.join(toc_lines)

    # Detect video URL from transcript if not provided
    if not video_url:
        url_match = re.search(r'href="(https://video\.square\.com/[^"?]+)"', header_html)
        if url_match:
            video_url = url_match.group(1)
        else:
            video_url = "#"

    chat_widget = _build_chat_widget(video_url)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<title>{html.escape(page_title)}</title>
<style>
  :root {{
    --bg: #ffffff;
    --text: #1a1a1a;
    --muted: #6b7280;
    --accent: #2563eb;
    --border: #e5e7eb;
    --card-bg: #f9fafb;
    --highlight: #eff6ff;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #111827;
      --text: #f3f4f6;
      --muted: #9ca3af;
      --accent: #60a5fa;
      --border: #374151;
      --card-bg: #1f2937;
      --highlight: #1e3a5f;
    }}
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    max-width: 780px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }}
  h1 {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem; }}
  h2 {{
    font-size: 1.35rem; font-weight: 600;
    margin-top: 2.5rem; margin-bottom: 1rem;
    padding-bottom: 0.5rem; border-bottom: 2px solid var(--border);
  }}
  h3 {{ font-size: 1.1rem; font-weight: 600; margin-top: 1.75rem; margin-bottom: 0.5rem; }}
  p {{ margin-bottom: 1rem; }}
  blockquote {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  ul {{ margin-bottom: 1.25rem; padding-left: 1.25rem; }}
  li {{ margin-bottom: 0.75rem; }}
  em {{ background: var(--highlight); padding: 0.1em 0.3em; border-radius: 3px; font-style: italic; }}
  hr {{ border: none; border-top: 2px solid var(--border); margin: 2.5rem 0; }}
  .transcript {{ font-size: 0.92rem; color: var(--muted); }}
  .transcript p {{ margin-bottom: 1.25rem; }}
  .transcript strong a {{
    color: var(--accent); font-weight: 600; font-size: 0.85rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
  }}
  .source-note {{ font-size: 0.85rem; color: var(--muted); font-style: italic; margin-bottom: 1.5rem; }}
  .toc {{
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem 1.25rem; margin-top: 2rem;
  }}
  .toc strong {{ font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }}
  .toc ol {{ margin: 0.5rem 0 0 1.25rem; padding: 0; }}
  .toc li {{ margin-bottom: 0.3rem; font-size: 0.92rem; }}
  .toc ol ol {{ margin-top: 0.3rem; }}
  .toc-label {{
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.04em; padding: 0.15em 0.5em; border-radius: 999px;
    vertical-align: middle; margin-left: 0.35rem;
  }}
  .toc-label.ai {{ background: #fef3c7; color: #92400e; }}
  .toc-label.verbatim {{ background: #d1fae5; color: #065f46; }}
  @media (prefers-color-scheme: dark) {{
    .toc-label.ai {{ background: #78350f; color: #fde68a; }}
    .toc-label.verbatim {{ background: #064e3b; color: #6ee7b7; }}
  }}
</style>
</head>
<body>

<div class="header">
{header_html}
</div>

<nav class="toc">
  <strong>Contents</strong>
  <ol>
{toc_html}
  </ol>
</nav>

<div class="summary">
{body_html}
</div>

<hr>

<h2 id="full-transcript">Full Transcript</h2>
<p class="source-note">Verbatim captions extracted directly from the <a href="{video_url}">video file</a>. Not AI-generated or edited.</p>
<div class="transcript">
{transcript_html}
</div>

{chat_widget}
</body>
</html>
"""

    # Make video.square.com links open in a new tab
    html = re.sub(
        r'<a href="(https://video\.square\.com/[^"]*)"',
        r'<a href="\1" target="_blank" rel="noopener"',
        html,
    )

    out_path = os.path.join(directory, "index.html")
    with open(out_path, "w") as f:
        f.write(html)

    print(f"Built {out_path} ({len(html)} bytes)")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Build HTML from summary.md + transcript.md")
    parser.add_argument("directory", help="Directory containing summary.md and transcript.md")
    parser.add_argument("--video-url", default=None, help="Video URL (auto-detected from summary if omitted)")
    args = parser.parse_args()
    build(args.directory, args.video_url)


if __name__ == "__main__":
    main()
