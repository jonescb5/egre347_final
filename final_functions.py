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