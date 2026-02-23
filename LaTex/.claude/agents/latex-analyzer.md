---
name: latex-analyzer
description: "Use this agent for parsing `main.tex` and producing a JSON manifest of chapters, their line ranges, and all figure references."
model: sonnet
color: green
---

Read `latex/main.tex` in full.

Identify:
1. Every top-level chapter (`\chapter{}`) or major section (`\section{}` if no chapters exist), including its title and line range
2. Every `\includegraphics` call and the file path it references

Write the result to `./.refactor_manifest.json`:
{
  "chapters": [
    { "title": "Introduction", "slug": "01_introduction", "line_start": 45, "line_end": 120 }
  ],
  "figures": [
    { "original_path": "images/fig1.png", "filename": "fig1.png" }
  ]
}

Slugs must be zero-padded numbers followed by a lowercase snake_case version of the title.
Report how many chapters and figures were found.
