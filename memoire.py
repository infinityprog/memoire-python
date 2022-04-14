import cv2

from work.DepthCalculation import DepthCalculation, Status
from work.DepthEstimation import depthEstimation
from work.Yolo import findObject, Object, jsonToObject
from work.util import crop
from datetime import datetime
import numpy as np

cap = cv2.VideoCapture('chaise2.mp4')
seconds = 0.1
fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
multiplier = fps * seconds

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    frameId = int(round(cap.get(1)))
    if frameId % multiplier == 0:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = findObject(img)
        objects = jsonToObject(result)
        for obj in objects:
            object = Object(**obj)
            # print(object.name)

            output = depthEstimation(img)
            output = crop(output, object)
            # print(output.shape)
            # # print(img.shape)
            depthCalculation = DepthCalculation(output)
            depthCalculation.calculate()
            depthCalculation.playSound()

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



