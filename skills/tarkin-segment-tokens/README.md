# Segment token manager

> Add or remove tokens (serial numbers, UUIDs) from audience segments while preserving segment metadata.

## What it does

Manages membership of audience segments by adding or removing tokens such as device serial numbers or UUIDs. It fetches the current segment details, displays them for confirmation, and then executes the modification while automatically preserving the segment's name, description, and type. Supports both staging and production environments, with an optional dry-run mode.

## Usage

Tell the skill what segment to modify, what tokens to add or remove, and which environment to target. It always asks for explicit confirmation before making changes.

- "Add [tokens] to segment [id] on [environment]"
- "Remove [serial number] from segment [name] on staging"

## Examples

- `"Remove serial number ABC123 from segment 50 on staging"`
- `"Add these UUIDs to the beta testers segment on production: UUID1, UUID2, UUID3"`
- `"Show me what's in segment 'pilot devices' on staging"`

## Why it was created

Manually modifying audience segments through the UI is error-prone for bulk operations and doesn't preserve metadata consistently. This skill automates the process with built-in safety checks — mandatory confirmation, metadata preservation, and dry-run support.
