from motor import car
import time

vehicle = car()
time.sleep(3)
vehicle.forward()
time.sleep(3)
vehicle.stop_car()
time.sleep(3)
vehicle.rotate_l()
time.sleep(3)
vehicle.rotate_r()
time.sleep(3)
vehicle.reverse()
time.sleep(3)
vehicle.shutdown_car()

