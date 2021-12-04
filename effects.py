import neopixel
from math import ceil, floor
from random import randint
from time import sleep

NUM_BULBS = 150
RGB_SIZE = 255 * 6
STEP_SIZE = floor(RGB_SIZE / NUM_BULBS)

def clear(pixels):
    pixels.fill((0, 0, 0))

def rainbow_effect(pixels):
    offset = randint(0, NUM_BULBS - 1)
    for i, (r, g, b) in enumerate(rainbow_gradient()):
        ii = (i + offset) % NUM_BULBS
        pixels[ii] = (r, g, b)

def christmas_effect(pixels):
    pixels.fill((255, 0, 0))
    for i in range(0, NUM_BULBS, 2):
        pixels[i] = (0, 255, 0)

def classic_effect(pixels):
    COLORS = [
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 0, 255)
    ]

    for i in range(NUM_BULBS):
        pixels[i] = COLORS[i % len(COLORS)]

def cycle_effect(pixels):
    while True:
        for (r, g, b) in rainbow_gradient():
            pixels.fill((r, g, b))
            sleep(0.5)

def mountain_effect(pixels):
    PEAKS = [0, 6, 36, 61, 96, 129, 149]

    top_color = (244, 186, 253)
    btm_color = (96, 1, 112)
    for idx in range(len(PEAKS) - 1):
        left = PEAKS[idx]
        right = PEAKS[idx + 1]
        gradient = color_gradient(top_color, btm_color, ceil((right - left) / 2) + 1)
        for offset, color in enumerate(gradient):
            pixels[left + offset] = color
            pixels[right - offset] = color

def color_gradient(start, end, num):
    rm = start[0] - end[0]
    gm = start[1] - end[1]
    bm = start[2] - end[2]

    for i in range(num):
        red = start[0] - floor(rm * i / num)
        green = start[1] - floor(gm * i / num)
        blue = start[2] - floor(bm * i / num)
        yield red, green, blue

def rainbow_gradient():
    r, g, b = 255, 0, 0
    for g in range(STEP_SIZE, 255, STEP_SIZE):
        yield r, g, b
    for r in range(255, STEP_SIZE, -STEP_SIZE):
        yield r, g, b
    for b in range(STEP_SIZE, 255, STEP_SIZE):
        yield r, g, b
    for g in range(255, STEP_SIZE, -STEP_SIZE):
        yield r, g, b
    for r in range(STEP_SIZE, 255, STEP_SIZE):
        yield r, g, b
    for b in range(255, STEP_SIZE, -STEP_SIZE):
        yield r, g, b

