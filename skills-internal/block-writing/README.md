# Brand Voice Writing Standards Skill

> Complete writing expertise for all all products and communications

An Agent Skill that transforms AI assistants into comprehensive brand writing experts. Provides guidance from initial content strategy through final copy review, with integrated brand voice standards and real content creation workflows.


**Note**
This skill is still under development and testing. Please feel free to request changes in github or reach out to @claydelk on Slack for questions or feedback.

## What This Skill Provides

### ✍️ **Content Creation Guidance**
- Smart recommendations for UI copy, marketing content, and support articles
- Component-specific writing guidance from consumer product's Arcade Design System and merchant product's Market Design System
- brand voice principles applied to specific content types and contexts
- Business vs consumer audience adaptations with appropriate design system patterns
- Writing patterns and templates for common scenarios
- Brand-specific adaptations for each product line

### 📝 **Style and Mechanics Support**
- Comprehensive style guidelines integrated with brand voice standards
- Grammar, punctuation, and formatting rules for different content types
- Accessibility and inclusive language requirements
- Content patterns and templates for common writing scenarios

### 🎯 **Content Strategy Integration**
- Growth messaging frameworks and positioning guidance
- Transactional communication standards for emails, SMS, and push notifications
- Legal copy and compliance language patterns
- Cross-product consistency validation

### ✅ **Content Quality Assurance**
- Validate content against brand writing standards and voice principles
- Accessibility and inclusive language guidelines
- Cross-platform consistency validation
- Brand voice and tone verification

## Products Covered

These standards apply to all all products:
- **consumer product** - Consumer financial services
- **merchant product** - Merchant and business tools
- **BNPL product** - Buy now, pay later services
- **Tidal** - Music streaming platform
- **Bitkey** - Bitcoin hardware wallet
- **Proto** - Emerging financial products

## Installation

This skill works with **Claude Desktop**, **Claude Code**, and **Goose**. Choose the installation method that matches your setup.

### Claude Desktop

1. **Download** the `block-writing` folder
2. Open **Claude Desktop**
3. Go to **Settings → Capabilities → Skills**
4. Click **Add skill** and select the `block-writing` folder
5. Start using the skill immediately!

### Claude Code

**Step 1: Copy to Skills Folder**

Copy the `block-writing` folder to your Claude skills directory:
- **Mac/Linux**: `~/.claude/skills/`
- **Windows**: `%USERPROFILE%\.claude\skills\`

**Step 2: Restart Claude Code**

Quit and reopen Claude Code to activate the skill.

**Verify It's Working**

Try asking Claude:
```
Write a button label for saving user preferences that follows brand voice principles
```

### Goose

**Quick Start:**
```bash
# 1. Copy skill to Goose directory
cp -r /path/to/block-writing ~/.config/goose/skills/

# 2. Load skill in Goose
skills__loadSkill block-writing

# 3. Test with a simple query
Write an error message for a failed payment that follows brand voice principles
```

**Full Installation for Content Teams:**

**Requirements:**
- Goose installed and configured

**Installation Steps:**

```bash
# Navigate to your Goose skills directory
cd ~/.config/goose/skills/

# Copy the block-writing skill
cp -r /path/to/block-writing ./block-writing
```

**Load the Skill:**
```bash
# In Goose, load the skill
skills__loadSkill block-writing
```

**Verify Installation:**
```
Write an error message for a failed consumer product payment that follows brand voice principles
```

Goose should respond with specific brand writing guidance including voice principles, style mechanics, and content best practices.

**Goose-Specific Features:**
- **File System Integration**: Review and edit content files directly using Goose's `developer__text_editor` tool
- **Content Analysis Integration**: Combine with Goose's `developer__analyze` tool to review existing content across codebases
- **Memory Integration**: Store project-specific style decisions and brand preferences using Goose's memory system


## Connect to Figma (Optional)

For enhanced design reviews, connect Claude to Figma so you can share design links and get instant feedback.

**Choose the Remote Server option** unless you have specific requirements for the Desktop Server.

### Option 1: Remote Server (Recommended)

**Requirements:**
- Claude Code installed
- Figma account (Starter, Professional, Organization, or Enterprise plan)

**Setup Steps:**

```bash
# Install Figma MCP
claude mcp add --transport http figma https://mcp.figma.com/mcp

# Restart Claude Code
# Authenticate with Figma when prompted
```

### Option 2: Desktop Server

**Requirements:**
- Figma desktop app (latest version)
- Claude Code installed
- Dev Mode access in Figma

**Setup Steps:**

1. Open Figma desktop app and switch to **Dev Mode** (`Shift + D`)
2. Enable **MCP server** in the Inspect panel
3. Connect Claude Code:
   ```bash
   claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
   ```
4. Restart Claude Code

**Using with Figma Links:**

Once connected, you can share Figma links for instant design reviews:

```
Review this design for Arcade compliance:
https://www.figma.com/file/abc123/Design?node-id=123-456

