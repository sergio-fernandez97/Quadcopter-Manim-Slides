---
title: "DDPG: actualización de layout y secuencia"
slide_number: 14
mode: update
target_file: slides/14_ddpg.py
target_class: DDPGSlide
update_type: restructure
additional_instructions: |
  Apply all changes listed below. Preserve all unmentioned logic and animations.
  Use context7 for any Manim or manim-slides API questions.
  Keep the slide Beamer-like, compact, and left-aligned whenever possible.
  Use the canonical project palette and invert external diagrams so they read as
  white strokes/letters on black background.
---

<!-- cite: LaTex/chapters/05_aprendizaje_por_diferencias_temporales.tex, sections: DDPG, Actor-Crítico, Actor: Deterministic Policy Gradient, Crítico: Deep Q-learning, Política de comportamiento, Algoritmo -->
<!-- cite: LaTex/chapters/06_aplicacion_y_evaluacion_de_metodos_rl.tex, sections: Proceso de entrenamiento, DDPG -->

# Actualización del slide 14 — DDPG

## Objetivo de esta actualización

- Reorganizar el slide para que la narrativa visual siga este orden:
  1. motivación
  2. esquema actor-crítico clásico
  3. comparación actor vs. crítico en dos mitades verticales
  4. exploración y estabilización
  5. diagrama final de entrenamiento + algoritmo
- Mantener frases cortas y priorizar lectura espacial clara.
- Conservar la notación matemática ya usada en el slide actual, salvo que una frase de apoyo necesite acortarse.

## CHANGE 1 — Motivación alineada a la izquierda + figura clásica actor-crítico

### Sección afectada

- `# === MOTIVACION ===` (variables `motivation_label`, `motivation_items`, `motivation_group`, `motivation_box`)

### Cambios requeridos

- `motivation_group` debe quedar claramente alineado a la izquierda, no centrado en la escena.
- Mantener el bloque de motivación compacto, con el texto principal en la mitad superior izquierda.
- Después de mostrar `motivation_group`, hacer `FadeIn` de la figura:

`LaTex/figures/05_aprendizaje_por_diferencias_temporales/actor_critic.png`

- Esta figura debe colocarse a la izquierda y debe verse invertida visualmente:
  - fondo negro
  - flechas, contornos y letras en blanco
- Si hace falta preprocesar la imagen para invertir colores durante el render, hacerlo; la prioridad es el resultado visual, no el mecanismo exacto.

### Texto de apoyo junto a la figura

- En el espacio disponible, agregar definiciones muy breves:
  - **Actor**: política determinista que propone la acción.
  - **Crítico**: red que estima el valor de esa acción.
- Debe mencionarse explícitamente que, en este trabajo, **actor y crítico corresponden a ANN**.
- Estas definiciones no deben convertirse en párrafos; prefiero dos cajas o notas cortas.

## CHANGE 2 — Reorganizar actor y crítico en dos mitades verticales

### Secciones afectadas

- `# === ACTOR ===`
- `# === CRITICO ===`
- transición previa a `# === ACTOR-CRITICO DIAGRAM ===`

### Cambio conceptual

- Antes de mostrar el diagrama final de entrenamiento, dividir visualmente el slide en dos columnas:
  - izquierda: **actor**
  - derecha: **crítico**
- La comparación debe sentirse simultánea, no como dos slides completamente independientes.

### Lado izquierdo — actor

- Comenzar por el actor.
- Usar la mitad izquierda para:
  - `actor_label`
  - `objective_box`
  - `objective_eq`
- Hacer `FadeIn` primero de esos tres elementos.
- Después, si el layout lo permite, introducir `grad_eq` y luego `update_eq` sin romper la columna izquierda.
- Si falta espacio, compactar ligeramente texto o ecuaciones antes que mandar elementos al centro.

### Lado derecho — crítico

- Reflejar la misma lógica para el crítico en la mitad derecha.
- Mostrar como mínimo:
  - `critic_label`
  - bloque principal del objetivo/pérdida del crítico
  - ecuación de actualización
- La primera aparición del crítico debe espejar la del actor: etiqueta, caja, ecuación principal.
- `q_approx` puede quedar como nota breve o línea introductoria corta si ayuda, pero no debe desplazar la pérdida principal.

### Regla de composición

- La lectura debe ser:

`actor (izquierda)  |  crítico (derecha)`

- Evitar que alguna ecuación cruce el eje vertical imaginario del slide.
- Si es necesario reducir contenido, priorizar:
  - objetivo del actor
  - pérdida del crítico
  - una sola regla de actualización por lado

