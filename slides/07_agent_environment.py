"""
Agent–environment interaction in reinforcement learning.

Illustrates the RL loop with agent, environment, actions, observations, and
rewards, highlighting the data flow for the quadcopter training setup.

Example:
    manim -pql slides/07_agent_environment.py AgentEnvironmentSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide

class AgentEnvironmentSlide(Slide):
    def construct(self):
        # Standalone title: Reinforcement Learning
        rl_title = Text("Aprendizaje por Refuerzo", font_size=64, color=YELLOW, weight=BOLD)
        rl_title.move_to(ORIGIN)
        self.play(FadeIn(rl_title), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(rl_title), run_time=1)
        self.wait(0.5)
        
        # Title
        title = Text("Interacción Agente–Entorno", font_size=48, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.add(title)
        self.wait(1)
        
        # Create the loop components in Sutton style
        # Agent box (left side)
        agent_box = Rectangle(
            width=3, height=2, 
            color=BLUE, fill_opacity=0.2, stroke_width=2
        ).shift(LEFT * 3)
        agent_label = Text("Agente", font_size=36, color=BLUE, weight=BOLD).move_to(agent_box.get_center())
        
        # Environment box (right side)
        env_box = Rectangle(
            width=3, height=2,
            color=GREEN, fill_opacity=0.2, stroke_width=2
        ).shift(RIGHT * 3)
        env_label = Text("Entorno", font_size=36, color=GREEN, weight=BOLD).move_to(env_box.get_center())
        
        # State input arrow (from left into Agent) - Sutton style
        state_input_arrow = Arrow(
            start=LEFT * 5.5,
            end=agent_box.get_left(),
            color=BLUE, stroke_width=3, buff=0.1
        )
        x_t_label_input = MathTex(r"x_t", font_size=32, color=BLUE).next_to(state_input_arrow, UP, buff=0.1)
        
        # Action arrow (Agent → Environment) - horizontal
        action_arrow = Arrow(
            start=agent_box.get_right(),
            end=env_box.get_left(),
            color=ORANGE, stroke_width=3, buff=0.1
        )
        a_t_label = MathTex(r"a_t", font_size=32, color=ORANGE).next_to(action_arrow, UP, buff=0.1)
        
        # Reward and Next State arrow (Environment → Agent) - horizontal back
        reward_state_arrow = Arrow(
            start=env_box.get_left(),
            end=agent_box.get_right(),
            color=PURPLE, stroke_width=3, buff=0.1
        ).shift(DOWN * 1.2)
        r_t_label = MathTex(r"r_t", font_size=32, color=GOLD).next_to(reward_state_arrow, DOWN, buff=0.1).shift(LEFT * 0.3)
        x_t1_label_arrow = MathTex(r"x_{t+1}", font_size=32, color=BLUE).next_to(reward_state_arrow, DOWN, buff=0.1).shift(RIGHT * 0.3)
        
        # Add sensor icon on state input
        sensor_icon = VGroup(
            Circle(radius=0.15, color=YELLOW, fill_opacity=0.5),
            Dot(radius=0.05, color=YELLOW)
        )
        sensor_icon.next_to(x_t_label_input, LEFT, buff=0.1)
        
        # Add actuator icon on action
        actuator_icon = VGroup(
            RegularPolygon(n=6, radius=0.15, color=RED, fill_opacity=0.5),
            Dot(radius=0.05, color=RED)
        )
        actuator_icon.next_to(a_t_label, RIGHT, buff=0.1)
        
        # Draw the loop in Sutton style
        self.play(
            FadeIn(agent_box), FadeIn(agent_label),
            FadeIn(env_box), FadeIn(env_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Show state input arrow
        self.play(
            Create(state_input_arrow), 
            FadeIn(sensor_icon),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Show action arrow
        self.play(
            Create(action_arrow), 
            FadeIn(actuator_icon),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Show reward and next state arrow
        self.play(
            Create(reward_state_arrow),
            run_time=1.5
        )
        self.wait(1)
        
        # Animation sequence in Sutton style
        # Step 1: State x_t enters Agent from left
        x_t_token = MathTex(r"x_t", font_size=36, color=BLUE, background_stroke_width=4, background_stroke_color=WHITE)
        x_t_token.move_to(LEFT * 5.5)
        estado_text = Text("Estado", font_size=20, color=BLUE).next_to(x_t_token, DOWN, buff=0.2)
        
        self.play(
            FadeIn(x_t_token),
            FadeIn(x_t_label_input),
            FadeIn(estado_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Move x_t along input arrow to Agent (move text with token)
        x_t_group = VGroup(x_t_token, estado_text)
        self.play(
            x_t_group.animate.move_to(agent_box.get_center()),
            run_time=2
        )
        self.wait(0.5)
        
        # Step 2: Agent outputs action a_t
        a_t_token = MathTex(r"a_t", font_size=36, color=ORANGE, background_stroke_width=4, background_stroke_color=WHITE)
        a_t_token.move_to(agent_box.get_center())
        accion_text = Text("Acción", font_size=20, color=ORANGE).next_to(a_t_token, DOWN, buff=0.2)
        
        self.play(
            FadeOut(x_t_group),
            FadeIn(a_t_token),
            FadeIn(a_t_label),
            FadeIn(accion_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Move a_t along action arrow to Environment (move text with token)
        a_t_group = VGroup(a_t_token, accion_text)
        self.play(
            a_t_group.animate.move_to(env_box.get_center()),
            run_time=2
        )
        self.wait(0.5)
        
        # Step 3: Environment returns reward r_t and next state x_{t+1}
        r_t_token = MathTex(r"r_t", font_size=36, color=GOLD, background_stroke_width=4, background_stroke_color=WHITE)
        r_t_token.move_to(env_box.get_center() + LEFT * 0.4)
        recompensa_text = Text("Recompensa", font_size=20, color=GOLD).next_to(r_t_token, DOWN, buff=0.2)
        
        x_t1_token = MathTex(r"x_{t+1}", font_size=36, color=BLUE, background_stroke_width=4, background_stroke_color=WHITE)
        x_t1_token.move_to(env_box.get_center() + RIGHT * 0.4)
        estado_siguiente_text = Text("Estado Siguiente", font_size=20, color=BLUE).next_to(x_t1_token, DOWN, buff=0.2)
        
        self.play(
            FadeOut(a_t_group),
            FadeIn(r_t_token),
            FadeIn(x_t1_token),
            FadeIn(r_t_label),
            FadeIn(x_t1_label_arrow),
            FadeIn(recompensa_text),
            FadeIn(estado_siguiente_text),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Step 4: Move r_t and x_{t+1} back to Agent along reward/state arrow
        # Calculate midpoint along the arrow
        arrow_start = env_box.get_left() + DOWN * 1.2
        arrow_end = agent_box.get_right() + DOWN * 1.2
        mid_point = (arrow_start + arrow_end) / 2
        
        r_t_group = VGroup(r_t_token, recompensa_text)
        x_t1_group = VGroup(x_t1_token, estado_siguiente_text)
        
        self.play(
            r_t_group.animate.move_to(mid_point + UP * 0.2),
            x_t1_group.animate.move_to(mid_point + DOWN * 0.2),
            run_time=2
        )
        self.wait(0.3)
        
        self.play(
            r_t_group.animate.move_to(arrow_end + UP * 0.2),
            x_t1_group.animate.move_to(arrow_end + DOWN * 0.2),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Step 5: x_{t+1} becomes x_t for next iteration (move to input position)
        x_t_new = MathTex(r"x_t", font_size=36, color=BLUE, background_stroke_width=4, background_stroke_color=WHITE)
        x_t_new.move_to(LEFT * 5.5)
        estado_new = Text("Estado", font_size=20, color=BLUE).next_to(x_t_new, DOWN, buff=0.2)
        x_t_new_group = VGroup(x_t_new, estado_new)
        
        self.play(
            FadeOut(r_t_group),
            Transform(x_t1_group, x_t_new_group),
            run_time=1.5
        )
        self.wait(1)
        
        # Show the complete loop label
        loop_label = Text("El ciclo continúa...", font_size=28, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(loop_label), run_time=1)
        self.wait(2)

