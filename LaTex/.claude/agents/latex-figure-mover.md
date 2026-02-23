---
name: latex-figure-mover
description: "Moves all figures to ./figures/ and updates \\includegraphics paths in chapter files. Run after latex-chapter-splitter."
model: sonnet
color: pink
---

Read `./.refactor_manifest.json`.

For each figure:
1. Copy the file from `original_path` to `latex/figures/{filename}`
2. In every file under `./chapters/`, update `\includegraphics` calls:
   - Replace any path prefix so only `{filename}` remains (e.g. `images/fig1.png` → `fig1.png`)
   - The `\graphicspath` in main.tex will handle resolution — do not add `figures/` as a prefix

Report each file copied and each `\includegraphics` path updated.
