# Viewing Figma files

> View Figma files, inspect page and frame structure, export node images, and read comments via the Figma REST API.

## What it does

Lets you interact with Figma files without leaving the terminal. It parses Figma URLs to extract file keys and node IDs, fetches file metadata and structure, renders specific frames as images for visual inspection, and retrieves comments and version history. All interactions happen through the Figma REST API using a personal access token.

## Usage

Paste a Figma URL or provide a file key. The skill automatically detects whether you want an overview, a specific frame, or comments.

- "Show me this Figma file: [url]"
- "What frames are in this design: [url]"
- "Show comments on [figma url]"

## Examples

- `"Show me the structure of this Figma file: https://www.figma.com/design/abc123/My-Design"`
- `"Render frame 1:3 from this file: [url]"`
- `"What are the unresolved comments on this design?"`

## Why it was created

Switching to Figma to check a design's structure, view a specific frame, or read comments breaks flow during product and engineering work. This skill brings Figma inspection directly into the agent workflow, making it easy to reference designs without context-switching.
