from RPi import GPIO
import time
delay = 0.002

class LCD:
    def __init__(self, list_D_pins, E, RS, is_vier_bits = False):
        self.list_D_pins = list_D_pins
        self.E = E
        self.RS = RS
        self.is_vier_bits = is_vier_bits

    @property
    def list_D_pins(self):
        """The list_D_pins property."""
        return self._list_D_pins
    @list_D_pins.setter
    def list_D_pins(self, value):
        if type(value) is list:
            self._list_D_pins = value
        else:
            raise TypeError
    
    @property
    def E(self):
        """The E property."""
        return self._E
    @E.setter
    def E(self, value):
        if type(value) is int:
            self._E = value
        else:
            raise TypeError
    
    @property
    def RS(self):
        """The RS property."""
        return self._RS
    @RS.setter
    def RS(self, value):
        if type(value) is int:
            self._RS = value
        else:
            raise TypeError
    
    @property
    def is_vier_bits(self):
        """The is_vier_bits property."""
        return self._is_vier_bits
    @is_vier_bits.setter
    def is_vier_bits(self, value):
        if type(value) is bool:
            self._is_vier_bits = value
        else:
            raise TypeError

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        for i in range(0, 8):
            GPIO.setup(self.list_D_pins[i], GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
        GPIO.setup(self.RS, GPIO.OUT)

    def __set_data_bits(self, byte):
        GPIO.output(self.E, GPIO.HIGH)
        for i in range(0, 8):
            bit = byte >> i & 1
            if bit == True:
                GPIO.output(self.list_D_pins[i], GPIO.HIGH)
            else:
                GPIO.output(self.list_D_pins[i], GPIO.LOW)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(delay)

    def __send_instruction(self, byte):
        GPIO.output(self.RS, GPIO.LOW)
        self.__set_data_bits(byte)

    def __send_character(self, byte):
        GPIO.output(self.RS, GPIO.HIGH)
        self.__set_data_bits(byte)

    def write_message(self, message):
        self.clear_LCD()
        x = 0
        message = list(message)
        eerst_pauze = True
        while x < len(message):                     #zal oneindig blijven doorgaan als de message langer is dan 32 tekens
            self.__send_character(ord(message[x]))
            x += 1
            if x == 16:
                self.change_cursor_location()
            elif x == 32:
                if eerst_pauze == True:
                    time.sleep(3)
                    eerst_pauze = False
                    for i in range(0, 16):          #witruimte voorzien achter de message
                        message.append(' ')
                x = 0
                self.change_cursor_location(0)               # cursor terug in het begin plaatsen
                voorste_letter = message[0]             #de voorste letter vanachter plaatsen
                message.pop(0)
                message.append(voorste_letter)
                time.sleep(0.5)

    def change_cursor_location(self, address = 0x40):
        data = 0b10000000 | address
        self.__send_instruction(data)

    def cursor_on(self, True_False = True):
        if True_False == True:
            self.__send_instruction(0b00001111)
        else:
            self.__send_instruction(0b00001100)

    def clear_LCD(self):
        self.__send_instruction(1)

    def display_on(self, True_False = True):
        if True_False == True:
            self.__send_instruction(0b00001111)
        else:
            self.__send_instruction(0b00001011)

    def init_LCD(self):
        self.__setup()
        if self.is_vier_bits == True:
            self.__send_instruction(0b00101000)
        else:
            self.__send_instruction(0b00111000)            # display juist instellen, eerst 1 is zodat het display weet over welke instructie je het hebt, de andere instellingen
        self.__send_instruction(0b00001100)
        self.__send_instruction(1)