---
title: "DDPG: Deep Deterministic Policy Gradient"
slide_number: 14
mode: create
additional_instructions: "Use Spanish for all labels. Use the diagram from LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/ddpg_algorithm.png (figure fig:ddpg_schema). Structure the slide as a sequence of concise beats: actor-critic overview, actor equations, critic equations, stabilization mechanisms, then finish with the LaTeX algorithm as the closing block."
---

<!-- cite: LaTex/chapters/05_aprendizaje_por_diferencias_temporales.tex, sections: DDPG, Distribución de estados con descuento, Actor-Crítico, Actor: Deterministic Policy Gradient, Crítico: Deep Q-learning, Política de comportamiento, Algoritmo -->

# DDPG: Deep Deterministic Policy Gradient

## Motivación
- DDPG extiende Q-learning a tareas de control continuo
- Combina un actor determinista con un crítico que aproxima $Q$
- Es un método **off-policy** con redes neuronales, replay buffer y redes objetivo

## Distribución de estados con descuento
- La optimización del actor y del crítico depende de estados visitados bajo una política de comportamiento $\beta$
- La frecuencia de visitas ponderada por descuento se define como:

$$\rho_{\beta}(\mathbf{x}') = \int_{\mathcal{X}}\sum_{i=1}^{\infty}\gamma^{i-1}\rho_{0}(\mathbf{x})\rho_{\beta}\left(\mathbf{x}\rightarrow \mathbf{x}', i\right)d\mathbf{x}$$

- Para la pareja estado-acción:

$$\rho_{\beta}(\mathbf{x}, \mathbf{u}) = \beta(\mathbf{u}|\mathbf{x})\rho_{\beta}(\mathbf{x})$$

- Esta notación permite expresar las esperanzas del actor y del crítico usando muestras de experiencia

## Actor-Crítico
- **Usar el diagrama** `LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/ddpg_algorithm.png` (`fig:ddpg_schema`)
- **Actor**: política determinista $\mu(\mathbf{x}; \bm\theta_{\mu})$
- **Crítico**: aproximación de la función de valor acción $Q(\mathbf{x}, \mathbf{u}; \bm\theta_Q)$
- El entorno produce recompensa y nuevo estado
- El crítico calcula el error TD y retroalimenta al actor

## Actor: objetivo y gradiente determinista
- El actor maximiza el desempeño esperado bajo la política de comportamiento $\beta$

$$
\begin{aligned}
J(\bm\theta_{\mu})
&= \mathbb{E}_{\mathbf{x}\sim\rho^{\beta}}\left[V_{\mu}(\mathbf{x})\right] \\
&= \mathbb{E}_{\mathbf{x}\sim\rho^{\beta}}\left[
Q_{\mu}(\mathbf{x}, \mu(\mathbf{x}; \bm\theta_{\mu}))\right]
\end{aligned}
$$

- El teorema de gradiente de política determinista permite calcular:

$$
\nabla_{\bm\theta_{\mu}}J(\bm\theta_{\mu})
= \mathbb{E}_{\mathbf{x}\sim \rho^{\beta}}
\left[
\nabla_{\mathbf{u}}Q(\mathbf{x}, \mathbf{u})
\nabla \mu(\mathbf{x};\bm\theta_{\mu})\big|_{\mathbf{u}=\mu(\mathbf{x};\bm\theta_{\mu})}
\right]
$$

- Actualización por ascenso en gradiente:

$$\bm\theta^{(k+1)}_{\mu} = \bm\theta^{(k)}_{\mu} + \alpha_{\mu} \nabla_{\bm\theta_{\mu}}J\left(\bm\theta_{\mu}^{(k)}\right)$$

## Crítico: aproximación de Q
- El crítico aproxima la función de valor acción asociada al actor:

$$Q(\mathbf{x}, \mathbf{u}; \bm\theta_{Q}) \approx Q_{\mu}(\mathbf{x}, \mathbf{u})$$

- La pérdida del crítico se construye a partir del error TD:

