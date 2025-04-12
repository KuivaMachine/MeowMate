from manim import *

class LottieExample(Scene):
    def construct(self):
        lottie = LottieObject("animation.json")
        self.play(ShowCreation(lottie))
        self.wait(2)