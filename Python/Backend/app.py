from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from RPi import GPIO
import pigpio
import time
from threading import Thread

# klasses importeren
from model.Ultrasonic_sensor import Ultrasonic_sensor
from model.PWM_reader import PWM_reader
from model.GPS import GPS
from model.Mcp_AD import Mcp_AD
from model.LCD import LCD

# socket setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Goeie J'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# pinnen
channel1_pin = 13
channel2_pin = 6
channel3_pin = 5
servo_pin = 16
esc_pin_hover = 21
esc_pin_forward = 20
trigger_rechts = 12
echo_rechts = 25
trigger_links = 19
echo_links = 26
spots = 17
RS = 2         # 0 is instructie, 1 is karakters
D0 = 3
D1 = 4
D2 = 0
D3 = 1
D4 = 23
D5 = 24
D6 = 22
D7 = 27
E = 18          # klokpuls voor het LCD
list_D_pins = [D0, D1, D2, D3, D4, D5, D6, D7]

# var
object_avoidance = False
automatic_spots = True
led_aan = False
running = True
ultrasonic_rechts_afstand = 0
ultrasonic_links_afstand = 0
coordinaten = [0, 0, 0]
battery_emty = False
battery_percentage = 0
max_speed_list = [5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
max_forward_speed = 10
max_hover_speed = 10

# methodes
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel1_pin, GPIO.IN)
    GPIO.setup(channel2_pin, GPIO.IN)
    GPIO.setup(channel3_pin, GPIO.IN)
    GPIO.setup(spots, GPIO.OUT)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(esc_pin_hover, GPIO.OUT)
    GPIO.setup(esc_pin_forward, GPIO.OUT)

def omvormen_voor_servo(value):
    puls_width = 4.8 + ((value - 1000) * 0.004)         # bij elke servo anders, min 530, max 2400
    return puls_width

def omvormen_voor_esc_hover(value):
    puls_width = 5 + (value - 1000) / 200 
    if puls_width < 5.1:
        puls_width = 5
    elif puls_width > max_hover_speed:
        puls_width = max_hover_speed
    return puls_width

def omvormen_voor_esc_forward(value):
    puls_width = 5 + (value - 1500) / 100 
    if puls_width < 5.1:
        puls_width = 5
    elif puls_width > max_forward_speed:
        puls_width = max_forward_speed
    return puls_width

def uitlezen_ultrasone_sensors():
    global ultrasonic_rechts_afstand
    global ultrasonic_links_afstand
    global running
    ultrasonic_sensor_links = Ultrasonic_sensor(echo_links, trigger_links)
    ultrasonic_sensor_rechts = Ultrasonic_sensor(echo_rechts, trigger_rechts)
    # ultrasonic sensors uitlezen
    while running == True:
        ultrasonic_rechts_afstand = ultrasonic_sensor_rechts.ultrasonic_sensor_uitlezen()
        ultrasonic_links_afstand = ultrasonic_sensor_links.ultrasonic_sensor_uitlezen()
        # print(ultrasonic_links_afstand, ultrasonic_rechts_afstand)
        time.sleep(0.2)

def besturing():
    global ultrasonic_rechts_afstand
    global ultrasonic_links_afstand
    global running
    # pwm servo objecten aanmaken
    servo = GPIO.PWM(servo_pin, 50)
    esc_hover = GPIO.PWM(esc_pin_hover, 50)
    esc_forward = GPIO.PWM(esc_pin_forward, 50)
    servo.start(0)                                      # 0 send hij niets
    esc_hover.start(5)
    esc_forward.start(5)
    # PWM reader objecten maken
    channel1 = PWM_reader(pi, channel1_pin)
    channel2 = PWM_reader(pi, channel2_pin)
    channel3 = PWM_reader(pi, channel3_pin)
    while running == True:
        if channel1.pulse_width():              # checken of er verbinding is met de controller
            puls_width_servo = omvormen_voor_servo(channel1.pulse_width())
            puls_width_forward = omvormen_voor_esc_forward(channel2.pulse_width())
            puls_width_hover = omvormen_voor_esc_hover(channel3.pulse_width())
            # print(puls_width_servo, puls_width_forward, puls_width_hover)
            if object_avoidance == True:
                if ultrasonic_rechts_afstand > 100 and ultrasonic_links_afstand > 100:
                    servo.ChangeDutyCycle(puls_width_servo)
                    esc_hover.ChangeDutyCycle(puls_width_hover)
                    esc_forward.ChangeDutyCycle(puls_width_forward)
                elif ultrasonic_rechts_afstand < 100 and ultrasonic_rechts_afstand < ultrasonic_links_afstand:
                    servo.ChangeDutyCycle(8.8)
                    esc_hover.ChangeDutyCycle(puls_width_hover)
                    esc_forward.ChangeDutyCycle(puls_width_forward)
                elif ultrasonic_links_afstand < 100 and ultrasonic_links_afstand < ultrasonic_rechts_afstand:
                    servo.ChangeDutyCycle(4.8)
                    esc_hover.ChangeDutyCycle(puls_width_hover)
                    esc_forward.ChangeDutyCycle(puls_width_forward)
                else:
                    esc_hover.ChangeDutyCycle(0)
                    esc_forward.ChangeDutyCycle(0)
            else:
                servo.ChangeDutyCycle(puls_width_servo)
                esc_hover.ChangeDutyCycle(puls_width_hover)
                esc_forward.ChangeDutyCycle(puls_width_forward)
        else:
            servo.ChangeDutyCycle(0)
            esc_hover.ChangeDutyCycle(0)
            esc_forward.ChangeDutyCycle(0)
    # wanneer het programma wordt afgesloten
    channel1.cancel()
    channel2.cancel()
    channel3.cancel()
    servo.ChangeDutyCycle(0)
    esc_hover.ChangeDutyCycle(0)
    esc_forward.ChangeDutyCycle(0)

