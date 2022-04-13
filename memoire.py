import cv2
from work.DepthEstimation import depthEstimation


img = cv2.imread('not_good.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

output = depthEstimation(img)
output = cv2.applyColorMap(output, cv2.COLORMAP_MAGMA)

scale_percent = 40 # percent of original size
width = int(output.shape[1] * scale_percent / 100)
height = int(output.shape[0] * scale_percent / 100)
dim = (width, height)

output = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)

while True:

    cv2.imshow('Image', output)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

