---
title: "iLQR: Regulador Cuadrático Lineal Iterativo"
slide_number: 13
mode: update
target_file: slides/13_ilqr.py
target_class: ILQRSlide
update_type: content_addition
additional_instructions: "Keep the new sections already added from the LaTeX source: (1) Control Óptimo before Motivación, (2) Función de valor V and Bellman equation, (3) Programación dinámica / iteración de valores, and (4) the full iLQR algorithm pseudocode at the end. In addition, restore the conceptual diagrams that were present in the previous visual version. Do not remove the current equations; instead, combine equations with compact diagrams that make the information flow easier to explain. Prefer side-by-side or stacked layouts that stay Beamer-like and uncluttered."
---

<!-- cite: LaTex/chapters/02_teoria_de_control.tex, sections: Control óptimo, Programación dinámica: Iteración de valores, iLQR -->

# iLQR: Regulador Cuadrático Lineal Iterativo

## Control Óptimo (NEW — keep)

Context for optimal control: find a trajectory that minimizes cost subject to dynamics.

$$\min_{\mathbf{u}_0, \cdots, \mathbf{u}_{T-1}} \sum_{t=0}^{T} c(\mathbf{x}_t, \mathbf{u}_t) \quad \text{s.t.} \quad \mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)$$

- $c: \mathcal{X} \times \mathcal{U} \to \mathbb{R}^+$: costo instantáneo
- $c(\boldsymbol{\tau})$: costo acumulado de la trayectoria

## Función de valor V (NEW — keep)

> **Definition**: La función de valor óptima $V_*$ satisface la ecuación de Bellman:

$$V_*(\mathbf{x}_t) = \min_{\mathbf{u}_t \in \mathcal{U}(\mathbf{x}_t)} \left\{ \underbrace{c(\mathbf{x}_t, \mathbf{u}_t) + V_*(\mathbf{x}_{t+1})}_{Q(\mathbf{x}_t, \mathbf{u}_t)} \right\}$$

where $\mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)$ and $V_*(\mathbf{x}_T) = c(\mathbf{x}_T, \mathbf{0})$.

- $Q(\mathbf{x}_t, \mathbf{u}_t)$: función de valor de la acción — costo inmediato + costo óptimo futuro

## Programación Dinámica: Iteración de Valores (NEW — keep)

- Principio de optimalidad de Bellman: si una secuencia es óptima, toda subsecuencia también lo es
- Iteración de valores resuelve la ecuación de Bellman recursivamente

$$V_{k+1}(\mathbf{x}) = \min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}$$

Ley de control óptimo:

$$\mu_{k+1}(\mathbf{x}) = \arg\min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}$$

## Motivación (EXISTING — keep as-is)

## Hipótesis (EXISTING — keep as-is)

## Trayectoria nominal (EXISTING — keep equation, ADD diagram)

- Preserve the nominal trajectory equation already in the slide.
- Restore a compact diagram that visually shows the sequence of nominal pairs
  $(\hat{\mathbf{x}}_1,\hat{\mathbf{u}}_1), (\hat{\mathbf{x}}_2,\hat{\mathbf{u}}_2), \ldots, (\hat{\mathbf{x}}_T,\hat{\mathbf{u}}_T)$
  along a horizontal time axis.
- Overlay one current state-control pair $(\mathbf{x}_t,\mathbf{u}_t)$ near the nominal one and show the deviations
  $\bar{\mathbf{x}}_t = \mathbf{x}_t - \hat{\mathbf{x}}_t$ and
  $\bar{\mathbf{u}}_t = \mathbf{u}_t - \hat{\mathbf{u}}_t$
  with short arrows or braces.
- The point of the diagram is to make “coordenadas relativas” visually obvious, not only algebraic.

## Aproximación lineal de la dinámica (EXISTING — keep equations, ADD local linearization sketch)

- Preserve the Taylor / Jacobian equations already in the slide.
- Add a small conceptual sketch that communicates:
  1. nonlinear dynamics $f$ around the nominal trajectory,
  2. a local tangent / linear approximation near $(\hat{\mathbf{x}}_t,\hat{\mathbf{u}}_t)$,
  3. the fact that the approximation changes with time.
