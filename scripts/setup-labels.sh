#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || "$1" != */* ]]; then
  echo "Usage: $0 owner/repository" >&2
  exit 2
fi

repo="$1"

command -v gh >/dev/null 2>&1 || {
  echo "GitHub CLI (command-line interface) is required." >&2
  exit 1
}
gh auth status >/dev/null
gh repo view "$repo" >/dev/null

existing_labels="$(gh label list --repo "$repo" --limit 1000 --json name --jq '.[].name')"

labels=(
  "loop:spec|BFD4F2|Contract drafted; awaiting human approval"
  "loop:ready|0E8A16|Human-approved and eligible to claim"
  "loop:building|1D76DB|Atomically claimed and being implemented"
  "loop:review|5319E7|Awaiting independent review"
  "loop:changes|D93F0B|Commit-specific must-fix findings exist"
  "loop:approved|006B2E|Review evidence complete; human merge decision remains"
  "loop:blocked|FBCA04|One answer or dependency is required"
  "loop:human-review|B60205|Automation requires a human decision"
  "loop:done|C5DEF5|Human merged or explicitly closed the work"
)

created=0
for entry in "${labels[@]}"; do
  IFS="|" read -r name colour description <<<"$entry"
  if grep -Fxq "$name" <<<"$existing_labels"; then
    echo "Exists:  $name"
    continue
  fi
  gh label create "$name" \
    --repo "$repo" \
    --color "$colour" \
    --description "$description"
  echo "Created: $name"
  created=$((created + 1))
done

echo "Label setup complete: $created created."
