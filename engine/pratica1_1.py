import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Funções de métricas
# -------------------------

def mae(img1, img2):
    return np.mean(np.abs(img1 - img2))

def mse(img1, img2):
    return np.mean((img1 - img2) ** 2)

def rmse(img1, img2):
    return np.sqrt(mse(img1, img2))

def correlacao(img1, img2):
    img1_f = img1.flatten()
    img2_f = img2.flatten()
    return np.corrcoef(img1_f, img2_f)[0,1]

def jaccard(img1, img2):
    # binarização simples
    _, b1 = cv2.threshold(img1,127,255,cv2.THRESH_BINARY)
    _, b2 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY)

    intersec = np.logical_and(b1, b2).sum()
    uniao = np.logical_or(b1, b2).sum()

    return intersec / uniao

# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread("cat1.jpeg")

# converter para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = gray.shape

# níveis de amostragem
scales = [1.0, 0.5, 0.25, 0.10]

results = []
images = []

for s in scales:

    # reduzir
    small = cv2.resize(gray, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA)

    # voltar para tamanho original
    resized = cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)

    images.append(resized)

    results.append({
        "scale": s,
        "MAE": mae(gray, resized),
        "MSE": mse(gray, resized),
        "RMSE": rmse(gray, resized),
        "CORR": correlacao(gray, resized),
        "JACCARD": jaccard(gray, resized)
    })

# -------------------------
# Mostrar imagens
# -------------------------

plt.figure(figsize=(12,4))

titles = ["100%", "50%", "25%", "10%"]

for i,img_show in enumerate(images):
    plt.subplot(1,4,i+1)
    plt.imshow(img_show, cmap="gray")
    plt.title(titles[i])
    plt.axis("off")

plt.show()

# -------------------------
# Mostrar métricas
# -------------------------

for r in results:
    print(f"\nEscala: {r['scale']*100:.0f}%")
    print("MAE:", r["MAE"])
    print("MSE:", r["MSE"])
    print("RMSE:", r["RMSE"])
    print("Correlação:", r["CORR"])
    print("Jaccard:", r["JACCARD"])
