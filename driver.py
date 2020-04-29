import time
import motor
import image_processing
import picamera


centroid_x = -1
res = (1280, 720)

def image_processor(col):

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
        centroid = image_processing.find_centroid(image, col)
        centroid_x = centroid[0]

        cap.truncate(0)  # reset capture array size to zero. effectively clears the array



def vehicle_control():
    """fsm"""

    global centroid_x
    global res
    lat_l = 2*(res[0]/5)
    lat_r = 3*lat_l
    vehicle = motor.L298N()
    try:
        speed = 75
        turn_rate = 50

        while True:

            if centroid_x < 0:
                vehicle.rotate_r(75)
                time.sleep(0.1)
                vehicle.rotate_l(25)
                time.sleep(0.05)
                vehicle.stop_car()

            elif centroid_x >= 0:

                if centroid_x <= lat_l:
                    vehicle.turn_l(speed, turn_rate)
                    print("left")
                elif centroid_x >= lat_r:
                    vehicle.turn_r(speed, turn_rate)
                    print("right")
                elif lat_l < centroid_x < lat_r:
                    vehicle.forward(speed)
                    print("forward")
    except KeyboardInterrupt:
        vehicle.shutdown()
