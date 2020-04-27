import RPi.GPIO as gpio

class car:
    def __init__(self):
        self.ena = 12
        self.in1 = 5
        self.in2 = 6
        self.enb = 13
        self.in3 = 20
        self.in4 = 21
        self.PWMf = 1000
        self.speed = 0
        self.turn_rate = 50
        gpio.setmode(gpio.BCM)
        gpio.setup(self.ena, gpio.OUT)
        gpio.setup(self.in1, gpio.OUT)
        gpio.setup(self.in2, gpio.OUT)
        gpio.setup(self.enb, gpio.OUT)
        gpio.setup(self.in3, gpio.OUT)
        gpio.setup(self.in4, gpio.OUT)
        self.spa = gpio.PWM(self.ena, self.PWMf)
        self.spb = gpio.PWM(self.enb, self.PWMf)
        self.spa.start(self.speed)
        self.spb.start(self.speed)


    def forward(self):

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.HIGH)
        gpio.output(self.in3, gpio.HIGH)
        gpio.output(self.in4, gpio.LOW)
        self.spa.ChangeDutyCycle(self.speed)
        self.spb.ChangeDutyCycle(self.speed)
        print("forward")
        return

    def reverse(self):

        gpio.output(self.in1, gpio.HIGH)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.spa.ChangeDutyCycle(self.speed)
        self.spb.ChangeDutyCycle(self.speed)
        print("reverse")
        return

    def rotate_r(self):

        gpio.output(self.in1, gpio.HIGH)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.HIGH)
        gpio.output(self.in4, gpio.LOW)
        self.spa.ChangeDutyCycle(self.turn_rate)
        self.spb.ChangeDutyCycle(self.turn_rate)
        print("rotate R")
        return

    def rotate_l(self):

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.HIGH)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.HIGH)
        self.spa.ChangeDutyCycle(self.turn_rate)
        self.spb.ChangeDutyCycle(self.turn_rate)
        print("rotate L")
        return

    def stop_car(self):
        """stop"""
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)
        print("stop")
        return

    def shutdown_car(self):
        gpio.cleanup()
        print("shutdown")
        return



