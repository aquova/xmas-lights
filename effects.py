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

