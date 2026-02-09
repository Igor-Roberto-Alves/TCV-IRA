from src.base import BaseScene, Color
from src.shapes import Triangle


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Triangle of Triangles")
        # Fundo Branco (para destacar as cores)
        self.background = Color(1, 1, 1)

        # --- DEFINIÇÃO DA GEOMETRIA ---
        # Imagine um triângulo grande com vértices:
        # Topo: (4.0, 5.0)
        # Esquerda: (2.0, 1.0)
        # Direita: (6.0, 1.0)

        # Calculando os Pontos Médios (Midpoints):
        p_top = (4.0, 5.0)
        p_left = (2.0, 1.0)
        p_right = (6.0, 1.0)

        p_mid_left = (3.0, 3.0)  # Entre Topo e Esquerda
        p_mid_right = (5.0, 3.0)  # Entre Topo e Direita
        p_mid_bottom = (4.0, 1.0)  # Entre Esquerda e Direita

        # --- ADICIONANDO OS 4 TRIÂNGULOS ---

        # 1. Triângulo Superior (Vermelho)
        # Conecta: Topo, Meio-Esq, Meio-Dir
        self.add(Triangle(p_top, p_mid_left, p_mid_right), Color(1.0, 0.0, 0.0))

        # 2. Triângulo Inferior Esquerdo (Azul)
        # Conecta: Meio-Esq, Esquerda, Meio-Baixo
        self.add(Triangle(p_mid_left, p_left, p_mid_bottom), Color(0.0, 0.0, 1.0))

        # 3. Triângulo Inferior Direito (Verde)
        # Conecta: Meio-Dir, Meio-Baixo, Direita
        self.add(
            Triangle(p_mid_right, p_mid_bottom, p_right),
            Color(0.0, 1.0, 0.0),  # Verde puro
        )

        # 4. Triângulo Central Invertido (Amarelo)
        # Conecta os 3 pontos médios
        self.add(
            Triangle(p_mid_left, p_mid_right, p_mid_bottom),
            Color(1.0, 1.0, 0.0),  # Vermelho + Verde = Amarelo
        )
