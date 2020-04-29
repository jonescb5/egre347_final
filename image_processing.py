import cv2


centroid_x = -1
res = (1280, 720)
green = {
        'H_low': 100, 'S_low': 20, 'V_low': 10,
        'H_high': 200, 'S_high': 100, 'V_high': 100
        }

blue = {
        'H_low': 200, 'S_low': 20, 'V_low': 10,
        'H_high': 240, 'S_high': 100, 'V_high': 100
        }

red = {
        'H_low': 300, 'S_low': 30, 'V_low': 10,
        'H_high': 20, 'S_high': 100, 'V_high': 100
        }


def preprocess(image, color):
    """does image preprocessing"""
    # format (H, S, V)
    # H values 0 to 180
    # S & V values 0 to 255
    global green
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)

    if color == "R":
        rlpos = (0, int(red['S_low'] * 2.55), int(red['V_low'] * 2.55))
        rhpos = (int(red['H_high'] / 2), int(red['S_high'] * 2.55), int(red['V_high'] * 2.55))
        rlneg = (int(red['H_low'] / 2), int(red['S_low'] * 2.55), int(red['V_low'] * 2.55))
        rhneg = (180, int(red['S_high'] * 2.55), int(red['V_high'] * 2.55))
        image_mask1 = cv2.inRange(image_hsv, rlpos, rhpos)
        image_mask2 = cv2.inRange(image_hsv, rlneg, rhneg)
        image_mask = image_mask1 + image_mask2
    elif color == "B":
        b_l = (int(blue['H_low'] / 2), int(blue['S_low'] * 2.55), int(blue['V_low'] * 2.55))
        b_h = (int(blue['H_high'] / 2), int(blue['S_high'] * 2.55), int(blue['V_high'] * 2.55))
        image_mask = cv2.inRange(image_hsv, b_l, b_h)
    elif color == "G":
        g_l = (int(green['H_low']/2), int(green['S_low'] * 2.55), int(green['V_low'] * 2.55))
        g_h = (int(green['H_high']/2), int(green['S_high'] * 2.55), int(green['V_high'] * 2.55))
        image_mask = cv2.inRange(image_hsv, g_l, g_h)

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



