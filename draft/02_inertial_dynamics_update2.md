---
title: "Dinámica inercial del cuadricóptero (v2)"
slide_number: 2
mode: update
target_file: slides/02_inertial_dynamics.py
target_class: InertialDynamicsSlide
additional_instructions: |
  Apply all changes listed below. Preserve all unmentioned logic and animations.
  Use context7 for any Manim API questions. Each change references the current
  source section so the agent can locate the exact code to modify.
---

# Cambios al slide 02 — Dinámica inercial (v2)

## CHANGE 1 — Envolver "Dinámica de traslación: ..." y "Dinámica de rotación: ..." en bloques rectangulares (lines ~50–86)

Actualmente `translation_statement` y `rotation_statement` son objetos `Text` simples.
Deben envolverse en `RoundedRectangle` siguiendo la paleta canónica del proyecto.

### translation_statement → translation_statement_group

```python
translation_statement = Text(
    "Dinámica de traslación: Relación entre coordenadas inerciales y velocidades locales",
    font_size=22,
    color=WHITE,
)
translation_stmt_box = RoundedRectangle(
    corner_radius=0.2,
    width=translation_statement.width + 0.6,
    height=translation_statement.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
translation_statement_group = VGroup(translation_stmt_box, translation_statement).arrange(ORIGIN)
translation_statement_group.shift(UP * 2.5)
```

### rotation_statement → rotation_statement_group

```python
rotation_statement = Text(
    "Dinámica de rotación: La velocidad angular inercial se relaciona con la angular local\nmediante una transformación.",
    font_size=22,
    color=WHITE,
    line_spacing=1.3,
)
rotation_stmt_box = RoundedRectangle(
    corner_radius=0.2,
    width=rotation_statement.width + 0.6,
    height=rotation_statement.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
rotation_statement_group = VGroup(rotation_stmt_box, rotation_statement).arrange(ORIGIN)
rotation_statement_group.shift(DOWN * 0.2)
```

Actualizar todas las referencias a `translation_statement` y `rotation_statement` para
que apunten a `translation_statement_group` y `rotation_statement_group` respectivamente
(Write, FadeOut, etc.).

## CHANGE 2 — Reemplazar S_, C_, T_ con \sin, \cos, \tan en la matriz de rotación expandida (line ~136–143)

En la `MathTex` de `rotation_expanded`, sustituir cada abreviatura por la función trigonométrica explícita:

| Notación antigua | Notación nueva |
|---|---|
| `S_{\varphi}` | `\sin\varphi` |
| `C_{\varphi}` | `\cos\varphi` |
| `T_{\theta}` | `\tan\theta` |
| `C_{\theta}` | `\cos\theta` |
| `S_{\varphi}/C_{\theta}` | `\dfrac{\sin\varphi}{\cos\theta}` |
| `C_{\varphi}/C_{\theta}` | `\dfrac{\cos\varphi}{\cos\theta}` |

Matriz resultante en LaTeX:

$$\mathbf{W}_{\boldsymbol{\eta}} = \begin{bmatrix} 1 & \sin\varphi\tan\theta & \cos\varphi\tan\theta \\ 0 & \cos\varphi & -\sin\varphi \\ 0 & \dfrac{\sin\varphi}{\cos\theta} & \dfrac{\cos\varphi}{\cos\theta} \end{bmatrix}$$

El código resultante:

```python
rotation_expanded = MathTex(
    r"\begin{bmatrix} \dot{\varphi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = "
    r"\begin{bmatrix}"
    r"1 & \sin\varphi\tan\theta & \cos\varphi\tan\theta \\"
    r"0 & \cos\varphi & -\sin\varphi \\"
    r"0 & \dfrac{\sin\varphi}{\cos\theta} & \dfrac{\cos\varphi}{\cos\theta}"
    r"\end{bmatrix}"
    r"\begin{bmatrix} p \\ q \\ r \end{bmatrix}",
    font_size=26,
)
```

> Reducir `font_size` a 26 (desde 28) para que la matriz con fracciones quepa en pantalla.

## CHANGE 3 — Notas importantes dentro de bloques rectangulares

### 3a — "Matriz de cambio de coordenadas..." (brace label, line ~159–168)

El texto bajo la llave (`matrix_label_expanded`) actualmente es texto libre. Reemplazar
por un bloque rectangular que aparezca **debajo** de la ecuación expandida de rotación:

```python
matrix_note = Text(
    "W_η: matriz de cambio de coordenadas de la velocidad angular",
    font_size=18,
    color=GRAY_A,
)
matrix_note_box = RoundedRectangle(
    corner_radius=0.15,
    width=matrix_note.width + 0.5,
    height=matrix_note.height + 0.35,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
matrix_note_group = VGroup(matrix_note_box, matrix_note).arrange(ORIGIN)
matrix_note_group.next_to(rotation_expanded, DOWN, buff=0.35)
```

Eliminar la `Brace` y el `matrix_label_expanded` originales y sustituirlos por
`FadeIn(matrix_note_group)` / `FadeOut(matrix_note_group)` en los mismos puntos
donde estaban `Create(matrix_brace)` y su FadeOut.

## CHANGE 4 — Nota "No aparece una nueva ley dinámica" en bloque a la izquierda de las ecuaciones de traslación (after line ~220)

Después de que se muestren las ecuaciones de traslación expandidas
(`\dot{x} = u`, `\dot{y} = v`, `\dot{z} = w`), agregar un bloque rectangular
**a la izquierda** de esas ecuaciones con la siguiente nota:

```python
no_new_law_text = Text(
    "No aparece una nueva\nley dinámica:\nu, v, w son simplemente\nlas derivadas temporales\nde x, y, z.",
    font_size=18,
    color=WHITE,
    line_spacing=1.3,
)
no_new_law_box = RoundedRectangle(
    corner_radius=0.2,
    width=no_new_law_text.width + 0.5,
    height=no_new_law_text.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
no_new_law_group = VGroup(no_new_law_box, no_new_law_text).arrange(ORIGIN)
no_new_law_group.next_to(translation_eq, LEFT, buff=0.6)
```

Hacer `FadeIn(no_new_law_group)` con un `self.next_slide()` después, para que el
presentador pueda detenerse a explicar este punto antes de continuar.
Hacer `FadeOut(no_new_law_group)` cuando se pase a la sección siguiente.

> `translation_eq` aquí se refiere al objeto que en ese momento contiene
> `translation_equations` (la forma expandida `\dot{x} = u` etc.),
> ya que la variable se reutiliza vía `Transform`.

## CHANGE 5 — Frase "Junto con la dinámica local..." al fondo de la pantalla (after line ~222)

Reemplazar el `self.wait(3)` final por una frase de cierre posicionada al fondo:

```python
closing_text = Text(
    "Junto con la dinámica local, estas relaciones completan\n"
    "el sistema de ecuaciones de movimiento de primer orden.",
    font_size=20,
    color=GRAY_A,
    line_spacing=1.3,
)
closing_box = RoundedRectangle(
    corner_radius=0.2,
    width=closing_text.width + 0.6,
    height=closing_text.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
closing_group = VGroup(closing_box, closing_text).arrange(ORIGIN)
closing_group.to_edge(DOWN, buff=0.3)

self.play(FadeIn(closing_group), run_time=1)
self.next_slide()
self.play(FadeOut(closing_group), run_time=0.8)
```

<!-- speaker: Enfatizar que esta slide no introduce fuerzas nuevas. Su rol es transformar
velocidades entre marcos. El cierre conecta con la dinámica local de la slide anterior. -->
