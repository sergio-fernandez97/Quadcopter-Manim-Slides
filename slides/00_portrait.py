"""
Portrait / title slide for the dissertation presentation.

Displays the UNAM and Facultad de Ciencias logos, dissertation title,
author, and advisor information. Then fades out and shows the objective.

Author: Sergio Fernández
Date: 2026-02-18
"""

import numpy as np
from PIL import Image, ImageOps
from manim import *
from manim_slides import Slide


def _invert_logo(path: str, tint_hex: str = "#CCCCCC") -> ImageMobject:
    """Load a logo, invert black→light gray, and set white background→transparent."""
    img = Image.open(path).convert("RGBA")
    r, g, b, a = img.split()
    # Invert the RGB channels (black becomes white/light)
    rgb_img = Image.merge("RGB", (r, g, b))
    inverted = ImageOps.invert(rgb_img)
    # Tint: blend toward the target color
    ri, gi, bi = inverted.split()
    arr = np.array(inverted, dtype=np.float32)
    # Parse tint
    tr = int(tint_hex[1:3], 16)
    tg = int(tint_hex[3:5], 16)
    tb = int(tint_hex[5:7], 16)
    # Blend: where original was dark (now bright after invert), push toward tint
    arr[:, :, 0] = np.clip(arr[:, :, 0] * (tr / 255.0), 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * (tg / 255.0), 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * (tb / 255.0), 0, 255)
    inverted_tinted = Image.fromarray(arr.astype(np.uint8), "RGB")
    # Rebuild with original alpha
    result = Image.merge("RGBA", (*inverted_tinted.split(), a))
    # Make near-black pixels (originally white background) transparent
    data = np.array(result)
    # After inversion, original white bg → near black; make transparent
    mask = (data[:, :, 0] < 30) & (data[:, :, 1] < 30) & (data[:, :, 2] < 30)
    data[mask, 3] = 0
    result = Image.fromarray(data, "RGBA")
    return ImageMobject(result)


