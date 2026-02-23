---
name: latex-main-patcher
description: "Rewrites main.tex to use \\input{} calls and adds \\graphicspath. Run after latex-figure-mover."
model: sonnet
color: cyan
---

Read `./.refactor_manifest.json` for chapter order and slugs.

Rewrite `./main.tex`:
1. Back up the original to `./main.tex.bak`
2. Keep the full preamble intact
3. Add `\graphicspath{{figures/}}` just before `\begin{document}` if not already present
4. Inside `\begin{document}...\end{document}`, replace each chapter's raw content with `\input{chapters/{slug}}` in the correct order
5. Keep any front matter (`\maketitle`, `\tableofcontents`, etc.) and back matter (`\bibliography`, `\appendix`, etc.) in place

Report the final structure of main.tex (preamble line count, input calls, back matter).
