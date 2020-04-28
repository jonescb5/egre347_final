import time
import picamera
import picamera.array
import final_functions
import motor

vehicle = motor.car()
cam = picamera.PiCamera()
# create references to the capture array and capture stream
# cam.start_preview()
cap = picamera.array.PiRGBArray(cam)

# wait for camera to warm up
time.sleep(2.0)
try:
    for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):

        image = frame.array  # capture a frame
        # do something with it
        centroid = final_functions.find_centroid(image)
        if centroid:
            print("target acquired")
            vehicle.forward()
        else:
            print("no target")
            vehicle.rotate_r()

        cap.truncate(0)  # reset capture array size to zero. effectively clears the array

except KeyboardInterrupt:
    vehicle.shutdown_car()


