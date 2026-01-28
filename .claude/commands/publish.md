Render and convert html the following scene: $ARGUMENTS

## Instructions
1. Render the scene:
```bash
uv run manim-slides render slides/${nn}_${name}Slide.py 
```
2. Convert the rendered scene (name of the class inside the script from above): 
```bash
uv run manim-slides convert ${Scene}Slide presentation/${nn}_${name}Slide.html -ccontrols=true
```