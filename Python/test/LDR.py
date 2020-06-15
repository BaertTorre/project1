from RPi import GPIO
from Esp8266 import Esp8266
import time

try:
    GPIO.setmode(GPIO.BCM)
    while True:
        data = Esp8266.read_LDR()
        data = int(data)
        print(data)
        time.sleep(1)
except KeyboardInterrupt as e:
    print(e)