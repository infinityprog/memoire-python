import numpy as np
import enum

class Status(enum.Enum):
    OK = 'Pas de danger'
    WARNING = 'Un objet est pas loin'
    DANGER = 'Attention vous etes trop proche'

class DepthCalculation:
    MAX_MIDDLE = 150
    MAX_DANGER = 200
    RATIO_PIXEL = 4
    status = ''

    def __init__(self, img):
        self.img = img

    def calculate(self):
        nbrDanger = (self.img[:,:] > 200).sum()
        nbrMiddle = (self.img[:,:] > 150).sum()

        print(nbrDanger)
        if nbrDanger > self.__getRatioPixel():
            self.status = Status.DANGER
        elif nbrMiddle > self.__getRatioPixel():
            self.status = Status.WARNING
        else:
            self.status = Status.OK


    def __getRatioPixel(self):
        return (self.img.shape[0] * self.img.shape[1]) / self.RATIO_PIXEL

    def result(self):
        return self.status.name
