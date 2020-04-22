import time
import picamera
import picamera.array
import cv2

x_res = 1640
y_res = 922
fps = 40

cam = picamera.PiCamera()
# set camera parameters
cam.resolution(x_res, y_res)
cam.framerate = fps
# create references to the capture array and capture stream
cap = picamera.array.PiRGBArray(cam, size=(x_res, y_res))
cap_stream = cam.capture_continuous(cap, format="bgr", use_video_port=True)
# wait for camera to warm up
time.sleep(2.0)

# DEBUG ITR
itr = 0

for frame in cap_stream:

    image = frame.array  # capture a frame
    # do something with it

    # TESTING STUFF
    cv2.imwrite('cap' + itr + '.jpg', image)

    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 1:
        break

    ++itr
