import cv2
from cv2.typing import MatLike
from src.utils.utils import Filter, create_blank
from cvzone.SelfiSegmentationModule import SelfiSegmentation

segmentor = SelfiSegmentation()


def apply_filter(frame: MatLike, filter: Filter):
    match filter:
        case Filter.BLUR:
            return blur_background(frame)
        case Filter.COLOR:
            return 


def blur_background(frame: MatLike):
    filtered_frame = frame
    # Apply Blur filter through GaussianBlur
    filtered_frame = cv2.GaussianBlur(frame, (0, 0), 9)
    return segmentor.removeBG(frame, filtered_frame, cutThreshold=0.50)

def color_background(frame:MatLike, color: str):
    filtered_frame = frame
    # Apply Blur filter through GaussianBlur
    filtered_frame = create_blank()
    return segmentor.removeBG(frame, filtered_frame, cutThreshold=0.50)