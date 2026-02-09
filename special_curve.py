from src.shapes import ImplicitFunction
from src.base import BaseScene, Color
import numpy as np


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Special Curve Scene")
        self.background = Color(1, 0.5, 0.31)

        def special_curve(point):
            x, y = point
            # Matriz de rotação [[cos(@), -sin(@)], [sin(@), cos(@)]]
            x, y = x * np.cos(np.pi) + y * np.sin(np.pi), -x * np.sin(
                np.pi
            ) + y * np.cos(np.pi)
            return (
                0.004
                + 0.110 * x
                - 0.177 * y
                - 0.174 * (x**2)
                + 0.224 * x * y
                - 0.303 * (y**2)
                - 0.168 * (x**3)
                + 0.327 * (x**2) * y
                - 0.087 * x * (y**2)
                - 0.013 * (y**3)
                + 0.235 * (x**4)
                - 0.667 * (x**3) * y
                + 0.745 * (x**2) * (y**2)
                - 0.029 * x * (y**3)
                + 0.072 * (y**4)
            )

        self.add(ImplicitFunction(special_curve), Color(0.8, 0, 0.9))
