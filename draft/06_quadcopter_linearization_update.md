---
title: "Linealización de dinámica de vuelo de cuadricóptero"
slide_number: 6
mode: update
target_file: slides/06_quadcopter_linearization.py
target_class: QuadcopterLinearizationSlide
update_type: RESTRUCTURE_FLOW
additional_instructions: |
  Mantener la slide actual como base, pero ampliarla para cubrir de forma
  completa la sección "Cuadricóptero como sistema de control" del capítulo
  LaTex/chapters/02_teoria_de_control.tex. El cambio principal ya no es solo
  mostrar el punto fijo y los jacobianos: la slide debe continuar hasta la
  aplicación del teorema de asignación de polos y cerrar con el algoritmo
  `alg:Control_retro`.

  Prioridades específicas pedidas por el usuario:
  1. Después de `u_star_eq_target`, mostrar debajo la ecuación
     `\omega_0 = \sqrt{\frac{g\cdot m}{4 \cdot k}}`.
  2. Resaltar visualmente el subsistema asociado a `\mathbf{y}` usando color
     y/o rectángulos, de modo que quede claro qué variables se conservan y
     cuáles se excluyen.
  3. Mantener en una misma escena todas las operaciones ligadas a la matriz de
     controlabilidad del subsistema; no desvanecer cada expresión
     inmediatamente.
  4. La escena que contiene "Al desacoplar las matrices" debe llenarse con el
     resto de la aplicación del teorema de asignación de polos, no quedar como
     una transición vacía.
  5. Al escoger los valores deseados de los polos, apoyarse en el diagrama de
     Poincaré provisto por el usuario: usarlo como explicación geométrica en el
     plano `( \det A, \operatorname{Tr} A )`.
  6. No renderizar ni rehacer media; solo preparar el guion preciso para la
     actualización de la slide.

  Mantener el estilo Beamer del deck:
  - texto breve
  - contenido mayormente estático
  - alineación a la izquierda
  - cajas sobrias con la paleta canónica
  - evitar escribir frases largas progresivamente
---

<!-- cite: LaTex/chapters/02_teoria_de_control.tex, sections: Cuadricóptero como sistema de control; Aplicación del teorema de asignación de polos -->

# Linealización de dinámica de vuelo de cuadricóptero

## Criterio general de actualización
- Conservar el arranque actual:
  - título
  - punto fijo `\mathbf{x}^* = \mathbf{0}`
  - condición de equilibrio para `\mathbf{u}^*`
  - jacobianos y matrices `\mathbf{A}`, `\mathbf{B}`
- Expandir la slide para que ya no termine en “no es controlable”
- El recorrido conceptual debe ser:
  - punto fijo y entrada de hover
  - jacobianos y linealización
  - sistema completo no controlable
  - extracción del subsistema controlable `\mathbf{y}`
  - matriz de controlabilidad del subsistema
  - desacoplamiento en cuatro canales de segundo orden
  - criterio geométrico con diagrama de Poincaré para fijar polos
  - matrices de ganancia
  - cierre con `alg:Control_retro`

## Escena 1: punto fijo y entrada de hover (MODIFY)
- Mantener la idea actual:

$$
\mathbf{x}^{*} = \mathbf{0}
$$

- Mantener la condición de equilibrio sobre `\dot w^{*}` y la solución
  particular:

$$
\mathbf{u}^{*} =
\left[\omega_0,\omega_0,\omega_0,\omega_0\right]^{\top}
$$

- Cambio obligatorio:
  - después de `u_star_eq_target`, añadir debajo y visible en la misma escena

$$
\omega_0 = \sqrt{\frac{g\cdot m}{4 \cdot k}}
$$

- Presentación sugerida:
  - arriba: `\mathbf{u}^{*}`
  - abajo, en color de acento `GREEN` o `YELLOW`: el valor explícito de
    `\omega_0`
- No retirar inmediatamente esta deducción; dejarla convivir brevemente con la
  transición hacia jacobianos

## Escena 2: jacobianos y matrices linealizadas (KEEP + SMALL CLEANUP)
- Mantener la evaluación de `\nabla_{\mathbf{x}} f` y `\nabla_{\mathbf{u}} f`
  en el punto fijo
- Mantener la obtención de `\mathbf{A}` y `\mathbf{B}`
- Reducir solo el ruido visual si hace falta, pero no recortar la idea central
- Si el espacio aprieta:
  - priorizar que se vea la estructura en bloques
  - no intentar que el espectador lea cada entrada
- Mensaje clave visible:
  - `\mathbf{A}` y `\mathbf{B}` provienen de evaluar los jacobianos en
    `(\mathbf{0}, \mathbf{u}^{*})`

## Escena 3: sistema completo no controlable, pero con subsistema útil (NEW)
- Introducir el diagnóstico:

$$
\operatorname{rango}\!\left(R(\mathbf{A},\mathbf{B})\right) < 12
$$

- Inmediatamente después, mostrar que se excluyen `x`, `y`, `u`, `v` y se
  conserva el subsistema:

