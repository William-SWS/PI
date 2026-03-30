import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("borboleta.jpeg", 0)

bordas = cv2.Canny(img, 100, 200)

plt.figure(figsize=(8,4))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(bordas, cmap="gray")
plt.axis('off')

plt.tight_layout()
plt.savefig("1_canny.png")
