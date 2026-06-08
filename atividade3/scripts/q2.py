import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================================================
# QUESTÃO 4 - Descritores de Imagem
# ==================================================

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
# 2. Média (Brilho geral)
# -------------------------
def calcular_media(img):
    altura, largura = img.shape
    soma = 0.0

    for y in range(altura):
        for x in range(largura):
            soma += img[y, x]
    media = soma / (altura * largura)

    return media


# -------------------------------
# 3. Variância (Contraste global)
# -------------------------------
def calcular_variancia(img, media):
    altura, largura = img.shape
    soma = 0.0

    for y in range(altura):
        for x in range(largura):
            soma += (img[y, x] - media) ** 2

    variancia = soma / (altura * largura)

    return variancia


# -----------------------------------------------------------
# 4. Energia (Uniformidade/Homogeneidade dos níveis de cinza)
# -----------------------------------------------------------
def calcular_energia(img):
    altura, largura = img.shape

    # Primeiro calculamos o histograma normalizado (probabilidades)
    frequencias = [0] * 256
    for y in range(altura):
        for x in range(largura):
            frequencias[img[y, x]] += 1
            
    energia = 0.0
    for i in range(256):
        p_i = frequencias[i] / (altura * largura)
        energia += p_i ** 2  # Soma das probabilidades ao quadrado

    return energia

# --------------------------------------------------------------------
# 5. Diferença Absoluta Horizontal (Variação de textura na horizontal)
# --------------------------------------------------------------------
def diferenca_horizontal(img):
    altura, largura = img.shape
    diff_horizontal = 0.0

    for y in range(altura):
        for x in range(largura - 1):
            atual = img[y, x]
            vizinho = img[y, x + 1]
            diff_horizontal += abs(atual - vizinho)

    diff_horizontal /= (altura * (largura - 1)) # Média por pixel vizinho
    return diff_horizontal


# ----------------------------------------------------------------
# 6. Diferença Absoluta Vertical (Variação de textura na vertical)
# ----------------------------------------------------------------
def diferenca_vertical(img):
    altura, largura = img.shape
    diff_vertical = 0.0

    for y in range(0, altura - 1):
        for x in range(largura):
            atual = img[y, x]
            vizinho = img[y + 1, x]
            diff_vertical += abs(atual - vizinho)

    diff_vertical /= ((altura - 1) * largura) # Média por pixel vizinho
    return diff_vertical


# -------------------------
# 7. Extrair descritores
# -------------------------

def extrair_descritores(img_gray):
    # Converter para float para evitar overflow nos cálculos matemáticos
    img_f = img_gray.astype(float)
    
    # --- A. Métricas Estatísticas Globais ---
    media = calcular_media(img_f)
    variancia = calcular_variancia(img_f, media)
    energia = calcular_energia(img_gray)

    # --- B. Medidas de Variação Espacial (Estruturais) ---
    diff_horizontal = diferenca_horizontal(img_f)
    diff_vertical = diferenca_vertical(img_f)

    return {
        "Média": media,
        "Variância": variancia,
        "Energia": energia,
        "Diff_Horizontal": diff_horizontal,
        "Diff_Vertical": diff_vertical
    }


# -------------------------
# 8. Carregar imagens
# -------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Carregando imagens...")
img1_path = os.path.join(SCRIPT_DIR, "..", "images", "blusa2.png")
img2_path = os.path.join(SCRIPT_DIR, "..", "images", "jacket2.png")
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)

if img1 is None or img2 is None:
    print("Erro ao carregar imagens")
    exit()

gray1 = to_gray(img1)
gray2 = to_gray(img2)
print("Imagens carregadas!")


# -------------------------
# 9. Criar pastas
# -------------------------
outdir = os.path.join(SCRIPT_DIR, "..", "resultados")
os.makedirs(outdir, exist_ok=True)
os.makedirs(os.path.join(outdir, "q4"), exist_ok=True)


# -------------------------
# 10. Extrair descritores
# -------------------------
descritores1 = extrair_descritores(gray1)
descritores2 = extrair_descritores(gray2)


# -------------------------
# 11. Mostrar resultados
# -------------------------
print("\n==============================")
print("DESCRITORES - IMAGEM 1")
print("==============================")

for chave, valor in descritores1.items():
    print(f"{chave}: {valor}")

print("\n==============================")
print("DESCRITORES - IMAGEM 2")
print("==============================")

for chave, valor in descritores2.items():
    print(f"{chave}: {valor}")


# -------------------------
# 12. Salvar imagens
# -------------------------
cv2.imwrite(os.path.join(outdir, "q4/imagem1_gray.png"), gray1)
cv2.imwrite(os.path.join(outdir, "q4/imagem2_gray.png"), gray2)


# -------------------------
# 13. Gráfico comparativo
# -------------------------
nomes = [
    "Média",
    "Variância",
    "Energia",
    "Dif. Horizontal",
    "Dif. Vertical"
]

valores1 = [
    descritores1["Média"],
    descritores1["Variância"],
    descritores1["Energia"],
    descritores1["Diff_Horizontal"],
    descritores1["Diff_Vertical"]
]

valores2 = [
    descritores2["Média"],
    descritores2["Variância"],
    descritores2["Energia"],
    descritores2["Diff_Horizontal"],
    descritores2["Diff_Vertical"]
]

x = np.arange(len(nomes))
largura_barra = 0.35

plt.figure(figsize=(12, 6))

plt.bar(x - largura_barra/2, valores1, largura_barra, label="Imagem 1")
plt.bar(x + largura_barra/2, valores2, largura_barra, label="Imagem 2")

plt.xticks(x, nomes)

plt.title("Comparação de Descritores")
plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(outdir, "q4/comparacao_descritores.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# -------------------------
# 14. Salvar relatório txt
# -------------------------
arquivo = open(os.path.join(outdir, "q4/descritores.txt"), "w")

arquivo.write("DESCRITORES - IMAGEM 1\n")
arquivo.write("========================\n")

for chave, valor in descritores1.items():
    arquivo.write(f"{chave}: {valor}\n")

arquivo.write("\n")

arquivo.write("DESCRITORES - IMAGEM 2\n")
arquivo.write("========================\n")

for chave, valor in descritores2.items():
    arquivo.write(f"{chave}: {valor}\n")

arquivo.close()

print("\nResultados salvos em resultados/q4")