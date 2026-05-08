---
name: slide
description: "Create or update a Manim slide from a markdown draft file in ./draft/. Orchestrates draft-reader, style-inspector, slide-builder/updater, math-validator, and slide-layout-validator agents. Use when the user wants to turn a draft into a presentation slide."
user-invocable: true
allowed-tools: Bash(uv run:*) Read Write Edit Agent
argument-hint: "<draft-file-or-topic> [--no-render] [--no-validate]"
---

Create or update a Manim slide from a markdown draft: $ARGUMENTS

## Arguments

- A path to a markdown file in `./draft/` (e.g., `draft/14_td_learning.md`)
- OR a topic name that matches an existing draft file (e.g., `td_learning`)
- Optional flag: `--no-render` to skip rendering and layout validation
- Optional flag: `--no-validate` to skip math and layout validation

## Instructions

### Step 0: Resolve the draft file

1. Parse `$ARGUMENTS` to separate the file/topic from flags (`--no-render`, `--no-validate`).
2. If the argument is a file path (contains `/` or ends with `.md`), use it directly.
3. If it is a topic name, glob for `draft/*{topic}*.md`.
4. If no match is found, list available drafts in `./draft/` and ask the user which one to use.
5. Read the draft file to confirm it exists and has content.

### Step 1: Parse the draft and inspect style (PARALLEL)

Launch **two agents in parallel** in a single message:

**Agent A — draft-reader:**
- Dispatch the `draft-reader` agent with:
  ```
  TASK: extract
  FILE: <resolved draft path>
  ```
- Receive CONTENT_SUMMARY JSON (including metadata and cited_files).

**Agent B — style-inspector:**
- Dispatch the `style-inspector` agent with:
  ```
  TASK: inspect
  FILES: all
  ```
- Receive STYLE_GUIDE JSON.

Both agents run in parallel since they have no dependencies on each other.

### Step 2: Determine mode (create vs update)

1. Extract metadata from CONTENT_SUMMARY: `mode`, `slide_number`, `target_file`, `target_class`.
2. If `mode` is explicitly set in metadata, use it.
3. Otherwise, check if a file with the `slide_number` prefix exists in `slides/`:
   - Run: `ls slides/ | grep "^$(printf '%02d' $slide_number)_"`
   - If a match exists → mode = `update`; extract target_file and target_class from the existing file
   - If no match → mode = `create`
4. If `slide_number` is null and mode is `create`:
   - Scan `slides/` for the highest NN prefix: `ls slides/*.py | sort -n | tail -1`
   - Set slide_number = max(NN) + 1
   - Derive `target_file` as `{NN}_{snake_case_title}.py`
   - Derive `target_class` as `{CamelCaseTitle}Slide`

### Step 3: Query context7 MCP

Before dispatching slide-builder or slide-updater, query the `context7` MCP server for:
- `manim-slides` API reference (slide transitions, ThreeDSlide usage)
- `manim` API reference (MathTex, BulletedList, VGroup, animations)

This satisfies the repo instruction requirement to ground generated code in Context7 references.

### Step 4: Build or update the slide

**If mode = `create`:**
1. Dispatch the `slide-builder` agent with:
   ```
   TASK: build
   SLIDE_TITLE: <metadata.title>
   OUTPUT_FILE: <target_file>
   CONTENT_SUMMARY: <JSON from Step 1 Agent A>
   STYLE_GUIDE: <JSON from Step 1 Agent B>
   ADDITIONAL_INSTRUCTIONS: <metadata.additional_instructions + relevant context7 API refs>
   ```
2. After the agent produces the `.py` file, register the new slide in `slides.toml`:
   - Read current `slides.toml`
   - Insert the new entry `slides/{target_file}.{TargetClass}Slide` at the correct position (sorted by NN prefix)
   - Write updated `slides.toml`

**If mode = `update`:**
1. Dispatch the `slide-updater` agent with:
   ```
   TASK: update
   TARGET_FILE: <target_file>
   TARGET_CLASS: <target_class>
   CHANGE_DESCRIPTION: <derived from CONTENT_SUMMARY changes>
   CHANGE_TYPE: <metadata.update_type or infer from content>
   CONTENT_SUMMARY: <JSON from Step 1 Agent A>
   STYLE_GUIDE: <JSON from Step 1 Agent B>
   ADDITIONAL_INSTRUCTIONS: <metadata.additional_instructions + relevant context7 API refs>
   ```

### Step 5: Validate math

Skip if `--no-validate` was passed or if CONTENT_SUMMARY has no equations.

1. Dispatch the `math-validator` agent with:
   ```
   TASK: validate
   SCENE_FILE_CONTENT: <the .py file produced in Step 4>
   CONTENT_SUMMARY: <JSON from Step 1 Agent A>
   ```
2. If `validation_status` is `FAIL`:
   - Report the specific errors
   - Dispatch back to `slide-builder` or `slide-updater` to fix only the flagged equations
   - Re-validate (max 1 retry)
3. If `PASS` or `WARN`: proceed (report warnings to user).

### Step 6: Render

Skip if `--no-render` was passed.

1. Render the scene:
   ```bash
   uv run manim-slides render slides/<target_file>
   ```
2. If render fails, report the error with stderr output. Do not proceed to HTML conversion.

### Step 7: Convert to HTML

Skip if `--no-render` was passed or Step 6 failed.

1. Convert to HTML:
   ```bash
   uv run manim-slides convert <TargetClass>Slide presentation/<nn>_<name>.html -ccontrols=true
   ```

### Step 8: Validate layout

Skip if `--no-render` was passed, `--no-validate` was passed, or Step 7 failed.

1. Dispatch the `slide-layout-validator` agent with the generated HTML file path.
2. If high-severity issues are found, report them to the user with specific element names and issue types.

### Step 9: Report

Summarize what was done:
- Draft file: `<path>`
- Cited LaTeX files: `<list or none>`
- Mode: `create` / `update`
- Scene file: `slides/<target_file>`
- Math validation: `PASS` / `WARN` / `FAIL` / `skipped`
- Render: `success` / `failed` / `skipped`
- Layout validation: `<results>` / `skipped`
- Suggest next steps: `/commit_push` to save changes
