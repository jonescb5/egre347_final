import time
import motor

centroid_x = -1
res = (1280, 720)


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
