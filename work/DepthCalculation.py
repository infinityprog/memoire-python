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
        nbrMiddle = 0;
        nbrDanger = 0;
        result = np.where(self.img > 200);
        print(np.size(result))
        for valuePixel in np.nditer(self.img):
            if valuePixel > self.MAX_MIDDLE:
                nbrMiddle += 1
            if valuePixel > self.MAX_DANGER:
                nbrDanger += 1
                # if nbrDanger > self.__getRatioPixel():
                #     break

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
