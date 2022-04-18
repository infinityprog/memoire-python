import cv2
import matplotlib.pyplot as plt

from work.DepthEstimation import depthEstimation

img = cv2.imread('data/images/yolo_compare.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = depthEstimation(img)

plt.imsave('result/images/midas/midas.jpg', img, format='jpg')
