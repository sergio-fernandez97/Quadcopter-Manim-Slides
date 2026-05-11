---
title: "GPS: Guided Policy Search"
slide_number: 15
mode: create
additional_instructions: "Use Spanish for all labels. Use the diagram from LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/gps_algorithm.png (figure fig:gps_schema), taking the attached image as the visual reference. Structure the slide as a step-by-step explanation of the training loop: local trajectory generation, local controller optimization, global policy training, and dual updates. Add concise labels directly over the diagram blocks/arrows when helpful."
---

<!-- cite: LaTex/chapters/04_busqueda_guiada_de_politicas_gps.tex, sections: Guided Policy Search, Optimización de trayectorias locales, Optimización de la política global, Algoritmo; LaTex/chapters/06_aplicacion_y_evaluacion_de_metodos_rl.tex, sections: Guided Policy Search -->

# GPS: Guided Policy Search

## Idea central
- GPS alterna entre **controladores locales** $p_i$ y una **política global** $\pi_{\bm\theta}$.
- Los controladores locales optimizan trayectorias cercanas a condiciones iniciales específicas.
- La política global aprende a imitar a todos los controladores y luego retroalimenta su comportamiento al costo local.
- El acoplamiento entre ambos niveles se fuerza con multiplicadores $\bm\lambda_t$ y penalizaciones $\nu_t$.

## Variables principales
- Controlador local lineal-gaussiano:

$$p_i(\mathbf{u}_t|\mathbf{x}_t) = \mathcal{N}\left(\mu_{ti}(\mathbf{x}_t), \mathbf{\Sigma}_{it}\right)$$

- Política global:

$$\pi_{\bm{\theta}}(\mathbf{u}_t|\mathbf{x}_t) = \mathcal{N}\left(\mu^{\pi}(\mathbf{x}_t; \bm\theta), \bm\Sigma^{\pi}(\mathbf{x}_t)\right)$$

## Diagrama del entrenamiento
- **Usar el diagrama** `LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/gps_algorithm.png` (`fig:gps_schema`) y tomar como referencia visual la imagen adjunta.
- Etiquetas sugeridas sobre el diagrama:
  - `Generación de trayectorias locales`
  - `Entrenamiento de política global`
  - `Actualizar \lambda_t y \nu_t`
  - `Añadir p_i a \mathcal{L}_{\theta}`
  - `Añadir \pi_{\theta} a \mathcal{L}_{p_i}`
  - `k = k + 1`
- La narrativa debe recorrer el diagrama en sentido horario: trayectorias locales $\rightarrow$ base de datos $\rightarrow$ política global $\rightarrow$ actualización de costos locales $\rightarrow$ actualización dual.

## Acoplamiento entre política global y controladores locales
- La versión operativa del esquema BADMM se expresa con tres actualizaciones:

$$
\bm\theta^{(k+1)} =
\argmin_{\bm\theta \in \Theta}
\left(
\sum_{i=1}^{N}\sum_{t=0}^{T-1}
\mathbb{E}_{\pi_{\bm\theta}(\mathbf{u}_t|\mathbf{x}_t)p_i(\mathbf{x}_t)}
\left[\bm\lambda_{t}^{\top(k)}\mathbf{u}_t\right]
+ \nu_t \phi_t^{\bm\theta}\left(\bm\theta, p_i^{(k)}\right)
\right)
$$

$$
p^{(k+1)} =
\argmin_{p}
\left(
\sum_{i=1}^{N}\sum_{t=0}^{T-1}
\mathbb{E}_{p_i(\mathbf{x}_t, \mathbf{u}_t)}
\left[c(\mathbf{x}_t, \mathbf{u}_t) - \bm\lambda_t^{\top(k)}\mathbf{u}_t\right]
+ \nu_t \phi_t^{p}\left(p_i, \bm\theta^{(k+1)}\right)
\right)
$$

$$
\bm{\lambda}_t^{(k+1)} =
\bm{\lambda}_t^{(k)} +
\alpha_{\bm\lambda}\,\nu_t
\left(
\mathbb{E}_{\pi_{\bm\theta}(\mathbf{u}_t|\mathbf{x}_t)p_i(\mathbf{x}_t)}[\mathbf{u}_t]
- \mathbb{E}_{p_i(\mathbf{x}_t, \mathbf{u}_t)}[\mathbf{u}_t]
\right)
$$

- Los términos de divergencia usados en los dos subproblemas son:

