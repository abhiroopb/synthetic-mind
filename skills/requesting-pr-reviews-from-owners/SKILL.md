---
Skill name: requesting-pr-reviews-from-owners
Skill description: >
roles: [frontend]
allowed-tools: ["Bash(gh pr view*, jq*, python3*, grep*, bash*)"]
---

# Checking PR Review Status

Extracts the list of Slack channels and team approval status from the code ownership bot comment on the current PR.

**STOP** if the current directory is not a Git repository with a GitHub remote, or if there is no open PR for the current branch. Inform the user and ask how to proceed.

## Step-by-step process

1. **Run the parsing script** to extract all data from the ownership bot comment:
   ```bash
   bash <skill_path>/parse-owner-bot.sh [PR_NUMBER_OR_URL]
   ```
   The argument is optional — omit it to use the current branch's PR. This returns JSON with: `pr_number`, `pr_url`, `pr_title`, `teams` (each with `name`, `approved`, `paths`, `slack_channels`), and `all_slack_channels`.

   If the script exits with an error, relay the error message to the user and stop.

2. **Get the PR diff for pending teams' file paths and summarize:**
   For each team where `approved` is `false`, get the changed files that fall under the team's `paths`:
   ```bash
   gh pr view <PR_NUMBER> --json files -q '.files[].path' | grep '<required_path_prefix>'
   ```
   Then summarize the code changes in those files in 1-2 lines max.

3. **Present results** as a markdown list showing:
   - Which teams still need to approve (❌) and which have approved (✅)
   - The Slack channel links (already clickable) — highlight channels for teams that still need approval
   - The file paths and change summary for each pending team

4. **Generate a copyable Slack message per pending team.** Include the change summary so reviewers have context. Present as plain text (NOT in a code block) so the user can copy-paste it directly into Slack with proper formatting:

   Hi :wave: could I please get a review on this PR?
   *<PR_TITLE>*
   <PR_URL>

   Changes in your area (`<required_path>`):
   <1-2 line summary of what changed>

## Related Skills

- `pr-manager` - Use when committing code, creating a PR, or pushing changes for review
- `address-pr-comments` - Use when addressing and resolving PR review comments