Check for:
- Correct component usage
- Content guidelines adherence
- Accessibility standards
```


## Usage Examples

### Basic Queries (All Platforms)

Try these queries to see the skill in action:

```
Write a button label for saving user preferences that follows brand voice principles
```

```
Create an error message for a failed payment that's upfront but not alarming
```

```
How should I write push notification copy for a consumer product promotion?
```

```
Review this marketing email for brand voice consistency
```

### Advanced Goose Workflows

**Content Audit and Review:**
```bash
# 1. Analyze existing content across project
developer__analyze path:/Users/yourname/marketing-site/content focus:"copy" max_depth:2

# 2. Get brand writing guidance on the analysis
Review this content analysis for brand writing standards compliance.
Focus on: voice consistency, accessibility, style mechanics.
```

**Content Creation and Editing:**
```bash
# 1. Create new content file
developer__text_editor path:/Users/yourname/project/new-feature-copy.md command:write file_text:"# Payment Confirmation\n\nDraft copy for payment success flow..."

# 2. Get content improvement suggestions
Review this payment confirmation copy for brand voice principles.
Apply: crisp messaging, self-assured tone, upfront communication.
```

**Brand Voice Consistency Audit:**
```bash
# 1. Search for existing copy patterns across codebase
developer__shell command:"rg -l 'button|error|success|notification' --type md --type txt /path/to/content"

# 2. Review findings with brand standards
I found these content files in my project. Can you help me audit them for brand voice consistency?
[paste file list from search results]
```

**Memory-Driven Content Consistency:**
```bash
# Store project context and decisions
memory__remember_memory category:"current_project" data:"Redesigning consumer product error messages. Focus on reducing user anxiety while being upfront about issues." is_global:false

# Store style preferences
memory__remember_memory category:"style_preferences" data:"Use contractions for conversational tone. Avoid technical jargon. Include specific next steps in all error messages." is_global:false

# Get contextual guidance
Based on my current project and style preferences, write an error message for insufficient funds.
```

**Combine with Other Skills:**
```bash
# Load both skills for comprehensive guidance
skills__loadSkill arcade-design-system
skills__loadSkill block-writing

# Then get integrated guidance
Write button copy for an Arcade modal that follows both brand writing standards and Arcade content guidelines.
Context: User needs to confirm account deletion.
```

## What's Included

This skill contains comprehensive resources organized by content type:

### 📋 **Core References** (`references/` directory)

**Foundational Guidelines:**
- **`foundations-block-voice-principles.md`**: Complete guide to the four voice principles (crisp, self-assured, fluent, upfront) with tactics and examples
- **`content-tag-taxonomy.md`**: Standardized tagging system for content organization and retrieval

**Product Writing Standards:**
- **`product-style-and-mechanics.md`**: Comprehensive style guide for punctuation, capitalization, formatting, and UI copy standards
- **`product-inclusive-language.md`**: Accessibility and non-discriminatory language guidelines for all content types
- **`product-point-of-view.md`**: Pronoun usage and perspective consistency across all products
- **`product-numbers.md`**: Formatting standards for currency, dates, phone numbers, and abbreviations
- **`product-brand-b-transactional-communications.md`**: Email, SMS, and push notification guidelines and templates
- **`product-brand-b-legal-footers.md`**: Legal copy and compliance language standards

**Creative Marketing Guidelines:**
- **`creative-square-style-guide.md`**: merchant product-specific brand voice, messaging, and style guidelines
- **`creative-brand-b-growth-writing-guidelines.md`**: Growth messaging frameworks and positioning strategies
- **`creative-creative-brand-c-brand-b-guidelines.md`**: BNPL product product messaging and brand voice standards
- **`creative-creative-brand-b-growth-messaging-framework.md`**: Strategic messaging frameworks for product marketing
- **`creative-creative-brand-b-financial-inclusion-whitepaper.md`**: Financial education and thought leadership content standards
- **`creative-dates-times-locations.md`**: Marketing-specific formatting for temporal and location references
- **`creative-inclusivity-and-transparency.md`**: Marketing copy accessibility and transparency guidelines
- **`creative-numbers.md`**: Marketing-specific number formatting and usage patterns
- **`creative-style-and-grammar.md`**: Grammar, punctuation, and style rules for marketing content

**Support Content Guidelines:**
- **`support-writing-principles.md`**: Core principles for help articles, troubleshooting guides, and customer support content
- **`support-specific-style.md`**: Support-specific voice adaptations and formatting requirements
- **`support-steps-writing.md`**: Guidelines for writing clear, actionable step-by-step instructions
- **`support-brand-b-web-help-template.md`**: Standardized template for consumer product help articles and web content
- **`support-how-to-article-template.md`**: Template structure for how-to guides and instructional content
- **`support-troubleshooting-article-template.md`**: Template for troubleshooting articles and problem-solving content
- **`support-cf1-article-guidelines.md`**: CF1-specific article formatting, style, and content requirements

**Component Writing Guidelines:**
- **`component-arcade-content-guidelines.md`**: Comprehensive content standards for UI components across all products, with primary guidance from consumer product's Arcade Design System
- **`component-square-content-guidelines.md`**: merchant product-specific component content standards for Market Design System, with business-focused voice and merchant audience adaptations
- **`component-decision-trees.md`**: Decision frameworks for writing content for different component types and contexts
- **`component-content-patterns.md`**: Reusable content templates, patterns, and examples for UI components
- **`component-quick-reference.md`**: Fast reference guide for character limits, formatting rules, and component-specific standards

## Quick Reference

### Most Common Guidelines
- **Voice & Tone**: `foundations-block-voice-principles.md`
- **UI Copy Standards**: `product-style-and-mechanics.md`
- **Marketing Copy**: `creative-style-and-grammar.md`
- **Accessibility**: `product-inclusive-language.md`
- **Transactional Comms**: `product-brand-b-transactional-communications.md`

### Product-Specific Guidelines
- **consumer product**: Multiple documents across both creative-marketing and product-writing
- **merchant product**: `creative-square-style-guide.md`
- **BNPL product**: `creative-creative-brand-c-brand-b-guidelines.md`

### Content Type Quick Access

**Writing UI copy**: Start with `product-style-and-mechanics.md` and `foundations-block-voice-principles.md`
**Creating error messages**: Use `product-style-and-mechanics.md` with voice principle "upfront"
**Marketing campaigns**: Begin with `creative-brand-b-growth-writing-guidelines.md` and relevant product guidelines
**Help articles**: Use `support-writing-principles.md` and appropriate article templates
**Email/SMS**: Reference `product-brand-b-transactional-communications.md`
**Legal copy**: Consult `product-brand-b-legal-footers.md`
**Accessibility review**: Apply `product-inclusive-language.md` standards

## How to Use This Documentation

### For Writers and Content Designers
1. **Start with Foundations** - Review voice principles and taxonomy
2. **Choose Your Category** - Search for resources related to creative, product, or support, based on your project
3. **Search by Tags** - Use the standardized tags to find relevant guidance
4. **Cross-Reference** - Many guidelines work together (e.g., voice + accessibility + product-specific rules)

### For AI-Assisted Writing
This documentation is formatted for Retrieval Augmented Generation (RAG) systems:
- Each document follows Atomic Markdown Format Standards v1.3.1
- Semantic anchors enable precise content retrieval
- Standardized metadata supports intelligent routing
- Tags enable fuzzy matching and contextual search

### Tag System
Documents use standardized, hyphenated tags for easy discovery:
- **Products**: `brand-b`, `brand-a`, `brand-c`, `brand-d`, `brand-e`, `brand-f`
- **Content Types**: `ui-copy`, `marketing-copy`, `email-notifications`, `legal-copy`
- **Audiences**: `customer-facing`, `merchant-facing`, `internal-comms`
- **Topics**: `voice-and-tone`, `accessibility`, `style-guide`, `grammar-rules`

## Goose Troubleshooting

### Common Issues and Solutions

**Skill not loading in Goose:**
```bash
# Check if skill directory exists
ls ~/.config/goose/skills/block-writing

