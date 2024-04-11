import paho.mqtt.client as mqtt
import sys
import time
import random

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("home/climate/boiler_switch/set")

def on_message(client, userdata, msg):
    if msg.topic == "home/climate/boiler_switch/set":
        print(f"Switch state changed to {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

host = sys.argv[sys.argv.index("--host") + 1] if "--host" in sys.argv else "mqtt.eclipse.org"
port = int(sys.argv[sys.argv.index("-p") + 1]) if "-p" in sys.argv else 1883
probability = float(sys.argv[sys.argv.index("-P") + 1]) if "-P" in sys.argv else 0.3
device_id = sys.argv[-1]

client.connect(host, port, 60)

# Simulate initial state
initial_state = "ON" if random.random() > 0.5 else "OFF"
client.publish("home/climate/boiler_switch", initial_state)

client.loop_start()

while True:
    time.sleep(10)
    # Simulate state change based on probability
    if random.random() < probability:
        new_state = "OFF" if initial_state == "ON" else "ON"
        client.publish("home/climate/boiler_switch", new_state)
        initial_state = new_state
