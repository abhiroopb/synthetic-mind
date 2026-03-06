# Knowledge Store Contribution Guide

This guide explains how to contribute to the Query Expert knowledge stores, which help the LLM better understand business context, data structures, and querying patterns for different brands and domains.

## Overview

Knowledge stores are organized hierarchically:
```
Knowledge/
├── brands/
|      {brand}/                         # Brand-level knowledge
│         ├── glossary.json                # Key terms and definitions
│         ├── context.txt                  # Business context for data
│         └── demographics.json            # Standard demographic segments
├── domains/
|       {domain}/                        # Domain-level knowledge (see your data domain catalog)
│         ├── glossary.json                # Key terms and definitions
│         ├── context.txt                  # Business context for data
│         └── {subdomain}/                 # Subdomain-level knowledge (see your data domain catalog)
│             ├── {topic}.txt              # Content
│             |── {topic}.json             # Structured data
│             └── {scope area}/            # Scoped knowledge area, not strictly defined like domains/subdomains
│                ├── description.txt          # Relevance and purpose
│                ├── {topic}.txt              # Content
│                └── {topic}.json             # Structured data
```

## Brand Knowledge Stores

Brand knowledge stores provide foundational context for querying data related to a specific business unit (e.g., Brand A, Brand B, Brand C).

### Required Files

#### 1. `glossary.json`
Defines key terms and their meanings to disambiguate user prompts.

**Purpose:** Helps the LLM translate business terminology into accurate data queries.

**Format:**
```json
{
  "term_name": "Definition and context for this term",
  "another_term": "How this term is used in data queries"
}
```

**Best Practices:**
- Include business-specific acronyms and their expansions
- Define terms that have multiple meanings in different contexts
- Reference specific table names or column values where applicable

#### 2. `context.txt`
Provides business context relevant to querying brand data.

**Purpose:** Gives the LLM understanding of how to best query brand data, including common patterns, assumptions, and considerations.

**Content Guidelines:**
- Explain the brand's business model and data ecosystem
- Describe common analysis patterns and use cases
- Note important filtering requirements or data quality considerations
- Reference key schemas or databases
- Include timing considerations (e.g., data freshness, historical availability)

#### 3. `demographics.json`
Defines standard demographic segments with values and naming conventions.

**Purpose:** Enables consistent querying of demographic data across analyses.

**Format:**
```json
{
  "demographic_category": {
    "description": "What this demographic represents",
    "column_name": "ACTUAL_COLUMN_NAME_IN_TABLES",
    "values": ["value1", "value2", "value3"],
    "notes": "Additional context about usage"
  }
}
```

**Best Practices:**
- Use actual column names from commonly-used tables
- List all valid categorical values
- Include notes about edge cases or special handling
- Reference the tables where these demographics are available

---

## Domain Knowledge Stores

Domain knowledge stores provide foundational context for querying data related to a specific domain (unrelated to brand)

### Structure

Create subdirectories like: `knowledge/domains/{domain}/{subdomain}/{scope_area}`

### Recommended Files

#### 1. `description.txt` (Recommended)
Provides high-level context about the subdirectory's relevance and scope. This should match what exists in your data domain catalog

**Purpose:** Helps the LLM determine if this information is relevant to a user's question.

**Content Guidelines:**
- 2-4 sentences describing what this subdirectory covers
- Key use cases or analysis types
- Relationship to other domains

#### 2. Content Files (`.txt` or `.json`)

You can organize domain knowledge in two ways:

##### **Option A: Data-Centric Organization** (See `domains/product/services/staff/` for example)
Organize files by how users conceptually view different data or business pieces:
- `employees.txt` - Employee data structures and tables
- `timecards.txt` - Time tracking data and logic
- `payroll.txt` - Payroll calculations and tables
- `benefits.txt` - Benefits enrollment and eligibility

##### **Option B: Workflow-Centric Organization**
Organize files by how users interact with the data:
- `workflows.txt` - Common analysis workflows
- `instructions.txt` - Step-by-step querying guidance
- `rules.txt` - Business rules and logic
- `validations.txt` - Data quality checks and filters

### Content Guidelines

Domain files should contain information relevant to:

1. **Data Structures**
   - Key tables and schemas (itemized list)
   - Important column names and their meanings
   - Relationships between tables (JOIN patterns)

2. **Query Patterns**
   - Common filters and WHERE conditions
   - Required aggregations or calculations
   - Typical date ranges or time windows

3. **Business Context**
   - Business rules that affect data interpretation
   - Edge cases and exceptions
   - Data quality considerations

4. **Expert References**
   - Usernames of domain experts and query pattern leaders
   - Table owners and maintainers
   - Slack channels for questions

5. **Categorical Values**
   - Valid values for key categorical columns
   - Status codes and their meanings
   - Segment definitions

### Best Practices

✅ **DO:**
- Itemize tables and schemas clearly (e.g., `YOUR_DB.YOUR_SCHEMA.FACT_TIMECARDS`)
- Include specific usernames of experts to follow
- List exact categorical column values (e.g., `status IN ('ACTIVE', 'PENDING', 'CLOSED')`)
- Provide concrete examples of filters and joins
- Explain WHY certain patterns are used, not just WHAT to do
- Keep content focused on data and querying, not general business processes

❌ **DON'T:**
- Include sensitive or confidential information
- Duplicate information already in table metadata
- Write generic advice that applies to all data
- Include outdated table names or deprecated patterns

### File Format Choice

- **Use `.txt`** for narrative explanations, workflows, and context
- **Use `.json`** for structured data like lists, mappings, or configurations

---

## Example: Brand A Staff Domain

```
knowledge/domains/product/services/staff/
├── domain_description.txt   # "Staff domain covers employee management..."
├── employees.txt            # Employee data tables and demographics
├── timecards.txt            # Time tracking logic and calculations
├── payroll.txt              # Payroll processing and payment tables
└── scheduling.txt           # Shift scheduling and availability
```

Each file contains:
- Relevant tables (e.g., `YOUR_DB.YOUR_SCHEMA.DIM_EMPLOYEES`)
- Key columns and their usage
- Common query patterns
- Expert usernames to reference
- Business rules specific to that topic

---

## Contributing

1. **Identify the Brand, Domain, and Sub-Domain**
   - Determine which brand your knowledge applies to
   - Decide if it's brand-level or domain-specific
   - create a nested scope area if relevant

2. **Choose Your Organization Strategy**
   - Data-centric: Organize by business entities
   - Workflow-centric: Organize by how users query

3. **Create Your Files**
   - Follow naming conventions (lowercase, underscores)
   - Use appropriate file formats (.txt or .json)

4. **Populate with Actionable Content**
   - Focus on information that improves query generation
   - Include specific table names, columns, and values
   - Reference domain experts

5. **Test and Iterate**
   - Use the knowledge store with Query Expert
   - Refine based on query quality improvements
   - Update as data structures evolve

---

## How the LLM Uses This Knowledge

The LLM leverages knowledge stores to:

1. **Expand User Prompts** - Translate business questions into technical query requirements
2. **Discover Tables** - Find relevant tables based on business context
3. **Generate Accurate Queries** - Apply domain-specific filters, joins, and logic
4. **Identify Experts** - Connect users with domain experts for validation
5. **Apply Business Rules** - Incorporate domain knowledge into query logic

By contributing to knowledge stores, you help the LLM provide more accurate, context-aware query assistance for your domain.