# If missing, copy the skill directory
cp -r /path/to/block-writing ~/.config/goose/skills/

# Try loading again
skills__loadSkill block-writing
```

**"Skill not found" error:**
```bash
# Check exact skill name in directory
ls ~/.config/goose/skills/

# Load using exact directory name
skills__loadSkill block-writing
```

**Skill loads but doesn't provide brand writing guidance:**
```bash
# Verify skill content is present
developer__text_editor path:~/.config/goose/skills/block-writing/SKILL.md command:view

# Try a specific brand writing query
Write a consumer product error message that follows brand voice principles
```

### Best Practices for Goose Users

**Skill Management:**
```bash
# Always load the skill at the start of content work
skills__loadSkill block-writing

# Combine with complementary skills
skills__loadSkill arcade-design-system  # For comprehensive UI guidance
```

**Memory Usage Patterns:**
```bash
# Store project-specific voice decisions
memory__remember_memory category:"voice_preferences" data:"consumer product onboarding: conversational and empowering. Error messages: upfront but reassuring." is_global:false tags:["voice", "brand-b"]

# Retrieve context before content creation
memory__retrieve_memories category:"voice_preferences" is_global:false
```

**Content Analysis Workflows:**
```bash
# Start with broad content analysis
developer__analyze path:/path/to/content max_depth:2

# Then focus on specific content types
developer__shell command:"rg -l 'error|success|button|notification' --type md /path/to/content"

# Get brand writing guidance
Review this content analysis for brand writing standards compliance. Focus on: voice consistency, style mechanics, accessibility.
```

## Contributing

When adding new guidelines:
1. **Use the conversion recipe**: See `/tools/rag-conversion-recipe.md` for step-by-step instructions
2. **Follow Atomic Markdown Format Standards** with proper structure and metadata
3. **Use standardized tags** from `/tools/content-tag-taxonomy.md`
4. **Include complete metadata** (Title, Audience, Author, Theme, etc.)
5. **Add semantic anchors** for RAG compatibility
6. **Cross-reference related documents** using proper slug format

---

**Last Updated**: January 2026  
**Maintained By**: Writing Standards Team  
**Format**: Atomic Markdown Standards v1.3.1
