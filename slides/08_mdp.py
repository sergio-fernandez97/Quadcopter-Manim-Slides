from manim import *

class StateDiagramAnimation(Scene):
    def construct(self):
        title = Text("Proceso de Decisión de Markov (MDP)", font_size=44)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(1.0)

        intro_equation = MathTex(
            r"x_0 \in \mathcal{X}, \quad u_0 \in \mathcal{U}(x_0)",
            font_size=36,
        )
        intro_label = Text("la dinámica comienza con estado inicial", font_size=24)
        intro_group = VGroup(intro_equation, intro_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(FadeIn(intro_equation), FadeIn(intro_label))

        x_label = Text("Conjunto de estados", font_size=22).next_to(
            intro_equation.get_part_by_tex(r"\mathcal{X}"), UP, buff=0.2
        )
        x_arrow = Arrow(
            x_label.get_bottom(),
            intro_equation.get_part_by_tex(r"\mathcal{X}").get_top(),
            buff=0.05,
        )
        self.play(GrowArrow(x_arrow), FadeIn(x_label))

        u_label = Text("Conjunto de acciones", font_size=22).next_to(
            intro_equation.get_part_by_tex(r"\mathcal{U}"), DOWN, buff=0.2
        )
        u_arrow = Arrow(
            u_label.get_top(),
            intro_equation.get_part_by_tex(r"\mathcal{U}").get_bottom(),
            buff=0.05,
        )
        self.play(GrowArrow(u_arrow), FadeIn(u_label))
        self.play(FadeOut(x_label), FadeOut(x_arrow), FadeOut(u_label), FadeOut(u_arrow))
        self.wait(0.4)

        transition_eq = MathTex(r"p(x_1 \mid u_0, x_0)", font_size=36)
        transition_label = Text("probabilidad de transición a x_1", font_size=24)
        transition_group = VGroup(transition_eq, transition_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(Transform(intro_group, transition_group))
        self.wait(0.5)

        sequence_eq = MathTex(
            r"x_1, u_1 \rightarrow p(x_2 \mid u_1, x_1) \rightarrow x_2",
            font_size=36,
        )
        sequence_label = Text("y así sucesivamente...", font_size=24)
        sequence_group = VGroup(sequence_eq, sequence_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(Transform(intro_group, sequence_group))
        self.wait(0.6)

        trajectory_eq = MathTex(
            r"x_0 \xrightarrow{u_0} x_1 \xrightarrow{u_1} x_2 \xrightarrow{u_2} \cdots "
            r"x_{t-1} \xrightarrow{u_{t-1}} x_{t} \xrightarrow{u_t} \cdots",
            font_size=32,
        )
        trajectory_label = Text("sucesión de estados y acciones", font_size=24)
        trajectory_group = VGroup(trajectory_eq, transition_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(Transform(intro_group, trajectory_group))
        self.wait(0.6)

        history_eq = MathTex(
            r"p(x_{t+1} \mid (x_0, u_0), (x_1, u_1), \cdots, (x_{t-1}, u_{t-1}), (x_t, u_t))",
            font_size=30,
        )
        history_label = Text("dinámica con historia completa", font_size=24)
        history_group = VGroup(history_eq, history_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(Transform(intro_group, history_group))
        self.wait(0.6)

        markov_eq = MathTex(r"p(x_{t+1} \mid u_t, x_t)", font_size=36)
        markov_label = Text("propiedad de markov", font_size=24)
        markov_group = VGroup(markov_eq, markov_label).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(Transform(intro_group, markov_group))
        self.wait(0.6)

        self.play(FadeOut(intro_group))

        subtitle = Text("Ejemplo: Robot de reciclaje", font_size=30)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        self.play(FadeIn(subtitle))

        problem_heading = Text("Planteamiento de problema", font_size=32)
        problem_points = BulletedList(
            "En cada paso de tiempo el robot tiene que decidir sobre lo siguiente:\n- Buscar latas activamente.\n- Esperar a que alguien traiga una lata.\n- Regresar a la base y recargar.",
            "Las decisiones se toman a partir del estado de la batería: high, low.",
            "La recompensa esta en función del número de latas recolectads.",
            font_size=26,
            buff=0.2,
        )
        problem_group = VGroup(problem_heading, problem_points).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_group))
        self.wait(1.0)

        elements_bullet = MathTex(
            r"\begin{aligned}"
            r"&\bullet\ \mathcal{S}=\{\text{high}, \text{low}\}.\\"
            r"&\bullet\ \mathcal{U}(\text{high})=\{\text{search}, \text{wait}\}.\\"
            r"&\bullet\ \mathcal{U}(\text{low})=\{\text{search}, \text{wait}, \text{recharge}\}.\\"
            r"&\bullet\ r_{\text{wait}}:= \# \text{esperado de latas}.\\"
            r"&\bullet\ r_{\text{search}}:= \# \text{esperado de latas}.\\"
            r"&\bullet\ r_{\text{search}} > r_{\text{wait}}."
            r"\end{aligned}",
            font_size=28,
        ).move_to(problem_group)
        self.play(Transform(problem_group, elements_bullet))
        self.wait(1.0)
        self.play(FadeOut(problem_group), FadeOut(title_group))

        # Create states
        high = Circle(radius=0.8, color=WHITE).shift(LEFT * 3)
        high_text = Text("high", font_size=32, color=YELLOW).move_to(high)
        high_group = VGroup(high, high_text)
        
        low = Circle(radius=0.8, color=WHITE).shift(RIGHT * 3)
        low_text = Text("low", font_size=32, color=YELLOW).move_to(low)
        low_group = VGroup(low, low_text)
        
        # Create action nodes (smaller and filled)
        wait_top = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(LEFT * 3 + UP * 2.5)
        wait_top_text = Text("wait", font_size=18).next_to(wait_top, LEFT, buff=0.2)
        wait_top_group = VGroup(wait_top, wait_top_text)
        
        search_top = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(RIGHT * 3 + UP * 2.5)
        search_top_text = Text("search", font_size=18).next_to(search_top, RIGHT, buff=0.2)
        search_top_group = VGroup(search_top, search_top_text)
        
        search_bottom = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(LEFT * 3 + DOWN * 2.5)
        search_bottom_text = Text("search", font_size=18).next_to(search_bottom, LEFT, buff=0.2)
        search_bottom_group = VGroup(search_bottom, search_bottom_text)
        
        wait_bottom = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(RIGHT * 3 + DOWN * 2.5)
        wait_bottom_text = Text("wait", font_size=18).next_to(wait_bottom, RIGHT, buff=0.2)
        wait_bottom_group = VGroup(wait_bottom, wait_bottom_text)

        recharge = Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLUE).move_to(ORIGIN)
        recharge_text = Text("recharge", font_size=18).next_to(recharge, UP, buff=0.2)
        recharge_group = VGroup(recharge, recharge_text)

        estados_label = Text("estados", font_size=26, color=YELLOW).move_to(LEFT * 6.2 + UP * 2.2)
        acciones_label = Text("acciones", font_size=24, color=BLUE).move_to(LEFT * 6.2 + UP * 0.6)

        prob_legend = Text("probabilidades de transición", font_size=22, color=LIGHT_GREY).move_to(LEFT * 5.2 + DOWN * 0.8)
        rewards_prefix = Text("recompensas ( ", font_size=22, color=WHITE)
        rewards_plus = Text("+", font_size=22, color=GREEN)
        rewards_comma = Text(",  ", font_size=22, color=WHITE)
        rewards_minus = Text("-", font_size=22, color=RED)
        rewards_suffix = Text(" )", font_size=22, color=WHITE)
        rewards_legend = VGroup(
            rewards_prefix, rewards_plus, rewards_comma, rewards_minus, rewards_suffix
        ).arrange(RIGHT, buff=0.05)
        rewards_legend.move_to(LEFT * 5.5 + DOWN * 1.6)

        def transition_label(prob_tex, reward_tex, reward_negative=False):
            label = MathTex(prob_tex, ",", reward_tex, font_size=24)
            label.set_color_by_tex(prob_tex, LIGHT_GREY)
            label.set_color_by_tex(reward_tex, RED if reward_negative else GREEN)
            label.set_color_by_tex(",", WHITE)
            return label
        
        # Self-loop labels (without green arrows)
        wait_top_label = transition_label("1", r"r_{\text{wait}}").move_to(LEFT * 3 + UP * 3.5)
        
        # search_top self-loop label
        search_top_label = transition_label(r"\beta", r"r_{\text{search}}").move_to(RIGHT * 3 + UP * 3.5)
        
        # search_bottom self-loop label
        search_bottom_label = transition_label(r"\alpha", r"r_{\text{search}}").move_to(LEFT * 3 + DOWN * 3.5)
        
        # wait_bottom self-loop label
        wait_bottom_label = transition_label("1", r"r_{\text{wait}}").move_to(RIGHT * 3 + DOWN * 3.5)
        
        # Create transitions between states and actions
        # high to wait_top
        high_wait_top = Arrow(high.get_top() + LEFT*0.3, wait_top.get_bottom(), color=WHITE, buff=0.05)
        
        # wait_top to high
        wait_top_high = Arrow(wait_top.get_bottom() + RIGHT*0.05, high.get_top() + RIGHT*0.3, color=WHITE, buff=0.05)
        
        # low to search_top
        low_search_top = CurvedArrow(low.get_top() + RIGHT*0.3, search_top.get_bottom(), angle=-0.3, color=WHITE)

        # search_top to low
        search_top_low = CurvedArrow(search_top.get_bottom() + LEFT*0.05, low.get_top() + LEFT*0.3, angle=-0.3, color=WHITE)
        search_top_low_label = transition_label(r"1-\beta", "-3", reward_negative=True).move_to(RIGHT * 1.5 + UP * 1.2)

        # search_top to high
        search_top_high = CurvedArrow(search_top.get_left() + DOWN*0.05, high.get_top() + RIGHT*0.3, angle=0.3, color=WHITE)
        
        # low to recharge to high
        low_recharge = Arrow(low.get_left(), recharge.get_right(), color=WHITE, buff=0.1)
        recharge_high = Arrow(recharge.get_left(), high.get_right(), color=WHITE, buff=0.1)
        low_high_label = transition_label("1", "0").next_to(recharge, UP, buff=0.6)
        
        # high to search_bottom
        high_search_bottom = Arrow(high.get_bottom() + LEFT*0.3, search_bottom.get_top(), color=WHITE, buff=0.05)
        
        # search_bottom to high
        search_bottom_high = Arrow(search_bottom.get_top() + RIGHT*0.05, high.get_bottom() + RIGHT*0.3, color=WHITE, buff=0.05)
        
        # search_bottom to low
        search_bottom_low = CurvedArrow(search_bottom.get_right(), low.get_bottom() + LEFT*0.3, angle=-0.5, color=WHITE)
        search_bottom_low_label = transition_label(r"1-\alpha", r"r_{\text{search}}").move_to(LEFT * 0.3 + DOWN * 2)
        
        # low to wait_bottom
        low_wait_bottom = Arrow(low.get_bottom() + RIGHT*0.3, wait_bottom.get_top(), color=WHITE, buff=0.05)
        
        # wait_bottom to low
        wait_bottom_low = Arrow(wait_bottom.get_top() + LEFT*0.05, low.get_bottom() + LEFT*0.3, color=WHITE, buff=0.05)
        
        # Animate
        self.play(
            Create(high_group),
            Create(low_group),
            FadeIn(estados_label)
        )
        self.wait(0.5)
        
        self.play(
            Create(wait_top_group),
            Create(search_top_group),
            Create(search_bottom_group),
            Create(wait_bottom_group),
            Create(recharge_group),
            FadeIn(acciones_label),
            FadeIn(prob_legend),
            FadeIn(rewards_legend)
        )
        self.wait(0.5)
        
        # Add transitions to action nodes and back
        # high <-> wait_top
        self.play(Create(high_wait_top))
        self.play(Write(wait_top_label))
        self.play(Create(wait_top_high))
        
        # low <-> search_top
        self.play(Create(low_search_top))
        self.play(Write(search_top_label))
        self.play(
            Create(search_top_low),
            Write(search_top_low_label)
        )
        self.play(Create(search_top_high))
        
        # low -> recharge -> high
        self.play(
            Create(low_recharge),
            Create(recharge_high),
            Write(low_high_label)
        )
        
        # high <-> search_bottom
        self.play(Create(high_search_bottom))
        self.play(Write(search_bottom_label))
        self.play(Create(search_bottom_high))
        
        # search_bottom -> low
        self.play(
            Create(search_bottom_low),
            Write(search_bottom_low_label)
        )
        
        # low <-> wait_bottom
        self.play(Create(low_wait_bottom))
        self.play(Write(wait_bottom_label))
        self.play(Create(wait_bottom_low))
        
        self.wait(2)
        
        # Optional: Animate a path through the states
        dot = Dot(color=RED, radius=0.15).move_to(high)
        self.play(FadeIn(dot))
        
        # Example path: high -> search_bottom -> high
        self.play(MoveAlongPath(dot, high_search_bottom.copy()), run_time=0.8)
        self.wait(0.3)
        self.play(MoveAlongPath(dot, search_bottom_high.copy()), run_time=0.8)
        
        x_label = MathTex("x", font_size=26, color=YELLOW).move_to(estados_label)
        u_label = MathTex("u", font_size=24, color=BLUE).move_to(acciones_label)
        prob_label = MathTex(
            r"p(x'|u, x)",
            font_size=22,
            color=LIGHT_GREY,
        ).move_to(prob_legend)
        rewards_label = MathTex(r"r(x', u, u')", font_size=22, color=WHITE).move_to(rewards_legend)

        self.play(
            Transform(estados_label, x_label),
            Transform(acciones_label, u_label),
            Transform(prob_legend, prob_label),
            Transform(rewards_legend, rewards_label),
        )
        self.wait(2)
