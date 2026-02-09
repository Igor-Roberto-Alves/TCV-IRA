import math
from src.shapes import ImplicitFunction
from src.base import BaseScene, Color


class DynamicMandelbrotColor:

    def __init__(self, parent_shape):
        self.parent = parent_shape

    def _get_color_values(self):
        
        numerador = math.log(self.parent.last_iter)
        denominador = math.log(self.parent.max_iter)
        t = numerador / denominador

   
        val = t  

 
        r = 1.0 - val
        g = 1.0 - val
        b = 1.0 - (0.5)*val

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
        super().__init__("Mandelbrot")
        self.background = Color(0, 0, 0)

        # Aumentei para 200 iterações para o gradiente ficar mais suave na borda
        self.max_iter = 200
        self.last_iter = 0

        def mandelbrot_check(p):
            x, y = p
            c = complex(x, y)
            z = 0

            for i in range(self.max_iter):
                z = z**2 + c
                if abs(z) > 2 * (10**10): # A escolha desse número foi arbitrária para aumentar o Range de iterações 
                    self.last_iter = i
                    return -1.0

            self.last_iter = self.max_iter
            return 1.0

        mandelbrot_shape = ImplicitFunction(mandelbrot_check)
        dynamic_color = DynamicMandelbrotColor(self) # Para colorir a partir das iterações

        self.add(mandelbrot_shape, dynamic_color)