def uitlezen_GPS_en_AD_converter():
    global LDR_value
    global running
    global coordinaten
    while running == True:
        coordinaten_temp = GPS1.read_GPS_cor()
        if coordinaten_temp is not None:
            coordinaten = coordinaten_temp
        LDR_value = Mcp1.read_channel(0)
        LDR_verwerken(LDR_value)
        battery_value = Mcp1.read_channel(1)
        battery_verwerken(battery_value)
        time.sleep(0.1)

def battery_verwerken(value):
    global battery_emty
    global battery_percentage
    if value > 600:
        value = 600
    elif value < 400:
        value = 400
        battery_emty = True
    battery_percentage = (value - 400) / 2
    battery_percentage = round(battery_percentage, 0)
    

def LDR_verwerken(LDR_value):
    global led_aan
    if automatic_spots == True:
        if LDR_value < 500:
            GPIO.output(spots, GPIO.HIGH)
        else:
            GPIO.output(spots, GPIO.LOW)
    else:
        if led_aan == True:
            GPIO.output(spots, GPIO.HIGH)
        else:
            GPIO.output(spots, GPIO.LOW)

def database_wegschrijven():
    global running
    global LDR_value
    global led_aan
    global coordinaten
    global ultrasonic_rechts_afstand
    global ultrasonic_links_afstand
    while running == True:
        time.sleep(10)
        id_time = DataRepository.make_time_event(200)
        DataRepository.add_ldr_waarde(LDR_value, id_time)
        DataRepository.add_led_waarde(led_aan, id_time)
        DataRepository.add_ultrasone_waarde(ultrasonic_rechts_afstand, ultrasonic_links_afstand, id_time)
        DataRepository.add_gps_data(coordinaten[0], coordinaten[1], coordinaten[2], id_time)
    
# SOCKET IO
@socketio.on('connect')             # connect ontvangt hij standaard bij connectie
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_object_avoidance_systems')
def object_avoidance_systems_socket(value):
    global object_avoidance
    if value == 'True':
        object_avoidance = True
    elif value == 'False':
        object_avoidance = False

@socketio.on('F2B_automatic_leds')
def automatic_spots_socket(value):
    global automatic_spots
    if value == 'True':
        automatic_spots = True
    elif value == 'False':
        automatic_spots = False

@socketio.on('F2B_manual_leds')
def manual_leds_socket(value):
    global led_aan
    if value == 'True':
        led_aan = True
    elif value == 'False':
        led_aan = False

@socketio.on('F2B_slider_forward')
def slider_forward(value):
    global max_forward_speed
    max_forward_speed = max_speed_list[int(value)]

@socketio.on('F2B_slider_hover')
def slider_hover(value):
    global max_hover_speed
    max_hover_speed = max_speed_list[int(value)]

@socketio.on('F2B_give_history_list')
def give_history_list():
    gps_data = DataRepository.give_last_gps_rows(100)
    response = DataRepository.json_or_formdata(gps_data)
    print(response)
    socketio.emit('B2F_history_list', response)

@socketio.on('F2B_give_location')
def give_location():
    if coordinaten != [0, 0, 0]:
        print('location send')
        socketio.emit('B2F_coordinaten', {'coor': coordinaten})

@socketio.on('F2B_give_battery')
def give_battery():
    socketio.emit('B2F_battery', battery_percentage)

@socketio.on('F2B_settings')
def give_settings():
    socketio.emit('B2F_settings', {'object_avoidance': object_avoidance, 'automatic_spots': automatic_spots, 'led_aan': led_aan})

try:
    setup()
    time.sleep(0.1)
    pi = pigpio.pi()
    GPS1 = GPS()
    begin_time = time.time()

    # LCD starten een IP weergeven
    LCD1 = LCD(list_D_pins, E, RS)
    LCD1.init_LCD()
    LCD1.write_message('192.168.4.1     168.254.10.1')

    # AD converter object maken
    Mcp1 = Mcp_AD(0, 0)

    # ultrasone sensors objecten aanmaken
    ultrasonic_sensor_rechts = Ultrasonic_sensor(echo_rechts, trigger_rechts)
    ultrasonic_sensor_links = Ultrasonic_sensor(echo_links, trigger_links)

    # ultrasonic sensors thread starten
    thread_ultrasoon = Thread(target=uitlezen_ultrasone_sensors)
    thread_ultrasoon.start()

    # analog to digital converter uitlezen
    thread_GPS_AD = Thread(target=uitlezen_GPS_en_AD_converter)
    thread_GPS_AD.start()

    # database thread starten
    thread_database = Thread(target=database_wegschrijven)
    thread_database.start()

    time.sleep(0.5)

    # besturing thread starten
    thread_besturing = Thread(target=besturing)
    thread_besturing.start()

    socketio.run(app, debug=False, host='0.0.0.0')

except KeyboardInterrupt as e:
    print(e)
finally:
    running = False
    Mcp1.closespi()
    LCD1.display_on(False)
    socketio.stop()
    time.sleep(7)                     # zodat alle threads mooi kunnen afsluiten
    GPIO.cleanup()
    pi.stop()
