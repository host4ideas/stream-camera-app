# importing required libraries
import cv2
import time
from threading import Thread  # library for implementing multi-threaded processing
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

segmentor = SelfiSegmentation()

# defining a helper class for implementing multi-threaded processing


class WebcamStream:
    def __init__(self, stream_id=0):
        self.stream_id = stream_id   # default is 0 for primary camera

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of webcam hardware/input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)

        # self.stopped is set to False when frames are being read from self.vcap stream
        self.stopped = True

        # reference to the thread for reading next available frame from input stream
        self.t = Thread(target=self.update, args=())
        # daemon threads keep running in the background while the program is executing
        self.t.daemon = True

    # method for starting the thread for grabbing next available frame in input stream
    def start(self):
        self.stopped = False
        self.t.start()

    # method for reading next frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # method for returning latest read frame
    def read(self):
        return self.frame

    # method called to stop reading frames
    def stop(self):
        self.stopped = True


def frame_processing(frame):
    filtered_frame = cv2.GaussianBlur(frame, (0, 0), 9)
    return segmentor.removeBG(frame, filtered_frame, cutThreshold=0.50)


# initializing and starting multi-threaded webcam capture input stream
# stream_id = 0 is for primary camera
webcam_stream = WebcamStream(stream_id=0)
webcam_stream.start()

# processing frames in input stream
num_frames_processed = 0
start = time.time()
while True:
    if webcam_stream.stopped is True:
        break
    else:
        frame = webcam_stream.read()

    # Frame processing
    frame = frame_processing(frame)

    num_frames_processed += 1

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
end = time.time()
webcam_stream.stop()  # stop the webcam stream

# printing time elapsed and fps
elapsed = end-start
fps = num_frames_processed/elapsed
print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(
    fps, elapsed, num_frames_processed))

# closing all windows
cv2.destroyAllWindows()
