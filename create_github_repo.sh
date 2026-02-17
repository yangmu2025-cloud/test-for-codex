#!/usr/bin/env bash
set -euo pipefail

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required." >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "Error: git is required." >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required." >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <repo-name> [public|private]"
  echo "Example: $0 my-new-repo public"
  exit 1
fi

REPO_NAME="$1"
VISIBILITY="${2:-public}"
if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
  echo "Error: visibility must be 'public' or 'private'." >&2
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Error: GITHUB_TOKEN is not set." >&2
  echo "Create a personal access token with 'repo' scope and export it before running this script." >&2
  exit 1
fi

PRIVATE_FLAG=false
if [[ "$VISIBILITY" == "private" ]]; then
  PRIVATE_FLAG=true
fi

response=$(curl -sS -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"${REPO_NAME}\",\"private\":${PRIVATE_FLAG}}")

repo_url=$(jq -r '.clone_url // empty' <<<"$response")
html_url=$(jq -r '.html_url // empty' <<<"$response")
message=$(jq -r '.message // empty' <<<"$response")

if [[ -z "$repo_url" ]]; then
  echo "Failed to create repository: ${message:-Unknown error}" >&2
  echo "$response" >&2
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$repo_url"
else
  git remote add origin "$repo_url"
fi

git push -u origin "$(git branch --show-current)"

echo "Repository created: $html_url"
echo "Remote 'origin' set to: $repo_url"
