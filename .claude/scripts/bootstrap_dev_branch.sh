#!/usr/bin/env bash

set -euo pipefail

REMOTE="${1:-origin}"
DEFAULT_BRANCH="${2:-main}"
TARGET_BRANCH="${3:-dev}"

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "ERROR=remote_not_found"
  echo "REMOTE=$REMOTE"
  exit 1
fi

git fetch "$REMOTE" "$DEFAULT_BRANCH" >/dev/null 2>&1 || true
git fetch "$REMOTE" "$TARGET_BRANCH" >/dev/null 2>&1 || true

if git ls-remote --exit-code --heads "$REMOTE" "$TARGET_BRANCH" >/dev/null 2>&1; then
  if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
    git branch --set-upstream-to="$REMOTE/$TARGET_BRANCH" "$TARGET_BRANCH" >/dev/null 2>&1 || true
    echo "DEV_STATUS=existing"
    echo "DEV_SOURCE=remote"
  else
    git branch --track "$TARGET_BRANCH" "$REMOTE/$TARGET_BRANCH" >/dev/null 2>&1
    echo "DEV_STATUS=tracked"
    echo "DEV_SOURCE=remote"
  fi
else
  if git show-ref --verify --quiet "refs/remotes/$REMOTE/$DEFAULT_BRANCH"; then
    START_POINT="$REMOTE/$DEFAULT_BRANCH"
  elif git show-ref --verify --quiet "refs/heads/$DEFAULT_BRANCH"; then
    START_POINT="$DEFAULT_BRANCH"
  else
    echo "ERROR=missing_default_branch"
    echo "DEFAULT_BRANCH=$DEFAULT_BRANCH"
    exit 1
  fi

  if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
    echo "DEV_STATUS=local_only"
    echo "DEV_SOURCE=local"
  else
    git branch "$TARGET_BRANCH" "$START_POINT" >/dev/null 2>&1
    echo "DEV_STATUS=created"
    echo "DEV_SOURCE=$START_POINT"
  fi

  git push -u "$REMOTE" "$TARGET_BRANCH" >/dev/null
fi

echo "DEV_BRANCH=$TARGET_BRANCH"
echo "ROOT=$ROOT"
