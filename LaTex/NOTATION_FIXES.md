# Notation Consistency Analysis - Proposed Fixes

**Document:** PhD/Master's Thesis on Quadcopter Control using Deep Reinforcement Learning
**Analysis Date:** 2026-03-28

---

## Critical Notation Rules

| Concept | Correct Notation | Description |
|---------|-----------------|-------------|
| Initial state | $\mathbf{x}_0$ | Bold, subscript 0 |
| Initial action | $\mathbf{u}_0$ | Bold, subscript 0 |
| Final state | $\mathbf{x}_T$ | Bold, subscript T |
| Final action | $\mathbf{u}_{T-1}$ | Bold, subscript T-1 |
| Trajectory | T+1 states, T actions | States indexed 0 to T, actions indexed 0 to T-1 |

---

## Summary of Issues Found

| Chapter | Issues | Priority |
|---------|--------|----------|
| Chapter 02 | Wrong trajectory indexing (starts at 1, ends at T+1) | High |
| Chapter 03 | Uses lowercase x, u instead of bold | High |
| Chapter 04 | Wrong initial state index (x_1 instead of x_0) | High |
| Chapter 05 | Wrong initial state index; non-bold in algorithms | High |
| Chapter 06 | Wrong initial state index (x_1 instead of x_0) | High |
| Chapter 09 | Uses `\textbf{}` instead of `\mathbf{}` | Medium |

---

## Detailed Fixes by Chapter

### Chapter 02: Teoría de Control

#### Issue 1: Initial state index should start at 0
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/02_teoria_de_control.tex:150` | `$\mathbf{x}_{1}$` | `$\mathbf{x}_{0}$` |

**Explanation:** Initial state should be $\mathbf{x}_0$, not $\mathbf{x}_1$.

---

#### Issue 2: Trajectory definition uses wrong indexing
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/02_teoria_de_control.tex:152` | `$\bm\tau = \{\mathbf{x}_{1}, \mathbf{u}_1, \mathbf{x}_2, \cdots, \mathbf{u}_{T}, \mathbf{x}_{T+1}\}$` | `$\bm\tau = \{\mathbf{x}_{0}, \mathbf{u}_0, \mathbf{x}_1, \cdots, \mathbf{u}_{T-1}, \mathbf{x}_{T}\}$` |

**Explanation:** A trajectory with T actions should have T+1 states indexed 0 to T, and T actions indexed 0 to T-1.

---

#### Issue 3: Final state uses $\mathbf{x}_{T+1}$ instead of $\mathbf{x}_T$
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/02_teoria_de_control.tex:157-160` | `$\mathbf{x}_{T+1}$` | `$\mathbf{x}_{T}$` |

**Explanation:** Final state should be $\mathbf{x}_T$, not $\mathbf{x}_{T+1}$.

---

#### Issue 4: Cost function summation indices
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/02_teoria_de_control.tex:157` | `$\sum_{t=1}^{T+1} c(\mathbf{x}_t, \mathbf{u}_t)$` | `$\sum_{t=0}^{T} c(\mathbf{x}_t, \mathbf{u}_t)$` |

**Explanation:** Summation should start at t=0 and end at t=T (accounting for T+1 states).

---

