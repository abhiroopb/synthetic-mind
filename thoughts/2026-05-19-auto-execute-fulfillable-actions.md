# Auto-Execute Fulfillable Actions

## TL;DR

When you find yourself telling an AI assistant "make sure you do this next time" more than once, the rule did not actually stick. Memory alone is not enough. The pattern that works is: update the skill file AND its launcher, in the same change, so the behavior fires automatically on the next run. Memory is for recall. Skills and launchers are for behavior.

## Context

In any long-running AI setup, you accumulate small directives.

"Always include the cycle field in the audit."
"Open the weekly status tab on Mondays."
"Run the EOD wrap-up when I say close of day."

The natural reflex is to save these as memory observations. That feels right because the system has a memory layer that captures preferences across sessions.

But memory has a quiet failure mode.

Memory is a retrieval surface. It only fires if something in the current turn triggers a relevant query. If the agent does not query, the rule does not surface, and the behavior reverts to default.

Worse, some triggers are time-gated. A rule about Mondays only fires if the agent runs a Monday check. A rule about end-of-day only fires if the agent recognizes the EOD intent. If the rule lives only in memory, the gate is the agent's discretion, not the calendar.

So you end up restating the directive every few weeks.

## The pattern

Codify behavior in two places, not one.

### 1. The skill file

The skill file is the contract for what the workflow does. If you want the Blueprint audit to always include the cycle field, that rule belongs in the blueprint audit skill, not in memory. The next time the skill runs, the rule is in the loaded instructions automatically.

This is the durable layer.

### 2. The launcher

The launcher is whatever wires the skill to a trigger. A scheduled job. A startup hook. A chief-of-staff routine. A keyword in the chat input.

If you want the weekly status tab to open on Mondays, the Monday check belongs in the launcher, not in the skill. Otherwise the skill has to ask "is it Monday?" every single time, which costs a tool call and depends on the agent remembering to ask.

The launcher is the activation layer. It decides whether the skill runs at all.

### Why both

Skill alone: the rule applies, but only when the user manually invokes the skill.

Launcher alone: the workflow fires on schedule, but the agent has to re-derive the rule each time, and the rule is invisible if you read the skill directly.

Skill + launcher: the rule is encoded in the workflow definition, and the workflow runs without prompting.

## How to spot the failure

A clean test: if you have to remind the agent of the same directive more than twice in a quarter, you did not codify it. You wrote a memory note and walked away.

The directive is still floating in the retrieval layer, not the execution layer.

The fix is one edit each: the skill file, and the launcher that calls it. Not a longer memory note.

## What memory is still for

Memory is great for context that does not have a single destination.

Stakeholder preferences. Stories that explain a past decision. Compressed summaries of long sessions. Things you might query later but cannot pre-bind to a specific skill.

When memory is doing what it is good at, you do not need to remind the agent of anything. The rule already runs.
