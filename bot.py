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
    all_contours = (cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))[1]
    biggest_contour = max(all_contours, key=cv2.contourArea)
    # calculate the moment of the biggest contour
    contour_moments = cv2.moments(biggest_contour)
    # calculated the centroid location of the blob from the moment from
    centroid_x = int(contour_moments["m10"] / contour_moments["m00"])
    centroid_y = int(contour_moments["m01"] / contour_moments["m00"])
    # TESTING STUFF
    print(centroid_x)
    print(centroid_y)
    cv2.circle(image, (centroid_x, centroid_y), 10, (0, 255, 0), 10)
    cv2.imwrite('cent.jpg', image)
    cap.truncate(0)  # reset capture array size to zero. effectively clears the array

    if itr == 0:
        exit()

    itr = itr + 1
