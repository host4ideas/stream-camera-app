import cv2
import base64
from typing import Any
import numpy.typing as npt
from enum import Enum
from aiohttp import web
import numpy as np


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


class RTCOfferRequest(web.Request):
    '''Helper class for POST request to /offer'''

    def __init__(self, sdp: str, type: str, video_transform: str):
        super().__init__()  # don't forget this to inherit from MediaStreamTrack!
        self.sdp = sdp
        self.type = type
        self.video_transform = video_transform


def array_to_base64(frame: npt.NDArray[Any]):
    '''Helper function to encode a cv2 ndarray image to a base64 string'''
    _, img_encoded = cv2.imencode('.jpg', frame)
    return base64.b64encode(img_encoded).decode()


def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


Filter = Enum('Filter', ['BLUR', 'COLOR', 'IMAGE'])
'''Enum with available filters for the user to use'''
