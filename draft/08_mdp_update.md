---
title: "Proceso de decisión de Márkov (MDP)"
slide_number: 8
mode: update
target_file: slides/08_mdp.py
target_class: MdpSlide
update_type: RESTRUCTURE_FLOW
additional_instructions: |
  Mantener la slide actual como base, pero insertar al inicio una introducción breve
  de RL inspirada en LaTex/figures/03_aprendizaje_por_refuerzo/framework-RL.jpeg.
  Antes de modificar slides/08_mdp.py, consultar tanto el video de referencia indicado
  en este draft como slides/08_mdp_reverse.py. Tratar slides/08_mdp_reverse.py como la
  fuente reverse-engineered del video y usarla para replicar la cadencia visual, la
  secuencia de apariciones y la lógica de resaltado del ejemplo. Reflejar esa animación
  en un ejemplo propio, sin copiar literalmente el contenido visual del video. Conservar
  estilo tipo Beamer: texto breve, alineación mayormente a la izquierda y animaciones
  sobrias con FadeIn/FadeOut. Verificar la notación y el orden conceptual con
  LaTex/chapters/03_aprendizaje_por_refuerzo.tex.
---

<!-- cite: LaTex/chapters/03_aprendizaje_por_refuerzo.tex, sections: Marco teórico, Interfaz agente-entorno, Proceso de decisión de Márkov -->
<!-- visual-reference: https://packaged-media.redd.it/hy5bxhl0xdag1/pb/m2-res_830p.mp4?m=DASHPlaylist.mpd&var=sgpssan&v=1&e=1778914800&s=a42d1cf44b31aa8d76f7500aac9ba64e7096e6de -->
<!-- implementation-reference: slides/08_mdp_reverse.py -->

# Proceso de decisión de Márkov (MDP)

## Criterio general de actualización
- Mantener la slide existente como punto de partida
- Corregir el título a **Proceso de decisión de Márkov (MDP)**
- Insertar primero una introducción corta de aprendizaje por refuerzo antes de entrar al MDP
- Preservar la mayor parte del contenido actual del bloque de MDP y del ejemplo del robot, pero hacerlo más fiel al capítulo y más limpio en el flujo
- En el bloque conceptual del MDP, cada idea debe aparecer, explicarse y luego desvanecerse antes de pasar a la siguiente

## Introducción breve a RL (NEW — insertar al inicio)
- Antes del contenido actual, mostrar un bloque rectangular con una definición breve:

> **Definición**: El aprendizaje por refuerzo es un paradigma en el que un agente interactúa con un entorno y aprende a tomar decisiones para maximizar recompensas acumuladas.

- Usar un diagrama similar a `LaTex/figures/03_aprendizaje_por_refuerzo/framework-RL.jpeg`
- Mantener solo los elementos esenciales: **agente**, **entorno**, flechas de interacción y notación de estado/acción
- No saturar esta parte con demasiada teoría; debe ser una introducción visual corta al problema secuencial

## Secuencia visual de la interfaz agente-entorno (NEW)
- Paso 1: hacer `FadeIn` del agente y del entorno
- Paso 2: hacer `FadeIn` del estado con:
  - etiqueta: **estado**
  - símbolo matemático: $X_t$
  - flecha correspondiente en el diagrama
- Paso 3: hacer `FadeIn` de la acción con:
  - etiqueta: **acción**
  - símbolo matemático: $U_t$
  - flecha correspondiente en el diagrama
- Paso 4: mencionar explícitamente que las letras mayúsculas representan variables aleatorias
- Paso 5: hacer `FadeIn` de las realizaciones observadas:

$$
X_t = x, \qquad U_t = u
$$

- Puede añadirse una frase corta debajo o al lado: "minúsculas = realizaciones observadas"
- No introducir todavía recompensa en esta parte; dejar el foco en estado, acción y notación
- Al terminar esta introducción, desvanecer el bloque para pasar al MDP

## Proceso de decisión de Márkov (MODIFY — usar el contenido actual, pero reorganizado)
- Mantener el flujo conceptual de la slide actual, pero reorganizarlo en pasos más claros
- Cada paso debe entrar con `FadeIn`, quedarse visible mientras se explica y luego salir con `FadeOut`
- Evitar acumular demasiadas ecuaciones al mismo tiempo

## Paso 1: dependencia de la historia completa (MODIFY)
- Introducir primero la idea de que, en general, el siguiente estado podría depender de toda la historia
- Mostrar una ecuación de historia completa, con notación compacta para no sobrecargar:

$$
\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid x_0,u_0,\ldots,x_t,u_t\right]
$$

- Acompañar con una frase breve: "en principio, el futuro puede depender de toda la historia"
- Después de explicarlo, hacer `FadeOut` de este bloque

## Paso 2: propiedad de Márkov explícita (MODIFY — importante)
- Mostrar la propiedad de Márkov de forma explícita y central:

$$
\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t\right]
=
\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t,\ldots,X_0=x_0,U_0=u_0\right]
$$

- Usar la forma con puntos suspensivos para simplificar la escritura, pero dejar claro verbalmente que representa toda la historia previa
- Añadir una frase breve: "el siguiente estado depende del presente, no de cómo se llegó ahí"
- Después de explicarlo, hacer `FadeOut` de este bloque

## Paso 3: notación simplificada de transición (MODIFY — importante)
- Inmediatamente después, introducir la notación simplificada:

$$
p(x_{t+1}\mid x_t,u_t)
:=
\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t\right]
$$

- Explicar de forma breve que esta escritura compacta se usará para las probabilidades de transición
- Este paso debe quedar visualmente limpio y aislado
- Después de explicarlo, hacer `FadeOut`

## Paso 4: dinámica secuencial del MDP (MODIFY)
- Conservar la idea actual del estado inicial, acción inicial y transición probabilista
- Mostrar de forma breve:

