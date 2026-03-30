import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("img_ruido.jpg", 0)
blur = cv2.GaussianBlur(img, (21, 21), 0)

plt.figure(figsize=(8,4))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(blur, cmap="gray")
plt.axis('off')

plt.tight_layout()
plt.savefig("1_gaussian.png")
