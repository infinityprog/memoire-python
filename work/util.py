import cv2

from work.DepthCalculation import Status


def crop(img, object):
    ylength = ((object.ymax - object.ymin) / 5)
    xlength = ((object.xmax - object.xmin) / 5)
    ymin = int(object.ymin + ylength)
    ymax = int(object.ymax - ylength)
    xmin = int(object.xmin + xlength)
    xmax = int(object.xmax - xlength)
    # calculate all image
    return img[int(object.ymin):int(object.ymax), int(object.xmin):int(object.xmax)]
    # return img[ymin:ymax, xmin:xmax]

def most_frequent(List):
    if len(List) == 0:
        return None
    return max(set(List), key = List.count)

def depthImg(img):
    output = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)

    scale_percent = 40 # percent of original size
    width = int(output.shape[1] * scale_percent / 100)
    height = int(output.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(output, dim, interpolation=cv2.INTER_AREA)

def findStatus(list):
    if len(list) == 0:
        return None

    if Status.DANGER in list:
        return Status.DANGER
    elif Status.WARNING in list:
        return Status.WARNING
    else:
        return Status.OK

def findStatusMin(list: list, num: int):
    if len(list) == 0:
        return None

    if Status.DANGER in list and list.count(Status.DANGER) >= num:
        return Status.DANGER
    elif Status.WARNING in list and list.count(Status.WARNING) >= num:
        return Status.WARNING
    else:
        return Status.OK


class VideoWriter:
    out = None
    def __init__(self, frameSize, fps):
        self.out = cv2.VideoWriter('output_video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), fps, frameSize)

    def write(self, img):
        self.out.write(img)

    def release(self):
        self.out.release()


