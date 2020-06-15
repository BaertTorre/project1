import time
from RPi import GPIO

servo_pin = 16

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)

def servo(graden):
    graden = int(graden)
    duty_cycle = (0.54 + (graden / 203) * 1.93) / 1000          # voor elke servo anders min 540, max 2470
    GPIO.output(servo_pin, GPIO.HIGH)
    time.sleep(duty_cycle)
    GPIO.output(servo_pin, GPIO.LOW)
    time.sleep(0.02 - duty_cycle)

try:
    setup()
    x = 100
    while True:
        if x == 100:
            graden = input('Geef graden op   >> ')
            x = 0
        servo(graden)
        x += 1
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()