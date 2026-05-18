"""
Reverse-engineered MDP animation inspired by the external reference video.

The scene follows the reference structure:
1. Generic MDP components on the left.
2. Concrete example with states/actions on the right.
3. Transition graph with probabilities and rewards.
4. Agent-environment loop plus controller indicator.

Example:
    uv run manim-slides render slides/08_mdp_reverse.py MdpReverseSlide
"""

from manim import *
from manim_slides import Slide


STATE_COOL = GREEN
STATE_HOT = ORANGE
STATE_OVERHEAT = GRAY_A
ACTION_FAST = BLUE_B
ACTION_SLOW = RED_C
HIGHLIGHT = YELLOW
BODY = WHITE
SUBDUED = GRAY_A


def serif_math(tex: str, font_size: int = 34, color=BODY) -> MathTex:
    mob = MathTex(tex, font_size=font_size, color=color)
    return mob


def make_arrow_label(prob: str, reward: str, prob_pos: np.ndarray, reward_pos: np.ndarray):
    prob_mob = MathTex(prob, font_size=26, color=BODY).move_to(prob_pos)
    reward_color = RED_C if reward.startswith("-") else GREEN
    reward_mob = MathTex(reward, font_size=26, color=reward_color).move_to(reward_pos)
    return VGroup(prob_mob, reward_mob), prob_mob, reward_mob


