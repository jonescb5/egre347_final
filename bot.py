import time
import picamera
import picamera.array
import cv2

with picamera as camera:
    # start camera
    camera.start_preview()
    # wait for the camera to get going
    time.sleep(2.0)

    while True:
        # get frame from camera

        #
