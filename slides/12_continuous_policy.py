"""
Continuous Policy slide - From discrete MDP to continuous control.

Introduces the stochastic policy as a multivariate normal distribution
and shows the neural network architecture for the mean function.

Example:
    uv run manim-slides render slides/12_continuous_policy.py ContinuousPolicySlide
"""

from manim import *
from manim_slides import Slide


class ContinuousPolicySlide(Slide):
    """Transition from discrete to continuous policy with neural network diagram."""

    def construct(self):
        # === TITLE ===
        title = Text("Política para control continuo", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === DISCRETE POLICY (recap) ===
        discrete_label = Text("MDP discreto y finito", font_size=26, color=GRAY_B)
        discrete_eq = MathTex(
            r"\pi(u|x) = \mathbb{P}[U_t = u \,|\, X_t = x]",
            font_size=32,
        )
        discrete_spaces = MathTex(
            r"u \in \mathcal{U}, \quad x \in \mathcal{X}",
            font_size=26,
            color=GRAY_B,
        )
        discrete_group = VGroup(discrete_label, discrete_eq, discrete_spaces).arrange(
            DOWN, buff=0.25
        )

        discrete_box = RoundedRectangle(
            corner_radius=0.2,
            width=discrete_group.width + 1.0,
            height=discrete_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        discrete_box.move_to(discrete_group)

        # === CONTINUOUS POLICY ===
        continuous_label = Text("Control continuo", font_size=26, color=BLUE)
        continuous_eq = MathTex(
            r"\pi(\mathbf{u}|\mathbf{x}) = p(\mathbf{u} \,|\, \mathbf{x})",
            font_size=32,
        )
        continuous_spaces = MathTex(
            r"\mathbf{u} \in \mathbb{R}^m, \quad \mathbf{x} \in \mathbb{R}^n",
            font_size=26,
            color=BLUE_C,
        )
        continuous_group = VGroup(
            continuous_label, continuous_eq, continuous_spaces
        ).arrange(DOWN, buff=0.25)

        continuous_box = RoundedRectangle(
            corner_radius=0.2,
            width=continuous_group.width + 1.0,
            height=continuous_group.height + 0.6,
            color=BLUE,
            fill_opacity=0.15,
            stroke_width=1,
        )
        continuous_box.move_to(continuous_group)

        # Stack both boxes: discrete upper half, continuous below it
        comparison_pair = VGroup(
            VGroup(discrete_box, discrete_group),
            VGroup(continuous_box, continuous_group),
        ).arrange(DOWN, buff=0.5)
        comparison_pair.move_to(UP * 0.6)

        # Reposition boxes to match group centers after arrange
        discrete_box.move_to(discrete_group.get_center())
        continuous_box.move_to(continuous_group.get_center())

        self.play(FadeIn(discrete_box), FadeIn(discrete_group))
        self.wait(0.5)
        self.next_slide()

        # Show continuous below discrete (both visible simultaneously)
        self.play(FadeIn(continuous_box), FadeIn(continuous_group))
        self.wait(0.5)
        self.next_slide()

        # === QUADCOPTER CONTEXT ===
        quad_note = MathTex(
            r"\text{Cuadric\'optero: } n = 12\ (\text{estado}),\ m = 4\ (\text{rotores})",
            font_size=22,
            color=YELLOW,
        )
        # Place below the comparison pair (continuous_box is the lower element)
        quad_note.next_to(
            VGroup(discrete_box, discrete_group, continuous_box, continuous_group),
            DOWN,
            buff=0.4,
        )

        self.play(FadeIn(quad_note))
        self.wait(0.5)
        self.next_slide()

        # Clear comparison section
        self.play(
            FadeOut(discrete_box),
            FadeOut(discrete_group),
            FadeOut(continuous_box),
            FadeOut(continuous_group),
            FadeOut(quad_note),
        )
        self.wait(0.3)

        # === STOCHASTIC POLICY AS MULTIVARIATE NORMAL ===
        policy_label = Text("Política estocástica parametrizada", font_size=26, color=BLUE)
        policy_eq = MathTex(
            r"\pi_{\boldsymbol{\theta}}(\mathbf{u}|\mathbf{x}) := \mathcal{N}\left(\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta}), \boldsymbol{\Sigma}(\mathbf{x})\right)",
            font_size=30,
        )
        policy_group = VGroup(policy_label, policy_eq).arrange(DOWN, buff=0.3)
        policy_group.move_to(UP * 1.5)

        policy_box = RoundedRectangle(
            corner_radius=0.2,
            width=policy_group.width + 0.8,
            height=policy_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        policy_box.move_to(policy_group)

        self.play(FadeIn(policy_box), FadeIn(policy_group))
        self.wait(0.5)
        self.next_slide()

        # === EXPLANATION OF COMPONENTS ===
        mu_explanation = MathTex(
            r"\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta})",
            r": \text{ media (acci\'on esperada)}",
            font_size=24,
        )
        mu_explanation[0].set_color(GREEN)

        sigma_explanation = MathTex(
            r"\boldsymbol{\Sigma}(\mathbf{x})",
            r": \text{ covarianza (exploraci\'on)}",
            font_size=24,
        )
        sigma_explanation[0].set_color(ORANGE)

        explanations = VGroup(mu_explanation, sigma_explanation).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        explanations.next_to(policy_box, DOWN, buff=0.45)

        self.play(FadeIn(explanations))
        self.wait(0.5)
        self.next_slide()

        # Clear stochastic policy section
        self.play(
            FadeOut(explanations),
            FadeOut(policy_box),
            FadeOut(policy_group),
        )
        self.wait(0.3)

        # === NEURAL NETWORK FOR MU ===
        nn_label = Text("Red neuronal completamente conectada", font_size=28, color=GREEN)
        nn_label.to_edge(UP, buff=0.6)

        mu_eq = MathTex(
            r"\boldsymbol{\mu}(\mathbf{x}; \boldsymbol{\theta}) = f_{\boldsymbol{\theta}}(\mathbf{x})",
            font_size=30,
        )
        mu_eq.next_to(nn_label, DOWN, buff=0.3)

        self.play(
            FadeOut(title),
            FadeIn(nn_label),
            FadeIn(mu_eq),
        )
        self.wait(0.5)
        self.next_slide()

        # === HORIZONTAL THREE-ZONE LAYOUT: theta_left | network_center | equations_right ===

        # --- CENTER ZONE: Neural network diagram ---
        layer_sizes = [4, 6, 6, 4]  # Input, hidden1, hidden2, output
        layer_colors = [BLUE, PURPLE, PURPLE, GREEN]
        layer_labels = [r"\mathbf{x}", "", "", r"\boldsymbol{\mu}"]
        neuron_radius = 0.13
        layer_spacing = 1.5
        neuron_spacing = 0.45

        layers = []
        all_neurons = VGroup()

        for i, (size, color) in enumerate(zip(layer_sizes, layer_colors)):
            layer = VGroup()
            for j in range(size):
                neuron = Circle(
                    radius=neuron_radius,
                    color=color,
                    fill_opacity=0.8,
                    stroke_width=2,
                )
                y_offset = (size - 1) / 2 * neuron_spacing
                neuron.move_to(
                    LEFT * (len(layer_sizes) - 1) / 2 * layer_spacing
                    + RIGHT * i * layer_spacing
                    + UP * (y_offset - j * neuron_spacing)
                )
                layer.add(neuron)
            layers.append(layer)
            all_neurons.add(layer)

        # Create connections between layers
        connections = VGroup()
        for i in range(len(layers) - 1):
            for neuron1 in layers[i]:
                for neuron2 in layers[i + 1]:
                    line = Line(
                        neuron1.get_center(),
                        neuron2.get_center(),
                        stroke_width=0.5,
                        color=GRAY,
                        stroke_opacity=0.4,
                    )
                    connections.add(line)

        # Network diagram group (neurons + connections together for positioning)
        network_diagram = VGroup(connections, all_neurons)

        # Layer labels (positioned relative to layers, added after network placed)
        input_label = MathTex(layer_labels[0], font_size=26, color=BLUE)
        output_label = MathTex(layer_labels[3], font_size=26, color=GREEN)
        hidden_label = Text("capas ocultas", font_size=16, color=GRAY_B)

        # --- LEFT ZONE: theta box ---
        theta_eq = MathTex(
            r"\boldsymbol{\theta} = \left(\mathbf{W}^{[\ell]}, \mathbf{b}^{[\ell]}\right)_{\ell=1}^{L} \in \Theta",
            font_size=22,
        )
        theta_desc = Text("pesos y sesgos por capa", font_size=18, color=GRAY_B)
        theta_group = VGroup(theta_eq, theta_desc).arrange(DOWN, buff=0.2)

        theta_box = RoundedRectangle(
            corner_radius=0.2,
            width=theta_group.width + 0.8,
            height=theta_group.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        theta_box.move_to(theta_group)
        theta_left = VGroup(theta_box, theta_group)

        # --- RIGHT ZONE: ANN equations ---
        ann_eq1 = MathTex(
            r"f_a(\mathbf{x}; \boldsymbol{\theta}) := \phi \circ T_L \circ \phi \circ T_{L-1} \circ \cdots \circ \phi \circ T_1(\mathbf{x})",
            font_size=22,
        )
        ann_eq2 = MathTex(
            r"T_{\ell}(\mathbf{z}) = \mathbf{W}^{[\ell]}\mathbf{z} + \mathbf{b}^{[\ell]}",
            font_size=22,
        )
        ann_eq3 = MathTex(
            r"\mathbf{W}^{[\ell]} \in \mathbb{R}^{n_{\ell} \times n_{\ell-1}}, \quad \mathbf{b}^{[\ell]} \in \mathbb{R}^{n_{\ell}}",
            font_size=20,
        )
        ann_eqs = VGroup(ann_eq1, ann_eq2, ann_eq3).arrange(DOWN, buff=0.3)

        ann_box = RoundedRectangle(
            corner_radius=0.2,
            width=ann_eqs.width + 0.6,
            height=ann_eqs.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        ann_box.move_to(ann_eqs)
        equations_right = VGroup(ann_box, ann_eqs)

        # --- Arrange three zones horizontally ---
        three_zone = VGroup(theta_left, network_diagram, equations_right).arrange(
            RIGHT, buff=0.5
        )
        three_zone.move_to(DOWN * 0.5)

        # Re-align boxes after arrange
        theta_box.move_to(theta_group.get_center())
        ann_box.move_to(ann_eqs.get_center())

        # Position neuron labels relative to layers (after network is placed)
        input_label.next_to(layers[0], DOWN, buff=0.25)
        output_label.next_to(layers[-1], DOWN, buff=0.25)
        hidden_label.next_to(VGroup(layers[1], layers[2]), UP, buff=0.25)

        # Animate neural network section
        self.play(Create(connections), run_time=1)
        self.play(FadeIn(all_neurons))
        self.wait(0.3)
        self.play(FadeIn(input_label), FadeIn(output_label), FadeIn(hidden_label))
        self.wait(0.3)
        self.play(FadeIn(theta_left), FadeIn(equations_right))
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)