$$
\mathcal{L}\left(\bm{\theta}_Q\right)
= \mathbb{E}_{\mathbf{x}, \mathbf{u}\sim \rho_{\beta}\text{, }\mathbf{x}'\sim p}
\left[
\left(
r(\mathbf{x}, \mathbf{u})
+ \gamma \max_{\mathbf{u}'}Q\left(\mathbf{x}', \mathbf{u}';\bar{\bm{\theta}}_{Q}\right)
- Q\left(\mathbf{x}, \mathbf{u};\bm{\theta}_{Q}\right)
\right)^2
\right]
$$

- En DDPG se reemplaza la optimización sobre acciones por el actor objetivo:

$$Q(\mathbf{x}, \mu(\mathbf{x};\bm\theta_{\mu}); \bm\theta_{Q}) := \max_{\mathbf{u}'}Q(\mathbf{x}, \mathbf{u}; \bm\theta_{Q})$$

- Objetivo práctico con replay buffer y redes objetivo:

$$
\mathcal{L}\left(\bm{\theta}_Q\right)
= \mathbb{E}_{(\mathbf{x}, \mathbf{u}, r, \mathbf{x}')\sim U(\mathcal{D}) }
\left[
\left(
r + \gamma Q\left(\mathbf{x}', \mu\left(\mathbf{x}';\bar{\bm\theta}_{\mu}\right); \bar{\bm\theta}_{Q}\right)
- Q\left(\mathbf{x}, \mathbf{u};\bm{\theta}_{Q}\right)
\right)^2
\right]
$$

- Actualización por descenso en gradiente:

$$\bm\theta_Q^{(k+1)} = \bm\theta_{Q}^{(k)} - \alpha_{Q} \nabla_{\bm\theta_Q} \mathcal{L}\left(\bm\theta_Q^{(k)}\right)$$

## Exploración y estabilización
- Política de comportamiento con ruido:

$$\mathbf{u}_t = \mu(\mathbf{x}_t;\bm\theta_{\mu}) + \mathcal{O}_t \quad \forall t \in \mathcal{T}$$

- $\mathcal{O}_t$ puede ser un proceso de Ornstein-Uhlenbeck para correlación temporal
- **Experience replay**: almacenar experiencias $e_t = (\mathbf{x}_t, \mathbf{u}_t, r_{t+1}, \mathbf{x}_{t+1})$ en $\mathcal{D}$
- Muestreo uniforme desde $\mathcal{D}$ rompe correlación y mejora eficiencia
- Redes objetivo $\bar{\bm\theta}_{\mu}$ y $\bar{\bm\theta}_{Q}$ estabilizan los objetivos del aprendizaje

## Gradientes por mini lote
- Gradiente del actor estimado por muestreo:

$$
\nabla_{\bm\theta_{\mu}} J \approx \frac{1}{N}\sum_{i=1}^{N}
\nabla_{\mathbf{u}}Q(\mathbf{x},\mathbf{u};\bm\theta_{Q})\Big|_{\mathbf{x}=\mathbf{x}_i, \mathbf{u}= \mu(\mathbf{x}_i)}
\nabla_{\bm\theta_{\mu}}\mu(\mathbf{x};\bm\theta_{\mu})\Big |_{\mathbf{x}=\mathbf{x}_i}
$$

- Gradiente del crítico estimado desde la memoria:

$$
\nabla_{\bm\theta_{Q}}\mathcal{L} \approx \frac{1}{N}\sum_{i=1}^{N}
\left(
r_{i+1} + \gamma Q\left(\mathbf{x}_{i+1},\mu(\mathbf{x}_{i+1};\bar{\bm\theta}_{\mu});\bar{\bm{\theta}}_{Q}\right)
- Q\left(\mathbf{x}, \mathbf{u};\bm{\theta}_{Q}\right)
\right)
\nabla_{\bm\theta_Q}Q(\mathbf{x}, \mathbf{u};\bm\theta_Q)
$$

- Actualización suave de redes objetivo:

$$
\bar{\bm\theta}_{Q}^{(k+1)} = \tau \bm\theta_{Q}^{(k+1)} +(1- \tau)\bar{\bm\theta}_{Q}^{(k)}
$$

$$
\bar{\bm\theta}_{\mu}^{(k+1)} = \tau \bm\theta_{\mu}^{(k+1)} +(1- \tau)\bar{\bm\theta}_{\mu}^{(k)}
$$

- $\tau \ll 1$ hace que las redes objetivo evolucionen lentamente

## Algoritmo DDPG
- Cerrar la slide con el algoritmo completo del capítulo

**Deep Deterministic Policy Gradient (Lillicrap et al.)**

1. Inicializar aleatoriamente las redes $Q\left(\cdot,\cdot;\bm\theta_Q\right)$ y $\mu\left(\cdot;\bm\theta_{\mu}\right)$
2. Inicializar las redes objetivo con los mismos parámetros: $\bar{\bm\theta}_{Q} \leftarrow \bm\theta_Q$, $\bar{\bm\theta}_{\mu} \leftarrow \bm\theta_{\mu}$
3. Inicializar el replay buffer $\mathcal{D}$
4. Para cada episodio:
   - Inicializar el proceso de ruido $\mathcal{O}$
   - Recibir observación inicial $\mathbf{x}_1$
   - Para cada paso $t$ del episodio:
     - Seleccionar $\mathbf{u}_t = \mu(\mathbf{x}_t ;\bm\theta_{\mu}) + \mathcal{O}$
     - Ejecutar $\mathbf{u}_t$, observar recompensa $r_t$ y nuevo estado $\mathbf{x}_{t+1}$
     - Almacenar $(\mathbf{x}_t, \mathbf{u}_t, r_t, \mathbf{x}_{t+1})$ en $\mathcal{D}$
     - Muestrear un mini-batch $(\mathbf{x}_i, \mathbf{u}_i, r_i, \mathbf{x}_{i+1})$ de tamaño $N$
     - Definir el objetivo del crítico:

$$y_i = r_i + \gamma Q\left(\mathbf{x}_{i+1}, \mu\left(\mathbf{x}_{i+1};\bar{\bm\theta}_{\mu}\right);\bar{\bm\theta}_{Q}\right)$$

     - Actualizar el crítico minimizando:

$$\mathcal{L} = \frac{1}{N}\sum_i \left(y_i -Q(\mathbf{x}_i, \mathbf{u}_i;\bm\theta_{Q})\right)^2$$

     - Actualizar el actor usando:

$$
\nabla_{\bm\theta_{\mu}} J \approx \frac{1}{N}\sum_{i}
\nabla_{\mathbf{u}}Q(\mathbf{x},\mathbf{u};\bm\theta_{Q})\Big|_{\mathbf{x}=\mathbf{x}_i, \mathbf{u}= \mu(\mathbf{x}_i)}
\nabla_{\bm\theta_{\mu}}\mu(\mathbf{x};\bm\theta_{\mu})\Big |_{\mathbf{x}=\mathbf{x}_i}
$$

     - Actualizar redes objetivo:

$$
\bar{\bm\theta}_{Q} \leftarrow \tau \bm\theta_{Q} +(1- \tau)\bar{\bm\theta}_{Q}
$$

$$
\bar{\bm\theta}_{\mu} \leftarrow \tau \bm\theta_{\mu} +(1- \tau)\bar{\bm\theta}_{\mu}
$$

<!-- speaker: Presentar DDPG como la extensión de Q-learning a control continuo. Introducir el esquema actor-crítico con el diagrama: el actor propone acciones y el crítico evalúa el valor de esas acciones. Explicar primero el objetivo del actor y su gradiente determinista, luego el objetivo del crítico como error TD cuadrático con redes objetivo. Destacar por qué experience replay, ruido de exploración y soft updates estabilizan el aprendizaje. Cerrar recorriendo el algoritmo completo paso a paso, conectando cada línea con las ecuaciones anteriores. -->
