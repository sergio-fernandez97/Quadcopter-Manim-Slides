## NEW SLIDES TO CREATE

### New Slide: Búsqueda de política guíada
- LaTex source: ./LaTex/04_busqueda_guiada_de_politicas_gps.tex
- Requirements: 
    * State the optimization problem. Mention that \pi_{\bm{\theta}} is stochastic policy (where the mean is an ANN).
    * Then change the color of the cost (argument of the expected value) and 

## SLIDES TO UPDATE

### Update: Política para control continuo (slides/12_continuous_policy.py, class ContinuousPolicySlide)
- LaTex source: 
    * LaTex/chapters/03_aprendizaje_por_refuerzo.tex, Subsection "3.3.1. Procesos de decisión de Markov en espacios continuos"
    * LaTex/chapters/06_aplicacion_y_evaluacion_d_metodos_rl.tex, Subsection "6.2.1. Guided Policy Search"
    * LaTex/chapters/09_redes_neuronales_artificiales.tex, Appendix B "B Redes neuronales artificiales"
- Current issues: 
    * At the end of the Scene (last three self.next_slide) many elements are overlapped. You can remove the title of the slide, the rectangle for "pesos y sesgos" can be at the right of the diagram instead of the bottom. The diagram could be even lower of the equation mu.  
- Required updates:
    * Based on the description in subsection 6.2.1, at the end describe how the ANN fits into the the quadcopter 
    control, use the equation \mathnf{u}_t^{\pi}.





