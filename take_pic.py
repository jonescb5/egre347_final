import time
import picamera
import picamera.array
import cv2
import image_processing

res = (1280, 720)

cam = picamera.PiCamera()
# create references to the capture array and capture stream
cam.start_preview()
cap = picamera.array.PiRGBArray(cam)
# wait for camera to warm up
time.sleep(2.0)
cam.capture(cap, format='bgr', use_video_port=True)
image = cap.array  # capture a frame
image_mask = image_processing.preprocess(image, "blue")
centroid = image_processing.find_centroid(image, "blue")
print(centroid)
cv2.imwrite('image.jpg', image)
cv2.circle(image, centroid, 5, (0, 255, 0), 1)
cv2.imwrite('cent_image.jpg', image)
cv2.imwrite('image_mask.jpg', image_mask)
cap.truncate(0)  # reset capture array size to zero. effectively clears the array
