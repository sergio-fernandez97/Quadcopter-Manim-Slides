---
title: "Estabilidad"
slide_number: 5
mode: update
target_file: slides/05_stabilization.py
target_class: StabilizationSlide
update_type: RESTRUCTURE_FLOW
additional_instructions: |
  Mantener la slide actual como base conceptual, pero actualizarla para que
  siga mejor la sección Estabilidad del capítulo. La prioridad es doble:
  corregir el contenido de la definición introductoria y acelerar el ritmo
  visual. Evitar escribir frases o ecuaciones completas con `Write`; preferir
  `FadeIn`, `FadeOut` y transiciones breves entre bloques. Mantener un estilo
  tipo Beamer: texto corto, cajas sobrias, contenido mayormente estático y
  alineado a la izquierda.
---

<!-- cite: LaTex/chapters/02_teoria_de_control.tex, sections: Estabilidad -->

# Estabilidad

## Actualización de contenido
- Antes de la definición matemática ya existente, introducir una definición en
  lenguaje natural inspirada directamente en el nuevo texto del capítulo:
  - la estabilidad es una propiedad fundamental de los sistemas de control
  - asegura que la evolución de los estados se mantenga acotada y predecible
  - este análisis permite diseñar estrategias de control efectivas
- Esta primera idea debe aparecer como una frase breve y clara, no como un
  párrafo largo

## Definiciones matemáticas
- Conservar la estructura general ya presente:
  - estabilidad en el sentido de Liapunov
  - estabilidad asintótica
  - estabilidad exponencial
- Mantenerlas condensadas y legibles
- No escribirlas línea por línea
- Si una formulación completa compite con el espacio, priorizar:
  - una frase corta por concepto
  - la condición matemática esencial

## Problema de estabilización por retroalimentación
- Actualizar esta definición para que siga la redacción actual del capítulo:
  - partir del sistema lineal

$$
\dot{\mathbf{x}}(t)=\mathbf{A}\mathbf{x}(t)+\mathbf{B}\mathbf{u}(t)
$$

  - indicar que se busca una ley de control de estados

$$
\mu:\mathbb{R}^{n_x}\rightarrow\mathbb{R}^{n_u}
$$

  - de la forma

$$
\mathbf{u}(t)=\mu(\mathbf{x}(t))=\mathbf{K}\mathbf{x}(t),
\qquad
\mathbf{K}\in\mathbb{R}^{n_u\times n_x}
$$

  - aclarar que $\mathbf{K}$ es la ganancia de retroalimentación
  - mostrar que al sustituir esta ley se obtiene el sistema de circuito cerrado

$$
\dot{\mathbf{x}}(t)=(\mathbf{A}+\mathbf{B}\mathbf{K})\mathbf{x}(t)
$$

  - cerrar con el objetivo correcto:
    elegir $\mathbf{K}$ para que el equilibrio $\mathbf{x}^{*}=\mathbf{0}$ sea
    asintóticamente estable

## Polos y teorema
- Mantener el cierre conceptual actual, pero más compacto:
  - la matriz $\mathbf{A}+\mathbf{B}\mathbf{K}$ determina la dinámica de
    circuito cerrado
  - sus valores propios son los polos del sistema
  - la estabilidad asintótica exige parte real estrictamente negativa
  - el teorema de asignación de polos relaciona esta meta con la
    controlabilidad de $(\mathbf{A},\mathbf{B})$
- Presentar esta parte como un cierre rápido, no como una secuencia larga

## Ajustes de formato
- Usar la paleta canónica del deck:
  - encabezados en `BLUE_B`
  - cajas con `BLUE_D`, `fill_opacity=0.12`, `stroke_width=1.5`
  - texto principal en `WHITE`
  - texto secundario en `GRAY_A`
  - resaltar solo términos clave como **estable**, **asintóticamente estable**,
    **polos**, **controlable**
- Mantener el título visible toda la slide
- Alinear el contenido principal a la izquierda dentro de cajas
- Reducir texto centrado al mínimo indispensable

## Ritmo y animación
- Acelerar la slide respecto a la versión actual
- Sustituir `Write(...)` sobre expresiones o frases completas por `FadeIn(...)`
- Usar aproximadamente un `next_slide()` por bloque lógico:
  - idea intuitiva
  - definiciones matemáticas
  - problema de estabilización
  - polos + teorema
- Reducir `wait(...)` al mínimo
- Evitar micro-pasos que fragmenten demasiado la lectura

## Criterio de actualización
- No rehacer la teoría; rehacer la presentación
- El cambio central es:
  - agregar la definición intuitiva inicial
  - corregir la definición de estabilización por retroalimentación
  - acelerar el flujo visual
- Si hace falta recortar texto, preservar primero:
  - la intuición de estabilidad
  - la forma de la ley de retroalimentación
  - la ecuación de circuito cerrado
  - la condición sobre los polos

<!-- speaker: Primero presentar estabilidad como idea intuitiva: estados acotados y comportamiento predecible cerca del equilibrio. Luego resumir las tres nociones matemáticas. Después actualizar el problema de estabilización por retroalimentación con la ley de estados, la ganancia K y el circuito cerrado. Cerrar rápido conectando polos, semiplano izquierdo y controlabilidad. -->
