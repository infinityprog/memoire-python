
def crop(img, object):
    ylength = ((object.ymax - object.ymin) / 10)
    xlength = ((object.xmax - object.xmin) / 10)
    ymin = int(object.ymin + ylength)
    ymax = int(object.ymax - ylength)
    xmin = int(object.xmin + xlength)
    xmax = int(object.xmax - xlength)
    print(object.ymin)
    print(object.ymax)
    print(ylength)
    print(ymin)
    print(ymax)
    # return img[int(object.ymin):int(object.ymax), int(object.xmin):int(object.xmax)] calculate all image
    return img[ymin:ymax, xmin:xmax]
