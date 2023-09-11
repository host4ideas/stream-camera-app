import cv2
import base64
from typing import Any
import numpy.typing as npt
from enum import Enum


def array_to_base64(frame: npt.NDArray[Any]):
    '''Helper function to encode a cv2 ndarray image to a base64 string'''
    _, img_encoded = cv2.imencode('.jpg', frame)
    return base64.b64encode(img_encoded)


Filter = Enum('Filter', ['BLUR', 'TEST'])
'''Enum with available filters for the user to use'''
