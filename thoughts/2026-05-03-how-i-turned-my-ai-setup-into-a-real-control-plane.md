# How I Turned My AI Setup Into a Real Control Plane

## TL;DR

My AI setup got much better once I stopped treating it like a bag of prompts and started treating it like a control plane. The repo now owns the durable behavior, home-directory files stay thin and local, skills live in clear runtime tiers, and workstreams carry real state instead of making each session rediscover the world.

## Context

For a while, the system worked, but it still felt a little improvised.

There were good workflows. There were good skills. There were useful notes and solid routines.

But the ownership model was fuzzy.

Some behavior lived in the repo. Some lived in the home directory. Some lived in setup glue that had grown over time. If something drifted, it was not always obvious which surface was supposed to own the fix.

That is usually the point where AI setups start feeling clever and fragile at the same time.

The breakthrough was not another model upgrade.

It was deciding that the system needed a real control plane.

## The idea

The control-plane model is simple.

The repo owns the durable behavior. The home directory owns the local adapters. Runtime state stays separate from both.

That one framing cleared up a lot.

### 1. Put the real policy in the repo

The shared `AGENTS.md` became the canonical place for durable rules.

That includes things like:

- instruction precedence
- side-effect boundaries
- routing defaults
- workflow ownership
- writing and operating norms

The important part is not that everything lives in one file. It is that the file has a job.

If a rule should travel with the system, the repo owns it.

That keeps behavior versioned, reviewable, and explainable.

### 2. Keep home-directory files thin

Home-directory config still matters, but now it acts more like an adapter layer.

That layer handles local runtime concerns, machine-specific setup, and startup behavior that should not redefine the shared system.

Once I started treating those files as adapters instead of alternate sources of truth, the setup got calmer.

When something drifted, it was easier to answer a basic question:

Is this a repo behavior problem or a local runtime problem?

### 3. Split the skill runtime by job, not by habit

The skill library had grown big enough that the old model was doing too much in one place.

Now there are three clear layers:

- a shared runtime for broadly useful active skills
- a project-local runtime for repo-specific behavior
- an archive shelf for specialist skills that should stay out of the hot path until needed

That is the part that made the system feel operational instead of just organized.

The archive is not deletion. It is cold storage with a promotion path.

Specialists stay available without making every routing decision noisier.

### 4. Let routing promote specialists on demand

Once the archive existed, the router stopped needing the whole world in active memory.

The better pattern was:

1. keep the active runtime small
2. look for a fit in the archive when needed
3. promote the skill into the active set only when the policy says it is worth it

That preserves breadth without paying the tax all the time.

It also makes the system easier to tune. Promotion policy becomes a first-class control instead of an accidental side effect of dumping more files into the live runtime.

### 5. Treat workstreams as state, not decoration

The other half of a control plane is continuity.

Workstreams, `CONTEXT.md`, watched source snapshots, and lightweight state rebuilders matter because they make the system resumable. The terminal becomes a surface. The state lives in files.

That changes the feel of the whole setup.

Instead of asking, "what did the model remember," the better question becomes, "what state did the system preserve?"

That is a much healthier foundation.

## Why this feels different from a prompt stack

A prompt stack can be useful. A bag of skills can be useful. A set of scripts can be useful.

But a control plane does something more specific.

It tells you:

- what owns behavior
- what owns local adaptation
- what state is durable
- how specialists come into play
- where to fix drift when the system stops matching reality

That is the difference between a neat setup and an operating environment.

## What I learned

**Ownership beats cleverness.** A system gets sturdier once every important rule has a clear home.

**Adapters should stay thin.** Local files are useful when they connect the machine to the system, not when they quietly redefine it.

**A smaller hot path is a better default.** Archive-backed promotion beats keeping every specialist live all the time.

**State matters more than session history.** Workstreams, snapshots, and rebuilders make the setup feel reliable in a way chat transcripts never do.

**The real upgrade was architectural.** The models helped, but the step-change came from deciding what this system actually is.

---

*Related: [The File That Runs My Entire AI Setup](./2026-04-06-agents-md-reference.md), [Start, Sync, Close: The AI Work Loop I Actually Needed](./2026-04-21-start-sync-close-loop.md), and [How the AI PM OS Spins Up My Entire Workday](./2026-04-12-how-ai-pm-os-works.md).*

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
