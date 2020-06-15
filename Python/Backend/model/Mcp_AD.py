import spidev

spi = spidev.SpiDev()        

class Mcp_AD:
    def __init__(self, bus = 0, device = 0):
        spi.open(bus, device)           # Bus SPI0 (SPI0 is de enigste die automatisch geactiveerd is, SPI1 & 2 bestaan ook), slave op CE 0 = GPIO8, CE 1 = GPIO9
        spi.max_speed_hz = 10 ** 5                # 100 kHz, anders is onze pi te snel voor het component

    @staticmethod
    def read_channel(channel):
        bytes_out = [0b00000001,0b10000000,0b00000000]               
        channel_byte = int(f'{channel:08b}')  << 4         #convert de int naar binair zonder er een string van te maken, bin(x) doet dit wel
        bytes_out[1] |= channel_byte
        bytes_in = spi.xfer(bytes_out)
        waarde = (bytes_in[1] << 8) | bytes_in[2]       # de eerste byte negeren, de 2de 8 opschuiven en er de derde achter zetten
        return waarde

    @staticmethod
    def closespi():
        spi.close() 

if __name__ == '__main__':
    Mcp1 = Mcp_AD(0, 0)
    while True:                                    
        waarde_analoog = Mcp1.read_channel(0)
        print(waarde_analoog)
