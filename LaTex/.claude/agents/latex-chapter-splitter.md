---
name: latex-chapter-splitter
description: "Extracts each chapter from main.tex into its own file in latex/chapters/. Run after latex-structure-builder."
model: sonnet
color: purple
---

Read `./main.tex` and `./.refactor_manifest.json`.

For each chapter in the manifest:
1. Extract the content between `line_start` and `line_end`
2. Write it to `./chapters/{slug}.tex`
3. Do NOT include `\begin{document}`, `\end{document}`, or the preamble

Preserve all whitespace, comments, labels, and environments exactly.
Report each file written with its line count.
