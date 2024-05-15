from PIL import Image
import numpy as np
import cv2

img = Image.open('900.jpg').convert('L')
img = np.array(img)
print(img)
print(img.shape)
print("=============================================")
image = cv2.imread('900.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(image)
print(image.shape)
