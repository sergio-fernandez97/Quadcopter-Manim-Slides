#!/usr/bin/env python3
"""Preserve presentation artifacts before a Claude worktree is removed."""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


SHELL_SEPARATORS = {"&&", "||", ";", "|"}
GIT_GLOBAL_OPTS_WITH_ARGS = {
    "-C",
    "-c",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--super-prefix",
    "--config-env",
}


def load_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"[worktree-transfer] Ignoring invalid hook payload: {exc}", file=sys.stderr)
        return {}


def extract_command(payload: dict) -> str:
    tool_input = payload.get("tool_input") or {}
    for key in ("command", "cmd"):
        value = tool_input.get(key) or payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def extract_cwd(payload: dict, fallback: Path) -> Path:
    tool_input = payload.get("tool_input") or {}
    for key in ("cwd", "workdir", "directory"):
        value = tool_input.get(key) or payload.get(key)
        if isinstance(value, str) and value.strip():
            return Path(value).expanduser()
    return fallback


def resolve_path(base_dir: Path, candidate: str) -> Path:
    path = Path(candidate).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (base_dir / path).resolve()


def split_shell_segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
    lexer.whitespace_split = True
    tokens = list(lexer)

    segments: list[list[str]] = []
    current: list[str] = []
    for token in tokens:
        if token in SHELL_SEPARATORS:
            if current:
                segments.append(current)
                current = []
            continue
        current.append(token)
    if current:
        segments.append(current)
    return segments


def parse_git_segment(segment: list[str], default_cwd: Path, repo_root: Path) -> list[Path]:
    if not segment:
        return []

    git_token = Path(segment[0]).name
    if git_token != "git":
        return []

    segment_cwd = default_cwd
    index = 1
    while index < len(segment):
        token = segment[index]
        if token in GIT_GLOBAL_OPTS_WITH_ARGS:
            if index + 1 >= len(segment):
                return []
            if token == "-C":
                segment_cwd = resolve_path(segment_cwd, segment[index + 1])
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        break

    if index >= len(segment):
        return []

    subcommand = segment[index]
    args = segment[index + 1 :]
    if subcommand == "worktree":
        return parse_worktree_targets(args, segment_cwd, repo_root)
    if subcommand == "branch":
        return parse_branch_targets(args, repo_root)
    return []


def parse_worktree_targets(args: list[str], segment_cwd: Path, repo_root: Path) -> list[Path]:
    if not args or args[0] != "remove":
        return []

    target_path: Path | None = None
    for token in args[1:]:
        if token.startswith("-"):
            continue
        target_path = resolve_path(segment_cwd, token)
        break

    if target_path is None:
        return []
    if is_claude_worktree(target_path, repo_root):
        return [target_path]
    return []


def parse_branch_targets(args: list[str], repo_root: Path) -> list[Path]:
    targets: list[Path] = []
    branch_to_worktree = get_branch_to_worktree_map(repo_root)
    for token in args:
        if token.startswith("-"):
            continue
        worktree_path = branch_to_worktree.get(token)
        if worktree_path and is_claude_worktree(worktree_path, repo_root):
            targets.append(worktree_path)
    return targets


def get_branch_to_worktree_map(repo_root: Path) -> dict[str, Path]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"[worktree-transfer] Unable to inspect worktrees: {exc}", file=sys.stderr)
        return {}

    mapping: dict[str, Path] = {}
    current_path: Path | None = None
    for line in proc.stdout.splitlines():
        if line.startswith("worktree "):
            current_path = Path(line[len("worktree ") :]).resolve()
            continue
        if line.startswith("branch refs/heads/") and current_path is not None:
            branch = line[len("branch refs/heads/") :]
            mapping[branch] = current_path
    return mapping


def is_claude_worktree(path: Path, repo_root: Path) -> bool:
    claude_worktrees_root = (repo_root / ".claude" / "worktrees").resolve()
    try:
        path.resolve().relative_to(claude_worktrees_root)
        return True
    except ValueError:
        return False


def transfer_presentation(worktree_path: Path, repo_root: Path) -> None:
    source_dir = worktree_path / "presentation"
    if not source_dir.is_dir():
        return

    items = [item for item in source_dir.iterdir() if not item.name.startswith(".")]
    if not items:
        return

    destination_dir = repo_root / "presentation"
    destination_dir.mkdir(parents=True, exist_ok=True)

    copied_names: list[str] = []
    for item in items:
        destination = destination_dir / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)
        copied_names.append(item.name)

    copied_names.sort()
    print(
        f"[worktree-transfer] Copied {len(copied_names)} item(s) from "
        f"{source_dir} to {destination_dir}: {', '.join(copied_names)}",
        file=sys.stderr,
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    payload = load_payload()
    command = extract_command(payload)
    if not command:
        return 0

    default_cwd = extract_cwd(payload, repo_root)
    segments = split_shell_segments(command)

    seen: set[Path] = set()
    for segment in segments:
        for worktree_path in parse_git_segment(segment, default_cwd, repo_root):
            if worktree_path in seen:
                continue
            seen.add(worktree_path)
            transfer_presentation(worktree_path, repo_root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
