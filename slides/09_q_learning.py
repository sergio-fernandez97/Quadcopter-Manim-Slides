"""
Q-learning update slide with grid-world intuition and Q-table.

Example:
    manim -pql slides/09_q_learning.py QLearningSlide
"""

from manim import *
from manim_slides import Slide


class QLearningSlide(Slide):
    def construct(self):
        title = Text("Q-Learning", font_size=56, color=BLUE_D, weight=BOLD)
        subtitle = Text(
            "Aprendizaje por refuerzo sin modelo",
            font_size=28,
            color=GRAY_B,
        )
        title.to_edge(UP, buff=0.4)
        subtitle.next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.2)
        self.wait(0.3)

        # Grid-world block (left)
        cell_size = 1.05
        grid_center = LEFT * 4 + UP * 0.1
        grid_cells = VGroup()
        for row in range(3):
            for col in range(3):
                cell = Square(
                    side_length=cell_size,
                    stroke_width=3,
                    color=BLUE_D,
                )
                cell.move_to(
                    grid_center
                    + RIGHT * cell_size * (col - 1)
                    + DOWN * cell_size * (row - 1)
                )
                grid_cells.add(cell)

        agent_body = Circle(
            radius=0.35,
            color=BLUE_E,
            fill_color=BLUE_E,
            fill_opacity=0.8,
            stroke_width=2,
        ).move_to(grid_center)
        agent_eyes = VGroup(
            Dot(agent_body.get_center() + LEFT * 0.12 + UP * 0.08, radius=0.03, color=WHITE),
            Dot(agent_body.get_center() + RIGHT * 0.12 + UP * 0.08, radius=0.03, color=WHITE),
        )
        agent = VGroup(agent_body, agent_eyes)

        arrows = VGroup(
            Arrow(agent.get_center() + UP * 0.1, agent.get_center() + UP * 0.75, buff=0, color=BLUE_D),
            Arrow(agent.get_center() + DOWN * 0.1, agent.get_center() + DOWN * 0.75, buff=0, color=BLUE_D),
            Arrow(agent.get_center() + LEFT * 0.1, agent.get_center() + LEFT * 0.75, buff=0, color=BLUE_D),
            Arrow(agent.get_center() + RIGHT * 0.1, agent.get_center() + RIGHT * 0.75, buff=0, color=BLUE_D),
        )

        action_labels = VGroup(
            Text("up", font_size=24, color=BLUE_D),
            Text("down", font_size=24, color=BLUE_D),
            Text("left", font_size=24, color=BLUE_D),
            Text("right", font_size=24, color=BLUE_D),
        )
        action_labels[0].next_to(grid_cells, DOWN + LEFT, buff=0.1)
        action_labels[1].next_to(grid_cells, DOWN + RIGHT, buff=0.1)
        action_labels[2].next_to(grid_cells, LEFT, buff=0.25)
        action_labels[3].next_to(grid_cells, DOWN, buff=0.25)

        chest = VGroup(
            RoundedRectangle(width=0.6, height=0.42, corner_radius=0.05)
            .set_fill(GOLD_E, opacity=0.9)
            .set_stroke(GOLD_D, width=2),
            Line(LEFT * 0.3, RIGHT * 0.3).set_stroke(GOLD_D, width=2),
            Circle(radius=0.05, color=BLUE_D, fill_opacity=1).move_to(DOWN * 0.05),
        )
        chest[1].shift(UP * 0.08)
        chest.move_to(grid_center + RIGHT * cell_size + UP * cell_size)

        action_text = Text("action a_t", font_size=26, color=BLUE_D)
        action_text.next_to(grid_cells, DOWN, buff=0.6)
        action_arrow = Arrow(
            action_text.get_right(),
            agent.get_center() + DOWN * 0.35,
            color=BLUE_D,
            buff=0.1,
        )

        self.play(
            LaggedStart(
                FadeIn(grid_cells),
                FadeIn(agent, scale=1.1),
                FadeIn(arrows),
                FadeIn(chest, scale=1.1),
                lag_ratio=0.15,
            ),
            run_time=1.6,
        )
        self.play(FadeIn(action_text), GrowArrow(action_arrow), FadeIn(action_labels), run_time=1.2)
        self.wait(0.4)

        # Reward star (center)
        reward_star = Star(
            n=5,
            outer_radius=0.28,
            inner_radius=0.12,
            color=YELLOW,
            fill_opacity=1,
        ).move_to(LEFT * 0.5 + UP * 0.1)
        reward_label = Text("reward r_t", font_size=26, color=BLUE_D).next_to(
            reward_star, DOWN, buff=0.15
        )

        # Q-table (right)
        table_data = [
            ["Q", "Q(1, up)", "Q(2, up)"],
            ["Q", "Q(1, left)", "Q(4, a')"],
            ["Q", "Q(3, a)", "Q(5, a')"],
            ["Q", "Q(4, dn)", "Q(6, an)"],
        ]
        col_labels = [
            Text("State 1", font_size=24, color=BLUE_D, weight=BOLD),
            Text("State 2", font_size=24, color=BLUE_D, weight=BOLD),
            Text("State 3", font_size=24, color=BLUE_D, weight=BOLD),
        ]
        q_table = Table(
            table_data,
            col_labels=col_labels,
            include_outer_lines=True,
            line_config={"stroke_color": BLUE_D, "stroke_width": 2},
        )
        q_table.scale(0.5)
        q_table.move_to(RIGHT * 4 + UP * 0.2)

        q_label = Text("Q-table", font_size=28, color=BLUE_D).next_to(q_table, DOWN, buff=0.2)
        q_arrow = CurvedArrow(
            q_label.get_left() + LEFT * 0.2,
            q_table.get_bottom() + UP * 0.2,
            angle=0.5,
            color=BLUE_D,
            stroke_width=3,
        )

        state_text = Text("state s_t", font_size=26, color=BLUE_D)
        state_arrow = CurvedArrow(
            grid_cells.get_right() + RIGHT * 0.2,
            q_table.get_left() + LEFT * 0.2,
            angle=-0.4,
            color=BLUE_D,
            stroke_width=3,
        )
        state_text.next_to(state_arrow, UP, buff=0.05)

        self.play(GrowFromCenter(reward_star), FadeIn(reward_label), run_time=0.9)
        self.play(
            FadeIn(q_table),
            FadeIn(q_label),
            Create(q_arrow),
            Create(state_arrow),
            FadeIn(state_text),
            run_time=1.6,
        )
        self.wait(0.4)

        # Update rule
        update_eq = MathTex(
            r"Q(s,a)\leftarrow Q(s,a)+\alpha\,[r+\gamma\max_{a'}Q(s',a')-Q(s,a)]",
            font_size=34,
            color=BLUE_D,
        )
        update_eq.to_edge(DOWN, buff=0.7)

        self.play(Write(update_eq), run_time=1.6)
        self.wait(0.4)

        # Extra key ideas
        concepts = VGroup(
            Text("1. Aprende Q(s,a) sin modelo del entorno.", font_size=24, color=GRAY_B),
            Text("2. Actualiza con TD: recompensa + mejor futuro.", font_size=24, color=GRAY_B),
            Text("3. Explora (epsilon) vs explota el max Q.", font_size=24, color=GRAY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        concepts.next_to(update_eq, UP, buff=0.3).shift(LEFT * 2.8)

        self.play(FadeIn(concepts, shift=UP * 0.2), run_time=1.2)
        self.wait(1.5)
