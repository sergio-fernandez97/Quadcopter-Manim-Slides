# LaTeX Refactor Project

## Project Goal
Refactor a monolithic `main.tex` into a modular structure using `\input{}` directives,
with chapters in `./chapters/` and figures in `./figures/`.

## Target Structure
```

main.tex
chapters/
├── 01_introduction.tex
├── 02_background.tex
└── ...
figures/
└── ... (all images)
```

## Rules
- Preserve ALL original LaTeX content exactly — no edits to prose or math
- Each chapter file must be self-contained (no `\begin{document}`)
- `main.tex` retains preamble + replaces chapter bodies with `\input{chapters/XX_name}`
- Add `\graphicspath{{figures/}}` to preamble
- All `\includegraphics` paths must be updated to just `{filename}` (no subdirectory)
- Do not break cross-references (`\label`, `\ref`, `\cite`)
- Shared state between agents lives in `./.refactor_manifest.json`
- After refactoring, the document must compile with `latexmk -pdf main.tex` from `./`

## Validation
Run `latexmk -pdf -interaction=nonstopmode main.tex` from `./` to verify.