class MdpReverseSlide(Slide):
    def construct(self):
        graph_shift = LEFT * 0.8
        example_shift = LEFT * 0.55
        loop_shift = RIGHT * 1.1

        generic_states = serif_math(
            r"\text{Estados: } S=\{s_1,s_2,\cdots,s_n\}",
            font_size=36,
        )
        generic_states.to_corner(UL, buff=0.75)

        generic_actions = serif_math(
            r"\text{Acciones: } A=\{a_1,a_2,\cdots,a_m\}",
            font_size=36,
        )
        generic_actions.next_to(generic_states, DOWN, aligned_edge=LEFT, buff=0.35)

        generic_transition = serif_math(
            r"\text{Funci\'on de transici\'on: } P(s_{t+1}\mid s_t,a_t)",
            font_size=34,
        )
        generic_transition.next_to(generic_actions, DOWN, aligned_edge=LEFT, buff=0.35)

        generic_reward = serif_math(
            r"\text{Funci\'on de recompensa: } R(s_t,a_t,s_{t+1})",
            font_size=34,
        )
        generic_reward.next_to(generic_transition, DOWN, aligned_edge=LEFT, buff=0.35)

        example_states = MathTex(
            r"S=\{",
            r"\text{Cool}",
            r",",
            r"\text{Hot}",
            r",",
            r"\text{Overheat}",
            r"\}",
            font_size=34,
        )
        example_states[1].set_color(STATE_COOL)
        example_states[3].set_color(STATE_HOT)
        example_states[5].set_color(STATE_OVERHEAT)
        example_states.move_to(RIGHT * 3.1 + UP * 3.0 + example_shift)

        example_actions = MathTex(
            r"A=\{",
            r"\text{Fast}",
            r",",
            r"\text{Slow}",
            r"\}",
            font_size=34,
        )
        example_actions[1].set_color(ACTION_FAST)
        example_actions[3].set_color(ACTION_SLOW)
        example_actions.next_to(example_states, DOWN, aligned_edge=RIGHT, buff=0.45)

        cool = Circle(radius=0.55, color=STATE_COOL, stroke_width=3).move_to(RIGHT * 1.25 + DOWN * 1.8 + graph_shift)
        hot = Circle(radius=0.55, color=STATE_HOT, stroke_width=3).move_to(RIGHT * 4.0 + UP * 0.25 + graph_shift)
        overheat = Circle(radius=0.55, color=STATE_OVERHEAT, stroke_width=3).move_to(RIGHT * 6.7 + DOWN * 0.2 + graph_shift)

        cool_label = Tex("Cool", font_size=26, color=STATE_COOL).move_to(cool)
        hot_label = Tex("Hot", font_size=26, color=STATE_HOT).move_to(hot)
        overheat_label = Tex("Overheat", font_size=22, color=STATE_OVERHEAT).move_to(overheat)

        cool_group = VGroup(cool, cool_label)
        hot_group = VGroup(hot, hot_label)
        overheat_group = VGroup(overheat, overheat_label)

        graph_nodes = VGroup(cool_group, hot_group, overheat_group)

        # Red / "Slow" transitions
        cool_to_hot = CurvedArrow(
            cool.get_top() + LEFT * 0.05,
            hot.get_left() + DOWN * 0.08,
            angle=-0.35,
            color=ACTION_SLOW,
            stroke_width=3,
            tip_length=0.22,
        )
        hot_to_overheat = CurvedArrow(
            hot.get_right() + DOWN * 0.02,
            overheat.get_left() + UP * 0.02,
            angle=-0.18,
            color=ACTION_SLOW,
            stroke_width=3,
            tip_length=0.22,
        )
        cool_slow_loop = CurvedArrow(
            cool.get_left() + UP * 0.38,
            cool.get_left() + DOWN * 0.38,
            angle=2.9,
            color=ACTION_SLOW,
            stroke_width=3,
            tip_length=0.18,
        )

        # Blue / "Fast" transitions
        hot_to_cool = CurvedArrow(
            hot.get_bottom() + LEFT * 0.04,
            cool.get_right() + UP * 0.06,
            angle=0.35,
            color=ACTION_FAST,
            stroke_width=3,
            tip_length=0.22,
        )
        hot_fast_loop = CurvedArrow(
            hot.get_right() + DOWN * 0.34,
            hot.get_top() + RIGHT * 0.28,
            angle=2.8,
            color=ACTION_FAST,
            stroke_width=3,
            tip_length=0.18,
        )
        cool_fast_loop = CurvedArrow(
            cool.get_left() + DOWN * 0.38,
            cool.get_bottom() + LEFT * 0.32,
            angle=2.8,
            color=ACTION_FAST,
            stroke_width=3,
            tip_length=0.18,
        )

        transitions = VGroup(
            cool_to_hot,
            hot_to_overheat,
            cool_slow_loop,
            hot_to_cool,
            hot_fast_loop,
            cool_fast_loop,
        )

        labels = VGroup()
        cool_hot_labels, prob_cool_hot, rew_cool_hot = make_arrow_label(
            "0.5",
            "+2",
            RIGHT * 2.3 + UP * 0.3 + graph_shift,
            RIGHT * 2.1 + UP * 0.8 + graph_shift,
        )
        labels.add(cool_hot_labels)

        hot_over_labels, prob_hot_over, rew_hot_over = make_arrow_label(
            "1.0",
            "-10",
            RIGHT * 5.6 + UP * 0.9 + graph_shift,
            RIGHT * 5.45 + UP * 1.45 + graph_shift,
        )
        labels.add(hot_over_labels)

        cool_loop_labels, prob_cool_loop, rew_cool_loop = make_arrow_label(
            "0.5",
            "+2",
            RIGHT * 0.8 + DOWN * 1.05 + graph_shift,
            RIGHT * 0.65 + DOWN * 0.45 + graph_shift,
        )
        labels.add(cool_loop_labels)

        hot_cool_labels, prob_hot_cool, rew_hot_cool = make_arrow_label(
            "0.5",
            "+1",
            RIGHT * 3.05 + DOWN * 0.45 + graph_shift,
            RIGHT * 3.35 + DOWN * 1.0 + graph_shift,
        )
        labels.add(hot_cool_labels)

        hot_loop_labels, prob_hot_loop, rew_hot_loop = make_arrow_label(
            "0.5",
            "+1",
            RIGHT * 4.35 + DOWN * 0.02 + graph_shift,
            RIGHT * 4.1 + DOWN * 0.82 + graph_shift,
        )
        labels.add(hot_loop_labels)

        cool_fast_labels, prob_cool_fast, rew_cool_fast = make_arrow_label(
            "1.0",
            "+1",
            RIGHT * 0.45 + DOWN * 2.2 + graph_shift,
            LEFT * 0.1 + DOWN * 2.45 + graph_shift,
        )
        labels.add(cool_fast_labels)

        # Yellow highlights used later in the animation.
        cool_fast_highlight = cool_fast_loop.copy().set_color(HIGHLIGHT).set_stroke(width=4)
        hot_over_highlight = hot_to_overheat.copy().set_color(HIGHLIGHT).set_stroke(width=4)
        cool_node_highlight = Circle(radius=0.7, color=HIGHLIGHT, stroke_width=3).move_to(cool)
        dot_on_slow_loop = Dot(cool_slow_loop.point_from_proportion(0.18), color=HIGHLIGHT, radius=0.08)

        # Agent-environment diagram for the second phase.
        agent_box = Rectangle(width=2.0, height=1.0, color=HIGHLIGHT, stroke_width=3)
        agent_text = Tex("Agent", font_size=30, color=HIGHLIGHT).move_to(agent_box)
        agent_group = VGroup(agent_box, agent_text).move_to(LEFT * 4.6 + DOWN * 0.1 + loop_shift)

        env_box = Rectangle(width=2.8, height=1.15, color=RED_C, stroke_width=3)
        env_text = Tex("Environment", font_size=28, color=RED_C).move_to(env_box)
        env_group = VGroup(env_box, env_text).move_to(LEFT * 4.75 + DOWN * 2.0 + loop_shift)

        obs_up = Arrow(
            env_group.get_left() + UP * 0.2 + LEFT * 1.2,
            agent_group.get_left(),
            buff=0.05,
            color=BODY,
            stroke_width=3,
            tip_length=0.18,
        )
        obs_down = Arrow(
            env_group.get_left() + UP * 1.1 + LEFT * 1.2,
            agent_group.get_left() + UP * 0.35,
            buff=0.05,
            color=BODY,
            stroke_width=3,
            tip_length=0.18,
        )
        action_arrow = Arrow(
            agent_group.get_right(),
            env_group.get_right() + UP * 0.05,
            buff=0.05,
            color=BODY,
            stroke_width=3,
            tip_length=0.18,
        )
        env_return = Arrow(
            env_group.get_left() + DOWN * 0.1,
            env_group.get_left() + DOWN * 0.1 + LEFT * 1.7,
            buff=0.05,
            color=BODY,
            stroke_width=3,
            tip_length=0.18,
        )
        env_return_up = Arrow(
            env_group.get_left() + DOWN * 0.1 + LEFT * 1.7,
            agent_group.get_left() + DOWN * 0.35 + LEFT * 1.7,
            buff=0.02,
            color=BODY,
            stroke_width=3,
            tip_length=0.16,
        )
        env_return_right = Arrow(
            agent_group.get_left() + DOWN * 0.35 + LEFT * 1.7,
            agent_group.get_left() + DOWN * 0.35,
            buff=0.02,
            color=BODY,
            stroke_width=3,
            tip_length=0.16,
        )

        o_label = serif_math("o", font_size=26).next_to(obs_up, LEFT, buff=0.2)
        r_label = serif_math("r", font_size=26).next_to(env_return_right, LEFT, buff=0.15)
        a_label = serif_math("a", font_size=26).next_to(action_arrow, RIGHT, buff=0.15)

        loop_group = VGroup(
            agent_group,
            env_group,
            obs_up,
            obs_down,
            action_arrow,
            env_return,
            env_return_up,
            env_return_right,
            o_label,
            r_label,
            a_label,
        )

        # Robot/controller icon.
        robot_head = RoundedRectangle(
            corner_radius=0.35,
            width=1.2,
            height=0.75,
            color=BODY,
            stroke_width=3,
        )
        robot_head.move_to(LEFT * 5.15 + UP * 2.0 + loop_shift)
        robot_antenna = Line(robot_head.get_top(), robot_head.get_top() + UP * 0.45, color=BODY, stroke_width=3)
        robot_dot = Dot(robot_antenna.get_end(), color=BODY, radius=0.08)
        robot_eye_left = Dot(robot_head.get_center() + LEFT * 0.28, color=BODY, radius=0.06)
        robot_eye_right = Dot(robot_head.get_center() + RIGHT * 0.28, color=BODY, radius=0.06)
        robot_group = VGroup(robot_head, robot_antenna, robot_dot, robot_eye_left, robot_eye_right)

        token_outline = Circle(radius=0.32, color=SUBDUED, stroke_width=2).move_to(LEFT * 3.95 + UP * 2.25 + loop_shift)
        token_red = Circle(radius=0.32, color=RED_C, fill_color=RED_C, fill_opacity=1, stroke_width=2).move_to(token_outline)
        token_blue = Circle(radius=0.32, color=ACTION_FAST, fill_color=ACTION_FAST, fill_opacity=1, stroke_width=2).move_to(token_outline)

        # Step 1
        self.play(FadeIn(generic_states))
        self.play(FadeIn(example_states), FadeIn(graph_nodes))
        self.next_slide()

        # Step 2
        self.play(FadeIn(generic_actions), FadeIn(example_actions))
        self.next_slide()

        # Step 3
        self.play(FadeIn(generic_transition))
        self.play(
            Create(cool_to_hot),
            Create(hot_to_cool),
            Create(cool_fast_loop),
            Create(cool_slow_loop),
            Create(hot_fast_loop),
            Create(hot_to_overheat),
            FadeIn(prob_cool_hot),
            FadeIn(prob_hot_cool),
            FadeIn(prob_cool_loop),
            FadeIn(prob_hot_loop),
            FadeIn(prob_cool_fast),
            FadeIn(prob_hot_over),
        )
        self.next_slide()

        # Step 4
        self.play(FadeIn(generic_reward))
        self.play(
            FadeIn(rew_cool_hot),
            FadeIn(rew_hot_cool),
            FadeIn(rew_cool_loop),
            FadeIn(rew_hot_loop),
            FadeIn(rew_cool_fast),
            FadeIn(rew_hot_over),
        )
        self.next_slide()

        # Step 5
        self.play(
            FadeIn(cool_fast_highlight),
            FadeIn(hot_over_highlight),
            FadeIn(cool_node_highlight),
        )
        self.next_slide()

        # Step 6
        self.play(
            FadeOut(generic_states),
            FadeOut(generic_actions),
            FadeOut(generic_transition),
            FadeOut(generic_reward),
            FadeOut(cool_fast_highlight),
            FadeOut(hot_over_highlight),
            FadeOut(cool_node_highlight),
        )
        self.play(FadeIn(loop_group))
        self.next_slide()

        # Step 7
        self.play(FadeIn(robot_group), FadeIn(token_outline))
        self.next_slide()

        # Step 8
        self.play(
            ReplacementTransform(token_outline, token_red),
            FadeIn(dot_on_slow_loop),
        )
        self.next_slide()

        # Step 9
        cool_flash = Circle(radius=0.52, color=HIGHLIGHT, fill_color=HIGHLIGHT, fill_opacity=0.25, stroke_width=0)
        cool_flash.move_to(cool)
        self.play(
            ReplacementTransform(token_red, token_blue),
            FadeOut(dot_on_slow_loop),
            FadeIn(cool_flash),
        )
        self.next_slide()

        # Step 10
        self.play(FadeOut(loop_group), FadeOut(robot_group), FadeOut(token_blue), FadeOut(cool_flash))
        self.wait(0.8)
