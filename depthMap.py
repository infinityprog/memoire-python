import cv2
import matplotlib.pyplot as plt
import timeit

from work.DepthEstimation import depthEstimation

img = cv2.imread('../../MiDaS/yolo_compare.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

start = timeit.default_timer()
img = depthEstimation(img)
stop = timeit.default_timer()
print(str(stop - start) + 's')

# plt.imsave('result/images/midas/middle_low.jpg', img, format='jpg')