class PortraitSlide(Slide):

    def construct(self):
        # ============================================================
        # SECTION 1 – Logo legend (top-left)
        # ============================================================
        escudo_unam = _invert_logo("legend/escudo_unam.png").scale_to_fit_height(1.6)
        escudo_fc = _invert_logo("legend/escudo_fc.png").scale_to_fit_height(1.6)
        faculty_label = VGroup(
            Text("Facultad de", font_size=24, color=WHITE),
            Text("Ciencias", font_size=28, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.05)
        unam_label = Text("UNAM", font_size=24, color=WHITE, weight=BOLD)
        faculty_block = VGroup(faculty_label, unam_label).arrange(DOWN, buff=0.12)

        legend = Group(escudo_unam, escudo_fc, faculty_block).arrange(RIGHT, buff=0.35)
        legend.to_corner(UL, buff=0.4)

        self.play(FadeIn(legend), run_time=1)
        self.next_slide()

        # ============================================================
        # SECTION 2 – Title, author, advisor in a box
        # ============================================================
        title = Text(
            "Métodos de aprendizaje por refuerzo\nprofundo para el control del sistema\ndinámico de vuelo de un cuadricóptero",
            font_size=36,
            color=BLUE_B,
            line_spacing=1.2,
        )

        separator = Line(LEFT * 3.5, RIGHT * 3.5, color=BLUE_D, stroke_width=1.5)

        author = Text(
            "Autor: Sergio Miguel Fernández Martínez",
            font_size=24,
            color=WHITE,
        )
        advisor = Text(
            "Asesor: Antonio Capella Kort",
            font_size=24,
            color=GRAY_A,
        )

        content = VGroup(title, separator, author, advisor).arrange(DOWN, buff=0.35)
        content.move_to(DOWN * 0.3)

        title_box = RoundedRectangle(
            corner_radius=0.25,
            width=content.width + 1.0,
            height=content.height + 0.8,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        ).move_to(content)

        self.play(FadeIn(title_box), run_time=0.5)
        self.play(Write(title), run_time=2)
        self.next_slide()

        self.play(Create(separator), FadeIn(author), FadeIn(advisor), run_time=1)
        self.next_slide()

        # ============================================================
        # SECTION 3 – Fade out and show objective
        # ============================================================
        all_elements = Group(legend, title_box, content)
        self.play(FadeOut(all_elements), run_time=1)

        objective_title = Text("Objetivo", font_size=36, color=BLUE_B)
        objective_title.to_edge(UP, buff=1.0)

        objective_text = Text(
            "Evaluar la aplicación de métodos de aprendizaje\n"
            "por refuerzo con redes neuronales en espacios\n"
            "continuos para la optimización del control de un\n"
            "sistema dinámico de vuelo de un cuadricóptero",
            font_size=28,
            color=WHITE,
            line_spacing=1.3,
        )
        objective_text.next_to(objective_title, DOWN, buff=0.6)

        obj_box = RoundedRectangle(
            corner_radius=0.2,
            width=objective_text.width + 0.8,
            height=objective_text.height + 0.6,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        ).move_to(objective_text)

        self.play(FadeIn(objective_title), run_time=1)
        self.next_slide()

        self.play(FadeIn(obj_box), Write(objective_text), run_time=2)
        self.next_slide()

        # ============================================================
        # SECTION 4 – Index / table of contents
        # ============================================================
        obj_elements = VGroup(objective_title, obj_box, objective_text)
        self.play(FadeOut(obj_elements), run_time=1)

        index_title = Text("Índice", font_size=36, color=BLUE_B)
        index_title.to_edge(UP, buff=0.5)
        self.play(FadeIn(index_title), run_time=0.5)
        self.next_slide()

        # -- Build index entries as two columns --
        topics = [
            ("1.", "Cuadricóptero como modelo matemático", [
                "Dinámica de traslación y rotación local",
                "Dinámica de traslación y rotación inercial",
                "Ecuaciones de movimiento de un cuadricóptero",
            ]),
            ("2.", "Teoría de control", [
                "Controlabilidad",
                "Estabilidad",
            ]),
            ("3.", "Control Óptimo", [
                "iLQR",
            ]),
            ("4.", "Aprendizaje por refuerzo", [
                "Interacción Agente–Entorno",
                "Proceso de Decisión de Markov (MDP)",
                "Episodio y retorno esperado",
                "Política y funciones de valor",
                "Q-Learning",
                "Model-free vs Model-based RL",
                "Política para control continuo",
            ]),
            ("5.", "Búsqueda guiada de política (GPS)", [
                "Optimización (BADMM)",
                "Algoritmo",
                "Resultados",
            ]),
            ("6.", "Deep Deterministic Policy Gradient (DDPG)", [
                "Actor-Crítico",
                "Algoritmo",
                "Resultados",
            ]),
            ("7.", "Conclusión", []),
        ]

        def _build_topic_group(num, name, subs):
            header = Text(f"{num} {name}", font_size=22, color=BLUE_B, weight=BOLD)
            lines = [header]
            for sub in subs:
                dot = Text("-", font_size=18, color=GRAY_A)
                label = Text(sub, font_size=18, color=GRAY_A)
                row = VGroup(dot, label).arrange(RIGHT, buff=0.15)
                lines.append(VGroup(Dot(radius=0.001, fill_opacity=0).shift(LEFT * 0.3), row).arrange(RIGHT, buff=0))
            grp = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            return grp

        topic_groups = [_build_topic_group(n, name, subs) for n, name, subs in topics]

        # Split into two columns: topics 1-4 left, 5-7 right
        col_left = VGroup(*topic_groups[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        col_right = VGroup(*topic_groups[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        col_right.align_to(col_left, UP)

        columns = VGroup(col_left, col_right).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        columns.next_to(index_title, DOWN, buff=0.5)

        idx_box = RoundedRectangle(
            corner_radius=0.2,
            width=columns.width + 0.8,
            height=columns.height + 0.6,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        ).move_to(columns)

        self.play(FadeIn(idx_box), FadeIn(columns), run_time=1.5)
        self.next_slide()
