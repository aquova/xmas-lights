import network
import time
from umqtt import MQTTClient
from lights import Lights

WIFI_NAME = "WIFI NAME"
WIFI_PASS = "PASSWORD"
MQTT_SERVER = "SERVER NAME"

MQTT_TOPIC = "bedroom/lights/christmas/#"
POWER_TOPIC = b"bedroom/lights/christmas/switch"
COLOR_TOPIC = b"bedroom/lights/christmas/color"
EFFECT_TOPIC = b"bedroom/lights/christmas/effects"

STATUS_DELAY = 30 # In seconds
STATUS_TOPIC = b"bedroom/lights/christmas/state"

GPIO_PIN = machine.Pin(0)

def connect_wifi():
    wlan.active(True)
    wlan.connect(WIFI_NAME, WIFI_PASS)

    print("Connecting to Wi-Fi...")
    time.sleep(10)

def connect_mqtt():
    client = MQTTClient('xmas_lights', MQTT_SERVER, keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    return client

def reconnect():
    print("Failed to connect to the MQTT broker. Reconnecting.")
    time.sleep(5)
    machine.reset()

def on_message(topic, msg):
    parsed = False
    if topic == POWER_TOPIC:
        parsed = True
        if msg == b"OFF" and lights.is_powered():
            lights.set_powered(False)
            lights.fill((0, 0, 0))
        elif msg == b"ON" and not lights.is_powered():
            lights.set_powered(True)
            parse_effect(lights.get_effect())
    elif topic == COLOR_TOPIC:
        parsed = True
        color = eval(msg)
        lights.set_color(color)
        lights.fill(color)
    elif topic == EFFECT_TOPIC:
        parsed = True
        parse_effect(msg)

    if parsed:
        client.publish(STATUS_TOPIC, "ON" if lights.is_powered() else "OFF")

def parse_effect(effect):
    # I'm not even 100% sure why I need this.
    if type(effect) is bytes:
        effect = effect.decode()
    if effect == "fill":
        lights.fill(lights.get_last_color())
    elif effect == "rainbow":
        lights.rainbow_effect()
    elif effect == "classic":
        lights.classic_effect()
    elif effect == "christmas":
        lights.christmas_effect()
    elif effect == "mountain":
        lights.mountain_effect()
    elif effect == "square":
        lights.square_effect()
    lights.set_effect(effect)

if __name__ == "__main__":
    wlan = network.WLAN(network.STA_IF)
    connect_wifi()
    try:
        client = connect_mqtt()
        print("Connected to MQTT broker")
    except OSError as e:
        reconnect()

    lights = Lights(GPIO_PIN)
    status_time = time.time()
    while True:
        current_time = time.time()
        if current_time - status_time > STATUS_DELAY:
            status_time = current_time
            client.publish(STATUS_TOPIC, "ON" if lights.is_powered() else "OFF")

        if not wlan.isconnected():
            connect_wifi()
            client = connect_mqtt()
        try:
            client.subscribe(MQTT_TOPIC)
        except OSError:
            client.disconnect()
            client = connect_mqtt()

        time.sleep(1)
