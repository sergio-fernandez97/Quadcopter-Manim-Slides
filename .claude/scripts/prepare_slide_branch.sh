#!/usr/bin/env bash

set -euo pipefail

BASE_BRANCH="dev"
WORKTREE_ROOT=".worktrees"
SLIDE_ID=""
SLUG=""
BRANCH_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_BRANCH="$2"
      shift 2
      ;;
    --worktree-root)
      WORKTREE_ROOT="$2"
      shift 2
      ;;
    --id)
      SLIDE_ID="$2"
      shift 2
      ;;
    --slug)
      SLUG="$2"
      shift 2
      ;;
    --branch)
      BRANCH_NAME="$2"
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

if [[ -z "$BRANCH_NAME" ]]; then
  if [[ -z "$SLIDE_ID" || -z "$SLUG" ]]; then
    echo "ERROR=missing_branch_metadata"
    exit 1
  fi

  CLEAN_SLUG="$(printf '%s' "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
  if [[ -z "$CLEAN_SLUG" ]]; then
    CLEAN_SLUG="slide-task"
  fi
  BRANCH_NAME="slide/${SLIDE_ID}-${CLEAN_SLUG}"
fi

if git show-ref --verify --quiet "refs/heads/$BASE_BRANCH"; then
  START_POINT="$BASE_BRANCH"
elif git show-ref --verify --quiet "refs/remotes/origin/$BASE_BRANCH"; then
  START_POINT="origin/$BASE_BRANCH"
else
  echo "ERROR=missing_base_branch"
  echo "BASE_BRANCH=$BASE_BRANCH"
  exit 1
fi

WORKTREE_BASE="$ROOT/$WORKTREE_ROOT"
mkdir -p "$WORKTREE_BASE"

WORKTREE_SAFE_NAME="${BRANCH_NAME//\//-}"
WORKTREE_PATH="$WORKTREE_BASE/$WORKTREE_SAFE_NAME"

TEMP_PATH_FILE="$(mktemp)"

if git worktree list --porcelain | awk -v branch="$BRANCH_NAME" '
  /^worktree / { path=$2 }
  /^branch refs\/heads\// {
    current=$0
    sub("^branch refs/heads/", "", current)
    if (current == branch) {
      print path
      found=1
      exit
    }
  }
  END { if (!found) exit 1 }
' >"$TEMP_PATH_FILE" 2>/dev/null; then
  EXISTING_PATH="$(cat "$TEMP_PATH_FILE")"
  rm -f "$TEMP_PATH_FILE"
  echo "WORKTREE_STATUS=reused"
  echo "BRANCH_NAME=$BRANCH_NAME"
  echo "WORKTREE_PATH=$EXISTING_PATH"
  echo "ROOT=$ROOT"
  exit 0
fi
rm -f "$TEMP_PATH_FILE" 2>/dev/null || true

if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  git worktree add "$WORKTREE_PATH" "$BRANCH_NAME" >/dev/null
  WORKTREE_STATUS="attached"
else
  git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" "$START_POINT" >/dev/null
  WORKTREE_STATUS="created"
fi

echo "WORKTREE_STATUS=$WORKTREE_STATUS"
echo "BRANCH_NAME=$BRANCH_NAME"
echo "WORKTREE_PATH=$WORKTREE_PATH"
echo "BASE_BRANCH=$BASE_BRANCH"
echo "ROOT=$ROOT"
