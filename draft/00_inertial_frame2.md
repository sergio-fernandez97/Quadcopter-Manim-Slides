---
title: "Marco inercial y local del cuadricóptero (v2)"
slide_number: 0
mode: update
target_file: slides/00_inertial_frame.py
target_class: InertialFrameSlide
additional_instructions: |
  Apply every change listed in the sections below to the existing InertialFrameSlide.
  Preserve all unmentioned logic and animations unchanged. Use context7 for any
  Manim / manim-slides API questions. Changes are grouped by section number matching
  the current source file.
---

# Cambios al slide 00 — Marco inercial y local (v2)

## CHANGE 1 — Título "Ángulos de Euler" (SECTION 3, line ~149)

Cambiar el texto del título de la sección de Euler de plural incorrecto a plural correcto:

- **Antes**: `"Ángulo de Euler"`
- **Después**: `"Ángulos de Euler"`

## CHANGE 2 — Orden de animaciones en SECTION 3: FadeIn del título DESPUÉS del FadeOut del cuadricóptero

Actualmente el `euler_title` hace FadeIn **antes** del FadeOut de la sección 1-2.
Debe invertirse el orden:

1. Primero ejecutar el FadeOut de todos los elementos de la sección anterior:
   `title`, `def_group`, `axes`, `x_label`, `y_label`, `z_label`, `quadcopter`,
   `x_arrow`, `y_arrow`, `z_arrow`, `omega1_label`, `omega2_label`, `omega3_label`, `omega4_label`.
2. **Después** del FadeOut, hacer `FadeIn(euler_title)` con el texto corregido `"Ángulos de Euler"`.
3. El `self.next_slide()` va después del FadeIn del título.

El bloque de código resultante debe quedar así (pseudocódigo):
```python
# Fade out sections 1–2
self.play(FadeOut(title), FadeOut(def_group), FadeOut(axes), ..., FadeOut(omega4_label), run_time=1)
# THEN fade in the Euler title
euler_title = Text("Ángulos de Euler", font_size=32, color=YELLOW).to_edge(UP, buff=0.5)
self.add_fixed_in_frame_mobjects(euler_title)
self.play(FadeIn(euler_title), run_time=1)
self.next_slide()
```

## CHANGE 3 — Reemplazar notación C_, S_ con \cos, \sin en todas las matrices (SECTION 3 & 4)

En las tres matrices elementales y en la `combined_matrix`, sustituir todas las abreviaturas:

| Notación antigua | Notación nueva |
|---|---|
| `C_{\varphi}` | `\cos\varphi` |
| `S_{\varphi}` | `\sin\varphi` |
| `C_{\theta}` | `\cos\theta` |
| `S_{\theta}` | `\sin\theta` |
| `C_{\psi}` | `\cos\psi` |
| `S_{\psi}` | `\sin\psi` |

Matrices resultantes en LaTeX:

