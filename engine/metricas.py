import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("cat.jpg", 0)

def adicionar_sal_pimenta(img, prob=0.15):
    noisy = img.copy()
    rand = np.random.rand(*img.shape)
    noisy[rand < prob/2] = 255
    noisy[rand > 1 - prob/2] = 0
    
    return noisy
    
img_ruido = adicionar_sal_pimenta(img, prob=0.25)

cv2.imwrite("metrica_original.png", img)
cv2.imwrite("metrica_ruido.png", img_ruido)

# -----------------------------
# 4. Converter para float
# -----------------------------
I = img.astype(np.float64)
K = img_ruido.astype(np.float64)

# -----------------------------
# 5. Métricas de erro
# -----------------------------

erro = I - K

# Erro máximo
erro_max = np.max(np.abs(erro))

# MAE
mae = np.mean(np.abs(erro))

# MSE
mse = np.mean(erro**2)

# RMSE
rmse = np.sqrt(mse)

# NMSE
nmse = mse / np.mean(I**2)

# -----------------------------
# 6. PSNR
# -----------------------------
max_pixel = 255
psnr = 10 * np.log10((max_pixel**2) / mse)

# -----------------------------
# 7. SNR
# -----------------------------
snr = 10 * np.log10(np.sum(I*2) / np.sum((I-K)*2))

# -----------------------------
# 8. Covariância
# -----------------------------
cov = np.cov(I.flatten(), K.flatten())[0,1]

# -----------------------------
# 9. Correlação
# -----------------------------
corr = np.corrcoef(I.flatten(), K.flatten())[0,1]

# -----------------------------
# 10. Índice de Jaccard
# -----------------------------
# binarizar imagens
I_bin = I > 0
K_bin = K > 0

intersec = np.logical_and(I_bin, K_bin).sum()
uniao = np.logical_or(I_bin, K_bin).sum()

jaccard = intersec / uniao

# -----------------------------
# 11. Mostrar resultados
# -----------------------------
print("===== MÉTRICAS DE QUALIDADE =====")
print("Erro Máximo:", erro_max)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("NMSE:", nmse)
print("PSNR:", psnr)
print("SNR:", snr)
print("Covariância:", cov)
print("Correlação:", corr)
print("Jaccard:", jaccard)