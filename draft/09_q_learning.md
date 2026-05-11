---
title: "Q-learning"
slide_number: 9
mode: create
additional_instructions: "Use a grid-based TicTacToe board for the example. Animate the Q-table updates step by step. Reveal equations progressively. Use Spanish for all text labels."
---

<!-- cite: LaTex/chapters/05_aprendizaje_por_diferencias_temporales.tex, sections: Q-learning -->
<!-- cite: LaTex/chapters/10_metodos_analiticos_y_numericos.tex, sections: Método Robbins-Monro -->

# Q-learning

## Ecuacion optima de Bellman
- Q-learning resuelve directamente la ecuacion optima de Bellman en terminos de $Q_*$
- No requiere conocer un modelo del entorno

$$Q_{*}(x, u) = \mathbb{E}\left[R_{t+1} + \gamma \max_{u'} Q_{*}(X_{t+1}, u') \mid X_t = x, U_t = u\right]$$

## Metodo Robbins-Monro
- Metodo iterativo para encontrar raices de una funcion desconocida $g(w) = 0$
- Solo requiere observaciones ruidosas $\tilde{g}(w, \eta) = g(w) + \eta$
- Regla de actualizacion:

$$w_{k+1} = w_k - \alpha_k \tilde{g}(w_k, \eta_k)$$

- $\alpha_k$ satisface: $\sum \alpha_k^2 < \infty$ y $\sum \alpha_k \to \infty$ (convergencia garantizada)

## Derivacion de Q-learning via Robbins-Monro
- Se busca resolver $g(Q_*(x, u)) = 0$ donde:

$$g(Q_*(x, u)) = Q_*(x, u) - \mathbb{E}[R + \gamma \max_{u'} Q_*(X', u') \mid x, u]$$

- Sin acceso a probabilidades de transicion, se usa la observacion sesgada con muestras $r_k$, $x_k'$:

$$\tilde{g}(Q_*(x,u)) = Q_*(x, u) - [r_k + \gamma \max_{u'} Q_*(x_k', u')]$$

- Esta observacion se descompone en:

$$\tilde{g} = \underbrace{Q_*(x,u) - \mathbb{E}[R + \gamma \max_{u'} Q_*(X', u') \mid x, u]}_{g(Q_*(x,u))} + \underbrace{\mathbb{E}[\cdots] - [r_k + \gamma \max_{u'} Q_*(x_k', u')]}_{\eta}$$

- Aplicando RM se obtiene la regla de actualizacion de Q-learning:

$$Q^{(k+1)}(x, u) = Q^{(k)}(x, u) - \alpha_k \left( Q^{(k)}(x, u) - [r_k + \gamma \max_{u'} Q_*(x_k', u')] \right)$$

## Supuestos practicos (bootstrapping)
- En la practica no se puede fijar $(x, u)$ repetidamente: se usan muestras secuenciales $(x_t, u_t, r_{t+1}, x_{t+1})$
- No se conoce $Q_*$: se reemplaza por la estimacion actual $Q^{(k)}$
- Este proceso se llama **bootstrapping**
- Resultado final:

$$Q^{(k+1)}(x_t, u_t) = Q^{(k)}(x_t, u_t) + \alpha \left( r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t) \right)$$

## Error TD
- El error TD mide la discrepancia entre la estimacion actual y la observacion obtenida

$$\delta_t = r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t)$$

- Cuando $Q^{(k)} \approx Q_*$, el valor esperado del error TD es cero:

$$\mathbb{E}[\delta_t \mid X_t = x, U_t = u] = \mathbb{E}[R_{t+1} + \gamma \max_{u'} Q_*(X_{t+1}, u') \mid x, u] - Q_*(x, u) = 0$$

- La ultima igualdad se cumple por la ecuacion de Bellman: $Q_*$ satisface exactamente $Q_*(x,u) = \mathbb{E}[R_{t+1} + \gamma \max_{u'} Q_*(X_{t+1}, u') \mid x, u]$
- Si $\mathbb{E}[\delta_t] \neq 0$, la estimacion $Q^{(k)}$ aun no es optima y el algoritmo sigue corrigiendo
- Un error TD cercano a cero indica que la estimacion es consistente con la estructura de Bellman

## Exploracion vs Explotacion
- **Explotacion**: usar la mejor politica disponible para maximizar la recompensa
- **Exploracion**: probar acciones menos conocidas para descubrir mejores estrategias
- Politica $\epsilon$-greedy balancea ambos objetivos

$$\pi_{\epsilon}(u \mid x) = \begin{cases} \arg\max_{u'} Q^{(k)}(x, u') & \text{con prob. } 1 - \epsilon \\ u \in \mathcal{U}(x) & \text{con prob. } \epsilon \end{cases}$$

- Se reduce $\epsilon$ gradualmente (e.g., $\epsilon = 1/k$) para garantizar convergencia (politica GLIE)

## Algoritmo Q-learning con politica $\epsilon$-greedy
- **Datos**: $\alpha \in (0,1]$, $\gamma \in [0,1)$, $\epsilon_0 \in (0,1)$, $K$ episodios, espacios $\mathcal{X}$ y $\mathcal{U}(x)$
- **Resultado**: Estimaciones $Q^{(k)}$ y politica objetivo $\mu$
- Pasos:
  1. Inicializar $Q^{(0)}(x, u) = 0$ para todo $(x, u)$
  2. Para cada episodio $k = 1, \ldots, K$:
     - Definir $\epsilon_k$ con decaimiento (e.g., $\epsilon_k = \epsilon_0 / k$)
     - Inicializar estado $x_1$
     - Mientras $x_t$ no sea terminal:
       - Muestrear $u_t \sim \pi_{\epsilon_k}(\cdot | x_t)$
       - Ejecutar $u_t$, observar $r_{t+1}$ y $x_{t+1}$
       - $\delta_t = r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t)$
       - $Q^{(k+1)}(x_t, u_t) = Q^{(k)}(x_t, u_t) + \alpha \delta_t$
       - $x_t \leftarrow x_{t+1}$
  3. $\mu(x) = \arg\max_{u} Q^{(K)}(x, u)$ para todo $x$

## Ejemplo: TicTacToe
- Tablero de 3x3 como entorno con estados y acciones finitos
- El agente (jugador X) aprende a jugar contra un oponente aleatorio
- La Q-tabla almacena valores $Q(x, u)$ para cada estado-accion
- Mostrar una partida donde el agente:
  1. Observa el estado del tablero $x_t$
  2. Selecciona una casilla $u_t$ usando $\pi_\epsilon$
  3. Recibe recompensa: $r = +1$ (ganar), $r = -1$ (perder), $r = 0$ (empate o continuar)
  4. Actualiza $Q(x_t, u_t)$ con la regla de Q-learning
- Animar la Q-tabla actualizandose tras cada jugada para ilustrar el aprendizaje

<!-- speaker: Comenzar con la ecuacion de Bellman optima. Introducir Robbins-Monro como herramienta para resolver g(w)=0 sin conocer g. Mostrar como se aplica RM a la ecuacion de Bellman: definir g(Q*), construir la observacion sesgada, y obtener la regla de actualizacion. Explicar los supuestos practicos (bootstrapping). Presentar el error TD y su interpretacion. Mostrar el algoritmo completo. Usar TicTacToe para hacer tangible el aprendizaje: la Q-tabla se actualiza tras cada jugada. Cerrar con exploracion vs explotacion y epsilon-greedy. -->