$$\mathbf{R}(\varphi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\varphi & \sin\varphi \\ 0 & -\sin\varphi & \cos\varphi \end{bmatrix}$$

$$\mathbf{R}(\theta) = \begin{bmatrix} \cos\theta & 0 & -\sin\theta \\ 0 & 1 & 0 \\ \sin\theta & 0 & \cos\theta \end{bmatrix}$$

$$\mathbf{R}(\psi) = \begin{bmatrix} \cos\psi & \sin\psi & 0 \\ -\sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

Matriz combinada:

$$\mathbf{R}(\psi,\theta,\varphi) = \begin{bmatrix} \cos\psi\cos\theta & \cos\psi\sin\theta\sin\varphi - \sin\psi\cos\varphi & \cos\psi\sin\theta\cos\varphi + \sin\psi\sin\varphi \\ \sin\psi\cos\theta & \sin\psi\sin\theta\sin\varphi + \cos\psi\cos\varphi & \sin\psi\sin\theta\cos\varphi - \cos\psi\sin\varphi \\ -\sin\theta & \cos\theta\sin\varphi & \cos\theta\cos\varphi \end{bmatrix}$$

> Usar `font_size=18` para la combined_matrix para que quepa en pantalla.

## CHANGE 4 — Etiquetas pequeñas para ℓ, k, b en su primera aparición (SECTION 3)

Cuando se muestran los torques por primera vez (`roll_torque` y `yaw_torque`),
agregar pequeñas etiquetas (Text, font_size=14, color=GRAY_A) que expliquen los
constantes la primera vez que aparecen.

**Junto con `roll_torque`** (`τ_φ = ℓk(ω₄² − ω₂²)`), agregar debajo del torque:

```python
label_ell = Text("ℓ: longitud del brazo", font_size=14, color=GRAY_A)
label_k   = Text("k: coeficiente de empuje", font_size=14, color=GRAY_A)
VGroup(label_ell, label_k).arrange(DOWN, buff=0.05).next_to(roll_torque, DOWN, buff=0.12)
```

Hacer FadeIn de estas etiquetas junto con `roll_torque`. Hacer FadeOut junto con
`roll_torque` cuando se limpie la sección.

**Junto con `yaw_torque`** (`τ_ψ = b Σ(-1)^{i+1} ω_i²`), agregar:

```python
label_b = Text("b: coeficiente de arrastre", font_size=14, color=GRAY_A)
label_b.next_to(yaw_torque, DOWN, buff=0.12)
```

Hacer FadeIn de `label_b` junto con `yaw_torque`. Hacer FadeOut junto con `yaw_torque`.

> Los tres mobjects (label_ell, label_k, label_b) deben ser registrados con
> `add_fixed_in_frame_mobjects`.

## CHANGE 5 — Simplificar animación de combinación de matrices y posicionar debajo del eje z (SECTION 4)

### 5a — No hacer "volar" las matrices hacia mult_expr

Reemplazar el bloque de animación actual (que mueve `roll_matrix`, `pitch_matrix`,
`yaw_matrix` hacia `mult_expr`) por una secuencia más limpia:

```python
# Fade out the three individual matrices directly
self.play(
    FadeOut(roll_matrix), FadeOut(pitch_matrix), FadeOut(yaw_matrix),
    run_time=1,
)
```

### 5b — Mostrar mult_expr una sola vez, abajo centrado bajo el eje z

Posicionar `mult_expr` con coordenadas de pantalla fijas (fixed-in-frame) que lo
coloquen en la parte baja de la pantalla, debajo del punto donde proyecta el eje z:

```python
mult_expr = MathTex(
    r"\mathbf{R}(\psi) \cdot \mathbf{R}(\theta) \cdot \mathbf{R}(\varphi)",
    font_size=28,
).move_to(np.array([0, -2.8, 0]))
self.add_fixed_in_frame_mobjects(mult_expr)
self.play(FadeIn(mult_expr), run_time=1)
self.next_slide()
```

### 5c — Posicionar combined_matrix también debajo del eje z

```python
combined_matrix = MathTex(
    r"\mathbf{R}(\psi,\theta,\varphi) = \begin{bmatrix} \cdots \end{bmatrix}",
    font_size=18,
).move_to(np.array([0, -3.0, 0]))
self.add_fixed_in_frame_mobjects(combined_matrix)
self.play(Transform(mult_expr, combined_matrix), run_time=2)
self.next_slide()
```

> Ambas expresiones deben estar en coordenadas de pantalla (`add_fixed_in_frame_mobjects`)
> y centradas horizontalmente en x=0, con y ≈ -2.8 a -3.0 (fondo de pantalla).

## CHANGE 6 — Una sola etiqueta "Empuje en la dirección z"; FadeOut al entrar "Sistema de referencia local" (SECTION 5)

### 6a — Eliminar el texto duplicado

Actualmente existen dos objetos con texto `"Empuje en la dirección z"`:
- `empuje_label` (posicionado arriba-izquierda)
- `thrust_label` (debajo de `thrust_eq`)

**Eliminar `thrust_label` completamente** — no crear este objeto ni hacer FadeIn de él.
Mantener solo `empuje_label`.

### 6b — FadeOut de empuje_label al entrar a SECTION 7

Cuando se hace FadeIn de `title_local` ("Sistema de referencia local"),
incluir `empuje_label` en el mismo `FadeOut`:

```python
self.play(
    FadeIn(title_local),
    FadeOut(empuje_label),   # ← agregar esta línea
    FadeIn(sistema_local_desc_group),
    run_time=1,
)
```

## CHANGE 7 — Texto "Marco Inercial {I}..." en bloque rectangular al fondo de pantalla (SECTION 6)

Reemplazar el `sistema_inercial_desc` actual (posicionado a la izquierda) por un
bloque de texto enmarcado en la parte inferior de la pantalla.

Texto actualizado: `"Marco Inercial {I}: Marco fijo global. Posición y orientación absolutas."`

Construcción:
```python
sistema_inercial_desc = Text(
    "Marco Inercial {I}: Marco fijo global. Posición y orientación absolutas.",
    font_size=18,
    color=WHITE,
)
inertial_box = RoundedRectangle(
    corner_radius=0.15,
    width=sistema_inercial_desc.width + 0.6,
    height=sistema_inercial_desc.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
inertial_desc_group = VGroup(inertial_box, sistema_inercial_desc).arrange(ORIGIN)
inertial_desc_group.to_edge(DOWN, buff=0.25)
self.add_fixed_in_frame_mobjects(inertial_desc_group)
self.play(FadeIn(inertial_desc_group), run_time=1)
```

Hacer FadeOut de `inertial_desc_group` cuando se sale de la sección inercial
(junto con los vectores ξ y η).

## CHANGE 8 — Mover etiqueta "posición angular" (η) más a la izquierda, cerca del centro (SECTION 6)

Actualmente `pos_angular_label` usa `to_edge(RIGHT, buff=1)` lo que empuja la
etiqueta y los vectores η fuera de la pantalla. Reposicionar el grupo completo:

```python
pos_angular_label = Text(
    "posición angular", font_size=24, color=WHITE,
).move_to(np.array([1.5, 0.5, 0]))   # más cerca del centro, no en el borde derecho
vector_eta_label = MathTex(
    r"\boldsymbol{\eta} = ", font_size=32,
).next_to(pos_angular_label, RIGHT, buff=0.3)
vector_eta_matrix = MathTex(
    r"\begin{bmatrix} \varphi \\ \theta \\ \psi \end{bmatrix}", font_size=32,
).next_to(vector_eta_label, RIGHT, buff=0.1)
```

> El grupo "posición lineal" (ξ) queda a la izquierda (`to_edge(LEFT, buff=1)`).
> El grupo "posición angular" (η) queda en el centro-derecha (`x ≈ 1.5`).
> Esto los hace visibles simultáneamente en pantalla.

## CHANGE 9 — Texto "Marco local {B}..." en bloque rectangular al fondo de pantalla (SECTION 7)

Mismo tratamiento que el cambio 7, pero para el sistema local:

```python
sistema_local_desc = Text(
    "Marco Local {B}: Marco fijo al vehículo. Velocidades lineales y angulares relativas.",
    font_size=18,
    color=WHITE,
)
local_box = RoundedRectangle(
    corner_radius=0.15,
    width=sistema_local_desc.width + 0.6,
    height=sistema_local_desc.height + 0.4,
    color=BLUE_D,
    fill_opacity=0.12,
    stroke_width=1.5,
)
local_desc_group = VGroup(local_box, sistema_local_desc).arrange(ORIGIN)
local_desc_group.to_edge(DOWN, buff=0.25)
self.add_fixed_in_frame_mobjects(local_desc_group)
```

Hacer FadeIn de `local_desc_group` cuando se muestra el título "Sistema de referencia
local" (junto con el FadeOut de `empuje_label` del cambio 6b).

Hacer FadeOut de `local_desc_group` al final de la sección local.

<!-- speaker: Recorrer primero la sección inercial enfatizando los vectores ξ y η, luego pasar al marco local mostrando υ y ω. El bloque al fondo ancla visualmente el nombre del marco en todo momento. -->
