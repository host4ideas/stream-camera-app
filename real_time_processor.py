# importing required libraries
import cv2
import time
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from webcam_stream import WebcamStream
from utils.utils import Filter
from typing import Callable, Any
import numpy.typing as npt


class RealTimeProcessor:
    '''Helper class to process video frames in real time by applying background filters'''

    def __init__(self, on_frame_change: Callable[[npt.NDArray[Any]], npt.NDArray[Any]], webcam_stream: WebcamStream, bg_filter=Filter.BLUR):
        self.__current_bg_filter = bg_filter
        self.__segmentor = SelfiSegmentation()
        self.webcam_stream = webcam_stream
        self.on_frame_change = on_frame_change

    def set_current_bg_filter(self, bg_filter: Filter):
        self.__current_bg_filter = bg_filter

    def frame_processing(self, frame):
        filtered_frame = frame
        # Apply Blur filter through GaussianBlur
        if self.__current_bg_filter == Filter.BLUR:
            filtered_frame = cv2.GaussianBlur(frame, (0, 0), 9)
        return self.__segmentor.removeBG(frame, filtered_frame, cutThreshold=0.50)

    def stop(self):
        self.webcam_stream.stop()

    def start(self):
        # If it was stopped, start again
        if self.webcam_stream.stopped is True:
            self.webcam_stream.stopped = False

        # processing frames in input stream
        num_frames_processed = 0
        start = time.time()
        while True:
            if self.webcam_stream.stopped is True:
                break
            else:
                frame = self.webcam_stream.read()

            # Frame processing
            frame = self.frame_processing(frame)
            self.on_frame_change(frame=frame)

            num_frames_processed += 1

            # cv2.imshow('frame', frame)
            # key = cv2.waitKey(1)
            # if key == ord('q'):
            #     break
        end = time.time()
        self.webcam_stream.stop()  # stop the webcam stream

        # printing time elapsed and fps
        elapsed = end-start
        fps = num_frames_processed/elapsed
        print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(
            fps, elapsed, num_frames_processed))

        # closing all windows
        # cv2.destroyAllWindows()
