---
title: "GPS: Búsqueda Guiada de Política"
slide_number: 15
mode: update
update_type: restructure
target_file: slides/15_gps.py
target_class: GPSSlide
---

# GPS: Búsqueda Guiada de Política — Update

## Overview of changes

Four structural changes to `GPSSlide` in `slides/15_gps.py`:

1. **Move "Idea central" to the bottom** — currently the first content section after the title; move it to be the last section (after "Configuración experimental").
2. **New section "Objetivo GPS"** — insert immediately after the title, before "Distribuciones".
3. **"Ciclo de entrenamiento GPS"** — invert image colors (dark-on-white → white-on-black) and replace the five floating text labels with numbered visual markers overlaid on the image.
4. **"Actualizaciones BADMM"** — instead of fading each update out before showing the next, fade them in and stack them: θ first, then p below it, then λ below p. All three remain visible simultaneously.

---

## Section order after this update

1. Title
2. **Objetivo GPS** ← new
3. Distribuciones
4. Ciclo de entrenamiento GPS ← image inverted, markers added
5. Actualizaciones BADMM ← stacked fade-in
6. Costo aumentado para iLQR
7. Configuración experimental
8. **Idea central** ← moved from position 2 to here

---

## Change 1 — New section: Objetivo GPS

Insert this section right after the title block and before the "Distribuciones" section.

### Content

**Section label:** `"Objetivo"` — `font_size=30, color=BLUE_B`

**Objective box** (single `RoundedRectangle` with `make_box`):

> Encontrar una política global $\pi_{\boldsymbol{\theta}}(\mathbf{u}_t | \mathbf{x}_t)$ que minimice el costo esperado de trayectoria mediante la coordinación de controladores locales $p_i(\mathbf{u}_t | \mathbf{x}_t)$, forzando su convergencia con restricciones de Lagrange.

Font size 24, color WHITE, line_spacing 1.3.

**Transition:** FadeIn label → next_slide → FadeIn box + text → next_slide → FadeOut all.

---

## Change 2 — Invert image colors in "Ciclo de entrenamiento GPS"

The image at `GPS_SCHEMA` has a white background with dark strokes/text. The slide background is black, which creates a jarring white rectangle. Invert the image so that:
- White background → black (matches slide background)
- Dark strokes, arrows, and text → white or light gray

### Implementation

Add a helper function at module level (alongside `GPS_SCHEMA`), following the same PIL pattern used in `slides/00_portrait.py`:

```python
def _invert_image(path) -> ImageMobject:
    """Invert a dark-on-white diagram to white-on-black for dark slide background."""
    from PIL import Image, ImageOps
    import numpy as np
    img = Image.open(str(path)).convert("RGBA")
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    inverted = ImageOps.invert(rgb)
    result = Image.merge("RGBA", (*inverted.split(), a))
    return ImageMobject(result)
```

Replace the `ImageMobject(str(GPS_SCHEMA))` call with `_invert_image(GPS_SCHEMA)`.

---

## Change 3 — Replace text labels with numbered visual markers in "Ciclo de entrenamiento GPS"

Remove `lbl1` through `lbl5` (the five `Text` mobjects and the `MathTex` in `lbl2`). Replace them with numbered step markers: a filled circle containing the step number, positioned near the corresponding part of the diagram cycle. Use a small `Arrow` (or none if the circle can sit directly on the element) to anchor each marker visually.

### Marker style

Each marker is a `VGroup` of:
- `Circle(radius=0.28, color=BLUE_B, fill_opacity=1)` as the badge background
- `Text(str(n), font_size=18, color=WHITE)` centered inside the circle

```python
def make_step_marker(n: int) -> VGroup:
    circle = Circle(radius=0.28, color=BLUE_B, fill_opacity=1, stroke_width=0)
    label  = Text(str(n), font_size=18, color=WHITE)
    label.move_to(circle.get_center())
    return VGroup(circle, label)
```

### Marker positions (relative to `diagram` ImageMobject)

The GPS diagram shows a clockwise cycle. Position each marker badge near the relevant region of the image:

| Step | Diagram region | Suggested position expression |
|------|---------------|-------------------------------|
| 1 | iLQR / local controllers (top-left arc) | `diagram.get_left() + RIGHT*1.0 + UP*1.4` |
| 2 | Trajectory database (bottom arc) | `diagram.get_bottom() + UP*0.6 + LEFT*1.8` |
| 3 | Global policy training (top-right arc) | `diagram.get_right() + LEFT*1.2 + UP*1.4` |
| 4 | Dual variable update (bottom-right arc) | `diagram.get_bottom() + UP*0.6 + RIGHT*1.8` |
| 5 | Iteration counter k = k+1 (top center) | `diagram.get_top() + DOWN*0.45` |

### Animation sequence

Reveal one marker per `next_slide`, same rhythm as the old text labels:

```
FadeIn(diag_label), FadeIn(diagram_frame), FadeIn(diagram) → next_slide
FadeIn(marker_1) → next_slide
FadeIn(marker_2) → next_slide
FadeIn(marker_3) → next_slide
FadeIn(marker_4) → next_slide
FadeIn(marker_5) → next_slide
FadeOut all → wait(0.3)
```

---

## Change 4 — Stack BADMM updates (no FadeOut between steps)

Currently each update (θ, p, λ) fades out before the next one appears. Instead, show them as a growing list: fade θ in, pause, fade p in below θ, pause, fade λ in below p. All three remain on screen until the final FadeOut.

### Layout

Build a single `VGroup` to hold all three rows; reveal each row individually with a separate `self.play` + `self.next_slide`:

```
badmm_label  (UP*2.8)
──────────────────────────────────────
row_theta:   [theta_desc  /  theta_eq + theta_box]
row_p:       [p_desc      /  p_eq     + p_box    ]
row_lambda:  [lambda_desc /  lambda_eq + lambda_box]
```

Each row is a `VGroup(desc, VGroup(box, eq))` arranged `DOWN, buff=0.15, aligned_edge=LEFT`.  
Rows are arranged with `VGroup(row_theta, row_p, row_lambda).arrange(DOWN, buff=0.35, aligned_edge=LEFT)` and placed below `badmm_label` with `buff=0.4`.

Font sizes may need to shrink to fit — use `font_size=20` for `desc` and `font_size=22` for the equations, and apply `shrink_to_fit_width` to each equation with `config.frame_width - 1.4`.

### Animation

```
FadeIn(badmm_label) → wait(0.3)
FadeIn(theta_desc, theta_box, theta_eq) → wait(0.5) → next_slide
FadeIn(p_desc, p_box, p_eq)             → wait(0.5) → next_slide
FadeIn(lambda_desc, lambda_box, lambda_eq) → wait(0.5) → next_slide
FadeOut(badmm_label, all rows) → wait(0.3)
```

The `lambda_box` retains the highlight style: `color=BLUE_B, fill_opacity=0.12, stroke_width=2`.

---

## Change 5 — Move "Idea central" to the bottom

Move the existing "Idea central" block verbatim (no content changes) to after the "Configuración experimental" section. It becomes the last section before `self.wait(1)`.

The closing `Text` ("GPS combina la precisión local...") that currently follows `config_box` should remain attached to the config section and stay in place.

After moving, "Idea central" has no trailing `FadeOut` — the slide ends there. Replace `FadeOut(idea_box, idea_group)` with a final `self.wait(1)`.
