from RPi import GPIO

servo_pin = 16

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    servo1 = GPIO.PWM(servo_pin, 50)
    servo1.start(0)     # 0 send hij niets
    while True:
        puls_width = float(input('puls with >  '))        # bij elke servo anders, min 2.3, max 11.5, beste 2.4 en 11.2
        servo1.ChangeDutyCycle(puls_width)
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()