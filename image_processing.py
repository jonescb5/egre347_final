# ******************************************************************
# Program: bot.py
#
# Programmer: Christopher Jones
#
# Due Date: April 30, 2020
#
# EGRE 347, Spring 2020       Instructor: Robert Klenke
#
# Pledge: I have neither given nor received unauthorized aid on this program.
#
# Description: Defines image processing functions for target acquisition using the openCV library
#
# ******************************************************************
import cv2

# The x coordinate of the centroid (global variable) initialized to -1 signifying
# that object was found
centroid_x = -1
# the resolution initialized to the default
res = (1280, 720)

# Dictionaries of the HSV values of the targets. This is done for easy calibration and tuning.
# Lighting conditions easily effect these values. An auto calibration sequence COULD be implemented.
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
    """
    Creates a discriminatory image mask for a given color target

    This function takes a BGR image and creates a binary image mask for the given color of the target.
    Basic preprocessing functions are used to optimize the image mask for target detection. This function returns a
    raw mask of the image whether there is a target or not. Given the arguments 'image' and 'color' it masks out all
    pixels that do not match the range specified by the color dictionaries turning them to black. Those pixels which
    are acceptable appear in white. If a target of the specified color range is not present in the frame the
    function will return an entirely black image mask.

    Parameters:
    image (BGR image): a raw capture from the RPi camera module
    color (string): selects the color of the target. Accepts "B", "G", or "R"

    Returns:
    N/A

    """

    # Blur the image to soften sharp details
    image_blur = cv2.GaussianBlur(image, (11, 11), 0)
    # Convert the image to the HSV color space
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)

    # The image mask is constructed in different ways depending on the color we are masking for.
    if color == "B":
        # The inRange function takes a upper and lower value for the HSV color space which
        # will be used to cut all other colors out of the image.
        b_l = (int(blue['H_low'] / 2), int(blue['S_low'] * 2.55), int(blue['V_low'] * 2.55))
        b_h = (int(blue['H_high'] / 2), int(blue['S_high'] * 2.55), int(blue['V_high'] * 2.55))
        # The inRange function returns a binary image with white representing the specified color range
        # and black as dead space.
        image_mask = cv2.inRange(image_hsv, b_l, b_h)
    elif color == "G":
        # A dictionary of the values for each color are used to provide the proper ranges.
        # The HSV color space is represented as Hue in degrees and Saturation and Value as percentages.
        # The inRange function accepts Hue values from 0 to 180 and Saturation and Value values from 0 to 255
        # so the values are converted before they are handed to the function
        g_l = (int(green['H_low']/2), int(green['S_low'] * 2.55), int(green['V_low'] * 2.55))
        g_h = (int(green['H_high']/2), int(green['S_high'] * 2.55), int(green['V_high'] * 2.55))
        image_mask = cv2.inRange(image_hsv, g_l, g_h)
    elif color == "R":
        # Red encompasses both sides of 0 degrees so two masks must be made and summed,
        # one from 'x' to 360 degrees and one from 0 to 'y' degrees.
        rlpos = (0, int(red['S_low'] * 2.55), int(red['V_low'] * 2.55))
        rhpos = (int(red['H_high'] / 2), int(red['S_high'] * 2.55), int(red['V_high'] * 2.55))
        rlneg = (int(red['H_low'] / 2), int(red['S_low'] * 2.55), int(red['V_low'] * 2.55))
        rhneg = (180, int(red['S_high'] * 2.55), int(red['V_high'] * 2.55))
        # create both masks
        image_mask1 = cv2.inRange(image_hsv, rlpos, rhpos)
        image_mask2 = cv2.inRange(image_hsv, rlneg, rhneg)
        # sum them to the final mask
        image_mask = image_mask1 + image_mask2
    # The mask is then eroded which essentially blurs the black into the edges of a white space
    # closing up any small voids that were left from the inRange function
    image_mask = cv2.erode(image_mask, None, iterations=2)
    # Dilation does the opposite and recedes and sharpens the borders of the white spaces that are left
    image_mask = cv2.dilate(image_mask, None, iterations=2)
    # These processes are resource intensive and the iterations should be limited in order to keep low
    # process times.

    return image_mask


def find_centroid(im, color):
    """
    Returns the x, y coordinates of the centroid of a target of the selected color

    This function utilizes the preprocessing function to make a mask then finds the largest object within
    the mask. The moment of the image is calculated and the x, y coordinates of the target's centroid are returned.

    Parameters:
    im (BGR image): a raw capture from the RPi camera module
    color (string): selects the color of the target. Accepts "B", "G", or "R"

    Returns:
    N/A

    """

    # Input image is first put through pre-processing to create a binary image mask isolating the target
    im_mask = preprocess(im, color)
    # The contours of the image are calculated by the findContours function. This finds the all of the border lines
    # around the blobs created by the preprocess function.
    all_contours = (cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))[1]
    # Make sure that a target was identified through pre-processing; If there was no target within the range that we
    # are looking for the image will be black and no contours will be found
    if len(all_contours) > 0:
        # We find the biggest contour within the set found and assume that it is the target
        biggest_contour = max(all_contours, key=cv2.contourArea)
        # We then calculate the moments of the polygonal contour we selected
        contour_moments = cv2.moments(biggest_contour)
        # We then take the first moment of x and divide it by the area ('m00')
        # We do the same for y
        x = int(contour_moments["m10"] / contour_moments["m00"])
        y = int(contour_moments["m01"] / contour_moments["m00"])
        # Since we are working with a polygon this gives the x and y coordinates of the
        # centroid within the image, in pixels
        # this coordinate is relative to the resolution of the image
        return x, y

    else:
        return -1, -1



