---
title: "Dinámica de traslación y rotación local"
slide_number: 1
mode: update
update_type: content
target_file: slides/01_newton_euler.py
target_class: NewtonEulerSlide
additional_instructions: "Do not rewrite the slide from scratch. Apply only the four targeted changes described below. Preserve all existing equation transforms, color assignments, and section ordering."
---

<!-- cite: LaTex/chapters/01_introduccion.tex, sections: Ecuaciones de movimiento -->

# Dinámica de traslación y rotación local — Update 2

## Overview of changes

Four surgical changes to `NewtonEulerSlide` in `slides/01_newton_euler.py`:

1. **Remove `newton_box`** — delete the `RoundedRectangle` around Newton's equation and the `Create(newton_box)` call.
2. **Add inertia matrix step** — after `rotation_expanded` is shown, insert a new step that displays the explicit inertia matrix `I` before transitioning to scalar angular velocities.
3. **Shift both equations left + show constants table** — after both `linear_velocities_expanded` and `angular_velocities_expanded` are on screen, animate them and their labels to the left half and reveal the constants table on the right.

---

## Change 1 — Remove `newton_box`

Delete the `newton_box` `RoundedRectangle` definition (the block that creates it) and remove `Create(newton_box)` from the `self.play(...)` call that introduces Newton's law.

The `newton_statement` label and `newton_eq_initial` equation remain unchanged — only the box is removed.

---

## Change 2 — Inertia matrix step inside "velocidades angulares"

### Where to insert

After the existing `self.play(Transform(euler_eq, rotation_expanded), run_time=1.5)` + `self.wait(1)` + `self.next_slide()` block, and **before** the `Transform` to `angular_velocities`.

### What to add

Display the inertia matrix `I` (from `eq:inertia_matrix` in the LaTeX) so the audience can see its diagonal structure before it is inverted. Show it as a separate labeled step to the right of, or below, the current `rotation_expanded` equation.

#### Label

```python
inertia_label = Text("Matriz de inercia:", font_size=22, color=GRAY_A)
```

#### Equation (from eq:inertia_matrix)

```python
inertia_eq = MathTex(
    r"\mathbf{I} = \begin{bmatrix} I_{xx} & 0 & 0 \\ 0 & I_{yy} & 0 \\ 0 & 0 & I_{zz} \end{bmatrix}",
    font_size=28,
)
```

Note from LaTeX: the matrix is diagonal because the quadcopter has a symmetric structure with respect to the xz and yz planes, giving `I_xx = I_yy`.

#### Layout

Place `inertia_label` + `inertia_eq` as a `VGroup(...).arrange(RIGHT, buff=0.3)` centered below the current `rotation_expanded`, with `buff=0.35` between them. Wrap with `make_box` (or equivalent `RoundedRectangle` with `color=BLUE_D, fill_opacity=0.12, stroke_width=1.5`).

#### Animation

```
self.play(FadeIn(inertia_label), FadeIn(inertia_box), FadeIn(inertia_eq))
self.wait(0.5)
self.next_slide()
self.play(FadeOut(inertia_label), FadeOut(inertia_box), FadeOut(inertia_eq))
self.wait(0.2)
```

Then continue with the existing `Transform(euler_eq, angular_velocities)` block.

---

## Change 3 — Shift both equations left + constants table

### Where to insert

This replaces the final section starting from the existing `angular_velocities_expanded` transform onward (after `self.next_slide()` that follows `angular_velocities_expanded`). The two brief "closing" text notes (`linear_close` and `angular_close`) are removed and replaced by this new combined finale.

### Step-by-step

After `angular_velocities_expanded` is on screen (both `newton_eq` holding linear vels and `euler_eq` holding angular vels are visible simultaneously):

#### 3a — Animate equations and labels to the left half

