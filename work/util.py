
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
