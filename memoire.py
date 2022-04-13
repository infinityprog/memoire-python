import cv2

from work.DepthCalculation import DepthCalculation
from work.DepthEstimation import depthEstimation
from work.Yolo import findObject, Object, jsonToObject
from work.util import crop
from datetime import datetime
import numpy as np

print(str(datetime.now()))
img = cv2.imread('good.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

result = findObject(img)
objects = jsonToObject(result)
object = Object(**objects[0])

# old = img.copy()
# img = crop(img, object)
output = depthEstimation(img)
output = crop(output, object)
print(output.shape)
# print(img.shape)
depthCalculation = DepthCalculation(output)
depthCalculation.calculate()

print(depthCalculation.result())
print(str(datetime.now()))
# output = cv2.applyColorMap(output, cv2.COLORMAP_MAGMA)
#
# scale_percent = 40 # percent of original size
# width = int(output.shape[1] * scale_percent / 100)
# height = int(output.shape[0] * scale_percent / 100)
# dim = (width, height)
#
# output = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)
#
# while True:
#
#     cv2.imshow('Image', output)
#     cv2.imshow('old', img)
#
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
#
# cv2.destroyAllWindows()
