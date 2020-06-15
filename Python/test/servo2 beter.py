import pigpio

servo_pin = 16

try:
    pi = pigpio.pi()
    while True:
        puls_width = int(input('puls with >  '))        # bij elke servo anders, bij mij min 530, max 2400
        pi.set_servo_pulsewidth(servo_pin, puls_width)
except KeyboardInterrupt as e:
    print(e)
finally:
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.stop()