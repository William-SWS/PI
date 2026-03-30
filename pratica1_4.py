import cv2
import numpy as np
from collections import deque

# -------------------------
# Definir vizinhança
# -------------------------

def get_neighbors(x, y, connectivity):

    if connectivity == 4:
        return [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1)
        ]

    elif connectivity == 8:
        return [
            (x-1, y), (x+1, y),
            (x, y-1), (x, y+1),
            (x-1, y-1), (x-1, y+1),
            (x+1, y-1), (x+1, y+1)
        ]


# -------------------------
# Contar componentes
# -------------------------

def contar_componentes(img, connectivity):

    h, w = img.shape
    visitado = np.zeros((h, w), dtype=bool)

    componentes = 0

    for i in range(h):
        for j in range(w):

            if img[i, j] == 255 and not visitado[i, j]:

                componentes += 1
                fila = deque([(i, j)])
                visitado[i, j] = True

                while fila:

                    x, y = fila.popleft()

                    for nx, ny in get_neighbors(x, y, connectivity):

                        if 0 <= nx < h and 0 <= ny < w:

                            if img[nx, ny] == 255 and not visitado[nx, ny]:

                                visitado[nx, ny] = True
                                fila.append((nx, ny))

    return componentes


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread("bin.png", cv2.IMREAD_GRAYSCALE)

# garantir imagem binária
_, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# -------------------------
# Contagem
# -------------------------

c4 = contar_componentes(bin_img, 4)
c8 = contar_componentes(bin_img, 8)

print("Componentes com 4-conectividade:", c4)
print("Componentes com 8-conectividade:", c8)
