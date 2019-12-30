#!/usr/bin/env python3

from time import sleep

from stripctl import APA102
from stripctl.colors import *

NUM = 60

strip = APA102(NUM)

strip[0] = BLUE
strip[len(strip)//2-1] = RED
strip[len(strip) - 1] = GREEN

strip.flush()