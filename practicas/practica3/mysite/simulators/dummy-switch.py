import paho.mqtt.client as mqtt
import time
import random
import argparse
import sys

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(f"iot/devices/{userdata['device_id']}/command")

def on_message(client, userdata, msg):
    print(f"Received command: {msg.payload.decode()}")
    if random.random() < userdata['probability']:
        print("Simulating failure in processing the command.")
    else:
        state = msg.payload.decode()
        client.publish(f"iot/devices/{userdata['device_id']}/state", state)
        print(f"State updated to {state}")

def main(host, port, probability, device_id):
    client = mqtt.Client(userdata={'device_id': device_id, 'probability': probability})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, 60)
    client.loop_start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dummy Switch Simulator')
    parser.add_argument('--host', default='redes2.ii.uam.es', help='MQTT broker host')
    parser.add_argument('-p', '--port', default=1883, type=int, help='MQTT broker port')
    parser.add_argument('-P', '--probability', default=0.3, type=float, help='Probability of failure to process a command')
    parser.add_argument('id', help='Device ID')
    
    args = parser.parse_args()

    main(args.host, args.port, args.probability, args.id)
