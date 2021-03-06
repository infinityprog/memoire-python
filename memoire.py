import cv2
from pygame import mixer
import sys

from result.check import ajustTime
from work.Compare import Compare
from work.DepthCalculation import DepthCalculation, Status
from work.DepthEstimation import depthEstimation
from work.Yolo import Object, jsonToObject, Yolo
from work.env import repCompare
from work.util import crop, most_frequent, findStatus, findStatusMin, drawBoundingBox

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

def main():
    yoloModelName = sys.argv[1] if len(sys.argv) > 1 else 'yolov5m'
    isCompare = sys.argv[2] if len(sys.argv) > 1 else False
    yolo = Yolo(yoloModelName)
    cap = cv2.VideoCapture('test.mp4')
    # seconds = 0.1
    fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    print('fps : ' + str(fps))
    # multiplier = fps * seconds
    compare = Compare()
    if isCompare:
        compare.initFile(repCompare(yoloModelName) + 'actual.csv')

    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #
    # videoWriter = VideoWriter((frame_width,frame_height), fps)
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
        # output2 = depthEstimation(img)
        # dImg = depthImg(output2)

        result = yolo.findObject(img)
        objects = jsonToObject(result)

        # Créer un seul bip et prendre le max du status
        statusOfObjectInImg = []
        depthMapImg = None
        lock = False
        for obj in objects:
            object = Object(**obj)

            if not lock:
                depthMapImg = depthEstimation(img)
                lock = True

            output = crop(depthMapImg, object)

            depthCalculation = DepthCalculation(output, 4)
            depthCalculation.calculate()

            if depthCalculation.status == Status.WARNING or depthCalculation.status == Status.DANGER:
                img = drawBoundingBox(img, object.name + " : " + str(object.confidence), object)

            statusOfObjectInImg.append(depthCalculation.status)

        # playSound(statusOfObjectInImg, oldStatusList)


        statusList.append(findStatus(statusOfObjectInImg))

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
            if depthMapImg is not None:
                cv2.imshow('depth', depthMapImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Si il reste du temps ça écrit une dernière fois
    if isCompare and frameId % fps != 0:
        if len(compareStatusList) == 0:
            compareStatusList.append(Status.OK.name)
        compare.writeComparaison(time, findStatusMin(compareStatusList, 1).name)

    cap.release()
    # videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
