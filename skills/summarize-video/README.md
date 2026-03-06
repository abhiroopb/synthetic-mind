# Summarize video

> Extract a transcript from an internal video, generate an AI summary with timestamped quotes, and publish as a styled HTML page.

## What it does

Takes an internal video URL, extracts the SRT caption file via the video platform's API, converts it into a clean transcript, and generates an AI-powered summary with key takeaways and timestamped direct quotes. The output is built into a styled HTML page and published to an internal hosting service for easy sharing.

## Usage

Provide a video URL as the argument. The skill handles transcript extraction, summarization, HTML generation, and publishing.

- "Summarize this video: [url]"
- "Create a summary page for [video url]"

## Examples

- `"Summarize this video: https://video.example.com/media/Q1+All+Hands/1_abc123"`
- `"Generate a summary for the product review recording"`
- `"Summarize and publish the design review video from last week"`

## Why it was created

Long internal videos (all-hands, product reviews, design critiques) contain valuable information but few people rewatch them. This skill makes video content searchable and skimmable by producing a summary with clickable timestamps that jump directly to key moments.
