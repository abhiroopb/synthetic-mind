# Piping Slack DMs to Amp (So I Can Use My Agent from My Phone)

## TL;DR

I built a Slack bot that pipes DMs to Amp. Send a message in Slack, it runs `amp -x "your message"` on my Mac, and replies in the same thread. Works from my phone, my iPad, anywhere. Node.js, Slack Bolt SDK, Socket Mode. About 80 lines of code that matter. The catch: it only works while my laptop is awake — cloud hosting is the next step.

## Context

Amp is incredible on my laptop. But I'm not always at my laptop. I'm in meetings, walking to get coffee, sitting on my couch. I kept wanting to ask Amp quick questions — "what's the status of that PR?", "search my memory for the cash rounding flag name", "check my calendar tomorrow" — and couldn't.

The fix seemed obvious: pipe Slack DMs to Amp. I already live in Slack on my phone. If I could DM a bot and have it run Amp commands, I'd have my agent in my pocket.

## The Build

### Stack

- **Node.js** with the Slack Bolt SDK
- **Socket Mode** — no public URL needed, no ngrok, no webhooks
- Amp's `-x` flag for non-interactive execution
- `--continue` with thread IDs for multi-turn conversations

### The core idea

Slack messages come in → spawn `amp -x "message"` → capture stdout → reply in the same Slack thread. Map Slack threads to Amp threads so follow-up messages continue the same conversation.

Here's the `runAmp` function that does the heavy lifting:

```javascript
function runAmp(message, ampThreadId = null) {
  return new Promise((resolve, reject) => {
    const args = ['-x', message, '--dangerously-allow-all'];
    if (ampThreadId) {
      args.push('--continue', ampThreadId);
    }

    const child = spawn('amp', args, {
      env: { ...process.env, HOME: os.homedir() },
      shell: true,
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => { stderr += data.toString(); });

    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`amp exited with code ${code}: ${stderr}`));
      } else {
        // Extract thread ID from stderr (amp prints it there)
        const threadMatch = stderr.match(/thread[:\s]+([A-Za-z0-9-]+)/i);
        resolve({
          output: stdout.trim(),
          threadId: threadMatch ? threadMatch[1] : ampThreadId,
        });
      }
    });
  });
}
```

And the message handler that ties it all together:

```javascript
const threadMap = new Map(); // Slack thread_ts → Amp thread ID

app.event('message', async ({ event, say }) => {
  // Only respond to DMs from me
  if (event.channel_type !== 'im') return;
  if (event.user !== ALLOWED_USER_ID) return;
  if (event.subtype) return; // Skip edits, joins, etc.

  const slackThread = event.thread_ts || event.ts;
  const ampThreadId = threadMap.get(slackThread) || null;

  try {
    // Show typing indicator
    await say({ text: '⏳ Running...', thread_ts: slackThread });

    const result = await runAmp(event.text, ampThreadId);

    // Store thread mapping for follow-ups
    if (result.threadId) {
      threadMap.set(slackThread, result.threadId);
    }

    // Reply in thread
    await say({
      text: result.output || '✅ Done (no output)',
      thread_ts: slackThread,
    });
  } catch (error) {
    await say({
      text: `❌ Error: ${error.message}`,
      thread_ts: slackThread,
    });
  }
});
```

### Thread mapping

This is the part that makes it feel like a real conversation, not just one-off commands. Slack threads have a `thread_ts` identifier. Amp threads have their own IDs. The `threadMap` bridges them — first message in a Slack thread creates a new Amp thread, follow-ups continue it with `--continue`.

### Security

Simple but important: `ALLOWED_USER_ID` check. Only my Slack user ID can trigger commands. Everyone else gets ignored. The bot only listens to DMs anyway, but defense in depth.

### The `--dangerously-allow-all` flag

Yeah, the name is scary. But think about what this bot does — it runs arbitrary commands on my machine via Slack. The whole point is remote execution. I need Amp to be able to use all its tools (file edits, shell commands, MCP servers) without prompting for confirmation. There's no human sitting at a terminal to click "yes." The security boundary is the `ALLOWED_USER_ID` check, not Amp's permission system.

## The Pivot

Here's what I didn't think about: this runs on my Mac. Socket Mode connects to Slack's API via a websocket from my machine. So when my laptop goes to sleep... the bot goes to sleep.

I built this imagining I'd use it from my phone while away from my desk. But "away from my desk" often means "laptop lid closed." Which means the bot is dead.

The fix is obvious in retrospect: run this on a server. A small VM, a Raspberry Pi, a container somewhere. But then you need Amp installed there, with all the MCP servers, credentials, and config. That's a bigger project.

For now, it works great when my laptop is open but I'm just not at it — meetings, couch, kitchen. Still useful. But cloud hosting is the real unlock.

## What I Learned

1. **`amp -x` is the killer feature for integrations.** Non-interactive execution turns Amp from a terminal tool into an API. Anything that can spawn a process can use Amp now.

2. **Thread continuity matters more than I expected.** Without `--continue`, every message is a cold start. With it, follow-up questions just work — "what about the iOS version?" after asking about a PR makes sense because Amp remembers the context.

3. **Socket Mode is criminally underrated.** No public URL, no SSL cert, no ngrok. Just `npm start` and you're connected. Perfect for personal bots.

4. **The laptop-must-be-awake constraint is the real limitation.** Everything else works. The architecture is sound. The UX is good. But it's tethered to my Mac being on. Cloud hosting would make this genuinely useful 24/7.

5. **80 lines of code can be transformative.** This isn't a complex system. It's a bridge — Slack on one side, Amp on the other, a thin layer of thread mapping in between. Sometimes the best tools are just good plumbing.

---

*Built with Amp. Tested by DM-ing myself from the bathroom.*
