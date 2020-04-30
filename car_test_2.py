import motor
import time

speed = 75
turn_rate = 35

vehicle = motor.L298N()
vehicle.turn_l(speed, turn_rate)
time.sleep(3)
vehicle.stop_car()
vehicle.shutdown()



