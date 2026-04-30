import cv2
import numpy as np

# Carregar imagem em escala de cinza
img = cv2.imread('cat.jpg', cv2.IMREAD_GRAYSCALE)
#img = cv2.imread('uece.jpg', cv2.IMREAD_GRAYSCALE)

# Verificar se carregou corretamente
if img is None:
    raise ValueError("Erro ao carregar a imagem.")

# Transformada de Fourier
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

# Magnitude do espectro (escala log)
magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

# Normalizar para 0–255 (uint8) para salvar como imagem
magnitude_norm = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
magnitude_norm = np.uint8(magnitude_norm)

# Salvar imagens
cv2.imwrite('espectro_cat.png', magnitude_norm)
#cv2.imwrite('espectro_uece.png', magnitude_norm)
