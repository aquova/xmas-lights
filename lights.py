from neopixel import NeoPixel

from math import ceil, floor
from random import randint
from time import sleep

BRIGHTNESS = 0.15
NUM_BULBS = 150
RGB_SIZE = 255 * 6
STEP_SIZE = floor(RGB_SIZE / NUM_BULBS)

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

class Lights(NeoPixel):
    def __init__(self, gpio_pin):
        super().__init__(gpio_pin, NUM_BULBS, bpp=3)
        self.last_color = (255, 255, 255)
        self.powered = False
        self.effect = "fill"
         
    def __setitem__(self, idx, color):
        corrected = (int(color[1] * BRIGHTNESS), int(color[0] * BRIGHTNESS), int(color[2] * BRIGHTNESS))
        super().__setitem__(idx, corrected)
        
    def fill(self, c):
        super().fill((int(BRIGHTNESS * c[1]), int(BRIGHTNESS * c[0]), int(BRIGHTNESS * c[2])))
        super().write()
    
    def is_powered(self):
        return self.powered

    def set_powered(self, p):
        self.powered = p
        
    def set_color(self, c):
        self.last_color = c
        
    def get_last_color(self):
        return self.last_color
    
    def set_effect(self, effect):
        self.effect = effect
        
    def get_effect(self):
        return self.effect
    
    def rainbow_effect(self):
        offset = randint(0, NUM_BULBS - 1)
        for i, (r, g, b) in enumerate(rainbow_gradient()):
            ii = (i + offset) % NUM_BULBS
            self[ii] = (r, g, b)
        self.write()

    def christmas_effect(self):
        self.fill((255, 0, 0))
        for i in range(0, NUM_BULBS, 2):
            self[i] = (0, 255, 0)
        self.write()

    def classic_effect(self):
        COLORS = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 0, 255)
        ]

        for i in range(NUM_BULBS):
            self[i] = COLORS[i % len(COLORS)]
        self.write()

    def mountain_effect(self):
        PEAKS = [0, 6, 36, 61, 96, 129, 149]

        top_color = (244, 186, 253)
        btm_color = (96, 1, 112)
        for idx in range(len(PEAKS) - 1):
            left = PEAKS[idx]
            right = PEAKS[idx + 1]
            gradient = color_gradient(top_color, btm_color, ceil((right - left) / 2) + 1)
            for offset, color in enumerate(gradient):
                self[left + offset] = color
                self[right - offset] = color
        self.write()

    def square_effect(self):
        WALLS = [0, 6, 61, 129, 149]
        COLORS = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
        ]

        for idx in range(len(WALLS) - 1):
            left = WALLS[idx]
            right = WALLS[idx + 1]
            color = COLORS[idx]
            for i in range(left, right + 1):
                self[i] = color
        self.write()
