---
title: "Sistema completo de ecuaciones de movimiento"
slide_number: 3
mode: update
target_file: slides/03_quadcopter_motion.py
target_class: QuadcopterMotionSlide
update_type: RESTRUCTURE_FLOW
additional_instructions: "La slide actual está casi bien. Preservar el arranque con sistema local vs sistema inercial y conservar la transición hacia sistema de control y linealización. Añadir solo una recapitulación más clara de que estas son las 12 ecuaciones de primer orden del modelo completo. Corregir cualquier texto que llame 'aceleración de rotores' a la variable de control: la entrada de control debe expresarse como velocidades angulares de rotores."
---

<!-- cite: LaTex/chapters/01_introduccion.tex, sections: Ecuaciones de movimiento, Momentos, fuerzas y torques -->

# Sistema completo de ecuaciones de movimiento

## Recapitulación del modelo completo (NEW — insertar después del bloque de ecuaciones local/inercial)
- Mantener las dos columnas actuales
- Añadir una frase breve que agrupe el contenido así:
  - dinámica local: $\dot u, \dot v, \dot w, \dot p, \dot q, \dot r$
  - cinemática inercial: $\dot \varphi, \dot \theta, \dot \psi, \dot x, \dot y, \dot z$
- Hacer explícito que juntas forman **12 ecuaciones diferenciales de primer orden**

## Vector de estado (EXISTING — conservar)
- Mantener la construcción del estado:

$$
\boldsymbol{x} =
\begin{bmatrix}
u & v & w & p & q & r & \varphi & \theta & \psi & x & y & z
\end{bmatrix}^{\top}
$$

- Añadir una frase corta que diga que este vector reagrupa las ecuaciones presentadas en las dos slides anteriores

## Variable de control (MODIFY — corregir redacción)
- Mantener el paso donde se introduce la entrada de control
- Cambiar la narrativa para que la entrada sea:

$$
\boldsymbol{u} =
\begin{bmatrix}
\omega_1 & \omega_2 & \omega_3 & \omega_4
\end{bmatrix}^{\top}
$$

- No describirla como "aceleración de rotores"
- Sí describirla como velocidades angulares de los rotores o entradas de control asociadas al empuje y a los torques

## Forma no lineal del sistema (EXISTING — conservar)
- Mantener:

$$
\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))
$$

- Añadir una frase breve que conecte esta forma compacta con el conjunto completo de ecuaciones de movimiento del capítulo

## Puente a sistemas de control (EXISTING — conservar)
- Mantener la transición hacia sistema de control continuo e independiente del tiempo
- Mantener la parte de linealización
- No sobrecargar esta slide con nuevas derivaciones; solo reforzar el puente entre el modelo físico y la formulación de control

## Criterio de actualización
- Cambios mínimos y quirúrgicos
- No rehacer la animación completa
- Mantener el flujo actual, pero hacerlo más fiel a la organización conceptual del capítulo

<!-- speaker: Enfatizar que la física ya quedó establecida: esta slide solo empaqueta las ecuaciones en una forma útil para teoría de control, sin perder la separación entre dinámica local y cinemática inercial. -->
