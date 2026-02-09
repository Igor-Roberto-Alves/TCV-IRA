import numpy as np


def In_out(V: list, p) -> bool:
    """
    Verifica se p está dentro do triângulo V usando Coordenadas Baricêntricas
    (Método do Produto Interno).
    """
    A, B, C = np.array(V[0]), np.array(V[1]), np.array(V[2])
    P = np.array(p)

    # 1. Vetores
    v0 = C - A
    v1 = B - A
    v2 = P - A

    # 2. Produtos Internos (Dot Products)
    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)

    # 3. Calcular denominador (Determinante)
    invDenom = 1 / (dot00 * dot11 - dot01 * dot01)

    # 4. Calcular coordenadas baricêntricas (u, v)
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom

    # A terceira coordenada w é implícita: w = 1 - u - v
    # Para estar dentro: u >= 0, v >= 0 e (u + v) < 1
    return (u >= 0) and (v >= 0) and (u + v <= 1)


def alternative_in_out(V: list, p) -> bool:
    """
    Verifica se p está dentro via Fecho Convexo (Jarvis March).
    Se len(Hull) == 3 -> Dentro.
    Se len(Hull) == 4 -> Fora.
    """
    # Lista de todos os pontos: Vértices + Ponto de teste
    points = V + [p]

    # Função auxiliar para orientação (Produto vetorial 2D / Cross Product)
    # Retorna: 0 (colinear), 1 (horário), 2 (anti-horário)
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def convex_hull(pts):
        n = len(pts)
        if n < 3:
            return []

        hull = []

        # 1. Encontrar o ponto mais à esquerda
        l = 0
        for i in range(1, n):
            if pts[i][0] < pts[l][0]:
                l = i

        # 2. Jarvis March
        p_curr = l
        while True:
            hull.append(pts[p_curr])

            # Escolhe o próximo ponto q. Inicialmente supomos que é (p_curr + 1)
            q = (p_curr + 1) % n

            # Verifica se existe algum ponto 'i' que é mais "anti-horário" que 'q'
            for i in range(n):
                if orientation(pts[p_curr], pts[i], pts[q]) == 2:
                    q = i

            p_curr = q

            # Se voltamos ao início, terminamos
            if p_curr == l:
                break

        return hull

    # Executa o algoritmo
    hull_points = convex_hull(points)

    # Lógica de Classificação:
    # Se o ponto P estiver DENTRO, o fecho convexo será apenas o triângulo original (tamanho 3).
    # Se P estiver FORA, ele fará parte do fecho convexo (tamanho 4).
    return len(hull_points) == 3


# --- Testando ---
if __name__ == "__main__":
    # Triângulo (0,0), (4,0), (0,3)
    triangulo = [[0, 0], [4, 0], [0, 3]]

    p_dentro = [1, 0]
    p_fora = [5, 5]

    print(f"Ponto {p_dentro} (Esperado: True):")
    print(f"  Baricêntrica: {_In_out(triangulo, p_dentro)}")
    print(f"  Jarvis March: {alternative_in_out(triangulo, p_dentro)}")

    print(f"\nPonto {p_fora} (Esperado: False):")
    print(f"  Baricêntrica: {_In_out(triangulo, p_fora)}")
    print(f"  Jarvis March: {alternative_in_out(triangulo, p_fora)}")
