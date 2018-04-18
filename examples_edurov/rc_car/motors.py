import time
import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self, a_pin, b_pin, reverse=False, pwd=False):
        self.reverse = reverse
        if not reverse:
            self.a_pin = a_pin
            self.b_pin = b_pin
        else:
            self.a_pin = b_pin
            self.b_pin = a_pin
        GPIO.setmode(GPIO.BCM)
        for pin in [a_pin, b_pin]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def forward(self, speed=1.0):
        if not self.reverse:
            GPIO.output(self.a_pin, GPIO.HIGH)
            GPIO.output(self.b_pin, GPIO.LOW)

    def backward(self, speed=1.0):
        if not self.reverse:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.a_pin, GPIO.LOW)
        GPIO.output(self.b_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


m1 = Motor(4, 18)
m2 = Motor(12, 19)

print('1 forward')
m1.forward()
time.sleep(2)

print('1 back')
m1.backward()
time.sleep(2)

print('1 stop')
m1.stop()
time.sleep(2)

print('2 forward')
m2.forward()
time.sleep(2)

print('2 back')
m2.backward()
time.sleep(2)

print('2 stop')
m2.stop()
time.sleep(2)

m1.cleanup()
m2.cleanup()
