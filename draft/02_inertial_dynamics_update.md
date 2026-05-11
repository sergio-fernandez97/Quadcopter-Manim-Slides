---
title: "Dinámica inercial del cuadricóptero"
slide_number: 2
mode: update
target_file: slides/02_inertial_dynamics.py
target_class: InertialDynamicsSlide
update_type: ADD_SECTION
additional_instructions: "La slide actual ya cubre casi todas las ecuaciones importantes. Preservar la matriz W y las ecuaciones explícitas de Euler. Agregar solo los puentes conceptuales que faltan desde la subsección 'Ecuaciones de movimiento': que W_eta describe la cinemática rotacional inercial y que \dot{x}, \dot{y}, \dot{z} no introducen una nueva ley dinámica, sino una relación cinemática."
---

<!-- cite: LaTex/chapters/01_introduccion.tex, sections: Ecuaciones de movimiento -->

# Dinámica inercial del cuadricóptero

## Idea central (NEW — insertar cerca del inicio)
- Esta slide no introduce nuevas fuerzas ni nuevos torques
- Su papel es conectar:
  - velocidades angulares locales $(p,q,r)$ con tasas de Euler
  - velocidades lineales locales $(u,v,w)$ con derivadas de posición inercial

## Rotación en el sistema inercial (EXISTING — reforzar lectura conceptual)
- Mantener la matriz de transformación:

$$
\begin{bmatrix}
\dot{\varphi}\\
\dot{\theta}\\
\dot{\psi}
\end{bmatrix}
=
\mathbf{W}_{\boldsymbol{\eta}}
\begin{bmatrix}
p\\
q\\
r
\end{bmatrix}
$$

- Mantener la expansión de $\mathbf{W}_{\boldsymbol{\eta}}$
- Añadir una frase breve que diga:
  - el lado izquierdo es un sistema de ecuaciones diferenciales de primer orden para los ángulos de Euler
  - la matriz $\mathbf{W}_{\boldsymbol{\eta}}$ transforma la velocidad angular local al sistema inercial

## Ecuaciones explícitas de rotación inercial (EXISTING — conservar)
- Mantener:

$$
\dot \varphi = p + (q \sin\varphi + r \cos\varphi)\tan\theta
$$

$$
\dot \theta = q\cos\varphi - r\sin\varphi
$$

$$
\dot \psi = (q\sin\varphi + r\cos\varphi)\sec\theta
$$

- Añadir una frase breve de cierre: estas ecuaciones describen la cinemática rotacional en el sistema inercial

## Traslación en el sistema inercial (EXISTING — añadir la idea que falta)
- Mantener:

$$
\dot x = u,
\qquad
\dot y = v,
\qquad
\dot z = w
$$

- Añadir explícitamente la idea del capítulo:
  - aquí no aparece una nueva ley dinámica
  - simplemente se identifica a $u$, $v$ y $w$ como derivadas temporales de $x$, $y$ y $z$

## Puente a la siguiente slide (NEW — cierre corto)
- Cerrar indicando que, junto con la dinámica local de la slide anterior, estas relaciones completan el conjunto de ecuaciones de movimiento de primer orden

<!-- speaker: Diferenciar claramente dinámica local y cinemática inercial. La slide debe dejar claro que aquí el aporte es la transformación entre marcos, no una nueva fuerza física. -->
