import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import os

BLOCK_SIZE = 64
FATOR_QUALIDADE = 2.0

MATRIZ_Q_BASE = np.array([
    [16, 11, 10, 16, 24,  40,  51,  61],
    [12, 12, 14, 19, 26,  58,  60,  55],
    [14, 13, 16, 24, 40,  57,  69,  56],
    [14, 17, 22, 29, 51,  87,  80,  62],
    [18, 22, 37, 56, 68,  109, 103, 77],
    [24, 35, 55, 64, 81,  104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.float32)


def to_gray(img):
    return (
        0.299 * img[:, :, 2] +
        0.587 * img[:, :, 1] +
        0.114 * img[:, :, 0]
    ).astype(np.uint8)


def _dct_matrix(N):
    C = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            C[i, j] = math.cos((2 * i + 1) * j * math.pi / (2 * N))
    return C


def _dct_normalization(N):
    c = np.ones(N)
    c[0] = math.sqrt(1 / N)
    c[1:] = math.sqrt(2 / N)
    return c


def dct2d(bloco, N=BLOCK_SIZE):
    bloco_f = bloco.astype(float) - 128.0
    C = _dct_matrix(N)
    c = _dct_normalization(N)
    return (c[:, None] * (C.T @ bloco_f @ C)) * c[None, :]


def idct2d(bloco_dct, N=BLOCK_SIZE):
    C = _dct_matrix(N)
    c = _dct_normalization(N)
    reconstruido = (C @ (bloco_dct * c[:, None]) * c[None, :]) @ C.T
    return reconstruido + 128.0


def obter_matriz_q(tamanho_bloco):
    if tamanho_bloco == 8:
        return MATRIZ_Q_BASE * FATOR_QUALIDADE
    if tamanho_bloco % 8 == 0:
        fator = tamanho_bloco // 8
        return np.kron(MATRIZ_Q_BASE, np.ones((fator, fator), dtype=np.float32)) * FATOR_QUALIDADE
    return np.ones((tamanho_bloco, tamanho_bloco), dtype=np.float32) * (16 * FATOR_QUALIDADE)


MATRIZ_Q = obter_matriz_q(BLOCK_SIZE)

# --- Carregar imagem ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(SCRIPT_DIR, "..", "images", "runner.png")
img = cv2.imread(img_path)
if img is None:
    print("Erro ao carregar imagem")
    raise SystemExit(1)

gray = to_gray(img)
altura, largura = gray.shape

# --- Criar diretorio de saida ---
outdir = os.path.join(SCRIPT_DIR, "..", "resultados")
bloco_dir = os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}")
os.makedirs(bloco_dir, exist_ok=True)

# --- Ajustar dimensoes para multiplo de BLOCK_SIZE ---
altura = (altura // BLOCK_SIZE) * BLOCK_SIZE
largura = (largura // BLOCK_SIZE) * BLOCK_SIZE
gray = gray[:altura, :largura]

# --- Compressao DCT por blocos ---
img_reconstruida = np.zeros_like(gray, dtype=float)
total_linhas = altura // BLOCK_SIZE

for linha in range(0, altura, BLOCK_SIZE):
    print(f"Processando linha {linha // BLOCK_SIZE + 1}/{total_linhas}")

    for col in range(0, largura, BLOCK_SIZE):
        bloco = gray[linha:linha + BLOCK_SIZE, col:col + BLOCK_SIZE]
        bloco_dct = dct2d(bloco)
        bloco_q = np.round(bloco_dct / MATRIZ_Q)
        bloco_dq = bloco_q * MATRIZ_Q
        img_reconstruida[linha:linha + BLOCK_SIZE, col:col + BLOCK_SIZE] = idct2d(bloco_dq)

img_reconstruida = np.clip(img_reconstruida, 0, 255).astype(np.uint8)
diferenca = cv2.absdiff(gray, img_reconstruida)

# --- Salvar resultados ---
cv2.imwrite(os.path.join(bloco_dir, "original_cinza.png"), gray)
cv2.imwrite(os.path.join(bloco_dir, "imagem_reconstruida.png"), img_reconstruida)
cv2.imwrite(os.path.join(bloco_dir, "diferenca.png"), diferenca)

# --- Plot ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, img_data, titulo in zip(
    axes,
    [gray, img_reconstruida, diferenca],
    ["Original", "Reconstruida", "Diferenca"],
):
    ax.imshow(img_data, cmap="gray")
    ax.set_title(titulo)
    ax.axis("off")

fig.tight_layout()
fig.savefig(os.path.join(bloco_dir, "resultado_geral_q3.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(outdir, "resultado_q3.png"), dpi=300, bbox_inches="tight")
print(f"Resultados salvos em {bloco_dir}")
plt.show()
