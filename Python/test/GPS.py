import serial
import math 
from math import sin, cos, sqrt, atan2, radians

ser = serial.Serial('/dev/serial0')     # open serial port (serial0 is altijd de seriele poort en geen bluetooth ongeacht de config)

class GPS:
    def __init__(self):
        self.x_new = None
        self.x_old = None
        self.y_new = None
        self.y_old = None
        self.coordinaten_raw = None
        self.speed = None
        self.old_time = None

    @staticmethod
    def read_serial():
        data = ser.readline()
        return data

    def read_GPS_cor(self):
        data = GPS.read_serial()
        coordinaten = None
        if data[0:6] == b'$GPGGA':
            self.coordinaten_raw = data.decode("utf-8")
            coordinaten = self.coordinaat_omzetten_naar_kommagetal()
        return coordinaten 

    def coordinaat_omzetten_naar_kommagetal(self):
        coordinaten = self.coordinaten_raw
        latitude_minuten = float(coordinaten[19:27])*100000*1.66666667           # coordinaat met graden en minuten omrekenen naar coordinaat in kommagetallen
        latitude_minuten = latitude_minuten / 10000000
        latitude = int(coordinaten[17:19]) + latitude_minuten
        longitude_minuten = float(coordinaten[33:41])*100000*1.66666667
        longitude_minuten = longitude_minuten / 10000000
        longitude = int(coordinaten[30:33]) + longitude_minuten
        self.x_new = longitude
        self.y_new = latitude
        self.speed = self.coordinaten_naar_km_per_uur()
        coordinaat = [self.y_new, self.x_new, self.speed]
        return coordinaat

    def coordinaten_naar_km_per_uur(self):
        speed = None
        time = int(self.coordinaten_raw[7:13])
        if self.x_old:
            distance = self.calculate_distance(self.x_new, self.y_new, self.x_old, self.y_old)
            time_difference = time - self.old_time
            speed = distance * (3600 / time_difference)
        self.old_time = time
        self.x_old = self.x_new
        self.y_old = self.y_new
        return speed

    def make_str_coordinaten(self):
        coordinaten = self.coordinaten_raw
        latitude = f"{coordinaten[17:19]}°{coordinaten[19:27]}' {coordinaten[28]}"
        longitude = f"{coordinaten[30:33]}°{coordinaten[33:41]}' {coordinaten[42]}"
        coordinaat = [latitude, longitude]
        return coordinaat

    @staticmethod
    def calculate_distance(x1,y1,x2,y2):  
        # approximate radius of earth in km
        R = 6373.0
        lat1 = radians(y1)
        lon1 = radians(x1)
        lat2 = radians(y2)
        lon2 = radians(x2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance


while True:
    GPS1 = GPS()
    print(GPS1.read_GPS_cor())