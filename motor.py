import RPi.GPIO as gpio
import time

ena = 12
in1 = 5
in2 = 6
enb =13
in3 = 20
in4 = 21
PWMf = 1000

gpio.setmode(gpio.BCM)
gpio.setup(ena, gpio.OUT)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(enb, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
spa = gpio.PWM(ena, PWMf)
spb = gpio.PWM(enb, PWMf)

time.sleep(3)

gpio.output(in1, gpio.LOW)
gpio.output(in2, gpio.HIGH)
gpio.output(in3, gpio.HIGH)
gpio.output(in4, gpio.LOW)

spa.start(100)
spb.start(100)

for x in range (0, 5):
    time.sleep(1)

gpio.cleanup()
print("run")
