import time
import RPi.GPIO as GPIO

MO_1a = 12
MO_1b = 4

MO_2a = 18
MO_2b = 19
pins = [MO_1a, MO_1b, MO_2a, MO_2b]

 
GPIO.setmode(GPIO.BCM)
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)

GPIO.output(MO_1a, GPIO.LOW)
GPIO.output(MO_1b, GPIO.LOW)
GPIO.output(MO_2a, GPIO.LOW)
GPIO.output(MO_2b, GPIO.LOW)

time.sleep(2)

GPIO.output(MO_1a, GPIO.HIGH)
GPIO.output(MO_1b, GPIO.LOW)
print('1 forward')

time.sleep(5)

GPIO.output(MO_1a, GPIO.LOW)
GPIO.output(MO_1b, GPIO.HIGH)
print('1 back')

time.sleep(5)


GPIO.output(MO_1a, GPIO.LOW)
GPIO.output(MO_1b, GPIO.LOW)
GPIO.output(MO_2a, GPIO.LOW)
GPIO.output(MO_2b, GPIO.LOW)

time.sleep(5)

GPIO.output(MO_2a, GPIO.HIGH)
GPIO.output(MO_2b, GPIO.LOW)
print('2 forward')

time.sleep(5)

GPIO.output(MO_2a, GPIO.LOW)
GPIO.output(MO_2b, GPIO.HIGH)
print('2 back')

time.sleep(5)

GPIO.output(MO_1a, GPIO.LOW)
GPIO.output(MO_1b, GPIO.LOW)
GPIO.output(MO_2a, GPIO.LOW)
GPIO.output(MO_2b, GPIO.LOW)

GPIO.cleanup()