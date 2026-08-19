from manim import *


class LagrangeLabScene(Scene):
    def construct(self):

        # Title
        title = Text("LagrangeLab: Lagrange Points", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Primary bodies
        body1 = Dot(LEFT * 2, radius=0.18)
        body2 = Dot(RIGHT * 2, radius=0.10)

        label1 = Text("Primary", font_size=20).next_to(body1, DOWN)
        label2 = Text("Secondary", font_size=20).next_to(body2, DOWN)

        self.play(
            FadeIn(body1),
            FadeIn(body2),
            Write(label1),
            Write(label2)
        )

        # Lagrange points
        points = {
            "L1": RIGHT * 0,
            "L2": RIGHT * 2.7,
            "L3": LEFT * 2.7,
            "L4": RIGHT * 0.0 + UP * 1.7,
            "L5": RIGHT * 0.0 + DOWN * 1.7,
        }

        dots = VGroup()
        labels = VGroup()

        for name, position in points.items():
            dot = Dot(position, radius=0.09)
            label = Text(name, font_size=20).next_to(dot, RIGHT, buff=0.12)

            dots.add(dot)
            labels.add(label)

        self.play(
            LaggedStart(
                *[FadeIn(dot) for dot in dots],
                lag_ratio=0.15
            )
        )

        self.play(
            LaggedStart(
                *[Write(label) for label in labels],
                lag_ratio=0.15
            )
        )

        # Highlight L1
        l1 = dots[0]

        self.play(
            l1.animate.scale(2.2),
            run_time=0.5
        )

        explanation = Text(
            "Five equilibrium regions in the rotating two-body system",
            font_size=22
        )
        explanation.to_edge(DOWN)

        self.play(Write(explanation))

        # Satellite motion
        satellite = Dot(points["L4"], radius=0.07)

        trajectory = VMobject()
        trajectory.set_points_as_corners([
            points["L4"],
            RIGHT * 0.8 + UP * 1.2,
            RIGHT * 1.1 + UP * 0.2,
            RIGHT * 0.5 + DOWN * 1.0,
            points["L5"],
        ])

        self.play(FadeIn(satellite))

        self.play(
            MoveAlongPath(
                satellite,
                trajectory,
                run_time=3,
                rate_func=linear
            )
        )

        self.wait(2)