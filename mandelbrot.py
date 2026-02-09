import math
from src.shapes import ImplicitFunction
from src.base import BaseScene, Color


class DynamicMandelbrotColor:
    def __init__(self, parent_shape):
        self.parent = parent_shape

    def _get_color_values(self):

        if self.parent.last_iter >= self.parent.max_iter:
            return 0.0, 0.0, 0.0

        numerador = math.log(1 + math.log(1 + self.parent.last_iter))
        denominador = math.log(1 + math.log(1 + self.parent.max_iter))
        t = numerador / denominador

        # 3. Inversão do Gradiente: Branco -> Azul Escuro

        # Queremos que t=0 (Longe) seja BRANCO (1, 1, 1)
        # Queremos que t=1 (Perto) seja AZUL ESCURO (0, 0, 0.5)

        # Matemática da interpolação:
        val = t  # O quão "perto" do conjunto estamos

        # Red e Green: Começam em 1.0 (Branco) e caem para 0.0 (Escuro)
        r = 1.0 - val
        g = 1.0 - val

        # Blue: Começa em 1.0 (Branco) e cai apenas até 0.5 (Azul Escuro)
        # Se caísse para 0, ficaria preto na borda, mas queremos azul.
        b = 1.0 - (0.5 * val)

        return r, g, b

    def __getattr__(self, name):
        r, g, b = self._get_color_values()
        if name == "r":
            return r
        if name == "g":
            return g
        if name == "b":
            return b
        return 0.0

    def __iter__(self):
        r, g, b = self._get_color_values()
        yield r
        yield g
        yield b

    def __getitem__(self, idx):
        return list(self)[idx]


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mandelbrot White to Blue")
        self.background = Color(1, 1, 1)

        # Aumentei para 200 iterações para o gradiente ficar mais suave na borda
        self.max_iter = 200
        self.last_iter = 0

        def mandelbrot_check(p):
            x, y = p
            c = complex(x, y)
            z = 0

            for i in range(self.max_iter):
                z = z**2 + c
                if abs(z) > 2 * (10**10):
                    self.last_iter = i
                    return -1.0

            self.last_iter = self.max_iter
            return -1.0

        mandelbrot_shape = ImplicitFunction(mandelbrot_check)
        dynamic_color = DynamicMandelbrotColor(self)

        self.add(mandelbrot_shape, dynamic_color)
