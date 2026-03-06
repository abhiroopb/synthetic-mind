# Databricks

> Query the Databricks Lakehouse using SQL via the Databricks CLI.

## What it does

Runs SQL queries against a Databricks Lakehouse using the Statement Execution API through the Databricks CLI. Supports listing catalogs, searching for tables, describing table schemas, running queries with structured result output, and handling long-running queries through async submission and polling. Uses OAuth for authentication.

## Usage

Use when you need to query Databricks, search tables and catalogs, describe schemas, or run SQL against Databricks data. Requires the Databricks CLI to be installed and authenticated.

Trigger phrases:
- "Query Databricks for..."
- "Search Databricks tables"
- "Run this SQL on Databricks"
- "Describe this Databricks table"

## Examples

- "List all available catalogs in Databricks"
- "Search for tables with 'payment' in the name"
- "Run a query to get the last 10 rows from the transactions table"

## Why it was created

Querying Databricks through the web UI is slow for quick lookups. This skill wraps the Databricks CLI into a streamlined workflow for running SQL, discovering tables, and handling query results — all from the terminal.
