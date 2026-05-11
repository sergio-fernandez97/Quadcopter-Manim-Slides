---
title: "iLQR: Regulador Cuadrático Lineal Iterativo"
slide_number: 13
mode: update
target_file: slides/13_ilqr.py
target_class: ILQRSlide
update_type: content_addition
additional_instructions: "Add missing sections from the LaTeX source. Insert them in logical order: (1) Optimal Control context before Motivation, (2) Value function V and Bellman equation after Motivation, (3) Value Iteration section, (4) replace the summary algorithm at the end with the full iLQR algorithm pseudocode. Keep existing sections (hypotheses, nominal trajectory, Taylor linearization, quadratic cost, backward pass, forward pass, line search, regularization) as-is."
---

<!-- cite: LaTex/chapters/02_teoria_de_control.tex, sections: Control óptimo, Programación dinámica: Iteración de valores, iLQR -->

# iLQR: Regulador Cuadrático Lineal Iterativo

## Control Óptimo (NEW — insert before Motivation)

Context for optimal control: find a trajectory that minimizes cost subject to dynamics.

$$\min_{\mathbf{u}_0, \cdots, \mathbf{u}_{T-1}} \sum_{t=0}^{T} c(\mathbf{x}_t, \mathbf{u}_t) \quad \text{s.t.} \quad \mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)$$

- $c: \mathcal{X} \times \mathcal{U} \to \mathbb{R}^+$: costo instantáneo
- $c(\boldsymbol{\tau})$: costo acumulado de la trayectoria

## Función de valor V (NEW — insert after Optimal Control)

> **Definition**: La función de valor óptima $V_*$ satisface la ecuación de Bellman:

$$V_*(\mathbf{x}_t) = \min_{\mathbf{u}_t \in \mathcal{U}(\mathbf{x}_t)} \left\{ \underbrace{c(\mathbf{x}_t, \mathbf{u}_t) + V_*(\mathbf{x}_{t+1})}_{Q(\mathbf{x}_t, \mathbf{u}_t)} \right\}$$

where $\mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)$ and $V_*(\mathbf{x}_T) = c(\mathbf{x}_T, \mathbf{0})$.

- $Q(\mathbf{x}_t, \mathbf{u}_t)$: función de valor de la acción — costo inmediato + costo óptimo futuro

## Programación Dinámica: Iteración de Valores (NEW — insert after V definition)

- Principio de optimalidad de Bellman: si una secuencia es óptima, toda subsecuencia también lo es
- Iteración de valores resuelve la ecuación de Bellman recursivamente

$$V_{k+1}(\mathbf{x}) = \min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}$$

Ley de control óptimo:

$$\mu_{k+1}(\mathbf{x}) = \arg\min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}$$

## Motivación (EXISTING — keep as-is)

## Hipótesis (EXISTING — keep as-is)

## Trayectoria nominal (EXISTING — keep as-is)

## Aproximación lineal de la dinámica (EXISTING — keep as-is)

## Aproximación cuadrática del costo (EXISTING — keep as-is)

## Backward Pass (EXISTING — keep as-is)

## Forward Pass (EXISTING — keep as-is)

## Búsqueda de línea (EXISTING — keep as-is)

## Regularización (EXISTING — keep as-is)

## Algoritmo iLQR (REPLACE existing summary with full algorithm)

Replace the current "Resumen del algoritmo iLQR" numbered-list summary with a proper pseudocode-style algorithm presentation that matches Algorithm 2 from the LaTeX:

**Algoritmo iLQR:**
```
Mientras no haya convergencia:
  1. Linealizar dinámica y cuadratizar costo:
     F_t = ∇f(x̂_t, û_t),  c_t = ∇c(x̂_t, û_t),  C_t = ∇²c(x̂_t, û_t)

  2. Backward pass: para t = T-1, ..., 0:
     Q_t = C_t + F_t^T V_{t+1} F_t
     q_t = c_t + F_t^T v_{t+1}
     K_t = -Q̃_uu^{-1} Q̃_ux
     k_t = -Q̃_uu^{-1} q̃_u
     V_t, v_t ← actualizar función de valor

  3. Forward pass con búsqueda de línea:
     u_t = û_t + α k_t + K_t(x_t - x̂_t)
     x_{t+1} = f(x_t, u_t)

  4. Verificar convergencia: |c(τ) - c(τ̂)| / c(τ̂) < ε_tol
  5. Actualizar trayectoria nominal: x̂_t ← x_t, û_t ← u_t
```

<!-- speaker: Walk through the algorithm step by step, emphasizing the alternation between backward (planning) and forward (execution) passes, and how line search + regularization ensure stability -->
