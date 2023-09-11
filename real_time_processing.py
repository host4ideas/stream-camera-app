# importing required libraries
import cv2
import time
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from webcam_stream import WebcamStream
from utils import BackgroundFilter, array_to_base64


class RealTimeProcessing:
    def __init__(self, webcam_stream: WebcamStream, bg_filter=BackgroundFilter.BLUR):
        self.__current_bg_filter = bg_filter
        self.__segmentor = SelfiSegmentation()
        self.webcam_stream = webcam_stream
        self.current_base64_frame = ""

    def set_current_bg_filter(self, bg_filter: BackgroundFilter):
        self.__current_bg_filter = bg_filter

    def get_current_bg_filter(self):
        return self.__current_bg_filter

    def frame_processing(self, frame):
        filtered_frame = frame
        # Apply Blur filter through GaussianBlur
        if self.__current_bg_filter == BackgroundFilter.BLUR:
            filtered_frame = cv2.GaussianBlur(frame, (0, 0), 9)
        return self.__segmentor.removeBG(frame, filtered_frame, cutThreshold=0.50)

    def stop(self):
        self.webcam_stream.stopped = True

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
            self.current_base64_frame = array_to_base64(frame)

            num_frames_processed += 1

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        end = time.time()
        self.webcam_stream.stop()  # stop the webcam stream

        # printing time elapsed and fps
        elapsed = end-start
        fps = num_frames_processed/elapsed
        print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(
            fps, elapsed, num_frames_processed))

        # closing all windows
        cv2.destroyAllWindows()
