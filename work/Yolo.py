import torch
import numpy as np
import json

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def findObject(img):
    return model(img)


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
