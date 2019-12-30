#!/usr/bin/env python3

import time

from stripctl import APA102
from stripctl.colors import *

def levels():
    lb = 0
    ub = 1
    step = .01

    x = lb
    while x < ub:
        yield x
        x += step

NUM = 60

strip = APA102(NUM)

for lvl in levels():
    with strip:
        strip.level = lvl
    time.sleep(.1)

# strip[0] = BLUE
# strip[len(strip)//2-1] = RED
# strip[len(strip) - 1] = GREEN

# strip.flush()