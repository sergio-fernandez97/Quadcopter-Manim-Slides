---
name: slide
description: "Create or update a Manim slide from a markdown draft file in ./draft/. Orchestrates draft-reader, style-inspector, slide-builder/updater, math-validator, slide-layout-validator, and slide-publisher."
user-invocable: true
allowed-tools: Read Write Edit Agent Bash(git:*) Bash(uv run:*) Bash(gh:*) Bash(.codex/scripts/bootstrap_dev_branch.sh:*) Bash(.codex/scripts/prepare_slide_branch.sh:*) Bash(.codex/scripts/publish_slide_pr.sh:*) mcp__context7__resolve-library-id mcp__context7__query-docs
argument-hint: "<draft-file-or-topic> [--no-render] [--no-validate] [--no-publish] [--draft-pr] [--update-existing-pr]"
---

Create or update a Manim slide from a markdown draft: $ARGUMENTS

## Arguments

- A path to a markdown file in `./draft/` (e.g. `draft/14_td_learning.md`)
- OR a topic name that matches an existing draft file (e.g. `td_learning`)
- Optional flag: `--no-render` to skip rendering and layout validation
- Optional flag: `--no-validate` to skip math and layout validation
- Optional flag: `--no-publish` to skip commit/push/PR creation
- Optional flag: `--draft-pr` to open the PR as a draft
- Optional flag: `--update-existing-pr` to update an existing PR on the current feature branch

## Instructions

### Step 0: Resolve arguments and draft file

1. Parse `$ARGUMENTS` into:
   - draft path or topic
   - `--no-render`
   - `--no-validate`
   - `--no-publish`
   - `--draft-pr`
   - `--update-existing-pr`
2. If the argument is a file path (contains `/` or ends with `.md`), use it directly.
3. If it is a topic name, glob for `draft/*{topic}*.md`.
4. If no match is found, list available drafts in `./draft/` and ask the user which one to use.
5. Read the draft file to confirm it exists and has content.

### Step 0.5: Enforce branch and worktree policy

1. Read the repository state:
   ```bash
   git branch --show-current
   git worktree list --porcelain
   git status --short --branch
   ```
2. If the user did not pass `--no-publish`, ensure `dev` exists:
   ```bash
   .codex/scripts/bootstrap_dev_branch.sh
   ```
3. Publishing rules:
   - Never publish from `main`
   - Never publish from `dev`
   - Prefer running inside a `slide/*` feature branch that was created for a dedicated worktree session
4. If the current branch is `main` or `dev` and publishing is enabled:
   - stop before making Git changes
   - tell the user to prepare a worktree with `/worktree_slide`
   - continue only if they rerun with `--no-publish`
5. If the current branch is not `slide/*` and publishing is enabled:
   - warn the user that the branch does not follow the slide branch convention
   - do not auto-publish unless the user explicitly confirms that branch is the intended PR branch

### Step 1: Parse the draft and inspect style (parallel)

Launch two agents in parallel in a single message:

**Agent A — draft-reader**
- Dispatch the `draft-reader` agent with:
  ```text
  TASK: extract
  FILE: <resolved draft path>
  ```
- Receive `CONTENT_SUMMARY` JSON.

**Agent B — style-inspector**
- Dispatch the `style-inspector` agent with:
  ```text
  TASK: inspect
  FILES: all
  ```
- Receive `STYLE_GUIDE` JSON.

### Step 2: Determine mode (create vs update)

1. Extract metadata from `CONTENT_SUMMARY`: `mode`, `slide_number`, `target_file`, `target_class`.
2. If `mode` is explicitly set in metadata, use it.
3. Otherwise, check whether a file with the `slide_number` prefix already exists in `slides/`.
   - If a match exists, use `update`.
   - If no match exists, use `create`.
4. If `slide_number` is null and mode is `create`:
   - scan `slides/` for the highest numbered slide
   - set `slide_number = max + 1`
   - derive `target_file` as `{NN}_{snake_case_title}.py`
   - derive `target_class` as `{CamelCaseTitle}Slide`

### Step 3: Query Context7 before writing slide code

Before dispatching `slide-builder` or `slide-updater`, query Context7 for:
- `manim-slides` APIs for `Slide`, `ThreeDSlide`, and transition control
- `manim` APIs for `MathTex`, `Tex`, `BulletedList`, `VGroup`, and animation primitives

If documentation conflicts with memory or repo habits, follow the retrieved docs.

### Step 4: Build or update the slide

