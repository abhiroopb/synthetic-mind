#!/usr/bin/env bash
set -euo pipefail

OWNER=$(gh repo view --json owner --jq '.owner.login')
NAME=$(gh repo view --json name --jq '.name')
NUM=$(gh pr view --json number --jq '.number')

gh api graphql \
  -f query='
    query {
      repository(owner: "'"$OWNER"'", name: "'"$NAME"'") {
        pullRequest(number: '"$NUM"') {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              comments(first: 10) {
                nodes {
                  databaseId
                  path
                  line
                  body
                  author { login }
                }
              }
            }
          }
        }
      }
    }' \
  --jq '
    .data.repository.pullRequest.reviewThreads.nodes[]
    | select(.isResolved == false)
    | {
        threadId: .id,
        comments: [
          .comments.nodes[]
          | {id: .databaseId, author: .author.login, path, line, body}
        ]
      }'
