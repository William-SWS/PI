import cv2

# Carregar imagem em escala de cinza
img = cv2.imread('cat1.jpeg', cv2.IMREAD_GRAYSCALE)
brilho = 80
gatodark = cv2.add(img, -brilho)
gatobranco = cv2.add(img, brilho)
gatoaltocontraste = cv2.convertScaleAbs(img, alpha=1.5, beta=0)

cv2.imwrite("gatodark.jpg", gatodark)
cv2.imwrite("gatobranco.jpg", gatobranco)
cv2.imwrite("gatoaltocontraste.jpg", gatoaltocontraste)

