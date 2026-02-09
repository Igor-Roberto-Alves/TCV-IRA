def det_triangle(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def In_out(V, P):
    A, B, C = V

    det_total = det_triangle(A, B, C)
    
    if det_total == 0: #Colineares
        return False

    det_u = det_triangle(P, B, C)
    

    det_v = det_triangle(A, P, C)

    u = det_u / det_total
    v = det_v / det_total


    return (u >= 0) and (v >= 0) and (1 - (v+u) >= 0)
