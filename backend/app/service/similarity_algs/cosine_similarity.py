import numpy as np

def cosine_similarity(vec1, vec2) -> float:
    a = np.dot(vec1, vec2)
    b = np.linalg.norm(vec1) * np.linalg.norm(vec2)

    # не учитываем случай деления на ноль 
    if b == 0:
        return 0.0

    return float(a / b)

# np.linalg.norm()
# https://numpy.org/devdocs/reference/generated/numpy.linalg.vector_norm.html