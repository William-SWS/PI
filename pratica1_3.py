import cv2
import numpy as np

# -------------------------
# Funções de ruído
# -------------------------

def ruido_gaussiano(img, media=0, sigma=25):
    gauss = np.random.normal(media, sigma, img.shape)
    noisy = img + gauss
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)


def ruido_sal_pimenta(img, prob=0.02):
    noisy = img.copy()

    rand = np.random.rand(*img.shape)

    noisy[rand < prob/2] = 0
    noisy[rand > 1 - prob/2] = 255

    return noisy


def ruido_speckle(img):
    gauss = np.random.randn(*img.shape)
    noisy = img + img * gauss
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread("uece.jpg", cv2.IMREAD_GRAYSCALE)

# -------------------------
# Gerar ruídos
# -------------------------

gauss = ruido_gaussiano(img)
salpimenta = ruido_sal_pimenta(img)
speckle = ruido_speckle(img)

cv2.imwrite("ruido_gaussiano.jpg", gauss)
cv2.imwrite("ruido_sal_pimenta.jpg", salpimenta)
cv2.imwrite("ruido_speckle.jpg", speckle)

# -------------------------
# Filtros
# -------------------------

def aplicar_filtros(nome, imagem):

    media = cv2.blur(imagem, (5,5))
    mediana = cv2.medianBlur(imagem, 5)
    gauss = cv2.GaussianBlur(imagem, (5,5), 0)

    cv2.imwrite(f"{nome}_media.jpg", media)
    cv2.imwrite(f"{nome}_mediana.jpg", mediana)
    cv2.imwrite(f"{nome}_gaussiano.jpg", gauss)


aplicar_filtros("gaussiano", gauss)
aplicar_filtros("sal_pimenta", salpimenta)
aplicar_filtros("speckle", speckle)

print("Processamento concluído. Imagens salvas.")