import numpy as np
import enum
from pygame import mixer


class Status(enum.Enum):
    OK = 'Pas de danger'
    WARNING = 'Un objet est pas loin'
    DANGER = 'Attention vous etes trop proche'


class DepthCalculation:
    MAX_MIDDLE = 150
    MAX_DANGER = 200
    RATIO_PIXEL = 2.5
    status = ''
    __sound = None

    def __init__(self, img, ratio=2.5):
        self.img = img
        self.RATIO_PIXEL = ratio
        mixer.init()
        self.__sound = mixer.Sound("beep.wav")

    def calculate(self):
        nbrDanger = (self.img[:, :] >= 200).sum()
        nbrMiddle = (self.img[:, :] >= 100).sum()

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

    def playSound(self):
        if self.status == Status.WARNING:
            self.__sound.play()
        elif self.status == Status.DANGER:
            self.__sound.play()
            self.__sound.play()
