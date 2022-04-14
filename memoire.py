import cv2
import time

from work.DepthCalculation import DepthCalculation, Status
from work.DepthEstimation import depthEstimation
from work.Yolo import findObject, Object, jsonToObject
from work.util import crop
from datetime import datetime
import numpy as np
from pygame import mixer

mixer.init()
sound=mixer.Sound("beep.wav")

def playSound(statusList, oldStatusList):

    lastStatus = oldStatusList[-4:]

    if Status.DANGER in statusList:
        print(Status.DANGER)
        sound.play()
        oldStatusList.append(Status.DANGER)
    elif Status.WARNING in statusList:
        print(Status.WARNING)
        sound.play()
        sound.play()
        oldStatusList.append(Status.WARNING)
    else:
        print(Status.OK)
        oldStatusList.append(Status.OK)


def depthImg(img):
    output = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)

    scale_percent = 40 # percent of original size
    width = int(output.shape[1] * scale_percent / 100)
    height = int(output.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(output, dim, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture('chaise2.mp4')
seconds = 0.1
fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
multiplier = fps * seconds

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    frameId = int(round(cap.get(1)))
    # Avoir une moyenne de status pour ne pas avoir danger et juste après ok
    oldStatusList = []
    if frameId % multiplier == 0:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = findObject(img)
        objects = jsonToObject(result)

        # Créer un seul bip et prendre le max du status
        statusOfObjectInImg = []
        for obj in filter( lambda o: o['confidence'] > 0.5, objects):
            object = Object(**obj)
            # print(object.name)
            # print(object.confidence)

            output = depthEstimation(img)
            # dImg = depthImg(output)
            output = crop(output, object)
            # print(output.shape)
            # # print(img.shape)
            depthCalculation = DepthCalculation(output)
            depthCalculation.calculate()
            statusOfObjectInImg.append(depthCalculation.status)


        depthCalculation.playSound()
        # playSound(statusOfObjectInImg, oldStatusList)
        cv2.putText(img,object.name + " : " + depthCalculation.result(), (10, 100), cv2.FONT_HERSHEY_SIMPLEX,1, 0, 3)
        cv2.imshow('frame',img)
        # time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



