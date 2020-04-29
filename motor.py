import RPi.GPIO as GPIO


class L298N:
    def __init__(self):
        self.ena = 12
        self.in1 = 5
        self.in2 = 6
        self.enb = 13
        self.in3 = 20
        self.in4 = 21
        self.PWMf = 1000

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.enb, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        self.spa = GPIO.PWM(self.ena, self.PWMf)
        self.spb = GPIO.PWM(self.enb, self.PWMf)
        self.spa.start(0)
        self.spb.start(0)
        print("init")

    def forward(self, speed):
        """drive forward"""

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(speed)


    def turn_l(self, speed, turn_rate):

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(turn_rate)
        self.spb.ChangeDutyCycle(speed)


    def turn_r(self, speed, turn_rate):

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(turn_rate)


    def reverse(self, speed):

        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(speed)
        return

    def rotate_l(self, rate):

        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(rate)
        self.spb.ChangeDutyCycle(rate)
        return

    def rotate_r(self, rate):

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        self.spa.ChangeDutyCycle(rate)
        self.spb.ChangeDutyCycle(rate)
        return

    def stop_car(self):
        """stop"""
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        return

    def shutdown(self):
        """shutdown"""
        GPIO.cleanup()




