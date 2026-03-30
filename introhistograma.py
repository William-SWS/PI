import cv2
import numpy as np

def plot_histogram(img):
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    hist_img = np.zeros((256,256), dtype=np.uint8)
    hist_norm = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    for x, y in enumerate(hist_norm):
        cv2.line(hist_img, (x,255), (x,255-int(y)), 255)
    return hist_img

def combine_img_hist(img, hist):
    hist_resized = cv2.resize(hist, (img.shape[1], img.shape[0]))
    return np.hstack((img, hist_resized))

# Lista de imagens
arquivos = ['gatodark.jpg', 'gatobranco.jpg', 'gatoaltocontraste.jpg']

combined_images = []
for arq in arquivos:
    img = cv2.imread(arq, cv2.IMREAD_GRAYSCALE)
    hist = plot_histogram(img)
    combined_images.append(combine_img_hist(img,hist))

# Salvar todas as 3 imagens lado a lado
cv2.imwrite('gatos_histogramas.jpg', np.hstack(combined_images))

# Equalizar gatodark e gatobranco
for nome in ['gatodark','gatobranco']:
    img = cv2.imread(f'{nome}.jpg', cv2.IMREAD_GRAYSCALE)
    img_eq = cv2.equalizeHist(img)
    hist_orig = plot_histogram(img)
    hist_eq = plot_histogram(img_eq)
    final_eq = np.hstack((combine_img_hist(img,hist_orig), combine_img_hist(img_eq,hist_eq)))
    cv2.imwrite(f'{nome}_equalizacao.jpg', final_eq)
