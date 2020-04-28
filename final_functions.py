import cv2


def preprocess(image):
    """does image preprocessing"""
    # format (H, S, V)
    # H values 0 to 180
    # S & V values 0 to 255
    rlpos = (0, 115, 90)
    rhpos = (10, 255, 255)
    rlneg = (170, 115, 90)
    rhneg = (180, 255, 255)
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)
    image_mask1 = cv2.inRange(image_hsv, rlpos, rhpos)
    image_mask2 = cv2.inRange(image_hsv, rlneg, rhneg)
    image_mask0 = image_mask1 + image_mask2
    image_mask = cv2.erode(image_mask0, None, iterations=3)
    image_mask = cv2.dilate(image_mask, None, iterations=2)

    return image_mask


def find_centroid(im):
    # preprocessing
    im_mask = preprocess(im)
    try:
        # find contours of the blob in the mask
        all_contours = (cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))[1]
        biggest_contour = max(all_contours, key=cv2.contourArea)
        # calculate the moment of the biggest contour
        contour_moments = cv2.moments(biggest_contour)
        # calculated the centroid location of the blob from the moment from
        centroid_x = int(contour_moments["m10"] / contour_moments["m00"])
        centroid_y = int(contour_moments["m01"] / contour_moments["m00"])

        return centroid_x, centroid_y

    except ValueError:
        return False

