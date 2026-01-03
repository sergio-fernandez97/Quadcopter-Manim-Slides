"""
Graph-world Markov Decision Process slide.

Illustrates a small MDP with branching transitions, probabilistic edges,
animated agent movement, and rewards on nodes/edges.

Example:
    manim -pql slides/08_mdp.py GraphWorldMDPSlide
"""

import numpy as np

from manim import *
from manim_slides import Slide


class GraphWorldMDPSlide(Slide):
    def construct(self):
        title = Text(
            "Proceso de Decisión de Markov (MDP)",
            font_size=48,
            color=YELLOW,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        subtitle = Text(
            "Mundo en grafo con acciones y probabilidades",
            font_size=32,
            color=GRAY_B,
        ).next_to(title, DOWN, buff=0.2)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.5)
        self.wait(0.5)

        # Positions for 6 states (kept visually centered and lowered to avoid title overlap)
        positions = {
            "S0": LEFT * 3 + UP * 0.5,
            "S1": LEFT * 1 + UP * 1.8,
            "S2": RIGHT * 2 + UP * 1.1,
            "S3": LEFT * 2 + DOWN * 2,
            "S4": RIGHT * 0.5 + DOWN * 2.6,
            "S5": RIGHT * 3 + DOWN * 0.6,
        }

        def create_state(name, color=BLUE_C):
            circle = Circle(radius=0.4, color=color, stroke_width=3, fill_opacity=0.15)
            label = Text(name, font_size=28, color=color, weight=BOLD)
            return VGroup(circle, label).arrange(CENTER, buff=0).move_to(positions[name])

        states = {name: create_state(name) for name in positions}

        graph_group = VGroup(*states.values())
        graph_group.shift(DOWN * 0.2)

        self.play(LaggedStart(*[FadeIn(s) for s in states.values()], lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # Edges with actions and probabilities
        edges = []

        def add_edge(source, target, prob=1.0, action_label=None, color=GRAY_B, angle=None, stroke=3):
            start_center = states[source][0].get_center()
            end_center = states[target][0].get_center()
            direction = end_center - start_center
            if np.linalg.norm(direction) != 0:
                direction = direction / np.linalg.norm(direction)
            start = start_center + direction * 0.42
            end = end_center - direction * 0.42
            arrow = CurvedArrow(start, end, angle=angle or 0, color=color, stroke_width=stroke)
            prob_tex = MathTex(
                rf"P={prob:.1f}",
                font_size=28,
                color=color,
            ).move_to(arrow.point_from_proportion(0.5) + UP * 0.25)
            if action_label:
                action_tex = Text(action_label, font_size=26, color=ORANGE).next_to(
                    arrow.point_from_proportion(0.2), LEFT, buff=0.12
                )
            else:
                action_tex = None
            edges.append((arrow, prob_tex, action_tex))
            return arrow, prob_tex, action_tex

        add_edge("S0", "S1", prob=0.6, action_label="a", color=ORANGE, angle=0.3, stroke=5)
        add_edge("S0", "S3", prob=0.4, action_label="a", color=ORANGE, angle=-0.3, stroke=3)
        add_edge("S1", "S2", prob=1.0, action_label="b", color=GREEN, angle=0.15, stroke=4)
        add_edge("S2", "S4", prob=0.7, action_label="c", color=BLUE, angle=-0.2, stroke=5)
        add_edge("S2", "S5", prob=0.3, action_label="c", color=BLUE, angle=0.25, stroke=3)
        add_edge("S4", "S3", prob=1.0, action_label="d", color=PURPLE, angle=0.2, stroke=4)

        anims = []
        for arrow, prob_tex, action_tex in edges:
            anims.append(Create(arrow))
            anims.append(FadeIn(prob_tex))
            if action_tex:
                anims.append(FadeIn(action_tex))

        self.play(LaggedStart(*anims, lag_ratio=0.07), run_time=2.5)
        self.wait(0.5)

        # Agent dot animation
        agent = Dot(point=states["S0"].get_center(), radius=0.12, color=YELLOW)
        self.play(FadeIn(agent, scale=1.2))
        self.wait(0.3)

        def reward_flash(target_mobj, value, color=GOLD):
            reward_label = Text(
                f"r_t={value:+}",
                font_size=24,
                color=color,
                weight=BOLD,
            )
            reward_label.next_to(target_mobj, UP, buff=0.1)
            self.play(FadeIn(reward_label, scale=1.1), Flash(target_mobj, color=color, flash_radius=0.5), run_time=1)
            return reward_label

        # Action a branching from S0
        self.play(MoveAlongPath(agent, edges[0][0].copy(), run_time=2, rate_func=rate_functions.ease_in_out_sine))
        reward_a = reward_flash(states["S1"], value=5)
        self.wait(0.3)

        # Transition with action b
        self.play(MoveAlongPath(agent, edges[2][0].copy(), run_time=2, rate_func=rate_functions.ease_in_out_sine))
        reward_b = reward_flash(edges[2][0], value=2, color=GREEN_E)
        self.wait(0.3)

        # Action c branching with probabilities
        self.play(MoveAlongPath(agent, edges[3][0].copy(), run_time=2, rate_func=rate_functions.ease_in_out_sine))
        reward_c = reward_flash(states["S4"], value=3)
        self.wait(0.3)

        self.play(MoveAlongPath(agent, edges[5][0].copy(), run_time=2, rate_func=rate_functions.ease_in_out_sine))
        reward_d = reward_flash(states["S3"], value=1, color=PURPLE_B)
        self.wait(1)

        # Keep rewards on screen for context
        self.add(reward_a, reward_b, reward_c, reward_d)
        summary = Text(
            "Probabilidades de transición P(s_{t+1}|s_t,a_t) y recompensas r_t mostradas en cada paso.",
            font_size=26,
            color=LIGHT_GRAY,
        ).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(summary, shift=UP * 0.2))
        self.wait(1.5)
