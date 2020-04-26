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

    #preprocessing
    print("frame got")
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(image_hsv, gl, gh)
    image_mask = cv2.erode(image_mask, None, iterations=1)
    image_mask = cv2.dilate(image_mask, None, iterations=1)

    # find contours of the blob in the mask
    conto = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # calculate the moment of the image
    momnt = cv2.moments(conto)
    # calculated the centroid location of the blob from the moment from
    loc = (int(momnt["m10"] / momnt["m00"]), int(momnt["m01"] / momnt["m00"]))
    # TESTING STUFF
    cv2.imwrite('mask.jpg', image_mask)

    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 0:
        exit()

    itr += 1