$$
\mathbf{y} =
\left(\varphi,\theta,\psi,z,p,q,r,w\right)^{\top}
$$

$$
\dot{\mathbf{y}} = \tilde{\mathbf{A}}\mathbf{y} + \tilde{\mathbf{B}}\mathbf{u}
$$

- Hacer explícito el resaltado del subsistema `\mathbf{y}`:
  - colorear las variables retenidas con un mismo acento
  - encerrar `\mathbf{y}` en una caja o rectángulo redondeado
  - si se muestra el estado completo `\mathbf{x}`, tachar o atenuar `x,y,u,v`
  - si se usan bloques matriciales, marcar las filas/columnas conservadas con
    un rectángulo transparente
- Esta escena debe dejar muy claro:
  - el sistema completo no es completamente controlable
  - la parte relevante para control lineal sí puede aislarse

## Escena 4: matriz de controlabilidad del subsistema (MODIFY — conservar todo junto)
- Mantener en una misma escena toda la secuencia:

$$
R\left(\tilde{\mathbf{A}},\tilde{\mathbf{B}}\right)
=
\left[\tilde{\mathbf{B}},\tilde{\mathbf{A}}\tilde{\mathbf{B}}\right]
$$

$$
=
\begin{bmatrix}
\mathbf{0} & \mathbf{B}_{3:6} \\
\mathbf{B}_{3:6} & \mathbf{0}
\end{bmatrix}
$$

$$
\operatorname{rango}\!\left(
R\left(\tilde{\mathbf{A}},\tilde{\mathbf{B}}\right)
\right)=8
$$

- Instrucción importante:
  - no hacer `FadeOut` de la primera igualdad antes de mostrar la segunda
  - no borrar la matriz antes de anunciar el rango
  - construir esta parte como una sola escena acumulativa
- El objetivo visual es que el espectador vea el argumento completo de
  controlabilidad del subsistema de un vistazo
- Frase de cierre sugerida:
  - “la pareja `(\tilde{\mathbf{A}},\tilde{\mathbf{B}})` sí es controlable”

## Escena 5: “Al desacoplar las matrices” (EXPAND)
- Conservar esta escena, pero convertirla en una escena realmente informativa
- Debe introducir que la representación matricial se reorganiza en cuatro
  subsistemas de segundo orden:
  - `z-w`
  - `\psi-r`
  - `\theta-q`
  - `\varphi-p`
- Mostrar las cuatro parejas en una retícula o en dos columnas, con la
  estructura repetida:

$$
\dot{\mathbf{x}}^{(i)}
=
\mathbf{A}^{(i)}\mathbf{x}^{(i)} + \mathbf{B}^{(i)}\mathbf{u}
$$

- Usar la matriz común

$$
\mathbf{A}^{(i)} =
\begin{bmatrix}
0 & 1 \\
0 & 0
\end{bmatrix}
$$

  para enfatizar que los cuatro canales comparten la misma forma dinámica base
- No dejar esta escena como una simple frase-puente; debe incluir ya la
  esencia del desacoplamiento del capítulo

## Escena 6: circuito cerrado y polinomios característicos (NEW, dentro del bloque de desacoplamiento)
- En la misma región temática de “Al desacoplar las matrices”, completar el
  resto de la aplicación del teorema de asignación de polos
- Mostrar que cada canal usa una ganancia distinta:
  - `\mathbf{K}^{(z)}`
  - `\mathbf{K}^{(\psi)}`
  - `\mathbf{K}^{(\theta)}`
  - `\mathbf{K}^{(\varphi)}`
- Luego resumir el circuito cerrado por canal, sin necesidad de escribir
  matrices gigantes si comprometen la lectura:

$$
\mathbf{A}^{(i)} + \mathbf{B}^{(i)}\mathbf{K}^{(i)}
$$

- Priorizar el paso hacia el polinomio característico:

$$
\chi_i(\lambda)=
\det\!\left(\mathbf{A}^{(i)}+\mathbf{B}^{(i)}\mathbf{K}^{(i)}-\lambda \mathbf{I}_2\right)
$$

- Mantener visibles, al menos de forma resumida, los cuatro polinomios del
  capítulo:
  - `\chi_z`
  - `\chi_{\psi}`
  - `\chi_{\theta}`
  - `\chi_{\varphi}`
- Si hace falta compactar:
  - mostrar uno completo
  - agrupar los otros tres como variaciones del mismo patrón cuadrático
- Mensaje clave:
  - el problema de control se reduce a escoger coeficientes del polinomio para
    que cada bloque `2\times2` tenga polos estables

## Escena 7: elección de polos mediante diagrama de Poincaré (NEW)
- Al determinar valores “correctos” para los coeficientes, usar el diagrama de
  Poincaré provisto por el usuario como apoyo visual central
