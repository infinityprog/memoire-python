import cv2
from pygame import mixer
import sys

from result.check import ajustTime
from work.Compare import Compare
from work.DepthCalculation import DepthCalculation, Status
from work.DepthEstimation import depthEstimation
from work.Yolo import Object, jsonToObject, Yolo
from work.env import repCompare
from work.util import crop, most_frequent, findStatus, findStatusMin

def main():
    cap = cv2.VideoCapture('chaise2.mp4')
    isCompare = sys.argv[1] if len(sys.argv) > 1 else False
    fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('hauteur : ' + str(frame_height) + 'px, largeur : ' + str(frame_width) + 'px')
    compare = Compare()
    if isCompare:
        compare.initFile(repCompare('depthmap') + 'actual.csv')

    statusList = []
    compareStatusList = []
    status = Status.OK
    time = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        frameId = int(round(cap.get(1)))
        # Avoir une moyenne de status pour ne pas avoir danger et juste après ok

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Créer un seul bip et prendre le max du status
        depthMapImg = depthEstimation(img)
        object = Object(60,100,300, 500, 1, 'test')
        output = crop(depthMapImg, object)
        # cv2.imshow('crop', output)
        depthCalculation = DepthCalculation(output)
        depthCalculation.calculate()


        statusList.append(depthCalculation.status)

        # Choisi le status à afficher sur l'image toutes les 1/2 secs
        if frameId % 5 == 0:
            status = findStatusMin(statusList, 3) if findStatusMin(statusList, 3) != None else Status.OK
            compareStatusList.append(status)
            statusList = []

        # Choisi le status qui va être comparé et écrire dans le fichier csv de comparaison
        if isCompare and frameId % fps == 0:
            time = compare.writeComparaison(time, findStatusMin(compareStatusList, 1).name)
            compareStatusList = []

        # Create video
        # videoWriter.write(img)
        if not isCompare:
            cv2.putText(img, status.name, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 3)
            cv2.imshow('frame',img)
            cv2.imshow('depth', depthMapImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Si il reste du temps ça écrit une dernière fois
    if isCompare and frameId % fps != 0:
        if len(compareStatusList) == 0:
            compareStatusList.append(Status.OK)
        compare.writeComparaison(time, findStatusMin(compareStatusList, 1).name)

    cap.release()
    # videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
