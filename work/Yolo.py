import torch
import numpy as np
import json

# Model
# model = torch.hub.load('.', 'custom', path='yolov5hc.pt', source='local', force_reload=True)  # custom model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5L.pt', force_reload=True)

class Yolo:

    model = None

    def __init__(self, name):
        self.model = torch.hub.load('ultralytics/yolov5', name)

    def findObject(self, img):
        return self.model(img)


class Object:
    def __init__(self, xmin, ymin, xmax, ymax, confidence, name):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.confidence = confidence
        self.name = name


def jsonToObject(modelResult):
    objects = json.loads(modelResult.pandas().xyxy[0].to_json(orient="records"))
    for value in objects:
        value.pop('class', None);
    return objects