- No presentar esta parte solo como manipulación algebraica del discriminante
- Explicar geométricamente:
  - para un sistema de segundo orden, la ubicación de los polos se interpreta
    en el plano `( \det A, \operatorname{Tr} A )`
  - la estabilidad asintótica requiere:
    - `\det A > 0`
    - `\operatorname{Tr} A < 0`
  - imponer `\Delta = (\operatorname{Tr}A)^2 - 4\det A = 0` lleva a la frontera
    de polos reales repetidos
- Conectar esto con la intención del capítulo:
  - escoger parámetros para ubicar los cuatro canales sobre la rama estable con
    `\Delta = 0`
  - interpretar el objetivo como un **degenerate sink** o polo doble estable en
    el diagrama
- La escena debe decir explícitamente algo como:
  - “no buscamos cualquier polo estable; buscamos una selección simple y
    repetida sobre la frontera `\Delta=0` con traza negativa”
- Después de esa explicación geométrica, sí conectar con las igualdades del
  capítulo:
  - discriminante nulo
  - signo correcto de los coeficientes
  - ejemplos de valores elegidos para `\tilde g`
- Evitar fijarse demasiado en un único canal; el diagrama debe servir como
  criterio común para `z`, `\psi`, `\theta` y `\varphi`

## Escena 8: matrices de ganancia resultantes (NEW)
- Mostrar el resultado final del diseño:
  - `\mathbf{K}^{(z)}`
  - `\mathbf{K}^{(\psi)}`
  - `\mathbf{K}^{(\theta)}`
  - `\mathbf{K}^{(\varphi)}`
- No es necesario narrar cada entrada una por una
- Presentarlas como “un conjunto de matrices de control que satisface las
  condiciones anteriores”
- Si la densidad visual es alta:
  - dividir en dos columnas
  - o mantener las fórmulas y acompañarlas con una sola frase corta:
    “cada canal recibe una realimentación de estados distinta, pero todas se
    suman sobre el mismo vector de control”

## Escena 9: cierre con algoritmo `alg:Control_retro` (NEW — final obligatorio)
- La slide debe terminar con el algoritmo de control por retroalimentación
  citado en el capítulo
- Mantener la estructura conceptual del algoritmo:
  - contribución `\mathbf{u}^{(z)}_t`
  - contribución `\mathbf{u}^{(\psi)}_t`
  - contribución `\mathbf{u}^{(\theta)}_t`
  - contribución `\mathbf{u}^{(\varphi)}_t`
  - suma total `\mathbf{u}_t`
  - actualización `\mathbf{x}_{t+1}=f(\mathbf{x}_t,\mathbf{u}_t)`
- No intentar mostrar pseudocódigo minúsculo ilegible
- Presentación sugerida:
  - caja tipo algoritmo o bloque escalonado
  - cada contribución como línea compacta
  - una última línea destacada para

$$
\mathbf{u}_{t} =
\mathbf{u}_{t}^{(z)} +
\mathbf{u}_{t}^{(\psi)} +
\mathbf{u}_{t}^{(\theta)} +
\mathbf{u}_{t}^{(\varphi)} +
\mathbf{u}^{*}
$$

- Cierre conceptual breve:
  - la ley total combina cuatro canales desacoplados alrededor del hover

## Ajustes visuales y de ritmo
- Mantener el título visible durante toda la slide
- Usar la paleta canónica:
  - títulos y encabezados en `BLUE_B`
  - cajas y contornos en `BLUE_D`
  - texto principal en `WHITE`
  - texto secundario en `GRAY_A`
  - resaltar `\mathbf{y}`, `\omega_0`, `\Delta=0`, `\operatorname{Tr}A<0`,
    `\det A>0` con color semántico
- Evitar `Write(...)` sobre frases completas
- Preferir:
  - `FadeIn`
  - `Transform`
  - reemplazo de bloques
- Usar `next_slide()` por bloque lógico amplio, no por igualdad individual
- Donde haya varias ecuaciones relacionadas, mantenerlas juntas el tiempo
  suficiente para que el argumento se lea completo

## Criterio final de contenido
- Esta actualización ya no debe detenerse en la linealización
- Debe cerrar el arco completo:
  - equilibrio
  - linealización
  - controlabilidad parcial
  - desacoplamiento
  - asignación de polos
  - ley de control final
- Si hay que recortar detalle algebraico, preservar primero:
  - la definición explícita de `\omega_0`
  - el resaltado del subsistema `\mathbf{y}`
  - la prueba visual de controlabilidad del subsistema
  - la interpretación con el diagrama de Poincaré
  - el algoritmo final de control

<!-- speaker: Primero recordar que el hover se obtiene haciendo iguales las cuatro velocidades angulares y mostrando explícitamente `\omega_0`. Luego pasar rápido a la linealización y al hecho importante: el sistema completo no es controlable, pero el subsistema `\mathbf{y}` sí. Después explicar que, al desacoplar las matrices, cada canal queda como un sistema de segundo orden; ahí conviene usar el diagrama de Poincaré para justificar por qué se eligen polos sobre `\Delta=0` con traza negativa y determinante positivo. Cerrar con las ganancias y con el algoritmo `alg:Control_retro` como ley de control total. -->
