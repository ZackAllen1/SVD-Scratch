from manim import *
import numpy as np


def rgb_to_hex(rgb):  # used in Intro(Scene) -> Sample Animation 2
    return str('#%02x%02x%02x' % rgb)


class CreateCircle(Scene):  # test scene
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class TitleSlide(Scene):
    def construct(self):
        a = MarkupText(
            f'<span fgcolor="{BLUE}">S</span>ingular <span fgcolor="{BLUE}">V</span>alue '
            f'<span fgcolor="{BLUE}">D</span>ecomposition\nfrom Scratch',
            color=WHITE,
            font_size=45
        )
        b = Text("By: Zachary Allen",
                 line_spacing=1, font_size=40)
        self.add(Group(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(LEFT*2).shift(UP*1.5))

        border = ScreenRectangle(height=8, color=BLUE, stroke_width=10)
        self.play(Create(border, run_time=5))
        self.wait(0.5)
        self.play(FadeOut(border, run_time=1.5))


class Intro(Scene):
    def construct(self):
        title = MarkupText(f'<span fgcolor="{BLUE}">Purpose and Structure</span>',
                           font_size=50)
        self.add(Group(title).shift(LEFT*3).shift(UP*3))
        b1 = Text("1. Conceptually and Mathematically describe SVD", font_size=30)
        b1.shift(RIGHT*3)
        b2 = Text("How? From the ground up, using proof of concept visuals (manim)\n to create intuition", font_size=30)
        b2.shift(RIGHT * 3)
        list_group = VGroup(b1, b2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*0.5).shift(UP)
        self.add(list_group)

        # sample animation 1, left side, graph w/ unit vectors
        grid = NumberPlane(x_range=(-4,4,1), y_range=(-4,4,1), x_length=2, y_length=2)
        grid.shift(np.array([-3,-1.5,0]))
        vec1 = Arrow(start=grid.coords_to_point(0, 0), end=grid.coords_to_point(2, 0, 0),
                     buff=0, color=RED)
        vec2 = Arrow(start=grid.coords_to_point(0, 0, 0), end=grid.coords_to_point(0, 2, 0),
                     buff=0, color=YELLOW)
        group1 = VGroup(grid, vec1, vec2)
        self.play(FadeIn(group1, run_time=2))

        # SAMPLE ANIMATION 1: linear transformation applied to left side
        grid2 = NumberPlane(x_range=(-4, 4, 1), y_range=(-4, 4, 1), x_length=2, y_length=2)
        grid2.apply_matrix([[1, -1],[0.25, -1]])
        grid2.shift(np.array([3, -1.5, 0]))
        direction = Arrow(start=[-1, -1.5, 0], end=[1, -1.5, 0], color=GOLD, stroke_width=2)
        vec3 = Arrow(start=grid2.coords_to_point(0, 0, 0), end=grid2.coords_to_point(2, 0, 0),
                     buff=0, color=RED)
        vec4 = Arrow(start=grid2.coords_to_point(0, 0, 0), end=grid2.coords_to_point(0, 2, 0),
                     buff=0, color=YELLOW)
        group2 = VGroup(direction, grid2, vec3, vec4)
        self.play(TransformFromCopy(group1, group2, run_time=3))
        self.wait(2)
        self.play(FadeOut(group1, group2, run_time=2))

        # SAMPLE ANIMATION 2: sliding pixel value from 0-255
        number_line = NumberLine(x_range=(0, 255), length=5, include_ticks=False).shift(np.array([0, -2, 0]))
        dot = Dot().move_to(number_line.get_left()).set_color(BLUE)
        rect = Rectangle(height=1.5, width=1.5).shift(DOWN)
        var = Variable(0, label="test", var_type=Integer)
        title = Tex("Pixel Value").next_to(number_line, DOWN)
        left_label = Tex("0").next_to(number_line, LEFT)
        right_label = Tex("255").next_to(number_line, RIGHT)

        # convert 0-255 variable to rgb, set it as fill on rectangle
        rect.add_updater(lambda o: o.set_fill(color=rgb_to_hex((int(var.tracker.get_value()),
                                                                int(var.tracker.get_value()),
                                                                int(var.tracker.get_value()))), opacity=1))
        # add graphic
        self.play(FadeIn(number_line, dot, rect, left_label, right_label, title))

        # change variable from 0 to 255 then 255 to 0, move dot correspondingly
        self.play(var.tracker.animate.set_value(255), MoveAlongPath(dot, number_line),
                  run_time=6,
                  rate_func=rate_functions.there_and_back_with_pause)

        # remove graphic
        self.play(FadeOut(number_line, dot, rect, left_label, right_label, title), run_time=2)


class Structure(Scene):
    def construct(self):
        title = MarkupText(f'<span fgcolor="{BLUE}">Purpose and Structure</span>',
                           font_size=50)
        self.add(Group(title).shift(LEFT * 3).shift(UP * 3))

        part1 = MarkupText(f'<span fgcolor="{RED}">Part 1 - Netflix and Matrix Properties</span>\n'
                           f'<span size="x-small">\t- Case Study, establish prereqs for SVD</span>')
        part2 = MarkupText(f'<span fgcolor="{GREEN}">Part 2 - SVD from Zero</span>\n'
                           f'<span size="x-small">\t- Using prereqs, derive/explain SVD</span>')
        part3 = MarkupText(f'<span fgcolor="{BLUE}">Part 3 - Applications of SVD</span>\n'
                           f'<span size="x-small">\t- Image Compression, PCA, Jupyter Notebooks</span>')
        list_group = VGroup(part1, part2, part3).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        list_group.shift(LEFT * 0.5).shift(DOWN*0.25)
        self.add(list_group)


class Netflix(Scene):
    def construct(self):
        # initial table
        t0 = Table(
            [["72", "88", "65", "...", "46"],
             ["0", "37",  "92", "...", "50"],
             ["23", "25", "70", "...", "57"],
             ["...", "...", "...", "...", "..."],
             ["92", "97", "0", "...", "53"]],
            row_labels=[Text("Batman"), Text("The Emoji Movie"), Text("Star Wars"), Tex(r"$\vdots$"), Text("No Way Home")],
            col_labels=[Text("Adam"), Text("Jake"), Text("Jane"), Tex(r"$\hdots$"), Text("Mary")],
            top_left_entry=Text("Netflix Database").set_color(RED),
            include_outer_lines=True).scale(0.25)

        # add side labels
        row_side = Tex(r"Movies", font_size=25)
        m = Tex(r"(m)", font_size=25)
        col_side = Tex(r"People (n)", font_size=25)

        self.play(FadeIn(t0.shift(np.array([-3, 2, 0])),
                         Group(row_side, m).arrange(DOWN).next_to(t0, LEFT),
                         col_side.next_to(t0, UP))
                  )
        self.wait(2)

        # highlight cell red at (3,2)
        important_cell = t0.get_highlighted_cell((3,2), color=RED)
        t0.add_to_back(important_cell)

        # first question/answer group
        question = Tex(r'Can we make a prediction for this cell?', font_size=25, color=RED)
        answer = Tex(r"Given Jake's similar scores to Adam \\ we could predict $\approx 35$\%",
                     font_size=25)
        qa_group = VGroup(question, answer).arrange(DOWN, aligned_edge=LEFT).next_to(t0, RIGHT).shift(np.array([0.5, 1, 0]))

        # animate question and red cell
        self.play(FadeIn(important_cell),
                  Write(qa_group[0]))

        # add yellow boxes to Adam and Jake columns
        box1 = SurroundingRectangle(t0.get_columns()[1])
        box2 = SurroundingRectangle(t0.get_columns()[2])
        self.wait(3)
        self.play(FadeIn(box1, box2))

        # new table with replaced value at (3,2) -> 35, cell is green
        t1 = Table(
            [["72", "88", "65", "...", "46"],
             ["35", "37",  "92", "...", "50"],
             ["23", "25", "70", "...", "57"],
             ["...", "...", "...", "...", "..."],
             ["92", "97", "0", "...", "53"]],
            row_labels=[Text("Batman"), Text("The Emoji Movie"), Text("Star Wars"), Tex(r"$\vdots$"), Text("No Way Home")],
            col_labels=[Text("Adam"), Text("Jake"), Text("Jane"), Tex(r"$\hdots$"), Text("Mary")],
            top_left_entry=Text("Netflix Database").set_color(RED),
            include_outer_lines=True).scale(0.25)
        t1.add_highlighted_cell((3, 2), color=GREEN)

        # remove yellow boxes, add answer, transform t0 -> t1
        self.wait(3)
        self.play(FadeOut(box1, box2))
        self.wait(1)
        self.play(FadeIn(qa_group[1]),
                  ReplacementTransform(t0, t1.shift(np.array([-3, 2, 0])))
                  )

        # second question/answer group
        question2 = Tex(r'Does this method always work?', font_size=25, color=RED)\
            .next_to(answer, DOWN).shift(LEFT*0.5)
        answer2 = Tex(r'Some things to consider:', font_size=25)
        answer2_a = MathTex(r'1. \>\> m \ll n', font_size=25)
        answer2_b = Tex(r'2. Real world matrix is sparse (mostly zeros)', font_size=25)
        answer2_b1 = Tex(r'Why?', font_size=25)
        qa_group2 = VGroup(question2, answer2, answer2_a, answer2_b, answer2_b1)\
            .arrange(DOWN, aligned_edge=LEFT).next_to(t1, RIGHT).shift(np.array([0.5, -1, 0]))

        # animate second question/answer group
        self.wait(2)
        self.play(Write(qa_group2[0]))
        self.play(FadeIn(qa_group2[1],
                         qa_group2[2].shift(RIGHT*0.25),
                         qa_group2[3].shift(RIGHT * 0.25),
                         qa_group2[4].shift(RIGHT * 0.5)))

        # how we will tackle netflix problem
        netflix_result = Text("Netflix Prize Spoiler: solving sparse case is beyond scope of lecture,"
                              " however, we\n "
                              "will learn methods to solve the dense case which were used in winning team's solution.",
                              t2c={'[0:21]': RED}, font_size=25, disable_ligatures=True)
        netflix_result.next_to(t1, DOWN).shift(np.array([3, -2, 0]))
        self.wait(2)
        self.play(FadeIn(netflix_result,
                         SurroundingRectangle(netflix_result, color=RED)))


class MatrixIntro(Scene):
    def construct(self):
        statement = Tex(r"Consider the general matrix ", r"$A \in \mathbb{R}^{m \times n}$",
                        r", a vector ", r"$x \in \mathbb{R}^n$",
                        r", and vector ", r"$b \in \mathbb{R}^m$", font_size=30).shift(np.array([-1.5, 3, 0]))
        statement[1][:].set_color(RED)
        statement[5][:].set_color(BLUE)

        a = Tex("A = ", font_size=30, color=RED).next_to(statement[0], DOWN, buff=0.75)
        m0 = MobjectMatrix([[MathTex("a_{11}"), MathTex("\hdots"), MathTex("a_{1n}")],
                            [MathTex("\\vdots"), MathTex("\ddots"), MathTex("\\vdots")],
                            [MathTex("a_{m1}"), MathTex("\hdots"), MathTex("a_{mn}")]]).scale(0.5).next_to(a, RIGHT)
        a_group = VGroup(a, m0).shift(np.array([0, -0.5, 0]))
        self.play(Write(statement[0:2]),
                  FadeIn(a_group))

        x = Tex("x = ", font_size=30)
        x0 = MobjectMatrix([[MathTex("x_1")],
                            [MathTex("x_2")],
                            [MathTex("\\vdots")],
                            [MathTex("x_n")]]).scale(0.5).next_to(x, RIGHT)
        x_group = VGroup(x, x0).next_to(a_group, RIGHT).shift(RIGHT)
        self.play(Write(statement[2:4]),
                  FadeIn(x_group))

        b = Tex("b = ", color=BLUE, font_size=30)
        b0 = MobjectMatrix([[MathTex("b_1")],
                            [MathTex("b_2")],
                            [MathTex("\\vdots")],
                            [MathTex("b_m")]]).scale(0.5).next_to(b, RIGHT)
        b_group = VGroup(b, b0).next_to(x_group, RIGHT).shift(RIGHT)
        self.play(Write(statement[4:]),
                  FadeIn(b_group))

        top_group = VGroup(statement, a_group, x_group, b_group)
