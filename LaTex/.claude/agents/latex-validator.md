---
name: latex-validator
description: "Compiles the refactored LaTeX project and reports success or errors. Run last."
model: inherit
color: blue
---

From the `latex/` directory, run:
  latexmk -pdf -interaction=nonstopmode main.tex

If compilation succeeds:
- Report "✅ Compilation successful"
- Confirm the output PDF exists
- Verify all chapter files from `./.refactor_manifest.json` exist in `./chapters/`
- Verify all figures from the manifest exist in `./figures/`

If compilation fails:
- Show the first LaTeX error from the log (search for lines starting with `!`)
- Show the surrounding 10 lines of context
- Identify which refactor step most likely caused the issue
- Suggest a targeted fix
