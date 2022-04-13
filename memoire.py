import cv2

from work.DepthCalculation import DepthCalculation
from work.DepthEstimation import depthEstimation
from work.Yolo import findObject, Object, jsonToObject
from work.util import crop
from datetime import datetime
import numpy as np
#
# print(str(datetime.now()))
# cap = cv2.VideoCapture('chaise.mp4')
#
# while cap.isOpened():
#     ret,frame = cap.read()
#     if not ret:
#         continue
#
#     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     #
#     result = findObject(img)
#     objects = jsonToObject(result)
#     object = Object(**objects[0])
#
#     output = depthEstimation(img)
#     output = crop(output, object)
#     print(output.shape)
#     # print(img.shape)
#     depthCalculation = DepthCalculation(output)
#     depthCalculation.calculate()
#
#     print(depthCalculation.result())
#     print(str(datetime.now()))
#     output = cv2.applyColorMap(output, cv2.COLORMAP_MAGMA)
#
#     scale_percent = 40 # percent of original size
#     width = int(output.shape[1] * scale_percent / 100)
#     height = int(output.shape[0] * scale_percent / 100)
#     dim = (width, height)
#
#     output = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)
#     #
#     # cv2.imshow('Image', output)
#     img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     cv2.imshow('old', img)
#
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
#
# cap.release()
# cv2.destroyAllWindows()
cap = cv2.VideoCapture('chaise2.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = findObject(img)
    objects = jsonToObject(result)
    for obj in objects:
        object = Object(**obj)
        print(object.name)

        output = depthEstimation(img)
        output = crop(output, object)
        print(output.shape)
        # print(img.shape)
        depthCalculation = DepthCalculation(output)
        depthCalculation.calculate()

        # print(depthCalculation.result())
        # print(str(datetime.now()))
        # output = cv2.applyColorMap(output, cv2.COLORMAP_MAGMA)
        #
        # scale_percent = 40 # percent of original size
        # width = int(output.shape[1] * scale_percent / 100)
        # height = int(output.shape[0] * scale_percent / 100)
        # dim = (width, height)
        #
        # output = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)

    cv2.putText(img,object.name + " : " + depthCalculation.result(), (10, 100), cv2.FONT_HERSHEY_SIMPLEX,1, 0, 3)
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
