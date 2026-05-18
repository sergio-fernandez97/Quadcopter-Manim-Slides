---
title: "Conclusión y trabajo futuro"
slide_number: 17
mode: create
additional_instructions: "Keep this slide very simple. Use two boxed bulleted lists: one for conclusion and one for future work. Prioritize short phrases over full sentences."
---

<!-- cite: LaTex/chapters/07_conclusion.tex, sections: Conclusión, Trabajo futuro -->

# Conclusión y trabajo futuro

## Conclusión
- Se evaluaron dos enfoques RL para control de vuelo: GPS y DDPG
- GPS aproximó parcialmente el desempeño de iLQR
- DDPG no estabilizó el cuadricóptero de forma confiable
- Los métodos clásicos generaron regiones conexas de estabilidad más claras
- GPS mostró potencial, pero con limitaciones en estabilidad global
- La confiabilidad depende fuertemente del entrenamiento y de la dinámica del sistema

## Trabajo futuro
- Extender GPS hacia esquemas híbridos MPC-GPS
- Evaluar métodos model-free más estables como TD3 y SAC
- Refinar el diseño de la función de recompensa
- Comparar algoritmos bajo criterios homogéneos de estabilidad y desempeño
- Usar muestreo dirigido basado en regiones estables de control clásico
- Explorar estrategias híbridas entre control clásico y ANN
- Probar arquitecturas ANN más robustas para mejorar generalización y estabilidad

<!-- speaker: Cerrar destacando que GPS fue la alternativa más consistente en este trabajo, mientras que DDPG mostró limitaciones importantes para este sistema. Después señalar que las extensiones más prometedoras combinan control clásico, mejores métodos model-free y entrenamiento más dirigido. -->
