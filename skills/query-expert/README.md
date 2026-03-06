# Query Expert

> Discover tables, search historical queries, and execute SQL on Snowflake using vector search and SSO authentication.

## What it does

Query Expert helps you write and execute SQL queries by combining semantic search over historical query patterns with direct Snowflake execution. You can discover tables by description, find expert query examples with JOIN patterns, check table permissions, browse domain-specific knowledge files, and search a company metric store. All commands output JSON for easy parsing.

## Usage

Invoke when you need to find the right tables for a question, discover how experts query certain data, check table access, or execute SQL. Follow the recommended workflow: understand the question → load knowledge → find tables → find expert queries → check permissions → execute.

**Trigger phrases:**
- "Help me write a query for revenue by customer"
- "Find tables related to payment transactions"
- "Search for queries about subscription states"

## Examples

- `"Find tables related to payment volume for brand A"`
- `"Search for historical queries about active customers"`
- `"Execute this SQL: SELECT COUNT(*) FROM my_table"`

## Why it was created

Writing SQL against a large data warehouse is hard when you don't know which tables exist, how they join, or what patterns experts use. This skill surfaces institutional query knowledge through vector search, so you can learn from the best queries already written rather than starting from scratch.
