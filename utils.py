import cv2
import base64
from numpy import ndarray
from enum import Enum


def array_to_base64(frame: ndarray):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer)


BackgroundFilter = Enum('BackgroundFilter', ['BLUR'])
