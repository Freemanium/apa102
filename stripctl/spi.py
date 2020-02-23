from spidev import SpiDev

class SPI:
    DEFAULT_FREQ = 8*1000**2 # 8MHz

    def __init__(self, bus_index, dev_index, freq=SPI.DEFAULT_FREQ):
        self.bus = bus_index
        self.dev = dev_index
        self.freq = freq
        self._spi = None

        self._open()
    
    def __del__(self):
        self._close()
    
    def _open(self):
        if not self._spi:
            self._spi = SpiDev()
            self._spi.open(self.bus, self.dev)
            self._spi.max_speed_hz = self.freq
    
    def _close(self):
        if self._spi:
            self._spi.close()
            self._spi = None
        
    def send(self, data):
        self._spi.writebytes2(bytes(data))