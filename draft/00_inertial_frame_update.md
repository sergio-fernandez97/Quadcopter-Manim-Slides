---
title: "Marco inercial y local del cuadricóptero"
slide_number: 0
mode: update
target_file: slides/00_inertial_frame.py
target_class: InertialFrameSlide
update_type: MODIFY_TEXT
additional_instructions: "La slide actual ya está bastante bien. Preservar la escena 3D, la sección de velocidades angulares de rotores, los ángulos de Euler, las matrices de rotación, el empuje total y las definiciones vectoriales. Hacer solo ajustes de narrativa para dejar más explícita la relación entre los marcos {I} y {B}, y entre los vectores q y v. Cuando se muestren los ángulos de Euler, agregar flechas curvas correctas alrededor del eje correspondiente de cada giro: roll alrededor de x, pitch alrededor de y y yaw alrededor de z."
---

<!-- cite: LaTex/chapters/01_introduccion.tex, sections: Sistemas de referencia, Momentos, fuerzas y torques -->

# Marco inercial y local del cuadricóptero

## Objetivo de la actualización
- Mantener la estructura actual casi intacta
- Reforzar que el sistema inercial describe posición y orientación absolutas
- Reforzar que el sistema local tiene origen en el centro de masa y describe velocidades lineales y angulares
- Hacer más explícito que fuerzas y torques generados por los rotores son las entradas físicas que gobiernan la dinámica

## Sistema inercial (EXISTING — solo ajustar redacción)
- Posición lineal:

$$
\boldsymbol{\xi} =
\begin{bmatrix}
x\\
y\\
z
\end{bmatrix}
$$

- Posición angular:

$$
\boldsymbol{\eta} =
\begin{bmatrix}
\varphi\\
\theta\\
\psi
\end{bmatrix}
$$

- Vector de posición inercial:

$$
\mathbf{q} =
\begin{bmatrix}
\boldsymbol{\xi}\\
\boldsymbol{\eta}
\end{bmatrix}
$$

## Sistema local (EXISTING — solo ajustar redacción)
- Velocidades lineales:

$$
\boldsymbol{\upsilon} =
\begin{bmatrix}
u\\
v\\
w
\end{bmatrix}
$$

- Velocidades angulares:

$$
\boldsymbol{\omega} =
\begin{bmatrix}
p\\
q\\
r
\end{bmatrix}
$$

- Vector de velocidades local:

$$
\mathbf{v} =
\begin{bmatrix}
\boldsymbol{\upsilon}\\
\boldsymbol{\omega}
\end{bmatrix}
$$

## Relación entre marcos (EXISTING — enfatizar idea central)
- La matriz de rotación transforma vectores del sistema local al sistema inercial

$$
\mathbf{R}(\boldsymbol{\eta}) = \mathbf{R}(\psi)\mathbf{R}(\theta)\mathbf{R}(\varphi)
$$

- Mantener las tres matrices elementales actuales de roll, pitch y yaw
- Añadir una frase breve que conecte esas matrices con la orientación completa del vehículo

## Ángulos de Euler (MODIFY — corregir indicación visual)
- Mantener la sección actual de Euler angles
- Añadir flechas curvas visibles alrededor del eje correcto para cada giro:
  - roll $\varphi$: alrededor del eje $x$
  - pitch $\theta$: alrededor del eje $y$
  - yaw $\psi$: alrededor del eje $z$
- Evitar flechas ambiguas o simplemente orbitando el cuadricóptero sin referencia clara al eje
- La indicación visual debe reforzar la correspondencia entre nombre del giro, eje y matriz de rotación mostrada

## Fuerzas y torques de rotores (EXISTING — dejar explícito que son entradas físicas)
- Mantener la relación entre velocidades angulares de rotores y fuerzas:

$$
f_i = k\omega_i^2
$$

- Mantener el empuje total:

$$
T_z = \sum_{i=1}^{4} f_i,
\qquad
\mathbf{T}_B =
\begin{bmatrix}
0\\
0\\
T_z
\end{bmatrix}
$$

- Mantener el vector de torques:

$$
\boldsymbol{\tau}_B =
\begin{bmatrix}
\tau_{\varphi}\\
\tau_{\theta}\\
\tau_{\psi}
\end{bmatrix}
$$

- Hacer explícito en el texto que estas cantidades preparan la derivación de las ecuaciones de movimiento en las siguientes slides

<!-- speaker: Cerrar la slide subrayando que aquí solo se fijan los marcos, la orientación y las entradas físicas del modelo; las ecuaciones de movimiento se derivan después a partir de Newton-Euler. -->
