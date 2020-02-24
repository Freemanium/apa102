from .spi import SPI
from colour import Color

from typing import Union, Optional as Opt, List, Iterator

ColorResolvable = Union[str, Color]
StripState = List[Color]
StripStateResolvable = Union[Color, StripState]

def normalize(arg: StripStateResolvable) -> StripStateResolvable:
    if isinstance(arg, list):
        return [Color(x) for x in arg]
    else:
        return Color(arg)

class APA102:
    def __init__(self, num_leds: int, auto_flush: bool = False, base_state: Opt[StripStateResolvable] = 'black', bus_index: int = 0, dev_index: int = 0, destructor: bool = True):
        self.num_leds = num_leds
        self.auto_flush = auto_flush
        self.destructor = destructor
        self._spi = SPI(bus_index, dev_index)
        self._level = 1.0

        self.base_state = base_state
        if base_state is not None:
            self.base_state = normalize(self.base_state)
            self.reset(True)

    def reset(self, flush: Opt[bool] = None):
        if flush is None:
            flush = self.auto_flush
        self.update(self.base_state, flush=flush)
    
    @property
    def level(self) -> float:
        """ Brightness level, 0.0 - 1.0. """
        return self._level
    
    @level.setter
    def level(self, val: float):
        self.update(self.state, val, flush=self.auto_flush)
        
    @property
    def state(self) -> StripState:
        """ List of Color objects. """
        return self._state
    
    @state.setter
    def state(self, val: StripStateResolvable):
        self.update(val, flush=self.auto_flush)

    def flush(self):
        """ Writes the internal state to the strip. """
        # protocol based on 
        # https://cpldcpu.wordpress.com/2014/11/30/understanding-the-apa102-superled/
        data = []

        # start frame
        data += [0x00] * 4

        brightness = int(self.level * 0b00011111) | 0b11100000
        for col in self.state:
            bgr = col.blue, col.green, col.red
            bgr = [round(x*255) for x in bgr]
            data += [brightness, *bgr]
        
        # end frame
        data += [0xFF] * 4

        self._spi.send(data)
    
    def update(self, states: StripStateResolvable, level: float = None, flush: bool = True):
        """ Updates the internal state, syncs with the strip if `flush` is `True`. """
        if not isinstance(states, list):
            states = [states] * len(self)
        if len(states) != len(self):
            raise ValueError(f'Expected {len(self)} states, but received {len(states)}')
        
        self._state = normalize(states)
        if level:
            if level < 0 or level > 1:
                raise ValueError(f'Level out of range: {level} (must be in [0,1])')
            self._level = level
        if flush:
            self.flush()
    
    def __getitem__(self, i: int) -> Color:
        return self.state[i]
    
    def __setitem__(self, i: int, x: ColorResolvable):
        self.state[i] = normalize(x)
        if self.auto_flush:
            self.flush()
        
    def __len__(self) -> int:
        return self.num_leds
    
    def __str__(self) -> str:
        return f'APA102<{len(self)}>'
    
    def __iter__(self) -> Iterator[Color]:
        return iter(self.state)
    
    def iter_idx(self) -> Iterator[int]:
        return iter(range(len(self.state)))
    
    def __enter__(self):
        """ Starts a block which is flushed at the end. """
        self._old_auto_flush = self.auto_flush
        self.auto_flush = False
    
    def __exit__(self, ex_type, ex_val, traceback):
        self.flush()
        self.auto_flush = self._old_auto_flush
    
    def __del__(self):
        if self.destructor:
            self.update('black', flush=True)