$$
\phi_t^{\bm\theta}\left(\bm\theta, p_i\right) :=
\mathbb{E}_{p_i(\mathbf{x}_t)}
\left[
D_{\text{KL}}\left(\pi_{\bm\theta}(\mathbf{u}_t|\mathbf{x}_t)\Vert p_i(\mathbf{u}_t|\mathbf{x}_t)\right)
\right]
$$

$$
\phi_t^{p}\left(p_i, \bm\theta\right) :=
\mathbb{E}_{p_i(\mathbf{x}_t)}
\left[
D_{\text{KL}}\left(p_i(\mathbf{u}_t|\mathbf{x}_t)\Vert \pi_{\bm\theta}(\mathbf{u}_t|\mathbf{x}_t)\right)
\right]
$$

## Paso 1: optimización de trayectorias locales
- Cada controlador $p_i$ se ajusta independientemente con costo aumentado:

$$
\mathcal{L}_{p_i}(p_i, \bm\theta) =
\sum_{t=0}^{T-1}
\mathbb{E}_{p_i(\mathbf{x}_t, \mathbf{u}_t)}
\left[
c(\mathbf{x}_t, \mathbf{u}_t)-\bm{\lambda}_t^{\top}\mathbf{u}_t
\right]
+ \nu_t \phi_{t}^{p}(p_i, \bm\theta)
$$

- El costo efectivo que recibe iLQR queda:

$$
\tilde{c}(\mathbf{x}_t, \mathbf{u}_t):=
c(\mathbf{x}_t, \mathbf{u}_t)-\bm{\lambda}_t^{\top}\mathbf{u}_t-\nu_t \log \pi_{\bm\theta}(\mathbf{x}_t|\mathbf{u}_t)
$$

- Para limitar cambios bruscos entre iteraciones se impone una región de confianza sobre trayectorias:

$$
\min_{p_i \in \mathcal{N}(\bm\tau)}\mathcal{L}_{p_i}(p_i, \bm\theta)
\quad \text{sujeto a}\quad
D_{\text{KL}}(p_i(\bm\tau)\Vert\hat{p}_i(\bm\tau))\leq \epsilon
$$

- El problema primal se reescribe con:

$$
\ell(\mathbf{x}_t, \mathbf{u}_t) =
\frac{1}{\eta + \nu_t}\tilde{c}(\mathbf{x}_t, \mathbf{u}_t)
- \frac{\eta}{\eta + \nu_t}\log\hat{p}_i(\mathbf{u}_t|\mathbf{x}_t)
$$

- Luego iLQR produce un controlador lineal-gaussiano variable en el tiempo:

$$
\mu_{ti}(\mathbf{x}_t) =
\hat{\mathbf{u}}_{it} + \alpha \mathbf{k}_{it} +
\mathbf{K}_{it} \left(\mathbf{x}_{t} - \hat{\mathbf{x}}_{it}\right),
\qquad
\mathbf{\Sigma}_{it} = \mathbf{Q}_{\mathbf{u,u}_{it}}^{-1}
$$

## Paso 2: actualización de la variable dual local
- Después de obtener $p_i$, se actualiza $\eta$ buscando satisfacer la restricción KL:

$$
D_{\text{KL}}(p_i(\bm\tau)\Vert\hat{p}_i(\bm\tau)) - \epsilon = 0
$$

- En la tesis esta ecuación se resuelve con el **método de Brent** en el espacio $\log(\eta)$.

## Paso 3: muestreo de trayectorias
- Cada controlador local genera $M$ trayectorias:

$$
\bm\tau_i^{(j,k+1)} \sim p_i^{(k+1)}(\bm\tau),
\qquad j \in \{1,\cdots,M\}
$$

- Estas trayectorias llenan el bloque central del diagrama $\{\tau_i^{(j)}\}$ y sirven para aproximar los valores esperados de la política global.

## Paso 4: entrenamiento de la política global
- La política global se ajusta como un problema de regresión ponderada hacia las acciones de los controladores locales:

$$
\bm{\theta}^{(k+1)} =
\arg \min_{\bm{\theta} \in \Theta}
\Bigg\{
\frac{1}{2N} \sum_{i=1}^{N} \sum_{t=0}^{T-1}
\mathbb{E}_{p_i(\mathbf{x}_t)}
\Big[
\nu_t
\left(
\bm{\mu}^{\pi}(\mathbf{x}_t; \bm{\theta}) - \bm{\mu}_{ti}(\mathbf{x}_t)
\right)^{\top}
\bm{\Sigma}_{ti}^{-1}
\left(
\bm{\mu}^{\pi}(\mathbf{x}_t; \bm{\theta}) - \bm{\mu}_{ti}(\mathbf{x}_t)
\right)
+ 2 \bm{\lambda}_{t}^{\top} \bm{\mu}^{\pi}(\mathbf{x}_t; \bm{\theta})
\Big]
\Bigg\}
$$

