---
title: "Slide Title Here"
slide_number: 14          # optional; auto-assigned if omitted
mode: create               # create | update; auto-detected if omitted
additional_instructions: "" # optional hints for slide-builder (e.g., "use 3D scene", "step-by-step equation reveal")
---

<!-- cite: LaTex/chapters/05_aprendizaje_por_diferencias_temporales.tex, sections: 5.1 -->

# Slide Title Here

## Section Name
- Bullet point concept
- Another concept

$$V(s_t) \leftarrow V(s_t) + \alpha \left[ r_{t+1} + \gamma V(s_{t+1}) - V(s_t) \right]$$

> **Definition**: The TD error measures the difference between the estimated
> value and the bootstrapped target.

## Another Section
- More concepts here

$$\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)$$

## Notation
- $V(s)$: State-value function
- $\alpha$: Learning rate
- $\gamma$: Discount factor
- $\delta_t$: TD error at time $t$

<!-- speaker: Explain how TD bridges MC and DP approaches -->
