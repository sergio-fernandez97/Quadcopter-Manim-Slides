---
title: "Controlabilidad"
slide_number: 4
mode: update
target_file: slides/04_controllability.py
target_class: ControllabilitySlide
update_type: RESTRUCTURE_FLOW
additional_instructions: |
  Mantener la slide actual como base. La prioridad no es añadir teoría nueva,
  sino corregir formato y ritmo: estilo tipo Beamer, texto breve, alineado a la
  izquierda, cajas sobrias y animaciones principalmente con FadeIn/FadeOut.
  Preservar el contenido conceptual existente y aplicar solo ajustes menores de
  redacción y notación para alinearlo con LaTex/chapters/02_teoria_de_control.tex.
---

<!-- cite: LaTex/chapters/02_teoria_de_control.tex, sections: Controlabilidad -->

# Controlabilidad

## Criterio general de actualización
- Conservar la estructura conceptual actual:
  - intuición breve
  - definición formal
  - matriz de controlabilidad
  - criterio de Kalman
- No rehacer la slide desde cero
- La mejora principal debe ser visual:
  - evitar texto centrado salvo ecuaciones realmente centrales
  - hacer aparecer frases completas con `FadeIn`, no con `Write`
  - reducir la cantidad de pausas y de subpasos intermedios
  - mantener menos elementos simultáneamente en pantalla
- Usar la paleta canónica del deck:
  - título y encabezados en `BLUE_B`
  - cajas con borde `BLUE_D`, `fill_opacity=0.12`, `stroke_width=1.5`
  - texto principal en `WHITE`
  - texto secundario en `GRAY_A`
  - resaltar solo términos clave como **controlable** o **alcanzable**

## Problema actual a corregir
- La slide actual tiene demasiados `Write` sobre frases completas
- La definición entra fragmentada en demasiados pasos
- La matriz de controlabilidad se construye columna por columna y frena innecesariamente el ritmo
- Hay varios bloques de texto centrados cuando deberían leerse como contenido de columna o de caja
- Los `wait` y `next_slide()` son más numerosos de lo necesario para esta cantidad de contenido

## Estructura visual propuesta

## Paso 1: intuición breve (MODIFY)
- Mantener una sola frase corta debajo del título, alineada a la izquierda
- Texto sugerido, más cercano al capítulo pero más conciso:

> La controlabilidad indica si un sistema puede llevar su estado a un objetivo mediante una entrada adecuada en tiempo finito.

- Esta frase debe entrar completa con `FadeIn`
- No dedicarle una secuencia larga ni retirarla inmediatamente; puede convivir con el inicio de la definición o desvanecerse rápido al pasar al bloque principal

## Paso 2: definición formal (MODIFY — simplificar y compactar)
- Convertir la definición en un único bloque dentro de una caja redondeada
- Mantener la esencia del capítulo:

$$
\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}
$$

$$
\mathbf{x}_1 = \mathbf{x}(t_1; \mathbf{x}_0, \mathbf{u})
$$

- Texto breve sugerido dentro o junto a la caja:
  - dado un estado inicial $\mathbf{x}_0 \in \mathbb{R}^{n_x}$
  - el estado $\mathbf{x}_1 \in \mathbb{R}^{n_x}$ es **controlable**
  - si existe $\mathbf{u} \in \mathcal{U}$ que lo alcanza en $t_1 > 0$
  - $\mathbf{x}_1$ es un estado **alcanzable** desde $\mathbf{x}_0$
- No dividir esta definición en seis bloques distintos
- Hacer como máximo dos apariciones:
  - primero la caja con el sistema y la condición principal
  - luego una línea corta que aclare “estado alcanzable”
- Si hace falta mencionar la solución particular $\mathbf{x}(t_1; \mathbf{x}_0, \mathbf{u})$, hacerlo en texto secundario pequeño, no como otro bloque protagonista

## Paso 3: matriz de controlabilidad (MODIFY — hacerla directa)
- Sustituir la construcción columna por columna por una aparición directa del bloque completo
- Usar la notación actualizada del capítulo con corchetes, no con paréntesis:

$$
R(\mathbf{A}, \mathbf{B}) =
\left[\mathbf{B}\ \mathbf{AB}\ \mathbf{A}^2\mathbf{B}\ \cdots\ \mathbf{A}^{n_x-1}\mathbf{B}\right]
\in \mathbb{R}^{n_x \times n_u \cdot n_x}
$$

- Añadir una sola línea breve:
  - “$[\cdot]$ denota concatenación horizontal de bloques”
- Este bloque debe entrar con `FadeIn`
- Si se quiere mantener continuidad visual, transformar la caja de la definición en la caja de la matriz en lugar de borrar todo y reconstruir desde cero

## Paso 4: criterio de Kalman (MODIFY — cierre rápido y limpio)
- Presentar el teorema en una sola caja final
- Mantener la redacción del capítulo:

$$
\operatorname{rango}\!\left(R(\mathbf{A}, \mathbf{B})\right) = n_x
$$

- Añadir una sola frase corta:
  - el sistema es completamente controlable si y solo si se cumple esta condición
  - en ese caso, la pareja $(\mathbf{A}, \mathbf{B})$ se denomina **controlable**
- Evitar separar esta parte en tres escenas pequeñas
- Lo ideal es que el criterio aparezca como cierre inmediato después de la matriz

## Ajustes menores de contenido desde LaTeX
- Actualizar la frase introductoria para incluir la idea de “entrada adecuada” y “tiempo finito”, pero sin volverla larga
- Cambiar la forma final de la matriz a la versión del capítulo con corchetes y término explícito $\mathbf{A}^2\mathbf{B}$
- Cambiar la condición final a notación en español: `rango`
- Mantener la idea de que el criterio se enuncia, no se deriva

## Restricciones de animación y ritmo
- No escribir frases letra por letra
- Usar `FadeIn` para texto y cajas
- Reservar `Transform` para pasar de un bloque conceptual al siguiente
- Reducir `wait(...)` a pausas cortas
- Usar aproximadamente un `next_slide()` por bloque lógico, no por línea
- Mantener el título visible durante toda la slide
- Priorizar lectura rápida sobre acumulación de microanimaciones

## Criterio de actualización
- Cambio principalmente de formato, no de contenido
- Conservar las ecuaciones esenciales ya presentes
- Hacer la slide más sobria, más estática y más rápida
- Si alguna frase compite con las ecuaciones, recortarla

<!-- speaker: Esta slide no necesita más teoría; necesita mejor ritmo. Primero intuición breve, luego definición compacta, después la matriz de controlabilidad y cerrar enseguida con Kalman. El mensaje clave es que la controlabilidad conecta alcanzabilidad con una condición algebraica concreta. -->
