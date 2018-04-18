import time

import RPi.GPIO as GPIO


class Motor(object):
    pwm_frequency = 490

    def __init__(self, a_pin, b_pin, reverse=False, pwm=False):
        self.reverse = reverse
        self.pwm = pwm
        if not reverse:
            self.a_pin = a_pin
            self.b_pin = b_pin
        else:
            self.a_pin = b_pin
            self.b_pin = a_pin
        for pin in [a_pin, b_pin]:
            GPIO.setup(pin, GPIO.OUT)

        if self.pwm:
            self.a_pwm = GPIO.PWM(self.a_pin, self.pwm_frequency)
            self.b_pwm = GPIO.PWM(self.b_pin, self.pwm_frequency)
            self.a_pwm.start(0)
            self.b_pwm.start(0)
        else:
            for pin in [a_pin, b_pin]:
                GPIO.output(pin, GPIO.LOW)

    def forward(self, speed=100.0):
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(speed)
            self.b_pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(self.a_pin, GPIO.HIGH)
            GPIO.output(self.b_pin, GPIO.LOW)

    def backward(self, speed=100.0):
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(0)
            self.b_pwm.ChangeDutyCycle(speed)
        else:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.HIGH)

    def stop(self):
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(0)
            self.b_pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.LOW)

    def close(self):
        if self.pwm:
            self.a_pwm.stop()
            self.b_pwm.stop()


GPIO.setmode(GPIO.BCM)
m1 = Motor(4, 18, pwm=True)
m2 = Motor(12, 19, pwm=True)

print('1 forward 20')
m1.forward(20)
time.sleep(2)

print('1 forward 50')
m1.forward(50)
time.sleep(2)

print('1 forward 100')
m1.forward(100)
time.sleep(2)

print('1 back 50')
m1.backward(50)
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

m1.stop()
m2.stop()
GPIO.cleanup()
