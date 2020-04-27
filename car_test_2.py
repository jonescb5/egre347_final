from motor import car
import time

vehicle = car()
while True:
    vehicle.rotate_r()
    time.sleep(3)
    vehicle.rotate_l()
    time.sleep(3)


