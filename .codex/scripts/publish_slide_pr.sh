#!/usr/bin/env bash

set -euo pipefail

BASE_BRANCH="dev"
BRANCH_NAME=""
COMMIT_MESSAGE=""
PR_TITLE=""
PR_BODY_FILE=""
PR_DRAFT=0
SKIP_PR=0
UPDATE_EXISTING_PR=0
FILES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_BRANCH="$2"
      shift 2
      ;;
    --branch)
      BRANCH_NAME="$2"
      shift 2
      ;;
    --message)
      COMMIT_MESSAGE="$2"
      shift 2
      ;;
    --pr-title)
      PR_TITLE="$2"
      shift 2
      ;;
    --pr-body-file)
      PR_BODY_FILE="$2"
      shift 2
      ;;
    --draft-pr)
      PR_DRAFT=1
      shift
      ;;
    --skip-pr)
      SKIP_PR=1
      shift
      ;;
    --update-existing-pr)
      UPDATE_EXISTING_PR=1
      shift
      ;;
    --file)
      FILES+=("$2")
      shift 2
      ;;
    *)
      echo "ERROR=unknown_argument"
      echo "ARG=$1"
      exit 1
      ;;
  esac
done

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

CURRENT_BRANCH="$(git branch --show-current)"
if [[ -z "$BRANCH_NAME" ]]; then
  BRANCH_NAME="$CURRENT_BRANCH"
fi

if [[ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]]; then
  echo "ERROR=branch_mismatch"
  echo "CURRENT_BRANCH=$CURRENT_BRANCH"
  echo "EXPECTED_BRANCH=$BRANCH_NAME"
  exit 1
fi

if [[ "$BRANCH_NAME" == "main" || "$BRANCH_NAME" == "$BASE_BRANCH" ]]; then
  echo "ERROR=protected_branch"
  echo "CURRENT_BRANCH=$BRANCH_NAME"
  exit 1
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "ERROR=no_files_specified"
  exit 1
fi

for file in "${FILES[@]}"; do
  if [[ -e "$file" ]] || git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
    git add -- "$file"
  else
    echo "WARN=missing_file:$file"
  fi
done

if git diff --cached --quiet; then
  COMMIT_CREATED=0
else
  if [[ -z "$COMMIT_MESSAGE" ]]; then
    echo "ERROR=missing_commit_message"
    exit 1
  fi
  git commit -m "$COMMIT_MESSAGE" >/dev/null
  COMMIT_CREATED=1
fi

git push -u origin "$BRANCH_NAME" >/dev/null

echo "PUSH_STATUS=success"
echo "BRANCH_NAME=$BRANCH_NAME"
echo "BASE_BRANCH=$BASE_BRANCH"
echo "COMMIT_CREATED=$COMMIT_CREATED"

if [[ "$SKIP_PR" -eq 1 ]]; then
  echo "PR_STATUS=skipped"
  exit 0
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "PR_STATUS=requires_mcp_or_gh"
  exit 0
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "PR_STATUS=requires_mcp_or_gh_auth"
  exit 0
fi

EXISTING_NUMBER="$(gh pr list --head "$BRANCH_NAME" --base "$BASE_BRANCH" --state open --json number --jq '.[0].number' 2>/dev/null || true)"
if [[ -n "$EXISTING_NUMBER" ]]; then
  if [[ "$UPDATE_EXISTING_PR" -eq 1 ]]; then
    if [[ -n "$PR_TITLE" ]]; then
      gh pr edit "$EXISTING_NUMBER" --title "$PR_TITLE" >/dev/null
    fi
    if [[ -n "$PR_BODY_FILE" ]]; then
      gh pr edit "$EXISTING_NUMBER" --body-file "$PR_BODY_FILE" >/dev/null
    fi
    echo "PR_STATUS=updated"
    echo "PR_NUMBER=$EXISTING_NUMBER"
  else
    echo "PR_STATUS=existing"
    echo "PR_NUMBER=$EXISTING_NUMBER"
  fi
  exit 0
fi

CREATE_ARGS=(pr create --base "$BASE_BRANCH" --head "$BRANCH_NAME")
if [[ "$PR_DRAFT" -eq 1 ]]; then
  CREATE_ARGS+=(--draft)
fi
if [[ -n "$PR_TITLE" ]]; then
  CREATE_ARGS+=(--title "$PR_TITLE")
fi
if [[ -n "$PR_BODY_FILE" ]]; then
  CREATE_ARGS+=(--body-file "$PR_BODY_FILE")
else
  CREATE_ARGS+=(--fill)
fi

PR_URL="$(gh "${CREATE_ARGS[@]}")"
echo "PR_STATUS=created"
echo "PR_URL=$PR_URL"
