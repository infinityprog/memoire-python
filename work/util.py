import cv2
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


class VideoWriter:
    out = None
    def __init__(self, frameSize, fps):
        self.out = cv2.VideoWriter('output_video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), fps, frameSize)

    def write(self, img):
        self.out.write(img)

    def release(self):
        self.out.release()


