# stripctl

## Installation

With `pip`:
```bash
pip install git+https://github.com/Freemanium/stripctl
```

With `pipenv`:
```bash
pipenv install git+https://github.com/Freemanium/stripctl#egg=stripctl
```

## Usage

```python
#!/usr/bin/env python3

import time
import math
from stripctl import APA102

strip = APA102(300)
strip.state = 'red'
strip.level = .2

STEPS = 300
DELAY = 0.02


def wave(progress: float) -> float:
    """ Smooth waveform in bounds [0.0, 1.0], starting at y=1.0 """
    return 0.5 * math.cos(progress * 2*math.pi) + 0.5

# Rainbow
try:
    while True:
        for step in range(STEPS):
            hue = wave(step / STEPS)
            with strip:
                for led in strip:
                    led.hue = hue
            time.sleep(DELAY)
    
except KeyboardInterrupt:
    print('^C')
```
