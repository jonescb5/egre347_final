import time
import picamera
import picamera.array
import cv2

cam = picamera.PiCamera()
# create references to the capture array and capture stream
# cam.start_preview()
cap = picamera.array.PiRGBArray(cam)

# wait for camera to warm up
time.sleep(2.0)

# DEBUG ITR
itr = 0

for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):

    image = frame.array  # capture a frame
    # do something with it
    print("frame got")
    # TESTING STUFF
    cv2.imwrite('cap' + str(itr) + '.jpg', image)

    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 5:
        exit()

    itr += 1
