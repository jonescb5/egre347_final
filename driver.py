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
# Description: Defines functions used in threads for target acquisition and vehicle control
#
# Dependencies: image_processing.py, motor.py
#
# ******************************************************************

import time
import motor
import image_processing
import picamera
import picamera.array

centroid_x = -1
res = (1280, 720)


def image_processor(col):
    """
    Captures and processes frames of the RPi Video Feed

    This function is designed to run as a daemon thread.
    The function takes a character argument 'R', 'G', or 'B'
    which selects the color of the target. The function initializes,
    and runs a video capture from the Pi camera. It calculates the
    coordinate of the selected target within the frame of video and
    outputs it to a global variable which is accessed by the vehicle_control
    function. The function loops while the RPi camera provides a video feed.

    Parameters:
    col (string): accepts 'R', 'G', or 'B'

    Returns:
    N/A
    * fills and updates global variable: centroid_x

    """

    global centroid_x
    global res
    global ready_flag
    # Initialize PiCamera object as cam
    cam = picamera.PiCamera()
    # Set resolution
    cam.resolution = res
    # Set frame rate
    cam.framerate = 90
    # create references to the capture array and capture stream
    cap = picamera.array.PiRGBArray(cam, size=res)
    # Start camera to let it adjust
    cam.start_preview()
    # wait for camera to warm up
    time.sleep(2.0)

    print("starting image_processing")
    # Capture video one frame at a time while the RPi continues to provide a video feed
    for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):
        # pull a frame from the capture stream
        image = frame.array
        # pass the image to the find_find centroid function to be processed
        # and output as the x, y coordinates of the centroid of the target
        centroid = image_processing.find_centroid(image, col)
        # select only the x value of the coordinate and update the
        # global variable centroid_x
        centroid_x = centroid[0]
        cap.truncate(0)  # reset capture array size to zero. effectively clears the array


def vehicle_control():
    """
    Controls the vehicle movement based on the coordinate provided by the image_processor daemon

    This function checks the global variable centroid_x in order to guide the vehicle to the target.
    This function runs as the main thread responding changes in the position of the target (global variable centroid_x).
    It initalizes the vehicle and then loops checking the position of the target. It is an FSM which searches for a
    when none has been detected. When one is detected it compares it's location within the frame and adjusts the
    vehicle's course towards the target.

    Parameters:
    This function takes no input arguments.
    It is reliant on global variables:
    res (resolution of the camera)
    centroid_x (the x coordinate of the target)

    Returns:
    N/A

    """

    global centroid_x
    global res
    global ready_flag
    # the frame is divided into sections dependent on the camera's resolution
    lat_l = 2*(res[0]/5)
    lat_r = 3*lat_l
    # the motor driver object is initialized as 'vehicle'
    vehicle = motor.L298N()
    # wait for controller to warm up
    time.sleep(5)
    print("Starting vehicle_control")

    try:
        # set speed and turn rate
        speed = 75
        turn_rate = 35

        while True:
            # The x coordinate is defined as -1 if no target was found
            # if that is the case the vehicle is in the 'search' state
            if centroid_x < 0:
                vehicle.rotate_r(75)
                time.sleep(0.05)
                vehicle.rotate_l(25)
                time.sleep(0.05)
                vehicle.stop_car()
            # if the x coordinate is greater than zero then a target has been found.
            elif centroid_x >= 0:
                # If a target has been found then check the x coordinate against the bounds
                # of the image frame.

                # If the target is in the left hand portion of the frame turn left
                if centroid_x <= lat_l:
                    vehicle.turn_l(speed, turn_rate)

                # If the target is in the right hand portion of the frame turn right
                elif centroid_x >= lat_r:
                    vehicle.turn_r(speed, turn_rate)

                # If the target is in the center of the frame go straight forward
                elif lat_l < centroid_x < lat_r:
                    vehicle.forward(speed)

    # A try-except block was added to allow for clean shutdown when a keyboard interrupt (^C) was issued
    except KeyboardInterrupt:
        # In this case the GPIO used for the motor driver is de-allocated
        vehicle.shutdown()
