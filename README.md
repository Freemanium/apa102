# stripctl

## Installation

```bash
pip install -U git+https://github.com/Freemanium/stripctl
```

## Usage

```python
import time
import math
from stripctl import APA102
from stripctl.colors import *

strip = APA102(60)
strip.reset(flush=True)

with strip:
    strip.update('red')

# Rainbow
i = 0
num_states = 300
while True:
    hue = .5*math.cos(i / num_states * 2 * math.pi) + .5
    with strip:
        for led in strip:
            led.hue = hue

    time.sleep(.02)
    i = (i+1) % num_states
```