$$
x_0 \in \mathcal{X}, \qquad u_0 \in \mathcal{U}(x_0)
$$

$$
p(x_1\mid x_0,u_0), \qquad p(x_2\mid x_1,u_1)
$$

- Luego cerrar con la trayectoria:

$$
x_0 \xrightarrow{u_0} x_1 \xrightarrow{u_1} x_2 \xrightarrow{u_2} \cdots x_t \xrightarrow{u_t} \cdots
$$

- Mantener la idea del slide actual: el agente no necesita conocer explícitamente estas probabilidades para interactuar con el entorno
- Este último bloque puede quedarse visible para conectar con el ejemplo

## Ejemplo: Robot de reciclaje (MODIFY — conservar ejemplo y notación)
- Mantener el ejemplo del robot de reciclaje
- Mantener la notación y los conjuntos del slide actual:

$$
\mathcal{X}=\{\text{high},\text{low}\}
$$

$$
\mathcal{U}(\text{high})=\{\text{search},\text{wait}\}, \qquad
\mathcal{U}(\text{low})=\{\text{search},\text{wait},\text{recharge}\}
$$

- Mantener también:
  - $r_{\text{search}}$
  - $r_{\text{wait}}$
  - $\alpha$, $\beta$
  - transición negativa con recompensa $-3$

## Presentación del ejemplo (MODIFY)
- Conservar el bloque inicial de planteamiento del problema, pero más compacto
- Luego conservar el bloque con los elementos del MDP del robot
- Después pasar al grafo del ejemplo
- Seguir un orden de aparición por capas, similar al video de referencia:
  - primero estados: conjunto y nodos
  - después acciones: conjunto de acciones
  - después transiciones: expresión matemática y aristas con sus probabilidades
  - después recompensas: expresión matemática y valores sobre las aristas correspondientes
- Tras explicar la estructura del MDP del robot, hacer `FadeOut` de las expresiones matemáticas y preservar visible el grafo
- Con el grafo todavía visible, hacer `FadeIn` del framework de RL para conectar el ejemplo concreto con la interfaz agente-entorno

## Estilo de animación para el robot de reciclaje (NEW)
- El objetivo no es dejar un diagrama completamente estático
- La referencia visual es el movimiento claro y secuencial del ejemplo enlazado por el usuario
- Antes de modificar la slide, consultar explícitamente este video de referencia para imitar su cadencia visual y la forma de recorrer el diagrama:
  - `https://packaged-media.redd.it/hy5bxhl0xdag1/pb/m2-res_830p.mp4?m=DASHPlaylist.mpd&var=sgpssan&v=1&e=1778914800&s=a42d1cf44b31aa8d76f7500aac9ba64e7096e6de`
- Consultar también `slides/08_mdp_reverse.py`, que es la reconstrucción reverse-engineered de ese video
- Usar `slides/08_mdp_reverse.py` como guía directa para la secuencia de aparición, resaltado, recorrido y atenuación
- Espejar esa lógica visual en un ejemplo propio del deck, sin depender del contenido exacto del video original
- Si hace falta mayor claridad sobre el ritmo de la secuencia, volver a consultar el video antes de ajustar la animación final
- Secuencia deseada para construir el ejemplo:
  - hacer `FadeIn` del conjunto de estados y de los nodos `high`, `low`
  - hacer `FadeIn` del conjunto de acciones
  - hacer `FadeIn` de la expresión matemática de transición y luego de las aristas con sus valores de probabilidad
  - hacer `FadeIn` de la expresión matemática de recompensa y luego de los valores de recompensa sobre las aristas correspondientes
  - hacer `FadeOut` de las expresiones matemáticas, preservando el grafo ya construido
  - hacer `FadeIn` del framework de RL sobre o junto al grafo preservado
- Para simular la toma de decisiones del agente:
  - colocar una moneda al lado de la caja del agente
  - simular el lanzamiento de la moneda con un cambio visible de color del círculo
  - usar ese evento como disparador de la selección de acción y del recorrido activo en el grafo
- Replicar esa idea con una animación tipo recorrido sobre el grafo:
  - resaltar un estado
  - resaltar la acción elegida
  - resaltar la transición activa
  - mover un marcador visible a lo largo del camino
  - mostrar la etiqueta de probabilidad y recompensa del arco activo
- Mientras una transición se explica, el resto del grafo puede quedar atenuado
- Al terminar cada mini-recorrido, retirar el resaltado antes de pasar al siguiente

## Recorridos sugeridos para la animación del ejemplo
- Recorrido 1: `high -> search -> high`
- Recorrido 2: `high -> search -> low`
- Recorrido 3: `low -> recharge -> high`
- Opcionalmente incluir `low -> wait -> low` si ayuda a cerrar la intuición
- Cada recorrido debe venir después del evento visual de la moneda, para reforzar que la decisión parte del agente
- No cambiar la notación del ejemplo actual; solo mejorar la claridad y el dinamismo

## Restricciones de estilo
- No escribir frases letra por letra
- Hacer aparecer frases completas con `FadeIn`
- Mantener texto corto
- Mantener la mayor parte del texto alineado a la izquierda
- Usar rectángulos redondeados para definición y listas
- Cuidar que el bloque introductorio de RL y el bloque del ejemplo compartan la misma paleta visual del resto del deck

<!-- speaker: Abrir con una definición breve de RL y una interfaz agente-entorno muy simple. Luego justificar por qué un MDP es una simplificación útil: primero historia completa, luego propiedad de Márkov, luego notación compacta p(x'|x,u), y finalmente la evolución secuencial. En el robot de reciclaje, usar el grafo para hacer tangible cómo estado, acción, transición y recompensa aparecen en un problema concreto. -->
