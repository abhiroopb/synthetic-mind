# The Prepare-Then-Approve Pattern

## TL;DR

One of the most useful AI workflow patterns is simple: prepare the action completely, then ask for approval before the side effect happens. That means gathering context, checking claims against bounded sources, drafting the exact follow-through, and only then asking whether to send, post, file, or update. It keeps the agent useful without making it reckless.

## Context

A lot of AI agent demos collapse two different jobs into one move.

They gather context and take action at the same time.

That can look impressive. It can also create the wrong kind of confidence.

In real work, plenty of actions are easy to draft and expensive to do wrong:

- replying to a legal question
- posting a status update
- filing something into a system of record
- editing a shared doc that other people are already using

The issue is not just safety theater. It is decision quality.

If the agent acts too early, you lose the moment where a human can inspect the assumptions, the tone, and the evidence before the system commits to something public.

The pattern that held up better for me was a stricter split between preparation and approval.

## The idea

The agent should do as much of the thinking and prep work as possible before it asks for a decision.

That usually means four steps.

### 1. Pull the dropped artifact into context

When someone drops a link, thread, email, or ticket into chat, the first job is not to answer yet.

The first job is to understand what the artifact is really asking for.

That can mean pulling the surrounding Slack thread, the referenced doc, the linked issue, or the prior decision history.

The point is to reconstruct the task, not just react to the URL.

### 2. Corroborate inside a bounded lane

This is the part I care about most.

The agent should check the claim, but not wander forever.

Bounded corroboration means choosing a small, relevant set of sources that can confirm or challenge the current draft. Enough to reduce obvious errors. Not so much that the system turns into a vague research spiral.

For a legal-style reply, that might mean:

- the original message
- the referenced policy or license terms
- one or two direct supporting sources

Not twenty tabs. Not speculative internet archaeology. Just enough to make the draft honest.

### 3. Build the exact follow-through

Once the agent has the context, it should prepare the real action.

Not a vague summary. The actual thing.

That might be:

- the reply message
- the Jira comment
- the Blueprint record fields
- the proposed Slack post
- the change to a shared document

This is what makes the pattern useful. The user is not approving a plan to go do more work later. They are approving the ready-to-send artifact.

### 4. Pause at the boundary

Only after the draft is concrete should the system ask for approval.

That pause matters because it creates a clean review surface.

The human can challenge the assumptions, edit the tone, or decide the action should not happen at all.

The agent has already done the hard part. The user keeps the final say over the side effect.

## A non-proprietary example

One recent case made this feel especially clear.

The incoming task was a legal-style question about whether a licensed marketing image could be cropped and annotated for a blog post. The useful version of the workflow was not to answer instantly. It was to prepare carefully.

The bounded source bundle was small on purpose:

- the original request
- the license terms for the image source
- one supporting help page clarifying modification rights

The better sequence looked like this:

1. read the question and the linked context
2. check the relevant license language directly
3. draft a response grounded in that exact language
4. present the message for approval before sending anything

That kept the workflow fast, but it also kept it inspectable.

The human decision happened at the right place, after the evidence and the draft existed, not before.

The prepared draft looked more like this than a vague summary:

> The license allows modification, so cropping and light annotation are fine as long as the other license terms still hold. The safer answer is yes, with the note that we should keep attribution and reuse conditions aligned with the original source.

That is the pattern in miniature: gather, verify, draft the actual answer, then pause.

## Why this pattern scales

The reason this keeps showing up is that many agent tasks are not pure execution and not pure brainstorming.

They live in the middle.

You want the agent to:

- gather context
- reduce the research burden
- draft the real next step

But you still want a human checkpoint before anything external changes.

That middle lane is where prepare-then-approve shines.

It is fast enough to feel agentic, but controlled enough to trust.

## What I learned

**Approval works better after the draft exists.** People make better calls when they are reviewing the real artifact, not an abstract plan.

**Corroboration should be bounded.** Enough evidence helps. Endless checking just hides uncertainty behind motion.

**Side effects need a clean boundary.** Drafting and deciding are different jobs. Treating them separately improves both.

**The best safety pattern is still useful.** If the workflow feels slower or more annoying than doing it manually, it will not survive.

**A lot of agent design is really review-surface design.** The quality of the handoff before the action matters almost as much as the action itself.

---

*Related: [How I Turned My AI Setup Into a Real Control Plane](./2026-05-03-how-i-turned-my-ai-setup-into-a-real-control-plane.md) and [I Stopped Telling My Agent Which Tool to Use](./2026-04-06-auto-pilot-skill.md).*

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
