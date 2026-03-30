import cv2
import numpy as np
import os

# ============================
# CONFIGURAÇÃO
# ============================

imagem_path = "uece.jpg"
saida = "bit_planes"
os.makedirs(saida, exist_ok=True)

# Ler imagem em escala de cinza
img = cv2.imread(imagem_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise ValueError("Erro ao carregar a imagem!")

# ============================
# FATIAMENTO EM NÍVEL DE BITS
# ============================

# Vamos gerar 8 imagens (bit 0 até bit 7)
for k in range(8):

    # Criar imagem vazia
    bit_plane = np.zeros_like(img, dtype=np.uint8)

    # Percorrer cada pixel manualmente
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            r = img[i, j]

            # Extrair bit k:
            # 1. Shift para direita k posições
            # 2. AND com 1 para pegar apenas o bit
            b_k = (r >> k) & 1

            # Escalar para visualização (0 ou 255)
            bit_plane[i, j] = b_k * 255

    # Salvar imagem
    nome = f"bit_plane_{k}.png"
    cv2.imwrite(os.path.join(saida, nome), bit_plane)

print("Planos de bits gerados com sucesso!")
