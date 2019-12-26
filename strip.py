from spi import SPI

class LedStrip:
    def __init__(self, num_leds, bus_index=0, dev_index=0):
        self.num_leds = num_leds
        self._spi = SPI(bus_index, dev_index)
    
    def update(self, states):
        if not isinstance(states, list):
            states = [states] * self.num_leds
        if len(states) != self.num_leds:
            raise RuntimeError(f'Invalid number of states: {len(states)}')
            
        data = []
        data += [0x00] * 4
        for state in states:
            r,g,b = state
            data += [(0b00001000 | 0b11000000), b, g, r]

        data += [0xFF] * 4

        self._spi.send(data)