import time

import RPi.GPIO as GPIO


class Motor(object):
    """Manages a DC motor through two GPIO pins"""
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

    def speed(self, speed):
        """Set the speed of the motor, speed<0 gives reverse rotation"""
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        if speed > 0:
            self.forward(speed)
        elif speed < 0:
            self.backward(speed * -1)
        else:
            self.stop()

    def forward(self, speed=100.0):
        """Turns the motor forward, speed can be used if pwm is enabled"""
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(speed)
            self.b_pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(self.a_pin, GPIO.HIGH)
            GPIO.output(self.b_pin, GPIO.LOW)

    def backward(self, speed=100.0):
        """Turns the motor backward, speed can be used if pwm is enabled"""
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(0)
            self.b_pwm.ChangeDutyCycle(speed)
        else:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.HIGH)

    def stop(self):
        """Stops the motor from rotating"""
        if self.pwm:
            self.a_pwm.ChangeDutyCycle(0)
            self.b_pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.LOW)

    def close(self):
        """Frees up the pwm controller if that is used"""
        if self.pwm:
            self.a_pwm.stop()
            self.b_pwm.stop()


class Button():
    """Imitates joystick behavior by gradually increasing the value"""
    max = 100
    ramp_time = 0.0

    def __init__(self):
        self.last = False
        self.value = 0

    def update(self, now):
        """Updates value depending on how long the button has been pressed"""
        if now is not self.last:
            self.last = now
            self.value = 0
            if now:
                self.start_press = time.time()
        else:
            if not now:
                self.value = 0
            else:
                if time.time() - self.start_press > self.ramp_time:
                    self.value = self.max
                else:
                    factor = (time.time() - self.start_press) / self.ramp_time
                    self.value = self.max * factor
