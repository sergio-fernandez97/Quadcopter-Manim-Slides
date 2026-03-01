## NEW SLIDES TO CREATE

## SLIDES TO UPDATE

### Update: Quadcopter's mathematical model (slides/00_inertial_frame.py, class InertialFrameSlide)
- LaTex source: LaTex/chapters/01_introduccion.tex, Section "1.2. Modelo matemático de un cuadricóptero"
- Cuerrent issues: 
    * The matrix `combined_matrix` suffers from improper orientation in 3D space — its plane is not facing the camera (non-orthogonal to the viewing direction), producing perspective distortion and poor legibility.
    * In "Sistema de referencia inercial". It can't be seen the euqaton at the right of "posición angular".
- Required updates:
    * Before presentig the euler angles, add a title named "Ángulo de Euler".
    * Increase the size of both the quadcopter and axis in each of corresponding figures when presenting roll, pitch and yaw.
    * For each axis corresponding to roll, pitch and yaw when presenting the euler angles add a curved arrow indicating the 
    direction.   
    * When presenting roll, pitch and yaw, add one label aligned horizontally with the torques named "torque". Analogously  add a label for the rotation matrices named "matriz de rotación".
    * When presenting the T_B add a label named "Empuje en la dirección z".
    * In the scene "Sistema de referencia inercial". Use the cur
    rent format for labels for "posición lineal" and "posición angular". Add a brief description for thise scene based on the LaTex source.
    * For "Sistema de referencia local" add the current format for labels. Add a brief description for thise scene based on the LaTex source.

### Update: Dinámica de traslación y rotación local (slides/01_newton_euler.py, class NewtonEulerSlide)
- LaTex source: LaTex/chapters/01_introduccion.tex, Section "1.2. Modelo matemático de un cuadricóptero"
- Required updates: Update the slide style according to ./CLAUDE.md.

### Update: Dinámica de traslación y rotación inercial (slides/02_inertial_dynamics.py, class InertialDynamicsSlide)
- LaTex source: LaTex/chapters/01_introduccion.tex, Section "1.2. Modelo matemático de un cuadricóptero"
- Required updates: Update the slide style according to ./CLAUDE.md.

### Update: Sistemas de control (slides/03_quadcopter_motion.py, class QuadcopterMotionSlide)
- LaTex source: 
    * LaTex/chapters/01_introduccion.tex, Section "1.2. Modelo matemático de un cuadricóptero"
    * LaTex/chapters/02_teoria_de_control.tex, Section "2.1. Sistemas de control"
- Required updates: Modify the existing code in order to comply the guidelines in ./CLAUDE.md
- Current issues: 
    * Notice that the last equation (linealization of the systme) has overlapped elements, the braquets with the equations

### Update: Estabilidad (sistemas de control) (slides/05_stabilization.py, class StabilizationSlide)
- LaTex source:
    * LaTex/chapters/01_introduccion.tex Section "2.3. Estabilidad"
- Required updates: Before presenting "Problema de estabilización" for linear systems, introduce the definition of stability. 

### Update: Linealización de dinámica de vuelo de cuadricóptero (slides/06_quadcopter_linearization.py, class QuadcopterLinearizationSlide)
- LaTex source: LaTex/chapters/01_introduccion.tex Section "2.5. Cuadricóptero como sistema de control"
- Required updates:
    * Modify the existing code in order to comply the styled specified ./CLAUDE.md
    * Present the controlability matrix in the left side of the slide and on the right side preset:  \dot{\mathbf{y}} = \mathbf{\tilde{A}}\mathbf{y} + \mathbf{\tilde{B}}\mathbf{u} and the equations expanded. Use labels and subtitles. Make sure there's no overlapping.
    * Add the missing contents from the source into the slide: the calculations in order to have the particular solution: the eigen values, values of the matrices. Also include the algorithm.





