---
title: "Política para control continuo"
slide_number: 12
mode: update
target_file: slides/12_continuous_policy.py
target_class: ContinuousPolicySlide
update_type: restructure
additional_instructions: "Use Spanish for all labels. Main goal: rearrange elements to avoid overlap and make the discrete-vs-continuous contrast explicit. Keep the slide Beamer-like and compact. In the ANN section, use a clear left-center-right layout: theta on the left, network in the center, essential equations on the right. Prioritize space over full formal detail."
---

<!-- cite: LaTex/chapters/09_redes_neuronales_artificiales.tex, sections: Arquitectura -->

# Política para control continuo

## Objetivo de esta actualización

- Corregir solapamientos entre cajas, grupos y notas.
- Hacer visible el contraste entre política discreta y política continua.
- Reorganizar la sección de red neuronal para que parámetros, arquitectura y ecuaciones se lean de izquierda a derecha.

## Cambio 1 — Contraste discreto vs continuo

- No reemplazar visualmente el caso discreto por el continuo en la misma posición.
- Mantener `discrete_group` visible en la parte superior.
- Ubicar `continuous_group` debajo de `discrete_group`, con separación suficiente para que ambas cajas se vean al mismo tiempo.
- El público debe poder comparar directamente:
  - arriba: `"MDP discreto y finito"`
  - abajo: `"Control continuo"`
- Si hace falta, reducir ligeramente `font_size` o `buff`, pero no permitir que una caja toque a la otra.
- El `quad_note` debe quedar debajo del bloque comparativo completo, sin invadir ninguna caja.

## Cambio 2 — Política estocástica parametrizada

- Mantener la ecuación gaussiana actual.
- Ajustar caja y explicaciones para que no se acerquen demasiado al borde inferior ni al siguiente bloque.
- Si falta espacio, prefiero texto un poco más pequeño antes que superposición.

## Cambio 3 — Red neuronal completamente conectada

Cuando aparezca `"Red neuronal completamente conectada"`, reemplazar la composición vertical actual por una estructura horizontal compacta de tres zonas:

1. izquierda: parámetros `\bm{\theta}`
2. centro: diagrama de la red
3. derecha: ecuaciones esenciales de la ANN

### Zona izquierda — parámetros

- `theta_box` y `theta_group` deben ir a la izquierda de la red, no abajo.
- Usar esta definición exacta:

$$\bm{\theta} = \left(\mathbf{W}^{[\ell]}, \mathbf{b}^{[\ell]}\right)_{\ell =1}^{L} \in \Theta$$

- Debajo puede ir una sola línea breve, por ejemplo: `"pesos y sesgos por capa"`.
- Esta caja debe alinearse verticalmente con la red para que se lea como entrada conceptual al modelo.

### Zona central — red

- Mantener la red neuronal completamente conectada como elemento central.
- La red debe quedar entre la caja de parámetros y las ecuaciones.
- Si es necesario, compactar el espaciado entre capas o el radio de neuronas antes que desplazar elementos hacia abajo.

### Zona derecha — ecuaciones esenciales

- A la derecha de la red mostrar una versión compacta de la definición de la red `eq:ANN` y de la transformación por capa.
- No hace falta usar la expresión completa anidada si no cabe; basta con la idea esencial.
- Priorizar estas dos piezas:

$$f_a(\mathbf{x}; \bm{\theta}) := \phi \circ T_L \circ \phi \circ T_{L-1} \circ \cdots \circ \phi \circ T_1(\mathbf{x})$$

$$T_{\ell}(\mathbf{z}) = \mathbf{W}^{[\ell]}\mathbf{z} + \mathbf{b}^{[\ell]}$$

- Si cabe una línea adicional, incluir solo la información mínima de dimensiones:

$$\mathbf{W}^{[\ell]} \in \mathbb{R}^{n_{\ell} \times n_{\ell-1}}, \qquad \mathbf{b}^{[\ell]} \in \mathbb{R}^{n_{\ell}}$$

- No incluir desarrollos largos de `\Theta` ni texto extenso a la derecha.

## Regla de layout para toda la sección ANN

- Ningún elemento debe quedar debajo de la red salvo etiquetas pequeñas estrictamente necesarias.
- El bloque completo debe leerse como:

$$\text{parámetros} \;\longrightarrow\; \text{red} \;\longrightarrow\; \text{mapeo}$$

- Si el ancho es crítico, reducir:
  - tamaño del texto descriptivo
  - separación horizontal entre columnas
  - cantidad de texto auxiliar

- No reducir la legibilidad matemática principal.

## Secuencia sugerida

1. Título
2. Contraste discreto vs continuo con ambos visibles
3. Nota del cuadricóptero
4. Política estocástica parametrizada
5. Red neuronal completamente conectada
6. Caja de parámetros a la izquierda + red en el centro + ecuaciones a la derecha

<!-- speaker: Primero contrasta política discreta y continua mostrando ambos bloques simultáneamente. Después, en la sección de ANN, explica de izquierda a derecha: parámetros por capa, red completamente conectada y mapeo resultante. La prioridad es evitar solapamientos y hacer evidente el contraste visual entre tipos de política. -->