- The diagram can be abstract; it does not need to be a full state-space plot.
- Emphasize visually that $\mathbf{A}_t$ and $\mathbf{B}_t$ are local derivatives evaluated on the nominal trajectory.

## Aproximación cuadrática del costo (EXISTING — keep equations, ADD curvature sketch)

- Preserve the quadratic approximation and partition of $\mathbf{C}_t$ and $\mathbf{c}_t$.
- Add a small cost-shape diagram to contrast:
  1. original nonlinear cost surface or curve,
  2. local quadratic bowl approximation near the nominal point.
- Use the diagram only to convey “cuadratizar costo localmente”; keep it simple.

## Backward Pass (EXISTING — keep equations, ADD recursion-flow diagram)

- Preserve boundary condition, $\mathbf{Q}_t$, $\mathbf{q}_t$, control law, gains, and value-function update.
- Restore a timeline-style backward recursion diagram over the horizon:
  $T \rightarrow T-1 \rightarrow \cdots \rightarrow 0$.
- The diagram should show information propagating backward from terminal cost toward earlier times.
- Mark that each step produces $(\mathbf{K}_t, \mathbf{k}_t)$ and updates $(\mathbf{V}_t, \mathbf{v}_t)$.
- The goal is to make “plan backward from the end” immediately readable before discussing formulas.

## Forward Pass (EXISTING — keep equations, ADD rollout diagram)

- Preserve the forward-pass equations and the note that a new nominal trajectory is produced.
- Restore a left-to-right rollout diagram:
  $\mathbf{x}_0 \rightarrow \mathbf{u}_0 \rightarrow \mathbf{x}_1 \rightarrow \cdots \rightarrow \mathbf{x}_T$.
- Show that controls are updated using
  $\alpha \mathbf{k}_t + \mathbf{K}_t(\mathbf{x}_t - \hat{\mathbf{x}}_t)$
  and then propagated through the true nonlinear dynamics $f$.
- Make the contrast with the backward pass clear:
  backward = compute gains, forward = simulate / rollout a new trajectory.

## Búsqueda de línea (EXISTING — keep equations, ADD alpha-selection diagram)

- Preserve the control update with $\alpha$ and the convergence criterion.
- Restore a compact visual for line search, for example one of:
  1. a mini plot of cost vs. $\alpha$,
  2. a ladder of candidate values $\alpha \in \{1, \tfrac{1}{2}, \tfrac{1}{4}, \ldots\}$ with the accepted step highlighted.
- The diagram should make clear that line search reduces step size when a full step is too aggressive.

## Regularización (EXISTING — keep equations, ADD stabilization diagram)

- Preserve the regularized $\tilde{\mathbf{Q}}_{\mathbf{uu}_t}$ and $\tilde{\mathbf{Q}}_{\mathbf{ux}_t}$ equations and the $\lambda$ update rules.
- Restore a small diagram that explains why regularization is needed:
  1. problematic Hessian / curvature,
  2. add $\lambda \mathbf{I}$,
  3. obtain a better-conditioned positive-definite matrix.
- If space allows, show the qualitative effect of increasing vs decreasing $\lambda$ with two arrows.

## Algoritmo iLQR (REPLACE existing summary with full algorithm, ADD global cycle diagram)

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

- Add one final compact “big picture” diagram or cycle:
  trayectoria nominal
  → linealizar/cuadratizar
  → backward pass
  → forward rollout
  → line search / regularización
  → nueva trayectoria nominal.
- This closing visual should unify the earlier local diagrams into one full iteration loop.

<!-- speaker: Keep the new theoretical sections. When discussing the core iLQR mechanics, recover the missing diagrams so the audience can see the flow of information: nominal trajectory and local coordinates, backward recursion from terminal cost, forward rollout of a new trajectory, step-size selection by line search, and conditioning via regularization. The diagrams should support explanation, not compete with the equations. -->
