import time
import picamera
import picamera.array
import final_functions
import motor
import threading


state = "SEARCH"
centroid = (0, 0)


def go():
    global state
    global centroid
    lat_l = 426
    lat_r = 854
    vehicle = motor.car()
    while True:

        if ~centroid:
            vehicle.search()
            state = "SEARCH"
            print("search")

        elif centroid:
            centroid_x = centroid[0]
            if state == "SEARCH":
                # vehicle.forward()
                state = "LOCK_ON"

            if state == "LOCK_ON":
                print("lock on")

                if centroid_x <= lat_l:
                    vehicle.turn_l()
                elif centroid_x >= lat_r:
                    vehicle.turn_r()
                elif lat_l < centroid_x < lat_r:
                    vehicle.stop_car()
                    print("gotteem")


def get_loc():

    global centroid
    cam = picamera.PiCamera()
    # create references to the capture array and capture stream
    cap = picamera.array.PiRGBArray(cam)
    # wait for camera to warm up
    time.sleep(2.0)

    for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):
        image = frame.array  # capture a frame
        # do something with it
        centroid = final_functions.find_centroid(image)

        cap.truncate(0)  # reset capture array size to zero. effectively clears the array


loc = threading.Thread(target=get_loc())
movement = threading.Thread(target=go())
print("starting loc")
loc.start()
print("starting movement")
movement.start()


