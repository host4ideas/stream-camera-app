"""timeout_req_ImageSender.py -- show use of ZMQ timeout options for restarts

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream. Images are jpg compressed before sending.

One of the issues with the REQ/REP messaging pattern is that the sending program
will stall if the receiving program is stopped and restarted. This example
program show one way to use ZMQ options to restart the sender when that happens.

This image sending program uses the REQ/REP messaging pattern. It demonstrates
one way to deal with a failure to receive a REP after a REQ is sent. If the
receiving program restarts, this sending program will automatically restart.

Use with the 'with_ImageHub.py' program to receive the images on the Mac. Brief
test instructions are in that program: with_ImageHub.py. Stop the
'with_ImageHub' program and restart it. It should resume receiving images after
it is restarted.

"""

# https://github.com/jeffbass/imagezmq/blob/master/examples/timeout_req_ImageSender.py

import sys
import zmq  # needed because we will be using zmq socket options & exceptions
import time
import socket
import imagezmq
import simplejpeg
import traceback
from time import sleep
from imutils.video import VideoStream


def sender_start(connect_to=None):
    sender = imagezmq.ImageSender(connect_to=connect_to)
    sender.zmq_socket.setsockopt(zmq.LINGER, 0)  # prevents ZMQ hang on exit
    # NOTE: because of the way PyZMQ and imageZMQ are implemented, the
    #       timeout values specified must be integer constants, not variables.
    #       The timeout value is in milliseconds, e.g., 2000 = 2 seconds.
    sender.zmq_socket.setsockopt(zmq.RCVTIMEO, 2000)  # set a receive timeout
    sender.zmq_socket.setsockopt(zmq.SNDTIMEO, 2000)  # set a send timeout
    return sender


# use either of the formats below to specifiy address of display computer
# connect_to='tcp://jeff-macbook:5555'
# connect_to='tcp://192.168.1.190:5555'
connect_to = 'tcp://192.168.0.19:5555'
sender = sender_start(connect_to)

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = VideoStream().start()
time.sleep(2.0)  # allow camera sensor to warm up
time_between_restarts = 5  # number of seconds to sleep between sender restarts
jpeg_quality = 85  # 0 to 100, higher is better quality, 95 is cv2 default
try:
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        jpg_buffer = simplejpeg.encode_jpeg(image, quality=jpeg_quality,
                                            colorspace='BGR', fastdct=True)
        try:
            reply_from_mac = sender.send_jpg(rpi_name, jpg_buffer)
        except (zmq.ZMQError, zmq.ContextTerminated, zmq.Again):
            if 'sender' in locals():
                print('Closing ImageSender.')
                sender.close()
            sleep(time_between_restarts)
            print('Restarting ImageSender.')
            sender = sender_start(connect_to)
except (KeyboardInterrupt, SystemExit):
    pass  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    if 'sender' in locals():
        sender.close()
    picam.stop()  # stop the camera thread
    sys.exit()
