import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Função de quantização
# -------------------------

def quantizar(img, niveis):

    L = 256
    fator = L // niveis

    img_q = (img // fator) * fator

    return img_q

# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread("cat2.jpg")

# converter para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# níveis desejados
levels = [128,8,4,2]

images = []

for l in levels:
    images.append(quantizar(gray, l))

# -------------------------
# Mostrar imagens
# -------------------------

plt.figure(figsize=(12,4))

for l in levels:

    img_q = quantizar(gray, l)

    nome_arquivo = f"cat2_quantizada_{l}_niveis.png"

    cv2.imwrite(nome_arquivo, img_q)

    print(f"Imagem salva: {nome_arquivo}")
