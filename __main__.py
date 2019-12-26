from strip import LedStrip
from time import sleep

# TODO:
# - brightness
# - geiles interface
# - 

NUM = 60

colors = [
    0x0B0300,
    0x190601,
    0x230902,
    0x2F0D03,
    0x401204,
    0x481405,
    0x521806,
    0x591007,
    0x622108,
    0x6E2508,
    0x772809,
    0x7F2A09,
    0x882D0A,
    0x90300A,
    0x96320A,
    0x9D330A,
    0xA6360A,
    0xB0390A,
    0xB0450A,
    0xB9480B,
    0xC1580B,
    0xCB610B,
    0xD3650C,
    0xD6740C,
    0xDC770B,
    0xDC810B,
    0xE5860B,
    0xED8E12,
    0xF2A113,
    0xF2B013,
    0xF5B51A,
    0xF9BA22,
    0xFBBD29,
    0xFEC232,
    0xFFC742,
    0xFECC55,
    0xFED166,
    0xFDD473,
    0xFDD880,
    0xFDE4A7,
    0xFDEABC,
    0xFDEEC8,
    0xFDF0D1,
    0xFDF3DA,
    0xFCF4E2
]

def hex2rgb(hex):
    r = (hex & 0xFF0000) >> 16
    g = (hex & 0x00FF00) >> 8
    b = hex & 0x0000FF
    return r,g,b

strip = LedStrip(NUM)

lb = 0
ub = NUM

states = []

while lb < ub:
    for i in range(lb, ub):
        states = [(0xFF, 0xFF, 0xFF)] * NUM
        states[i] = (0xFF, 0x00, 0x00)
        for k in range(0, lb):
            states[k] = (0x00, 0xFF, 0x00)
        for k in range(ub, NUM):
            states[k] = (0x00, 0x00, 0xFF)
        strip.update(states)
        sleep(.005)
    ub -= 1

    for i in range(lb, ub):
        states = [(0xFF, 0xFF, 0xFF)] * NUM
        states[NUM-i-1] = (0xFF, 0x00, 0x00)
        for k in range(0, lb):
            states[k] = (0x00, 0xFF, 0x00)
        for k in range(ub, NUM):
            states[k] = (0x00, 0x00, 0xFF)
        strip.update(states)
        sleep(.005)
    lb += 1


states[NUM//2-1] = (0xFF, 0x00, 0x00)
strip.update(states)



# for state in colors:
#     r, g, b = hex2rgb(state)
#     print(f'{r:02X} {g:02X} {b:02X}')
#     strip.update([(r,g,b)] * NUM)
#     sleep(.5)
    