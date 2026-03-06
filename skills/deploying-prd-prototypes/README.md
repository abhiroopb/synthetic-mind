# Deploying PRD prototypes

> Deploy interactive prototypes from product requirements documents to an internal hosting service for sharing.

## What it does

This skill automates the process of building and deploying static website prototypes from PRDs. It handles the full workflow: scaffolding the project, configuring the build for the correct base path, deploying via REST API, and updating the PRD with the deployed URL. It also supports versioning and rollback.

## Usage

Use when you need to build a demo, prototype, or static site from a product requirements document and share it internally. Prototypes are stored in a local `prototypes/` directory (gitignored) and deployed to a hosted URL.

## Examples

- "Build and deploy a prototype for the neighborhoods feature"
- "Deploy the latest version of my checkout demo"
- "Roll back the cash-rounding prototype to the previous version"

## Why it was created

Sharing interactive prototypes with stakeholders requires hosting infrastructure. This skill streamlines the build-deploy cycle so PMs and designers can iterate on demos quickly without managing infrastructure.
