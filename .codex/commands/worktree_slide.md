Prepare a dedicated slide branch and git worktree for a new Codex session: $ARGUMENTS

## Arguments

- Required: a slide identifier and topic slug, for example `14 td_learning`
- Optional: a full branch name such as `slide/14-td-learning`

## Instructions

1. Resolve the branch metadata:
   - If the user gave `NN topic_slug`, convert it to `slide/NN-topic-slug`
   - If the user gave a full `slide/...` branch name, use it directly

2. Ensure `dev` exists and tracks the remote:
   ```bash
   .codex/scripts/bootstrap_dev_branch.sh
   ```

3. Create or reuse a worktree from `dev`:
   ```bash
   .codex/scripts/prepare_slide_branch.sh --id <nn> --slug <topic_slug>
   ```
   or, when a full branch name was provided:
   ```bash
   .codex/scripts/prepare_slide_branch.sh --branch <branch_name>
   ```

4. Report:
   - the feature branch name
   - the worktree path
   - whether the worktree was created or reused
   - the next step: launch a dedicated `codex` session from that path, then run `/slide <draft-or-topic>`

5. Do not modify slide files in this command. This command only prepares the branch/worktree environment.
