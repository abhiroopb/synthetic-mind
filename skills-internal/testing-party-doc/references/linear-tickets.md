# Create Linear Tickets from Bugs

Load when the user asks to create Linear tickets from bugs logged in the Bugs tab.

## Prerequisites
- The `linear` skill must be installed (see [SETUP.md](../SETUP.md))
- Bugs must already be logged in the Bugs tab of the Google Doc

## Workflow

1. **Read the Bugs tab** from the destination doc:
   ```bash
   cd ~/.claude/skills/gdrive && uv run gdrive-cli.py read <doc-id> --tab <bugs-tab-id>
   ```

2. **Parse the Bugs table** to extract rows where the Bug column is filled in. Skip empty rows and rows that already have a Linear Ticket value.

3. **Ask the user** for Linear ticket details:
   > I found **N** bugs in the Bugs tab without Linear tickets. To create tickets, I need:
   > - **Team key** (required): e.g., `RTLMOB`, `SPOS`
   > - **Labels** (optional): e.g., `bug`, `testing-party`
   > - **Priority** (optional): 1 (Urgent), 2 (High), 3 (Medium), 4 (Low)
   >
   > Which team should these tickets be filed under?

4. **Create a Linear ticket for each bug** using the linear skill CLI:
   ```bash
   cd ~/.claude/skills/linear && npx tsx linear-cli.ts create-issue \
     --title "<bug description>" \
     --team "<team-key>" \
     --description "**Platform:** <platform> | **Device:** <device> | **Mode:** <mode> | **Severity:** <severity> | **Reporter:** <reporter>" \
     --json
   ```
   Parse the JSON response to extract the ticket identifier (e.g., `RTLMOB-123`) and URL.

5. **Write ticket identifiers back** into the "Linear Ticket" column of the Bugs tab. Use `docs batch-update` to insert the ticket identifier (linked to the ticket URL) into each corresponding row:
   ```bash
   cd ~/.claude/skills/gdrive && cat << 'EOF' | uv run gdrive-cli.py docs batch-update <doc-id>
   {
     "requests": [
       {
         "insertText": {
           "location": { "index": <cell-index>, "tabId": "<bugs-tab-id>" },
           "text": "<ticket-identifier>"
         }
       }
     ]
   }
   EOF
   ```

6. **Report results** to the user:
   > Created **N** Linear tickets from the Bugs tab:
   > - `TEAM-123`: <bug description>
   > - `TEAM-124`: <bug description>
   > ...
   >
   > The ticket identifiers have been written back into the Google Doc.
