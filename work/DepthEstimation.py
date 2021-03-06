import cv2
import numpy as np
import torch

# model_type = "DPT_Large"  # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
# model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

midas = torch.hub.load("intel-isl/MiDaS", model_type)
# torch.save(midas, 'midas-small.pt')
# midas

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform


def depthEstimation(img):
    imgWithDeep = depthEstimationPur(img)

    imgWithDeep = cv2.normalize(imgWithDeep, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    return (imgWithDeep * 255).astype(np.uint8)

def depthEstimationPur(img):
    input_batch = transform(img).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    # return prediction.cpu().numpy()
    return prediction.cpu().numpy()

def normalizeDepthMap(depthmap):
    imgWithDeep = cv2.normalize(depthmap, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    return (imgWithDeep * 255).astype(np.uint8)
