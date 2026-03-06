## Add /reflect skill for guided Loop reflections

Adds a new skill that guides users through writing meaningful self-reflections for **Loop in The Hub**.

### What it does

Unlike other skills that generate content, `/reflect` is a **prompting exercise**—it asks thoughtful questions and the user does the writing. This helps turn the often-rushed task of writing Loop reflections into a genuine moment of reflection.

### The approach

Loop asks: *"Reflect on your experiences, growth, and contributions."*

Most people treat this as a recap (what happened). This skill reframes it as actual reflection (what it meant) by guiding users through five areas:

| Section | Shift in thinking |
|---------|-------------------|
| **Impact & Meaning** | "What did you do?" → "What felt meaningful?" |
| **Relationships & Influence** | "Who did you work with?" → "Who made an impression on you?" |
| **Growth & Insight** | "What did you learn?" → "What surprised you or challenged an assumption?" |
| **Intention & Direction** | "What's next?" → "What's pulling at your attention?" |
| **Closing** | Overall check-in on how you're feeling |

### How it works

1. User runs `/reflect`
2. Skill prompts one question at a time, conversationally
3. User writes their own responses
4. Skill compiles their words into a formatted reflection
5. User copies to Loop in The Hub

### Files added

- `skills/reflect/SKILL.md` — Skill definition with prompts and agent guidelines
- `skills/reflect/README.md` — Documentation and usage guide
- Updated `skills-manifest.json`

### Why this matters

Reflection is a practice that benefits from structure. This skill provides that structure without taking over the thinking—helping people write more insightful reflections while keeping their authentic voice.
