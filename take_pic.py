import time
import picamera
import picamera.array
import cv2
from final_functions import preprocess

cam = picamera.PiCamera()
# create references to the capture array and capture stream
# cam.start_preview()
cap = picamera.array.PiRGBArray(cam)
# wait for camera to warm up
time.sleep(2.0)
cam.capture(cap, format='bgr', use_video_port=True)
image = cap.array  # capture a frame
image = preprocess(image)
cv2.imwrite('pic1.jpg', image)
cap.truncate(0)  # reset capture array size to zero. effectively clears the array
