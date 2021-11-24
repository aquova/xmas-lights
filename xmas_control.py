from paho.mqtt.client import Client
import board, neopixel
import math, time

NUM_BULBS = 150
GPIO_PIN = board.D18
ORDER = neopixel.RGB
BRIGHTNESS = 0.15

RGB_SIZE = 255 * 6
STEP_SIZE = math.floor(RGB_SIZE / NUM_BULBS)

POWER_TOPIC = "bedroom/lights/christmas/switch"
COLOR_TOPIC = "bedroom/lights/christmas/color"
EFFECT_TOPIC = "bedroom/lights/christmas/effects"

class Lights:
    def __init__(self):
        self.last_color = (255, 255, 255)
        self.powered = False
        self.effect_running = False

    def is_powered(self):
        return self.powered

    def set_powered(self, p):
        self.powered = p

    def format_powered_state(self):
        return "ON" if self.powered else "OFF"

    def set_color(self, c):
        self.last_color = c

    def get_last_color(self):
        return self.last_color

    def format_color_state(self):
        return f"{self.last_color[0]},{self.last_color[1]},{self.last_color[2]}"

    def set_effect(self, is_running):
        self.effect_running = is_running

    def is_effect_running(self):
        return self.effect_running

xmas_state = Lights()

client = Client(client_id = "Christmas_Lights")
pixels = neopixel.NeoPixel(GPIO_PIN, NUM_BULBS, brightness=BRIGHTNESS, pixel_order=ORDER)

def on_message(client, userdata, message):
    topic = message.topic
    command = message.payload.decode()

    if topic == POWER_TOPIC:
        if command == "OFF":
            xmas_state.set_powered(False)
            clear()
        elif command == "ON":
            if not xmas_state.is_powered():
                restore()
            xmas_state.set_powered(True)
    elif topic == COLOR_TOPIC:
        rgb = command.split(",")
        color = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        xmas_state.set_color(color)
        pixels.fill(color)
    elif topic == EFFECT_TOPIC:
        if command == "fill":
            restore()
        elif command == "rainbow":
            rainbow_effect()

def clear():
    pixels.fill((0, 0, 0))

def restore():
    pixels.fill(xmas_state.get_last_color())

def rainbow_effect():
    for i, (r, g, b) in enumerate(rainbow_gradient()):
        if i == NUM_BULBS:
            break
        pixels[i] = (r, g, b)

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

client.on_message = on_message
client.connect("jupiter.lan")
client.subscribe("bedroom/lights/christmas/#")
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