## CHANGE 3 — Exploración y estabilización: primero replay, soft update al final

### Sección afectada

- `# === ESTABILIZACION ===`

### Cambios requeridos

- La sección `"Exploración y estabilización"` debe aparecer en la parte baja del slide.
- Antes de hablar de ruido o de actualización suave, explicar primero **Experience Replay**.

### Orden interno deseado

1. Replay buffer `\mathcal{D}`
2. Tuplas de experiencia
3. Muestreo uniforme / mini-lotes
4. Política ruidosa de exploración
5. Soft update de parámetros objetivo

### Contenido mínimo obligatorio

- Mencionar explícitamente las tuplas muestreadas:

$$e_t = (\mathbf{x}_t,\mathbf{u}_t,r_{t+1},\mathbf{x}_{t+1})$$

- Explicar de forma breve que el muestreo uniforme rompe correlación temporal.
- La ecuación de política ruidosa

$$\mathbf{u}_t = \mu(\mathbf{x}_t;\bm\theta_{\mu}) + \mathcal{O}_t$$

  debe aparecer después de la explicación de replay.
- Las ecuaciones de `soft_q` y `soft_mu` deben quedar al final de esta sección.

## CHANGE 4 — Recuperar el diagrama de entrenamiento al final + algoritmo a la derecha

### Secciones afectadas

- `# === ACTOR-CRITICO DIAGRAM ===`
- `# === ALGORITMO FINAL ===`

### Cambio principal

- El diagrama de entrenamiento que hoy no se aprovecha visualmente debe mostrarse al final junto al algoritmo.
- Usar el diagrama actual de DDPG:

`LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/ddpg_algorithm.png`

- También debe verse invertido:
  - fondo negro
  - trazos y letras en blanco

### Layout final deseado

- Izquierda: diagrama DDPG.
- Derecha: bloque `=== ALGORITMO FINAL ===`.
- El diagrama debe quedar alineado a la izquierda, no centrado.
- El algoritmo debe quedar compacto a la derecha, con frases más cortas si hace falta.

### Regla de síntesis para el algoritmo

- Reducir frases largas.
- Prefiero pasos cortos del tipo:
  - inicializar actor y crítico
  - copiar a redes objetivo
  - almacenar experiencia en `\mathcal{D}`
  - muestrear mini-lote
  - actualizar crítico
  - actualizar actor
  - soft update

- Si el texto actual no cabe, resumirlo; no sacrificar el diagrama final.

## CHANGE 5 — Referencias al proceso de entrenamiento real usado en este trabajo

### Fuente

- `LaTex/chapters/06_aplicacion_y_evaluacion_de_metodos_rl.tex`, subsección DDPG dentro de `Proceso de entrenamiento`

### Incluir de forma compacta cuando haya espacio

- Actor y crítico: ANN con arquitectura base comparable a la usada en GPS.
- Replay buffer con capacidad máxima `10^5`.
- Mini-lote `N = 128`.
- Hiperparámetros:
  - `\alpha_{\mu}=10^{-3}`
  - `\alpha_{Q}=10^{-4}`
  - `\gamma=0.99`
  - `\tau=10^{-3}`
- Entrenamiento:
  - 10 épocas
  - `K=5` episodios por época
  - `T=750` pasos máximos por episodio

### Prioridad

- Estos datos pueden ir como nota compacta o caja secundaria en la zona del algoritmo final.
- Si falta espacio, mantener al menos:
  - `N=128`
  - `\gamma=0.99`
  - `\tau=10^{-3}`
  - buffer `10^5`

## Secuencia sugerida

1. Título
2. Motivación, alineada a la izquierda
3. Figura clásica actor-crítico + definiciones breves de actor y crítico como ANN
4. Distribución de estados con descuento, si sigue cabiendo sin saturar
5. Comparación vertical actor vs. crítico, comenzando con el actor
6. Exploración y estabilización desde la parte inferior
7. Soft update al final de esa sección
8. Diagrama final DDPG a la izquierda + algoritmo resumido a la derecha

<!-- speaker: Presentar primero la motivación y el esquema clásico actor-crítico. Luego comparar actor y crítico lado a lado: el actor propone acciones continuas y el crítico evalúa su calidad mediante el error TD. En exploración y estabilización, empezar por experience replay y las tuplas almacenadas, después ruido de exploración y cerrar con redes objetivo. Terminar conectando el diagrama de entrenamiento con un algoritmo resumido y los hiperparámetros usados en este trabajo. -->