- En la implementación, esta expectativa se aproxima con muestras:

$$
\frac{1}{2NM}
\sum_{i=1}^{N}\sum_{t=0}^{T-1}\sum_{j=1}^{M}
\nu_t
\left(\mathbf{u}_t^{\pi (j)} - \mathbf{u}_{ti}^{(j)}\right)^{\top}
\bm\Sigma_{ti}^{-1}
\left(\mathbf{u}_t^{\pi (j)} - \mathbf{u}_{ti}^{(j)}\right)
+ 2 \bm\lambda_t^{\top}\mathbf{u}_t^{\pi(j)}
$$

- Donde:

$$
\mathbf{u}_{t}^{\pi (j)} = \mu\left(\mathbf{x}_{ti}^{(j)}; \bm\theta^{(k)}\right)
$$

## Paso 5: actualización de la covarianza y multiplicadores
- La covarianza global se actualiza con:

$$
\bm\Sigma^{\pi (k+1)} =
\left(\sum_{i=1}^{N}\sum_{t=1}^{T}\nu_t^{(k)}\right)
\left(
\sum_{i=1}^{N}\sum_{t=0}^{T-1}\nu_t^{(k)}\mathbf{C}_{t,i}^{-1}
\right)^{-1}
$$

- El multiplicador de Lagrange que alinea acciones locales y globales se actualiza empíricamente como:

$$
\bm\lambda_t^{(k+1)} =
\bm\lambda_t^{(k)} +
\alpha_{\bm\lambda}
\left(
\frac{1}{NM}\sum_{i=1}^{N}\sum_{j=1}^{M}
(\mathbf{u}_{ti}^{(j,k+1)}-\mathbf{u}_{t}^{\pi(j,k+1)})
\right)
$$

- $\nu_t$ se incrementa cuando la divergencia KL entre $p_i(\mathbf{u}_t|\mathbf{x}_t)$ y $\pi_{\bm\theta}(\mathbf{u}_t|\mathbf{x}_t)$ es alta, y se reduce cuando esa divergencia es suficientemente baja.

## Narrativa paso a paso sobre el diagrama
1. Inicializar la política global $\pi_{\bm\theta}$ y obtener $N$ controladores locales iniciales.
2. Con cada controlador local $p_i(\mathbf{u}_t|\mathbf{x}_t)$ simular $M$ trayectorias y almacenarlas en la base central $\{\tau_i^{(j)}\}$.
3. Usar esas trayectorias para optimizar la política global $\pi_{\bm\theta}$ con respecto a $\mathcal{L}_{\bm\theta}$.
4. Inyectar la política global actualizada dentro del costo local por medio de $\tilde c(\mathbf{x}_t,\mathbf{u}_t)$ y reoptimizar cada $p_i$ con iLQR.
5. Ajustar la variable dual $\eta$ con Brent para respetar la restricción KL de trayectorias.
6. Actualizar $\bm\lambda_t$ y $\nu_t$ para forzar consistencia entre acciones locales y globales.
7. Incrementar la iteración $k \leftarrow k+1$ y repetir el ciclo.

## Configuración usada en la tesis
- Número de iteraciones de GPS: $K=5$
- Número de controladores locales: $N=7$
- Número de trayectorias por controlador en cada iteración: $M=800$
- Optimización de $\pi_{\bm\theta}$: Adam con tasa de aprendizaje $\alpha=0.01$
- Actualización de $\bm\lambda_t$: $\alpha_{\bm\lambda}=0.01$
- Inicialización de $\nu_t$: $0.001$ para todo $t$
- Búsqueda de Brent sobre $\log(\eta)$ en el intervalo $\left[\log(10^{-4}), \log(10^{4})\right]$

<!-- speaker: Presentar GPS como un ciclo de acoplamiento entre planeación local y aprendizaje global. Recorrer el diagrama en sentido horario: primero explicar cómo cada controlador local optimiza trayectorias con iLQR y una restricción KL, luego cómo esas trayectorias entrenan la política global, y finalmente cómo las variables duales \lambda_t, \nu_t y \eta fuerzan consistencia entre ambos niveles. Cerrar remarcando que el algoritmo repite este ciclo hasta que la política global capture el comportamiento de todos los controladores locales. -->
