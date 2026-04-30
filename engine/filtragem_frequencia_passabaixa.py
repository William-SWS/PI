import cv2
import numpy as np

# =========================
# 1. Ler imagem (grayscale)
# =========================
img = cv2.imread("cat.jpg", cv2.IMREAD_GRAYSCALE)
img = img.astype(np.float32)

# =========================
# 2. FFT
# =========================
dft = np.fft.fft2(img)
dft_shift = np.fft.fftshift(dft)

# =========================
# 3. Criar grade de frequência
# =========================
rows, cols = img.shape
crow, ccol = rows // 2, cols // 2

u = np.arange(rows)
v = np.arange(cols)
U, V = np.meshgrid(u, v, indexing='ij')

D = np.sqrt((U - crow)**2 + (V - ccol)**2)

# =========================
# 4. Filtros passa-baixa
# =========================

D0 = 30  # frequência de corte
n = 2    # ordem do Butterworth

# 4.1 Ideal
H_ideal = np.zeros((rows, cols))
H_ideal[D <= D0] = 1

# 4.2 Butterworth
H_butter = 1 / (1 + (D / D0)**(2 * n))

# 4.3 Gaussiano
H_gauss = np.exp(-(D**2) / (2 * (D0**2)))

# =========================
# 5. Aplicar filtros
# =========================
def apply_filter(H, name):
    G = dft_shift * H

    # Inversa
    g_ishift = np.fft.ifftshift(G)
    img_back = np.fft.ifft2(g_ishift)
    img_back = np.abs(img_back)

    # Normalizar para salvar
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
    img_back = img_back.astype(np.uint8)

    cv2.imwrite(f"passabaixa-{name}.png", img_back)


apply_filter(H_ideal, "ideal")
apply_filter(H_butter, "butterworth")
apply_filter(H_gauss, "gaussian")
