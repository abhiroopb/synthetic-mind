# How the AI PM OS Spins Up My Entire Workday

## TL;DR

The AI PM OS starts with one shell command, opens a planning workspace, writes a launch plan, derives a lightweight state view, and then spins up the right workstreams in parallel. The trick is that every workspace resumes from its own `CONTEXT.md`, so the system can survive crashes, restarts, and long gaps without losing the thread.

## Context

Most AI workflows still assume a single chat window. That breaks down fast when your day includes planning, meetings, follow-ups, writing, research, and a few half-finished threads that all matter for different reasons.

I wanted a system that could answer a more practical question:

What should be open right now, and how does each thread pick up from where it left off?

## The startup command

Everything begins here:

```
start-day
```

In the public `ai-pm-os` repo, the `start-day` launcher does a small number of deliberate things:

1. validates prerequisites
2. boots or reuses `cmux`
3. opens the Chief of Staff workspace
4. waits for a valid `system/today-plan.json`
5. derives `system/state/queue.json` and `system/state/now.json`
6. opens the selected workstreams

That is the entire control loop.

## Step 1: the Chief of Staff plans the day

The first workspace is the planner, not the executor.

The Chief of Staff agent reads:

- recent notes
- routine context files
- workstream context files
- per-workstream config metadata

Then it writes `system/today-plan.json`.

That plan includes:

- which workstreams to open
- which ones to skip
- a startup prompt for each selected workstream
- a short summary of the day's focus

This separation is important. The planner decides what deserves attention. It does not try to finish all the work itself.

## Step 2: derive a quick state view

The public repo adds a small state-derivation step after the plan is written.

`system/scripts/build-state-from-plan.py` reads `today-plan.json` and produces two files:

- `queue.json`: the ranked list of recommended workstreams
- `now.json`: the current top recommendation plus a few fallbacks

That layer is intentionally lightweight. Internally I use a richer command-center model, but for the public repo I wanted something people could inspect instantly without inheriting a lot of extra machinery.

It's a good example of a design principle I keep coming back to: preserve the useful shape, remove the private complexity.

## Step 3: open workstreams in parallel

Once the plan exists, `start-day.sh` loops through the shortlisted workstreams and opens one `cmux` workspace per item.

Each workspace gets a startup prompt that points it back to its own folder and current objective. That means the agent is not starting from a blank slate. It is starting from a saved narrative state.

In practice, that state usually lives in two files:

- `workstreams/<slug>/CONTEXT.md`
- `workstreams/<slug>/config.yaml`

The config file gives the launcher metadata. The context file gives the agent continuity.

## Step 4: let the files, not the terminal, hold memory

This is the part that makes the whole system feel reliable.

If the terminal dies, nothing important is lost.

When the workspace opens again later, the agent reads `CONTEXT.md` and can answer questions like:

- what changed last time?
- what is still blocked?
- what decision is pending?
- what should happen next?

That turns the terminal into a temporary surface rather than the only place where state exists.

## Workstreams versus routines

Not everything in the system is a project.

Some folders are durable loops like:

- to-do review
- comms triage
- meeting prep
- scheduled maintenance

Those live as `routines/`, not `workstreams/`. They use the same continuity model, but they represent a different kind of job. That split prevents the system from treating infinite loops and finite deliverables as if they were the same thing.

## Why this feels better than tab chaos

A normal workday usually becomes accidental multitasking. Too many tabs, too many half-started notes, too many threads mixed into one place.

The AI PM OS works better because it makes the structure explicit:

- one planner
- multiple focused executors
- durable state per thread
- a ranking of what matters now

That is enough orchestration to feel intentional without becoming heavy.

## What I learned

**A launcher script can carry a lot of product value.** The shell glue is not glamorous, but it is what turns a pile of prompts into a reusable experience.

**Derived state is worth it when it improves inspectability.** `queue.json` and `now.json` are simple, but they make the system easier to reason about.

**Resume quality matters more than startup polish.** A beautiful launch flow is not enough if the second session is confusing.

**The public version got better when I simplified it.** The exported repo became more useful once I resisted the urge to ship every internal layer.

---

*Related: [I Built an AI PM OS](./2026-04-12-ai-pm-os.md) and [Why the AI PM OS Feels More Powerful Than a Chatbot](./2026-04-12-why-ai-pm-os-is-powerful.md).*

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
