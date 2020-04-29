import cv2
import picamera
import picamera.array
import time


centroid_x = -1
res = (1280, 720)


def preprocess(image, color):
    """does image preprocessing"""
    # format (H, S, V)
    # H values 0 to 180
    # S & V values 0 to 255
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)

    if color == "red":
        rlpos = (0, 115, 90)
        rhpos = (10, 255, 255)
        rlneg = (170, 115, 90)
        rhneg = (180, 255, 255)
        image_mask1 = cv2.inRange(image_hsv, rlpos, rhpos)
        image_mask2 = cv2.inRange(image_hsv, rlneg, rhneg)
        image_mask = image_mask1 + image_mask2
    elif color == "blue":
        blpos = (80, 80, 80)
        bhpos = (130, 255, 255)
        image_mask = cv2.inRange(image_hsv, blpos, bhpos)

    image_mask = cv2.erode(image_mask, None, iterations=2)
    image_mask = cv2.dilate(image_mask, None, iterations=2)

    return image_mask


def find_centroid(im, color):
    """find the centroid"""
    im_mask = preprocess(im, color)
    # find contours of the blob in the mask
    all_contours = (cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))[1]
    if len(all_contours) > 0:
        biggest_contour = max(all_contours, key=cv2.contourArea)
        # calculate the moment of the biggest contour
        contour_moments = cv2.moments(biggest_contour)
        # calculated the centroid location of the blob from the moment from
        x = int(contour_moments["m10"] / contour_moments["m00"])
        y = int(contour_moments["m01"] / contour_moments["m00"])
        return x, y

    else:
        return -1, -1


def image_processing():

    global centroid_x
    global res
    cam = picamera.PiCamera()
    cam.resolution = res
    cam.framerate = 90
    # create references to the capture array and capture stream
    # cam.start_preview()
    cap = picamera.array.PiRGBArray(cam, size=res)
    # wait for camera to warm up
    time.sleep(2.0)

    for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):
        image = frame.array  # capture a frame
        # do something with it
        centroid = find_centroid(image, "blue")
        centroid_x = centroid[0]

        cap.truncate(0)  # reset capture array size to zero. effectively clears the array


