import cv2
import numpy as np
import os

# ============================
# CONFIGURAÇÃO INICIAL
# ============================

# Caminho da imagem de entrada
caminho_imagem = "uece.jpg"

# Criar pasta de saída
saida = "realces"
os.makedirs(saida, exist_ok=True)

# Ler imagem em escala de cinza
img = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

# Garantir que a imagem foi carregada
if img is None:
    raise ValueError("Erro ao carregar a imagem!")

# Converter para float para evitar problemas em operações matemáticas
img_float = img.astype(np.float32)

# ============================
# 1. NEGATIVO
# ============================
# Fórmula: s = L - 1 - r

L = 256  # níveis de cinza (0-255)

negativo = (L - 1) - img_float

# Converter para uint8
negativo = np.clip(negativo, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(saida, "negativo.jpg"), negativo)


# ============================
# 2. TRANSFORMAÇÃO LOGARÍTMICA
# ============================
# Fórmula: s = c * log(1 + r)

c = 255 / np.log(1 + np.max(img_float))

log_img = c * np.log(1 + img_float)

log_img = np.clip(log_img, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(saida, "logaritmica.jpg"), log_img)


# ============================
# 3. TRANSFORMAÇÃO EXPONENCIAL (GAMMA)
# ============================
# Fórmula: s = c * r^gamma

gamma = 2.0  # >1 escurece, <1 clareia
c = 255 / (np.max(img_float) ** gamma)

exp_img = c * (img_float ** gamma)

exp_img = np.clip(exp_img, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(saida, "exponencial.jpg"), exp_img)


# ============================
# 4. TRANSFORMAÇÃO LINEAR
# ============================
# Fórmula: s = a*r + b

a = 1.5  # contraste
b = 30   # brilho

linear = a * img_float + b

linear = np.clip(linear, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(saida, "linear.jpg"), linear)


# ============================
# 5. FATIAMENTO DE NÍVEL DE CINZA
# ============================
# Destaca uma faixa de intensidades

A = 100  # limite inferior
B = 180  # limite superior

fatiamento = np.zeros_like(img_float)

# Pixels dentro do intervalo recebem valor alto
fatiamento[(img_float >= A) & (img_float <= B)] = 255

# Fora do intervalo mantém valor original (opcional)
fatiamento[(img_float < A) | (img_float > B)] = img_float[(img_float < A) | (img_float > B)]

fatiamento = np.clip(fatiamento, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(saida, "fatiamento.jpg"), fatiamento)

# ============================
# FIM
# ============================

print("Processamento concluído! Imagens salvas na pasta:", saida)
