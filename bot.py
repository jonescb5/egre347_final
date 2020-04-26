import time
import picamera
import picamera.array
import cv2

gl = (29, 86, 6)
gh = (64, 255, 255)

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
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(image_hsv, gl, gh)


    # TESTING STUFF
    cv2.imwrite('mask.jpg', image_mask)

    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 0:
        exit()

    itr += 1
