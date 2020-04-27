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
cam.capture_continuous(cap, format='bgr', use_video_port=True)
image = cap.array  # capture a frame
cv2.imwrite('pic.jpg', image)
cap.truncate(0)  # reset capture array size to zero. effectively clears the array
