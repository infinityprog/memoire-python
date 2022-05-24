import cv2

from work.DepthCalculation import Status

def crop(img, object):
    return img[int(object.ymin):int(object.ymax), int(object.xmin):int(object.xmax)]

def drawBoundingBox(img, label, object):
    start_point = (int(object.xmin), int(object.ymin))
    end_point = (int(object.xmax), int(object.ymax))
    color = (0, 0, 255)
    img = cv2.rectangle(img, start_point, end_point, color, 2)
    img = cv2.rectangle(img, (int(object.xmin), int(object.ymin) - 20 ), (int(object.xmax), int(object.ymin)), color, -1)
    return cv2.putText(img, label, (int(object.xmin), int(object.ymin) - 5) ,cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)


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


