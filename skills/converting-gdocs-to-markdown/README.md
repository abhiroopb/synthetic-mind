# Converting Google Docs to Markdown

> Convert Google Docs into properly formatted markdown files for your repository.

## What it does

Reads a Google Doc (including multi-tab documents) via the Google Drive API, converts the content to well-structured markdown with proper headers, lists, tables, and code blocks, and saves it to the appropriate directory in your repository following naming conventions. Supports single tabs, specific tabs, or all tabs at once.

## Usage

Use when you need to import documentation from Google Drive into a local repository as markdown. Requires the gdrive skill to be installed and authenticated.

Trigger phrases:
- "Convert this Google Doc to markdown"
- "Import the PRD from Google Docs"
- "Turn this gdoc into a local markdown file"

## Examples

- "Convert the PRD at this Google Docs URL to markdown and save it in requirements/"
- "Import all tabs from this Google Doc as markdown"
- "Pull the research doc from Google Drive and add it to the repo"

## Why it was created

Product documentation often lives in Google Docs but needs to be version-controlled in a repository. This skill automates the conversion process, applying consistent formatting and directory conventions.
