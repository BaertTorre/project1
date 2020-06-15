import serial

ser = serial.Serial('/dev/ttyS0')     # open serial port (serial0 is altijd de seriele poort en geen bluetooth ongeacht de config)

class Esp8266:
    @staticmethod
    def read_serial():
        data = ser.readline()
        return data

    @staticmethod
    def read_LDR():
        data = Esp8266.read_serial()
        coordinaten = None
        if data[0:6] == b'$GPGGA':
            coordinaten = data.decode("utf-8")
            if coordinaten[8] == ',':
                return None 
            else:
                return coordinaten
            

if __name__ == '__main__':
    while True:
        coordinaten = [0, 0, 0]
        print(coordinaten[2])