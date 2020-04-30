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
# Description: Defines class for controlling the L298N Dual H-Bridge DC motor controller;
#              A commonly available motor controller topology.
#
# ******************************************************************

import RPi.GPIO as GPIO


class L298N:
    def __init__(self):
        """
        Initializes the motor controller object

        Initializes the motor controller object. Asinges default values to the GPIO pins used to
        communicate with the L298N.

        Parameters:
        N/A

        Returns:
        N/A

        """
        self.ena = 12  # Set pin number for PWM to motor A
        self.in1 = 5   # Set pin number for digital IN1
        self.in2 = 6   # Set pin number for digital IN2
        self.enb = 13  # Set pin number for PWM to motor B
        self.in3 = 20  # Set pin number for digital IN3
        self.in4 = 21  # Set pin number for digital IN4
        self.PWMf = 1000  # Set PWM frequency (Hz)

        GPIO.setmode(GPIO.BCM)  # Set GPIO pins to correspond with processor pin numbers

        # Set all of the pins as outputs
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.enb, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        # Define the enable pins as PWM. The default pins support hardware PWM.
        self.spa = GPIO.PWM(self.ena, self.PWMf)
        self.spb = GPIO.PWM(self.enb, self.PWMf)
        # Start PWM at zero percent duty cycle
        self.spa.start(0)
        self.spb.start(0)

    def forward(self, speed):
        """
        Drive straight forward
        :param speed: percentage value for wheel speed
        :return: void
        """

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(speed)


    def turn_l(self, speed, turn_rate):
        """
        Turn left while driving forward
        :param speed: percentage value for right wheel speed
        :param turn_rate: percentage value for left wheel speed
        :return: void
        """
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(turn_rate)
        self.spb.ChangeDutyCycle(speed)


    def turn_r(self, speed, turn_rate):
        """
        Turn right while moving forward
        :param speed: percentage value for left wheel speed
        :param turn_rate: percentage value for right wheel speed
        :return: void
        """
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(turn_rate)

    def reverse(self, speed):
        """
        Drive in reverse
        :param speed: percentage value for wheel speed
        :return: void
        """
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        self.spa.ChangeDutyCycle(speed)
        self.spb.ChangeDutyCycle(speed)

    def rotate_l(self, rate):
        """
        Rotate in place counter clockwise
        :param rate: percentage value for wheel speed
        :return: void
        """
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.spa.ChangeDutyCycle(rate)
        self.spb.ChangeDutyCycle(rate)

    def rotate_r(self, rate):
        """
        Rotate in place clockwise
        :param rate: percentage value for wheel speed
        :return: void
        """
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        self.spa.ChangeDutyCycle(rate)
        self.spb.ChangeDutyCycle(rate)
        return

    def stop_car(self):
        """
        Stop movement
        :return: void
        """
        self.spa.ChangeDutyCycle(0)
        self.spb.ChangeDutyCycle(0)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

        return

    def shutdown(self):
        """
        Clean up GPIO associated with the motor driver
        :return: void
        """
        GPIO.cleanup()




