from spi import SPI

# TODO: Test if brightness setting can be changed per-led

def crop(x, lb, ub):
    if x < lb:
        return lb
    elif x > ub:
        return ub
    else:
        return x

def make_rgb(x):
    """ Normalizes the argument and returns an RGB tuple. """
    if isinstance(x, int):
        r = (x & 0xFF0000) >> 16
        g = (x & 0x00FF00) >> 8
        b = (x & 0x0000FF)
        return r, g, b
    elif isinstance(x, (tuple, list)):
        return tuple(x)
    else:
        raise TypeError(x)

class APA102:
    def __init__(self, num_leds, auto_flush=False, bus_index=0, dev_index=0):
        self.num_leds = num_leds
        self._spi = SPI(bus_index, dev_index)

        self.auto_flush = auto_flush
        self.reset()

    def reset(self):
        self._level = 1.0
        self._state = [0xFF] * len(self)
    
    @property
    def level(self):
        """ Brightness level, 0.0 - 1.0. """
        return self._level
    
    @level.setter
    def level(self, val):
        self._level = crop(val, 0.0, 1.0)
        if self.auto_flush:
            self.flush()
        
    @property
    def state(self):
        """ List of RGB-tuples. """
        return self._state
    
    @state.setter
    def state(self, val):
        self.update(val, flush=self.auto_flush)

    @property
    def colors(self):
        """ List of LED colors as an int. """
        colors = []
        for r, g, b in self.state:
            col = (r << 16) | (g << 8) | (b)
            colors.push(col)
        return colors

    def flush(self):
        """ Writes the internal state to the strip. """
        # protocol based on 
        # https://cpldcpu.wordpress.com/2014/11/30/understanding-the-apa102-superled/
        data = []

        # start frame
        data += [0x00] * 4

        brightness = (self.level * 0b00111111) | 0b11000000
        for r, g, b in self.state:
            data += [brightness, b, g, r]
        
        # end frame
        data += [0xFF] * 4

        self._spi.send(data)
    
    def update(self, state, level=None, flush=True):
        """ Updates the internal state, syncs with the strip if `flush` is `True`. """
        if not isinstance(states, list):
            states = [states] * len(self)
        if len(states) != len(self):
            raise RuntimeError(f'Expected {len(self)} states, but received {len(states)}')
        
        self._state = [make_rgb(state) for x in states]
        if level:
            self._level = crop(level, 0.0, 1.0)
        if flush:
            self.flush()
    
    def __getitem__(self, i):
        return self.state[i]
    
    def __setitem__(self, i, x):
        self.state[i] = x
        if self.auto_flush:
            self.flush()
        
    def __len__(self):
        return self.num_leds
    
    def __str__(self):
        return f'APA102<{len(self)}>'
    
    def __iter__(self):
        return iter(self.state)