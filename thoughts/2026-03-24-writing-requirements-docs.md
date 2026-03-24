# We Built an AI Skill That Writes Product Requirements Docs

## TL;DR

Over five weeks, a small team went from "we should put our specs in markdown" to a fully working AI skill that guides PMs through writing structured product requirements — complete with auto-referenced internal data sources, co-located prototypes, and a sub-one-hour first draft. The key insight: PRDs aren't special documents. They're structured markdown that an agent can scaffold, research, and assemble faster than any PM can from scratch.

## Context

Every PM I know has the same complaint about product specs: they take forever to write, they're always slightly different formats, they live in Google Docs where they rot, and nobody reads them until something goes wrong.

In early February 2026, a few of us decided to try something different. What if product specs were markdown files in a Git repo? What if they lived alongside prototypes? And what if an AI agent could do 80% of the scaffolding work?

The idea started simple: stand up a repo with a clear folder structure — `requirements/`, `architecture/`, `releases/`, `prototypes/` — and write specs in markdown. Version-controlled. Reviewable via PR. Searchable. No more Google Docs graveyards.

But the real unlock came when a teammate built an agent skill to automate the writing process itself.

## The Idea

### Week 1: Structure first

The repo went up with a markdown-first philosophy. Product areas got their own scopes — payments, point-of-sale, retail, and so on. Each area had the same folder structure:

```
payments-checkout/
  requirements/
  architecture/
  releases/
  prototypes/
```

Clean, predictable, boring in the best way. Any PM could find any spec by navigating the folder tree. No search required.

### Week 2: The skill

A teammate built the `writing-requirements-docs` skill — an agent module that guides a PM through creating a structured PRD. It came with a `GUIDE.md` that defined the exact sections every requirements doc should have:

- Problem statement
- User stories
- Success metrics
- Requirements (functional and non-functional)
- Open questions
- Dependencies

The skill doesn't just create a template and leave you alone. It walks you through each section, asks clarifying questions, and drafts content based on your answers. Think of it as pair-writing with an agent that knows what a good PRD looks like.

### Week 3: Internal source integration

This was the game-changer. The skill got updated to automatically search internal sources when building out a PRD:

- **Slack** — finds relevant conversations and decisions
- **Data warehouse** — pulls metrics and usage data
- **Project management tools** — references related tickets and roadmap items
- **Enterprise search** — surfaces existing docs and prior art

So when you're writing a requirements doc for a new checkout feature, the agent finds the Slack thread where the team discussed it, pulls the current conversion metrics, links the related engineering tickets, and cites the previous spec that touched the same area. All automatically.

### Week 4: First real test

A PM used the skill to write a "Spread of Hours" spec — a compliance feature for labor law calculations. Complete with a working prototype.

**It took less than an hour.** The PM said the experience was smooth. The agent handled the research, the PM provided the product judgment, and the output was a clean markdown spec with a functional prototype sitting right next to it in the same folder.

That's the model: agent does the grunt work, PM does the thinking.

### Week 5: Golden path

Leadership saw the results and pushed to make this the standard approach — a "golden path" for writing product specs. The channel that started as a temporary experiment became permanent infrastructure.

## What I Learned

**Markdown beats Google Docs for specs.** Version control, PR reviews, co-located prototypes, searchability — it's better in every way that matters for technical documents. The only thing Google Docs has is real-time collaboration, and for specs, async review via PR is actually preferable.

**Agent skills work best as guides, not generators.** The skill doesn't generate a PRD from a one-line prompt. It walks you through the process section by section. The PM stays in the loop, making decisions and providing context. The agent handles structure, research, and drafting. That division of labor is what makes the output actually good.

**Auto-referencing internal sources is the real unlock.** Any PM can write a problem statement. The hard part is finding the supporting data — the Slack thread from three months ago, the usage metrics, the related spec from another team. The agent does that research in seconds instead of hours.

**Prototypes should live with requirements, not separately.** When the prototype is in the same folder as the spec, it gets reviewed together. The spec describes what should happen; the prototype shows what it looks like. Engineers can see both in context.

**The first real test matters more than months of iteration.** We spent two weeks on structure and tooling. Then one PM used it for a real spec and validated the whole approach in under an hour. Ship the minimum, test it on a real problem, iterate from there.

---

*Related: [I Replaced My Morning Routine with a Single Command](./2026-03-05-start-of-day.md) — another skill that turned a manual process into an agent-guided workflow.*

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
