import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def to_gray(img):
    return (
        0.299 * img[:, :, 2] +
        0.587 * img[:, :, 1] +
        0.114 * img[:, :, 0]
    ).astype(np.uint8)


def calcular_media(img):
    total_pixels = img.shape[0] * img.shape[1]
    soma = 0.0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            soma += img[y, x]
    return soma / total_pixels


def calcular_variancia(img, media):
    total_pixels = img.shape[0] * img.shape[1]
    soma = 0.0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            diff = img[y, x] - media
            soma += diff * diff
    return soma / total_pixels


def calcular_energia(img):
    altura, largura = img.shape
    frequencias = [0] * 256
    for y in range(altura):
        for x in range(largura):
            frequencias[img[y, x]] += 1

    total_pixels = altura * largura
    energia = 0.0
    for i in range(256):
        p_i = frequencias[i] / total_pixels
        energia += p_i * p_i
    return energia


def diferenca_horizontal(img):
    altura, largura = img.shape
    diff = 0.0
    for y in range(altura):
        for x in range(largura - 1):
            diff += abs(img[y, x] - img[y, x + 1])
    return diff / (altura * (largura - 1))


def diferenca_vertical(img):
    altura, largura = img.shape
    diff = 0.0
    for y in range(altura - 1):
        for x in range(largura):
            diff += abs(img[y, x] - img[y + 1, x])
    return diff / ((altura - 1) * largura)


def extrair_descritores(img_gray):
    img_f = img_gray.astype(float)
    media = calcular_media(img_f)
    return {
        "Media": media,
        "Variancia": calcular_variancia(img_f, media),
        "Energia": calcular_energia(img_gray),
        "Dif_Horizontal": diferenca_horizontal(img_f),
        "Dif_Vertical": diferenca_vertical(img_f),
    }


def imprimir_descritores(rotulo, descritores):
    print(f"\n{'=' * 30}")
    print(f"DESCRITORES - {rotulo}")
    print('=' * 30)
    for chave, valor in descritores.items():
        print(f"{chave}: {valor}")


def salvar_arquivo_txt(caminho, descritores1, descritores2):
    with open(caminho, "w") as f:
        for rotulo, desc in [("IMAGEM 1", descritores1), ("IMAGEM 2", descritores2)]:
            f.write(f"DESCRITORES - {rotulo}\n")
            f.write("========================\n")
            for chave, valor in desc.items():
                f.write(f"{chave}: {valor}\n")
            f.write("\n")


# --- Carregar imagens ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
img1_path = os.path.join(SCRIPT_DIR, "..", "images", "blusa2.png")
img2_path = os.path.join(SCRIPT_DIR, "..", "images", "jacket2.png")

img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
if img1 is None or img2 is None:
    print("Erro ao carregar imagens")
    raise SystemExit(1)

gray1 = to_gray(img1)
gray2 = to_gray(img2)

# --- Diretorio de saida ---
outdir = os.path.join(SCRIPT_DIR, "..", "resultados", "q4")
os.makedirs(outdir, exist_ok=True)

# --- Extrair descritores ---
descritores1 = extrair_descritores(gray1)
descritores2 = extrair_descritores(gray2)

# --- Exibir ---
imprimir_descritores("IMAGEM 1", descritores1)
imprimir_descritores("IMAGEM 2", descritores2)

# --- Salvar imagens cinza ---
cv2.imwrite(os.path.join(outdir, "imagem1_gray.png"), gray1)
cv2.imwrite(os.path.join(outdir, "imagem2_gray.png"), gray2)

# --- Grafico comparativo ---
nomes = list(descritores1.keys())
valores1 = list(descritores1.values())
valores2 = list(descritores2.values())
nomes_graf = ["Media", "Variancia", "Energia", "Dif. Horizontal", "Dif. Vertical"]

x = np.arange(len(nomes))
largura_barra = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - largura_barra / 2, valores1, largura_barra, label="Imagem 1")
plt.bar(x + largura_barra / 2, valores2, largura_barra, label="Imagem 2")
plt.xticks(x, nomes_graf)
plt.title("Comparacao de Descritores")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(outdir, "comparacao_descritores.png"), dpi=300, bbox_inches="tight")
plt.show()

# --- Salvar relatorio ---
salvar_arquivo_txt(os.path.join(outdir, "descritores.txt"), descritores1, descritores2)
print(f"\nResultados salvos em {outdir}")
