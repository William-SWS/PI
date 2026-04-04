import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("cat.jpg", 0)
ruido = np.random.normal(0, 50, img.shape)
img_ruido = img + ruido
np.clip(img_ruido, 0, 255).astype(np.uint8)

cv2.imwrite('img_ruido.jpg', img_ruido)

plt.figure(figsize=(8,4))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_ruido, cmap="gray")
plt.axis('off')

plt.tight_layout()
plt.savefig("1_ruido.png")
