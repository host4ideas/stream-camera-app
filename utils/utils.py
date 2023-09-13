import cv2
import base64
from typing import Any
import numpy.typing as npt
from enum import Enum


class Args:
    '''Helper class for webrtc_server options'''
    cert_file = None
    '''SSL certificate file (for HTTPS)'''
    key_file = None
    '''SSL key file (for HTTPS)'''
    host = "0.0.0.0"
    '''Host for HTTP server (default: 0.0.0.0)'''
    port = 5938
    '''Port for HTTP server (default: 8080)'''
    verbose = False


def array_to_base64(frame: npt.NDArray[Any]):
    '''Helper function to encode a cv2 ndarray image to a base64 string'''
    _, img_encoded = cv2.imencode('.jpg', frame)
    return base64.b64encode(img_encoded)


Filter = Enum('Filter', ['BLUR', 'TEST'])
'''Enum with available filters for the user to use'''