#### Issue 5: Bellman equation boundary condition
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/02_teoria_de_control.tex:183` | `$V_{*}(\mathbf{x}_{T+1})=c(\mathbf{x}_{T+1}, \bm{0})$` | `$V_{*}(\mathbf{x}_{T})=c(\mathbf{x}_{T}, \bm{0})$` |

**Explanation:** Terminal cost should be evaluated at $\mathbf{x}_T$.

---

### Chapter 03: Aprendizaje por Refuerzo

#### Issues 6-9: State/Action notation uses lowercase instead of bold

Replace all lowercase state/action variables with bold notation:

| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/03_aprendizaje_por_refuerzo.tex:30` | `$x_t$`, `$u_t$` | `$\mathbf{x}_t$`, `$\mathbf{u}_t$` |
| `chapters/03_aprendizaje_por_refuerzo.tex:34` | `$x_t$`, `$u_t$` | `$\mathbf{x}_t$`, `$\mathbf{u}_t$` |
| `chapters/03_aprendizaje_por_refuerzo.tex:40` | `$x_t$`, `$u_t$` | `$\mathbf{x}_t$`, `$\mathbf{u}_t$` |
| `chapters/03_aprendizaje_por_refuerzo.tex:43` | `$x_t$`, `$u_t$` | `$\mathbf{x}_t$`, `$\mathbf{u}_t$` |
| `chapters/03_aprendizaje_por_refuerzo.tex:45` | `$x_0 \xrightarrow{u_0} x_1$` | `$\mathbf{x}_0 \xrightarrow{\mathbf{u}_0} \mathbf{x}_1$` |
| `chapters/03_aprendizaje_por_refuerzo.tex:56` | `\bm\tau = \{x_0, u_0, r_1, x_1, \cdots\}` | `\bm\tau = \{\mathbf{x}_0, \mathbf{u}_0, r_1, \mathbf{x}_1, \cdots\}` |
| `chapters/03_aprendizaje_por_refuerzo.tex:63` | `\mathbf{E} = \{x_0, u_0, \cdots, x_{T}\}` | `\mathbf{E} = \{\mathbf{x}_0, \mathbf{u}_0, \cdots, \mathbf{x}_{T}\}` |

**Explanation:** For consistency with control theory notation in Chapter 02 and continuous spaces, states and actions should use bold notation $\mathbf{x}$ and $\mathbf{u}$.

---

### Chapter 04: Búsqueda Guiada de Políticas GPS

#### Issue 10: Initial state distribution uses wrong index
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/04_busqueda_guiada_de_politicas_gps.tex:27` | `$p_{i}(\mathbf{x}_1)$` | `$p_{i}(\mathbf{x}_0)$` |

**Explanation:** Initial state distribution should reference $\mathbf{x}_0$.

---

#### Issue 11: Trajectory distribution summation indices
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/04_busqueda_guiada_de_politicas_gps.tex:27` | `$\prod_{t=1}^{T-1}$` | `$\prod_{t=0}^{T-1}$` |

**Explanation:** Product should start at t=0.

---

#### Issue 12: Cost summation indices
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/04_busqueda_guiada_de_politicas_gps.tex:22` | `$\sum_{t=1}^{T} c(\mathbf{x}_t, \mathbf{u}_t)$` | `$\sum_{t=0}^{T-1} c(\mathbf{x}_t, \mathbf{u}_t)$` |

**Explanation:** With T actions (indices 0 to T-1) and T+1 states (indices 0 to T), cost should sum from t=0 to T-1.

---

#### Issue 13: Trajectory set definition
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/04_busqueda_guiada_de_politicas_gps.tex:358` | `t\in \{1, \cdots, T\}` | `t\in \{0, \cdots, T\}` |

**Explanation:** Trajectory should start at t=0.

---

### Chapter 05: Aprendizaje por Diferencias Temporales

#### Issues 14-17: Algorithm uses non-bold notation and wrong initial index

| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/05_aprendizaje_por_diferencias_temporales.tex:117` | `Inicializar estado $x_1 \in \mathcal{X}$` | `Inicializar estado $\mathbf{x}_0 \in \mathcal{X}$` |
| `chapters/05_aprendizaje_por_diferencias_temporales.tex:118` | `$x_t \in \mathcal{X}$` | `$\mathbf{x}_t \in \mathcal{X}$` |
| `chapters/05_aprendizaje_por_diferencias_temporales.tex:119` | `$u_t \sim \pi(\cdot|x_t)$` | `$\mathbf{u}_t \sim \pi(\cdot|\mathbf{x}_t)$` |
| `chapters/05_aprendizaje_por_diferencias_temporales.tex:125` | `Ejecutar $u_t$, observar $r_{t+1}$ y $x_{t+1}$` | `Ejecutar $\mathbf{u}_t$, observar $r_{t+1}$ y $\mathbf{x}_{t+1}$` |
| `chapters/05_aprendizaje_por_diferencias_temporales.tex:304` | `Recibir observación inicial $\mathbf{x}_1$` | `Recibir observación inicial $\mathbf{x}_0$` |

**Explanation:** Q-learning algorithm should use bold notation and start at index 0.

---

### Chapter 06: Aplicación y Evaluación de Métodos RL

#### Issue 18: Initial state sampling uses wrong index
| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/06_aplicacion_y_evaluacion_de_metodos_rl.tex:165` | `posición inicial $\mathbf{x}_1 \in \mathcal{X}$` | `posición inicial $\mathbf{x}_0 \in \mathcal{X}$` |

