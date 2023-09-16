import cv2
import flet as ft
from typing import Any
import numpy.typing as npt
from src.utils.helpers import array_to_base64, Filter
from src.utils.background_filters import blur_background


class CameraImage(ft.UserControl):
    def __init__(self, current_filter: Filter):
        super().__init__()

        self.webcam_stopped = True

        # Default black image
        self.camera_img_default = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

        # Declare Image component to show camera capture
        self.img_camera = ft.Image(
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            src_base64=self.camera_img_default
        )

        self.current_filter = current_filter

    def handle_frame_change(self, frame: npt.NDArray[Any]):
        self.img_camera.src_base64 = array_to_base64(frame)
        self.update()

    def stop_streaming(self):
        self.webcam_stopped = True

    def start_streaming(self):
        if self.webcam_stopped == True:
            self.webcam_stopped = False
            vcap = cv2.VideoCapture(0)
            while True:
                if vcap.isOpened() is False:
                    print("[Exiting]: Error accessing webcam stream.")
                    break
                if self.webcam_stopped == True:
                    self.img_camera.src_base64 = self.camera_img_default
                    self.update()
                    break
                grabbed, frame = vcap.read()
                frame = blur_background(frame)
                if grabbed is False:
                    print('[Exiting] No more frames to read')
                    break
                self.handle_frame_change(frame)
            vcap.release()

    def build(self):
        return self.img_camera
