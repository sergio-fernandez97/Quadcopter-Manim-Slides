# hello.py
from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle(color=BLUE).set_fill(BLUE, opacity=0.5)
        square = Square(color=RED)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
