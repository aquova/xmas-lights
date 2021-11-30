from paho.mqtt.client import Client
import board, neopixel
import multiprocessing, time
import effects

GPIO_PIN = board.D18
ORDER = neopixel.RGB
BRIGHTNESS = 0.15

POWER_TOPIC = "bedroom/lights/christmas/switch"
COLOR_TOPIC = "bedroom/lights/christmas/color"
EFFECT_TOPIC = "bedroom/lights/christmas/effects"

class Lights:
    def __init__(self):
        self.last_color = (255, 255, 255)
        self.powered = False
        self.effect = "fill"
        self.effect_process = None

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

    def set_effect(self, effect, process):
        self.effect = effect
        if self.effect_process:
            self.effect_process.terminate()
            # Block until process is really dead
            while self.effect_process.is_alive():
                time.sleep(0.1)
            self.effect_process = None

        if process:
            self.effect_process = process
            self.effect_process.start()

    def get_effect(self):
        return self.effect

xmas_state = Lights()

client = Client(client_id = "Christmas_Lights")
pixels = neopixel.NeoPixel(GPIO_PIN, effects.NUM_BULBS, brightness=BRIGHTNESS, pixel_order=ORDER)

def restore():
    effect = xmas_state.get_effect()
    parse_effect(effect)

def parse_effect(effect_str):
    effect_thread = None
    if effect_str == "fill":
        pixels.fill(xmas_state.get_last_color())
    elif effect_str == "rainbow":
        effects.rainbow_effect(pixels)
    elif effect_str == "classic":
        effects.classic_effect(pixels)
    elif effect_str == "christmas":
        effects.christmas_effect(pixels)
    elif effect_str == "cycle":
        effect_thread = multiprocessing.Process(target=effects.cycle_effect, args=(pixels,))
    elif effect_str == "mountain":
        effects.mountain_effect(pixels)
    xmas_state.set_effect(effect_str, effect_thread)

def on_message(client, userdata, message):
    topic = message.topic
    command = message.payload.decode()

    if topic == POWER_TOPIC:
        if command == "OFF":
            xmas_state.set_powered(False)
            effects.clear(pixels)
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
        parse_effect(command)

client.on_message = on_message
client.connect("jupiter.lan")
client.subscribe("bedroom/lights/christmas/#")
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
