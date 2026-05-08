"""
Q-learning slide: Bellman optimality, Robbins-Monro derivation, TD error,
exploration vs exploitation, epsilon-greedy algorithm, and TicTacToe example.

Example:
    uv run manim-slides render slides/09_q_learning.py QLearningSlide
"""

from manim import *
from manim_slides import Slide


class QLearningSlide(Slide):
    def construct(self):
        # === TITLE ===
        title = Text("Q-learning", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === ECUACION OPTIMA DE BELLMAN ===
        bellman_label = Text("Ecuacion optima de Bellman", font_size=32, color=BLUE)
        bellman_eq = MathTex(
            r"Q_{*}(x, u) = \mathbb{E}\left[R_{t+1} + \gamma\max_{u'}Q_{*}(X_{t+1}, u') \mid X_t=x, U_t=u\right]",
            font_size=30,
        )
        bellman_desc = Text(
            "Q-learning resuelve directamente esta ecuacion en terminos de Q*",
            font_size=22,
            color=GRAY_B,
        )
        bellman_group = VGroup(bellman_label, bellman_eq, bellman_desc).arrange(
            DOWN, buff=0.25
        )
        bellman_group.next_to(title, DOWN, buff=0.5)

        bellman_box = RoundedRectangle(
            corner_radius=0.2,
            width=bellman_group.width + 0.8,
            height=bellman_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        bellman_box.move_to(bellman_group)

        self.play(FadeIn(bellman_box), FadeIn(bellman_group))
        self.wait(0.5)
        self.next_slide()

        no_model = Text(
            "No requiere conocer un modelo del entorno",
            font_size=24,
            color=GREEN,
        )
        no_model.next_to(bellman_box, DOWN, buff=0.4)
        self.play(FadeIn(no_model))
        self.wait(0.5)
        self.next_slide()

        # Clear Bellman section
        self.play(
            FadeOut(bellman_box),
            FadeOut(bellman_group),
            FadeOut(no_model),
        )
        self.wait(0.3)

        # === METODO ROBBINS-MONRO ===
        rm_label = Text("Metodo Robbins-Monro", font_size=32, color=BLUE)
        rm_label.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(rm_label))
        self.wait(0.3)

        rm_desc = Text(
            "Metodo iterativo para encontrar raices de g(w) = 0\nusando observaciones ruidosas",
            font_size=22,
            color=GRAY_B,
            line_spacing=1.2,
        )
        rm_desc.next_to(rm_label, DOWN, buff=0.3)
        self.play(FadeIn(rm_desc))
        self.wait(0.5)
        self.next_slide()

        rm_eq = MathTex(
            r"w_{k+1} = w_{k} - \alpha_k \tilde{g}(w_k, \eta_k)",
            font_size=34,
        )
        rm_eq.next_to(rm_desc, DOWN, buff=0.4)

        rm_eq_box = RoundedRectangle(
            corner_radius=0.2,
            width=rm_eq.width + 0.8,
            height=rm_eq.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        rm_eq_box.move_to(rm_eq)

        self.play(FadeIn(rm_eq_box), FadeIn(rm_eq))
        self.wait(0.5)
        self.next_slide()

        rm_noise = Text(
            "Solo requiere observaciones ruidosas: g_tilde(w, eta) = g(w) + eta",
            font_size=20,
            color=GRAY_B,
        )
        rm_noise.next_to(rm_eq_box, DOWN, buff=0.4)
        self.play(FadeIn(rm_noise))
        self.wait(0.5)
        self.next_slide()

        # Clear RM section
        self.play(
            FadeOut(rm_label),
            FadeOut(rm_desc),
            FadeOut(rm_eq),
            FadeOut(rm_eq_box),
            FadeOut(rm_noise),
        )
        self.wait(0.3)

        # === DERIVACION DE Q-LEARNING VIA ROBBINS-MONRO ===
        deriv_label = Text(
            "Derivacion de Q-learning via Robbins-Monro",
            font_size=32,
            color=BLUE,
        )
        deriv_label.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(deriv_label))
        self.wait(0.3)

        # Step 1: g(Q*)
        g_label = Text("Funcion g cuya raiz es la ecuacion de Bellman:", font_size=22, color=GRAY_B)
        g_label.next_to(deriv_label, DOWN, buff=0.4)

        g_eq = MathTex(
            r"g(Q_{*}(x, u)) = Q_{*}(x, u) - \mathbb{E}[R + \gamma \max_{u'}Q_{*}(X', u') \mid x, u]",
            font_size=28,
        )
        g_eq.next_to(g_label, DOWN, buff=0.3)

        self.play(FadeIn(g_label), FadeIn(g_eq))
        self.wait(0.5)
        self.next_slide()

        # Step 2: tilde{g} (biased observation)
        gtilde_label = Text("Observacion con muestras:", font_size=22, color=GRAY_B)
        gtilde_label.next_to(g_eq, DOWN, buff=0.4)

        gtilde_eq = MathTex(
            r"\tilde{g}(Q_{*}(x,u)) = Q_{*}(x, u) - [r_k + \gamma \max_{u'} Q_{*}(x_k', u')]",
            font_size=28,
        )
        gtilde_eq.next_to(gtilde_label, DOWN, buff=0.3)

        self.play(FadeIn(gtilde_label), FadeIn(gtilde_eq))
        self.wait(0.5)
        self.next_slide()

        # Step 3: Decomposition
        decomp_label = Text("Descomposicion en g + ruido:", font_size=22, color=GRAY_B)
        decomp_label.next_to(gtilde_eq, DOWN, buff=0.4)

        decomp_eq = MathTex(
            r"\tilde{g} = \underbrace{Q_*(x,u) - \mathbb{E}[R + \gamma \max_{u'} Q_*(X', u') \mid x, u]}_{g(Q_*(x,u))}",
            r"+ \underbrace{\mathbb{E}[\cdots] - [r_k + \gamma \max_{u'} Q_*(x_k', u')]}_{\eta}",
            font_size=22,
        )
        decomp_eq.next_to(decomp_label, DOWN, buff=0.3)

        self.play(FadeIn(decomp_label), FadeIn(decomp_eq))
        self.wait(0.5)
        self.next_slide()

        # Clear derivation steps
        self.play(
            FadeOut(deriv_label),
            FadeOut(g_label),
            FadeOut(g_eq),
            FadeOut(gtilde_label),
            FadeOut(gtilde_eq),
            FadeOut(decomp_label),
            FadeOut(decomp_eq),
        )
        self.wait(0.3)

        # Step 4: RM applied to Q
        rm_app_label = Text(
            "Aplicacion de Robbins-Monro a Q*",
            font_size=32,
            color=BLUE,
        )
        rm_app_label.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(rm_app_label))
        self.wait(0.3)

        rm_q_pre = MathTex(
            r"Q^{(k+1)}(x, u) = Q^{(k)}(x, u) - \alpha_k \left( Q^{(k)}(x, u) - [r_k + \gamma \max_{u'} Q_*(x_k', u')] \right)",
            font_size=26,
        )
        rm_q_pre.next_to(rm_app_label, DOWN, buff=0.5)

        self.play(FadeIn(rm_q_pre))
        self.wait(0.5)
        self.next_slide()

        # Clear RM application
        self.play(FadeOut(rm_app_label), FadeOut(rm_q_pre))
        self.wait(0.3)

        # === BOOTSTRAPPING ===
        boot_label = Text("Bootstrapping", font_size=32, color=BLUE)
        boot_label.next_to(title, DOWN, buff=0.5)

        boot_def = Text(
            "Se usan muestras secuenciales (x_t, u_t, r_{t+1}, x_{t+1})\ny se reemplaza Q* por la estimacion actual Q^(k)",
            font_size=22,
            color=GRAY_B,
            line_spacing=1.2,
        )

        boot_group = VGroup(boot_label, boot_def).arrange(DOWN, buff=0.3)
        boot_group.next_to(title, DOWN, buff=0.5)

        boot_box = RoundedRectangle(
            corner_radius=0.2,
            width=boot_group.width + 0.8,
            height=boot_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        boot_box.move_to(boot_group)

        self.play(FadeIn(boot_box), FadeIn(boot_group))
        self.wait(0.5)
        self.next_slide()

        # Final Q-learning update
        final_label = Text("Regla de actualizacion Q-learning", font_size=24, color=GREEN)
        final_eq = MathTex(
            r"Q^{(k+1)}(x_t, u_t) = Q^{(k)}(x_t, u_t) + \alpha \left( r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t) \right)",
            font_size=26,
        )
        final_group = VGroup(final_label, final_eq).arrange(DOWN, buff=0.3)
        final_group.next_to(boot_box, DOWN, buff=0.5)

        final_box = RoundedRectangle(
            corner_radius=0.2,
            width=final_group.width + 0.8,
            height=final_group.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        final_box.move_to(final_group)

        self.play(FadeIn(final_box), FadeIn(final_group))
        self.wait(0.5)
        self.next_slide()

        # Clear bootstrapping section
        self.play(
            FadeOut(boot_box),
            FadeOut(boot_group),
            FadeOut(final_box),
            FadeOut(final_group),
        )
        self.wait(0.3)

        # === ERROR TD ===
        td_label = Text("Error TD (Temporal Difference)", font_size=32, color=BLUE)
        td_label.next_to(title, DOWN, buff=0.5)

        td_eq = MathTex(
            r"\delta_t = r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t)",
            font_size=30,
        )
        td_desc = Text(
            "Mide la discrepancia entre la estimacion actual y la observacion",
            font_size=22,
            color=GRAY_B,
        )

        td_group = VGroup(td_label, td_eq, td_desc).arrange(DOWN, buff=0.3)
        td_group.next_to(title, DOWN, buff=0.5)

        td_box = RoundedRectangle(
            corner_radius=0.2,
            width=td_group.width + 0.8,
            height=td_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        td_box.move_to(td_group)

        self.play(FadeIn(td_box), FadeIn(td_group))
        self.wait(0.5)
        self.next_slide()

        # Expected TD error = 0
        td_exp_label = Text("Cuando Q^(k) aproxima Q*:", font_size=22, color=GRAY_B)
        td_exp_eq = MathTex(
            r"\mathbb{E}[\delta_t \mid X_t = x, U_t = u] = \mathbb{E}[R_{t+1} + \gamma \max_{u'} Q_*(X_{t+1}, u') \mid x, u] - Q_*(x, u) = 0",
            font_size=24,
        )
        td_exp_group = VGroup(td_exp_label, td_exp_eq).arrange(DOWN, buff=0.2)
        td_exp_group.next_to(td_box, DOWN, buff=0.4)

        td_exp_box = RoundedRectangle(
            corner_radius=0.2,
            width=td_exp_group.width + 0.8,
            height=td_exp_group.height + 0.5,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=1,
        )
        td_exp_box.move_to(td_exp_group)

        self.play(FadeIn(td_exp_box), FadeIn(td_exp_group))
        self.wait(0.5)
        self.next_slide()

        # Clear TD section
        self.play(
            FadeOut(td_box),
            FadeOut(td_group),
            FadeOut(td_exp_box),
            FadeOut(td_exp_group),
        )
        self.wait(0.3)

        # === EXPLORACION VS EXPLOTACION ===
        expl_title = Text("Exploracion vs Explotacion", font_size=32, color=BLUE)
        expl_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(expl_title))
        self.wait(0.3)

        # Exploitation side
        exploit_label = Text("Explotacion", font_size=26, color=GREEN)
        exploit_items = VGroup(
            Text("Usar la mejor politica", font_size=20, color=WHITE),
            Text("disponible para maximizar", font_size=20, color=WHITE),
            Text("la recompensa", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        exploit_group = VGroup(exploit_label, exploit_items).arrange(DOWN, buff=0.2)
        exploit_group.move_to(LEFT * 3 + DOWN * 0.5)

        exploit_box = RoundedRectangle(
            corner_radius=0.2,
            width=exploit_group.width + 0.6,
            height=exploit_group.height + 0.5,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=1,
        )
        exploit_box.move_to(exploit_group)

        # Exploration side
        explore_label = Text("Exploracion", font_size=26, color=ORANGE)
        explore_items = VGroup(
            Text("Probar acciones menos", font_size=20, color=WHITE),
            Text("conocidas para descubrir", font_size=20, color=WHITE),
            Text("mejores estrategias", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        explore_group = VGroup(explore_label, explore_items).arrange(DOWN, buff=0.2)
        explore_group.move_to(RIGHT * 3 + DOWN * 0.5)

        explore_box = RoundedRectangle(
            corner_radius=0.2,
            width=explore_group.width + 0.6,
            height=explore_group.height + 0.5,
            color=ORANGE,
            fill_opacity=0.1,
            stroke_width=1,
        )
        explore_box.move_to(explore_group)

        self.play(
            FadeIn(exploit_box), FadeIn(exploit_group),
            FadeIn(explore_box), FadeIn(explore_group),
        )
        self.wait(0.5)
        self.next_slide()

        # Epsilon-greedy policy
        eps_label = Text("Politica epsilon-greedy", font_size=24, color=YELLOW)
        eps_eq = MathTex(
            r"\pi_{\epsilon}(u \mid x) = \begin{cases} \arg\max_{u'} Q^{(k)}(x, u') & \text{con prob. } 1 - \epsilon \\ u \in \mathcal{U}(x) & \text{con prob. } \epsilon \end{cases}",
            font_size=26,
        )
        eps_group = VGroup(eps_label, eps_eq).arrange(DOWN, buff=0.2)
        eps_group.next_to(explore_box, DOWN, buff=0.5).move_to(DOWN * 2.5)

        eps_box = RoundedRectangle(
            corner_radius=0.2,
            width=eps_group.width + 0.8,
            height=eps_group.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        eps_box.move_to(eps_group)

        self.play(FadeIn(eps_box), FadeIn(eps_group))
        self.wait(0.5)
        self.next_slide()

        # GLIE note
        glie_note = Text(
            "GLIE: epsilon se reduce gradualmente para garantizar convergencia",
            font_size=20,
            color=GRAY_B,
        )
        glie_note.next_to(eps_box, DOWN, buff=0.2)
        self.play(FadeIn(glie_note))
        self.wait(0.5)
        self.next_slide()

        # Clear exploration section
        self.play(
            FadeOut(expl_title),
            FadeOut(exploit_box),
            FadeOut(exploit_group),
            FadeOut(explore_box),
            FadeOut(explore_group),
            FadeOut(eps_box),
            FadeOut(eps_group),
            FadeOut(glie_note),
        )
        self.wait(0.3)

        # === ALGORITMO Q-LEARNING ===
        algo_title = Text("Algoritmo Q-learning", font_size=32, color=BLUE)
        algo_title.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(algo_title))
        self.wait(0.3)

        # Algorithm inputs
        algo_inputs = MathTex(
            r"\alpha \in (0,1], \quad \gamma \in [0,1), \quad \epsilon_0 \in (0,1), \quad K \text{ episodios}",
            font_size=24,
        )
        algo_inputs.next_to(algo_title, DOWN, buff=0.3)
        self.play(FadeIn(algo_inputs))
        self.wait(0.3)

        # Algorithm steps as pseudo-code
        step_fs = 18
        steps = VGroup(
            Text("1. Inicializar Q(x, u) = 0 para todo (x, u)", font_size=step_fs),
            Text("2. Para cada episodio k = 1, ..., K:", font_size=step_fs),
            Text("   a. Definir epsilon_k con decaimiento", font_size=step_fs, color=GRAY_B),
            Text("   b. Inicializar estado x_1", font_size=step_fs, color=GRAY_B),
            Text("   c. Mientras x_t no sea terminal:", font_size=step_fs, color=GRAY_B),
            Text("      - Muestrear u_t ~ pi_epsilon(.|x_t)", font_size=step_fs, color=GRAY_B),
            Text("      - Ejecutar u_t, observar r_{t+1} y x_{t+1}", font_size=step_fs, color=GRAY_B),
            MathTex(
                r"\delta_t = r_{t+1} + \gamma \max_{u'} Q^{(k)}(x_{t+1}, u') - Q^{(k)}(x_t, u_t)",
                font_size=22,
                color=YELLOW,
            ),
            MathTex(
                r"Q^{(k+1)}(x_t, u_t) = Q^{(k)}(x_t, u_t) + \alpha \cdot \delta_t",
                font_size=22,
                color=YELLOW,
            ),
            MathTex(
                r"\mu(x) = \arg\max_u Q^{(K)}(x, u) \quad \forall x",
                font_size=22,
                color=GREEN,
            ),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        steps.next_to(algo_inputs, DOWN, buff=0.3)

        algo_box = RoundedRectangle(
            corner_radius=0.2,
            width=steps.width + 0.8,
            height=steps.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        algo_box.move_to(steps)

        self.play(FadeIn(algo_box), FadeIn(steps))
        self.wait(0.5)
        self.next_slide()

        # Clear algorithm section
        self.play(
            FadeOut(algo_title),
            FadeOut(algo_inputs),
            FadeOut(algo_box),
            FadeOut(steps),
        )
        self.wait(0.3)

        # === EJEMPLO: TICTACTOE ===
        ttt_title = Text("Ejemplo: TicTacToe", font_size=32, color=BLUE)
        ttt_title.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(ttt_title))
        self.wait(0.3)

        ttt_desc = Text(
            "Tablero 3x3. El agente (X) aprende contra oponente aleatorio.",
            font_size=22,
            color=GRAY_B,
        )
        ttt_desc.next_to(ttt_title, DOWN, buff=0.3)
        self.play(FadeIn(ttt_desc))
        self.wait(0.5)
        self.next_slide()

        # --- Build the board ---
        cell_size = 0.8
        board_cells = VGroup()
        cell_map = {}
        for row in range(3):
            for col in range(3):
                sq = Square(side_length=cell_size, color=WHITE, stroke_width=2)
                sq.move_to(
                    LEFT * 3
                    + UP * (1 - row) * cell_size
                    + RIGHT * col * cell_size
                )
                board_cells.add(sq)
                cell_map[(row, col)] = sq

        board_label = Text("Tablero (estado x_t)", font_size=18, color=GRAY_B)
        board_label.next_to(board_cells, DOWN, buff=0.3)

        # --- Build the Q-table ---
        q_table_title = Text("Q-tabla", font_size=22, color=YELLOW)

        # Column headers
        header_casilla = Text("Casilla", font_size=16, color=GRAY_B)
        header_q = Text("Q(x, u)", font_size=16, color=GRAY_B)

        # We will show Q-values for available cells
        q_rows = VGroup()
        q_labels = []
        q_values = []
        positions = [(0, 0), (0, 1), (0, 2),
                     (1, 0), (1, 1), (1, 2),
                     (2, 0), (2, 1), (2, 2)]
        for pos in positions:
            lbl = Text(f"({pos[0]},{pos[1]})", font_size=16, color=WHITE)
            val = Text("0.00", font_size=16, color=WHITE)
            row_g = VGroup(lbl, val).arrange(RIGHT, buff=1.0)
            q_rows.add(row_g)
            q_labels.append(lbl)
            q_values.append(val)

        header_row = VGroup(header_casilla, header_q).arrange(RIGHT, buff=0.7)
        q_table_content = VGroup(header_row, *q_rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        q_table_group = VGroup(q_table_title, q_table_content).arrange(DOWN, buff=0.2)
        q_table_group.move_to(RIGHT * 3 + DOWN * 0.3)

        q_table_box = RoundedRectangle(
            corner_radius=0.2,
            width=q_table_group.width + 0.6,
            height=q_table_group.height + 0.4,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        q_table_box.move_to(q_table_group)

        self.play(
            FadeOut(ttt_desc),
            FadeIn(board_cells),
            FadeIn(board_label),
            FadeIn(q_table_box),
            FadeIn(q_table_group),
        )
        self.wait(0.5)
        self.next_slide()

        # --- Simulate a game with Q-table updates ---
        # Move sequence: X plays, O plays, X plays, X wins
        marks = []
        alpha = 0.3
        gamma_val = 0.9

        # Helper to update a Q-value text
        def make_new_val(idx, new_val_num, color=WHITE):
            new_t = Text(f"{new_val_num:.2f}", font_size=16, color=color)
            new_t.move_to(q_values[idx])
            return new_t

        # --- Move 1: X plays (1,1) center ---
        move1_label = Text("Turno 1: X juega (1,1)", font_size=20, color=GREEN)
        move1_label.next_to(board_cells, UP, buff=0.4)

        x_mark_1 = Text("X", font_size=28, color=GREEN, weight=BOLD)
        x_mark_1.move_to(cell_map[(1, 1)])
        marks.append(x_mark_1)

        highlight_1 = SurroundingRectangle(cell_map[(1, 1)], buff=0.05, color=YELLOW)

        self.play(FadeIn(move1_label), Create(highlight_1))
        self.play(FadeIn(x_mark_1))

        # Update Q(x, (1,1)) = 0 + alpha*(0 + gamma*0 - 0) = 0 -> small positive for illustration
        # We show a non-trivial update for pedagogic purposes
        new_val_4 = make_new_val(4, 0.10, GREEN)
        self.play(Transform(q_values[4], new_val_4))

        # Highlight Q-table row
        q_highlight_1 = SurroundingRectangle(q_rows[4], buff=0.05, color=YELLOW)
        self.play(Create(q_highlight_1))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(highlight_1), FadeOut(q_highlight_1), FadeOut(move1_label))
        self.wait(0.2)

        # --- Move 2: O plays (0,0) ---
        move2_label = Text("Turno 2: O juega (0,0)", font_size=20, color=RED)
        move2_label.next_to(board_cells, UP, buff=0.4)

        o_mark_1 = Text("O", font_size=28, color=RED, weight=BOLD)
        o_mark_1.move_to(cell_map[(0, 0)])
        marks.append(o_mark_1)

        self.play(FadeIn(move2_label), FadeIn(o_mark_1))

        # Mark (0,0) as unavailable in Q-table
        new_val_0 = Text("---", font_size=16, color=GRAY)
        new_val_0.move_to(q_values[0])
        self.play(Transform(q_values[0], new_val_0))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(move2_label))
        self.wait(0.2)

        # --- Move 3: X plays (0,2) ---
        move3_label = Text("Turno 3: X juega (0,2)", font_size=20, color=GREEN)
        move3_label.next_to(board_cells, UP, buff=0.4)

        x_mark_2 = Text("X", font_size=28, color=GREEN, weight=BOLD)
        x_mark_2.move_to(cell_map[(0, 2)])
        marks.append(x_mark_2)

        highlight_3 = SurroundingRectangle(cell_map[(0, 2)], buff=0.05, color=YELLOW)

        self.play(FadeIn(move3_label), Create(highlight_3))
        self.play(FadeIn(x_mark_2))

        # Update Q(x, (0,2))
        new_val_2 = make_new_val(2, 0.15, GREEN)
        self.play(Transform(q_values[2], new_val_2))

        q_highlight_3 = SurroundingRectangle(q_rows[2], buff=0.05, color=YELLOW)
        self.play(Create(q_highlight_3))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(highlight_3), FadeOut(q_highlight_3), FadeOut(move3_label))
        self.wait(0.2)

        # --- Move 4: O plays (2,0) ---
        move4_label = Text("Turno 4: O juega (2,0)", font_size=20, color=RED)
        move4_label.next_to(board_cells, UP, buff=0.4)

        o_mark_2 = Text("O", font_size=28, color=RED, weight=BOLD)
        o_mark_2.move_to(cell_map[(2, 0)])
        marks.append(o_mark_2)

        self.play(FadeIn(move4_label), FadeIn(o_mark_2))

        new_val_6 = Text("---", font_size=16, color=GRAY)
        new_val_6.move_to(q_values[6])
        self.play(Transform(q_values[6], new_val_6))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(move4_label))
        self.wait(0.2)

        # --- Move 5: X plays (2,2) -> X wins diagonal ---
        move5_label = Text("Turno 5: X juega (2,2) -> Victoria!", font_size=20, color=GREEN)
        move5_label.next_to(board_cells, UP, buff=0.4)

        x_mark_3 = Text("X", font_size=28, color=GREEN, weight=BOLD)
        x_mark_3.move_to(cell_map[(2, 2)])
        marks.append(x_mark_3)

        highlight_5 = SurroundingRectangle(cell_map[(2, 2)], buff=0.05, color=YELLOW)

        self.play(FadeIn(move5_label), Create(highlight_5))
        self.play(FadeIn(x_mark_3))

        # Win: r = +1, update Q-values for winning move
        new_val_8 = make_new_val(8, 0.30, GREEN)
        self.play(Transform(q_values[8], new_val_8))

        # Also update previous moves via propagation
        new_val_2_up = make_new_val(2, 0.24, GREEN)
        new_val_4_up = make_new_val(4, 0.22, GREEN)
        self.play(
            Transform(q_values[2], new_val_2_up),
            Transform(q_values[4], new_val_4_up),
        )

        # Highlight winning diagonal
        diag_line = Line(
            cell_map[(0, 2)].get_center() + UL * 0.2,
            cell_map[(2, 0)].get_center() + DR * 0.2,
            color=GREEN,
            stroke_width=4,
        )
        # Correct diagonal: (0,0) to (2,2) but X is at (1,1), (0,2), (2,2) — that's anti-diagonal
        # Actually X is at (1,1), (0,2), (2,2) which is not a line. Let me fix:
        # (0,2), (1,1), (2,0) is anti-diagonal but (2,0) is O. X has (1,1),(0,2),(2,2).
        # Let's just highlight the winning cells
        win_highlights = VGroup(
            SurroundingRectangle(cell_map[(0, 2)], buff=0.05, color=GREEN, stroke_width=3),
            SurroundingRectangle(cell_map[(1, 1)], buff=0.05, color=GREEN, stroke_width=3),
            SurroundingRectangle(cell_map[(2, 2)], buff=0.05, color=GREEN, stroke_width=3),
        )

        # Draw the diagonal line from (0,2) through (1,1) to (2,2)
        diag_line = Line(
            cell_map[(0, 2)].get_center(),
            cell_map[(2, 2)].get_center(),
            color=GREEN,
            stroke_width=4,
        )

        self.play(Create(win_highlights), FadeOut(highlight_5))
        self.wait(0.5)
        self.next_slide()

        # Reward summary
        reward_text = VGroup(
            Text("r = +1 (ganar), r = -1 (perder), r = 0 (continuar)", font_size=18, color=GRAY_B),
            MathTex(
                r"Q^{(k+1)}(x_t, u_t) = Q^{(k)}(x_t, u_t) + \alpha \cdot \delta_t",
                font_size=24,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.2)
        reward_text.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(reward_text))
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)
