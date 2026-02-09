from src.base import BaseScene, Color
from src.shapes import Triangle


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Triangle Scene")
        self.background = Color(1, 1, 1)

        # Add some triangles to the scene
        self.add(
            Triangle((1.0, 1.0), (3.0, 1.0), (2.0, 3.0)), Color(1.0, 0.0, 0.0)
        )  # Red triangle
        self.add(
            Triangle(
                (5.0, 4.0), (3.0 + 0.005, 1.0 + 0.005), (2.0 + 0.005, 3.0 + 0.005)
            ),
            Color(0, 0, 1.0),
        )
