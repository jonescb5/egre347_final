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

# DEBUG ITR
itr = 0

for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):

    image = frame.array  # capture a frame
    # do something with it

    #preprocessing
    image_mask = preprocess(image)
    print("frame got")


    # find contours of the blob in the mask
    conto = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # calculate the moment of the image
    momnt = cv2.moments(conto)
    # calculated the centroid location of the blob from the moment from
    coord = (int(momnt["m10"] / momnt["m00"]), int(momnt["m01"] / momnt["m00"]))
    # TESTING STUFF
    print(coord)
    cv2.imwrite('mask.jpg', image_mask)

    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 0:
        exit()

    itr = itr + 1