**If mode = `create`:**
1. Dispatch `slide-builder` with:
   ```text
   TASK: build
   SLIDE_TITLE: <metadata.title>
   OUTPUT_FILE: <target_file>
   CONTENT_SUMMARY: <JSON from draft-reader>
   STYLE_GUIDE: <JSON from style-inspector>
   ADDITIONAL_INSTRUCTIONS: <metadata.additional_instructions + relevant Context7 notes>
   ```
2. Register the new slide in `slides.toml` in sorted numeric order.

**If mode = `update`:**
1. Dispatch `slide-updater` with:
   ```text
   TASK: update
   TARGET_FILE: <target_file>
   TARGET_CLASS: <target_class>
   CHANGE_DESCRIPTION: <derived from CONTENT_SUMMARY changes>
   CHANGE_TYPE: <metadata.update_type or inferred type>
   CONTENT_SUMMARY: <JSON from draft-reader>
   STYLE_GUIDE: <JSON from style-inspector>
   ADDITIONAL_INSTRUCTIONS: <metadata.additional_instructions + relevant Context7 notes>
   ```

### Step 5: Validate math

Skip this step if `--no-validate` was passed or if `CONTENT_SUMMARY` has no equations.

1. Dispatch `math-validator` with:
   ```text
   TASK: validate
   SCENE_FILE_CONTENT: <the scene file content>
   CONTENT_SUMMARY: <JSON from draft-reader>
   ```
2. If `validation_status` is `FAIL`:
   - report the errors
   - send only those fixes back to `slide-builder` or `slide-updater`
   - re-validate once
3. If `PASS` or `WARN`, continue and capture the result for the publish report.

### Step 6: Render

Skip if `--no-render` was passed.

1. Render the scene:
   ```bash
   uv run manim-slides render slides/<target_file> <TargetClass>
   ```
2. If render fails, report the error and stop before HTML conversion or publishing.

### Step 7: Convert to HTML

Skip if `--no-render` was passed or render failed.

1. Convert the scene:
   ```bash
   uv run manim-slides convert <TargetClass> presentation/<nn>_<name>.html -ccontrols=true
   ```

### Step 8: Validate layout

Skip if `--no-render` was passed, `--no-validate` was passed, or HTML conversion failed.

1. Dispatch `slide-layout-validator` with the generated HTML file path.
2. If high-severity issues are found, report them before publication.

### Step 9: Publish to a PR targeting `dev`

Skip this step if `--no-publish` was passed.

1. Determine the publication file scope:
   - always `slides/<target_file>`
   - include `slides.toml` if it changed
   - include the draft file only if the user expects the draft to ship with the slide
   - include directly related source files only
   - never include `media/` or `presentation/` output unless the user explicitly asked for generated artifacts in git
2. Build commit/PR metadata:
   - commit message: `feat(slides): add <topic>` for new slides
   - commit message: `feat(slides): update <topic>` for existing slides
   - PR title should mirror the change in concise imperative form
   - PR body must include draft path, cited LaTeX files, validation result, render result, and layout result
3. Dispatch `slide-publisher` with:
   ```text
   TASK: publish
   BASE_BRANCH: dev
   FEATURE_BRANCH: <current branch>
   SCENE_FILE: slides/<target_file>
   DRAFT_FILE: <resolved draft path or none>
   OPTIONAL_FILES: <comma-separated files or none>
   COMMIT_MESSAGE: <derived commit message>
   PR_TITLE: <derived PR title>
   PR_BODY_SUMMARY: <markdown summary>
   DRAFT_PR: <true if --draft-pr else false>
   UPDATE_EXISTING_PR: <true if --update-existing-pr else false>
   VALIDATION_STATUS: <PASS|WARN|skipped>
   RENDER_STATUS: <success|skipped>
   LAYOUT_STATUS: <pass|warn|skipped>
   ```
4. PR tool preference:
   - prefer the configured GitHub MCP/app in the Codex environment
   - if MCP PR tooling is unavailable, allow the publisher to fall back to `gh`
   - if neither path is available, report that the branch was pushed and PR creation still needs GitHub connectivity

### Step 10: Report

Summarize:
- draft file
- cited LaTeX files
- mode: `create` or `update`
- scene file
- math validation result
- render result
- layout validation result
- publication result: `skipped`, `pushed`, `pr created`, `pr updated`, or `manual follow-up required`
- next step only when blocked, for example `gh auth login` or GitHub MCP setup
