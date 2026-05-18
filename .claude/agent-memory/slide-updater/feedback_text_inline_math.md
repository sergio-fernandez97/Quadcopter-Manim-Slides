---
name: text-inline-math
description: How to embed inline LaTeX math inside Manim Text() objects
metadata:
  type: feedback
---

To embed inline math in a `Text()` object, use dollar-sign LaTeX syntax with a raw string:

```python
Text(
    r"$\mathbf{W}_{\boldsymbol{\eta}}$ transforma la velocidad angular local al sistema inercial.",
    font_size=20,
    color=GRAY_B,
)
```

Or mixing plain text and math on multiple lines:

```python
Text(
    "No aparece una nueva ley dinámica: $u$, $v$, $w$ son simplemente\n"
    "las derivadas temporales de $x$, $y$, $z$.",
    font_size=20,
    color=GRAY_B,
    line_spacing=1.3,
)
```

**Why:** Manim's `Text()` class supports inline LaTeX via `$...$` dollar syntax. This avoids switching to `MathTex` for prose text that contains occasional math symbols.

**How to apply:** Use this pattern for secondary body notes (GRAY_B, font_size=20) that mix Spanish prose with math variables. Always use raw string prefix `r"..."` when the string contains backslashes.
