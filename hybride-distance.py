import cv2
import sys

import numpy as np

from result.check import ajustTime
from work.Compare import Compare
from work.DepthCalculation import DepthCalculation, Status
from work.DepthEstimation import depthEstimation, depthEstimationPur, normalizeDepthMap
from work.Yolo import Object, jsonToObject, Yolo
from work.env import repCompare
from work.util import crop, most_frequent, findStatus, findStatusMin, drawBoundingBox, getDistance, VideoWriter


def calculateDistanceDepthMap(depthMapImg) -> Status:
    object = Object(60,100,300, 500, 1, 'test')
    output = crop(depthMapImg, object)
    depthCalculation = DepthCalculation(output)
    depthCalculation.calculate()
    return depthCalculation.status

def main():
    yoloModelName = sys.argv[1] if len(sys.argv) > 1 else 'yolov5m'
    isCompare = sys.argv[2] if len(sys.argv) > 1 else False
    yolo = Yolo(yoloModelName)
    cap = cv2.VideoCapture('large.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    print('fps : ' + str(fps))
    compare = Compare()
    if isCompare:
        compare.initFile(repCompare('hybride') + 'actual.csv')

    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #
    # videoWriter = VideoWriter((frame_width * 2 ,frame_height), fps)
    statusList = []
    status = Status.OK
    time = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        frameId = int(round(cap.get(1)))
        # Avoir une moyenne de status pour ne pas avoir danger et juste après ok

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = yolo.findObject(img)
        objects = jsonToObject(result)
        depthMap = depthEstimationPur(img)
        depthMapImg = normalizeDepthMap(depthMap)

        # Créer un seul bip et prendre le max du status
        statusOfObjectInImg = []
        for obj in filter( lambda o: o['confidence'] > 0.3, objects):
            object = Object(**obj)

            output = crop(depthMap, object)

            depthCalculation = DepthCalculation(output, 4)
            depthCalculation.calculatePur()

            if depthCalculation.status == Status.WARNING or depthCalculation.status == Status.DANGER:
                height, width = output.shape
                distanceRelative = output[int(height / 2), int(width / 2)]
                cv2.circle(img, (int(object.xmin + (width / 2)), int(object.ymin + (height / 2))), 5, (0,0,255), -1)

                distance = int(getDistance(distanceRelative))
                img = drawBoundingBox(img, object.name + " : " + str(distance) + 'cm', object)

            statusOfObjectInImg.append(depthCalculation.status)

        statusYolo = findStatus(statusOfObjectInImg)
        statusDepthMap = calculateDistanceDepthMap(depthMapImg)

        if statusYolo in [Status.WARNING, Status.DANGER]:
            statusList.append(statusYolo)
        elif statusDepthMap in [Status.WARNING, Status.DANGER]:
            statusList.append(statusDepthMap)
        else:
            statusList.append(Status.OK)

        # Choisi le status à afficher sur l'image toutes les 1/2 secs
        if not isCompare and frameId % 15 == 0:
            status = findStatusMin(statusList, 3)
            statusList = []

        # Choisi le status qui va être comparé et écrire dans le fichier csv de comparaison
        if isCompare and frameId % fps == 0:
            time = compare.writeComparaison(time, findStatusMin(statusList, 7).name)
            statusList = []

        # Create video
        if not isCompare:
            cv2.putText(img, status.name, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 3)
            cv2.imshow('frame',img)
            # videoWriter.write(np.concatenate((cv2.cvtColor(depthMapImg,cv2.COLOR_GRAY2RGB), img), axis=1))
            cv2.imshow('depth', depthMapImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Si il reste du temps ça écrit une dernière fois
    if isCompare and frameId % fps != 0:
        if len(statusList) == 0:
            statusList.append(Status.OK)
        compare.writeComparaison(time, findStatusMin(statusList, 7).name)

    cap.release()
    # videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
