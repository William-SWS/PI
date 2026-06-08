import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# ==================================================
# QUESTÃO 3 - Compressão de Imagem com DCT (JPEG)
# ==================================================

# Tamanho dos blocos usados na DCT/IDCT
# Ajuste para 8, 16, 32, etc.
BLOCK_SIZE = 64

# -------------------------
# 1. Converter para cinza
# -------------------------
def to_gray(img):
    altura, largura, _ = img.shape
    gray = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            # Conversão manual para tons de cinza usando a fórmula de luminância
            valor = int(0.299 * r + 0.587 * g + 0.114 * b) 

            if valor > 255:
                valor = 255

            gray[y, x] = valor

    return gray


# -------------------------
# 2. DCT 2D Manual
# -------------------------
def dct2d(bloco, N=BLOCK_SIZE):
    '''
    Aplica a DCT-II bidimensional manualmente em um bloco
    '''
    dct_bloco = np.zeros((N, N))

    # Centraliza o bloco em torno de zero (subtrai 128) como no JPEG padrão
    bloco_f = bloco.astype(float) - 128.0

    for u in range(N):
        for v in range(N):
            soma = 0.0
            for x in range(N):
                for y in range(N):
                    cos_x = math.cos(((2*x + 1) * u * math.pi) / (2 * N))
                    cos_y = math.cos(((2*y + 1) * v * math.pi) / (2 * N))

                    soma += bloco_f[x, y] * cos_x * cos_y

            # Constantes de normalização c(u) e c(v)
            cu = math.sqrt(1/N) if u == 0 else math.sqrt(2/N)
            cv = math.sqrt(1/N) if v == 0 else math.sqrt(2/N)
            dct_bloco[u, v] = cu * cv * soma

    return dct_bloco


# -------------------------
# 3. IDCT 2D Manual
# -------------------------
def idct2d(bloco_dct, N=BLOCK_SIZE):
    """
    Aplica a IDCT-III bidimensional manualmente em um bloco 8x8.
    """
    bloco_reconstruido = np.zeros((N, N))

    for x in range(N):
        for y in range(N):
            soma = 0.0
            for u in range(N):
                for v in range(N):
                    cu = math.sqrt(1/N) if u == 0 else math.sqrt(2/N)
                    cv = math.sqrt(1/N) if v == 0 else math.sqrt(2/N)

                    cos_x = math.cos(((2*x + 1) * u * math.pi) / (2 * N))
                    cos_y = math.cos(((2*y + 1) * v * math.pi) / (2 * N))

                    soma += cu * cv * bloco_dct[u, v] * cos_x * cos_y

            # Desfaz a centralização somando 128
            bloco_reconstruido[x, y] = soma + 128.0

    return bloco_reconstruido


# -------------------------
# 4. Matriz de Quantização
# -------------------------
# Uma matriz padrão de luminância simplificada. 
# Valores mais altos significam maior compressão (e maior perda) nas altas frequências.
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

# Fator de qualidade: ajuste para mais ou para menos compressão (ex: 1.0 = padrão, 3.0 = muita compressão)
FATOR_QUALIDADE = 2.0 

# -------------------------------------------------------------
# 5. Função para adaptar a Matriz de Quantização Dinamicamente
# -------------------------------------------------------------
def obter_matriz_q(tamanho_bloco):
    if tamanho_bloco == 8:
        return MATRIZ_Q_BASE * FATOR_QUALIDADE
    
    # Se for maior que 8 (ex: 16, 32), expande usando Kronecker
    if tamanho_bloco % 8 == 0:
        fator = tamanho_bloco // 8
        matriz_expandida = np.kron(MATRIZ_Q_BASE, np.ones((fator, fator), dtype=np.float32))
        return matriz_expandida * FATOR_QUALIDADE
    
    # Caso coloque um tamanho bizarro não múltiplo de 8, gera uma matriz padrão flat
    return np.ones((tamanho_bloco, tamanho_bloco), dtype=np.float32) * (16 * FATOR_QUALIDADE)


# Gerando a matriz correta para o tamanho escolhido
MATRIZ_Q_AJUSTADA = obter_matriz_q(BLOCK_SIZE)

# -------------------------
# 7. Carregar imagem
# -------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Carregando imagem...")
img_path = os.path.join(SCRIPT_DIR, "..", "images", "runner.png")
img = cv2.imread(img_path)

if img is None:
    print("Erro ao carregar imagem")
    exit()

gray = to_gray(img)
altura, largura = gray.shape
print("Imagem carregada!")


# -------------------------
# 8. Criar pastas
# -------------------------
outdir = os.path.join(SCRIPT_DIR, "..", "resultados")
os.makedirs(outdir, exist_ok=True)
os.makedirs(os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}"), exist_ok=True)


# -------------------------
# 9. Ajustar tamanho
# -------------------------
# JPEG trabalha em blocos NxN
# então a imagem precisa ser múltipla de BLOCK_SIZE
nova_altura = (altura // BLOCK_SIZE) * BLOCK_SIZE
nova_largura = (largura // BLOCK_SIZE) * BLOCK_SIZE
gray = gray[:nova_altura, :nova_largura]
altura, largura = gray.shape


# -------------------------
# 10. Compressão com DCT
# -------------------------

img_reconstruida = np.zeros_like(gray, dtype=float)
print(f"Processando blocos {BLOCK_SIZE}x{BLOCK_SIZE}...")

# Loop por blocos NxN
for y in range(0, altura, BLOCK_SIZE):
    print(f"Linha de blocos: {y}/{altura}")

    for x in range(0, largura, BLOCK_SIZE):
        bloco = gray[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]  # Extrair bloco
        bloco_dct = dct2d(bloco, BLOCK_SIZE)  # DCT
        bloco_quantizado = np.round(bloco_dct / MATRIZ_Q_AJUSTADA) # Quantização
        bloco_desquantizado = bloco_quantizado * MATRIZ_Q_AJUSTADA   # Desquantização
        bloco_idct = idct2d(bloco_desquantizado, BLOCK_SIZE) # IDCT
        img_reconstruida[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = bloco_idct   # Salvar bloco

# Garante que os pixels fiquem no intervalo válido [0, 255]
imagem_reconstruida = np.clip(img_reconstruida, 0, 255).astype(np.uint8)


# -------------------------
# 11. Salvar imagens
# -------------------------
cv2.imwrite(os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}/original_cinza.png"), gray)
cv2.imwrite(os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}/imagem_reconstruida.png"), imagem_reconstruida)

diferenca = cv2.absdiff(gray, imagem_reconstruida)
cv2.imwrite(os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}/diferenca.png"), diferenca)


# -------------------------
# 12. Mostrar resultados
# -------------------------
plt.figure(figsize=(15, 5))

# Original
plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray")
plt.title("Original")
plt.axis("off")

# Reconstruída
plt.subplot(1, 3, 2)
plt.imshow(imagem_reconstruida, cmap="gray")
plt.title("Reconstruída")
plt.axis("off")

# Diferença
plt.subplot(1, 3, 3)
plt.imshow(diferenca, cmap="gray")
plt.title("Diferença")
plt.axis("off")

plt.tight_layout()

plt.savefig(os.path.join(outdir, f"q3_{BLOCK_SIZE}x{BLOCK_SIZE}/resultado_geral_q3.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(outdir, "resultado_q3.png"), dpi=300, bbox_inches="tight")
print(f"\nResultados salvos em {outdir}")
plt.show()