```python
self.play(
    newton_eq.animate.scale(0.75).to_edge(LEFT, buff=0.4).shift(UP * 0.5),
    linear_label.animate.scale(0.75).to_edge(LEFT, buff=0.4).shift(UP * 2.5),
    euler_eq.animate.scale(0.75).to_edge(LEFT, buff=0.4).shift(DOWN * 1.5),
    angular_label.animate.scale(0.75).to_edge(LEFT, buff=0.4).shift(DOWN * 0.0),
    run_time=1.2,
)
self.wait(0.4)
```

Exact positions may need slight adjustment during rendering; keep equations left-aligned and non-overlapping.

#### 3b — Constants table (right half)

Build the table as a `VGroup` of rows. Each row is a `VGroup` of `MathTex` (symbol) + `Text` (value + unit + meaning) arranged horizontally. All rows are stacked with `arrange(DOWN, buff=0.18, aligned_edge=LEFT)`.

**Table header:**

```python
table_title = Text("Constantes del modelo", font_size=22, color=BLUE_B)
```

**Table data** (from `tab:quadcopter_cons` in the LaTeX):

| Symbol | Value | Unit | Meaning |
|--------|-------|------|---------|
| $g$ | $9.81$ | $\text{m·s}^{-2}$ | constante de gravitación |
| $m$ | $0.468$ | $\text{kg}$ | masa del cuadricóptero |
| $\ell$ | $0.225$ | $\text{m}$ | distancia rotor–centro de masa |
| $b$ | $2.98 \times 10^{-6}$ | $-$ | coeficiente de arrastre |
| $k$ | $1.14 \times 10^{-7}$ | $-$ | coeficiente de elevación |
| $I_{xx}$ | $4.856 \times 10^{-3}$ | $\text{kg·m}^2$ | inercia eje $x$ |
| $I_{yy}$ | $4.856 \times 10^{-3}$ | $\text{kg·m}^2$ | inercia eje $y$ |
| $I_{zz}$ | $8.801 \times 10^{-3}$ | $\text{kg·m}^2$ | inercia eje $z$ |

**Implementation pattern:**

Each row uses `MathTex` for the symbol and value/unit, and `Text` for the meaning. Use `font_size=18` throughout the table to fit all eight rows. Symbols and values must use `MathTex`, not `Text` (per project math-rendering rule).

```python
def table_row(sym, val, unit, meaning):
    s = MathTex(sym,  font_size=18, color=YELLOW)
    v = MathTex(val,  font_size=18, color=WHITE)
    u = MathTex(unit, font_size=18, color=GRAY_A)
    m = Text(meaning, font_size=16, color=GRAY_A)
    return VGroup(s, v, u, m).arrange(RIGHT, buff=0.25)
```

Stack all rows into a `VGroup` with `arrange(DOWN, buff=0.15, aligned_edge=LEFT)`.

Place `table_title` above the rows with `buff=0.3`, then wrap the `VGroup(table_title, rows)` in a `make_box`-style `RoundedRectangle(color=BLUE_D, fill_opacity=0.12, stroke_width=1.5)`.

Position the entire table group `.to_edge(RIGHT, buff=0.4)` and vertically centered.

#### 3c — Animation

```
self.play(FadeIn(table_title), FadeIn(table_box), FadeIn(table_rows))
self.wait(0.5)
self.next_slide()
self.play(
    FadeOut(newton_eq), FadeOut(linear_label),
    FadeOut(euler_eq),  FadeOut(angular_label),
    FadeOut(table_title), FadeOut(table_box), FadeOut(table_rows),
)
self.wait(0.3)
```

---

## What to preserve unchanged

- All existing sections before the `angular_velocities_expanded` transform: title, idea central, opening statement, Newton/Euler statement+equations, forces note, linear velocity expansion chain.
- Color assignments: `linear_velocity_color = YELLOW`, `angular_velocity_color = BLUE`.
- The existing `newton_statement` and its `Write` animation.
- The existing `rotation_expanded` transform and its `next_slide`.
- The `explanation_linear` and `explanation_angular` helper texts and their `FadeOut` calls.