**Explanation:** Episode should start with initial state $\mathbf{x}_0$.

---

### Chapter 09: Redes Neuronales Artificiales

#### Issues 19-21: Uses `\textbf{}` instead of `\mathbf{}` for vectors

| Location | Current | Proposed Fix |
|----------|---------|--------------|
| `chapters/09_redes_neuronales_artificiales.tex:27` | `$f_a(\textbf{x}; \bm{\theta})$` | `$f_a(\mathbf{x}; \bm{\theta})$` |
| `chapters/09_redes_neuronales_artificiales.tex:169` | `$(\textbf{x}, \textbf{y})$` | `$(\mathbf{x}, \mathbf{y})$` |
| `chapters/09_redes_neuronales_artificiales.tex:180` | `$p(x, y)$` | `$p(\mathbf{x}, \mathbf{y})$` |

**Explanation:** `\textbf{}` is for text mode bold. Mathematical vectors should use `\mathbf{}` in math mode.

---

## Indexing Summary Table

| Concept | Chapter 02 (Current) | Chapter 03 (Current) | Correct |
|---------|---------------------|----------------------|---------|
| Initial state index | 1 | 0 | **0** |
| Initial action index | 1 | 0 | **0** |
| Final state index | T+1 | T | **T** |
| Final action index | T | T-1 | **T-1** |
| State notation | $\mathbf{x}_t$ ✓ | $x_t$ ✗ | **$\mathbf{x}_t$** |
| Action notation | $\mathbf{u}_t$ ✓ | $u_t$ ✗ | **$\mathbf{u}_t$** |

---

## Recommended Global Changes

### 1. Consistent Bold Notation for State/Action Vectors

**Find and replace across all chapters:**

| Find | Replace |
|------|---------|
| `$x_0$` (as state) | `$\mathbf{x}_0$` |
| `$x_t$` (as state) | `$\mathbf{x}_t$` |
| `$x_T$` (as state) | `$\mathbf{x}_T$` |
| `$u_0$` (as action) | `$\mathbf{u}_0$` |
| `$u_t$` (as action) | `$\mathbf{u}_t$` |
| `$u_{T-1}$` (as action) | `$\mathbf{u}_{T-1}$` |

**Note:** Be careful not to replace when $x$ refers to a scalar variable (not state vector).

### 2. Trajectory Indexing Convention

**Standard convention:** States $\{\mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_T\}$ (T+1 states) and actions $\{\mathbf{u}_0, \mathbf{u}_1, \ldots, \mathbf{u}_{T-1}\}$ (T actions).

**Update all trajectory definitions to reflect:**
- Initial state: $\mathbf{x}_0$
- Final state: $\mathbf{x}_T$
- Initial action: $\mathbf{u}_0$
- Final action: $\mathbf{u}_{T-1}$

### 3. Add Notation Clarification Note

Consider adding a notation note at the beginning of Chapter 03 or in the preamble:

```latex
% Notation: Throughout this document, bold symbols ($\mathbf{x}$, $\mathbf{u}$) denote
% vector-valued states and actions in continuous spaces. The trajectory consists of
% T+1 states $\{\mathbf{x}_0, \ldots, \mathbf{x}_T\}$ and T actions $\{\mathbf{u}_0, \ldots, \mathbf{u}_{T-1}\}$.
```

---

## Verification Steps

After implementing fixes, verify:

1. **Consistent bold notation:** All state/action variables use `\mathbf{x}` and `\mathbf{u}`
2. **Correct indexing:** Initial state $\mathbf{x}_0$, final state $\mathbf{x}_T$, final action $\mathbf{u}_{T-1}$
3. **Trajectory sums:** Cost summations use indices $t=0$ to $T-1$ (for T actions)
4. **Cross-references:** Update any references to trajectory indexing

---

**Report generated by:** Claude Code Analysis Team
**Date:** 2026-03-28