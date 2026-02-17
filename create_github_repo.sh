#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
用法:
  ./create_github_repo.sh <repo-name> [public|private] [description]

示例:
  ./create_github_repo.sh my-new-repo public
  ./create_github_repo.sh my-new-repo private "用于测试的仓库"
USAGE
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: $cmd is required." >&2
    exit 1
  fi
}

validate_context() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: current directory is not a git repository." >&2
    exit 1
  fi

  local branch
  branch="$(git branch --show-current)"
  if [[ -z "$branch" ]]; then
    echo "Error: unable to detect current branch." >&2
    exit 1
  fi
}

parse_args() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  if [[ $# -lt 1 || $# -gt 3 ]]; then
    usage
    exit 1
  fi

  REPO_NAME="$1"
  VISIBILITY="${2:-public}"
  DESCRIPTION="${3:-}"

  if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
    echo "Error: visibility must be 'public' or 'private'." >&2
    exit 1
  fi

  if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo "Error: GITHUB_TOKEN is not set." >&2
    echo "Hint: create a token with 'repo' scope and run: export GITHUB_TOKEN=your_token" >&2
    exit 1
  fi
}

create_repo() {
  local private_flag payload
  private_flag=false
  [[ "$VISIBILITY" == "private" ]] && private_flag=true

  payload="$(jq -n \
    --arg name "$REPO_NAME" \
    --arg description "$DESCRIPTION" \
    --argjson private "$private_flag" \
    '{name: $name, description: $description, private: $private}')"

  RESPONSE="$(curl -fsS -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/user/repos \
    -d "$payload" 2>/dev/null || true)"

  REPO_URL="$(jq -r '.clone_url // empty' <<<"$RESPONSE")"
  HTML_URL="$(jq -r '.html_url // empty' <<<"$RESPONSE")"

  if [[ -z "$REPO_URL" ]]; then
    local message errors
    message="$(jq -r '.message // "Unknown error"' <<<"$RESPONSE")"
    errors="$(jq -r '.errors[]?.message? // empty' <<<"$RESPONSE")"

    echo "Failed to create repository: $message" >&2
    if [[ -n "$errors" ]]; then
      echo "Details: $errors" >&2
    fi
    echo "Raw response: $RESPONSE" >&2
    exit 1
  fi
}

set_remote_and_push() {
  local branch
  branch="$(git branch --show-current)"

  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REPO_URL"
  else
    git remote add origin "$REPO_URL"
  fi

  git push -u origin "$branch"
}

main() {
  require_cmd curl
  require_cmd git
  require_cmd jq

  parse_args "$@"
  validate_context
  create_repo
  set_remote_and_push

  echo "Repository created: $HTML_URL"
  echo "Remote 'origin' set to: $REPO_URL"
}

main "$@"
