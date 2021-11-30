import neopixel
import math, time

NUM_BULBS = 150
RGB_SIZE = 255 * 6
STEP_SIZE = math.floor(RGB_SIZE / NUM_BULBS)

def clear(pixels):
    pixels.fill((0, 0, 0))

def rainbow_effect(pixels):
    for i, (r, g, b) in enumerate(rainbow_gradient()):
        if i == NUM_BULBS:
            break
        pixels[i] = (r, g, b)

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
            time.sleep(0.5)

def mountain_effect(pixels):
    PEAKS = [0, 6, 36, 61, 96, 129, 149]

    # top_color = (255, 255, 255)
    top_color = (0, 255, 0)
    btm_color = (255, 0, 0)
    for idx in range(len(PEAKS) - 1):
        left = PEAKS[idx]
        right = PEAKS[idx + 1]
        gradient = color_gradient(top_color, btm_color, math.ceil((right - left) / 2))
        for offset, color in enumerate(gradient):
            pixels[left + offset] = color
            pixels[right - offset] = color

def color_gradient(start, end, num):
    rm = start[0] - end[0]
    gm = start[1] - end[1]
    bm = start[2] - end[2]

    for i in range(num):
        red = start[0] - math.floor(rm * i / num)
        green = start[1] - math.floor(gm * i / num)
        blue = start[2] - math.floor(bm * i / num)
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

