---
title: "Política para control continuo"
slide_number: 12
update_target: slides/12_continuous_policy.py
---

# Política para control continuo

## Slide 1 — Title
- Title: "Política para control continuo"

## Slide 2 — Discrete vs Continuous comparison
- Left box (gray): **MDP discreto y finito** — $\pi(u|x) = \mathbb{P}[U_t = u \,|\, X_t = x]$, $u \in \mathcal{U},\ x \in \mathcal{X}$
- Right box (blue): **Control continuo** — $\pi(\mathbf{u}|\mathbf{x}) = p(\mathbf{u} \,|\, \mathbf{x})$, $\mathbf{u} \in \mathbb{R}^m,\ \mathbf{x} \in \mathbb{R}^n$

## Slide 3 — Quadcopter context note
- Note (yellow): Cuadricóptero: $n = 12$ (estado), $m = 4$ (rotores)

## Slide 4 — Stochastic parametrized policy

> **Política estocástica parametrizada**

$$\pi_{\boldsymbol{\theta}}(\mathbf{u}|\mathbf{x}) := \mathcal{N}\left(\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta}), \boldsymbol{\Sigma}(\mathbf{x})\right)$$

**PR feedback**: Add a label at the bottom of this box reading "Normal multivariada" (in a subtle color, e.g., GRAY_B or BLUE_C) to clarify that $\mathcal{N}$ refers to a Multivariate Normal distribution.

- $\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta})$: media (acción esperada) [GREEN]
- $\boldsymbol{\Sigma}(\mathbf{x})$: covarianza (exploración) [ORANGE]

## Slide 5 — Neural network for $\boldsymbol{\mu}$

$$\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta}) = f_{\boldsymbol{\theta}}(\mathbf{x})$$

**Red neuronal completamente conectada** with:
- 3-zone horizontal layout: theta box (left) | network diagram (center) | ANN equations (right)
- Network: 4 layers [4, 6, 6, 4] neurons, colors [BLUE, PURPLE, PURPLE, GREEN]
- Theta box (yellow): $\boldsymbol{\theta} = \left(\mathbf{W}^{[\ell]}, \mathbf{b}^{[\ell]}\right)_{\ell=1}^{L} \in \Theta$ — "pesos y sesgos por capa"
- ANN equations:
  - $f_a(\mathbf{x}; \boldsymbol{\theta}) := \phi \circ T_L \circ \phi \circ T_{L-1} \circ \cdots \circ \phi \circ T_1(\mathbf{x})$
  - $T_{\ell}(\mathbf{z}) = \mathbf{W}^{[\ell]}\mathbf{z} + \mathbf{b}^{[\ell]}$
  - $\mathbf{W}^{[\ell]} \in \mathbb{R}^{n_{\ell} \times n_{\ell-1}},\ \mathbf{b}^{[\ell]} \in \mathbb{R}^{n_{\ell}}$
