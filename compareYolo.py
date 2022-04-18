import sys
import torch
import timeit
from datetime import datetime
# Model
model = torch.hub.load('ultralytics/yolov5', sys.argv[1])  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = 'data/images/yolo_compare.jpg'  # or file, Path, PIL, OpenCV, numpy, list

print(datetime.now())
start = timeit.default_timer()
# Inference
results = model(img)
stop = timeit.default_timer()
print(datetime.now())

# Results
results.save(save_dir='result/images/' + sys.argv[1])
fichier = open("result/images/"+sys.argv[1]+"/result.txt", "a")
fichier.write(sys.argv[1] + ' : ' + str(stop - start) + 's')
fichier.close()
print(str(stop - start) + 's')
