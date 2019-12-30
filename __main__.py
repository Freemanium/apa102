#!/usr/bin/env python3

import time

from stripctl import APA102, Color

strip = APA102(60)

with strip:
    strip.reset(flush=True)

def approx(a, b, eps=10 ** -5):
    return abs(b-a) <= eps

led = strip[29]
led.red = 1
while True:
    asc = True
    with strip:
        if asc:
            led.hue += .01
        else:
            led.hue -= .01
        if approx(led.hue, 1):
            asc = False
        elif approx(led.hue, 0):
            asc = False
    
    time.sleep(.02)