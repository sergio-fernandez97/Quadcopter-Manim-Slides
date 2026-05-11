---
title: "Dinámica local por Newton-Euler"
slide_number: 1
mode: update
target_file: slides/01_newton_euler.py
target_class: NewtonEulerSlide
update_type: ADD_SECTION
additional_instructions: "La estructura actual ya contiene casi todas las ecuaciones correctas. Preservar el flujo actual Newton -> Euler -> ecuaciones explícitas. Agregar solo las ideas conceptuales que faltan de la subsección 'Ecuaciones de movimiento': cuerpo rígido, fuerza externa = gravedad + empuje, sistema local no inercial, teorema de transporte y significado del término de Coriolis/centrífugo. Verificar cada coeficiente y signo contra el LaTeX citado antes de tocar fórmulas."
---

<!-- cite: LaTex/chapters/01_introduccion.tex, sections: Ecuaciones de movimiento -->

# Dinámica local por Newton-Euler

## Idea central (NEW — insertar al inicio o justo después de la apertura actual)
- Modelar al cuadricóptero como un **sólido rígido**
- Explicar que las ecuaciones de Newton-Euler combinan:
  - traslación del centro de masa
  - rotación del cuerpo
- Mantener el tono breve: la slide ya funciona, solo falta hacer explícito este puente conceptual

## Traslación en el sistema local (EXISTING — añadir explicación faltante)
- Recordar la segunda ley de Newton:

$$
m\dot{\boldsymbol{\upsilon}} = \mathbf{f}
$$

- Hacer explícito que, para el cuadricóptero, la fuerza externa neta es la suma de:
  - gravedad
  - empuje total de los rotores

- Añadir la ecuación intermedia clave del capítulo:

$$
m\dot{\boldsymbol{\upsilon}} =
\mathbf{R}^{\top}\mathbf{G} + \mathbf{T}_{B}
- \boldsymbol{\omega} \times (m\boldsymbol{\upsilon}),
\qquad
\mathbf{G} =
\begin{bmatrix}
0\\
0\\
-g
\end{bmatrix}
$$

- Explicar brevemente por qué aparece el término cruzado:
  - el sistema local rota
  - por tanto no es inercial
  - el teorema de transporte introduce el término de Coriolis/centrífugo

## Velocidades lineales en el sistema local (EXISTING — conservar)
- Mantener las ecuaciones actuales de $\dot u$, $\dot v$ y $\dot w$
- Añadir solo una frase breve de cierre: estas tres ecuaciones describen la dinámica de traslación en el sistema local

## Rotación en el sistema local (EXISTING — añadir explicación faltante)
- Mantener la segunda ley de Euler, pero hacer explícito que:
  - el torque actúa sobre el cuerpo rígido
  - el momento angular es $\mathbf{I}\boldsymbol{\omega}$

$$
\boldsymbol{\tau}_B =
\mathbf{I}\dot{\boldsymbol{\omega}} +
\boldsymbol{\omega} \times (\mathbf{I}\boldsymbol{\omega})
$$

- Si se conserva la forma expandida actual, añadir una frase breve que diga que esta se obtiene al despejar $\dot{\boldsymbol{\omega}}$

## Velocidades angulares en el sistema local (EXISTING — conservar)
- Mantener las ecuaciones actuales de $\dot p$, $\dot q$ y $\dot r$
- Añadir una frase breve de cierre: estas tres ecuaciones corresponden a la dinámica de rotación en el sistema local

## Criterio de actualización
- No reescribir la slide desde cero
- No cambiar el orden principal de la derivación
- Insertar únicamente los puentes conceptuales faltantes entre las ecuaciones ya presentes

<!-- speaker: Explicar que el aporte nuevo de esta slide no es solo listar ecuaciones, sino justificar por qué la dinámica local incluye gravedad proyectada, empuje y términos ficticios por trabajar en un marco rotante. -->
