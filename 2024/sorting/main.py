from manim import *
from typing import List


class SortingScene(Scene):

    def create_vector(self, vector: List[int]) -> VGroup:
        vec_group = VGroup()
        for value in vector:
            square = Square().scale(0.4)
            value_text = Text(str(value)).move_to(square.get_center())
            group = VGroup(square, value_text)
            vec_group.add(group)
        vec_group.arrange(RIGHT, buff=0.1)
        return vec_group

    def construct(self):
        # Constants
        watermark_username = "@yan.rodriguescs"
        scene_title = "Ordenação de vetores"
        notation_str = r"A = \langle a_{1}, a_{2}, \dots, a_{n} \rangle"
        solution_str = r"A^{'} = \langle a^{'}_{1}, a^{'}_{2}, \dots, a^{'}_{n} \rangle"
        solution_idx_str = r"a^{'}_{1} \leq a^{'}_{2} \leq \dots \leq a^{'}_{n}"
        algorithm_title = "Insertion-Sort"

        # Create text objects
        watermark = Text(watermark_username, font_size=12).move_to([0, 6.5, 0])
        sorting_problem_text = Text(scene_title).move_to([0, 0, 0])
        algorithm_text = Text(algorithm_title).move_to([0, 5, 0])
        notation_tex = MathTex(notation_str)
        solution_tex = MathTex(solution_str, color="RED")
        solution_idx_tex = MathTex(solution_idx_str, color="RED").next_to(
            solution_tex, DOWN
        )

        # Animations
        self.play(Write(watermark), Write(sorting_problem_text))
        self.play(sorting_problem_text.animate.move_to([0, 5, 0]))
        self.play(Write(notation_tex.move_to([0, 0, 0]), run_time=1.5))
        self.pause(2.3)
        self.play(
            ReplacementTransform(notation_tex, solution_tex),
        )
        self.play(Write(solution_idx_tex))
        self.wait(2.2)

        self.play(Unwrite(solution_tex), Unwrite(solution_idx_tex))

        # Create a vector with 6 positions
        vector_values = [5, 2, 4, 6, 1, 3]

        vec_group = VGroup()
        boxes_group = [Square().scale(0.4) for i in vector_values]
        text_group = [Text(str(value)) for value in vector_values]

        for idx in range(len(vector_values)):
            group = VGroup(boxes_group[idx], text_group[idx])
            vec_group.add(group)

        vec_group.arrange(RIGHT, buff=0)

        self.play(
            ReplacementTransform(sorting_problem_text, algorithm_text),
            Create(vec_group),
        )

        # Create a pointer
        pointer = (
            Triangle(color=BLUE)
            .set_fill(BLUE, opacity=1)
            .scale(0.2)
            .next_to(vec_group[1], DOWN)
        )
        self.play(Create(pointer))

        # Insertion Sort Animation
        for i in range(1, len(vector_values)):
            current_value = vector_values[i]
            position = i

            # Move pointer to the current element
            self.play(pointer.animate.next_to(vec_group[position], DOWN))
            self.wait(1)

            while position > 0 and vector_values[position - 1] > current_value:
                # Swap the elements visually
                vector_values[position], vector_values[position - 1] = (
                    vector_values[position - 1],
                    vector_values[position],
                )

                # Animate the movement
                self.play(
                    vec_group[position].animate.move_to(
                        vec_group[position - 1].get_center()
                    ),
                    vec_group[position - 1].animate.move_to(
                        vec_group[position].get_center()
                    ),
                    pointer.animate.next_to(vec_group[position - 1], DOWN),
                    run_time=1.2,
                )

                # Swap elements in the visual vector
                vec_group[position], vec_group[position - 1] = (
                    vec_group[position - 1],
                    vec_group[position],
                )

                position -= 1

            # Update pointer
            self.wait(0.2)

        self.play(vec_group.animate.set_color(RED), pointer.animate.set_color(RED))

        self.play(Uncreate(vec_group), Uncreate(pointer))

        code = """
        from typing import List

        def insertion_sort(
            vetor: List[int]
        ):
            n = len(vetor)

            for i in range(1, n):
                chave = vetor[i]
                j = i - 1

                while j >= 0 and chave < vetor[j]:
                    vetor[j + 1] = vetor[j]
                    j = j - 1

                vetor[j + 1] = chave
        """
        rendered_code = Code(
            code=code,
            tab_width=4,
            font_size=19,
            background_stroke_color=BLACK,
            language="Python",
            font="Monospace",
        )

        self.play(Write(rendered_code.move_to([0, 0, 0])))

        self.wait(7.5)
